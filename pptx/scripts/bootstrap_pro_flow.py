from __future__ import annotations

import argparse
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt


def set_shape_text(shape, text: str, size: int, color: RGBColor, bold: bool = True) -> None:
    tf = shape.text_frame
    tf.clear()
    p = tf.paragraphs[0]
    p.text = text
    p.alignment = PP_ALIGN.CENTER
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color


def parse_steps(raw: str) -> list[str]:
    parts = [x.strip() for x in raw.split(",") if x.strip()]
    return parts if parts else ["Input", "Plan", "Execute", "Observe", "Reply"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Add a professional horizontal flow diagram to an existing PPTX slide.")
    parser.add_argument("--input", required=True, help="Input PPTX path")
    parser.add_argument("--output", required=True, help="Output PPTX path")
    parser.add_argument("--slide", required=True, type=int, help="1-based slide index")
    parser.add_argument("--name", default="FLOW_PROFESSIONAL", help="Flow container name, use FLOW_*")
    parser.add_argument("--left", type=float, default=0.95)
    parser.add_argument("--top", type=float, default=2.4)
    parser.add_argument("--width", type=float, default=11.8)
    parser.add_argument("--height", type=float, default=2.5)
    parser.add_argument("--steps", default="Input,Plan,Execute,Observe,Reply")
    parser.add_argument("--node-prefix", default="FLOW_NODE")
    parser.add_argument("--link-prefix", default="FLOW_LINK")
    args = parser.parse_args()

    inp = Path(args.input)
    if not inp.exists():
        raise FileNotFoundError(f"PPTX not found: {inp}")

    prs = Presentation(str(inp))
    if args.slide < 1 or args.slide > len(prs.slides):
        raise ValueError(f"--slide must be in [1, {len(prs.slides)}], got {args.slide}")
    slide = prs.slides[args.slide - 1]

    panel = slide.shapes.add_shape(
        MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
        Inches(args.left),
        Inches(args.top),
        Inches(args.width),
        Inches(args.height),
    )
    panel.name = args.name
    panel.fill.solid()
    panel.fill.fore_color.rgb = RGBColor(233, 243, 252)
    panel.line.color.rgb = RGBColor(116, 164, 202)

    steps = parse_steps(args.steps)
    gap = 0.24
    node_w = (args.width - (len(steps) + 1) * gap) / len(steps)
    node_h = 1.15
    node_y = args.top + (args.height - node_h) / 2
    nodes = []
    for i, step in enumerate(steps, start=1):
        node_x = args.left + gap + (i - 1) * (node_w + gap)
        node = slide.shapes.add_shape(
            MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE,
            Inches(node_x),
            Inches(node_y),
            Inches(node_w),
            Inches(node_h),
        )
        node.name = f"{args.node_prefix}_{i:02d}"
        node.fill.solid()
        node.fill.fore_color.rgb = RGBColor(207, 230, 249)
        node.line.color.rgb = RGBColor(101, 158, 203)
        set_shape_text(node, step, 11, RGBColor(18, 66, 114), True)
        nodes.append(node)

    for i in range(len(nodes) - 1):
        n1 = nodes[i]
        n2 = nodes[i + 1]
        x1 = n1.left + n1.width
        y1 = n1.top + n1.height // 2
        x2 = n2.left
        y2 = n2.top + n2.height // 2
        conn = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, x1, y1, x2, y2)
        conn.name = f"{args.link_prefix}_{i + 1:02d}"
        conn.line.color.rgb = RGBColor(116, 164, 202)
        conn.line.width = Pt(2)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print(f"Created: {out}")


if __name__ == "__main__":
    main()
