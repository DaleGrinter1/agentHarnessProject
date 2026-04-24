# Core Beliefs

These beliefs shape how this repository supports long-running coding agents.

## Repository Knowledge Wins

- The repository is the system of record.
- `AGENTS.md` is a map, not an encyclopedia.
- Durable context belongs in checked-in docs and state files that can be
  validated.

## Plans Must Survive Context Loss

- Non-trivial work needs one durable markdown plan and machine-readable state.
- Active initiatives use one `PLAN_<initiative>.md` plus JSON state files.
- Handoffs should leave the next session able to resume without guesswork.

## Incremental Progress Beats One-Shotting

- Work one feature or milestone at a time.
- Leave the repo in a clean, reviewable state after each meaningful step.
- Progress should be visible in append-only records, not buried in chat.

## Small, Verifiable Changes

- Prefer small reversible edits.
- Keep functions and docs easy to review.
- Do not claim validation that was not run.

## Honest Scaffolding

Until the product is defined, prefer:

- better repo navigation
- better planning and validation
- safer defaults

Avoid:

- speculative product features
- architecture theater
- dependency-heavy tooling without a real need
