#!/bin/bash
set -euo pipefail
source_dir="$(cd "$(dirname "$0")" && pwd)"
build_dir="$source_dir/../../build/macos"
mkdir -p "$build_dir"
destination="$build_dir/Kanban Rememory Runner.app"
scratch="$(mktemp -d "$build_dir/.build.XXXXXX")"
output="$scratch/Kanban Rememory Runner.app"
backup="$scratch/previous.app"
cleanup() {
  if [[ -d "$backup" && ! -e "$destination" ]]; then
    mv "$backup" "$destination" || return
  fi
  rm -rf "$scratch"
}
trap cleanup EXIT
mkdir -p "$output/Contents/MacOS"
cp "$source_dir/info.plist" "$output/Contents/Info.plist"
revision="$(git -C "$source_dir" rev-parse --short HEAD)"
if [[ -n "$(git -C "$source_dir" status --porcelain -- src/macos tools/kanban tools/manage-kanban-board.py)" ]]; then
  revision="$revision (local changes)"
fi
/usr/libexec/PlistBuddy -c "Add :NSHumanReadableCopyright string Build $revision" "$output/Contents/Info.plist"
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
cp "$source_dir/../../tools/manage-kanban-board.py" "$validator/"
cp "$source_dir/../../tools/kanban/"*.py "$validator/kanban/"
codesign --force --sign - "$output"
codesign --verify --strict "$output"
if [[ -e "$destination" ]]; then
  mv "$destination" "$backup"
fi
mv "$output" "$destination"
printf 'Build %s: %s\n' "$revision" "$destination"
