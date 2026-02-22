# agent_skills

Reusable skills for Codex-style agents.

## Skills Overview

| Skill | When to use | Entry |
| --- | --- | --- |
| `pptx` | Creating/editing `.pptx`, slide redesign, chart/table/flow/timeline professionalization, and style migration. | `pptx/SKILL.md` |
| `literature-research-synthesis` | Literature review, related-work writing, evidence mapping, and research gap analysis. | `literature-research-synthesis/SKILL.md` |

## PPTX (Concise)

- Focus: script-driven PowerPoint creation, editing, and QA.
- Typical tasks: table redraw, flowchart cleanup, chart/timeline redesign, and visual consistency upgrades.
- Core resources: `pptx/references/` and `pptx/scripts/`.

## Literature Research Synthesis (Concise)

- Focus: reproducible end-to-end literature synthesis workflow.
- Core steps: search planning, source screening, evidence matrix, integrated narrative, output packaging.
- Core resources: `literature-research-synthesis/references/` and `literature-research-synthesis/agents/openai.yaml`.

## Usage

1. Open the target skill's `SKILL.md`.
2. Follow the required workflow and decision rules.
3. Reuse bundled references/scripts instead of rebuilding from scratch.

## Release Tags

- `literature-research-synthesis-v1.0.0`
