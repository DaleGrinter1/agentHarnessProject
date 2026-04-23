---
name: agent-observability
description: Improve visibility into sandboxed agent behavior by standardizing logs, run metadata, sandbox IDs, timings, outputs, and failure diagnostics. Use when debugging agent runs, adding instrumentation, or making multi-agent systems supportable.
---

# Agent Observability

Use this skill when agent runs need better instrumentation, clearer diagnostics,
or more useful execution records.

## Read First

1. `AGENTS.md`
2. `docs/RELIABILITY.md`
3. `docs/SECURITY.md`
4. The relevant agent docs, sandbox entrypoints, and active initiative

## Workflow

1. Identify what operators or future agents need to answer during failures.
2. Add or refine structured run metadata at agent start and finish.
3. Capture sandbox identifiers, command path, duration, outcome, and important
   artifacts.
4. Make failure reasons explicit and easy to search.
5. Keep logs signal-rich rather than noisy.
6. Validate that both a successful run and a failing run are diagnosable.
7. Update docs and plan state with the new observability expectations.

## What Good Coverage Looks Like

- a run can be matched to a sandbox or execution identifier
- start and finish are visible
- failure reasons are explicit
- timing or duration is captured
- important outputs are traceable
- secrets are not logged

## Guardrails

- Do not log secrets or raw sensitive env values.
- Prefer structured logs or consistent key fields over ad hoc print noise.
- Capture enough context for another agent or human to resume quickly.
- Do not add verbose instrumentation that obscures the important state changes.

## Validation

- Exercise one successful path and one failing path when practical.
- Confirm the resulting logs or metadata answer the intended debugging
  questions.
- Run the most direct tests for any logging or metadata changes first.
- Run broader repo validation when the work changes shared docs or harness
  behavior.

## Handoff Notes

Record:

- what metadata is now emitted
- how runs are correlated to sandboxes or agents
- what failure signals operators should watch for
- any remaining blind spots in the diagnostic surface
