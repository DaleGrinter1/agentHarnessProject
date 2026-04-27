# Scale Modal Sandbox Harness Into An Agent Harness

This ExecPlan is a living document. Keep `Progress`, `Surprises & Discoveries`,
`Decision Log`, and `Outcomes & Retrospective` current as work proceeds.

This plan must be maintained in accordance with `docs/PLANS.md`.

## Purpose / Big Picture

Turn the current Modal sandbox command runner into the foundation for a
controlled OpenAI Agents SDK harness. After this initiative, the repo should
have a small orchestrator that can delegate bounded coding or research tasks to
sandboxed workers, track their state, summarize their results, and enforce
resource limits before any expensive parallel or GPU work is exposed.

## Surprises & Discoveries

- Observation: The current repo already has the sandbox execution plane but not
  the agent control plane.
  Evidence: `scripts/modal_sandbox_demo.py` and `scripts/run_modal_sandbox.sh`
  support repo-mounted command execution, while `src/` contains no product
  harness yet.

- Observation: The repo's local skills already map to the blog's next harness
  layers.
  Evidence: `skills/multi-agent-orchestrator/`,
  `skills/sandbox-agent-scaffolder/`, and `skills/agent-observability/`.

- Observation: The first control-plane layer can be tested without Modal
  credentials by injecting a fake command executor.
  Evidence: `tests/test_agent_harness.py` validates Modal helper output parsing,
  success, command failure, and timeout handling.

- Observation: Operator-visible status does not need a UI framework yet.
  Evidence: `scripts/agent_status.py` renders the latest JSONL worker records
  as a terminal dashboard, and `--watch` can follow worker status from another
  terminal.

- Observation: Modal SDK versions can complete `Sandbox.wait()` without
  returning the process exit code directly.
  Evidence: A live worker smoke run produced sandbox id
  `sb-VcJbcRalaRfh9Kun5TDEHk`, stdout `Python 3.12.10`, and `returncode:
  null`; Modal's reference exposes the completed exit code through
  `Sandbox.returncode` and `Sandbox.poll()`.

## Decision Log

- Decision: Treat this as a new initiative rather than extending the completed
  `modal-sandbox-hardening` plan.
  Rationale: The existing plan completed the command-runner workflow; this work
  adds orchestration, state, quotas, and observability around it.
  Date/Author: 2026-04-27 / Codex

- Decision: Start with manager-style orchestration where the orchestrator calls
  workers as bounded tools.
  Rationale: The orchestrator should keep ownership of the final answer while
  workers perform short-lived implementation bursts and return concise
  summaries.
  Date/Author: 2026-04-27 / Codex

- Decision: Require quota and run metadata before GPU or broad async fan-out.
  Rationale: Parallel sandboxes are powerful but can create cost and debugging
  risk if the harness cannot identify active workers and resource usage.
  Date/Author: 2026-04-27 / Codex

- Decision: Start with a small typed Python contract rather than adopting the
  full Agents SDK runtime in the first patch.
  Rationale: The current repo has no product application yet, so a narrow
  `WorkerTask` and `WorkerResult` surface gives later Agents SDK integration a
  stable boundary while preserving the existing Modal runner.
  Date/Author: 2026-04-27 / Codex

## Outcomes & Retrospective

Not started. The first completed outcome should be a minimal, observable
orchestrator-to-worker path using the existing Modal sandbox helper or a narrow
Agents SDK wrapper around it.

## Context and Orientation

The repository is currently a lightweight harness scaffold. Modal sandbox
execution lives in `scripts/modal_sandbox_demo.py`, with
`scripts/run_modal_sandbox.sh` providing the preferred repo-mounted command
path. Usage notes live in `docs/references/modal-sandbox.md`.

The Modal blog notes retained in
`docs/references/modal-openai-agents-sdk-blog.md` are informative guidance for
this initiative. The repo remains the system of record, so implementation
choices must still follow `AGENTS.md`, `ARCHITECTURE.md`, `docs/RELIABILITY.md`,
and `docs/SECURITY.md`.

The first harness contract lives in `src/agent_harness/`. `WorkerTask` is the
orchestrator-owned request: `task_id`, `objective`, `command`, `worker_name`,
workspace paths, timeout, resource class, network setting, package additions,
and non-secret environment values. `WorkerResult` is the machine-readable
summary returned to the orchestrator: task id, worker name, status, command,
return code, timestamps, duration, resource class, sandbox id, app name,
workdir, stdout/stderr tails, summary, and error.

Terminal worker statuses are `succeeded`, `failed`, `timed_out`, and
`runner_error`. The orchestrator owns final user-facing synthesis. The Modal
worker runner owns only the bounded sandbox execution request and concise
result translation.

## Plan of Work

First, define the minimal harness API: orchestrator input, worker task shape,
worker result summary, run metadata, and failure states. Then scaffold a small
agent harness module and smoke command that can run one sandboxed worker against
the repo. After the single-worker path is visible and testable, add an async
worker pool with quotas, status listing, timeouts, cancellation, and summaries.
Only after the pool is reliable should the initiative add snapshot branching or
GPU resource classes.

## Concrete Steps

1. Define the control-plane contract.

   ```sh
   rg "modal_sandbox|run_modal_sandbox|agent" scripts src docs
   ```

   Success looks like a short design note in this plan naming the orchestrator,
   worker input, worker output, and run metadata fields.

2. Scaffold a minimal single-worker harness.

   ```sh
   python -m py_compile scripts/modal_sandbox_demo.py
   python -m unittest tests.test_agent_harness
   python scripts/run_agent_worker.py \
     --task-id smoke \
     --objective "prove the worker path" \
     --cmd "python -V"
   scripts/run_modal_sandbox.sh "python -V"
   ```

   Success looks like one documented command that invokes a bounded worker in a
   Modal sandbox and records sandbox id, command, return code, duration, and a
   concise result summary.

3. Add worker-pool state and quotas.

   ```sh
   python scripts/agent_status.py
   ./scripts/validate-harness.sh
   ./scripts/execplan/check.sh
   ```

   Success looks like active worker state being listable by id, with explicit
   max concurrency and no GPU access unless quota configuration enables it.

4. Add snapshot and skill hooks only after the pool exists.

   Success looks like snapshot ids and selected skills being recorded in run
   metadata, with secrets excluded from prompts, manifests, snapshots, and
   generated artifacts.

## Machine State

Document the JSON handoff files for this initiative:

- `state/feature-list.json` is the canonical implementation checklist.
- Every feature starts with `"passes": false`.
- `state/session-state.json` tracks the active feature, blockers, next action,
  and handoff rules.
- `state/progress.jsonl` is append-only and records meaningful checkpoints with
  structured evidence.

## Progress

- [x] (2026-04-27T00:55:00Z) Captured the Modal blog learnings as a repo
  reference and opened this active initiative.
- [x] (2026-04-27T02:20:38Z) Define the minimal orchestrator and worker
  contract.
- [x] (2026-04-27T02:20:38Z) Scaffold the single-worker Python path with
  mocked runner validation.
- [x] (2026-04-27T02:33:28Z) Add a dependency-free terminal status dashboard
  backed by JSONL worker records.
- [x] (2026-04-27T02:57:51Z) Fix Modal sandbox return-code compatibility so a
  successful live sandbox command is not misclassified as failed when
  `Sandbox.wait()` returns `None`.
- [ ] (2026-04-27T00:55:00Z) Scaffold and validate a single sandboxed worker
  path.
- [ ] (2026-04-27T00:55:00Z) Add quota-bound async worker-pool state.
- [ ] (2026-04-27T00:55:00Z) Add snapshot and skill hooks after the pool is
  observable.

## Testing Approach

Use the narrowest smoke path first: a worker should run a harmless command in a
repo-mounted Modal sandbox and return structured metadata. Add failure-path
checks for non-zero exits, timeout, cancellation, and blocked network behavior.
For documentation and plan state changes, run `./scripts/execplan/check.sh` and
`./scripts/validate-harness.sh`.

## Constraints & Considerations

- Keep OpenAI API keys, Modal credentials, and provider secrets outside prompts,
  committed files, snapshots, and generated artifacts.
- Keep worker sessions short-lived and summarize them back to the orchestrator.
- Do not expose GPU resource classes until quotas and operator-visible status
  exist.
- Prefer repo-local skills for specialized instructions rather than adding a
  large permanent orchestrator prompt.
- Preserve the existing command-runner entrypoints while adding the higher-level
  harness.
