---
name: pptx
description: "Use this skill whenever a PowerPoint file (.pptx) is involved, including creating new decks, editing existing presentations, extracting content, splitting/combining slides, and inserting style-aligned images/charts/tables/flow diagrams from local assets, generated visuals, or web sources. Trigger when users ask for table redraw, flowchart professionalization, existing deck upgrades, chart/table/flow/timeline creation or redesign, visual embedding, or background style updates. If users explicitly ask for charts/flows, always apply professional diagram techniques; also apply them proactively when slide content would be clearer with chart/flow visuals."
---

# PPTX Skill (Runbook)

Use this skill to create/edit/QA `.pptx` with deterministic scripts.
Keep this file short; load details from `references/` only when needed.

## 1. Mode Select

Choose one:
1. Read/analyze
2. Edit existing deck/template
3. Create new deck

If user asks for charts/tables/flow/timeline or professional upgrade, enable `Professional Redraw Mode`.
If user changes style family (for example tech -> floral), enable `Theme Migration Mode`.

## 2. Mandatory Preflight

Run before visual QA:

```bash
python -c "import PIL, pptx, defusedxml"
```

If preflight fails, fix dependencies first.

## 3. Scope Lock

Before content build:
1. Lock slide count target (`N±1` default, exact only if user requires exact).
2. Lock style tuple (`A-F`, `G`, optional `H`) from `references/style-presets.md`.
3. Lock page roles (`cover`, `section`, `content`) for background system.
4. For time-sensitive decks, lock date scope (`from`, `to`).

## 4. Sample Gate (Required)

Do not batch-rollout until sample approval.

1. Build 3 sample slides:
- `cover`
- `section`
- `content`
2. If professional redraw is requested, include:
- 1 table sample (`TABLE_*`)
- 1 flow sample (`FLOW_*`, `FLOW_NODE_*`, `FLOW_LINK_*`)
3. Ask for approval, then continue rollout.

If user asks to pause/review, stop at diagnosis/plan and wait for explicit OK.

## 5. Theme Migration Mode (Required For Style-Family Swaps)

Use when background/style family changes (for example corporate -> cultural, tech -> floral).

Execution order:
1. Run Theme Token Pass:
- Centralize colors first (`scripts/theme_tokens.py`).
- Apply the same token family to title/subtitle/body/footer/cards/charts/flow.
2. Build 3 samples and get approval.
3. Run text/background fusion pass:
- `scripts/background_fusion_pass.py`
4. Run decor placement pass (avoid text lanes):
- `scripts/decor_placement.py`
5. Run theme residual checks:
- `scripts/theme_migration_check.py`
- `scripts/qa_check.py --check-theme-consistency --check-decor-text-intrusion`

Read:
- `references/cultural-hakka-patterns.md`
- `references/object-realism-guidelines.md`

## 6. Professional Redraw Mode (Required For Upgrade Requests)

Trigger when:
1. User asks chart/table/flow/timeline redraw.
2. User asks professional redesign/upgrade.
3. Text-heavy content should be converted into table/flow for clarity.

Minimum standards:
1. Use semantic tables (`add_table`), not fake rectangle grids.
2. Use explicit flow naming:
- `FLOW_*`
- `FLOW_NODE_*`
- `FLOW_LINK_*`
3. Use `VIZ_*` for non-process visuals.
4. Re-run QA after insertion.

## 7. Core Naming For QA

1. `TITLE_BOX_*`
2. `SUBTITLE_BOX_*`
3. `BODY_BOX_*` or `CONTENT_PANEL_*`
4. `CALLOUT_BOX_*`
5. `FOOTER_BOX_*`
6. `TABLE_*`
7. `FLOW_*`, `FLOW_NODE_*`, `FLOW_LINK_*`
8. `VIZ_*`
9. decorative objects: `DECOR_*` / `PERSIMMON_*` / `FLOWER_*` / `ORNAMENT_*`

## 8. Readability-First Gates

Hard pass/fail:
1. No text overlap.
2. No text overflow.
3. Subtitle/body safe gap pass.
4. No panel-vs-visual overlap.
5. No footer collision.
6. Table style checks pass when tables exist.
7. Flow structure + bounds pass when flow exists.
8. Theme consistency pass for style-family migration.
9. Decor/text intrusion pass when decorative objects exist.

Recommended typography minimums:
1. Title >= 32pt
2. Subtitle >= 16pt
3. Body >= 18pt

## 9. Automation Baseline

Use this default sequence:

```bash
python scripts/generate_backgrounds.py --sources-dir assets/scenic --output-dir work/bg --count 10 --style-tuple A1+G13+H1
python scripts/apply_backgrounds.py input.pptx --bg-dir work/bg --pattern "bg-*.jpg" --overlay-mode none
python scripts/harmonize_text.py input.pptx --profile high-contrast --size-scale 1.08
python scripts/fix_title_no_wrap.py --input input.pptx --output input-fixed.pptx --slides 1-999 --title-width 10.9
python scripts/theme_tokens.py --write-default work/theme-tokens.json
python scripts/background_fusion_pass.py input-fixed.pptx input-fused.pptx
python scripts/decor_placement.py input-fused.pptx input-fused-safe.pptx --decor-prefixes "DECOR_,PERSIMMON_,FLOWER_,ORNAMENT_" --text-prefixes "TITLE_BOX_,SUBTITLE_BOX_,BODY_BOX_,CALLOUT_BOX_,FOOTER_BOX_"
python scripts/qa_check.py input-fused-safe.pptx --strict --json-out work/qa-report.json --check-text-overlap --check-layout-lanes --check-panel-visual-overlap --check-text-overflow --check-reference-url-length --check-table-style --check-flow-structure --check-flow-bounds --check-theme-consistency --check-decor-text-intrusion
python scripts/theme_migration_check.py input-fused-safe.pptx --strict --json-out work/theme-migration-report.json
python scripts/export_pdf.py input-fused-safe.pptx --strict --json-out work/pdf-report.json
```

## 10. Workflow Shortcuts

Read/analyze:

```bash
python -m markitdown presentation.pptx
python scripts/thumbnail.py presentation.pptx
```

Edit existing template:

```bash
python scripts/thumbnail.py template.pptx
python scripts/office/unpack.py template.pptx unpacked/
python scripts/clean.py unpacked/
python scripts/office/pack.py unpacked/ output.pptx --original template.pptx
python scripts/fix_title_no_wrap.py --input output.pptx --output output-fixed.pptx --slides 1-999
```

## 11. Temporal Fact Guardrails

For "latest/progress/release timeline" decks:
1. Lock date scope before build.
2. Prefer latest stable over prerelease unless user requests prerelease.
3. Keep `as_of`, scope, and computed metrics in machine-readable output.
4. Flag out-of-range claims.

## 12. References Map

Load only what you need:
1. style tuple selection: `references/style-presets.md`
2. layout + QA policy: `references/design-and-qa.md`
3. background roles/diversity: `references/background-system.md`
4. visuals + licensing: `references/visual-assets.md`
5. professional diagram/table rules: `references/professional-diagrams-and-tables.md`
6. automation + regression: `references/automation-and-regression.md`
7. culture-led floral patterns: `references/cultural-hakka-patterns.md`
8. object realism: `references/object-realism-guidelines.md`

## 13. Dependencies

1. `pip install "markitdown[pptx]"`
2. `pip install Pillow`
3. `npm install -g pptxgenjs`
4. LibreOffice (`soffice`) for PDF conversion
5. Poppler (`pdftoppm`) for slide image rendering
