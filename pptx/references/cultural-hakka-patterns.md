# Cultural Hakka Patterns

Use this reference when the user asks for Hakka-floral, Taiwanese floral fabric, or similar culture-led visual language.

## Scope

- This file defines practical visual grammar for slide backgrounds and decorative systems.
- It does not claim a single canonical style; it provides production-safe defaults for deck design.

## Visual Grammar

1. Pattern logic:
- Prefer repeated tile systems over sparse random icons.
- Keep one dominant motif family per deck (for example: peony-led floral + vine lines).
- Support motifs with one secondary set only (for example: plum blossom dots).

2. Color logic:
- Use high-saturation warm cores for motifs.
- Keep text-support regions lower-contrast and lower-frequency than decorative regions.
- Avoid mixing cold neon-tech palettes with culture-floral themes in the same deck.

3. Composition logic:
- Define three tiers: `cover`, `section`, `content`.
- For `content` slides, reserve stable text lanes and keep high-frequency motifs outside those lanes.
- Decorative objects (for example fruit icons) should stay in edge or corner lanes unless explicitly requested.

## Safe Defaults

1. Background strategy:
- Build tile pattern first.
- Add motif-scale variation second.
- Add readability glaze last.

2. Theme token strategy:
- Centralize colors in one token source.
- Apply token pass to title/subtitle/body/footer/card/chart/flow components before final QA.

3. Review gate:
- Always produce three sample slides first (`cover/section/content`) for style approval.
- Do not batch-rollout full deck before this gate passes.

## Common Failure Patterns

1. Background replaced, but text components still use prior theme colors.
2. Decorative elements overlap text-safe zones.
3. Hard opaque panels that visually detach from patterned fabric language.
4. Uncontrolled motif density causing scan fatigue.
