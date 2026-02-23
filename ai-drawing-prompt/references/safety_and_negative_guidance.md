# Safety And Negative Guidance

Apply safety constraints before prompt optimization.

## 1. Safety First

1. Reject disallowed intent (harm, exploitation, illegal instructions, non-consensual abuse).
2. Offer a safe substitute objective.
3. Continue only with compliant content.

## 2. Model-Specific Negative Handling

Use the negative or exclusion mechanism that the model actually supports.

### OpenAI GPT Image

- Use natural-language avoidances inside the main prompt.
- Keep avoidances concrete:
  - "no watermark"
  - "no extra fingers"
  - "avoid oversaturated neon colors"

### Midjourney

- Use `--no` for explicit exclusions.
- Keep exclusions short and visual.
- Do not use `--no` to bypass moderation or create disallowed outputs.

### SDXL

- Use weighted prompt fragments.
- Use negative weights to suppress unwanted traits where the pipeline supports weighted prompts.
- Keep one concern per weighted phrase for easier tuning.

### FLUX

- Assume no classic standalone negative-prompt channel for core workflows.
- Rewrite prompt positively:
  - Replace "no blur" with "sharp focus and crisp edges".
  - Replace "no clutter" with "minimal clean background".

## 3. Avoidance Taxonomy

Prefer this order:
1. Technical defects (artifacts, distortion, low detail).
2. Composition issues (cropping, framing, perspective mismatch).
3. Style mismatches (wrong era, palette, render medium).
4. Policy and legal boundaries (unsafe, disallowed, infringing requests).

## 4. Quality Guardrail Checklist

Before returning a prompt pack, verify:
1. Every exclusion is model-correct.
2. No unsupported parameters are present.
3. Unsafe intent is removed or refused.
4. Prompt still states positive desired outcome clearly.
