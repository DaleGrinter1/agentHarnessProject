# Reliability

This document defines how we validate behavior and handle failure. The details
below are intentionally conservative until the project has real requirements.

## Minimum Expectations

- new behavior should include tests when practical
- bug fixes should include a regression test when practical
- failures should be explicit and easy to diagnose
- validation should be run before claiming work is complete

## To Define

### Required Tests

- What test suites are required before merge?
- Which kinds of changes require unit, integration, or end-to-end tests?

### Performance Expectations

- Are there response-time, memory, or throughput targets?
- What performance regressions are unacceptable?

### Retries And Timeouts

- Which operations may retry?
- What are the timeout defaults and limits?
- When should the system fail fast instead?

### Failure Reporting

- How should user-visible failures be surfaced?
- What should be logged?
- What metadata is required for debugging?

## Guidance For Agents

Until concrete standards are added:

- prefer deterministic behavior over clever retries
- fail with clear messages rather than swallowing errors
- do not claim validation passed unless commands were actually run
