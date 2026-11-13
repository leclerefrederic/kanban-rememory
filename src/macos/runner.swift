import AppKit
import SwiftUI

final class RunnerDelegate: NSObject, NSApplicationDelegate {
    func applicationDidFinishLaunching(_ notification: Notification) {
        if let url = Bundle.main.url(forResource: "app-icon", withExtension: "icns"),
           let icon = NSImage(contentsOf: url) {
            NSApplication.shared.applicationIconImage = icon
        }
    }
}

@main
struct Runner: App {
    @NSApplicationDelegateAdaptor(RunnerDelegate.self) private var delegate
    var body: some Scene {
        WindowGroup("Kanban Rememory Runner") { WatcherView() }
    }
}

struct WatcherView: View {
    @State private var watchers: [Watcher] = []
    @State private var selection: URL?
    @State private var statuses: [URL: ServiceStatus] = [:]
    @State private var checkedRepository: URL?
    @State private var checkingRepository = false
    @State private var creating = false
    @State private var engine = "codex"
    @State private var executable = ""
    @State private var purpose = ""
    @State private var editing = false
    @State private var deleting = false
    @State private var seconds = ""
    @State private var message = ""
    @State private var failed = false
    @AppStorage("watcher-history") private var storedHistory = Data()
    @State private var history: [String: RunHistory] = [:]

    private var selected: Watcher? { watchers.first { $0.id == selection } }

    var body: some View {
        NavigationSplitView {
            List(watchers, selection: $selection) { watcher in
                VStack(alignment: .leading) {
                    Text(watcher.label)
                    Text(watcher.engine).foregroundStyle(.secondary)
                }.tag(watcher.id)
            }.navigationTitle("Watchers").frame(minWidth: 250)
        } detail: {
            if let watcher = selected {
                Form {
                    Section(watcher.label) {
                        LabeledContent("Engine", value: watcher.engine)
                        LabeledContent("Executable", value: watcher.executable)
                        LabeledContent("Working directory", value: watcher.plist["WorkingDirectory"] as? String ?? "Unknown")
                        LabeledContent("Trigger", value: watcher.trigger)
                        LabeledContent("Service state", value: statuses[watcher.id]?.state ?? "Unknown")
                        LabeledContent("Last run", value: history[watcher.label]?.latest?.date.formatted() ?? "Unknown")
                        LabeledContent("Last result", value: history[watcher.label]?.latest?.result ?? "Unknown")
                    }
                    Section("Recent Runs") {
                        ForEach(history[watcher.label]?.events ?? []) { event in
                            LabeledContent(event.count > 1 ? "\(event.result) (\(event.count))" : event.result) {
                                Text(event.date.formatted())
                            }
                        }
                    }
                    if watcher.editable {
                        Button("Delete Watcher", role: .destructive) { deleting = true }
                    } else {
                        Text("Only disabled watchers created by KRR can be edited or deleted.").foregroundStyle(.secondary)
                    }
                }.formStyle(.grouped)
                .toolbar {
                    Button("Run Now") { perform {
                        let status = try LaunchAgents.status(watcher)
                        guard status.loaded && !status.active else {
                            throw WatcherError(message: "The watcher must be loaded and idle.")
                        }
                        try LaunchAgents.checked(["kickstart", "\(LaunchAgents.domain)/\(watcher.label)"])
                    }}.disabled(statuses[watcher.id]?.loaded != true || statuses[watcher.id]?.active != false)
                    if watcher.editable {
                        Button("Activate Watcher") { perform { try ManagedWatchers.activate(watcher) } }
                    }
                    Button("Edit Watcher") {
                        seconds = watcher.interval.map(String.init) ?? ""
                        editing = true
                    }.disabled(!watcher.editable || watcher.interval == nil)
                    Button("Refresh") { perform(refresh) }
                }
                .sheet(isPresented: $editing) {
                    VStack(alignment: .leading, spacing: 16) {
                        Text("Edit Watcher").font(.headline)
                        TextField("Interval in seconds", text: $seconds)
                        HStack {
                            Button("Cancel") { editing = false }
                            Button("Save") {
                                editing = false
                                if let interval = Int(seconds), interval > 0 {
                                    perform { try LaunchAgents.change(watcher, interval: interval) }
                                }
                            }.disabled((Int(seconds) ?? 0) <= 0)
                        }
                    }.padding().frame(width: 320)
                }
                .confirmationDialog("Delete this watcher?", isPresented: $deleting) {
                    Button("Delete Watcher", role: .destructive) {
                        perform { try LaunchAgents.change(watcher, interval: nil) }
                    }
                }
            } else {
                Text("Select a Codex or Claude Code watcher.").foregroundStyle(.secondary)
                    .toolbar { Button("Refresh") { perform(refresh) } }
            }
        }.toolbar {
            Button(action: chooseRepository) { Label("New Watcher", systemImage: "plus") }
                .disabled(checkingRepository)
        }
        .sheet(isPresented: $creating) {
            if let repository = checkedRepository {
                let label = ManagedWatchers.label(for: repository, purpose: purpose)
                Form {
                    LabeledContent("Repository", value: repository.path)
                    Picker("Engine", selection: $engine) {
                        Text("Codex").tag("codex")
                        Text("Claude Code").tag("claude")
                    }
                    TextField("Absolute executable path", text: $executable)
                    TextField("Interval in seconds", text: $seconds)
                    TextField("Purpose suffix (optional)", text: $purpose)
                    LabeledContent("LaunchAgent label", value: label)
                    Text("The watcher is created disabled. Activation schedules a status check.")
                    HStack {
                        Button("Cancel") { creating = false }
                        Button("Create Disabled Watcher") {
                            guard let interval = Int(seconds) else { return }
                            creating = false
                            Task { @MainActor in
                                do {
                                    try await verify(repository)
                                    perform {
                                let file = try ManagedWatchers.create(
                                    repository: repository, executable: URL(fileURLWithPath: executable),
                                    engine: engine, interval: interval, label: label,
                                    agents: ManagedWatchers.inactive, records: ManagedWatchers.records
                                ) {
                                    try LaunchAgents.requireAvailable(label)
                                }
                                        selection = file
                                    }
                                } catch {
                                    message = error.localizedDescription
                                    failed = true
                                }
                            }
                        }.disabled((Int(seconds) ?? 0) <= 0 || !executable.hasPrefix("/"))
                    }
                }.formStyle(.grouped).frame(width: 560, height: 380)
            }
        }
        .frame(minWidth: 770, minHeight: 460)
        .task {
            history = (try? JSONDecoder().decode([String: RunHistory].self, from: storedHistory)) ?? [:]
            perform(refresh)
            while !Task.isCancelled {
                try? await Task.sleep(for: .seconds(15))
                if !Task.isCancelled { try? refresh() }
            }
        }
        .alert("Watcher operation failed", isPresented: $failed) {
            Button("OK", role: .cancel) {}
        } message: { Text(message) }
    }

    private func chooseRepository() {
        guard ProcessInfo.processInfo.environment["KRR_FIXTURE_DIRECTORY"] == nil else { return }
        let panel = NSOpenPanel()
        panel.title = "Select Repository Root"
        panel.canChooseFiles = false
        panel.canChooseDirectories = true
        panel.allowsMultipleSelection = false
        checkingRepository = true
        panel.begin { response in
            guard response == .OK, let directory = panel.url else {
                checkingRepository = false
                return
            }
            Task { @MainActor in
                defer { checkingRepository = false }
                do {
                    try await verify(directory)
                    checkedRepository = directory
                    seconds = "300"
                    purpose = ""
                    executable = ""
                    creating = true
                } catch {
                    message = error.localizedDescription
                    failed = true
                }
            }
        }
    }

    private func verify(_ directory: URL) async throws {
        guard let resources = Bundle.main.resourceURL else {
            throw WatcherError(message: "Open the installed application bundle to access its validator.")
        }
        let validator = resources.appendingPathComponent("validator/manage-kanban-board.py")
        try await Task.detached(priority: .userInitiated) {
            try RepositoryPreflight.check(directory, validator: validator)
        }.value
    }

    private func refresh() throws {
        let fixture = ProcessInfo.processInfo.environment["KRR_FIXTURE_DIRECTORY"]
        let directory = fixture.map { URL(fileURLWithPath: $0, isDirectory: true) } ?? LaunchAgents.directory
        watchers = FileManager.default.fileExists(atPath: directory.path) ? try LaunchAgents.discover(in: directory) : []
        if fixture == nil && FileManager.default.fileExists(atPath: ManagedWatchers.inactive.path) {
            watchers += try LaunchAgents.discover(in: ManagedWatchers.inactive)
        }
        var refreshed: [URL: ServiceStatus] = [:]
        for watcher in watchers where fixture == nil {
            guard let status = try? LaunchAgents.status(watcher) else { continue }
            refreshed[watcher.id] = status
            guard !status.active, let runs = status.runs, runs > 0, let exitCode = status.exitCode else { continue }
            var entry = history[watcher.label] ?? RunHistory()
            guard entry.observedRuns != runs else { continue }
            entry.observedRuns = runs
            entry.record(exitCode == 0 ? "Exited successfully" : "Exit code \(exitCode)",
                         significant: exitCode != 0, repeatedFailure: exitCode != 0)
            history[watcher.label] = entry
        }
        statuses = refreshed
        if let data = try? JSONEncoder().encode(history), data != storedHistory { storedHistory = data }
    }

    private func perform(_ operation: () throws -> Void) {
        do { try operation(); try refresh() }
        catch { message = error.localizedDescription; failed = true }
    }
}
