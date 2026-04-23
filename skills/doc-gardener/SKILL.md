---
name: doc-gardener
description: Audit and improve repo knowledge quality by finding stale docs, broken local links, legacy path regressions, missing routing context, and drift between docs and code. Use for periodic cleanup, doc audits, and harness maintenance.
---

# Doc Gardener

Use this skill for doc hygiene and repository-knowledge maintenance.

## Primary Targets

- `AGENTS.md`
- `ARCHITECTURE.md`
- `docs/`
- active initiative plans and state
- validation scripts that enforce doc structure

## Workflow

1. Run `./scripts/execplan/check.sh`.
2. Inspect affected docs and routing pages.
3. Look for stale facts, broken links, missing canonical references, and drift
   between docs and code.
4. Make small reviewable fixes.
5. Re-run validation and log the cleanup in the relevant initiative.

## What To Look For

- outdated file paths
- broken local markdown links
- docs that no longer match scripts or repo layout
- active plans whose state files no longer match reality
- missing ownership, validation, or handoff details

## Guardrails

- Prefer updating canonical docs over adding new ones.
- Keep `AGENTS.md` concise and map-style.
- Do not preserve deprecated planning patterns just because they already exist.
