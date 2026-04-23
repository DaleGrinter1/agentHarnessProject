#!/bin/sh

set -eu

echo "Running execplan validation..."
python3 scripts/execplan/validate-state.mjs

echo "Execplan checks passed."
