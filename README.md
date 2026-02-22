# agent_skills

Skill collection for Codex-style agents.

## Included Skills

| Skill | Purpose | Key Files |
| --- | --- | --- |
| `pptx` | Create, edit, and QA PowerPoint files with script-driven workflows. | `pptx/SKILL.md`, `pptx/references/`, `pptx/scripts/` |
| `literature-research-synthesis` | Research and synthesize academic/industry literature into citation-backed narratives. | `literature-research-synthesis/SKILL.md`, `literature-research-synthesis/references/`, `literature-research-synthesis/agents/openai.yaml` |

## literature-research-synthesis

This skill provides a reproducible end-to-end workflow for literature review tasks, including related work writing, evidence mapping, and research gap analysis.

### Workflow Coverage

1. Lock review contract (scope, goals, audience, date range, constraints).
2. Plan search strategy (keywords, Boolean queries, search logs, source portfolio).
3. Apply source selection methodology and screening criteria.
4. Build evidence matrix with methods, metrics, limitations, and evidence strength.
5. Synthesize integrated narrative (consensus, disagreement, gaps, opportunities).
6. Package outputs with consistent naming, bibliography source files, and export checks.

### Key Reference Files

- `literature-research-synthesis/references/search-plan-template.md`
- `literature-research-synthesis/references/search-sources-catalog.md`
- `literature-research-synthesis/references/source-selection-methodology.md`
- `literature-research-synthesis/references/evidence-matrix-template.md`
- `literature-research-synthesis/references/synthesis-outline-template.md`
- `literature-research-synthesis/references/methodology-output-decision-tree.md`
- `literature-research-synthesis/references/output-export-checklist.md`
- `literature-research-synthesis/references/output-naming-and-folder-policy.md`
- `literature-research-synthesis/references/literature-synthesis-decision-flow.md`

### Default Output Convention

- Output folder: `outputs/{report_slug}-{run_date}/`
- Basename: `{report_slug}-literature-review-{run_date}`
- Bibliography source of truth: `{basename}.bib` (preferred) or `{basename}.ris`
- Default citation target: `30-40` sources unless user overrides

## Release Tags

- `literature-research-synthesis-v1.0.0` (initial release of this skill)
