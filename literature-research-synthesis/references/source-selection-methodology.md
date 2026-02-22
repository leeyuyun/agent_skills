# Source Selection Methodology (State-of-the-Art)

Use this method to choose literature sources with high recall, high precision, and auditability.

## 1. Protocol-First

Freeze before retrieval:
1. Research question and boundaries.
2. Inclusion and exclusion criteria.
3. Time scope and `as_of`.
4. Citation range target (default `30-40`).

Rationale: locking protocol early reduces post-hoc source bias.

## 2. Source Portfolio Design

Select by functional role:
1. Broad discovery source for recall.
2. Domain source for precision.
3. Preprint source for frontier coverage.
4. Optional policy source when governance claims are needed.

Rationale: no single database has complete coverage.

## 3. Hybrid Retrieval

Run all channels:
1. Boolean queries for explicit concept control.
2. Semantic retrieval for latent synonym and paraphrase coverage.
3. Citation expansion:
- Backward references from seed papers.
- Forward citations to capture updates.

Rationale: combining lexical and semantic retrieval lowers omission risk.

## 4. Search QA Layer

1. Review query quality using PRESS-style checks.
2. Keep PRISMA-S style logs:
- Source
- Query string
- Filters
- Run date
- Hit count

Rationale: reproducibility is a quality criterion, not optional documentation.

## 5. Screening Strategy

1. Deduplicate first.
2. Title and abstract screening.
3. Full-text screening for uncertain records.
4. Use human-in-the-loop decisions even when ML ranking is used.

Rationale: automated ranking is a prioritization tool, not a final adjudicator.

## 6. Evidence-Quality Layer

Apply fit-for-purpose quality checks:
1. Risk-of-bias tools for primary studies.
2. Review-quality tools for secondary studies.
3. Certainty frameworks for major conclusions.

Rationale: synthesis strength depends on evidence quality, not source count alone.

## 7. Stopping Rule

Stop when all conditions hold:
1. Thematic saturation reached.
2. New additions produce low marginal insight.
3. Citation count and source-mix targets are satisfied.

Rationale: stopping by count only can miss under-covered themes.
