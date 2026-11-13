# Build Kanban Rememory Runner for macOS

Run `bash src/macos/build-app.sh` from the repository root.

Use `build/macos/Kanban Rememory Runner.app` for acceptance testing. Keep exactly one visible app bundle in that directory. The build compiles and verifies a staged bundle before replacing the previous app. About displays the source revision and indicates local changes.

Keep diagnostic copies, fixture repositories, and test executables in temporary directories outside the delivery folder. Remove them after verification.
