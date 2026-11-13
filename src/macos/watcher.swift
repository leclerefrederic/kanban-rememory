import AppKit
import SwiftUI

struct Watcher: Identifiable {
    let file: URL
    let label: String
    let engine: String
    let executable: String
    let plist: [String: Any]
    let editable: Bool
    var id: URL { file }
    var interval: Int? { plist["StartInterval"] as? Int }
    var trigger: String {
        if let interval { return "Every \(interval) seconds" }
        if let paths = plist["WatchPaths"] as? [String] { return paths.joined(separator: ", ") }
        return "Unknown"
    }
}

enum LaunchAgents {
    static var directory: URL {
        FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent("Library/LaunchAgents")
    }
    static var domain: String { "gui/\(getuid())" }

    static func discover(in directory: URL) throws -> [Watcher] {
        let files = try FileManager.default.contentsOfDirectory(
            at: directory, includingPropertiesForKeys: [.isRegularFileKey, .isSymbolicLinkKey]
        )
        return files.compactMap { file in
            guard file.pathExtension == "plist",
                  let values = try? file.resourceValues(forKeys: [.isRegularFileKey, .isSymbolicLinkKey]),
                  values.isRegularFile == true, values.isSymbolicLink == false,
                  let bytes = try? Data(contentsOf: file),
                  let plist = (try? PropertyListSerialization.propertyList(from: bytes, format: nil)) as? [String: Any],
                  let label = plist["Label"] as? String,
                  !label.isEmpty,
                  label.range(of: #"^[A-Za-z0-9][A-Za-z0-9._-]*$"#, options: .regularExpression) != nil,
                  let executable = plist["Program"] as? String ?? (plist["ProgramArguments"] as? [String])?.first,
                  executable.hasPrefix("/") else { return nil }
            let name = URL(fileURLWithPath: executable).lastPathComponent
            guard let engine = ["codex": "Codex", "claude": "Claude Code"][name] else { return nil }
            return Watcher(file: file, label: label, engine: engine, executable: executable, plist: plist, editable: false)
        }.sorted { $0.label < $1.label }
    }

    static func call(_ arguments: [String]) throws -> (Int32, String) {
        let process = Process()
        let output = Pipe()
        process.executableURL = URL(fileURLWithPath: "/bin/launchctl")
        process.arguments = arguments
        process.standardOutput = output
        process.standardError = output
        try process.run()
        let data = output.fileHandleForReading.readDataToEndOfFile()
        process.waitUntilExit()
        return (process.terminationStatus, String(decoding: data, as: UTF8.self))
    }

    static func checked(_ arguments: [String]) throws {
        let (code, output) = try call(arguments)
        if code != 0 { throw WatcherError(message: output.trimmingCharacters(in: .whitespacesAndNewlines)) }
    }

    static func status(_ watcher: Watcher) throws -> ServiceStatus {
        let (code, output) = try call(["print", "\(domain)/\(watcher.label)"])
        if code == 0 { return ServiceStatus(output) }
        if output.localizedCaseInsensitiveContains("could not find service") { return ServiceStatus("") }
        throw WatcherError(message: output)
    }

    static func change(_ watcher: Watcher, interval: Int?) throws {
        guard let current = try discover(in: directory).first(where: { $0.id == watcher.id }),
              current.editable, NSDictionary(dictionary: current.plist).isEqual(to: watcher.plist) else {
            throw WatcherError(message: "The watcher changed or cannot be managed. Refresh and try again.")
        }
        let original = try Data(contentsOf: watcher.file)
        let service = try status(watcher)
        guard !service.active else { throw WatcherError(message: "Wait for the current run to finish.") }
        var updated = watcher.plist
        if let interval { updated["StartInterval"] = interval }
        let replacement = try interval.map { _ in
            try PropertyListSerialization.data(fromPropertyList: updated, format: .xml, options: 0)
        }
        if service.loaded { try checked(["bootout", "\(domain)/\(watcher.label)"]) }
        do {
            if let replacement {
                try replacement.write(to: watcher.file, options: .atomic)
                if service.loaded { try checked(["bootstrap", domain, watcher.file.path]) }
            } else {
                try FileManager.default.removeItem(at: watcher.file)
            }
        } catch {
            let operationError = error
            do {
                try original.write(to: watcher.file, options: .atomic)
                if service.loaded { try checked(["bootstrap", domain, watcher.file.path]) }
            } catch {
                throw WatcherError(message: "Change failed: \(operationError.localizedDescription). Recovery failed: \(error.localizedDescription)")
            }
            throw operationError
        }
    }
}

struct WatcherError: LocalizedError {
    let message: String
    var errorDescription: String? { message }
}

struct ServiceStatus {
    let loaded: Bool
    let state: String
    let runs: Int?
    let exitCode: Int?

    init(_ output: String) {
        func value(_ key: String) -> String? {
            let prefix = key + " = "
            return output.split(separator: "\n").map {
                $0.trimmingCharacters(in: .whitespaces)
            }.first(where: { $0.hasPrefix(prefix) }).map { String($0.dropFirst(prefix.count)) }
        }
        loaded = !output.isEmpty
        state = value("state") ?? (loaded ? "Unknown" : "Not loaded")
        runs = value("runs").flatMap(Int.init)
        exitCode = value("last exit code").flatMap(Int.init)
    }

    var active: Bool {
        loaded && !["not running", "waiting", "exited"].contains(state)
    }
}

struct RunHistory: Codable {
    struct Event: Identifiable, Codable {
        var id = UUID()
        let result: String
        var date: Date
        var count = 1
    }
    var latest: Event?
    var events: [Event] = []
    var observedRuns: Int?

    mutating func record(_ result: String, significant: Bool, repeatedFailure: Bool, at date: Date = Date()) {
        latest = Event(result: result, date: date)
        guard significant else { return }
        if repeatedFailure, events.first?.result == result {
            events[0].count += 1
            events[0].date = date
        } else {
            events.insert(Event(result: result, date: date), at: 0)
            events = Array(events.prefix(20))
        }
    }
}
