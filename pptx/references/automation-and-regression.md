# Automation And Regression

Use this reference to run the validated end-to-end workflow with deterministic scripts.

## Scripts Added To `scripts/`

- `scripts/generate_backgrounds.py`: build text-safe scenic backgrounds from local source images; writes background registry.
- `scripts/apply_backgrounds.py`: apply one or many backgrounds to slides; includes transparency fallback reporting.
- `scripts/harmonize_text.py`: harmonize text color/size for readability profiles.
- `scripts/fix_title_no_wrap.py`: enforce single-line title/subtitle policy with deterministic sizing.
- `scripts/qa_check.py`: run quantitative QA + layout safety QA (text overlaps, text-overflow risk, panel/visual overlap, safe gaps, lane separation, footer collisions, reference URL length, flow bounds).
- `scripts/export_pdf.py`: export PDF and verify timestamp + page count consistency.
- `scripts/theme_tokens.py`: create/validate centralized theme token JSON.
- `scripts/theme_migration_check.py`: detect residual legacy-theme colors after style swaps.
- `scripts/background_fusion_pass.py`: apply deterministic text/background fusion styling.
- `scripts/decor_placement.py`: relocate decorative shapes away from text-safe zones.

## Minimal Standard Flow (Required)

1. Style confirm (`A-F/G/H`) and asset plan.
2. Environment preflight (dependencies for render/QA).
3. Generate backgrounds.
4. Apply backgrounds to PPTX.
5. Harmonize text + run title no-wrap.
6. For style-family migration, run token pass + fusion + decor placement.
7. Run quantitative QA.
8. Fix and re-run QA.
9. Export PDF and run output consistency check.
10. For "latest/progress" decks, persist date-scope + latest-stable metrics in source registry.

Example commands:

```bash
python -c "import PIL, pptx, defusedxml"
python scripts/generate_backgrounds.py --sources-dir assets/scenic --output-dir work/bg --count 10 --style-tuple A1+G13+H1
python scripts/apply_backgrounds.py input.pptx --bg-dir work/bg --pattern "bg-*.jpg" --overlay-mode none
python scripts/harmonize_text.py input.pptx --profile high-contrast --size-scale 1.08
python scripts/fix_title_no_wrap.py --input input.pptx --output input-fixed.pptx --slides 1-999 --title-width 10.9
python scripts/theme_tokens.py --write-default work/theme-tokens.json
python scripts/background_fusion_pass.py input-fixed.pptx input-fused.pptx
python scripts/decor_placement.py input-fused.pptx input-fused-safe.pptx --decor-prefixes "DECOR_,PERSIMMON_,FLOWER_,ORNAMENT_" --text-prefixes "TITLE_BOX_,SUBTITLE_BOX_,BODY_BOX_,CALLOUT_BOX_,FOOTER_BOX_"
python scripts/qa_check.py input-fused-safe.pptx --strict --json-out work/qa-report.json --check-text-overlap --check-layout-lanes --check-panel-visual-overlap --check-text-overflow --check-reference-url-length --check-flow-structure --check-flow-bounds --check-table-style --check-theme-consistency --check-decor-text-intrusion
python scripts/theme_migration_check.py input-fused-safe.pptx --strict --json-out work/theme-migration-report.json
python scripts/export_pdf.py input-fused-safe.pptx --strict --json-out work/pdf-report.json
```

If user asks for text directly on the background:

```bash
python scripts/qa_check.py input-fixed.pptx --strict --json-out work/qa-report.json --check-text-overlap --check-layout-lanes --check-reference-url-length --require-no-panel-mode
```

If patterned backgrounds are used without explicit panel style:

```bash
python scripts/qa_check.py input-fixed.pptx --strict --json-out work/qa-report.json --check-text-overlap --check-layout-lanes --check-reference-url-length --check-panel-conflicts
```

## Fallback Rule For Transparency Failure

If PPT shape transparency is not serialized correctly (`<a:alpha>` missing):

- Do not rely on runtime overlay shape transparency.
- Use prebaked text-safe backgrounds from `generate_backgrounds.py`.
- Keep report artifacts from `apply_backgrounds.py` to record fallback usage.

## Quantitative QA Gates (Suggested Defaults)

- Body text contrast: `>= 4.5:1`
- Heading contrast: `>= 3.0:1`
- Background mean brightness: `105-225`
- Unique background ratio on content slides: `>= 0.60`
- Adjacent repeat backgrounds: `0` (except when explicitly requested)
- Text overlap pairs: `0`
- Text overflow issues: `0`
- Subtitle/body safe-gap violations: `0`
- Panel-vs-visual overlap issues: `0`
- Content/callout lane overlaps: `0`
- Reference column/note overlaps: `0`
- Footer collisions: `0`
- Reference display URL length violations: `0`
- Panel conflict pairs (opaque container overlap): `0`
- Flow bounds violations: `0`
- PPT slide count must equal PDF page count

## Regression Cases (Run Every Skill Update)

Run at least these reproducible cases:

1. Multi-background deck (10 slides) with `A1+G13+H1`.
2. Single-background deck (10 slides) with direct text on image.
3. High-contrast projector profile (`harmonize_text.py --profile projector`).
4. Long-title deck where slides 2/3/9/10 exceed 18 CJK chars, verify no wrapped title after `fix_title_no_wrap.py`.
5. Patterned-background deck in `no-panel` mode; verify no opaque container overlap in QA report.
6. Time-scoped "latest" deck; verify source registry stores `from/to`, `as_of`, and `latest stable` (not prerelease unless requested).
7. Dense full-visual deck with two bullets + table on same slide; verify no `text_overflow_issues`.
8. Theme migration deck (for example tech -> floral) and verify:
- no `theme_consistency_issues`
- no `decor_text_intrusion_issues`
- sample gate approved before full rollout

Keep each case output and its `qa-report.json` + `pdf-report.json` for comparison.
