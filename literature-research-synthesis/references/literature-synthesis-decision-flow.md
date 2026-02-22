# Literature Research Synthesis Decision Flow

Use this map when you need an end-to-end view of how the skill decides:
- methodology,
- source strategy,
- output format,
- visual design,
- final quality gates.

```mermaid
flowchart TD
    A[Start Request] --> B[Lock Review Contract<br/>question, scope, target, constraints, audience, dates, style]
    B --> C{Missing critical fields?}
    C -->|Yes| D[Propose defaults and continue]
    C -->|No| E[Proceed]
    D --> E

    E --> F[Plan Search Strategy<br/>keywords, boolean, sources, filters, logs]
    F --> G[Source Selection Methodology<br/>protocol-first + portfolio + hybrid retrieval]
    G --> H[Search QA<br/>PRESS-style query review + PRISMA-S logs]
    H --> I[Screening<br/>dedupe -> title/abstract -> full-text]
    I --> J{Stop rule met?<br/>saturation + composition target}
    J -->|No| F
    J -->|Yes| K[Build Evidence Matrix]

    K --> L[Synthesize Narrative<br/>clusters, consensus vs dispute, limits, gaps]
    L --> M{Primary analysis goal?}
    M -->|Field map / coverage| N[Scoping review]
    M -->|Rigorous inclusion/exclusion| O[Systematic-lite]
    M -->|Pooled quantitative effect| P[Meta-analysis compatible]
    M -->|Policy / recommendation| Q[Evidence-to-decision]
    M -->|Quick internal briefing| R[Narrative synthesis]

    N --> S[Select Draft/Final Artifact Bundle]
    O --> S
    P --> S
    Q --> S
    R --> S

    S --> T{Quantitative or comparative synthesis?}
    T -->|Yes| U[Require >=1 table<br/>and >=1 figure when useful]
    T -->|No| V[Visuals optional]
    U --> W[Generate reproducible visuals from data + script]
    V --> X[Prepare narrative-first output]
    W --> Y[Visual Readability Gates<br/>no text-line overlap, no text-border overlap,<br/>clean captions, no false continuity]
    Y --> Z{Visual issues found?}
    Z -->|Yes| ZA[Creation feedback loop<br/>issue -> deterministic layout change]
    ZA --> ZB{2+ failed revisions?}
    ZB -->|No| W
    ZB -->|Yes| ZC[Fallback simplified template]
    ZC --> W
    Z -->|No| X

    X --> AA[Artifact policy<br/>basename + one output folder + figures/tables/data/scripts]
    AA --> AB[Cache-proof output<br/>proof file -> final file]
    AB --> AC[Compile/Export<br/>Pandoc or LaTeX-native path]
    AC --> AD[Final Quality Gates<br/>scope, traceability, citation, placement, reproducibility]
    AD --> AE{All gates pass?}
    AE -->|No| AF[Targeted revision by failed gate]
    AF --> AC
    AE -->|Yes| AG[Deliver final package]
```

## Decision Notes

1. Lock protocol before heavy retrieval to reduce post-hoc bias.
2. Stop by thematic saturation and composition quality, not citation count alone.
3. Decide methodology from intent first, then choose format and artifact bundle.
4. Treat visuals as evidence objects: reproducible, traceable, and layout-audited.
5. Convert user feedback into issue-indexed layout actions during figure iteration.
6. Freeze final figures with stable `*-final` names to avoid viewer cache confusion.
