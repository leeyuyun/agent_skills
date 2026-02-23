# Iteration Playbook

Use this playbook when first-pass results miss the target.

## 1. Three-Round Loop

1. Round 1: Generate baseline with conservative controls.
2. Round 2: Adjust one dimension at a time (composition, lighting, style, detail).
3. Round 3: Final polish (artifact suppression, color balance, quality level, seed lock).

## 2. Failure -> Fix Mapping

### Subject incorrect or drifting

- Tighten noun phrases and action verbs.
- Move key subject tokens to the first sentence.
- Reduce style overload.

Model hints:
- Midjourney: lower `--c`, use fixed `--seed`.
- SDXL: raise steps moderately, keep weighted fragments simple.
- FLUX: simplify long prompt chains; keep structure explicit.
- OpenAI: restate exact subject constraints and pose in plain language.

### Composition wrong (framing, angle, object placement)

- Add explicit shot type and camera angle.
- Add distance cues (close-up, medium shot, wide shot).
- Add positional constraints (left/right/foreground/background).

Model hints:
- Midjourney: enforce `--ar` and reduce `--c`.
- FLUX: add stronger composition language in the first half of the prompt.
- SDXL/OpenAI: explicitly state framing and relative placement.

### Style mismatch

- Replace vague style terms with medium + era + texture cues.
- Add palette direction and lighting intent.

Model hints:
- Midjourney: tune `--s` and `--weird`.
- SDXL: adjust style fragments and weights.
- FLUX/OpenAI: use descriptive style clauses and remove contradictory adjectives.

### Low detail or artifacts

- Ask for material details and surface textures.
- Increase quality-related controls.
- Add defect avoidances (for example: extra limbs, broken geometry, watermark).

Model hints:
- Midjourney: raise `--q` (where supported).
- SDXL: increase `steps` and tune `cfg_scale`.
- FLUX: increase `steps` and set output format intentionally.
- OpenAI: set higher quality and specify clean rendering constraints.

## 3. Variant Strategy

For each user request, return:
1. Anchor variant: closest safe baseline.
2. Stretch variant: bolder style or composition.
3. Production variant: balanced quality and reliability.

Keep deltas explicit between variants so the user can choose intentionally.

## 4. Stop Criteria

Stop iterating when:
1. Core subject is stable across two consecutive runs.
2. Composition matches brief.
3. No critical artifacts remain.
4. Further edits only produce cosmetic tradeoffs.
