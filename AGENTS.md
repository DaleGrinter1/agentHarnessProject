# AGENTS.md

## Purpose
This repository is for building and maintaining a small AI-assisted software project.
Agents should optimize for correctness, small changes, readability, and easy review.

## How to work
- Read this file first.
- Then read `README.md`.
- Before major changes, read the relevant docs in `docs/`.
- Prefer small, reversible edits.
- Explain intended changes before making broad refactors.
- Run tests and linting before concluding work.
- Do not invent architecture; follow `docs/ARCHITECTURE.md`.
- Do not add dependencies unless necessary and justified.
- If uncertain, leave a short note in the plan and choose the safest path.

## Source of truth
- Product goals: `docs/PRODUCT.md`
- Architecture: `docs/ARCHITECTURE.md`
- Reliability expectations: `docs/RELIABILITY.md`
- Security constraints: `docs/SECURITY.md`
- Execution plans: `docs/exec-plans/`

## Coding standards
- Keep functions small.
- Prefer explicit names over clever abstractions.
- Add tests for behavior changes.
- Keep diffs reviewable.

## Validation
- Run project tests before finishing.
- If tests fail, summarize the cause clearly.
- Never claim something works unless it was validated.

## When asked to build something new
1. Restate the goal briefly
2. Inspect relevant files
3. Propose a small implementation plan
4. Implement incrementally
5. Run validation
6. Summarize what changed