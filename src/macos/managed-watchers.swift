import Foundation

enum ManagedWatchers {
    static var records: URL {
        FileManager.default.homeDirectoryForCurrentUser
            .appendingPathComponent("Library/Application Support/Kanban Rememory Runner/Watchers")
    }

    static var inactive: URL { records.deletingLastPathComponent().appendingPathComponent("Inactive") }

    static func label(for repository: URL, purpose: String) -> String {
        func slug(_ value: String) -> String {
            value.lowercased().replacingOccurrences(of: "[^a-z0-9]+", with: "-", options: .regularExpression)
                .trimmingCharacters(in: CharacterSet(charactersIn: "-"))
        }
        let suffix = slug(purpose)
        return "kanban.rememory." + slug(repository.lastPathComponent) + (suffix.isEmpty ? "" : "." + suffix)
    }

    static func owns(_ label: String, file: URL, bytes: Data, records: URL = records) -> Bool {
        guard file.lastPathComponent == label + ".plist" else { return false }
        return (try? Data(contentsOf: records.appendingPathComponent(label + ".plist"))) == bytes
    }

    static func create(repository: URL, executable: URL, engine: String, interval: Int, label: String,
                       agents: URL, records: URL, checkCollision: () throws -> Void) throws -> URL {
        guard label.range(of: #"^kanban\.rememory\.[a-z0-9][a-z0-9.-]*$"#, options: .regularExpression) != nil,
              interval > 0,
              ["codex", "claude"].contains(engine), executable.lastPathComponent == engine,
              FileManager.default.isExecutableFile(atPath: executable.path) else {
            throw WatcherError(message: "Choose a valid engine executable, label and interval.")
        }
        try checkCollision()
        let prompt = "Inspect this Kanban Rememory project and summarize its current board status. Do not change files, pick up or close a Batch, or publish anything."
        let arguments = engine == "codex"
            ? ["--ask-for-approval", "never", "exec", "--sandbox", "read-only", prompt]
            : ["-p", "--permission-mode", "plan", "--tools", "", "--", prompt]
        let plist: [String: Any] = [
            "Label": label, "ProgramArguments": [executable.path] + arguments,
            "WorkingDirectory": repository.path, "StartInterval": interval, "RunAtLoad": false,
            "EnvironmentVariables": ["PATH": executable.deletingLastPathComponent().path + ":/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"]
        ]
        let bytes = try PropertyListSerialization.data(fromPropertyList: plist, format: .xml, options: 0)
        for folder in [agents, records] {
            try FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
        }
        let file = agents.appendingPathComponent(label + ".plist")
        let record = records.appendingPathComponent(label + ".plist")
        try bytes.write(to: file, options: .withoutOverwriting)
        do { try bytes.write(to: record, options: .withoutOverwriting) }
        catch {
            if (try? Data(contentsOf: file)) == bytes { try? FileManager.default.removeItem(at: file) }
            throw error
        }
        return file
    }

    static func activate(_ watcher: Watcher) throws {
        let bytes = try Data(contentsOf: watcher.file)
        guard owns(watcher.label, file: watcher.file, bytes: bytes),
              !((try LaunchAgents.status(watcher)).loaded) else {
            throw WatcherError(message: "Only a verified, unloaded watcher can be activated.")
        }
        guard watcher.file.deletingLastPathComponent() == inactive else {
            throw WatcherError(message: "This watcher is already installed. Check its launchd status.")
        }
        try FileManager.default.createDirectory(at: LaunchAgents.directory, withIntermediateDirectories: true)
        let installed = LaunchAgents.directory.appendingPathComponent(watcher.file.lastPathComponent)
        try bytes.write(to: installed, options: .withoutOverwriting)
        do {
            try LaunchAgents.checked(["bootstrap", LaunchAgents.domain, installed.path])
        } catch {
            if (try? Data(contentsOf: installed)) == bytes,
               (try? LaunchAgents.status(watcher).loaded) == false {
                try? FileManager.default.removeItem(at: installed)
            }
            throw error
        }
        try FileManager.default.removeItem(at: watcher.file)
    }
}
