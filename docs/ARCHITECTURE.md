# Architecture

This document defines repo structure and implementation boundaries. It is
written to be useful even before the application architecture is decided.

## Current Structure

- `src/`: application code
- `tests/`: automated tests
- `docs/`: product, architecture, reliability, security, and execution plans

## Default Conventions

Until a project-specific architecture is defined, follow these defaults:

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
