import Combine
import Foundation

/// Control of Terminal windows. Faked in tests.
protocol TerminalWindows {
    /// Runs the executable launcher script in a new window, minimizes it and returns its window ID.
    func open(script: URL) throws -> Int
    func bringForward(_ window: Int) throws
    func minimize(_ window: Int) throws
    func exists(_ window: Int) -> Bool
}

/// One Claude Code session started by KR in its own Terminal window.
final class ClaudeSession {
    enum State: Equatable { case working, waiting(String), ended }

    let task: String
    let repository: URL
    let directory: URL
    let window: Int
    private(set) var state = State.working
    private let terminal: TerminalWindows
    private let alert: (_ task: String, _ id: String) -> Void
    private var handled = Set<String>()
    private var consumed = 0

    init(task: String, repository: URL, directory: URL, window: Int, terminal: TerminalWindows,
         alert: @escaping (_ task: String, _ id: String) -> Void) {
        self.task = task
        self.repository = repository
        self.directory = directory
        self.window = window
        self.terminal = terminal
        self.alert = alert
    }

    /// Reads new signals, then checks that the window still exists. Only this session's window is touched.
    func poll() {
        guard state != .ended else { return }
        for line in newLines() { apply(line) }
        if state != .ended && !terminal.exists(window) { state = .ended }
    }

    private func newLines() -> [String] {
        guard let data = try? Data(contentsOf: directory.appendingPathComponent("signals.jsonl")) else { return [] }
        var lines = String(decoding: data, as: UTF8.self).components(separatedBy: "\n")
        lines.removeLast()  // empty after the last newline, or a line still being written
        let fresh = Array(lines.dropFirst(consumed))
        consumed = lines.count
        return fresh
    }

    private func apply(_ line: String) {
        guard state != .ended,
              let object = try? JSONSerialization.jsonObject(with: Data(line.utf8)) as? [String: Any],
              let event = object["event"] as? String else { return }
        switch event {
        case "waiting":
            // Once per intervention: a repeated ID is ignored, even after the work resumed.
            guard let id = object["id"] as? String, handled.insert(id).inserted else { return }
            state = .waiting(id)
            try? terminal.bringForward(window)
            alert(task, id)
        case "resumed":
            guard case .waiting = state else { return }
            try? terminal.minimize(window)
            state = .working
        case "ended":
            state = .ended
        default:
            return
        }
    }
}

enum ClaudeLaunch {
    static func quote(_ text: String) -> String { "'" + text.replacingOccurrences(of: "'", with: "'\\''") + "'" }

    static func protocolText(signalTool: URL) -> String {
        let tool = "python3 " + quote(signalTool.path)
        return """
        You run in a Terminal window that Kanban Rememory Runner keeps minimized while you work. \
        Tell it explicitly when you need the user:
        - Before you ask the user a question or wait for a decision, run `\(tool) waiting --id ID` \
        with a new unique ID for that question (for example q1, q2), then ask your question in this session.
        - If the answer is unclear and you ask for clarification, do not signal again and do not signal that you resumed.
        - Only after you have the answer and continue working, run `\(tool) resumed`.
        - Never signal because a command is slow or because you are thinking. Signal only when you need the user.
        """
    }

    /// Script that the Terminal window runs. It records the end of the session when it exits.
    static func script(repository: URL, directory: URL, claude: URL) -> String {
        """
        #!/bin/bash
        cd \(quote(repository.path)) || exit 1
        export KRR_SESSION_DIR=\(quote(directory.path))
        trap 'printf "{\\"event\\":\\"ended\\"}\\n" >> "$KRR_SESSION_DIR/signals.jsonl"' EXIT
        \(quote(claude.path)) --append-system-prompt "$(cat \(quote(directory.appendingPathComponent("protocol.txt").path)))" \
        "$(cat \(quote(directory.appendingPathComponent("task.txt").path)))"

        """
    }

    /// Writes the session files. Returns the executable launcher script.
    static func prepare(task: String, repository: URL, claude: URL, signalTool: URL, in directory: URL) throws -> URL {
        try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
        try task.write(to: directory.appendingPathComponent("task.txt"), atomically: true, encoding: .utf8)
        try protocolText(signalTool: signalTool)
            .write(to: directory.appendingPathComponent("protocol.txt"), atomically: true, encoding: .utf8)
        let launcher = directory.appendingPathComponent("launch.sh")
        try script(repository: repository, directory: directory, claude: claude)
            .write(to: launcher, atomically: true, encoding: .utf8)
        try FileManager.default.setAttributes([.posixPermissions: 0o700], ofItemAtPath: launcher.path)
        return launcher
    }

    /// Arguments of the Telegram attention alert, through the project's own setup wrapper.
    static func alertArguments(repository: URL, task: String, id: String) -> [String] {
        [repository.appendingPathComponent("agents/tools/configure-telegram.py").path, "run", "--send", "--",
         "attention", "--task", task, "--id", id,
         "--text", "Claude Code is waiting for your answer in its Terminal window.",
         "--chat-name", "Claude Code · Terminal · " + task]
    }
}

/// Terminal control through AppleScript. KR needs the macOS Automation permission for Terminal.
struct TerminalApp: TerminalWindows {
    private func run(_ source: String) throws -> NSAppleEventDescriptor {
        var failure: NSDictionary?
        let result = NSAppleScript(source: source)?.executeAndReturnError(&failure)
        guard let result else {
            let message = failure?[NSAppleScript.errorMessage] as? String ?? "AppleScript failed."
            throw WatcherError(message: "Cannot control Terminal: \(message)")
        }
        return result
    }

    private func literal(_ text: String) -> String {
        "\"" + text.replacingOccurrences(of: "\\", with: "\\\\").replacingOccurrences(of: "\"", with: "\\\"") + "\""
    }

    func open(script: URL) throws -> Int {
        // The window created by do script is the frontmost one.
        let result = try run("""
        tell application "Terminal"
            do script \(literal(script.path))
            set created to id of window 1
            set miniaturized of window id created to true
            return created
        end tell
        """)
        return Int(result.int32Value)
    }

    func bringForward(_ window: Int) throws {
        _ = try run("""
        tell application "Terminal"
            set miniaturized of window id \(window) to false
            set index of window id \(window) to 1
            activate
        end tell
        """)
    }

    func minimize(_ window: Int) throws {
        _ = try run("tell application \"Terminal\" to set miniaturized of window id \(window) to true")
    }

    func exists(_ window: Int) -> Bool {
        // The running check keeps AppleScript from launching Terminal again after the user quit it.
        let source = """
        if application "Terminal" is running then
            tell application "Terminal" to return exists window id \(window)
        end if
        return false
        """
        return (try? run(source).booleanValue) ?? true
    }
}

extension ClaudeLaunch {
    static func findClaude() -> URL? {
        let home = FileManager.default.homeDirectoryForCurrentUser.path
        let paths = (ProcessInfo.processInfo.environment["PATH"] ?? "").split(separator: ":").map(String.init)
        return (paths + [home + "/.local/bin", home + "/.npm-global/bin", "/opt/homebrew/bin", "/usr/local/bin", "/usr/bin"])
            .filter { $0.hasPrefix("/") }.map { URL(fileURLWithPath: $0 + "/claude") }
            .first { FileManager.default.isExecutableFile(atPath: $0.path) }
    }
}

/// The sessions KR started, polled once a second. They are not restored after KR quits.
final class SessionStore: ObservableObject {
    struct Row: Identifiable, Equatable {
        let id: UUID
        let task: String
        let state: ClaudeSession.State
    }

    @Published private(set) var rows: [Row] = []
    private var sessions: [(UUID, ClaudeSession)] = []
    private var timer: Timer?
    private let terminal: TerminalWindows
    private let root: URL

    init(terminal: TerminalWindows = TerminalApp(), root: URL = ManagedWatchers.records.deletingLastPathComponent()
            .appendingPathComponent("Sessions")) {
        self.terminal = terminal
        self.root = root
    }

    func start(task: String, repository: URL) throws {
        let tools = repository.appendingPathComponent("agents/tools")
        let signal = tools.appendingPathComponent("krr-signal.py")
        guard FileManager.default.fileExists(atPath: signal.path),
              FileManager.default.fileExists(atPath: tools.appendingPathComponent("configure-telegram.py").path) else {
            throw WatcherError(message: "Install the Kanban Rememory tools in this repository: agents/tools/krr-signal.py and configure-telegram.py are required.")
        }
        guard let claude = ClaudeLaunch.findClaude() else { throw WatcherError(message: "No claude executable detected.") }
        let id = UUID()
        let directory = root.appendingPathComponent(id.uuidString)
        let launcher = try ClaudeLaunch.prepare(task: task, repository: repository, claude: claude, signalTool: signal, in: directory)
        let window = try terminal.open(script: launcher)
        let session = ClaudeSession(task: task, repository: repository, directory: directory, window: window,
                                    terminal: terminal) { task, ident in
            // Off the main thread; a disabled or failing Telegram never matters to the window.
            DispatchQueue.global().async {
                let process = Process()
                process.executableURL = URL(fileURLWithPath: "/usr/bin/python3")
                process.arguments = ["-I"] + ClaudeLaunch.alertArguments(repository: repository, task: task, id: ident)
                process.currentDirectoryURL = repository
                process.standardOutput = FileHandle.nullDevice
                process.standardError = FileHandle.nullDevice
                try? process.run()
                process.waitUntilExit()
            }
        }
        sessions.append((id, session))
        publish()
        if timer == nil {
            timer = Timer.scheduledTimer(withTimeInterval: 1, repeats: true) { [weak self] _ in self?.poll() }
        }
    }

    private func poll() {
        sessions.forEach { $0.1.poll() }
        publish()
    }

    private func publish() {
        let current = sessions.map { Row(id: $0.0, task: $0.1.task, state: $0.1.state) }
        if current != rows { rows = current }
    }
}
