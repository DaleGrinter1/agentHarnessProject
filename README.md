# Project Starter

This repository is a lightweight starter for an AI-assisted software project
with a reusable Modal-based sandbox harness for remote command execution. It is
still intentionally generic enough to define the actual product later without
having to reorganize the repo first.

## What This Repo Includes

- `AGENTS.md`: working agreement for agents operating in this repo
- `ARCHITECTURE.md`: top-level repo structure and implementation boundaries
- `docs/`: source-of-truth documents for product specs, design, planning,
  reliability, security, references, and generated artifacts
- `skills/`: repo-local reusable agent workflows for recurring tasks
- `scripts/`: lightweight automation, validation, and sandbox harness entrypoints
- `src/`: application code
- `tests/`: automated tests

## Recommended Reading Order

1. `AGENTS.md`
2. `README.md`
3. `ARCHITECTURE.md`
4. the product specs index in `docs/product-specs`
5. `docs/PLANS.md`
6. `docs/RELIABILITY.md`
7. `docs/SECURITY.md`

## Current State

This repo is a scaffold, not a finished application. The documentation is
written to be:

- safe for agents to follow before project details exist
- easy for humans to replace with project-specific decisions later
- explicit about what is still undecided

The repo also includes a working Modal sandbox path for harness-style
development:

- `scripts/modal_sandbox_demo.py`: configurable Python entrypoint for launching
  a Modal sandbox
- `scripts/run_modal_sandbox.sh`: preferred wrapper for mounting the repo at
  `/workspace` and running commands there
- `docs/references/modal-sandbox.md`: quickstart and usage notes

## How To Customize It

1. Replace the placeholder sections in the product specs index under
   `docs/product-specs` with real goals,
   users, and non-goals.
2. Update `ARCHITECTURE.md` once you know the language, modules, and data
   flow.
3. Fill in `docs/RELIABILITY.md` with the actual test, performance, and failure
   expectations.
4. Fill in `docs/SECURITY.md` before handling secrets, credentials, or
   production systems.
5. Add code under `src/` and matching tests under `tests/`.

## Working Norms

- Prefer small, reviewable changes.
- Keep docs aligned with reality.
- Do not add dependencies casually.
- Avoid broad refactors until the product direction is clear.

## Harness Workflow

Before a product exists, this repo should help with disciplined change-making
more than application behavior.

1. Read `AGENTS.md`, this file, and the relevant docs in `docs/`.
2. For non-trivial work, create or update an active initiative under
   `docs/exec-plans/active/` using `docs/exec-plans/PLAN_TEMPLATE.md`.
3. Keep the durable narrative in one `PLAN_<initiative>.md`.
4. Track implementation checklist and handoff state in JSON under `state/`.
5. Run `./scripts/execplan/check.sh` before concluding harness changes.

For repo-mounted remote execution with the current harness:

```sh
scripts/run_modal_sandbox.sh "python -V && ls -la"
```

## OpenAI Docs MCP

This repo includes a VS Code MCP configuration at `.vscode/mcp.json` for the
OpenAI developer documentation server:

- Server name: `openaiDeveloperDocs`
- Server URL: `https://developers.openai.com/mcp`

For Codex CLI and the Codex IDE extension, the official setup is shared at the
user level rather than stored in the repo. Configure it once with:

```sh
codex mcp add openaiDeveloperDocs --url https://developers.openai.com/mcp
codex mcp list
```

`AGENTS.md` already instructs agents to use this MCP server for OpenAI-related
work.

## Validation

There is no product-specific application toolchain configured yet.

Current harness validation:

- `./scripts/execplan/check.sh`
- `./scripts/validate-harness.sh`

Current sandbox harness entrypoints:

- `scripts/run_modal_sandbox.sh`
- `python scripts/modal_sandbox_demo.py --help`

Before declaring product work complete in the future, define and document:

- test command(s)
- lint/format command(s)
- any environment setup needed for local development
