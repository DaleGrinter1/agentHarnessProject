# Execution Plans

This directory contains the repository’s durable execution tracking system.

## Layout

- `PLAN_TEMPLATE.md`: starting point for new initiative plans
- `active/`: current initiatives
- `completed/`: finished initiatives and historical plan records
- `tech-debt-tracker.md`: cross-initiative debt that should not disappear into
  chat history

## Active Initiative Rules

Each active initiative must contain exactly one `PLAN_<initiative>.md` and a
`state` directory with:

- `feature-list.json`
- `session-state.json`
- `progress.jsonl`

The markdown plan is the narrative source. The JSON files are the canonical
execution state.

## Default Workflow

1. Start from `PLAN_TEMPLATE.md`.
2. Create an initiative directory in `active/`.
3. Keep the plan, feature list, session state, and progress log in sync.
4. Do not create markdown task files as the default checklist mechanism.
5. Run `./scripts/execplan/check.sh`.
