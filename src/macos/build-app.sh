#!/bin/bash
set -euo pipefail
source_dir="$(cd "$(dirname "$0")" && pwd)"
output="$source_dir/../../build/macos/Kanban Rememory Runner.app"
mkdir -p "$output/Contents/MacOS"
cp "$source_dir/info.plist" "$output/Contents/Info.plist"
architecture="$(uname -m)"
xcrun swiftc -module-cache-path "$source_dir/../../build/macos/module-cache" -target "$architecture-apple-macos13.0" -warnings-as-errors \
  "$source_dir/runner.swift" "$source_dir/watcher.swift" -o "$output/Contents/MacOS/runner"

iconset="$source_dir/../../build/macos/app-icon.iconset"
mkdir -p "$iconset" "$output/Contents/Resources"
for size in 16 32 128 256 512; do
  sips -z "$size" "$size" "$source_dir/app-icon.png" --out "$iconset/icon_${size}x${size}.png" >/dev/null
  sips -z "$((size * 2))" "$((size * 2))" "$source_dir/app-icon.png" --out "$iconset/icon_${size}x${size}@2x.png" >/dev/null
done
iconutil -c icns "$iconset" -o "$output/Contents/Resources/app-icon.icns"
codesign --force --sign - "$output"
codesign --verify --strict "$output"
