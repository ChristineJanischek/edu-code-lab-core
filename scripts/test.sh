#!/usr/bin/env sh
set -eu

./tests/smoke.sh
sh ./tests/template_validation.sh
