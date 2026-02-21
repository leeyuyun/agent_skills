# Visual Assets And Tables

Use this reference when a deck needs image/chart/table insertion driven by style choices.

For master-tier background architecture, variant caps, readability overlays, and performance limits, also apply:
- `references/background-system.md`

## Quick Workflow

1. Record style tuple: `Primary (A-F) + Layout (G) + Motion (H)`.
2. Build an asset plan per slide:
   - `slide number`
   - `visual type` (`photo`, `illustration`, `chart`, `table`, `map`, `icon row`)
   - `purpose` (`hero`, `evidence`, `comparison`, `process`)
   - `source` (`local`, `generated`, `web`)
   - `placement` (`full-bleed`, `split`, `card`, `sidebar`)
3. Produce assets (reuse local first, then generate, then fetch web if needed).
4. Embed assets into PPTX.
5. Run QA (content, layout, contrast, license/source log).

When using script automation, map style tuple to executable parameters:
- `python scripts/generate_backgrounds.py --style-tuple A1+G13+H1 ...`
- Persist style tuple in the asset registry for reproducibility.

## Style To Visual Direction

Use this as default mapping when the user does not specify concrete image subjects.

| Primary style | Preferred visuals | Table style |
|---|---|---|
| `A*` Corporate/Executive | Clean business photography, subtle geography/context shots, restrained icons | Header emphasis, muted zebra rows, strong numeric alignment |
| `B*` Startup/Pitch | Product screenshots, growth charts, team/action images | Compact KPI tables, bold key metric column |
| `C*` Tech/Engineering | Architecture diagrams, system topology, UI captures | Monospace-friendly labels, dense but consistent grid |
| `D*` Marketing/Brand | Campaign visuals, product hero imagery, lifestyle scenes | Campaign comparison tables, clear CTA/status columns |
| `E*` Education/Story | Step-by-step illustrations, explainer diagrams | Learning tables, high readability, larger row spacing |
| `F*` Aesthetic/Material | Mood imagery based on sub-style (e.g., `F10` Nordic uses natural landscapes) | Minimal decoration, material-consistent lines/colors |

## Layout Grammar To Asset Placement

- `G2` Image-led: use one dominant hero visual per slide.
- `G3` Split: keep text/image ratio near `40/60` or `50/50`.
- `G4` Cards: use 2-6 cards, each with one icon/image + short text.
- `G5` Timeline: one visual anchor per major step.
- `G8` Matrix: each quadrant should include one visual or data artifact.
- `G9` Comparison: prefer table + one supporting chart/image.
- `G10` Map-based: use one map or region visual as primary evidence.

## Asset Source Strategy

Use this priority order:

1. Local reusable assets (`assets/`, user files, brand libraries).
2. Programmatically generated assets (deterministic and editable).
3. Web-sourced assets (only when local/generated assets are insufficient).

### Local Assets

- Prefer assets already approved by the user/brand system.
- Normalize filenames to meaningful names (`slide-03-supply-chain-map.png`).
- Keep one asset folder per task to avoid accidental reuse.

### Generated Assets

Use generated visuals when you need repeatability or data accuracy:
- Charts from CSV/TSV/XLSX (`pandas` + `matplotlib`).
- Simple maps/diagrams with `Pillow`/`matplotlib`/SVG.
- Icon-style illustrations via geometric primitives when photos are unavailable.

Minimum generated asset standard:
- Width >= `1600px` for full-width usage.
- Use transparent background only when slide background is controlled.
- Keep a script or command that can regenerate the asset.

### Web-Sourced Assets

- Respect copyright and licensing. Prefer sources with clear usage rights.
- Record provenance for each downloaded image:
  - URL
  - License/usage note
  - Download date
  - Slide usage
- Reject images that are low-resolution, watermarked, or visually off-style.
- Record source timestamp and slide usage in registry outputs.

## Embedding Rules

### Images

- Always set intentional placement: full-bleed, split-panel, or card thumbnail.
- Preserve readability with overlays/scrims when text sits on top of images.
- Do not stretch images disproportionately.
- For scenic backgrounds, enforce controlled variety:
  - Prefer multiple related variants over one repeated image.
  - Avoid accidental adjacent repeats on content slides.
  - Keep style coherence with one shared tone and texture language.

Python `python-pptx` pattern:

```python
from pptx import Presentation
from pptx.util import Inches

prs = Presentation("input.pptx")
slide = prs.slides[2]
slide.shapes.add_picture(
    "assets/slide-03-hero.jpg",
    Inches(6.6), Inches(1.2), Inches(6.1), Inches(4.8)
)
prs.save("output.pptx")
```

PptxGenJS pattern:

```js
slide.addImage({
  path: "assets/slide-03-hero.jpg",
  x: 6.6, y: 1.2, w: 6.1, h: 4.8
});
```

### Tables

- Use tables for exact comparisons, assumptions, pricing tiers, or KPI baselines.
- Keep header row visually distinct.
- Right-align numeric columns; keep unit labels explicit.
- Avoid more than 7 columns on standard 16:9 slides unless user requests dense layout.

Python `python-pptx` table pattern:

```python
table = slide.shapes.add_table(4, 4, Inches(0.7), Inches(2.0), Inches(12.0), Inches(3.2)).table
table.cell(0, 0).text = "Channel"
table.cell(0, 1).text = "Revenue"
table.cell(0, 2).text = "Margin"
table.cell(0, 3).text = "YoY"
```

## QA Checklist For Visual Insertion

- Every content slide has at least one meaningful visual element.
- Visual subject matches selected style tuple.
- No overflow, overlap, or clipping after insertion.
- Text contrast remains readable over images.
- Table headers/body styles are consistent deck-wide.
- Source/provenance notes exist for generated and downloaded visuals.
- At least one fix-and-verify cycle completed after inserting visuals.
