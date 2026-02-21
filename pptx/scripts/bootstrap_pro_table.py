from __future__ import annotations

import argparse
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt


def set_cell_text(cell, text: str, size: int, color: RGBColor, bold: bool, align) -> None:
    cell.text = text
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = cell.text_frame.paragraphs[0]
    p.alignment = align
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color


def parse_headers(raw: str) -> list[str]:
    parts = [x.strip() for x in raw.split(",") if x.strip()]
    return parts if parts else ["Column A", "Column B", "Column C", "Column D"]


def parse_rows(raw: str, cols: int) -> list[list[str]]:
    if not raw.strip():
        return [
            ["Item 1", "120", "Q1", "Ready"],
            ["Item 2", "98", "Q2", "On Track"],
            ["Item 3", "76", "Q3", "Watch"],
            ["Item 4", "62", "Q4", "Blocked"],
        ]
    rows: list[list[str]] = []
    for row in raw.split(";"):
        vals = [x.strip() for x in row.split("|")]
        if len(vals) < cols:
            vals.extend([""] * (cols - len(vals)))
        rows.append(vals[:cols])
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a professional semantic table to an existing PPTX slide.")
    parser.add_argument("--input", required=True, help="Input PPTX path")
    parser.add_argument("--output", required=True, help="Output PPTX path")
    parser.add_argument("--slide", required=True, type=int, help="1-based slide index")
    parser.add_argument("--name", default="TABLE_PROFESSIONAL", help="Table shape name, use TABLE_*")
    parser.add_argument("--left", type=float, default=0.9)
    parser.add_argument("--top", type=float, default=2.1)
    parser.add_argument("--width", type=float, default=11.5)
    parser.add_argument("--height", type=float, default=3.9)
    parser.add_argument("--headers", default="Metric,Value,Owner,Status")
    parser.add_argument(
        "--rows",
        default="",
        help="Semicolon-separated rows; each row uses | separator. Example: A|10|Team1|Ready;B|12|Team2|Risk",
    )
    args = parser.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        raise FileNotFoundError(f"PPTX not found: {inp}")

    prs = Presentation(str(inp))
    if args.slide < 1 or args.slide > len(prs.slides):
        raise ValueError(f"--slide must be in [1, {len(prs.slides)}], got {args.slide}")
    slide = prs.slides[args.slide - 1]

    headers = parse_headers(args.headers)
    rows = parse_rows(args.rows, len(headers))
    shape = slide.shapes.add_table(
        len(rows) + 1,
        len(headers),
        Inches(args.left),
        Inches(args.top),
        Inches(args.width),
        Inches(args.height),
    )
    shape.name = args.name
    table = shape.table

    col_w = args.width / len(headers)
    for c in range(len(headers)):
        table.columns[c].width = Inches(col_w)

    for c, title in enumerate(headers):
        cell = table.cell(0, c)
        cell.fill.solid()
        cell.fill.fore_color.rgb = RGBColor(28, 92, 150)
        set_cell_text(cell, title, 12, RGBColor(245, 251, 255), True, PP_ALIGN.CENTER)

    for r, row in enumerate(rows, start=1):
        for c, value in enumerate(row):
            cell = table.cell(r, c)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor(237, 246, 254) if r % 2 else RGBColor(225, 239, 251)
            align = PP_ALIGN.RIGHT if value.replace(",", "").replace(".", "").isdigit() else PP_ALIGN.LEFT
            if c == 0:
                align = PP_ALIGN.CENTER
            set_cell_text(cell, value, 11, RGBColor(24, 66, 102), False, align)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print(f"Created: {out}")


if __name__ == "__main__":
    main()
