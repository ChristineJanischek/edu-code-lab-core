#!/usr/bin/env sh
set -eu

VALIDATOR="./core/tooling/validate_task_template.sh"
VALID_FILE="./tests/fixtures/templates/valid-task-v1.json"
INVALID_FILE="./tests/fixtures/templates/invalid-task-v1.json"

echo "[test] Template validator: valid sample"
sh "$VALIDATOR" "$VALID_FILE"

echo "[test] Template validator: invalid sample should fail"
if sh "$VALIDATOR" "$INVALID_FILE"; then
  echo "Ungueltiges Template wurde faelschlicherweise akzeptiert"
  exit 1
fi

echo "[test] Template validation OK"