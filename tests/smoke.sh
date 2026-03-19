#!/usr/bin/env sh
set -eu

echo "[test] Smoke-Test: README vorhanden"
[ -f README.md ]
echo "[test] OK"
