# AGENTS.md

## Purpose
This repository is an AI-assisted development harness. Optimize for
correctness, small changes, readability, and easy review.

## Start Here
- Read this file first.
- Then read `README.md`.
- Read the relevant docs in `docs/` before non-trivial changes.
- For non-trivial work, create an execution plan in `docs/exec-plans/`.
- Prefer small, reversible edits.
- Explain intended changes before making broad refactors.
- Run available validation before concluding work.
- Do not invent architecture; follow `docs/ARCHITECTURE.md`.
- Do not add dependencies unless necessary and justified.
- If uncertain, leave a short note in the plan and choose the safest path.

## Source of truth
- Product goals: `docs/PRODUCT.md`
- Architecture: `docs/ARCHITECTURE.md`
- Reliability expectations: `docs/RELIABILITY.md`
- Security constraints: `docs/SECURITY.md`
- Harness workflow: `docs/HARNESS.md`
- Execution plans: `docs/exec-plans/`

## Coding standards
- Keep functions small.
- Prefer explicit names over clever abstractions.
- Add tests for behavior changes.
- Keep diffs reviewable.

## Validation
- Run project tests before finishing when they exist.
- Run `scripts/validate-harness.sh` for harness-level checks.
- If tests fail, summarize the cause clearly.
- Never claim something works unless it was validated.

Always use the OpenAI developer documentation MCP server if you need to work with the OpenAI API, ChatGPT Apps SDK, Codex,… without me having to explicitly ask.