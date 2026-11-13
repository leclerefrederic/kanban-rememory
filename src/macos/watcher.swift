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
            return Watcher(file: file, label: label, engine: engine, executable: executable, plist: plist, editable: directory == ManagedWatchers.inactive && ManagedWatchers.owns(label, file: file, bytes: bytes))
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

    static func isDisabled(_ watcher: Watcher) throws -> Bool {
        let (code, output) = try call(["print-disabled", domain])
        guard code == 0 else { throw WatcherError(message: output) }
        return output.split(separator: "\n").contains {
            let line = $0.trimmingCharacters(in: .whitespaces)
            return line == "\"\(watcher.label)\" => disabled" || line == "\"\(watcher.label)\" => true"
        }
    }

    static func requireAvailable(_ label: String) throws {
        let installed = directory.appendingPathComponent(label + ".plist")
        let (code, output) = try call(["print", "\(domain)/\(label)"])
        guard !FileManager.default.fileExists(atPath: installed.path),
              code != 0, output.localizedCaseInsensitiveContains("could not find service") else {
            throw WatcherError(message: "The label is already in use or cannot be checked.")
        }
    }

    static func status(_ watcher: Watcher) throws -> ServiceStatus {
        let (code, output) = try call(["print", "\(domain)/\(watcher.label)"])
        if code == 0 { return ServiceStatus(output) }
        if output.localizedCaseInsensitiveContains("could not find service") { return ServiceStatus("") }
        throw WatcherError(message: output)
    }

    static func change(_ watcher: Watcher, interval: Int?) throws {
        guard let current = try discover(in: ManagedWatchers.inactive).first(where: { $0.id == watcher.id }),
              current.editable, NSDictionary(dictionary: current.plist).isEqual(to: watcher.plist),
              !(try status(watcher)).loaded else {
            throw WatcherError(message: "Only a verified, disabled watcher can be edited or deleted.")
        }
        let record = ManagedWatchers.records.appendingPathComponent(watcher.file.lastPathComponent)
        let original = try Data(contentsOf: watcher.file)
        if let interval {
            var updated = watcher.plist
            updated["StartInterval"] = interval
            let replacement = try PropertyListSerialization.data(fromPropertyList: updated, format: .xml, options: 0)
            try replacement.write(to: watcher.file, options: .atomic)
            do { try replacement.write(to: record, options: .atomic) }
            catch {
                try original.write(to: watcher.file, options: .atomic)
                throw error
            }
        } else {
            try FileManager.default.removeItem(at: watcher.file)
            try FileManager.default.removeItem(at: record)
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
