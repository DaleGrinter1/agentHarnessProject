---
name: bugfix-with-regression-test
description: Handle bugfix work by reproducing the issue, adding a failing or targeted regression test when practical, applying the smallest safe fix, validating the result, and updating plan state. Use for defects, regressions, and reliability fixes.
---

# Bugfix With Regression Test

Use this skill when fixing a defect or behavior regression.

## Workflow

1. Read the relevant docs and active initiative state.
2. Reproduce the bug or define the failing behavior precisely.
3. Add a regression test when practical.
4. Make the smallest safe fix.
5. Re-run the relevant validation.
6. Update the active plan and JSON state with the result.

## Bugfix Rules

- Prefer a regression test before the fix when feasible.
- If a test is not practical, explain why in the plan or progress log.
- Avoid broad refactors unless the bug demands them.
- Keep failure handling explicit and easy to diagnose.

## Validation

- Run the most direct test command first.
- Then run broader repo validation that matches the change scope.
- Do not claim the bug is fixed without a concrete verification step.

## Handoff Notes

Record:

- what was broken
- how it was reproduced
- what test or check now protects it
- any remaining risk
