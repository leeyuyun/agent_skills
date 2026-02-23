# Source Selection

Use this file to decide which documentation to trust when model behavior or parameters conflict.

## Priority Order

1. Provider official docs (OpenAI, Midjourney, Stability, Black Forest Labs).
2. Provider official API references and release notes.
3. Community references only for examples, never as authority.

## Source Classification

### Core

- OpenAI image generation guide.
- Midjourney parameter list and parameter pages.
- Stability SDXL documentation and API schema docs.
- Black Forest Labs FLUX API and prompting guides.

Reason:
- These define authoritative parameter names, ranges, and supported behaviors.

### Support

- OpenAI Codex skill-authoring docs and `openai/skills` repository.

Reason:
- These guide how to package this skill for robust triggering and low-context operation.

### Exclude

- Marketplace listings and "awesome" aggregators as behavioral authority.
- Third-party wrappers that restate provider APIs without guarantees.

Reason:
- High drift risk and inconsistent validation.

## Update Trigger

Recheck official sources when:
1. A parameter fails unexpectedly.
2. A model version changes.
3. Output quality regresses after no prompt changes.
4. New resolution/quality limits appear in runtime errors.
