# agent_skills

Reusable skills for Codex-style agents, focused on practical workflows, reproducibility, and high-quality outputs.

## Repository Description

`agent_skills` is a curated skill pack for Codex and similar coding agents.  
It includes production-oriented skills for slide automation, literature synthesis, and skill creation workflows.

## Suggested Tags (Keywords)

`codex` `agent-skills` `openai-codex` `skill-creator` `pptx` `literature-review` `research-synthesis` `automation` `workflow` `prompt-engineering`

## Skills Overview

| Skill | When to use | Entry |
| --- | --- | --- |
| `pptx` | Creating/editing `.pptx`, slide redesign, chart/table/flow/timeline professionalization, and style migration. | `pptx/SKILL.md` |
| `literature-research-synthesis` | Literature review, related-work writing, evidence mapping, and research gap analysis. | `literature-research-synthesis/SKILL.md` |
| `skill-creator` | Creating or updating other skills with structured frontmatter, progressive disclosure, and reusable references/scripts. | `skill-creator/SKILL.md` |

## Skill Highlights

### PPTX

- Focus: script-driven PowerPoint creation, editing, and QA.
- Typical tasks: table redraw, flowchart cleanup, chart/timeline redesign, and visual consistency upgrades.
- Core resources: `pptx/references/` and `pptx/scripts/`.

### Literature Research Synthesis

- Focus: reproducible end-to-end literature synthesis workflow.
- Core steps: search planning, source screening, evidence matrix, integrated narrative, and output packaging.
- Core resources: `literature-research-synthesis/references/` and `literature-research-synthesis/agents/openai.yaml`.

### Skill Creator

- Focus: creating high-quality skills that are concise, trigger correctly, and scale through progressive disclosure.
- Core outputs: `SKILL.md`, `agents/openai.yaml`, and optional `references/`, `scripts/`, `assets/`.
- Core resources: `skill-creator/references/` and `skill-creator/scripts/`.

## Usage

1. Open the target skill's `SKILL.md`.
2. Follow the required workflow and decision rules.
3. Reuse bundled references/scripts instead of rebuilding from scratch.
4. For new skill development, start with `skill-creator/SKILL.md`.

## Release Tags

| Tag | Date | Note |
| --- | --- | --- |
| `pptx-v1.0.0` | `2026-02-22` | Initial `pptx` skill release |
| `literature-research-synthesis-v1.0.0` | `2026-02-22` | Initial literature research synthesis skill release |
| `skill-creator-v1.0.0` | `2026-02-23` | Add `skill-creator` skill from OpenAI system skills baseline |
