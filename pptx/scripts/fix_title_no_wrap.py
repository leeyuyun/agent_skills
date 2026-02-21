from __future__ import annotations

import argparse
from pathlib import Path

from PIL import ImageFont
from pptx import Presentation
from pptx.enum.text import MSO_AUTO_SIZE, PP_ALIGN
from pptx.util import Inches, Pt


FONT_NAME = "Microsoft JhengHei"
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msjh.ttc",
    r"C:\Windows\Fonts\msjhbd.ttc",
    r"C:\Windows\Fonts\msjh.ttf",
]


def parse_slides(expr: str) -> set[int]:
    result: set[int] = set()
    for part in expr.split(","):
        token = part.strip()
        if not token:
            continue
        if "-" in token:
            a, b = token.split("-", 1)
            start = int(a.strip())
            end = int(b.strip())
            lo, hi = min(start, end), max(start, end)
            for n in range(lo, hi + 1):
                result.add(n)
        else:
            result.add(int(token))
    return result


def find_font_path() -> str | None:
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return path
    return None


def text_width_px(text: str, pt_size: int, font_path: str | None) -> int:
    if not text:
        return 0
    px_size = max(1, int(round(pt_size * 96 / 72)))
    font = ImageFont.truetype(font_path, px_size) if font_path else ImageFont.load_default()
    box = font.getbbox(text)
    return max(0, box[2] - box[0])


def fit_pt_size(
    text: str,
    box_width_emu: int,
    slide_width_emu: int,
    max_pt: int,
    min_pt: int,
    font_path: str | None,
) -> int:
    slide_width_px = 1920
    box_width_px = box_width_emu * slide_width_px / max(1, slide_width_emu)
    cap = box_width_px * 0.96
    for pt in range(max_pt, min_pt - 1, -1):
        if text_width_px(text, pt, font_path) <= cap:
            return pt
    return min_pt


def shape_text(shape) -> str:
    return "\n".join(p.text for p in shape.text_frame.paragraphs).strip()


def top_text_shapes(slide, title_zone_top_in: float) -> list:
    items = []
    for sh in slide.shapes:
        if not getattr(sh, "has_text_frame", False):
            continue
        txt = shape_text(sh)
        if not txt:
            continue
        if sh.top <= Inches(title_zone_top_in):
            items.append(sh)
    items.sort(key=lambda s: (s.top, s.left))
    return items


def enforce_single_line(shape, pt_size: int, bold: bool) -> None:
    tf = shape.text_frame
    tf.word_wrap = False
    tf.auto_size = MSO_AUTO_SIZE.NONE
    tf.margin_left = Inches(0.02)
    tf.margin_right = Inches(0.02)
    for p in tf.paragraphs:
        p.alignment = PP_ALIGN.LEFT
        p.font.name = FONT_NAME
        p.font.size = Pt(pt_size)
        p.font.bold = bold
        for run in p.runs:
            run.font.name = FONT_NAME
            run.font.size = Pt(pt_size)
            run.font.bold = bold


def main() -> None:
    parser = argparse.ArgumentParser(description="Fix PPTX title/subtitle wrapping.")
    parser.add_argument("--input", required=True, help="Input PPTX path")
    parser.add_argument("--output", required=True, help="Output PPTX path")
    parser.add_argument("--slides", default="1-999", help="Slides to patch. Example: 2,3 or 2-5,8")
    parser.add_argument("--title-left", type=float, default=0.9, help="Title/subtitle left position in inches")
    parser.add_argument("--title-width", type=float, default=10.9, help="Title/subtitle width in inches")
    parser.add_argument("--title-zone-top", type=float, default=2.65, help="Only inspect text boxes above this Y")
    parser.add_argument("--title-max-pt", type=int, default=42)
    parser.add_argument("--title-min-pt", type=int, default=30)
    parser.add_argument("--subtitle-max-pt", type=int, default=20)
    parser.add_argument("--subtitle-min-pt", type=int, default=14)
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if not input_path.exists():
        raise FileNotFoundError(f"Input PPTX not found: {input_path}")

    slide_ids = parse_slides(args.slides)
    font_path = find_font_path()
    prs = Presentation(str(input_path))

    patched = []
    for idx, slide in enumerate(prs.slides, start=1):
        if idx not in slide_ids:
            continue

        top_shapes = top_text_shapes(slide, title_zone_top_in=args.title_zone_top)
        if len(top_shapes) < 2:
            continue

        title = top_shapes[0]
        subtitle = top_shapes[1]
        title.left = Inches(args.title_left)
        title.width = Inches(args.title_width)
        subtitle.left = Inches(args.title_left)
        subtitle.width = Inches(args.title_width)

        title_pt = fit_pt_size(
            text=shape_text(title),
            box_width_emu=int(title.width),
            slide_width_emu=int(prs.slide_width),
            max_pt=args.title_max_pt,
            min_pt=args.title_min_pt,
            font_path=font_path,
        )
        subtitle_pt = fit_pt_size(
            text=shape_text(subtitle),
            box_width_emu=int(subtitle.width),
            slide_width_emu=int(prs.slide_width),
            max_pt=args.subtitle_max_pt,
            min_pt=args.subtitle_min_pt,
            font_path=font_path,
        )

        enforce_single_line(title, pt_size=title_pt, bold=True)
        enforce_single_line(subtitle, pt_size=subtitle_pt, bold=False)
        patched.append((idx, title_pt, subtitle_pt))

    prs.save(str(output_path))
    print(f"Created: {output_path}")
    if patched:
        for idx, title_pt, subtitle_pt in patched:
            print(f"Slide {idx}: title={title_pt}pt subtitle={subtitle_pt}pt")
    else:
        print("No slides patched.")


if __name__ == "__main__":
    main()
