from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

from pptx import Presentation


def parse_rgb_list(raw: str) -> list[tuple[int, int, int]]:
    colors: list[tuple[int, int, int]] = []
    if not raw.strip():
        return colors
    for item in raw.split(";"):
        t = item.strip().replace("-", ",").replace(" ", "")
        if not t:
            continue
        parts = t.split(",")
        if len(parts) != 3:
            continue
        try:
            r, g, b = int(parts[0]), int(parts[1]), int(parts[2])
        except ValueError:
            continue
        if 0 <= r <= 255 and 0 <= g <= 255 and 0 <= b <= 255:
            colors.append((r, g, b))
    return colors


def rgb_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def safe_rgb_from_fill(shape) -> tuple[int, int, int] | None:
    try:
        c = shape.fill.fore_color.rgb
        if c is None:
            return None
        return int(c[0]), int(c[1]), int(c[2])
    except Exception:
        return None


def safe_rgb_from_text(shape) -> tuple[int, int, int] | None:
    if not getattr(shape, "has_text_frame", False):
        return None
    tf = shape.text_frame
    for p in tf.paragraphs:
        for run in p.runs:
            try:
                c = run.font.color.rgb
                if c is not None:
                    return int(c[0]), int(c[1]), int(c[2])
            except Exception:
                pass
        try:
            c = p.font.color.rgb
            if c is not None:
                return int(c[0]), int(c[1]), int(c[2])
        except Exception:
            pass
    return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect residual colors from previous visual themes in PPTX.")
    parser.add_argument("pptx", help="Input PPTX")
    parser.add_argument(
        "--blocked-colors",
        default="80,229,255;109,255,190;255,221,113",
        help="Semicolon-separated RGB triplets, e.g. '80,229,255;109,255,190'",
    )
    parser.add_argument("--distance-max", type=float, default=24.0)
    parser.add_argument("--json-out", default=None)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    blocked = parse_rgb_list(args.blocked_colors)
    if not blocked:
        raise SystemExit("No valid blocked colors provided")

    prs = Presentation(str(Path(args.pptx)))
    issues: list[dict] = []

    for i, slide in enumerate(prs.slides, start=1):
        for sh in slide.shapes:
            name = getattr(sh, "name", "") or "<unnamed>"
            fill_rgb = safe_rgb_from_fill(sh)
            if fill_rgb is not None:
                for b in blocked:
                    d = rgb_distance(fill_rgb, b)
                    if d <= args.distance_max:
                        issues.append(
                            {
                                "slide": i,
                                "shape": name,
                                "channel": "fill",
                                "rgb": fill_rgb,
                                "blocked_rgb": b,
                                "distance": round(d, 2),
                            }
                        )
                        break

            text_rgb = safe_rgb_from_text(sh)
            if text_rgb is not None:
                for b in blocked:
                    d = rgb_distance(text_rgb, b)
                    if d <= args.distance_max:
                        issues.append(
                            {
                                "slide": i,
                                "shape": name,
                                "channel": "text",
                                "rgb": text_rgb,
                                "blocked_rgb": b,
                                "distance": round(d, 2),
                            }
                        )
                        break

    report = {
        "pptx": str(Path(args.pptx)),
        "blocked_colors": blocked,
        "distance_max": args.distance_max,
        "issue_count": len(issues),
        "issues": issues,
        "pass": len(issues) == 0,
    }
    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.strict and issues:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
