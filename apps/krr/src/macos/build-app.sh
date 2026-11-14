#!/bin/bash
set -euo pipefail
source_dir="$(cd "$(dirname "$0")" && pwd)"
repository_root="$(cd "$source_dir/../../../.." && pwd)"
output="${1:-$source_dir/../../build/macos/Kanban Rememory Runner.app}"
scratch="$(mktemp -d)"
trap 'rm -rf "$scratch"' EXIT
mkdir -p "$output/Contents/MacOS"
cp "$source_dir/info.plist" "$output/Contents/Info.plist"
architecture="$(uname -m)"
xcrun swiftc -module-cache-path "$scratch/module-cache" -target "$architecture-apple-macos13.0" -warnings-as-errors \
  "$source_dir/runner.swift" "$source_dir/watcher.swift" "$source_dir/repository-preflight.swift" "$source_dir/managed-watchers.swift" -o "$output/Contents/MacOS/runner"

iconset="$scratch/app-icon.iconset"
mkdir -p "$iconset" "$output/Contents/Resources"
for size in 16 32 128 256 512; do
  sips -z "$size" "$size" "$source_dir/app-icon.png" --out "$iconset/icon_${size}x${size}.png" >/dev/null
  sips -z "$((size * 2))" "$((size * 2))" "$source_dir/app-icon.png" --out "$iconset/icon_${size}x${size}@2x.png" >/dev/null
done
iconutil -c icns "$iconset" -o "$output/Contents/Resources/app-icon.icns"
validator="$output/Contents/Resources/validator"
mkdir -p "$validator/kanban"
cp "$repository_root/agents/tools/manage-kanban-board.py" "$validator/"
cp "$repository_root/agents/tools/kanban/"*.py "$validator/kanban/"
codesign --force --sign - "$output"
codesign --verify --strict "$output"
