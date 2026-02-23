# Model Profiles

Use this file to map one creative brief into provider-correct parameters.

## OpenAI GPT Image (`gpt-image-1`)

Use when strong text understanding and direct API control are needed.

Prompt strategy:
- Write explicit subject, environment, lighting, composition, and style intent.
- Fold avoidances into the prompt text (no dedicated negative-prompt field in this guide).
- Keep instructions concrete and visual, not abstract.

Reference image guidance:
- Use image input + instruction prompt together.
- Split instructions into two lists:
  - `Preserve`: pose/composition/palette/identity cues to keep.
  - `Change`: age, clothes, background, style, or lighting changes.
- Keep preserve/change statements short and non-conflicting.

Key controls:
- `size`: `1024x1024`, `1024x1536`, `1536x1024`.
- `quality`: `low`, `medium`, `high`, `auto`.
- `background`: `transparent`, `opaque`, `auto`.
- `output_format`: `png`, `jpeg`, `webp`.
- `output_compression`: `0-100` (for `jpeg`/`webp`).
- Moderation setting is available in the response configuration flow.

Observed limits noted in the guide:
- Higher latency than standard text responses.
- Text rendering in images can still be inconsistent.
- Exact composition and consistency may need iterative retries.

## Midjourney

Use when artistic stylization and fast creative exploration are needed.

Prompt strategy:
- Start with a concise, high-information base prompt.
- Add only relevant parameters.
- Keep exclusions concrete with `--no`.

Reference image guidance:
- Put reference image URL(s) before the text prompt.
- Use text prompt to state what to preserve and what to change.
- If image-weight controls are available in your Midjourney surface, tune them conservatively.

Common controls:
- `--ar` aspect ratio.
- `--c` (chaos): `0-100`.
- `--q` (quality): V7 supports `.25`, `.5`, `1`.
- `--s` (stylize): `0-1000`, default `100`.
- `--seed`: `0` to `4294967295`.
- `--weird` for unusual aesthetics.
- `--no` for unwanted objects/styles.

## SDXL (Stability)

Use when weighted prompts and stable diffusion-style control are preferred.

Prompt strategy:
- Split concept into weighted prompt fragments when the caller supports it.
- Use negative weights to reduce unwanted elements.
- Keep style and composition instructions separable for easier tuning.

Reference image guidance:
- Prefer img2img/inpainting workflows when the API surface supports them.
- Control edit strength with denoise/strength style settings from the runtime.
- Start medium strength, then move lower to preserve more or higher to transform more.

Common controls:
- `cfg_scale`: `0-35`, default near `7`.
- `steps`: typical `10-50` for quality/speed tradeoff.
- `seed`: fixed for reproducibility.
- `text_prompts[]` with per-fragment `weight` (negative weight to de-emphasize).

Resolution guidance:
- Prefer native SDXL-friendly presets (for example `1024x1024`, `1152x896`, `1216x832`, `1344x768`).

## FLUX (Black Forest Labs)

Use when detailed natural-language prompts and photoreal style control are needed.

Prompt strategy:
- Follow this structure:
  `shot type + subject + context + style + composition details + atmosphere + technical specs`
- Keep instructions explicit and descriptive.
- Do not emit a separate negative-prompt block for classic FLUX workflows.

Reference image guidance:
- Use image-conditioned mode only when your FLUX endpoint/runtime exposes it.
- Keep instruction text explicit about `preserve` and `change`.
- Avoid overloading with many style constraints in the same pass.

Common controls (`flux-pro-1.1` API profile):
- `width`, `height`: `256-1440`, each multiple of `32`.
- `steps`: `1-50` (default around `40`).
- `guidance`: `1.5-5`.
- `safety_tolerance`: `0-6`.
- `output_format`: `jpeg` or `png`.
- `prompt_upsampling`: boolean.

FLUX.2 notes:
- Resolution range from `64x64` up to `4MP`, width and height multiples of `16`.

## Quick Selection Heuristic

1. Choose OpenAI GPT Image for direct instruction following and API-native edits.
2. Choose Midjourney for stylistic exploration and strong aesthetic priors.
3. Choose SDXL for weighted-prompt control in diffusion pipelines.
4. Choose FLUX for highly descriptive cinematic prompts and robust prompt parsing.

## Reference Image Workflow Heuristic

1. Ask for one primary reference image first; add more only if needed.
2. Extract 3-6 `preserve` attributes and 2-5 `change` attributes.
3. Set edit strength:
   - `low`: preserve composition/identity.
   - `medium`: preserve layout, restyle appearance.
   - `high`: keep only broad structure.
4. Generate three variants with different strength levels.

## Sources

- OpenAI image generation guide: https://platform.openai.com/docs/guides/image-generation?image-generation-model=gpt-image-1
- Midjourney parameter docs:
  - https://docs.midjourney.com/hc/en-us/articles/32859204029709-Parameter-List
  - https://docs.midjourney.com/hc/en-us/articles/32099348346765-Chaos-Variety
  - https://docs.midjourney.com/hc/en-us/articles/32176522101773-Quality
  - https://docs.midjourney.com/hc/en-us/articles/32196176868109-Stylize
  - https://docs.midjourney.com/hc/en-us/articles/32604356340877-Seeds
  - https://docs.midjourney.com/hc/en-us/articles/32173351982093-No
- Stability SDXL docs:
  - https://staging-api.stability.ai/docs
  - https://stability.ai/sdxl-aws-documentation
- Black Forest Labs docs:
  - https://docs.bfl.ai/api-reference/models/generate-an-image-with-flux-11-%5Bpro%5D
  - https://docs.bfl.ai/guides/prompting_guide_flux2
  - https://docs.bfl.ai/api_integration/skills_integration
