# Methodology and Output Decision Tree

Use this tree at project start.

## Step 1: Decide Target and Constraints

1. What is the primary target?
- Course assignment
- Thesis/dissertation
- Journal/conference submission
- Internal briefing
2. Are there binding format/citation constraints?
- Department handbook
- Submission guideline
- Required template (DOCX/TEX)
3. If constraints exist, they override defaults.

## Step 2: Decide Methodology

1. Is the goal to map the field and identify clusters or gaps quickly?
- Yes: Use Scoping review.
- No: Continue.
2. Is the goal to produce high-rigor, reproducible inclusion/exclusion decisions?
- Yes: Use Systematic-lite or full systematic review.
- No: Continue.
3. Is the goal to estimate pooled effect size or compare quantitative outcomes?
- Yes: Use Meta-analysis compatible synthesis.
- No: Continue.
4. Is the goal policy or implementation recommendation across constraints?
- Yes: Use Evidence-to-decision synthesis.
- No: Use Narrative synthesis with explicit uncertainty.

## Step 3: Decide Draft and Final Output Format

1. Draft format is chosen by workflow and constraints:
- Markdown for iterative collaboration
- DOCX for review-heavy workflows
- LaTeX for template-bound technical writing
2. Final submission is usually PDF for formal outputs unless target rules require otherwise.
3. Suggested artifact bundles:
- Quick exploratory/internal: `{basename}.md`
- Internal formal review: `{basename}.md` + `{basename}.docx`
- External/archival/submission: `{basename}.md` + `{basename}.docx|{basename}.tex` + `{basename}.pdf`
4. Visual-output rule:
- If the synthesis is quantitative or comparative, include at least one table.
- Include at least one figure when visual comparison materially improves interpretation.

## Step 4: Decide Citation Style

Use this precedence order:
1. Submission guideline or school mandate.
2. Discipline norm.
3. Regional norm.

## Step 5: Bibliography Source-of-Truth

1. Maintain citation data continuously in `{basename}.bib` (preferred) or `{basename}.ris`.
2. Avoid last-stage manual rewriting of all references.
3. Generate formatted references from the bibliography source file.

All outputs must be written under:
- `outputs/{report_slug}-{run_date}/`

## Step 6: Minimum Quality Checks

1. Citation target met (default `30-40` unless user overrides).
2. Source mix includes peer-reviewed, preprint (if relevant), and policy/standards (if relevant).
3. Claims are source-traceable.
4. Citation style follows precedence order (guideline/school > discipline > region).
5. Bibliography source file (`.bib`/`.ris`) exists and matches the final reference list.
6. Output artifacts match selected format path and target constraints.
7. File names use one consistent basename.
8. All artifacts are stored in one output folder.
9. Every figure/table includes number, title, source, date, and unit (if applicable).
10. Every figure/table is referenced in body text.
11. Visuals are reproducible from source data (`.csv`/`.xlsx`) plus script/method, or documented exception.
12. Visual quality is publication-safe (vector preferred; raster at least 300 DPI).
