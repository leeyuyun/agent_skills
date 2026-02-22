# Output Export Checklist

Choose artifacts from the decision tree:
1. Quick exploratory: `{basename}.md`
2. Internal formal: `{basename}.md` + `{basename}.docx`
3. External or archival: `{basename}.md` + `{basename}.docx|{basename}.tex` + `{basename}.pdf`
4. Keep bibliography source file: `{basename}.bib` (preferred) or `{basename}.ris`
5. When visuals exist, keep reproducible assets in:
- `figures/`
- `tables/`
- `data/`
- `scripts/`

Use folder and basename policy from:
`references/output-naming-and-folder-policy.md`

## 1. Authoring Base File

1. Confirm target and constraints first (course/thesis/submission/internal + handbook/guideline/template).
2. Write and finalize the draft base file (`.md`, `.docx`, or `.tex`) according to constraints.
3. Maintain citations from bibliography source file (`.bib`/`.ris`) during drafting.
4. Ensure reference section is generated from bibliography source where possible.
5. Ensure `output_dir` already exists.
6. For each figure/table, prepare caption metadata:
- Number and title.
- Source and access date.
- Unit/scale where applicable.
7. Prefer figure generation from source data (`.csv`/`.xlsx`) with scriptable steps.
8. For mechanism/process diagrams, enforce readability hard rules:
- no text overlaps with lines/arrows/box borders.
- place step labels outside core geometry and connect with short leader arrows.
- keep core labels inside shape-safe margins.
9. For iterative visual review, generate proof images with unique names:
- `{figure}-proof-{timestamp}.png` for review.
- `{figure}-final.png` as the locked reference target in report files.
10. If overlap persists after two revisions, switch to simplified layout template.

## 2. Preferred Conversion Path (Pandoc)

Use when `pandoc` is available:

```bash
pandoc {basename}.md --citeproc --bibliography {basename}.bib -o {basename}.docx
pandoc {basename}.md --citeproc --bibliography {basename}.bib -o {basename}.pdf
```

If PDF conversion needs a LaTeX engine:

```bash
pandoc {basename}.md --citeproc --bibliography {basename}.bib -o {basename}.pdf --pdf-engine=xelatex
```

## 3. Alternative PDF Path (LibreOffice)

If Markdown to PDF is not available directly:
1. Convert Markdown to DOCX.
2. Export DOCX to PDF with LibreOffice.

```bash
pandoc {basename}.md --citeproc --bibliography {basename}.bib -o {basename}.docx
soffice --headless --convert-to pdf {basename}.docx --outdir .
```

## 4. LaTeX-Native Path (when template-bound)

If target provides a LaTeX template:
1. Keep citations in `.bib`.
2. Compile with template-required engine.
3. Produce submission PDF from `.tex`.

## 5. Validation Checks

1. Generated files match the selected format path.
2. Final output format satisfies target constraints (PDF by default for formal outputs unless overridden).
3. Heading hierarchy is preserved.
4. Tables render correctly in generated rich formats (DOCX/PDF when present).
5. Hyperlinks and references remain intact.
6. Citation style follows priority: guideline/school > discipline > region.
7. Bibliography source file (`.bib`/`.ris`) exists and aligns with final reference list.
8. Citation count matches requested range (default `30-40`).
9. All artifacts are in one output folder.
10. All filenames share the same basename.
11. Every figure/table has number, title, source, date, and unit (if applicable).
12. Every figure/table is referenced in body text.
13. External datasets used in visuals are cited in references.
14. Visual reproducibility is preserved (`data/` + `scripts/`) or exception is documented.
15. Chart quality:
- Vector preferred (`.svg`/`.pdf`) for non-photo charts.
- Raster figures at least 300 DPI.
16. No-overlap check for diagrams:
- text does not intersect lines, arrows, or shape borders.
- callout lines do not cross key labels.
17. Figure placement check in final PDF:
- intended section flow is preserved.
- figure does not appear after references unless explicitly required.
18. Caption hygiene check:
- avoid duplicate numbering in caption body.
19. Data semantics check:
- use scatter/bar for independent milestones; do not imply continuity without evidence.
20. Typography and language consistency check across visual elements.
21. Bibliography hygiene check:
- no malformed/concatenated entries.
- standards or special entry types compile cleanly in selected bibliography style.
22. Cache-proof reference check:
- report references `*-final` figure names, not transient proof names.
23. Issue-to-change trace check:
- every user-reported visual issue is mapped to explicit layout edits before closeout.
