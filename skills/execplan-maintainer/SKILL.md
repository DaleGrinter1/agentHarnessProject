---
name: execplan-maintainer
description: Keep an active initiative's PLAN_<initiative>.md, feature-list.json, session-state.json, and progress.jsonl aligned during non-trivial work. Use when creating a new initiative, resuming long-running work, or closing out a plan-driven change.
---

# ExecPlan Maintainer

Use this skill for any non-trivial repo work that should follow the repository's
markdown-plan-plus-JSON-state workflow.

## Read First

1. `AGENTS.md`
2. `docs/PLANS.md`
3. `docs/exec-plans/index.md`
4. The initiative `PLAN_<initiative>.md`
5. `state/session-state.json`
6. `state/feature-list.json`
7. `state/progress.jsonl`

## Core Workflow

1. Decide whether the task is non-trivial enough to need an active initiative.
2. If needed, create one initiative directory with exactly one `PLAN_<initiative>.md`.
3. Represent implementation checklist state in `feature-list.json`.
4. Represent current handoff state in `session-state.json`.
5. Append meaningful checkpoints to `progress.jsonl`.
6. Keep the markdown plan in sync with decisions, surprises, validation, and
   actual progress.

## Guardrails

- Do not create per-task markdown files by default.
- Do not create `tasks/` directories.
- Treat `feature-list.json` as the canonical checklist.
- Keep `progress.jsonl` append-only.
- Mark a feature as passing only after meaningful validation.

## Closeout

- Update `Outcomes & Retrospective`.
- Clear or advance `active_feature_id`.
- Set `next_action` to the real next step.
- Run `./scripts/execplan/check.sh`.
