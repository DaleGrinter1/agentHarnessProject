# Architecture

This document defines the canonical repo layout and implementation boundaries.
It is intentionally useful before a product architecture exists.

## System Of Record

Repository knowledge lives in checked-in documents, not in chat history.

- `AGENTS.md` is the routing map.
- `ARCHITECTURE.md` is the top-level structure map.
- `docs/` contains product, design, planning, reliability, security, and
  reference material.
- `docs/exec-plans/active/` contains current initiative plans and JSON state.
- `docs/exec-plans/completed/` contains finished plan history.

## Current Structure

- `src/`: application code
- `tests/`: automated tests
- `scripts/`: repo automation and validation
- `docs/product-specs`: canonical product intent
- `docs/design-docs`: design beliefs and deeper design docs
- `docs/exec-plans`: planning rules, active initiatives, completed history
- `docs/references`: external or internal supporting references
- `docs/generated`: generated snapshots such as schema summaries

## Default Conventions

Until a product-specific architecture is defined, follow these defaults:

- keep `src/` organized by domain or feature, not by abstract layers unless the
  project clearly benefits from that split
- keep modules small and explicitly named
- keep side effects near the edges of the system
- keep pure logic easy to test in isolation
- mirror important `src/` behavior with tests in `tests/`

## To Define Later

Replace this section with concrete answers once the project direction is known.

### Folders

- Which top-level folders are expected?
- Are generated files committed or ignored?
- Which docs are normative versus informative?

### Major Modules

- What are the main components of the system?
- Which modules own data access, business logic, and interfaces?

### Data Flow

- Where does input enter the system?
- How is it transformed and validated?
- Where are outputs persisted, returned, or emitted?

### Key Constraints

- What architectural decisions are already fixed?
- What coupling should be avoided?
- What performance or deployment constraints matter?

## Guidance For Agents

Until this document is customized:

- prefer simple files and shallow abstractions
- do not introduce framework-heavy structure without a clear need
- avoid cross-cutting refactors that imply an architecture choice
- keep repo knowledge aligned with the code and scripts that enforce it
