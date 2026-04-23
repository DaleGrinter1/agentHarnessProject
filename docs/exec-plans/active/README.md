# Active ExecPlans

Each active initiative gets one directory and one durable markdown plan.

Required contents:

- `PLAN_<initiative>.md`
- `state/feature-list.json`
- `state/session-state.json`
- `state/progress.jsonl`

Use markdown for narrative context and decisions. Use JSON for implementation
state and handoff. Do not create `tasks/` directories or per-task markdown files
unless explicitly requested.
