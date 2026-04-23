#!/bin/sh

set -eu

echo "Validating harness scaffold..."

required_files="
AGENTS.md
README.md
docs/PRODUCT.md
docs/ARCHITECTURE.md
docs/RELIABILITY.md
docs/SECURITY.md
docs/HARNESS.md
docs/exec-plans/TEMPLATE.md
src/README.md
tests/README.md
"

for path in $required_files; do
  if [ ! -f "$path" ]; then
    echo "Missing required file: $path" >&2
    exit 1
  fi
done

for path in docs/exec-plans src tests; do
  if [ ! -d "$path" ]; then
    echo "Missing required directory: $path" >&2
    exit 1
  fi
done

echo "Harness scaffold validation passed."
