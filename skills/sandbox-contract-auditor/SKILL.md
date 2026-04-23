---
name: sandbox-contract-auditor
description: Audit a sandboxed agent's execution contract by checking inputs, outputs, mounts, env vars, permissions, timeouts, and network policy against the documented intent. Use for isolation reviews, permission hardening, and pre-release safety checks.
---

# Sandbox Contract Auditor

Use this skill when reviewing whether a sandboxed agent has the minimum access
and runtime surface it actually needs.

## Read First

1. `AGENTS.md`
2. `docs/SECURITY.md`
3. `docs/RELIABILITY.md`
4. `docs/references/modal-sandbox.md`
5. The relevant active initiative and agent docs

## Workflow

1. Identify the agent's documented purpose and success path.
2. Enumerate what the agent can read, write, execute, and access over the
   network.
3. Compare the actual sandbox contract to the documented need.
4. Flag over-broad mounts, env exposure, package access, timeouts, or network
   permissions.
5. Tighten the contract with the smallest safe script, config, or doc change.
6. Re-test the intended behavior after hardening.
7. Record remaining risk and any follow-up work clearly in the active plan.

## What To Check

- input and output paths
- mounted directories and remote paths
- exposed env vars and secrets handling
- network policy
- timeout and resource settings
- dependency installation surface
- failure behavior when blocked access is attempted

## Guardrails

- Prefer least privilege.
- Do not accept undocumented access as harmless by default.
- Keep safety boundaries explicit in code and docs.
- If an agent needs broader access than expected, document the reason instead
  of silently normalizing it.

## Validation

- Prove the agent still succeeds on its intended path after hardening.
- Verify blocked or disallowed paths fail in an explicit, diagnosable way.
- Run `./scripts/validate-harness.sh` for harness-facing changes.
- Run `./scripts/execplan/check.sh` when docs or plan state change.

## Handoff Notes

Record:

- the audited agent and intended contract
- the access that was removed, narrowed, or confirmed
- the command or test used to prove the safe path still works
- any remaining contract ambiguity or operational risk
