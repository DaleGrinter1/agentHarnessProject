# Modal And OpenAI Agents SDK Blog Notes

Source: https://modal.com/blog/building-with-modal-and-the-openai-agent-sdk

Read date: 2026-04-27

## Why This Matters Here

The blog describes a coding-agent harness that starts with shell execution,
moves that execution into Modal Sandboxes, then grows into a parallel,
state-aware research system. This repo already has the first reusable piece:
`scripts/modal_sandbox_demo.py` and `scripts/run_modal_sandbox.sh` provide a
repo-mounted Modal execution path. The next useful step is to treat that path as
the execution plane for a higher-level agent harness.

## Transferable Learnings

1. Keep the harness and compute boundary explicit.

   The harness should own model calls, orchestration, approvals, tracing, task
   state, and recovery. Modal Sandboxes should own command execution,
   filesystem mutation, dependency installation, resource shape, and snapshots.
   This mirrors the OpenAI sandbox guidance that separates the control plane
   from the sandbox execution plane.

2. Prefer sandboxed shell access over host shell access.

   A local `exec(command)` tool is easy to prototype and unsafe to operate. The
   repo should continue routing model-directed commands through Modal by
   default, with network, timeout, CPU, memory, and future GPU options made
   explicit.

3. Use sessions for user-facing continuity, not unlimited implementation memory.

   The orchestrator can carry high-level task memory. Worker/subagent sessions
   should be short-lived and summarized back to the orchestrator so tool logs,
   command output, and code exploration do not overwhelm the main context.

4. Use agents-as-tools before full handoffs for coding work.

   For this repo, the better first orchestration shape is a manager agent that
   stays responsible for the final answer and invokes bounded worker agents as
   tools. Full ownership handoffs can wait until a specialist truly needs to own
   the next user-facing turn.

5. Make parallelism visible and quota-bound.

   A subagent pool should track each worker by id, task, sandbox id, current
   status, active tool, resource class, start time, timeout, and final summary.
   Expensive resources, especially GPUs, need fixed quotas before they are
   exposed to model-directed orchestration.

6. Treat filesystem snapshots as both acceleration and memory.

   When workers all repeat setup, a snapshot can preserve a prepared workspace
   so later workers branch from the same dependency state. Snapshot ids should
   be stored as run metadata and never treated as a substitute for a concise
   worker summary.

7. Keep skills pluggable.

   Prompting for specialized work should live in skills or task files that an
   orchestrator can select, not in one ever-growing harness prompt. This repo
   already has local skills that can become the discovery layer for future
   sandboxed agents.

## Implications For This Repo

- Keep `docs/references/modal-sandbox.md` focused on the current command
  runner.
- Use `docs/exec-plans/active/agent-harness-scaling/` for the next initiative:
  an Agents SDK oriented harness that layers orchestration on top of the
  existing Modal wrapper.
- Do not add GPU defaults until quota and cost controls exist.
- Do not place secrets, Modal credentials, OpenAI keys, or provider tokens in
  prompts, task files, committed manifests, snapshots, or generated artifacts.
- Before exposing async subagents, add operator-visible run metadata and a
  narrow smoke scenario that proves success, failure, timeout, and cancellation
  behavior are understandable.

