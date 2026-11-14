import Foundation

final class FakeTerminal: TerminalWindows {
    var calls: [String] = []
    var alive = true
    func open(script: URL) throws -> Int { calls.append("open"); return 7 }
    func bringForward(_ window: Int) throws { calls.append("front \(window)") }
    func minimize(_ window: Int) throws { calls.append("min \(window)") }
    func exists(_ window: Int) -> Bool { alive }
}

var failures = 0
func check(_ condition: Bool, _ name: String, line: Int = #line) {
    if !condition { failures += 1; print("FAIL line \(line): \(name)") }
}

let directory = FileManager.default.temporaryDirectory.appendingPathComponent("krr-test-" + UUID().uuidString)
try FileManager.default.createDirectory(at: directory, withIntermediateDirectories: true)
let signals = directory.appendingPathComponent("signals.jsonl")
func write(_ text: String) {
    if let handle = try? FileHandle(forWritingTo: signals) {
        handle.seekToEndOfFile(); handle.write(Data(text.utf8)); try? handle.close()
    } else { try? text.write(to: signals, atomically: true, encoding: .utf8) }
}
func waiting(_ id: String) -> String { "{\"event\":\"waiting\",\"id\":\"\(id)\"}\n" }
let resumed = "{\"event\":\"resumed\"}\n"

func makeSession(_ terminal: FakeTerminal, alerts: @escaping (String) -> Void) -> ClaudeSession {
    try? FileManager.default.removeItem(at: signals)
    return ClaudeSession(task: "Export", repository: directory, directory: directory, window: 7, terminal: terminal) { _, id in alerts(id) }
}

// A slow command writes no signal: nothing moves.
do {
    let terminal = FakeTerminal(); var sent: [String] = []
    let session = makeSession(terminal) { sent.append($0) }
    session.poll(); session.poll()
    check(session.state == .working && terminal.calls.isEmpty && sent.isEmpty, "silence changes nothing")
}

// Waiting brings the window forward once with one alert; a repeated signal changes nothing.
do {
    let terminal = FakeTerminal(); var sent: [String] = []
    let session = makeSession(terminal) { sent.append($0) }
    write(waiting("q1")); session.poll()
    check(session.state == .waiting("q1") && terminal.calls == ["front 7"] && sent == ["q1"], "waiting once")
    write(waiting("q1")); session.poll()
    check(terminal.calls == ["front 7"] && sent == ["q1"], "repeated ID ignored")
    // Clarification: still waiting, window stays visible, nothing minimized.
    session.poll()
    check(!terminal.calls.contains("min 7"), "stays visible while unresolved")
    write(resumed); session.poll()
    check(session.state == .working && terminal.calls == ["front 7", "min 7"], "resumed minimizes")
    write(waiting("q1")); session.poll()
    check(sent == ["q1"], "an ID is never alerted twice, even after resume")
    write(resumed + resumed); session.poll()
    check(terminal.calls == ["front 7", "min 7"] && session.state == .working, "resumed only counts after waiting")
}

// A second intervention with a new ID is a new alert.
do {
    let terminal = FakeTerminal(); var sent: [String] = []
    let session = makeSession(terminal) { sent.append($0) }
    write(waiting("q1") + resumed + waiting("q2")); session.poll()
    check(sent == ["q1", "q2"] && session.state == .waiting("q2"), "new ID alerts again")
}

// A partial last line waits for its newline; garbage lines are ignored.
do {
    let terminal = FakeTerminal(); var sent: [String] = []
    let session = makeSession(terminal) { sent.append($0) }
    write("not json\n{\"event\":\"waiting\",\"id\":\"q1\"}"); session.poll()
    check(sent.isEmpty, "partial line is not read")
    write("\n"); session.poll()
    check(sent == ["q1"], "complete line is read")
}

// A closed window ends the session and nothing else is touched afterward.
do {
    let terminal = FakeTerminal(); var sent: [String] = []
    let session = makeSession(terminal) { sent.append($0) }
    write(waiting("q1")); session.poll()
    terminal.alive = false; session.poll()
    check(session.state == .ended, "closed window ends the session")
    write(resumed + waiting("q2")); session.poll()
    check(terminal.calls == ["front 7"] && sent == ["q1"], "no action after the end")
}

// The launcher reports the end of the session.
do {
    let terminal = FakeTerminal(); var sent: [String] = []
    let session = makeSession(terminal) { sent.append($0) }
    write("{\"event\":\"ended\"}\n"); session.poll()
    check(session.state == .ended && terminal.calls.isEmpty, "ended signal")
}

// Launch files: quoting, environment, executable script.
do {
    let repository = URL(fileURLWithPath: "/tmp/it's a repo")
    let script = ClaudeLaunch.script(repository: repository, directory: directory, claude: URL(fileURLWithPath: "/usr/local/bin/claude"))
    check(script.contains("cd '/tmp/it'\\''s a repo' ||"), "repository path quoted")
    check(script.contains("KRR_SESSION_DIR="), "session directory exported")
    check(script.contains("--append-system-prompt"), "protocol appended")
    let launcher = try ClaudeLaunch.prepare(task: "Export it's data", repository: repository,
        claude: URL(fileURLWithPath: "/usr/local/bin/claude"), signalTool: URL(fileURLWithPath: "/r/krr-signal.py"), in: directory)
    let mode = (try FileManager.default.attributesOfItem(atPath: launcher.path)[.posixPermissions] as? Int) ?? 0
    check(mode == 0o700, "launcher is private and executable")
    check((try String(contentsOf: directory.appendingPathComponent("task.txt"))) == "Export it's data", "task written verbatim")
    check((try String(contentsOf: directory.appendingPathComponent("protocol.txt"))).contains("waiting --id"), "protocol written")
    let syntax = Process(); syntax.executableURL = URL(fileURLWithPath: "/bin/bash"); syntax.arguments = ["-n", launcher.path]
    try syntax.run(); syntax.waitUntilExit()
    check(syntax.terminationStatus == 0, "launcher is valid bash")
}

// Alert goes through the project's setup wrapper as an attention alert.
do {
    let arguments = ClaudeLaunch.alertArguments(repository: URL(fileURLWithPath: "/r"), task: "Export", id: "q1")
    check(arguments.prefix(4) == ["/r/agents/tools/configure-telegram.py", "run", "--send", "--"], "wrapper used")
    check(arguments.contains("attention") && arguments.contains("q1"), "attention alert with the intervention ID")
}

try? FileManager.default.removeItem(at: directory)
print(failures == 0 ? "All Swift tests passed." : "\(failures) Swift test(s) failed.")
exit(failures == 0 ? 0 : 1)
