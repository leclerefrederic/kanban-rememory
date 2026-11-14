import Foundation

enum RepositoryPreflight {
    @discardableResult
    static func check(_ selectedDirectory: URL, validator: URL, requiresBatchLayout: Bool = true,
                      resolveRoot: Bool = false) throws -> URL {
        let process = Process()
        let output = Pipe()
        process.executableURL = URL(fileURLWithPath: "/usr/bin/git")
        process.arguments = ["-C", selectedDirectory.path, "rev-parse", "--show-toplevel"]
        process.standardOutput = output
        process.standardError = FileHandle.nullDevice
        try process.run()
        let data = output.fileHandleForReading.readDataToEndOfFile()
        process.waitUntilExit()
        guard process.terminationStatus == 0 else {
            throw WatcherError(message: "Select a Git worktree.")
        }
        let path = String(decoding: data, as: UTF8.self).trimmingCharacters(in: .newlines)
        let directory = URL(fileURLWithPath: path, isDirectory: true).resolvingSymlinksInPath()
        guard resolveRoot || directory.path == selectedDirectory.resolvingSymlinksInPath().path else {
            throw WatcherError(message: "Select the repository root: \(path)")
        }
        let board = directory.appendingPathComponent("project/kanban", isDirectory: true)
        let configuration = board.appendingPathComponent("workflow.json")
        guard FileManager.default.fileExists(atPath: directory.appendingPathComponent("AGENTS.md").path),
              let data = try? Data(contentsOf: configuration),
              let workflow = try? JSONDecoder().decode(Workflow.self, from: data),
              !workflow.stages.isEmpty else {
            throw WatcherError(message: "Set up Kanban Rememory and verify AGENTS.md and project/kanban/workflow.json.")
        }
        for stage in workflow.stages {
            var isDirectory: ObjCBool = false
            guard stage.range(of: #"^[a-z0-9][a-z0-9-]*$"#, options: .regularExpression) != nil,
                  FileManager.default.fileExists(atPath: board.appendingPathComponent(stage).path, isDirectory: &isDirectory),
                  isDirectory.boolValue else {
                throw WatcherError(message: "Check the configured stage directory: \(stage)")
            }
        }
        if requiresBatchLayout {
            for path in ["project/specs/draft", "project/specs/ready", "project/specs/approved", "project/batches"] {
                var isDirectory: ObjCBool = false
                guard FileManager.default.fileExists(atPath: directory.appendingPathComponent(path).path,
                                                     isDirectory: &isDirectory), isDirectory.boolValue else {
                    throw WatcherError(message: "Set up the required Batch directory: \(path)")
                }
            }
        }

        guard FileManager.default.isReadableFile(atPath: validator.path) else {
            throw WatcherError(message: "Cannot read the bundled validator at \(validator.path).")
        }
        let validation = Process()
        let diagnostics = Pipe()
        validation.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
        validation.arguments = ["-I", "-B", "-c",
            "import runpy, sys; script = sys.argv.pop(1); sys.path.insert(0, sys.argv.pop(1)); runpy.run_path(script, run_name='__main__')",
            validator.path, validator.deletingLastPathComponent().path, "validate"]
        validation.environment = ["KRR_VALIDATION_ROOT": directory.path, "PATH": "/usr/bin:/bin",
                                  "GIT_OPTIONAL_LOCKS": "0"]
        validation.standardOutput = diagnostics
        validation.standardError = diagnostics
        try validation.run()
        let details = diagnostics.fileHandleForReading.readDataToEndOfFile()
        validation.waitUntilExit()
        guard validation.terminationStatus == 0 else {
            throw WatcherError(message: String(decoding: details, as: UTF8.self))
        }

        return directory
    }

    private struct Workflow: Decodable {
        let stages: [String]
    }
}
