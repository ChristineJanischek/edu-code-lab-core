#!/usr/bin/env sh
set -eu

echo "[build] Verifiziere Mindeststruktur"
for path in core/platform core/tooling core/templates core/integrations docs .github/workflows; do
  [ -d "$path" ] || { echo "Fehlt: $path"; exit 1; }
done

echo "[build] OK"
