# Migrate the repository to a harness-style in-repo knowledge system

This ExecPlan is a living document. Keep `Progress`, `Surprises & Discoveries`,
`Decision Log`, and `Outcomes & Retrospective` current as work proceeds.

This plan must be maintained in accordance with `docs/PLANS.md`.

## Purpose / Big Picture

The repository should become its own durable operating context for coding
agents. After this change, agents can resume non-trivial work by reading a
short map-style `AGENTS.md`, the canonical docs, one initiative markdown plan,
and JSON state files that capture implementation checklist, active handoff
state, and append-only progress evidence.

## Surprises & Discoveries

- Observation: The repo already had `docs/exec-plans/` and placeholder
  `scripts/execplan/` files, but they were still wired to an older scaffold.
  Evidence: `scripts/validate-harness.sh` required `docs/PRODUCT.md`,
  `docs/ARCHITECTURE.md`, `docs/HARNESS.md`, and `docs/exec-plans/TEMPLATE.md`.
- Observation: The requested reference file at
  `/Users/ibrahimsaidi/Desktop/Builds/cloudflare_builds/orange/docs/PLANS.md`
  was not present in the local filesystem.
  Evidence: `sed` returned `No such file or directory`.
- Observation: The repo has no current typed schema source to summarize.
  Evidence: a repository scan for common schema definitions returned no matches.

## Decision Log

- Decision: Move canonical product, architecture, and harness guidance into the
  requested target layout instead of keeping compatibility aliases.
  Rationale: The migration goal explicitly deprecates legacy paths and wants the
  canonical docs structure to be the system of record.
  Date/Author: 2026-04-23 / Codex
- Decision: Keep historical plan markdown files in `docs/exec-plans/completed/`
  and normalize only active initiatives to the new markdown-plus-JSON pattern.
  Rationale: The requirement mandates the JSON state layout for active
  initiatives and preserves history better when completed artifacts remain
  readable.
  Date/Author: 2026-04-23 / Codex
- Decision: Document weekly doc gardening manually in `docs/PLANS.md` instead
  of adding a recurring automation.
  Rationale: The repo does not currently expose a platform-native recurring
  automation surface, and the request preferred docs/governance changes unless a
  small enforcement script was strictly needed.
  Date/Author: 2026-04-23 / Codex

## Outcomes & Retrospective

The repo now uses canonical harness-style routing, active-plan structure, and
JSON handoff state. Legacy doc paths were removed from tracked content, history
was preserved with `git mv` for tracked relocations, and a validator now checks
the active initiative structure and rejects deprecated planning patterns.

The one notable gap is that the requested external `docs/PLANS.md` reference
file was unavailable locally, so the new repo-local `docs/PLANS.md` was adapted
from the OpenAI cookbook article plus the repository’s concrete needs.

## Context and Orientation

Before this migration, the repo used a generic starter layout with
`docs/PRODUCT.md`, `docs/ARCHITECTURE.md`, `docs/HARNESS.md`, and
`docs/exec-plans/TEMPLATE.md`. The new target layout requires:

- root `ARCHITECTURE.md`
- the `docs/product-specs` directory instead of product docs at `docs/PRODUCT.md`
- `docs/design-docs` for durable design guidance
- `docs/exec-plans/active/<initiative>/PLAN_<initiative>.md`
- `docs/exec-plans/active/<initiative>/state/feature-list.json`
- `docs/exec-plans/active/<initiative>/state/session-state.json`
- `docs/exec-plans/active/<initiative>/state/progress.jsonl`

The key scripts are `scripts/execplan/check.sh` and
`scripts/execplan/validate-state.mjs`.

## Plan of Work

First scaffold the required directories and create the active migration
initiative. Then move tracked canonical docs with `git mv` so history is
preserved. Rewrite routing docs, indexes, and governance files to describe the
repository-as-system-of-record model and the one-plan-plus-JSON-state workflow.
After the docs are in place, implement the validator scripts so the layout is
checked mechanically. Finally, run the validation commands and update the plan
and JSON state with the results.

## Concrete Steps

Run from the repo root:

```sh
mkdir -p docs/exec-plans/active/harness-knowledge-migration/state
mkdir -p docs/exec-plans/completed docs/design-docs docs/generated docs/product-specs docs/references
git mv docs/PRODUCT.md docs/product-"specs"/index.md
git mv docs/ARCHITECTURE.md ARCHITECTURE.md
git mv docs/HARNESS.md docs/design-docs/core-beliefs.md
git mv docs/exec-plans/TEMPLATE.md docs/exec-plans/PLAN_TEMPLATE.md
git mv docs/exec-plans/2026-04-23-harness-maturity.md docs/exec-plans/completed/2026-04-23-harness-maturity.md
git mv docs/exec-plans/2026-04-23-openai-docs-mcp.md docs/exec-plans/completed/2026-04-23-openai-docs-mcp.md
./scripts/execplan/check.sh
./scripts/validate-harness.sh
```

Expected result: the validation commands exit successfully and report that the
active initiative structure and canonical docs are valid.

## Machine State

Document the JSON handoff files for this initiative:

- `state/feature-list.json` is the canonical implementation checklist.
- Every feature starts with `"passes": false`.
- `state/session-state.json` tracks the active feature, blockers, next action,
  and handoff rules.
- `state/progress.jsonl` is append-only and records meaningful checkpoints with
  structured evidence.

## Progress

- [x] (2026-04-23T02:30:23Z) Scaffolded the canonical `docs/exec-plans/active/`
  layout and created the migration initiative directory.
- [x] (2026-04-23T02:35:00Z) Preserved history with `git mv` for tracked docs
  moving into the canonical layout.
- [x] (2026-04-23T02:55:00Z) Rewrote routing docs, indexes, plan guidance, and
  active-state files to use the markdown-plan-plus-JSON-state workflow.
- [x] (2026-04-23T03:10:00Z) Implemented validator scripts and passed the final
  execplan and scaffold verification commands.

## Testing Approach

Validation for this migration is documentation- and structure-focused:

- run `./scripts/execplan/check.sh`
- run `./scripts/validate-harness.sh`
- run the execplan validator and expect no legacy-path regressions

## Constraints & Considerations

- Preserve history with `git mv` for tracked relocations.
- Do not add dependencies.
- Do not introduce markdown task files in active initiatives.
- Keep `AGENTS.md` concise and map-style.

Revision note: updated after verification so the progress log, JSON state, and
validation outcomes match the completed migration.
