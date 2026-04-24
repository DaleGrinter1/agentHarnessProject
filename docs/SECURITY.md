# Security

This document defines the safety rules for working in this repository. Replace
these defaults with project-specific requirements before handling real secrets
or production systems.

## Default Rules

### Secret Handling

- never commit secrets, credentials, tokens, or private keys
- use environment variables or local untracked files for secrets
- redact sensitive values from logs, examples, and test fixtures

### Protected Files

Until this section is customized, agents should treat these as requiring extra
care before editing:

- deployment or infrastructure configuration
- authentication and authorization logic
- secret-loading code
- CI/CD workflows

### Risky Actions

Require explicit approval before:

- deleting large sets of files
- changing security-sensitive defaults
- rotating or modifying secret material
- running commands that affect external systems
- making irreversible data migrations

## To Define

- which files or directories are never edited automatically
- what approval steps are required for production-impacting work
- any compliance, privacy, or audit constraints

## Guidance For Agents

Until this document is customized:

- choose the safest reasonable path
- prefer additive changes over destructive ones
- pause before editing code that touches credentials, auth, or deployment
- preserve history with `git mv` when relocating tracked files
