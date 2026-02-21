from __future__ import annotations

import argparse
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE
from pptx.util import Pt


def parse_prefixes(raw: str) -> list[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def has_prefix(name: str, prefixes: list[str]) -> bool:
    return any(name.startswith(p) for p in prefixes)


def add_soft_backing(slide, target_shape, idx: int, rgb: tuple[int, int, int], transparency: float) -> None:
    pad_x = int(target_shape.width * 0.015)
    pad_y = int(target_shape.height * 0.10)
    x = max(0, int(target_shape.left) - pad_x)
    y = max(0, int(target_shape.top) - pad_y)
    w = int(target_shape.width) + pad_x * 2
    h = int(target_shape.height) + pad_y * 2

    back = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE, x, y, w, h)
    back.name = f"FUSION_BACK_{idx}"
    back.fill.solid()
    back.fill.fore_color.rgb = RGBColor(*rgb)
    back.fill.transparency = transparency
    back.line.fill.background()


def apply_panel_style(shape, fill_rgb: tuple[int, int, int], line_rgb: tuple[int, int, int], transparency: float) -> None:
    shape.fill.solid()
    shape.fill.fore_color.rgb = RGBColor(*fill_rgb)
    shape.fill.transparency = transparency
    shape.line.color.rgb = RGBColor(*line_rgb)
    shape.line.width = Pt(0.8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply text/background fusion pass to PPTX.")
    parser.add_argument("input_pptx")
    parser.add_argument("output_pptx")
    parser.add_argument("--target-prefixes", default="TITLE_BOX_,SUBTITLE_BOX_,BODY_BOX_,CALLOUT_BOX_,FOOTER_BOX_")
    parser.add_argument("--fill-rgb", default="106,48,58")
    parser.add_argument("--line-rgb", default="212,170,114")
    parser.add_argument("--back-rgb", default="94,40,52")
    parser.add_argument("--panel-transparency", type=float, default=0.22)
    parser.add_argument("--back-transparency", type=float, default=0.35)
    args = parser.parse_args()

    fill_rgb = tuple(int(x.strip()) for x in args.fill_rgb.split(","))  # type: ignore[assignment]
    line_rgb = tuple(int(x.strip()) for x in args.line_rgb.split(","))  # type: ignore[assignment]
    back_rgb = tuple(int(x.strip()) for x in args.back_rgb.split(","))  # type: ignore[assignment]
    target_prefixes = parse_prefixes(args.target_prefixes)

    prs = Presentation(str(Path(args.input_pptx)))
    back_idx = 0
    for slide in prs.slides:
        targets = [sh for sh in slide.shapes if has_prefix(getattr(sh, "name", "") or "", target_prefixes)]
        for sh in targets:
            add_soft_backing(slide, sh, back_idx, back_rgb, args.back_transparency)
            back_idx += 1
            apply_panel_style(sh, fill_rgb, line_rgb, args.panel_transparency)

    out = Path(args.output_pptx)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print(f"Wrote: {out}")


if __name__ == "__main__":
    main()
