# Background System Design

Use this reference when style changes require varied but controlled slide backgrounds.

## 1) Background System Design (Master-Based)

Define background architecture with three Master tiers:

- `cover`: strongest visual impact, one hero composition.
- `section`: medium-intensity compositions for chapter transitions.
- `content`: readability-first compositions for most slides.

### Variant Control + Diversity Target

Control style drift while keeping diversity:

- Keep one shared visual language per deck (same color family + texture language).
- Cap background variants per deck section:
  - `cover`: 1-2 variants
  - `section`: 2-3 variants
  - `content`: 3-6 variants
- Ensure diversity coverage:
  - At least `60%` of content slides use different background source images.
  - Avoid repeating the exact same background on adjacent content slides unless intentionally paired.

### Safe Area And Grid Rules

- Reserve a text-safe area of at least `0.5"` from each edge.
- Reserve chart-safe zones with calm texture (low-frequency area) behind dense data.
- Snap major visual anchors to a consistent grid (recommended 12-column structure for 16:9).
- Keep title block position stable within each tier (`cover`/`section`/`content`).

## 2) Readability Guardrails

Apply for scenic/patterned backgrounds:

- Add overlay/scrim by default on text slides.
- Recommended overlay opacity:
  - Light text on dark image: `20-40%` dark scrim
  - Dark text on light image: `25-45%` light scrim
- Target text contrast ratio:
  - Body text: `>= 4.5:1`
  - Large headings: `>= 3:1`
- Avoid high-frequency texture behind body text (use blur, darken, or move text block).

Projection stress check:
- Verify readability at reduced brightness (simulate projector washout).
- Reject slides where labels become unreadable at ~70% brightness.

Transparency fallback rule:
- If PPT overlay transparency is not serialized correctly, replace runtime overlays with prebaked text-safe backgrounds.
- Keep fallback events in reports to avoid silent regressions.

## 3) Brand Visual Governance

Maintain consistent brand look across diverse backgrounds:

- Normalize all backgrounds to a shared tone curve and saturation range.
- Use one dominant palette and one accent family.
- Keep texture/material language consistent (e.g., film grain OR paper grain, not both mixed arbitrarily).

### Asset Library And Naming

Store reusable background assets with deterministic naming:

- `bg-{tier}-{theme}-{variant}-{aspect}-{version}.jpg`
- Example: `bg-content-europe-landscape-v03-16x9-r1.jpg`

Track assets in a registry (`csv` or `json`) with:
- `asset_id`
- `tier`
- `theme`
- `style_tuple` (`A-F/G/H`)
- `source_type` (`local/generated/web`)
- `source_url_or_script`
- `license_note`
- `slides_used`

## 4) Performance And Delivery

Prevent large files and playback lag:

- Use target raster size aligned to slide ratio:
  - 16:9 deck: `1920x1080` (default), up to `2560x1440` only when needed.
- Use JPEG quality range `78-88` for photo backgrounds unless artifacts are visible.
- Prefer progressive optimization before embedding many images.
- Keep single background image size typically under `700 KB` for standard decks.
- Keep total deck size target under `80 MB` unless user explicitly needs print-grade assets.

Cross-device reliability:
- Open and inspect on at least one additional renderer path (PowerPoint + PDF render path).
- Check no element shift after export to PDF and re-open.

## 5) Acceptance Checklist (Pass/Fail)

Pass only when all checks are true:

1. Background system has `cover/section/content` tiers with explicit variant caps.
2. Diversity target met (`>=60%` unique content backgrounds, no accidental adjacent repeats).
3. Readability guardrails met (overlay + contrast thresholds + projection stress check).
4. Brand governance applied (tone normalization + naming + asset registry updated).
5. Performance targets met (resolution, compression, deck size, cross-device verification).
