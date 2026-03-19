#!/usr/bin/env sh
set -eu

for file in README.md CONTRIBUTING.md SECURITY.md docs/INTEGRATIONSVERTRAG.md; do
  [ -f "$file" ] || { echo "Fehlende Release-Grundlage: $file"; exit 1; }
done

echo "[release-check] OK"
