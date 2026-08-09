#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

CONFIG_FILE="config/probe_2026_2027.json"
LAYOUT_TEMPLATE="config/layout_template_v003.json"
TRANSFER_XLS="${1:-../../09_Import_und_Pruefung/Eingang/Wochenplaene_2025_2026_transfer.xls}"
TARGET_SCHOOL_YEAR="${2:-2026/2027}"
PRINT_MODE="${3:-auto}"

python3 wochenplan_generator.py \
  --config "$CONFIG_FILE" \
  --layout-template "$LAYOUT_TEMPLATE" \
  --transfer-xls "$TRANSFER_XLS" \
  --target-school-year "$TARGET_SCHOOL_YEAR" \
  --print-mode "$PRINT_MODE"
