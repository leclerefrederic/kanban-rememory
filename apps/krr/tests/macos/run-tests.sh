#!/bin/bash
# Builds and runs the KRR logic tests with a fake Terminal. Run from anywhere.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
sources="$here/../../src/macos"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
xcrun swiftc -module-cache-path "$scratch/module-cache" -target "$(uname -m)-apple-macos13.0" -warnings-as-errors \
  "$sources/claude-sessions.swift" "$sources/watcher.swift" "$sources/managed-watchers.swift" "$here/main.swift" -o "$scratch/tests"
"$scratch/tests"
