# Professional Diagrams And Tables

Use this reference when a deck needs professional table redraw, flowchart redesign, or timeline upgrades.

## Quick Use

1. Start with two sample slides:
- one table sample (`TABLE_*`)
- one process-flow sample (`FLOW_*`) or non-process visual sample (`VIZ_*`)
2. Approve style and hierarchy.
3. Roll out in batch.
4. Run QA with `--check-table-style` and `--check-flow-structure`.

## Table Standards

- Use semantic tables (`add_table`), never rectangle-only fake tables.
- Keep table width inside content-safe area.
- Prefer up to 7 columns on 16:9 slides.
- Keep header visually distinct from body.
- Use zebra rows for dense data.
- Right-align numeric values.
- Keep labels concise and unit-explicit.

Recommended naming:
- `TABLE_<topic>`

## Flow / Timeline Standards

- Use explicit process grammar:
  - start/input
  - process
  - decision (diamond) when branching is needed
  - output/end
- Keep connector direction consistent (left-to-right by default).
- Keep key milestones to 4-6 in timeline slides.
- Separate primary path from secondary notes.

Recommended naming:
- flow container: `FLOW_<topic>`
- node: `FLOW_NODE_<topic>_<n>`
- connector/arrow: `FLOW_LINK_<topic>_<n>`
- non-process visual container (cards/matrix/timeline): `VIZ_<topic>`

## Typography And Readability

- Title: 32pt or above.
- Diagram/table labels: 11pt or above.
- Dense body text in table cells: 10pt or above.
- Keep contrast and no-overlap rules from `references/design-and-qa.md`.

## QA Checklist

- Table/flow slide names follow required prefixes.
- Table has header and body rows.
- Header/body font sizes pass minimums.
- Numeric columns are right-aligned.
- Flow slides include enough nodes and links for the intended process.
- `FLOW_NODE_*` / `FLOW_LINK_*` remain inside matching `FLOW_*` bounds.
- At least one fix-and-verify loop is completed after insertion.

## Command Example

```bash
python scripts/qa_check.py output.pptx --strict --json-out qa-report.json --check-text-overlap --check-layout-lanes --check-table-style --check-flow-structure
```
