# Add repo-local skills for recurring agent workflows

This ExecPlan is a living document. Keep `Progress`, `Surprises & Discoveries`,
`Decision Log`, and `Outcomes & Retrospective` current as work proceeds.

This plan must be maintained in accordance with `docs/PLANS.md`.

## Purpose / Big Picture

This change adds reusable repo-local skills so future agents can follow
consistent workflows for plan maintenance, bugfixes with regression coverage,
doc hygiene, Modal sandbox operations, agent scaffolding, contract reviews,
observability, and multi-agent orchestration. After this lands, an agent should
be able to discover the skills directory, select the right workflow, and
execute common harness tasks with less ambiguity.

## Surprises & Discoveries

- Observation: Creating a repo-local hidden `.codex/` directory was blocked in
  this sandbox.
  Evidence: `mkdir -p .codex/skills` returned `Operation not permitted`.
- Observation: The repo did not already contain a tracked skills directory.
  Evidence: a filesystem scan found no existing `SKILL.md` files in the repo.

## Decision Log

- Decision: Create the skills in a tracked top-level `skills/` directory.
  Rationale: It keeps the skills visible and versioned in the repo without
  requiring a hidden directory that this environment would not let me create.
  Date/Author: 2026-04-23 / Codex
- Decision: Start with a small set of skills tied to repeated harness
  workflows, then expand only when a new workflow proves worth standardizing.
  Rationale: These are high-frequency, easy-to-do-inconsistently tasks that
  benefit from standardization without turning the skills directory into a grab
  bag.
  Date/Author: 2026-04-23 / Codex
- Decision: Add a second wave of agent-focused skills before product code
  expands further.
  Rationale: The project goal is to run multiple agents in separate sandboxes,
  so codifying scaffolding, contract audits, orchestration, and observability
  early will make later implementation work more consistent.
  Date/Author: 2026-04-23 / Codex

## Outcomes & Retrospective

Eight repo-local skills now exist:

- `execplan-maintainer`
- `bugfix-with-regression-test`
- `doc-gardener`
- `modal-sandbox-operator`
- `sandbox-agent-scaffolder`
- `sandbox-contract-auditor`
- `multi-agent-orchestrator`
- `agent-observability`

The repo routing docs now mention the `skills/` directory so future contributors
can discover and use these workflows intentionally. The skill inventory now
covers both general harness maintenance and the first layer of agent-specific
workflow guidance for a multi-sandbox system.

The skills are intentionally small and workflow-specific. They are a good fit
for this repo because they standardize repeated harness motions without adding a
lot of extra policy text.

## Context and Orientation

The repo already has durable planning and validation through `AGENTS.md`,
`docs/PLANS.md`, `docs/exec-plans/`, and `scripts/execplan/check.sh`. What it
lacked was reusable task-level guidance for common agent motions. The new
tracked `skills/` directory holds one folder per workflow, each with a required
`SKILL.md`.

## Plan of Work

Create a new active initiative for this skill scaffolding work. Then add
skill folders under `skills/`, each with concise trigger metadata and workflow
instructions. Finally, update the repo routing docs so the new skills are
discoverable and run the repo validation commands.

## Concrete Steps

Run from the repo root:

```sh
mkdir -p docs/exec-plans/active/skill-scaffolding/state skills
python3 scripts/execplan/validate-state.mjs
./scripts/execplan/check.sh
./scripts/validate-harness.sh
```

Expected result: the new plan and state validate, the skills exist under
`skills/`, and the repo knowledge checks still pass.

## Machine State

Document the JSON handoff files for this initiative:

- `state/feature-list.json` is the canonical implementation checklist.
- Every feature starts with `"passes": false`.
- `state/session-state.json` tracks the active feature, blockers, next action,
  and handoff rules.
- `state/progress.jsonl` is append-only and records meaningful checkpoints with
  structured evidence.

## Progress

- [x] (2026-04-23T03:08:14Z) Created the active initiative layout and confirmed
  the repo had no existing tracked skills directory.
- [x] (2026-04-23T03:15:00Z) Added the initial repo-local skills and updated
  routing docs.
- [x] (2026-04-23T03:16:00Z) Ran validation and finalized the initiative state.
- [x] (2026-04-23T11:40:00Z) Realigned the active initiative narrative after
  adding `modal-sandbox-operator` as a fourth skill.
- [x] (2026-04-23T11:55:00Z) Added four agent-focused skills for scaffolding,
  contract review, orchestration, and observability, then refreshed the
  initiative state.

## Testing Approach

- run `python3 scripts/execplan/validate-state.mjs`
- run `./scripts/execplan/check.sh`
- run `./scripts/validate-harness.sh`
- inspect the `skills/` directory for the expected skill folders

## Constraints & Considerations

- Keep the skill specs concise and workflow-oriented.
- Avoid extra skill documentation beyond `SKILL.md`.
- Prefer repo-local tracked skills over machine-local hidden config for this
  change.
