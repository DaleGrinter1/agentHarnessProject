#!/bin/sh

set -eu

echo "Validating repository knowledge scaffold..."

product_specs_index=docs/product-"specs"/index.md

required_files="
AGENTS.md
README.md
ARCHITECTURE.md
docs/design-docs/index.md
docs/design-docs/core-beliefs.md
$product_specs_index
docs/references/index.md
docs/generated/db-schema.md
docs/PLANS.md
docs/RELIABILITY.md
docs/SECURITY.md
docs/exec-plans/PLAN_TEMPLATE.md
docs/exec-plans/index.md
docs/exec-plans/active/README.md
docs/exec-plans/tech-debt-tracker.md
docs/DESIGN.md
docs/FRONTEND.md
docs/PRODUCT_SENSE.md
docs/QUALITY_SCORE.md
scripts/execplan/check.sh
scripts/execplan/validate-state.mjs
src/README.md
tests/README.md
"

for path in $required_files; do
  if [ ! -f "$path" ]; then
    echo "Missing required file: $path" >&2
    exit 1
  fi
done

for path in docs docs/exec-plans docs/exec-plans/active docs/exec-plans/completed docs/design-docs docs/generated docs/product-specs docs/references src tests; do
  if [ ! -d "$path" ]; then
    echo "Missing required directory: $path" >&2
    exit 1
  fi
done

./scripts/execplan/check.sh

echo "Repository knowledge scaffold validation passed."
