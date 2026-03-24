#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 <path-to-edu-code-lab-courses>"
  exit 2
fi

COURSES_REPO_PATH="$1"
LOCK_FILE="$COURSES_REPO_PATH/.core-association.lock"
VALIDATOR="./core/tooling/validate_task_template.sh"

if [ ! -d "$COURSES_REPO_PATH" ]; then
  echo "Courses-Pfad existiert nicht: $COURSES_REPO_PATH"
  exit 1
fi

if [ ! -f "$LOCK_FILE" ]; then
  echo "Lock-Datei fehlt: $LOCK_FILE"
  exit 1
fi

CORE_REPO_VAL="$(grep -E '^CORE_REPO=' "$LOCK_FILE" | head -n1 | cut -d'=' -f2-)"
CORE_REF_VAL="$(grep -E '^CORE_REF=' "$LOCK_FILE" | head -n1 | cut -d'=' -f2-)"
TASK_SCHEMA_VERSION_VAL="$(grep -E '^TASK_SCHEMA_VERSION=' "$LOCK_FILE" | head -n1 | cut -d'=' -f2-)"
VALIDATOR_PATH_VAL="$(grep -E '^VALIDATOR_PATH=' "$LOCK_FILE" | head -n1 | cut -d'=' -f2-)"

if [ -z "$CORE_REPO_VAL" ] || [ -z "$CORE_REF_VAL" ] || [ -z "$TASK_SCHEMA_VERSION_VAL" ] || [ -z "$VALIDATOR_PATH_VAL" ]; then
  echo "Lock-Datei unvollstaendig: CORE_REPO, CORE_REF, TASK_SCHEMA_VERSION, VALIDATOR_PATH sind Pflicht"
  exit 1
fi

if [ ! -f "$VALIDATOR" ]; then
  echo "Core-Validator nicht gefunden: $VALIDATOR"
  exit 1
fi

TASK_FILES="$(find "$COURSES_REPO_PATH/courses" -type f -name '*.task.json' 2>/dev/null || true)"

if [ -z "$TASK_FILES" ]; then
  echo "Keine Task-Dateien gefunden unter: $COURSES_REPO_PATH/courses"
  exit 1
fi

echo "[association] CORE_REPO=$CORE_REPO_VAL"
echo "[association] CORE_REF=$CORE_REF_VAL"
echo "[association] TASK_SCHEMA_VERSION=$TASK_SCHEMA_VERSION_VAL"
echo "[association] VALIDATOR_PATH=$VALIDATOR_PATH_VAL"

echo "[association] Starte Validierung..."
for file in $TASK_FILES; do
  sh "$VALIDATOR" "$file"
done

echo "[association] OK"