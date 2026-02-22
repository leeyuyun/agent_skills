---
name: literature-research-synthesis
description: Research and synthesize academic and industry literature into structured, citation-backed narratives. Use when requests involve literature review, related work writing, state-of-the-art mapping, evidence matrix building, research gap analysis, or comprehensive synthesis reports for a specific topic, domain, or time window.
---

# Literature Research Synthesis

Build a reproducible literature review workflow and convert source findings into clear integrated narratives.
Use concise outputs for quick decisions and deep outputs for formal review writing.

## 1. Lock Review Contract

Define these items before searching:
1. Research question and scope boundary.
2. Primary goal type:
- Course assignment
- Thesis/dissertation
- Journal or conference submission
- Internal briefing
3. Binding constraints:
- Department handbook
- Journal/conference author guidelines
- Template requirements (Word/LaTeX)
4. Audience type (research, product, policy, executive, student).
5. Date scope (`from`, `to`, `as_of`).
6. Review depth:
- Rapid scan
- Structured review
- Systematic-lite review
7. Source policy (journals, conferences, preprints, standards, patents, reports).
8. Citation target (default `30-40` sources unless user explicitly overrides).
9. Citation style decision using this priority:
- Submission guideline or school mandate
- Discipline norm
- Regional norm
10. Bibliography source-of-truth file from project start:
- `{basename}.bib` (preferred) or `{basename}.ris`

If user does not specify all fields, propose defaults and proceed.
Default decision rules:
1. Decide goal first.
2. Check constraints second.
3. Draft in Markdown, Word, or LaTeX based on constraints and collaboration needs.
4. For formal submission, final artifact is usually PDF unless target rules say otherwise.
5. Keep citations in BibTeX/RIS continuously; avoid end-stage manual citation rewriting.

## 2. Plan Search Strategy

Build a transparent retrieval plan:
1. Expand topic keywords and synonyms.
2. Build Boolean strings using `references/search-plan-template.md`.
3. Select domain-appropriate databases and search engines using `references/search-sources-catalog.md`.
4. Log query strings, filters, and execution dates.
5. Prefer recent sources for fast-changing topics and report exact dates.
6. Mix source types to reduce bias (for example peer-reviewed + preprints + policy/standards).

## 3. Source Selection Decision Methodology

Use the default advanced method:
1. Protocol-first: lock question, scope, inclusion/exclusion, and citation target before searching.
2. Source portfolio design: combine at least one broad index, one domain source, one preprint source, and optional policy source.
3. Hybrid retrieval:
- Boolean retrieval for recall.
- Semantic retrieval for relevance.
- Citation network expansion (backward and forward chaining).
4. Search quality assurance:
- PRESS-style query review.
- PRISMA-S style search logging.
5. Human-in-the-loop screening with optional active-learning prioritization.
6. Evidence quality layer:
- Risk-of-bias tools for primary studies.
- Review-quality tools for secondary syntheses.
- Certainty assessment for key claims.
7. Stop rule: thematic saturation reached and citation composition target satisfied.

Load `references/source-selection-methodology.md` when deciding sources for non-trivial reviews.

## 4. Methodology and Output Decision Tree

Use this decision tree before writing:
1. Decide the target first:
- Course assignment
- Thesis/dissertation
- Journal/conference submission
- Internal briefing
2. Apply binding constraints:
- If handbook/guideline/template specifies format or citation style, follow it.
3. Select methodology:
- If the request asks for evidence map, coverage scan, or topic landscape:
- Methodology: Scoping review.
- Draft format:
  Markdown for iterative collaboration.
  Markdown + DOCX when stakeholder review is expected.
4. If the request asks for rigorous conclusion with transparent inclusion/exclusion:
- Methodology: Systematic-lite or full systematic review workflow.
- Draft format: Markdown or LaTeX.
5. If the request asks to quantify effect size or pooled performance:
- Methodology: Meta-analysis compatible synthesis.
- Draft format: Markdown or LaTeX with explicit methods appendix.
6. If the request asks for policy or implementation recommendation:
- Methodology: Evidence-to-decision synthesis.
- Draft format:
  Markdown + DOCX for policy memo.
7. If request is quick internal briefing with low formality:
- Methodology: Narrative synthesis with explicit uncertainty.
- Draft format: Markdown only unless user asks otherwise.

Output strategy:
1. Draft: Markdown / DOCX / LaTeX according to target and constraints.
2. Final submission: usually PDF for formal deliverables.
3. If target requires source file handoff, include DOCX or TEX alongside PDF.
4. Citation style priority always stays:
- submission/school rules > discipline norm > regional norm.
5. Bibliography file (`.bib` or `.ris`) is maintained from start to finish.
6. For quantitative comparison, trend, timeline, or method-performance synthesis:
- include at least one table.
- include at least one figure when visual comparison improves interpretation.

Figure and table constraints:
1. Every figure/table must have number, title, source, date, and unit (if applicable).
2. Every figure/table must be referenced at least once in body text.
3. Prefer reproducible visuals from source data (`.csv`/`.xlsx`) plus generation script.
4. Avoid screenshot-only visuals unless source data is unavailable; note this explicitly.
5. Image quality:
- Prefer vector (`.svg`/`.pdf`) for line/bar/scatter style charts.
- If raster is required, use at least 300 DPI.
6. Table quality:
- define each column clearly.
- state metric/statistical context.
- record missing-value handling rule.
7. External data used in visuals must also appear in references/citations.
8. For mechanism/process diagrams, enforce a no-overlap layout contract:
- no text intersects lines, arrowheads, or box borders.
- keep step labels outside core geometry; use short leader arrows.
- reserve center zone for core objects only (for example cavity + gain medium).
- avoid routing callout lines through core labels.
9. For non-continuous milestone data, use scatter points or categorical bars; avoid trend lines that imply continuity.
10. Do not print citation keys directly in the chart area unless explicitly requested.
11. Keep caption wording clean:
- avoid duplicate numbering text inside caption body (for example `Figure 1: Figure 1 ...`).
12. Keep visual language consistent:
- unified terminology and language style across title, axis, legend, and caption.

See `references/methodology-output-decision-tree.md` for detailed criteria.

## 5. Screen Sources and Track Reasons

Apply explicit inclusion and exclusion criteria:
1. Remove duplicates.
2. Perform title/abstract screening.
3. Perform full-text check when needed.
4. Record include/exclude reasons for traceability.

Always preserve source metadata: title, authors, year, venue, URL/DOI, and access date.

## 6. Build Evidence Matrix

Use `references/evidence-matrix-template.md` and extract:
1. Question or problem.
2. Method and data.
3. Key results and metrics.
4. Limitations and threats to validity.
5. Relevance to review question.
6. Evidence strength (`low`, `medium`, `high`).

## 7. Synthesize Into Integrated Narrative

Synthesize beyond per-paper summaries:
1. Cluster studies by theme, method, or application.
2. Separate consensus findings from contested findings.
3. Compare evaluation setups before claiming superiority.
4. Identify research gaps and practical opportunities.
5. Distinguish source-backed facts from model inference.

Use `references/synthesis-outline-template.md` for final writing structure.

## 8. Output Package

Return exactly what user asks. If unspecified, provide:
1. Executive summary (5 to 10 bullets).
2. Thematic synthesis.
3. Evidence matrix.
4. Research gaps and recommendations.
5. Reference list in consistent style with `30-40` citations by default.
6. Bibliography source file (`.bib` or `.ris`) used to generate citations.
7. When visuals are used:
- figure and table captions with source/date/unit metadata.
- reproducible visual assets and source data references.

For long reports, keep headline insights first and move detailed tables to appendix.

## 9. Output Artifact Policy

Naming and folder rules are mandatory:
1. Define `report_slug` from topic in kebab-case.
2. Define `run_date` in `YYYYMMDD`.
3. Create output folder:
- `outputs/{report_slug}-{run_date}/`
4. Use one basename for all artifacts:
- `{report_slug}-literature-review-{run_date}`
5. Write all generated files into that folder only.

Choose output artifacts using the decision tree:
1. Quick exploratory output: `{basename}.md`.
2. Internal formal review: `{basename}.md` + `{basename}.docx`.
3. External or archival report: `{basename}.md` + `{basename}.docx` + `{basename}.pdf`.
4. Always keep bibliography source in same folder:
- `{basename}.bib` or `{basename}.ris`.
5. When figures/tables are present, keep structured subfolders under output dir:
- `figures/`
- `tables/`
- `data/`
- `scripts/`
6. For iterated figures that are likely to be cached by viewers:
- render a review proof file with unique suffix (for example `*-proof-{timestamp}.png`).
- lock a stable final file (for example `*-final.png`) and reference this in `.md/.tex/.docx`.
- optionally keep legacy alias only for compatibility, not for final references.

Use `references/output-export-checklist.md` for conversion and validation steps.

## 10. Quality Gates

Require these checks before finalizing:
1. Scope fit: no off-topic sections.
2. Traceability: key claims link to sources.
3. Date clarity: `as_of` and date window are explicit.
4. Balance: include conflicting evidence when available.
5. Uncertainty handling: avoid overclaiming weak evidence.
6. Citation count check: default range `30-40` unless user requests another range.
7. Citation style check: applied by priority (submission/school > discipline > region).
8. Bibliography integrity check: `.bib`/`.ris` exists and is aligned with reference list.
9. Artifact check: generated outputs match decision-tree selection and target constraints.
10. Naming check: generated files follow basename rule.
11. Folder check: all artifacts exist under one output folder.
12. Figure/table metadata check:
- each visual has number/title/source/date/unit (if applicable).
13. Figure/table traceability check:
- each visual is referenced in body text.
- each external data source is cited in references.
14. Visual reproducibility check:
- source data file and generation method/script are present, or exception is documented.
15. Rendering quality check:
- vector preferred; raster at least 300 DPI.
- tables remain readable in final PDF/DOCX.
16. Diagram readability check:
- no text-line overlap.
- no text-border overlap.
- no callout-line crossing through key labels.
17. Figure placement check:
- figure must appear in the intended section flow (not deferred after references).
18. Caption quality check:
- no duplicate numbering phrases.
- source/date/unit metadata complete.
19. Data encoding check:
- visual mark type matches data semantics (no false continuity).
20. Typography and language consistency check:
- no mixed style drift unless explicitly requested.
21. Bibliography hygiene check:
- no malformed or concatenated BibTeX entries.
- avoid unnecessary mega-author citations in main conclusions when simpler domain-canonical evidence exists.
22. Cache-proof rendering check:
- final document references cache-busting final figure names.
23. Issue-to-change trace check:
- when user reports visual issues, map each issue to explicit coordinate/layout changes before finalization.
24. Fallback layout check:
- if overlap persists after two revisions, switch to simplified template (fewer callouts, larger spacing).

## 11. Creation Feedback Loop

Apply this loop when a report includes custom figures:
1. Produce first-pass figure and run overlap checks.
2. Collect user readability feedback in issue form (`Issue 1`, `Issue 2`, ...).
3. Map each issue to one deterministic layout action:
- move label.
- resize box/font.
- reroute leader line.
- split text into two lines.
4. Re-render to proof filename and validate before replacing final figure.
5. Update final report only after proof passes readability checks.
6. If repeated edits still fail, switch to simplified template and preserve the data/logic.

## References

Load only what is needed:
1. Search execution and logs: `references/search-plan-template.md`
2. Search source selection: `references/search-sources-catalog.md`
3. Source decision logic: `references/source-selection-methodology.md`
4. Method/output decision tree: `references/methodology-output-decision-tree.md`
5. Extraction structure: `references/evidence-matrix-template.md`
6. Writing structure: `references/synthesis-outline-template.md`
7. Export workflow: `references/output-export-checklist.md`
8. Naming and folder policy: `references/output-naming-and-folder-policy.md`
9. End-to-end decision map: `references/literature-synthesis-decision-flow.md`

If user requests systematic-review rigor, report screening counts and protocol decisions explicitly.
