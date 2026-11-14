import AppKit
import SwiftUI

final class RunnerDelegate: NSObject, NSApplicationDelegate {
    private var statusItem: NSStatusItem?
    var openWatchers: (() -> Void)?

    @objc private func showWatchers() {
        NSApp.activate(ignoringOtherApps: true)
        openWatchers?()
    }

    func applicationDidFinishLaunching(_ notification: Notification) {
        if ProcessInfo.processInfo.environment["KRR_FIXTURE_DIRECTORY"] == nil {
            let item = NSStatusBar.system.statusItem(withLength: NSStatusItem.variableLength)
            let mark = NSImage(size: NSSize(width: 17, height: 14), flipped: false) { _ in
                NSColor.black.setFill()
                for x in [CGFloat(0), 6, 12] {
                    NSBezierPath(roundedRect: NSRect(x: x, y: 1, width: 5, height: 12),
                                 xRadius: 1.2, yRadius: 1.2).fill()
                }
                return true
            }
            mark.isTemplate = true
            mark.accessibilityDescription = "Open Kanban Rememory Runner"
            item.button?.image = mark
            item.button?.toolTip = "Open Kanban Rememory Runner"
            item.button?.target = self
            item.button?.action = #selector(showWatchers)
            statusItem = item
        }
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
        WindowGroup("Kanban Rememory Runner", id: "watchers") {
            WatcherView(registerOpenAction: { delegate.openWatchers = $0 })
                .preferredColorScheme(appearance == "System" ? nil : appearance == "Dark" ? .dark : .light)
        }.windowResizability(.contentSize)
    }
}

private struct WatcherProfile: Codable {
    let name: String
    let icon: String
}

struct WatcherView: View {
    var registerOpenAction: ((@escaping () -> Void) -> Void)?
    @Environment(\.openWindow) private var openWindow
    @State private var repositoryPath = ""
    @State private var repositoryFeedback = ""
    @State private var availableEngines: [String: String] = [:]
    @State private var choosingIcon = false
    @State private var editingTarget: Watcher?
    private let iconNames = ["Folder", "Code", "Document", "Server", "Terminal", "Tools", "Bolt", "Clock", "Branch", "Package", "Cloud", "Settings"]
    @State private var watchers: [Watcher] = []
    @State private var selection: URL?
    @State private var disabledInstallations: Set<URL> = []
    @State private var statuses: [URL: ServiceStatus] = [:]
    @State private var checkedRepository: URL?
    @State private var checkingRepository = false
    @State private var creating = false
    @State private var engine = "codex"
    @AppStorage("appearance") private var appearance = "System"
    @AppStorage("watcher-profiles") private var storedProfiles = Data()
    @State private var profiles: [String: WatcherProfile] = [:]
    @State private var watcherName = ""
    @State private var icon = "folder"
    @State private var settings = false
    @State private var details = false
    private let icons = ["folder", "chevron.left.forwardslash.chevron.right", "doc.text", "server.rack", "terminal", "wrench", "bolt", "clock", "arrow.triangle.branch", "shippingbox", "cloud", "gearshape"]
    @State private var deleting = false
    @State private var seconds = ""
    @State private var message = ""
    @State private var failed = false
    @AppStorage("watcher-history") private var storedHistory = Data()
    @State private var history: [String: RunHistory] = [:]

    private var selected: Watcher? { watchers.first { $0.id == selection } }

    var body: some View {
        Group {
            if creating { watcherForm }
            else { watcherList }
        }.navigationTitle("Watchers")
        .toolbar {

            if !creating {
                Button(action: chooseRepository) { Label("New Watcher", systemImage: "plus") }
                .disabled(checkingRepository || !live)
            Button { settings.toggle() } label: { Label("Settings", systemImage: "gearshape") }
                .popover(isPresented: $settings) {
                    VStack(alignment: .leading, spacing: 12) {
                    Text("Settings").font(.headline)
                    Text("Appearance").font(.subheadline)
                    Picker("Appearance", selection: $appearance) {
                        ForEach(["System", "Light", "Dark"], id: \.self) { Text($0) }
                    }.pickerStyle(.segmented).labelsHidden()
                    }.padding().frame(width: 280)
                }
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
        .frame(width: 470, height: 380)
        .onAppear {
            let showWindow = openWindow
            registerOpenAction? { showWindow(id: "watchers") }
        }
        .task {
            profiles = (try? JSONDecoder().decode([String: WatcherProfile].self, from: storedProfiles)) ?? [:]
            history = (try? JSONDecoder().decode([String: RunHistory].self, from: storedHistory)) ?? [:]
            perform(refresh)
            if !live, let prefix = ProcessInfo.processInfo.environment["KRR_VISUAL_CAPTURE"] {
                try? await Task.sleep(for: .milliseconds(500))
                try? capturePreview(prefix)
                NSApplication.shared.terminate(nil)
                return
            }
            while !Task.isCancelled {
                try? await Task.sleep(for: .seconds(15))
                if !Task.isCancelled { try? refresh() }
            }
        }
        .alert("Watcher operation failed", isPresented: $failed) {
            Button("OK", role: .cancel) {}
        } message: { Text(message) }
    }

    private var watcherList: some View {
        Group {
            if watchers.isEmpty {
                VStack(spacing: 10) {
                    Image(systemName: "folder").font(.system(size: 26)).foregroundStyle(.teal)
                    Text("No watchers").font(.headline)
                    Button("New Watcher", action: chooseRepository)
                        .buttonStyle(.borderedProminent).tint(.teal)
                        .disabled(checkingRepository || !live)
                }.frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                ScrollView { watcherGroup }
            }
        }
    }

    private var watcherGroup: some View {
            VStack(spacing: 0) {
                ForEach(watchers) { watcher in
                    if watcher.label != watchers.first?.label { Divider().padding(.leading, 62) }
                    watcherRow(watcher)
                }
            }
            .background(.primary.opacity(0.035), in: RoundedRectangle(cornerRadius: 16))
            .overlay { RoundedRectangle(cornerRadius: 16).strokeBorder(.primary.opacity(0.10)) }
            .padding(16)
    }

    @MainActor private func capturePreview(_ prefix: String) throws {
        for (name, scheme) in [("light", ColorScheme.light), ("dark", .dark)] {
            let renderer = ImageRenderer(content: VStack(alignment: .leading, spacing: 0) {
                Text("Watchers").font(.title2.bold()).padding([.top, .horizontal], 16)
                watcherGroup
                Spacer(minLength: 0)
            }.frame(width: 420, height: 320)
             .background(scheme == .dark ? Color(white: 0.12) : Color(white: 0.96))
             .environment(\.colorScheme, scheme))
            renderer.scale = 2
            if let image = renderer.cgImage,
               let data = NSBitmapImageRep(cgImage: image).representation(using: .png, properties: [:]) {
                try data.write(to: URL(fileURLWithPath: prefix + "-" + name + ".png"))
            }
        }
    }

    private func watcherRow(_ watcher: Watcher) -> some View {
            HStack(spacing: 12) {
                Image(systemName: previewIndex(watcher).map { ["rectangle.split.3x1", "doc.text", "server.rack", "gearshape"][$0] } ?? profiles[watcher.label]?.icon ?? "folder")
                    .font(.system(size: 18, weight: .medium))
                    .frame(width: 38, height: 38)
                    .background(Color.teal.opacity(0.16), in: RoundedRectangle(cornerRadius: 9))
                    .foregroundStyle(.teal)
                    .accessibilityHidden(true)
                VStack(alignment: .leading, spacing: 3) {
                    Text(displayName(watcher)).font(.headline)
                    Text("\(watcher.engine) · \(state(watcher))").foregroundStyle(.secondary)
                    if state(watcher) == "Deactivating", (statuses[watcher.id]?.active == true || !live) {
                        Text("Waiting for the current run to finish").font(.caption).foregroundStyle(.secondary)
                    }
                }
                Spacer()
                if state(watcher) == "Ready" {
                    Button("Run Now") { if live { perform { try run(watcher) } } }
                } else if state(watcher) == "Disabled" && (watcher.editable || !live) {
                    Button("Activate") { if live { perform { try ManagedWatchers.activate(watcher) } } }
                } else if state(watcher) == "Running" {
                    ProgressView().controlSize(.small).accessibilityLabel("Running")
                }
                Menu {
                    Button("Details") { selection = watcher.id; details = true }
                    if isManaged(watcher) {
                        if !watcher.editable { Text("Deactivate to edit") }
                        Button("Edit Watcher") {
                            beginEdit(watcher)
                        }.disabled(!watcher.editable)
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
            }.padding(.horizontal, 12).padding(.vertical, 10)
                .buttonStyle(.bordered).tint(.teal)
    }

    private var live: Bool { ProcessInfo.processInfo.environment["KRR_FIXTURE_DIRECTORY"] == nil }
    private var cleanName: String { watcherName.trimmingCharacters(in: .whitespacesAndNewlines) }

    private var iconPicker: some View {
        Button { choosingIcon.toggle() } label: {
            HStack {
                Image(systemName: icon).foregroundStyle(.teal)
                Text(iconNames[icons.firstIndex(of: icon) ?? 0])
                Image(systemName: "chevron.down").font(.caption)
            }
        }
        .popover(isPresented: $choosingIcon, arrowEdge: .bottom) {
            LazyVGrid(columns: Array(repeating: GridItem(.fixed(36), spacing: 6), count: 6), spacing: 6) {
                ForEach(icons.indices, id: \.self) { index in
                    Button {
                        icon = icons[index]
                        choosingIcon = false
                    } label: {
                        Image(systemName: icons[index]).frame(width: 30, height: 30)
                            .overlay(alignment: .bottomTrailing) {
                                if icon == icons[index] { Image(systemName: "checkmark.circle.fill").font(.caption2) }
                            }
                    }.buttonStyle(.borderless)
                        .background(icon == icons[index] ? Color.teal.opacity(0.3) : .clear,
                                    in: RoundedRectangle(cornerRadius: 6))
                        .accessibilityLabel(iconNames[index])
                        .help(iconNames[index])
                }
            }.padding(10)
        }
    }

    private var watcherForm: some View {
        VStack(alignment: .leading, spacing: 13) {
            Text(editingTarget == nil ? "New Watcher" : "Edit Watcher").font(.title2.bold())
            Grid(alignment: .leading, horizontalSpacing: 12, verticalSpacing: 9) {
                GridRow { Text("Watcher Name"); TextField("Watcher Name", text: $watcherName) }
                GridRow {
                    Text("Repository")
                    HStack {
                        TextField("Paste a folder path", text: $repositoryPath)
                            .onSubmit { checkRepository() }
                        if checkedRepository != nil {
                            Image(systemName: "checkmark.circle").foregroundStyle(.teal)
                                .accessibilityLabel("Repository validated")
                        }
                        Button("Browse…", action: browseRepository)

                    }
                }
                GridRow {
                    Text("")
                    HStack {
                        Text(repositoryFeedback).font(.caption).foregroundStyle(.secondary).lineLimit(2)
                        Spacer()
                        if checkedRepository == nil { Button("Verify", action: checkRepository).disabled(checkingRepository) }
                    }
                }
                GridRow {
                    Text("Engine")
                    Picker("Engine", selection: $engine) {
                        Text("Codex").tag("codex").disabled(availableEngines["codex"] == nil)
                        Text("Claude Code").tag("claude").disabled(availableEngines["claude"] == nil)
                    }.pickerStyle(.segmented).labelsHidden()
                }
                if availableEngines.isEmpty {
                    GridRow {
                        Text("")
                        HStack {
                            Text("No supported CLI detected").font(.caption)
                        }
                    }
                }
                GridRow {
                    Text("Run every")
                    HStack { TextField("5", text: $seconds).frame(width: 65); Text("minutes") }
                }
                GridRow { Text("Icon"); iconPicker }
            }.textFieldStyle(.roundedBorder)
            Spacer(minLength: 0)
            Divider()
            HStack {
                Spacer()
                Button("Cancel") { creating = false }.keyboardShortcut(.cancelAction)
                Button(editingTarget == nil ? "Create Watcher" : "Save", action: saveWatcher)
                    .buttonStyle(.borderedProminent).tint(.teal)
                    .disabled(checkedRepository == nil || availableEngines[engine] == nil || cleanName.isEmpty
                              || intervalSeconds == nil || checkingRepository)
            }
        }.padding(20)
        .onChange(of: repositoryPath) { value in
            if value != checkedRepository?.path { checkedRepository = nil; repositoryFeedback = "" }
        }
    }

    private var intervalSeconds: Int? {
        guard let minutes = Double(seconds), minutes.isFinite,
              minutes >= 1.0 / 60, minutes <= Double(Int32.max) / 60 else { return nil }
        return Int((minutes * 60).rounded())
    }

    private func saveWatcher() {
        guard let repository = checkedRepository, let path = availableEngines[engine],
              let interval = intervalSeconds else { return }
        perform {
            if let watcher = editingTarget {
                try LaunchAgents.change(watcher, interval: interval, repository: repository,
                                        executable: URL(fileURLWithPath: path), engine: engine)
                saveProfile(watcher.label)
            } else {
                let file = try ManagedWatchers.allocateLabel { label in
                    guard try LaunchAgents.isAvailable(label) else { return nil }
                    do {
                        return try ManagedWatchers.create(repository: repository, executable: URL(fileURLWithPath: path),
                                                          engine: engine, interval: interval, label: label,
                                                          agents: ManagedWatchers.inactive, records: ManagedWatchers.records) {}
                    } catch let error as CocoaError where error.code == .fileWriteFileExists { return nil }
                }
                saveProfile(file.deletingPathExtension().lastPathComponent)
            }
            creating = false
        }
    }

    private func previewIndex(_ watcher: Watcher) -> Int? {
        guard !live, ProcessInfo.processInfo.environment["KRR_VISUAL_CAPTURE"] != nil,
              let index = Int(watcher.label.replacingOccurrences(of: "fixture-", with: "")),
              (0..<4).contains(index) else { return nil }
        return index
    }

    private func displayName(_ watcher: Watcher) -> String {
        if let index = previewIndex(watcher) { return ["Kanban Rememory", "Docs Site", "API Service", "Build Tools"][index] }
        return profiles[watcher.label]?.name ?? watcher.label
    }

    private func isManaged(_ watcher: Watcher) -> Bool {
        live && (watcher.editable || ManagedWatchers.installedAndOwned(watcher))
    }

    private func state(_ watcher: Watcher) -> String {
        if let index = previewIndex(watcher) { return ["Ready", "Disabled", "Running", "Deactivating"][index] }
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
        guard live else { return }
        editingTarget = nil
        checkedRepository = nil
        repositoryPath = ""
        repositoryFeedback = ""
        watcherName = ""
        seconds = "5"
        icon = "folder"
        detectEngines()
        creating = true
    }

    private func beginEdit(_ watcher: Watcher) {
        editingTarget = watcher
        watcherName = displayName(watcher)
        icon = profiles[watcher.label]?.icon ?? "folder"
        seconds = String(Double(watcher.interval ?? 300) / 60)
        detectEngines()
        engine = watcher.engine == "Codex" ? "codex" : "claude"
        if FileManager.default.isExecutableFile(atPath: watcher.executable) { availableEngines[engine] = watcher.executable }
        repositoryPath = watcher.plist["WorkingDirectory"] as? String ?? ""
        creating = true
        checkRepository()
    }

    private func detectEngines() {
        let home = FileManager.default.homeDirectoryForCurrentUser.path
        let paths = (ProcessInfo.processInfo.environment["PATH"] ?? "").split(separator: ":").map(String.init)
        availableEngines = [:]
        for name in ["codex", "claude"] {
            availableEngines[name] = (paths + [home + "/.local/bin", home + "/.npm-global/bin", "/opt/homebrew/bin", "/usr/local/bin", "/usr/bin"])
                .filter { $0.hasPrefix("/") }.map { $0 + "/" + name }
                .first { FileManager.default.isExecutableFile(atPath: $0) }
        }
        engine = availableEngines["codex"] != nil ? "codex" : "claude"
    }

    private func browseRepository() {
        let panel = NSOpenPanel()
        panel.canChooseFiles = false
        panel.canChooseDirectories = true
        panel.begin { response in
            guard response == .OK, let url = panel.url else { return }
            repositoryPath = url.path
            checkRepository()
        }
    }

    private func checkRepository() {
        let path = (repositoryPath.trimmingCharacters(in: .whitespacesAndNewlines) as NSString).expandingTildeInPath
        guard !checkingRepository, path.hasPrefix("/"), let resources = Bundle.main.resourceURL else { return }
        let input = repositoryPath
        checkingRepository = true
        repositoryFeedback = "Checking repository…"
        Task { @MainActor in
            defer { checkingRepository = false }
            do {
                let validator = resources.appendingPathComponent("validator/manage-kanban-board.py")
                let root = try await Task.detached {
                    try RepositoryPreflight.check(URL(fileURLWithPath: path), validator: validator, resolveRoot: true)
                }.value
                guard repositoryPath == input else { return }
                checkedRepository = root
                repositoryPath = root.path
                repositoryFeedback = ""
            } catch {
                if repositoryPath == input {
                    checkedRepository = nil
                    repositoryFeedback = error.localizedDescription
                }
            }
        }
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
