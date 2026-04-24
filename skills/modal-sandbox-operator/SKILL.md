---
name: modal-sandbox-operator
description: Operate, debug, and evolve the repo's Modal sandbox workflow by using the documented entrypoints, validating common execution paths, and keeping scripts, docs, and plan state aligned. Use for Modal sandbox runs, wrapper/helper changes, env-loading issues, mount/workdir bugs, and harness troubleshooting.
---

# Modal Sandbox Operator

Use this skill when the main task is to run, troubleshoot, or modify the
repository's Modal sandbox workflow.

## Read First

1. `AGENTS.md`
2. `docs/references/modal-sandbox.md`
3. `README.md`
4. `ARCHITECTURE.md`
5. The relevant active initiative in `docs/exec-plans/active/` when the work is
   non-trivial

## Primary Targets

- `scripts/modal_sandbox_demo.py`
- `scripts/run_modal_sandbox.sh`
- `.env`
- `.env.example`
- `docs/references/modal-sandbox.md`
- active exec-plan files for sandbox-related initiatives

## Workflow

1. Confirm whether the task is operational usage, bugfixing, or workflow
   evolution.
2. Use the documented entrypoint that best matches the task:
   `scripts/run_modal_sandbox.sh` for the common repo-mounted case,
   `python scripts/modal_sandbox_demo.py` for direct flag-level control.
3. Reproduce the current behavior with the smallest command that demonstrates
   the issue or desired path.
4. Inspect the relevant inputs in order:
   Modal auth, `.env` loading, app naming, mount selection, remote path,
   workdir, dependency installation, network blocking, timeout, and resource
   flags.
5. Apply the smallest safe change in scripts or docs.
6. Re-run the narrowest useful sandbox check first, then broader harness
   validation.
7. Update the relevant plan and state files when the work is non-trivial.

## Common Modes

- **Basic smoke run**: confirm the helper or wrapper can execute a minimal
  command successfully.
- **Mount and workdir validation**: verify the repo is mounted where the docs
  claim and the command runs in the expected directory.
- **Env troubleshooting**: check whether local `.env` values are loaded and
  whether required variables are documented in `.env.example`.
- **Isolation checks**: validate behavior with flags like `--block-network`.
- **Harness evolution**: adjust CLI flags, defaults, or printed diagnostics
  without expanding the script scope unnecessarily.

## Guardrails

- Prefer the documented wrapper before inventing a new sandbox entrypoint.
- Keep the helper generic; do not bake product-specific logic into harness
  infrastructure.
- Avoid broad refactors when a focused script, env, or doc fix is enough.
- Keep failure output explicit and easy to diagnose.
- If behavior changes, update the canonical docs in
  `docs/references/modal-sandbox.md`.
- For non-trivial changes, use the repo's exec-plan workflow rather than
  tracking state only in chat.

## Validation

- Run the smallest direct command that proves the target behavior.
- When changing helper or wrapper behavior, exercise both the direct Python
  helper and the shell wrapper when relevant.
- Run `./scripts/validate-harness.sh` for harness-facing changes.
- Run `./scripts/execplan/check.sh` when plan/state files are touched or when
  the change affects repo knowledge.
- Do not claim the sandbox path works without a concrete command-based check.

## Handoff Notes

Record:

- the command path used to reproduce or validate behavior
- whether the issue involved auth, env loading, mounts, workdir, network, or
  resource settings
- what script or doc now defines the intended behavior
- any remaining setup requirement or operational risk
