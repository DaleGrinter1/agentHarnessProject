---
name: sandbox-agent-scaffolder
description: Create or extend a sandboxed agent by scaffolding the expected config, entrypoint, env surface, docs, and validation hooks in the repo's preferred structure. Use when adding a new agent, splitting one agent into several roles, or standardizing an ad hoc sandboxed worker.
---

# Sandbox Agent Scaffolder

Use this skill when the task is to introduce a new sandboxed agent or bring an
existing one into a consistent repo shape.

## Read First

1. `AGENTS.md`
2. `ARCHITECTURE.md`
3. `docs/references/modal-sandbox.md`
4. `docs/RELIABILITY.md`
5. The relevant active initiative in `docs/exec-plans/active/` when the work is
   non-trivial

## Workflow

1. Clarify the agent's role, inputs, outputs, and sandbox needs.
2. Reuse the repo's existing harness and file patterns before inventing a new
   structure.
3. Scaffold the smallest complete agent shape:
   config surface, execution entrypoint, env contract, and validation hook.
4. Define mounts, workdir, timeout, network expectations, and any required
   packages explicitly.
5. Keep the agent's responsibility narrow and easy to reason about.
6. Update the canonical docs and active plan state to reflect the new agent.
7. Validate the scaffold with the narrowest meaningful smoke test first, then
   broader harness checks.

## Primary Targets

- agent configuration files
- sandbox entrypoints and wrappers
- `.env.example`
- agent-facing docs and exec-plan files
- tests or smoke-test scripts that prove the scaffold works

## Guardrails

- Do not copy-paste a near-duplicate agent without documenting why a separate
  role is needed.
- Prefer one clean scaffold pattern across agents rather than custom layouts.
- Keep setup requirements explicit instead of relying on hidden defaults.
- Avoid mixing orchestration logic into a single agent's task code unless the
  design clearly calls for it.

## Validation

- Run the most direct smoke test for the new agent first.
- Exercise the expected sandbox path with the documented helper or wrapper.
- Run `./scripts/validate-harness.sh` for harness-facing changes.
- Run `./scripts/execplan/check.sh` when docs or plan state change.
- Do not claim an agent scaffold is ready without a concrete execution check.

## Handoff Notes

Record:

- the new agent's purpose and scope
- required env vars and mounts
- timeout, network, and workdir expectations
- the command that proves the scaffold works
