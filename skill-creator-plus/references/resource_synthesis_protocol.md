# Resource Synthesis Protocol

## Goal
Before generating a new skill, study local and curated resources, then synthesize a reusable design.

## Source Priority
1. Local skills (workspace/user installed)
2. Official OpenAI skills/docs
3. Agent skill standards
4. Community repositories

## Study Steps
1. Read `references/codex_skills_resources_zh.md`.
2. Scan available local `SKILL.md` metadata (name/description).
3. Build candidate list with: relevance, reuse value, maturity, risk.

## Classification
- Core: directly solves target problem.
- Support: improves reliability, quality, or delivery.
- Exclude: low relevance or outdated.

## Synthesis Output (must provide)
- Target task
- Core skills selected + reason
- Support skills selected + reason
- Rejected candidates + reason
- Final workflow (3-7 steps)
- Boundaries / non-goals
