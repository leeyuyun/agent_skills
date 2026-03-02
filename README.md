# agent_skills

Reusable skills for Codex-style agents, focused on practical workflows, reproducibility, and high-quality outputs.

## Repository Description

`agent_skills` is a curated skill pack for Codex and similar coding agents.  
It includes production-oriented skills for slide automation, literature synthesis, Excel workbook automation, and skill creation workflows.

## Suggested Tags (Keywords)

`codex` `agent-skills` `openai-codex` `skill-creator-plus` `pptx` `literature-review` `research-synthesis` `excel` `openpyxl` `pandas` `xlsxwriter` `automation` `workflow` `prompt-engineering` `ai-drawing` `image-generation` `flight-fare-watch` `airfare` `travel-intelligence`

## Skills Overview

| Skill | When to use | Entry |
| --- | --- | --- |
| `pptx` | Creating/editing `.pptx`, slide redesign, chart/table/flow/timeline professionalization, and style migration. | `pptx/SKILL.md` |
| `literature-research-synthesis` | Literature review, related-work writing, evidence mapping, and research gap analysis. | `literature-research-synthesis/SKILL.md` |
| `skill-creator-plus` | Creating or updating skills with mandatory pre-study of local skills and curated resources before synthesis and generation. | `skill-creator-plus/SKILL.md` |
| `ai-drawing-prompt` | Building model-specific, safe image prompt packs with iteration plans for OpenAI GPT Image, Midjourney, SDXL, and FLUX. | `ai-drawing-prompt/SKILL.md` |
| `excel-workbook` | Creating/cleaning/analyzing `.xlsx`/`.xlsm`/`.csv` with deterministic edits, formula safety, and report-ready outputs. | `excel-workbook/SKILL.md` |
| `flight-fare-watch` | Daily business-travel fare intelligence from CSV inputs: public-fare survey, quote comparison, and recommendation reports. | `flight-fare-watch/SKILL.md` |

## Skill Highlights

### PPTX

- Focus: script-driven PowerPoint creation, editing, and QA.
- Typical tasks: table redraw, flowchart cleanup, chart/timeline redesign, and visual consistency upgrades.
- Core resources: `pptx/references/` and `pptx/scripts/`.

### Literature Research Synthesis

- Focus: reproducible end-to-end literature synthesis workflow.
- Core steps: search planning, source screening, evidence matrix, integrated narrative, and output packaging.
- Core resources: `literature-research-synthesis/references/` and `literature-research-synthesis/agents/openai.yaml`.

### Skill Creator Plus

- Focus: creating high-quality skills with a study-first workflow before generation.
- Core outputs: `SKILL.md`, `agents/openai.yaml`, and optional `references/`, `scripts/`, `assets/`.
- Since `v1.2.0`: enforce QA gates for script-based skills (QA/Test section in `SKILL.md`, runnable QA script, and `references/qa-checklist.md`).
- Core resources: `skill-creator-plus/references/` and `skill-creator-plus/scripts/`.

### AI Drawing Prompt

- Focus: production-ready AI image prompt engineering with model-specific parameter mapping.
- Core outputs: prompt pack with primary prompt, parameter block, negative/avoidance rules, variants, and iteration plan.
- Core resources: `ai-drawing-prompt/references/` and `ai-drawing-prompt/agents/openai.yaml`.

### Excel Workbook

- Focus: deterministic Excel workbook profiling, cleaning, transformation, and automation.
- Core steps: lock workbook contract, optionally request a reference template, pick engine (`openpyxl`/`pandas`/`xlsxwriter`), apply edits, then validate formulas and totals.
- Core resources: `excel-workbook/references/` and `excel-workbook/scripts/`.

### Flight Fare Watch

- Focus: reproducible daily airfare monitoring and internal-vs-public quote comparison.
- Core outputs: `watchlist.csv`, `outputs/recommendations.csv`, and `outputs/daily-fare-report.md`.
- Core resources: `flight-fare-watch/references/`, `flight-fare-watch/scripts/`, and `flight-fare-watch/agents/openai.yaml`.

## Usage

1. Open the target skill's `SKILL.md`.
2. Follow the required workflow and decision rules.
3. Reuse bundled references/scripts instead of rebuilding from scratch.
4. For new skill development, start with `skill-creator-plus/SKILL.md`.

## Release Tags

| Tag | Date | Note |
| --- | --- | --- |
| `pptx-v1.0.0` | `2026-02-22` | Initial `pptx` skill release |
| `literature-research-synthesis-v1.0.0` | `2026-02-22` | Initial literature research synthesis skill release |
| `skill-creator-v1.0.0` | `2026-02-23` | Add `skill-creator` skill from OpenAI system skills baseline |
| `skill-creator-plus-v1.1.0` | `2026-02-23` | Merge and upgrade `skill-creator` to `skill-creator-plus` with study+synthesis workflow |
| `skill-creator-plus-v1.1.1` | `2026-02-23` | Fix `SKILL.md` UTF-8 BOM issue to restore frontmatter parsing and skill discovery |
| `skill-creator-plus-v1.2.0` | `2026-02-26` | Enforce mandatory QA gates for script-based skills (QA section, QA script, and `qa-checklist` validation) |
| `ai-drawing-prompt-v1.0.0` | `2026-02-23` | Add AI drawing prompt skill with reference-image workflow and model profiles |
| `excel-workbook-v1.0.0` | `2026-02-24` | Add Excel workbook automation skill with optional reference-template prompt and formula-safe workflow |
| `flight-fare-watch-v1.0.0` | `2026-03-02` | Add flight fare watch skill for daily public-fare survey and recommendation generation from CSV data |
