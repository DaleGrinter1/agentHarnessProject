# Project Starter

This repository is a lightweight starter for an AI-assisted software project.
It is intentionally generic so you can define the actual product later without
having to reorganize the repo first.

## What This Repo Includes

- `AGENTS.md`: working agreement for agents operating in this repo
- `docs/`: source-of-truth documents that define goals, architecture,
  reliability, security, harness workflow, and execution plans
- `scripts/`: lightweight automation that stays dependency-free unless a real
  project need appears
- `src/`: application code
- `tests/`: automated tests

## Recommended Reading Order

1. `AGENTS.md`
2. `README.md`
3. `docs/PRODUCT.md`
4. `docs/ARCHITECTURE.md`
5. `docs/RELIABILITY.md`
6. `docs/SECURITY.md`
7. `docs/HARNESS.md`

## Current State

This repo is a scaffold, not a finished application. The documentation is
written to be:

- safe for agents to follow before project details exist
- easy for humans to replace with project-specific decisions later
- explicit about what is still undecided

## How To Customize It

1. Replace the placeholder sections in `docs/PRODUCT.md` with real goals,
   users, and non-goals.
2. Update `docs/ARCHITECTURE.md` once you know the language, modules, and data
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
2. For non-trivial work, create an execution plan from
   `docs/exec-plans/TEMPLATE.md`.
3. Prefer doc, script, and structure improvements over speculative features.
4. Run `scripts/validate-harness.sh` before concluding harness changes.

## Validation

There is no language-specific toolchain configured yet.

Current harness validation:

- `scripts/validate-harness.sh`

Before declaring product work complete in the future, define and document:

- test command(s)
- lint/format command(s)
- any environment setup needed for local development
