from __future__ import annotations

import argparse
import json
from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE


def push_to_back(slide, shape, index: int = 2) -> None:
    sp_tree = slide.shapes._spTree
    elm = shape.element
    sp_tree.remove(elm)
    sp_tree.insert(index, elm)


def strip_existing_bg_layers(slide) -> None:
    prefixes = ("BG_IMAGE_", "BG_OVERLAY_", "BG_APPLY_", "EURO_BG_", "HARMONY_STRIP_")
    for shape in list(slide.shapes):
        if shape.name.startswith(prefixes):
            shape.element.getparent().remove(shape.element)


def transparency_supported(shape) -> bool:
    return "<a:alpha" in shape.element.xml


def collect_backgrounds(bg_dir: Path, pattern: str) -> list[Path]:
    files = sorted(bg_dir.glob(pattern))
    if not files:
        raise FileNotFoundError(f"No backgrounds found in {bg_dir} with pattern '{pattern}'")
    return files


def apply(
    input_pptx: Path,
    output_pptx: Path,
    backgrounds: list[Path],
    *,
    single_bg: Path | None,
    overlay_mode: str,
    overlay_transparency: float,
) -> dict:
    prs = Presentation(str(input_pptx))
    slides = list(prs.slides)

    if single_bg is None and len(backgrounds) < len(slides):
        raise ValueError(
            f"Need >= {len(slides)} backgrounds, got {len(backgrounds)}"
        )

    report = {
        "input": str(input_pptx),
        "output": str(output_pptx),
        "slide_count": len(slides),
        "overlay_mode_requested": overlay_mode,
        "overlay_mode_effective": overlay_mode,
        "fallback_used": False,
        "slides": [],
    }

    for idx, slide in enumerate(slides, start=1):
        strip_existing_bg_layers(slide)
        bg = single_bg if single_bg else backgrounds[idx - 1]
        pic = slide.shapes.add_picture(str(bg), 0, 0, prs.slide_width, prs.slide_height)
        pic.name = f"BG_IMAGE_{idx}"
        push_to_back(slide, pic, 2)

        used_overlay = False
        if overlay_mode == "shape":
            ov = slide.shapes.add_shape(
                MSO_AUTO_SHAPE_TYPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height
            )
            ov.name = f"BG_OVERLAY_{idx}"
            ov.fill.solid()
            ov.fill.fore_color.rgb = RGBColor(18, 31, 46)
            ov.fill.transparency = overlay_transparency
            ov.line.fill.background()
            if transparency_supported(ov):
                push_to_back(slide, ov, 3)
                used_overlay = True
            else:
                # Transparency unsupported in this environment -> remove overlay and fallback.
                ov.element.getparent().remove(ov.element)
                report["fallback_used"] = True
                report["overlay_mode_effective"] = "prebaked"

        report["slides"].append(
            {
                "index": idx,
                "background": str(bg),
                "shape_overlay_applied": used_overlay,
            }
        )

    if input_pptx.resolve() == output_pptx.resolve():
        tmp = output_pptx.with_name(f"{output_pptx.stem}.tmp{output_pptx.suffix}")
        prs.save(str(tmp))
        try:
            tmp.replace(output_pptx)
            report["output"] = str(output_pptx)
            return report
        except PermissionError:
            fallback = output_pptx.with_name(f"{output_pptx.stem}-bg-applied{output_pptx.suffix}")
            n = 2
            while fallback.exists():
                fallback = output_pptx.with_name(f"{output_pptx.stem}-bg-applied-{n}{output_pptx.suffix}")
                n += 1
            tmp.replace(fallback)
            report["output"] = str(fallback)
            return report

    prs.save(str(output_pptx))
    report["output"] = str(output_pptx)
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply generated backgrounds to a PPTX.")
    parser.add_argument("input", help="Input PPTX path")
    parser.add_argument("--output", default=None, help="Output PPTX path (default: in-place)")
    parser.add_argument("--bg-dir", default=".", help="Background directory")
    parser.add_argument("--pattern", default="bg-*.jpg", help="Glob pattern under bg-dir")
    parser.add_argument("--single-bg", default=None, help="Use one background for all slides")
    parser.add_argument(
        "--overlay-mode",
        choices=["none", "shape"],
        default="none",
        help="Use PPT shape overlay (may fallback if transparency unsupported)",
    )
    parser.add_argument(
        "--overlay-transparency",
        type=float,
        default=0.35,
        help="Overlay transparency for shape mode (0-1)",
    )
    parser.add_argument(
        "--report-json",
        default=None,
        help="Write apply report to JSON (default: <output>.bg-report.json)",
    )
    args = parser.parse_args()

    input_pptx = Path(args.input)
    output_pptx = Path(args.output) if args.output else input_pptx
    bg_dir = Path(args.bg_dir)
    single_bg = Path(args.single_bg) if args.single_bg else None

    if not input_pptx.exists():
        raise FileNotFoundError(f"Input PPTX not found: {input_pptx}")
    if single_bg and not single_bg.exists():
        raise FileNotFoundError(f"single-bg not found: {single_bg}")
    if not single_bg and not bg_dir.exists():
        raise FileNotFoundError(f"bg-dir not found: {bg_dir}")

    backgrounds = [] if single_bg else collect_backgrounds(bg_dir, args.pattern)
    report = apply(
        input_pptx,
        output_pptx,
        backgrounds,
        single_bg=single_bg,
        overlay_mode=args.overlay_mode,
        overlay_transparency=args.overlay_transparency,
    )

    report_path = (
        Path(args.report_json)
        if args.report_json
        else Path(report["output"]).with_suffix(".bg-report.json")
    )
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Updated {report['output']}")
    print(f"Report: {report_path}")
    if report["fallback_used"]:
        print("Note: transparency fallback used (shape overlay unsupported, prefer prebaked backgrounds).")


if __name__ == "__main__":
    main()
