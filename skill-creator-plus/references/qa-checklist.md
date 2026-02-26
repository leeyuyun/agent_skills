# QA Checklist

## Goal
Ensure generated skills include explicit, runnable QA coverage instead of format-only validation.

## Release Gate

All checks must pass:

1. `SKILL.md` includes a QA/Test section with clear pass/fail gate.
2. Script-based skills include at least one QA/test script under `scripts/`.
3. Script-based skills include `references/qa-checklist.md`.
4. `scripts/quick_validate.py <skill-folder>` passes.
5. The skill's QA script(s) run successfully and results are reported.

## Regression Focus

- Skills with scripts but missing QA gate language.
- Skills with QA language but no runnable QA scripts.
- Skills with scripts but no `references/qa-checklist.md`.
- False positives on non-script skills.

