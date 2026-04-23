# Harness

This repository is currently a generic harness scaffold, not a product repo.
Its job is to make future AI-assisted development safer, clearer, and easier to
validate.

## Harness Goals

- provide a predictable place for source, tests, docs, and plans
- make agent workflows explicit before product details exist
- keep validation lightweight and honest
- avoid premature framework or architecture lock-in

## What Belongs Here Now

- repo operating guidance
- documentation templates that can later be made project-specific
- small scripts that validate or support the harness itself
- minimal automation that does not assume a language stack

## What Does Not Belong Here Yet

- user-facing product features
- framework-specific app structure without a clear project need
- dependency-heavy tooling added only for polish
- automation that implies a deployment or runtime choice

## Practical Workflow

1. Read `AGENTS.md`, `README.md`, and the relevant docs.
2. If the change is non-trivial, add an execution plan under
   `docs/exec-plans/`.
3. Make the smallest high-confidence change.
4. Update docs if the repo workflow or expectations changed.
5. Run harness validation.

## Maturity Checklist

The harness is in reasonable shape when it has:

- clear navigation for agents and humans
- explicit source-of-truth docs
- a standard place for execution plans
- at least one working validation command
- no fake claims about product behavior or test coverage

## Open Decisions

These should stay open until the future project makes them concrete:

- programming language and runtime
- application framework
- real test and lint toolchain
- deployment model
- product-specific architecture
