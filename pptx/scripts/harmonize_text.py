from __future__ import annotations

import argparse
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.util import Pt


PROFILES = {
    "balanced": {
        "title": RGBColor(30, 58, 78),
        "subtitle": RGBColor(54, 78, 95),
        "body": RGBColor(28, 45, 58),
        "label": RGBColor(46, 80, 60),
        "footer": RGBColor(70, 88, 102),
    },
    "high-contrast": {
        "title": RGBColor(18, 49, 68),
        "subtitle": RGBColor(34, 57, 74),
        "body": RGBColor(16, 37, 50),
        "label": RGBColor(36, 63, 47),
        "footer": RGBColor(47, 64, 77),
    },
    "projector": {
        "title": RGBColor(10, 35, 53),
        "subtitle": RGBColor(20, 44, 62),
        "body": RGBColor(8, 28, 42),
        "label": RGBColor(28, 51, 36),
        "footer": RGBColor(35, 53, 66),
    },
}


def classify_text_shape(shape) -> str:
    name = shape.name
    if name == "TextBox 4":
        return "title"
    if name == "TextBox 5":
        return "subtitle"
    if name == "TextBox 6":
        return "body"
    if name == "TextBox 8":
        return "label"
    if name == "TextBox 9":
        return "footer"

    if shape.top < 1900000:
        return "title"
    return "body"


def set_shape_text(shape, rgb: RGBColor, *, size_scale: float, bold_override: bool | None) -> None:
    if not shape.has_text_frame:
        return
    for p in shape.text_frame.paragraphs:
        base_size = p.font.size.pt if p.font.size is not None else None
        if base_size is not None:
            p.font.size = Pt(base_size * size_scale)
        p.font.name = "Microsoft JhengHei"
        p.font.color.rgb = rgb
        if bold_override is not None:
            p.font.bold = bold_override
        for run in p.runs:
            if run.font.size is not None and run.font.size.pt is not None:
                run.font.size = Pt(run.font.size.pt * size_scale)
            run.font.name = "Microsoft JhengHei"
            run.font.color.rgb = rgb
            if bold_override is not None:
                run.font.bold = bold_override


def main() -> None:
    parser = argparse.ArgumentParser(description="Harmonize text color and size for readability.")
    parser.add_argument("input", help="Input PPTX")
    parser.add_argument("--output", default=None, help="Output PPTX (default: in-place)")
    parser.add_argument(
        "--profile",
        choices=["balanced", "high-contrast", "projector"],
        default="balanced",
        help="Text contrast profile",
    )
    parser.add_argument("--size-scale", type=float, default=1.0, help="Scale all text sizes")
    args = parser.parse_args()

    input_pptx = Path(args.input)
    output_pptx = Path(args.output) if args.output else input_pptx
    if not input_pptx.exists():
        raise FileNotFoundError(f"Input PPTX not found: {input_pptx}")

    palette = PROFILES[args.profile]
    prs = Presentation(str(input_pptx))

    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            kind = classify_text_shape(shape)
            bold = True if kind in ("title", "label") else None
            set_shape_text(
                shape,
                palette.get(kind, palette["body"]),
                size_scale=args.size_scale,
                bold_override=bold,
            )

    if input_pptx.resolve() == output_pptx.resolve():
        tmp = output_pptx.with_name(f"{output_pptx.stem}.tmp{output_pptx.suffix}")
        prs.save(str(tmp))
        try:
            tmp.replace(output_pptx)
            print(f"Updated {output_pptx}")
            return
        except PermissionError:
            fallback = output_pptx.with_name(f"{output_pptx.stem}-text-harmonized{output_pptx.suffix}")
            n = 2
            while fallback.exists():
                fallback = output_pptx.with_name(
                    f"{output_pptx.stem}-text-harmonized-{n}{output_pptx.suffix}"
                )
                n += 1
            tmp.replace(fallback)
            print(f"Updated {fallback}")
            return

    prs.save(str(output_pptx))
    print(f"Updated {output_pptx}")


if __name__ == "__main__":
    main()
