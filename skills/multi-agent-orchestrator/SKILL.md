---
name: multi-agent-orchestrator
description: Design or refine how multiple sandboxed agents coordinate by defining task routing, handoff boundaries, shared state rules, retries, and failure handling. Use when adding agent-to-agent workflows or reducing orchestration ambiguity.
---

# Multi-Agent Orchestrator

Use this skill when the task is to make multiple sandboxed agents work together
predictably.

## Read First

1. `AGENTS.md`
2. `ARCHITECTURE.md`
3. `docs/RELIABILITY.md`
4. The relevant active initiative, agent docs, and orchestration code

## Workflow

1. List the participating agents and the responsibility of each one.
2. Define ownership boundaries so agents do not overlap or fight over the same
   work.
3. Specify the handoff format, status markers, and success or failure states.
4. Decide retry, timeout, cancellation, and escalation behavior.
5. Keep orchestration logic separate from individual agent task logic when
   practical.
6. Validate at least one realistic end-to-end multi-agent path.
7. Update docs and plan state so a future agent can resume the workflow
   without re-deriving the design.

## Design Focus

- task routing and role selection
- machine-readable handoffs when practical
- shared state ownership
- failure containment between agents
- retry boundaries
- operator-visible status and outcome reporting

## Guardrails

- Avoid overlapping ownership between agents.
- Fail clearly when an upstream agent returns unusable output.
- Prefer deterministic handoff contracts over implicit conventions.
- Do not hide orchestration policy inside scattered agent-specific files if one
  central place can express it more clearly.

## Validation

- Run the narrowest realistic multi-agent scenario first.
- Confirm both success and failure paths are understandable.
- Run the most relevant direct tests for orchestration code first.
- Run broader harness validation when the workflow touches shared sandbox
  infrastructure or repo docs.

## Handoff Notes

Record:

- the participating agents and their boundaries
- the handoff contract used
- retry, timeout, and cancellation rules
- the scenario used to validate the orchestration path
