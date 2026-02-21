# Design And QA Reference

Use this reference for visual direction and final QA when producing PPTX output.

## Design Baseline

- Pick one dominant color and one accent. Avoid equal visual weight across all colors.
- Use clear type hierarchy:
  - Title: 36-44pt
  - Section header: 20-24pt
  - Body: 14-16pt
  - Caption: 10-12pt
- Keep minimum margins at 0.5".
- Keep spacing consistent (0.3" to 0.5" between blocks).
- Ensure every slide has a visual element (image, icon, chart, shape, or data callout).
- Confirm style before building new decks. Use `references/style-presets.md`.
- Record a style tuple before building:
  - Primary visual style: one from `A-F`
  - Layout grammar: one or two from `G`
  - Motion style: one from `H` when needed

## Layout Guidance

Vary layouts intentionally across slides:
- Two-column text + visual
- Card/grid sections (2x2 or 2x3)
- Comparison columns
- Process/timeline flow
- Full or half-bleed image with overlay text

Avoid repeated title + bullets layout across the full deck.
Avoid a single unchanged background style across all slides unless the user explicitly requests strict uniformity.
Avoid mixing multiple primary styles from `A-F` in one deck unless explicitly requested.

## Panel Policy (Readability-Critical)

Decide panel strategy before full content fill:

- `panelless`: text and diagrams are placed directly on prepared text-safe backgrounds.
- `panel-based`: containers are used intentionally for specific layouts.

Use these rules:
- Do not use opaque white/light panels as a default on patterned backgrounds.
- If readability issues exist, first test panelless + stronger type contrast before adding large panels.
- If panels are required, prefer low-opacity/soft-edge containers and keep them away from title/subtitle anchors.
- Keep body and diagram regions on the same policy (avoid mixed panel modes by accident).

## Title No-Wrap Policy (Required Unless User Overrides)

Use this as default behavior for slide titles and subtitles:

- Set `text_frame.word_wrap = False`.
- Set `text_frame.auto_size = NONE`.
- Use explicit width budget for title boxes (recommended `10.9"` on 16:9 deck).
- Apply single-line fit by reducing font size within safe bounds:
  - Title: `42pt -> 30pt`
  - Subtitle: `20pt -> 14pt`
- Keep title/subtitle left anchor consistent across slides (recommended `0.9"`).

If the title still overflows after minimum font size:
- Widen title box first.
- Then shorten text (preferred) or switch to two-line title only with explicit user approval.

## Background Variation Guidance

Use a consistent but varied pattern across deck sections:
- Cover: strongest visual treatment (hero background).
- Section divider slides: medium-intensity visual treatment.
- Content slides: cleaner variants optimized for readability.
- Data-heavy slides: calmer backgrounds with stronger contrast on data blocks.

Apply background system constraints from:
- `references/background-system.md`

## Common Failures To Catch

- Overlapping elements
- Text overflow/cutoff
- Body text box too short for bullet count (visual overflow into chart/table zone)
- Title unexpectedly wrapped to multiple lines
- Title auto-resized inconsistently across slides
- Weak contrast (text or icons)
- Inconsistent alignment and spacing
- Placeholder leftovers
- Missing or colliding citations/footers
- Repeated identical background composition causing visual monotony
- Slides drifting away from chosen style tuple (`A-F + G + H`)
- Too many layout grammars used in one deck (visual inconsistency)
- Theme token drift (some cards/charts still using previous theme colors)
- Decorative objects (fruit/icons/stickers) intruding into text-safe lanes

## Layout Safety Gates (Required)

Use these gates as hard pass/fail checks:

1. Textbox collision gate:
- No overlapping text-bearing shapes on any slide.

2. Subtitle/body safe gap:
- Keep a minimum vertical gap between subtitle and body zones.
- Default threshold: `>= 0.18"` (increase if typography is heavy).

3. Content/callout lane separation:
- Reserve a dedicated callout lane (typically right side).
- Main content text boxes must not overlap that lane.

4. Reference slide dedicated layout:
- Do not reuse generic body layout for dense source lists.
- Use dedicated reference layout (e.g., two-column references + separate note/footer).

5. Reference URL compression:
- Slide-visible reference URLs must be shortened for readability.
- Put full URLs in external source registry JSON.

6. Reference-note separation:
- Reference columns and reference note/footers must have fixed safe spacing.

7. Footer collision gate:
- Footer/source line and page number badge must not collide with any text box.

8. No-panel mode fallback:
- If user asks for text directly on background, remove panel-style text containers.
- Compensate with stronger font weight/contrast and rerun QA.
9. Panel overlap/duplication gate:
- No slide should contain stacked container boxes that visually merge into a white block behind text.
- No body panel should overlap a chart/flow panel region.
10. Diagram-region parity:
- Diagram container style must match body container policy for the same slide set unless explicitly varied by design.
11. Text-fit gate:
- `CONTENT_PANEL_*` must pass text-fit estimation (no overflow risk).
- Treat text overflow as hard fail even when geometric overlap is zero.
12. Panel-vs-visual overlap gate:
- `CONTENT_PANEL_*` must not overlap `TABLE_*`, `FLOW_*`, or `VIZ_*` regions.
13. Flow bounds gate:
- `FLOW_NODE_*` and `FLOW_LINK_*` must remain inside corresponding `FLOW_*` container.

## Content QA

```bash
python -m markitdown output.pptx
python -m markitdown output.pptx | grep -iE "xxxx|lorem|ipsum|this.*(page|slide).*layout"
```

Fix typos, missing content, wrong ordering, and all placeholder text.

Quantitative checks (recommended defaults):
- Body contrast `>= 4.5:1`
- Heading contrast `>= 3.0:1`
- Background mean brightness in `[105, 225]`
- Unique content background ratio `>= 0.60`
- Panel conflict count `== 0` (no overlapping opaque container pairs).
- Text overflow issues `== 0`
- Panel-vs-visual overlap issues `== 0`
- Flow bounds issues `== 0`
- Theme consistency issues `== 0` when style-family migration is requested
- Decor/text intrusion issues `== 0` when decorative objects are used

## Visual QA

Render slides to images and inspect:

```bash
python scripts/office/soffice.py --headless --convert-to pdf output.pptx
pdftoppm -jpeg -r 150 output.pdf slide
```

Re-render only affected slides after fixes:

```bash
pdftoppm -jpeg -r 150 -f N -l N output.pdf slide-fixed
```

## Verification Loop (Mandatory)

1. Generate deck.
2. Run content QA and visual QA.
3. List concrete issues.
4. Fix issues.
5. Re-verify affected slides.
6. Repeat until no new issues are found.

Do not finalize before at least one fix-and-verify cycle.

If using script automation:

```bash
python scripts/fix_title_no_wrap.py --input output.pptx --output output-fixed.pptx --slides 1-999
python scripts/qa_check.py output-fixed.pptx --strict --json-out qa-report.json --check-text-overlap --check-layout-lanes --check-panel-visual-overlap --check-text-overflow --check-reference-url-length --check-flow-structure --check-flow-bounds --check-table-style --check-theme-consistency --check-decor-text-intrusion
python scripts/theme_migration_check.py output-fixed.pptx --strict --json-out theme-migration-report.json
```

No-panel mode check (when requested):

```bash
python scripts/qa_check.py output-fixed.pptx --strict --json-out qa-report.json --check-text-overlap --check-layout-lanes --check-reference-url-length --require-no-panel-mode
```

Panel conflict check (recommended when using patterned backgrounds):

```bash
python scripts/qa_check.py output-fixed.pptx --strict --json-out qa-report.json --check-text-overlap --check-layout-lanes --check-reference-url-length --check-panel-conflicts
```

## Style Compliance Check (Required)

Before finalizing, explicitly verify:

1. Primary style (`A-F`) remains consistent deck-wide.
2. Layout grammar (`G`) is used consistently and intentionally.
3. Motion style (`H`) matches delivery context and does not distract from content.
4. For style-family migration, verify no residual legacy colors remain on targeted shapes (`theme_consistency_issues == 0`).

## Background System Compliance Check (Required)

Before finalizing, explicitly verify:

1. `cover/section/content` tiers are defined and implemented consistently.
2. Variant caps and diversity targets are met (including adjacent repeat checks).
3. Readability guardrails are met (overlay + contrast + projection stress check).
4. Performance targets are met (resolution/compression/deck size/cross-device render).

## Output Consistency Check (Required)

After final PPT updates:

```bash
python scripts/export_pdf.py output.pptx --strict --json-out pdf-report.json
```

Pass criteria:
1. PDF timestamp is newer than PPT timestamp.
2. PDF page count equals PPT slide count.
