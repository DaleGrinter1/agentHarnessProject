# Title

Configure OpenAI Docs MCP for this repository

## Goal

Provide a small, reviewable repo-local setup for the OpenAI developer docs MCP
server and document the matching Codex CLI setup.

## Scope

- In scope:
  - Add a repo-local VS Code MCP configuration for the OpenAI docs server.
  - Document how to use the same server with Codex CLI.
- Out of scope:
  - Installing global Codex configuration on the user's machine.
  - Adding any non-OpenAI MCP servers.

## Relevant Context

- Related docs:
  - `AGENTS.md`
  - `README.md`
  - `docs/HARNESS.md`
- Relevant files:
  - `.vscode/mcp.json`
  - `docs/exec-plans/2026-04-23-openai-docs-mcp.md`
- Constraints:
  - Keep the change additive and repo-local where possible.
  - Do not commit secrets or credentials.

## Plan

1. Inspect the existing repo guidance and validation.
2. Add the smallest repo-local MCP configuration.
3. Document the shared Codex CLI setup needed outside the repo.
4. Run harness validation.
5. Summarize outcomes and follow-ups.

## Risks

- Codex CLI MCP configuration is user-level, not repo-local.
- Different editors use different MCP config file locations.

## Validation

- Tests to run:
  - `scripts/validate-harness.sh`
- Lint/format checks to run:
  - None
- Manual checks, if any:
  - Confirm `.vscode/mcp.json` matches the official Docs MCP URL.

## Notes

This plan intentionally keeps the repo change small and avoids assuming a
specific editor beyond the documented VS Code MCP file location.
