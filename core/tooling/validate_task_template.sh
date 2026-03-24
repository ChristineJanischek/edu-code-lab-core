#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <task-template.json>"
  exit 2
fi

file="$1"

if [ ! -f "$file" ]; then
  echo "Datei nicht gefunden: $file"
  exit 1
fi

require_key() {
  key="$1"
  if ! grep -Eq '"'"$key"'"[[:space:]]*:' "$file"; then
    echo "Pflichtfeld fehlt: $key"
    exit 1
  fi
}

require_key "schemaVersion"
require_key "id"
require_key "title"
require_key "learningObjective"
require_key "difficulty"
require_key "points"
require_key "durationMinutes"
require_key "solution"

if ! grep -Eq '"schemaVersion"[[:space:]]*:[[:space:]]*"1\.0"' "$file"; then
  echo "schemaVersion muss 1.0 sein"
  exit 1
fi

if ! grep -Eq '"difficulty"[[:space:]]*:[[:space:]]*"(easy|medium|hard)"' "$file"; then
  echo "difficulty muss easy, medium oder hard sein"
  exit 1
fi

if ! grep -Eq '"points"[[:space:]]*:[[:space:]]*[1-9][0-9]*' "$file"; then
  echo "points muss eine positive ganze Zahl sein"
  exit 1
fi

if ! grep -Eq '"durationMinutes"[[:space:]]*:[[:space:]]*[1-9][0-9]*' "$file"; then
  echo "durationMinutes muss eine positive ganze Zahl sein"
  exit 1
fi

if ! grep -Eq '"solution"[[:space:]]*:[[:space:]]*\{' "$file"; then
  echo "solution muss ein Objekt sein"
  exit 1
fi

if ! grep -Eq '"type"[[:space:]]*:[[:space:]]*"(text|code)"' "$file"; then
  echo "solution.type muss text oder code sein"
  exit 1
fi

if ! grep -Eq '"content"[[:space:]]*:[[:space:]]*"[^"]+"' "$file"; then
  echo "solution.content darf nicht leer sein"
  exit 1
fi

echo "[validate] OK: $file"