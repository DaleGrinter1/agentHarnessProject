# AGENTS.md

This file is the routing map. The repository itself is the system of record.

## Read Order

1. `AGENTS.md`
2. `README.md`
3. `ARCHITECTURE.md`
4. The doc most relevant to the task in `docs/`
5. For non-trivial work, `docs/PLANS.md`
6. Then `docs/exec-plans/index.md`

## Canonical Path Map

- Architecture map: `ARCHITECTURE.md`
- Product intent: `docs/product-specs`
- Design guidance: `docs/design-docs`
- Planning rules: `docs/PLANS.md`
- Active execution work: `docs/exec-plans/active`
- Completed execution history: `docs/exec-plans/completed`
- Reusable agent workflows: `skills`
- Reliability rules: `docs/RELIABILITY.md`
- Security rules: `docs/SECURITY.md`
- Reference material: `docs/references`
- Generated snapshots: `docs/generated`

## Routing By Work Type

- Product scope or user outcomes: read the product specs index in
  `docs/product-specs`
- Architecture or file ownership: read `ARCHITECTURE.md`
- UX, interaction, or visual direction: read `docs/DESIGN.md`, `docs/FRONTEND.md`, then `docs/design-docs/`
- Reliability, validation, or release risk: read `docs/RELIABILITY.md` and `docs/QUALITY_SCORE.md`
- Security-sensitive work: read `docs/SECURITY.md` first
- Non-trivial implementation or refactors: read `docs/PLANS.md` and work from an initiative in `docs/exec-plans/active/`
- Repeated repo workflows: check `skills/` for reusable task guidance

## Planning Read Order

For plan-driven work, read in this order:

1. `docs/exec-plans/PLAN_TEMPLATE.md`
2. `docs/exec-plans/index.md`
3. The initiative `PLAN_<initiative>.md`
4. `state/session-state.json`
5. `state/feature-list.json`
6. `state/progress.jsonl`

## Planning Rules

- Active initiatives use exactly one `PLAN_<initiative>.md` plus:
  - `state/feature-list.json`
  - `state/session-state.json`
  - `state/progress.jsonl`
- The markdown plan is the durable narrative.
- JSON state is the canonical implementation checklist and handoff state.
- Do not use markdown task files or `tasks/` directories as the default planning mechanism.

## Deprecated Paths

- Do not use the legacy hidden agent-metadata directory.
- Do not use the old product shortcut directory.
- Do not introduce new per-task markdown files in active initiatives unless
  explicitly requested.

## Validation

- Run `./scripts/execplan/check.sh` for execplan and knowledge-base validation.
- Run other project tests only when they exist and are relevant.

Use the OpenAI developer documentation MCP server for OpenAI API, ChatGPT, Apps SDK, Codex, and related OpenAI platform work when it is available.
