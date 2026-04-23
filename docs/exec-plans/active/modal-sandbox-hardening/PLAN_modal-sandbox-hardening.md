# Harden Modal Sandbox Helper For Reuse

This ExecPlan is a living document. Keep `Progress`, `Surprises & Discoveries`,
`Decision Log`, and `Outcomes & Retrospective` current as work proceeds.

This plan must be maintained in accordance with `docs/PLANS.md`.

## Purpose / Big Picture

Turn the repo’s Modal sandbox demo into a repeatable local workflow for running
commands against a repo-mounted sandbox with sensible defaults. After this
change, a contributor should be able to authenticate once, run a single wrapper
command, and get a Modal sandbox with the repository mounted at `/workspace`
without remembering the low-level flags.

## Surprises & Discoveries

- Observation: The existing helper was already enough to prove auth and basic
  sandbox creation, so the remaining gap was workflow ergonomics rather than
  Modal API support.
  Evidence: Successful local repo-mounted run reported by the user.

## Decision Log

- Decision: Keep the existing Python script as the implementation entrypoint and
  add a shell wrapper for the common repo-mounted case.
  Rationale: This preserves one configurable code path while giving the user a
  faster default command.
  Date/Author: 2026-04-23 / Codex

- Decision: Default the Modal app name from the repository name when an
  explicit value is not provided.
  Rationale: Reusing a stable app name improves continuity without forcing
  per-user manual configuration.
  Date/Author: 2026-04-23 / Codex

## Outcomes & Retrospective

The repo now has a more practical Modal sandbox workflow: the Python helper
supports repo-aware defaults and explicit resource flags, and a new shell
wrapper provides a one-command repo-mounted entrypoint. The lightweight
validation passed, including Python compilation and the repo harness checks.
Future work could add higher-level presets for common agent tasks, but the
current setup is already solid for local command execution inside Modal.

## Context and Orientation

The current Modal helper lives in `scripts/modal_sandbox_demo.py`. It creates a
Modal app, defines a runtime image, optionally uploads a local directory, and
runs a shell command inside a Sandbox. The repo already ignores `.env` and
ships `.env.example` for local token configuration. Supporting usage notes live
in `docs/references/modal-sandbox.md`.

## Plan of Work

Update `scripts/modal_sandbox_demo.py` to support repo-aware defaults and
resource flags, add `scripts/run_modal_sandbox.sh` as a convenience wrapper for
the common mount-and-run flow, refresh the `.env.example` comments, and update
the Modal sandbox reference doc. Validate with Python compilation plus the repo
knowledge-base checks.

## Concrete Steps

1. Review the current helper and docs:

   ```sh
   sed -n '1,260p' scripts/modal_sandbox_demo.py
   sed -n '1,260p' docs/references/modal-sandbox.md
   ```

   Success looks like understanding the existing flags and usage notes.

2. Update the helper, add the wrapper, and refresh docs.

   Success looks like the helper supporting `--mount-repo` and the wrapper
   delegating to the Python entrypoint.

3. Validate the implementation:

   ```sh
   ./.venv-modal/bin/python -m py_compile scripts/modal_sandbox_demo.py
   ./scripts/validate-harness.sh
   ```

   Success looks like both commands exiting successfully.

## Machine State

Document the JSON handoff files for this initiative:

- `state/feature-list.json` is the canonical implementation checklist.
- Every feature starts with `"passes": false`.
- `state/session-state.json` tracks the active feature, blockers, next action,
  and handoff rules.
- `state/progress.jsonl` is append-only and records meaningful checkpoints with
  structured evidence.

## Progress

- [x] (2026-04-23T06:20:00Z) Defined the feature scope and selected the wrapper
  plus repo-aware-defaults approach.
- [x] (2026-04-23T06:21:00Z) Validated the updated helper, wrapper, docs, and
  exec-plan state.

## Testing Approach

Compile the Python helper with `py_compile`, inspect the wrapper help text, and
run `./scripts/validate-harness.sh` to ensure the repo docs and execution-plan
state remain consistent.

## Constraints & Considerations

- Do not store real Modal credentials in tracked files.
- Keep the shell wrapper simple and transparent so it is easy to inspect.
- Preserve the direct Python entrypoint for advanced use cases.
