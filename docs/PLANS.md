# PLANS.md

This document defines how the repository uses execution plans for non-trivial
work.

## Purpose

Use an execution plan when work is large enough that a future agent or human
could lose context, make the wrong change order, or miss important validation.

The plan is a living implementation narrative. JSON state is the machine-owned
handoff surface.

## When A Plan Is Required

Use a plan for:

- repo-wide migrations
- non-trivial refactors
- multi-file feature work
- work expected to span multiple sessions
- changes with meaningful validation or rollback concerns

Skip a plan only for clearly trivial edits.

## Active Initiative Layout

Each active initiative lives in its own directory under
`docs/exec-plans/active/<initiative>/` and must contain:

- `PLAN_<initiative>.md`
- `state/feature-list.json`
- `state/session-state.json`
- `state/progress.jsonl`

## Narrative Plan Rules

The markdown plan is the durable narrative and must stay aligned with the
implementation. Start from `docs/exec-plans/PLAN_TEMPLATE.md`.

Required sections:

- `## Purpose / Big Picture`
- `## Surprises & Discoveries`
- `## Decision Log`
- `## Outcomes & Retrospective`
- `## Context and Orientation`
- `## Plan of Work`
- `## Concrete Steps`
- `## Machine State`
- `## Progress`
- `## Testing Approach`
- `## Constraints & Considerations`

## Machine State Rules

`state/feature-list.json` is the canonical implementation checklist.

- Each feature needs a stable `id`.
- Every feature starts with `"passes": false`.
- Only mark a feature passing after meaningful validation.

`state/session-state.json` is the session handoff file.

- Track the active feature, blockers, next action, and handoff rules.
- Keep it current enough that a fresh agent can resume immediately.

`state/progress.jsonl` is append-only progress history.

- Each line is one JSON object.
- Record meaningful checkpoints, not chatter.
- Include timestamps, actor, type, summary, and valid feature references.
- Evidence should point to commands, files, tests, or observable outcomes.

## Default Workflow

1. Read `AGENTS.md`, `README.md`, and the relevant canonical docs.
2. Read `docs/exec-plans/PLAN_TEMPLATE.md`.
3. Read `docs/exec-plans/index.md`.
4. Read the initiative plan and all three state files.
5. Update the plan and JSON state as the work evolves.
6. Run validation before concluding the work.

## What Not To Do

- Do not create per-task markdown files by default.
- Do not create `tasks/` directories inside active initiatives.
- Do not keep implementation state only in chat or commit messages.
- Do not leave feature completion ambiguous.

## Completed Work

When an initiative is finished and handed off cleanly, move it or summarize it
into `docs/exec-plans/completed/`.

## Weekly Doc Gardening

This repo does not currently depend on a platform-native recurring automation.
Use a manual weekly doc-gardening pass instead:

1. Run `./scripts/execplan/check.sh`.
2. Search for deprecated legacy-path regressions with the repo validation
   scripts.
3. Fix stale links, outdated ownership notes, and docs that no longer match the
   code.
4. Update the relevant active plan or add a completed note if the cleanup was
   substantial.

## Reference Note

The requested external `docs/PLANS.md` reference file was not present at the
provided absolute path during this migration, so this repo-local version was
adapted from the OpenAI cookbook guidance and the repository’s actual workflow.
