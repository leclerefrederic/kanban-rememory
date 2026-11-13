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
    @AppStorage("appearance") private var appearance = "System"
    @NSApplicationDelegateAdaptor(RunnerDelegate.self) private var delegate
    var body: some Scene {
        WindowGroup("Kanban Rememory Runner") { WatcherView().preferredColorScheme(appearance == "System" ? nil : appearance == "Dark" ? .dark : .light) }
    }
}

private struct WatcherProfile: Codable {
    let name: String
    let icon: String
}

struct WatcherView: View {
    @State private var watchers: [Watcher] = []
    @State private var selection: URL?
    @State private var disabledInstallations: Set<URL> = []
    @State private var statuses: [URL: ServiceStatus] = [:]
    @State private var checkedRepository: URL?
    @State private var checkingRepository = false
    @State private var creating = false
    @State private var engine = "codex"
    @State private var executable = ""
    @AppStorage("appearance") private var appearance = "System"
    @AppStorage("watcher-profiles") private var storedProfiles = Data()
    @State private var profiles: [String: WatcherProfile] = [:]
    @State private var watcherName = ""
    @State private var icon = "folder"
    @State private var settings = false
    @State private var details = false
    private let icons = ["folder", "chevron.left.forwardslash.chevron.right", "doc.text", "server.rack", "terminal", "gearshape"]
    @State private var editing = false
    @State private var deleting = false
    @State private var seconds = ""
    @State private var message = ""
    @State private var failed = false
    @AppStorage("watcher-history") private var storedHistory = Data()
    @State private var history: [String: RunHistory] = [:]

    private var selected: Watcher? { watchers.first { $0.id == selection } }

    var body: some View {
        List(watchers) { watcher in
            HStack(spacing: 12) {
                Image(systemName: profiles[watcher.label]?.icon ?? "folder")
                    .frame(width: 24)
                    .foregroundStyle(.teal)
                    .accessibilityHidden(true)
                VStack(alignment: .leading, spacing: 3) {
                    Text(displayName(watcher)).font(.headline)
                    Text("\(watcher.engine) · \(state(watcher))").foregroundStyle(.secondary)
                }
                Spacer()
                if state(watcher) == "Ready" {
                    Button("Run Now") { perform { try run(watcher) } }
                } else if state(watcher) == "Disabled" && watcher.editable {
                    Button("Activate") { perform { try ManagedWatchers.activate(watcher) } }
                } else if state(watcher) == "Running" {
                    ProgressView().controlSize(.small).accessibilityLabel("Running")
                }
                Menu {
                    Button("Details") { selection = watcher.id; details = true }
                    if isManaged(watcher) {
                        Button("Edit Watcher") {
                            selection = watcher.id
                            watcherName = displayName(watcher)
                            icon = profiles[watcher.label]?.icon ?? "folder"
                            seconds = watcher.interval.map(String.init) ?? ""
                            editing = true
                        }
                    }
                    if ManagedWatchers.installedAndOwned(watcher) && live {
                        if disabledInstallations.contains(watcher.id) {
                            Button("Finish Deactivation") {
                                perform { _ = try ManagedWatchers.deactivate(watcher) }
                            }.disabled(statuses[watcher.id]?.active != false)
                        } else {
                            Button("Deactivate") { perform {
                                try ManagedWatchers.requestDeactivation(watcher)
                                if try !LaunchAgents.status(watcher).active {
                                    _ = try ManagedWatchers.deactivate(watcher)
                                }
                            }}
                        }
                    }
                    if watcher.editable {
                        Button("Delete Watcher", role: .destructive) { selection = watcher.id; deleting = true }
                    }
                } label: {
                    Image(systemName: "ellipsis").accessibilityLabel("Watcher actions")
                }
                .menuIndicator(.hidden)
                .fixedSize()
            }.padding(.vertical, 7)
        }
        .overlay {
            if watchers.isEmpty { Text("No watchers").foregroundStyle(.secondary) }
        }
        .navigationTitle("Watchers")
        .toolbar {
            Button(action: chooseRepository) { Label("New Watcher", systemImage: "plus") }
                .disabled(checkingRepository || !live)
            Button { settings.toggle() } label: { Label("Settings", systemImage: "gearshape") }
                .popover(isPresented: $settings) {
                    Picker("Appearance", selection: $appearance) {
                        ForEach(["System", "Light", "Dark"], id: \.self) { Text($0) }
                    }.pickerStyle(.segmented).padding().frame(width: 320)
                }
        }
        .sheet(isPresented: $details) {
            if let watcher = selected {
                Form {
                    LabeledContent("Service label", value: watcher.label)
                    LabeledContent("Executable", value: watcher.executable)
                    LabeledContent("Repository", value: watcher.plist["WorkingDirectory"] as? String ?? "Unknown")
                    LabeledContent("Trigger", value: watcher.trigger)
                    LabeledContent("Last run", value: history[watcher.label]?.latest?.date.formatted() ?? "Unknown")
                    LabeledContent("Last result", value: history[watcher.label]?.latest?.result ?? "Unknown")
                    ForEach(history[watcher.label]?.events ?? []) { event in
                        LabeledContent("\(event.result) (\(event.count))", value: event.date.formatted())
                    }
                    Button("Done") { details = false }
                }.formStyle(.grouped).frame(width: 480, height: 320)
            }
        }
        .sheet(isPresented: $editing) {
            if let watcher = selected {
                Form {
                    TextField("Watcher Name", text: $watcherName)
                    iconPicker
                    if watcher.editable { TextField("Interval in seconds", text: $seconds) }
                    HStack {
                        Button("Cancel") { editing = false }
                        Button("Save") {
                            editing = false
                            perform {
                                if watcher.editable, let interval = Int(seconds), interval != watcher.interval {
                                    try LaunchAgents.change(watcher, interval: interval)
                                }
                                saveProfile(watcher.label)
                            }
                        }.disabled(cleanName.isEmpty || (watcher.editable && (Int(seconds) ?? 0) <= 0))
                    }
                }.formStyle(.grouped).frame(width: 380, height: 220)
            }
        }
        .confirmationDialog("Delete this watcher?", isPresented: $deleting) {
            Button("Delete Watcher", role: .destructive) {
                guard let watcher = selected else { return }
                perform {
                    try LaunchAgents.change(watcher, interval: nil)
                    profiles.removeValue(forKey: watcher.label)
                    persistProfiles()
                }
            }
        }
        .sheet(isPresented: $creating) {
            if let repository = checkedRepository {
                Form {
                    LabeledContent("Repository", value: repository.path)
                    Picker("Engine", selection: $engine) {
                        Text("Codex").tag("codex")
                        Text("Claude Code").tag("claude")
                    }
                    TextField("Absolute executable path", text: $executable)
                    TextField("Interval in seconds", text: $seconds)
                    TextField("Watcher Name", text: $watcherName)
                    iconPicker
                    Text("The watcher is created disabled. Activation schedules a status check.")
                    HStack {
                        Button("Cancel") { creating = false }
                        Button("Create Watcher") {
                            guard let interval = Int(seconds) else { return }
                            creating = false
                            Task { @MainActor in
                                do {
                                    try await verify(repository)
                                    perform {
                                        let file = try ManagedWatchers.allocateLabel { label in
                                            guard try LaunchAgents.isAvailable(label) else { return nil }
                                            do {
                                                return try ManagedWatchers.create(
                                                    repository: repository, executable: URL(fileURLWithPath: executable),
                                                    engine: engine, interval: interval, label: label,
                                                    agents: ManagedWatchers.inactive, records: ManagedWatchers.records
                                                ) {}
                                            } catch let error as CocoaError where error.code == .fileWriteFileExists {
                                                return nil
                                            }
                                        }
                                        saveProfile(file.deletingPathExtension().lastPathComponent)
                                    }
                                } catch {
                                    message = error.localizedDescription
                                    failed = true
                                }
                            }
                        }.disabled((Int(seconds) ?? 0) <= 0 || !executable.hasPrefix("/") || cleanName.isEmpty)
                    }
                }.formStyle(.grouped).frame(width: 560, height: 380)
            }
        }
        .frame(minWidth: 380, minHeight: 250)
        .task {
            profiles = (try? JSONDecoder().decode([String: WatcherProfile].self, from: storedProfiles)) ?? [:]
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

    private var live: Bool { ProcessInfo.processInfo.environment["KRR_FIXTURE_DIRECTORY"] == nil }
    private var cleanName: String { watcherName.trimmingCharacters(in: .whitespacesAndNewlines) }

    private var iconPicker: some View {
        Picker("Icon", selection: $icon) {
            ForEach(Array(zip(icons, ["Folder", "Code", "Document", "Server", "Terminal", "Tools"])), id: \.0) {
                Label($0.1, systemImage: $0.0).tag($0.0)
            }
        }
    }

    private func displayName(_ watcher: Watcher) -> String {
        profiles[watcher.label]?.name ?? watcher.label
    }

    private func isManaged(_ watcher: Watcher) -> Bool {
        live && (watcher.editable || ManagedWatchers.installedAndOwned(watcher))
    }

    private func state(_ watcher: Watcher) -> String {
        if disabledInstallations.contains(watcher.id) { return "Deactivating" }
        if watcher.editable { return "Disabled" }
        guard let status = statuses[watcher.id] else { return "Unknown" }
        if !status.loaded { return "Not loaded" }
        return status.active ? "Running" : "Ready"
    }

    private func run(_ watcher: Watcher) throws {
        let status = try LaunchAgents.status(watcher)
        guard status.loaded, !status.active, try !LaunchAgents.isDisabled(watcher) else {
            throw WatcherError(message: "The watcher must be loaded, enabled and idle.")
        }
        try LaunchAgents.checked(["kickstart", "\(LaunchAgents.domain)/\(watcher.label)"])
    }

    private func saveProfile(_ label: String) {
        profiles[label] = WatcherProfile(name: cleanName, icon: icon)
        persistProfiles()
    }

    private func persistProfiles() {
        if let bytes = try? JSONEncoder().encode(profiles) { storedProfiles = bytes }
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
                    watcherName = directory.lastPathComponent
                    icon = "folder"
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
        disabledInstallations = Set(watchers.filter {
            fixture == nil && ManagedWatchers.installedAndOwned($0) && (try? LaunchAgents.isDisabled($0)) == true
        }.map(\.id))
        statuses = refreshed
        if let data = try? JSONEncoder().encode(history), data != storedHistory { storedHistory = data }
    }

    private func perform(_ operation: () throws -> Void) {
        do { try operation(); try refresh() }
        catch { message = error.localizedDescription; failed = true }
    }
}
