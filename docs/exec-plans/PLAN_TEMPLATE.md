# <Short, action-oriented description>

This ExecPlan is a living document. Keep `Progress`, `Surprises & Discoveries`,
`Decision Log`, and `Outcomes & Retrospective` current as work proceeds.

This plan must be maintained in accordance with `docs/PLANS.md`.

## Purpose / Big Picture

Explain what someone gains after this change, how they can see it working, and
what behavior or workflow becomes possible.

## Surprises & Discoveries

Capture unexpected behaviors, bugs, implementation constraints, or workflow
insights that changed the approach.

- Observation:
  Evidence:

## Decision Log

Record each material decision.

- Decision:
  Rationale:
  Date/Author:

## Outcomes & Retrospective

Summarize what shipped, what remains, and what future contributors should learn
from the work.

## Context and Orientation

Describe the current state as if the reader knows nothing. Name key files and
paths explicitly. Define non-obvious terms.

## Plan of Work

Describe the sequence of edits in prose. Name the files or directories that
will change and what will be added, moved, or removed.

## Concrete Steps

List the exact commands to run, where to run them, and what a short successful
result looks like.

## Machine State

Document the JSON handoff files for this initiative:

- `state/feature-list.json` is the canonical implementation checklist.
- Every feature starts with `"passes": false`.
- `state/session-state.json` tracks the active feature, blockers, next action,
  and handoff rules.
- `state/progress.jsonl` is append-only and records meaningful checkpoints with
  structured evidence.

## Progress

Use timestamped checkboxes that always reflect reality.

- [ ] (YYYY-MM-DDTHH:MM:SSZ) Example incomplete step.
- [x] (YYYY-MM-DDTHH:MM:SSZ) Example completed step.

## Testing Approach

Describe the commands, observations, and acceptance checks that prove the work.

## Constraints & Considerations

List important safety, rollout, compatibility, or scope constraints.
