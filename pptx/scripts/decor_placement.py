from __future__ import annotations

import argparse
from pathlib import Path

from pptx import Presentation

EMU_PER_INCH = 914400


def parse_prefixes(raw: str) -> list[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def has_prefix(name: str, prefixes: list[str]) -> bool:
    return any(name.startswith(p) for p in prefixes)


def rect(shape) -> tuple[int, int, int, int]:
    x1 = int(shape.left)
    y1 = int(shape.top)
    return x1, y1, x1 + int(shape.width), y1 + int(shape.height)


def intersects_or_near(a: tuple[int, int, int, int], b: tuple[int, int, int, int], gap: int) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return not (ax2 + gap <= bx1 or bx2 + gap <= ax1 or ay2 + gap <= by1 or by2 + gap <= ay1)


def move_to_lane(shape, slide_w: int, slide_h: int, lane: str) -> None:
    margin = int(0.35 * EMU_PER_INCH)
    if lane == "top-right":
        shape.left = max(0, slide_w - int(shape.width) - margin)
        shape.top = margin
    elif lane == "bottom-right":
        shape.left = max(0, slide_w - int(shape.width) - margin)
        shape.top = max(0, slide_h - int(shape.height) - margin)
    elif lane == "top-left":
        shape.left = margin
        shape.top = margin
    else:
        shape.left = margin
        shape.top = max(0, slide_h - int(shape.height) - margin)


def main() -> None:
    parser = argparse.ArgumentParser(description="Relocate decorative shapes away from text-safe zones.")
    parser.add_argument("input_pptx")
    parser.add_argument("output_pptx")
    parser.add_argument("--decor-prefixes", default="DECOR_,PERSIMMON_,FLOWER_,ORNAMENT_")
    parser.add_argument("--text-prefixes", default="TITLE_BOX_,SUBTITLE_BOX_,BODY_BOX_,CALLOUT_BOX_,FOOTER_BOX_")
    parser.add_argument("--min-gap-inch", type=float, default=0.10)
    parser.add_argument("--lane-order", default="top-right,bottom-right,top-left,bottom-left")
    args = parser.parse_args()

    decor_prefixes = parse_prefixes(args.decor_prefixes)
    text_prefixes = parse_prefixes(args.text_prefixes)
    lane_order = parse_prefixes(args.lane_order)
    min_gap = int(args.min_gap_inch * EMU_PER_INCH)

    prs = Presentation(str(Path(args.input_pptx)))
    moved = 0
    for slide in prs.slides:
        text_shapes = [sh for sh in slide.shapes if has_prefix(getattr(sh, "name", "") or "", text_prefixes)]
        decor_shapes = [sh for sh in slide.shapes if has_prefix(getattr(sh, "name", "") or "", decor_prefixes)]
        text_rects = [rect(sh) for sh in text_shapes]

        for deco in decor_shapes:
            deco_rect = rect(deco)
            if not any(intersects_or_near(deco_rect, tr, min_gap) for tr in text_rects):
                continue
            for lane in lane_order:
                move_to_lane(deco, prs.slide_width, prs.slide_height, lane)
                deco_rect = rect(deco)
                if not any(intersects_or_near(deco_rect, tr, min_gap) for tr in text_rects):
                    moved += 1
                    break

    out = Path(args.output_pptx)
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print(f"Wrote: {out}")
    print(f"Moved decor shapes: {moved}")


if __name__ == "__main__":
    main()
