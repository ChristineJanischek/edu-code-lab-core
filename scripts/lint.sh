#!/usr/bin/env sh
set -eu

echo "[lint] Keine Tabs in Markdown-Dateien"
if grep -RIn --include='*.md' "\t" .; then
  echo "Tabs in Markdown gefunden"
  exit 1
fi

echo "[lint] Keine trailing spaces in Shell/Markdown"
if grep -RIn --include='*.sh' --include='*.md' "[[:blank:]]$" .; then
  echo "Trailing spaces gefunden"
  exit 1
fi

echo "[lint] OK"
