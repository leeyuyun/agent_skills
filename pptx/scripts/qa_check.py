from __future__ import annotations

import argparse
import hashlib
import io
import json
import math
import re
from pathlib import Path

from PIL import Image, ImageStat
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
from pptx.enum.text import PP_ALIGN

EMU_PER_INCH = 914400
PT_PER_INCH = 72.0


def luminance(rgb: tuple[float, float, float]) -> float:
    vals = []
    for v in rgb:
        x = v / 255.0
        vals.append(x / 12.92 if x <= 0.03928 else ((x + 0.055) / 1.055) ** 2.4)
    return 0.2126 * vals[0] + 0.7152 * vals[1] + 0.0722 * vals[2]


def contrast_ratio(a: tuple[float, float, float], b: tuple[float, float, float]) -> float:
    l1, l2 = luminance(a), luminance(b)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def first_text_rgb(shape) -> tuple[float, float, float]:
    if not shape.has_text_frame:
        return (0.0, 0.0, 0.0)

    def rgb_or_none(color_obj):
        if color_obj is None:
            return None
        try:
            return color_obj.rgb
        except AttributeError:
            return None

    for p in shape.text_frame.paragraphs:
        c = rgb_or_none(p.font.color)
        if c is not None:
            return (float(c[0]), float(c[1]), float(c[2]))
        for run in p.runs:
            c = rgb_or_none(run.font.color)
            if c is not None:
                return (float(c[0]), float(c[1]), float(c[2]))
    return (0.0, 0.0, 0.0)


def is_heading(shape) -> bool:
    if shape.top < 1900000:
        return True
    if not shape.has_text_frame:
        return False
    for p in shape.text_frame.paragraphs:
        if p.font.size is not None and p.font.size.pt is not None and p.font.size.pt >= 24:
            return True
        for run in p.runs:
            if run.font.size is not None and run.font.size.pt is not None and run.font.size.pt >= 24:
                return True
            if run.font.bold:
                return True
    return False


def has_nonempty_text(shape) -> bool:
    if not shape.has_text_frame:
        return False
    for p in shape.text_frame.paragraphs:
        if p.text and p.text.strip():
            return True
    return False


def intersects(a, b) -> bool:
    ax1, ay1 = int(a.left), int(a.top)
    ax2, ay2 = ax1 + int(a.width), ay1 + int(a.height)
    bx1, by1 = int(b.left), int(b.top)
    bx2, by2 = bx1 + int(b.width), by1 + int(b.height)
    return not (ax2 <= bx1 or bx2 <= ax1 or ay2 <= by1 or by2 <= ay1)


def intersection_area(a, b) -> int:
    ax1, ay1 = int(a.left), int(a.top)
    ax2, ay2 = ax1 + int(a.width), ay1 + int(a.height)
    bx1, by1 = int(b.left), int(b.top)
    bx2, by2 = bx1 + int(b.width), by1 + int(b.height)
    w = min(ax2, bx2) - max(ax1, bx1)
    h = min(ay2, by2) - max(ay1, by1)
    if w <= 0 or h <= 0:
        return 0
    return w * h


def vgap_emu(upper, lower) -> int:
    upper_bottom = int(upper.top) + int(upper.height)
    lower_top = int(lower.top)
    return lower_top - upper_bottom


def parse_prefixes(raw: str) -> list[str]:
    return [x.strip() for x in raw.split(",") if x.strip()]


def shape_name(shape) -> str:
    return getattr(shape, "name", "") or ""


def has_prefix(name: str, prefixes: list[str]) -> bool:
    return any(name.startswith(p) for p in prefixes)


def extract_urls(text: str) -> list[str]:
    return re.findall(r"(https?://\S+|www\.\S+)", text)


def first_text_font_pt(shape) -> float | None:
    if not shape.has_text_frame:
        return None
    for p in shape.text_frame.paragraphs:
        if p.font.size is not None and p.font.size.pt is not None:
            return float(p.font.size.pt)
        for run in p.runs:
            if run.font.size is not None and run.font.size.pt is not None:
                return float(run.font.size.pt)
    return None


def shape_width_pt(shape) -> float:
    return (float(shape.width) / float(EMU_PER_INCH)) * PT_PER_INCH


def shape_height_pt(shape) -> float:
    return (float(shape.height) / float(EMU_PER_INCH)) * PT_PER_INCH


def weighted_text_len(text: str, ascii_factor: float) -> float:
    n = 0.0
    for ch in text:
        n += 1.0 if ord(ch) > 127 else ascii_factor
    return n


def cell_font_pt(cell) -> float | None:
    tf = cell.text_frame
    if tf is None:
        return None
    for p in tf.paragraphs:
        if p.font.size is not None and p.font.size.pt is not None:
            return float(p.font.size.pt)
        for run in p.runs:
            if run.font.size is not None and run.font.size.pt is not None:
                return float(run.font.size.pt)
    return None


def cell_alignment(cell):
    tf = cell.text_frame
    if tf is None:
        return None
    for p in tf.paragraphs:
        if (p.text or "").strip():
            return p.alignment
    return None


def solid_fill_rgb(target) -> tuple[int, int, int] | None:
    try:
        color = target.fill.fore_color.rgb
        if color is None:
            return None
        return int(color[0]), int(color[1]), int(color[2])
    except Exception:
        return None


def is_numeric_text(text: str) -> bool:
    t = text.strip()
    if not t:
        return False
    t = t.replace(",", "").replace("%", "")
    return bool(re.match(r"^[+\-]?\d+(\.\d+)?$", t))


def is_connector_shape(shape) -> bool:
    try:
        if shape.shape_type == MSO_SHAPE_TYPE.LINE:
            return True
    except Exception:
        pass
    tag = str(getattr(getattr(shape, "element", None), "tag", ""))
    return tag.endswith("}cxnSp")


def is_arrow_shape(shape) -> bool:
    try:
        return "ARROW" in str(shape.auto_shape_type)
    except Exception:
        return False


def parse_rgb_list(raw: str) -> list[tuple[int, int, int]]:
    vals: list[tuple[int, int, int]] = []
    if not raw.strip():
        return vals
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
            vals.append((r, g, b))
    return vals


def rgb_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2)


def shape_bounds(shape) -> tuple[int, int, int, int]:
    x1, y1 = int(shape.left), int(shape.top)
    x2, y2 = x1 + int(shape.width), y1 + int(shape.height)
    return x1, y1, x2, y2


def bounds_close_or_overlap(a: tuple[int, int, int, int], b: tuple[int, int, int, int], gap: int) -> bool:
    ax1, ay1, ax2, ay2 = a
    bx1, by1, bx2, by2 = b
    return not (ax2 + gap <= bx1 or bx2 + gap <= ax1 or ay2 + gap <= by1 or by2 + gap <= ay1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run quantitative QA checks for PPTX visual quality.")
    parser.add_argument("pptx", help="Input PPTX")
    parser.add_argument("--min-contrast-body", type=float, default=4.5)
    parser.add_argument("--min-contrast-heading", type=float, default=3.0)
    parser.add_argument("--bg-brightness-min", type=float, default=105.0)
    parser.add_argument("--bg-brightness-max", type=float, default=225.0)
    parser.add_argument("--min-unique-bg-ratio", type=float, default=0.60)
    parser.add_argument("--check-text-overlap", action="store_true", help="Fail when any text shapes overlap")
    parser.add_argument(
        "--text-overlap-ignore-prefixes",
        default="",
        help="Comma-separated shape-name prefixes to exclude from overlap check",
    )
    parser.add_argument(
        "--check-layout-lanes",
        action="store_true",
        help="Enable subtitle/body gap, callout lane, reference-note, and footer collision checks",
    )
    parser.add_argument("--min-subtitle-body-gap-inch", type=float, default=0.18)
    parser.add_argument("--subtitle-prefixes", default="SUBTITLE_BOX_")
    parser.add_argument("--body-prefixes", default="CONTENT_PANEL_,BODY_BOX_")
    parser.add_argument("--callout-prefixes", default="CALLOUT_TEXT,CALLOUT_BOX_")
    parser.add_argument("--reference-column-prefixes", default="REF_COL_")
    parser.add_argument("--reference-note-prefixes", default="REF_NOTE")
    parser.add_argument("--footer-prefixes", default="FOOTER_TEXT_,FOOTER_BADGE_,FOOTER_BOX_,CITATION_,SOURCE_")
    parser.add_argument(
        "--check-reference-url-length",
        action="store_true",
        help="Check URL length in reference text zones; enforce shortened display URLs on slides",
    )
    parser.add_argument("--reference-prefixes", default="REF_,SOURCE_")
    parser.add_argument("--max-reference-url-length", type=int, default=56)
    parser.add_argument(
        "--check-text-overflow",
        action="store_true",
        help="Estimate and fail when text in designated boxes likely overflows shape bounds",
    )
    parser.add_argument("--overflow-prefixes", default="CONTENT_PANEL_,BODY_BOX_,CALLOUT_BOX_")
    parser.add_argument("--overflow-default-font-pt", type=float, default=16.0)
    parser.add_argument("--overflow-line-height-multiplier", type=float, default=1.2)
    parser.add_argument("--overflow-ascii-factor", type=float, default=0.55)
    parser.add_argument(
        "--check-panel-visual-overlap",
        action="store_true",
        help="Fail when body text panels overlap table/flow/visual regions",
    )
    parser.add_argument("--panel-overlap-prefixes", default="CONTENT_PANEL_,BODY_BOX_,CALLOUT_BOX_")
    parser.add_argument("--visual-region-prefixes", default="TABLE_,FLOW_,VIZ_")
    parser.add_argument(
        "--require-no-panel-mode",
        action="store_true",
        help="Fail if panel-style shape names are present (for direct-text-on-background mode)",
    )
    parser.add_argument(
        "--check-panel-conflicts",
        action="store_true",
        help="Fail when panel-style container shapes overlap each other",
    )
    parser.add_argument("--panel-prefixes", default="CONTENT_PANEL,BODY_BOX_,SUBTITLE_BOX_,FOOTER_BOX_,REF_PANEL,REF_INTRO_PANEL")
    parser.add_argument(
        "--check-table-style",
        action="store_true",
        help="Enable table naming/style checks (header/body fonts, header row, numeric alignment)",
    )
    parser.add_argument("--table-prefixes", default="TABLE_")
    parser.add_argument("--table-header-min-font-pt", type=float, default=11.0)
    parser.add_argument("--table-body-min-font-pt", type=float, default=10.0)
    parser.add_argument("--table-min-rows", type=int, default=2, help="Minimum rows including header")
    parser.add_argument("--table-min-cols", type=int, default=2)
    parser.add_argument(
        "--table-check-numeric-alignment",
        action="store_true",
        help="Require right alignment for numeric table values",
    )
    parser.add_argument(
        "--check-flow-structure",
        action="store_true",
        help="Enable flow structure checks (naming, nodes, links, node font size)",
    )
    parser.add_argument("--flow-prefixes", default="FLOW_")
    parser.add_argument("--flow-node-prefixes", default="FLOW_NODE_")
    parser.add_argument("--flow-link-prefixes", default="FLOW_LINK_,FLOW_ARROW_,FLOW_CONN_")
    parser.add_argument(
        "--flow-ignore-text-prefixes",
        default="TITLE_BOX_,SUBTITLE_BOX_,FOOTER_,FOOTER_TEXT_,FOOTER_BADGE_,CITATION_,SOURCE_,REF_",
    )
    parser.add_argument("--min-flow-slides", type=int, default=1)
    parser.add_argument("--min-flow-nodes", type=int, default=3)
    parser.add_argument("--min-flow-links", type=int, default=2)
    parser.add_argument("--flow-min-node-font-pt", type=float, default=10.0)
    parser.add_argument(
        "--check-flow-bounds",
        action="store_true",
        help="Fail when FLOW_NODE_/FLOW_LINK_ shapes are outside their FLOW_ container",
    )
    parser.add_argument(
        "--check-theme-consistency",
        action="store_true",
        help="Fail when blocked legacy theme colors are still present on targeted shapes",
    )
    parser.add_argument(
        "--theme-blocked-colors",
        default="80,229,255;109,255,190;255,221,113",
        help="Semicolon-separated RGB list considered legacy/out-of-theme",
    )
    parser.add_argument("--theme-color-distance-max", type=float, default=24.0)
    parser.add_argument(
        "--theme-fill-prefixes",
        default="TITLE_BOX_,SUBTITLE_BOX_,BODY_BOX_,CALLOUT_BOX_,FOOTER_BOX_,VIZ_,FLOW_,TABLE_",
    )
    parser.add_argument(
        "--theme-font-prefixes",
        default="TITLE_BOX_,SUBTITLE_BOX_,BODY_BOX_,CALLOUT_BOX_,FOOTER_BOX_,VIZ_,FLOW_,TABLE_",
    )
    parser.add_argument(
        "--check-decor-text-intrusion",
        action="store_true",
        help="Fail when decorative shapes overlap or are too close to text-safe shapes",
    )
    parser.add_argument("--decor-prefixes", default="DECOR_,PERSIMMON_,FLOWER_,ORNAMENT_")
    parser.add_argument("--decor-ignore-prefixes", default="")
    parser.add_argument(
        "--decor-text-prefixes",
        default="TITLE_BOX_,SUBTITLE_BOX_,BODY_BOX_,CALLOUT_BOX_,FOOTER_BOX_",
    )
    parser.add_argument("--decor-min-gap-inch", type=float, default=0.10)
    parser.add_argument("--strict", action="store_true", help="Exit non-zero if any check fails")
    parser.add_argument("--json-out", default=None, help="Write report JSON")
    args = parser.parse_args()

    pptx_path = Path(args.pptx)
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")

    prs = Presentation(str(pptx_path))
    slide_count = len(prs.slides)
    bg_hashes: list[str] = []
    bg_means: list[float] = []
    contrast_issues: list[dict] = []
    text_overlap_pairs: list[dict] = []
    subtitle_body_gap_issues: list[dict] = []
    content_callout_overlap_issues: list[dict] = []
    reference_note_overlap_issues: list[dict] = []
    footer_collision_issues: list[dict] = []
    reference_url_length_issues: list[dict] = []
    panel_mode_issues: list[dict] = []
    panel_conflict_pairs: list[dict] = []
    panel_visual_overlap_issues: list[dict] = []
    text_overflow_issues: list[dict] = []
    table_style_issues: list[dict] = []
    flow_structure_issues: list[dict] = []
    flow_bounds_issues: list[dict] = []
    theme_consistency_issues: list[dict] = []
    decor_text_intrusion_issues: list[dict] = []
    flow_slides = 0
    table_count = 0
    adjacent_repeat = 0

    ignore_overlap_prefixes = parse_prefixes(args.text_overlap_ignore_prefixes)
    subtitle_prefixes = parse_prefixes(args.subtitle_prefixes)
    body_prefixes = parse_prefixes(args.body_prefixes)
    callout_prefixes = parse_prefixes(args.callout_prefixes)
    ref_col_prefixes = parse_prefixes(args.reference_column_prefixes)
    ref_note_prefixes = parse_prefixes(args.reference_note_prefixes)
    footer_prefixes = parse_prefixes(args.footer_prefixes)
    ref_prefixes = parse_prefixes(args.reference_prefixes)
    panel_prefixes = parse_prefixes(args.panel_prefixes)
    panel_overlap_prefixes = parse_prefixes(args.panel_overlap_prefixes)
    visual_region_prefixes = parse_prefixes(args.visual_region_prefixes)
    overflow_prefixes = parse_prefixes(args.overflow_prefixes)
    table_prefixes = parse_prefixes(args.table_prefixes)
    flow_prefixes = parse_prefixes(args.flow_prefixes)
    flow_node_prefixes = parse_prefixes(args.flow_node_prefixes)
    flow_link_prefixes = parse_prefixes(args.flow_link_prefixes)
    flow_ignore_text_prefixes = parse_prefixes(args.flow_ignore_text_prefixes)
    theme_fill_prefixes = parse_prefixes(args.theme_fill_prefixes)
    theme_font_prefixes = parse_prefixes(args.theme_font_prefixes)
    decor_prefixes = parse_prefixes(args.decor_prefixes)
    decor_ignore_prefixes = parse_prefixes(args.decor_ignore_prefixes)
    decor_text_prefixes = parse_prefixes(args.decor_text_prefixes)
    blocked_colors = parse_rgb_list(args.theme_blocked_colors)
    decor_gap_emu = int(args.decor_min_gap_inch * EMU_PER_INCH)

    for i, slide in enumerate(prs.slides, start=1):
        text_shapes = [sh for sh in slide.shapes if has_nonempty_text(sh)]

        bg_shapes = [sh for sh in slide.shapes if sh.name.startswith("BG_IMAGE_")]
        if bg_shapes:
            blob = bg_shapes[0].image.blob
            digest = hashlib.sha1(blob).hexdigest()
            bg_hashes.append(digest)
            img = Image.open(io.BytesIO(blob)).convert("RGB")
            mean = sum(ImageStat.Stat(img).mean) / 3
            bg_means.append(mean)
            if i > 1 and bg_hashes[-2] == digest:
                adjacent_repeat += 1

            # Contrast sampling per text shape against region under text box.
            w_scale = img.width / prs.slide_width
            h_scale = img.height / prs.slide_height
            for sh in slide.shapes:
                if not sh.has_text_frame:
                    continue
                texts = [p.text.strip() for p in sh.text_frame.paragraphs if p.text.strip()]
                if not texts:
                    continue
                l = max(0, int(sh.left * w_scale))
                t = max(0, int(sh.top * h_scale))
                r = min(img.width, int((sh.left + sh.width) * w_scale))
                b = min(img.height, int((sh.top + sh.height) * h_scale))
                if r <= l or b <= t:
                    continue
                crop = img.crop((l, t, r, b))
                bg_rgb = tuple(ImageStat.Stat(crop).mean)
                fg_rgb = first_text_rgb(sh)
                ratio = contrast_ratio(fg_rgb, bg_rgb)
                threshold = args.min_contrast_heading if is_heading(sh) else args.min_contrast_body
                if ratio < threshold:
                    contrast_issues.append(
                        {
                            "slide": i,
                            "shape": sh.name,
                            "contrast_ratio": round(ratio, 2),
                            "required_min": threshold,
                        }
                    )

        if args.check_theme_consistency and blocked_colors:
            for sh in slide.shapes:
                nm = shape_name(sh)
                if has_prefix(nm, theme_fill_prefixes):
                    fill_rgb = solid_fill_rgb(sh)
                    if fill_rgb is not None:
                        for blocked in blocked_colors:
                            dist = rgb_distance(fill_rgb, blocked)
                            if dist <= args.theme_color_distance_max:
                                theme_consistency_issues.append(
                                    {
                                        "slide": i,
                                        "shape": nm,
                                        "channel": "fill",
                                        "rgb": fill_rgb,
                                        "blocked_rgb": blocked,
                                        "distance": round(dist, 2),
                                    }
                                )
                                break

                if has_prefix(nm, theme_font_prefixes) and has_nonempty_text(sh):
                    fg = first_text_rgb(sh)
                    fg_rgb = (int(fg[0]), int(fg[1]), int(fg[2]))
                    for blocked in blocked_colors:
                        dist = rgb_distance(fg_rgb, blocked)
                        if dist <= args.theme_color_distance_max:
                            theme_consistency_issues.append(
                                {
                                    "slide": i,
                                    "shape": nm,
                                    "channel": "text",
                                    "rgb": fg_rgb,
                                    "blocked_rgb": blocked,
                                    "distance": round(dist, 2),
                                }
                            )
                            break

        if args.check_decor_text_intrusion:
            decor_shapes = [
                sh
                for sh in slide.shapes
                if has_prefix(shape_name(sh), decor_prefixes)
                and not (decor_ignore_prefixes and has_prefix(shape_name(sh), decor_ignore_prefixes))
            ]
            text_safe_shapes = [sh for sh in slide.shapes if has_prefix(shape_name(sh), decor_text_prefixes)]
            for deco in decor_shapes:
                deco_bounds = shape_bounds(deco)
                for text_sh in text_safe_shapes:
                    if getattr(deco, "shape_id", None) == getattr(text_sh, "shape_id", None):
                        continue
                    if bounds_close_or_overlap(deco_bounds, shape_bounds(text_sh), decor_gap_emu):
                        decor_text_intrusion_issues.append(
                            {
                                "slide": i,
                                "decor_shape": shape_name(deco),
                                "text_shape": shape_name(text_sh),
                                "min_gap_emu": decor_gap_emu,
                            }
                        )
                        break

        if args.check_text_overlap:
            for a_idx in range(len(text_shapes)):
                for b_idx in range(a_idx + 1, len(text_shapes)):
                    a = text_shapes[a_idx]
                    b = text_shapes[b_idx]
                    an = shape_name(a)
                    bn = shape_name(b)
                    if (ignore_overlap_prefixes and has_prefix(an, ignore_overlap_prefixes)) or (
                        ignore_overlap_prefixes and has_prefix(bn, ignore_overlap_prefixes)
                    ):
                        continue
                    if intersects(a, b):
                        text_overlap_pairs.append({"slide": i, "shape_a": an, "shape_b": bn})

        if args.check_layout_lanes:
            subtitles = [sh for sh in slide.shapes if has_prefix(shape_name(sh), subtitle_prefixes)]
            bodies = [sh for sh in slide.shapes if has_prefix(shape_name(sh), body_prefixes)]
            callouts = [sh for sh in slide.shapes if has_prefix(shape_name(sh), callout_prefixes)]
            ref_cols = [sh for sh in slide.shapes if has_prefix(shape_name(sh), ref_col_prefixes)]
            ref_notes = [sh for sh in slide.shapes if has_prefix(shape_name(sh), ref_note_prefixes)]
            footers = [sh for sh in slide.shapes if has_prefix(shape_name(sh), footer_prefixes)]

            min_gap_emu = int(args.min_subtitle_body_gap_inch * EMU_PER_INCH)
            for sub in subtitles:
                for body in bodies:
                    if int(body.top) >= int(sub.top):
                        gap = vgap_emu(sub, body)
                        if gap < min_gap_emu:
                            subtitle_body_gap_issues.append(
                                {
                                    "slide": i,
                                    "subtitle": shape_name(sub),
                                    "body": shape_name(body),
                                    "gap_emu": gap,
                                    "required_min_emu": min_gap_emu,
                                }
                            )
                    elif intersects(sub, body):
                        subtitle_body_gap_issues.append(
                            {
                                "slide": i,
                                "subtitle": shape_name(sub),
                                "body": shape_name(body),
                                "gap_emu": -1,
                                "required_min_emu": min_gap_emu,
                            }
                        )

            for body in bodies:
                for call in callouts:
                    if intersects(body, call):
                        content_callout_overlap_issues.append(
                            {"slide": i, "body": shape_name(body), "callout": shape_name(call)}
                        )

            for col in ref_cols:
                for note in ref_notes:
                    if intersects(col, note):
                        reference_note_overlap_issues.append(
                            {"slide": i, "reference_column": shape_name(col), "reference_note": shape_name(note)}
                        )

            for ft in footers:
                for tx in text_shapes:
                    if getattr(tx, "shape_id", None) == getattr(ft, "shape_id", None):
                        continue
                    if intersects(ft, tx):
                        footer_collision_issues.append(
                            {"slide": i, "footer": shape_name(ft), "other_text_shape": shape_name(tx)}
                        )

        if args.check_panel_visual_overlap:
            panel_shapes = [
                sh
                for sh in slide.shapes
                if has_prefix(shape_name(sh), panel_overlap_prefixes) and has_nonempty_text(sh)
            ]
            visual_shapes = [
                sh
                for sh in slide.shapes
                if has_prefix(shape_name(sh), visual_region_prefixes) or getattr(sh, "has_table", False)
            ]
            for panel in panel_shapes:
                for visual in visual_shapes:
                    if getattr(panel, "shape_id", None) == getattr(visual, "shape_id", None):
                        continue
                    if intersects(panel, visual):
                        panel_visual_overlap_issues.append(
                            {
                                "slide": i,
                                "panel": shape_name(panel),
                                "visual": shape_name(visual) or "<table-shape>",
                                "intersection_area_emu2": intersection_area(panel, visual),
                            }
                        )

        if args.check_text_overflow:
            target_text_shapes = [
                sh
                for sh in slide.shapes
                if has_prefix(shape_name(sh), overflow_prefixes) and has_nonempty_text(sh)
            ]
            for sh in target_text_shapes:
                text_frame = sh.text_frame
                paragraphs = [p for p in text_frame.paragraphs if (p.text or "").strip()]
                if not paragraphs:
                    continue
                font_pt = first_text_font_pt(sh) or args.overflow_default_font_pt
                line_height_pt = font_pt * args.overflow_line_height_multiplier
                capacity_lines = max(1, int(shape_height_pt(sh) // line_height_pt))
                chars_per_line = max(6, int(shape_width_pt(sh) / max(1.0, font_pt * 0.9)))
                estimated_lines = 0
                for p in paragraphs:
                    txt = (p.text or "").strip()
                    if not txt:
                        continue
                    weighted = weighted_text_len(txt, args.overflow_ascii_factor)
                    estimated_lines += max(1, int(math.ceil(weighted / chars_per_line)))
                if estimated_lines > capacity_lines:
                    text_overflow_issues.append(
                        {
                            "slide": i,
                            "shape": shape_name(sh),
                            "estimated_lines": estimated_lines,
                            "capacity_lines": capacity_lines,
                            "font_pt": round(font_pt, 2),
                            "line_height_pt": round(line_height_pt, 2),
                            "shape_height_pt": round(shape_height_pt(sh), 2),
                            "shape_width_pt": round(shape_width_pt(sh), 2),
                        }
                    )

        if args.check_reference_url_length:
            for sh in text_shapes:
                nm = shape_name(sh)
                if not has_prefix(nm, ref_prefixes):
                    continue
                txt = sh.text_frame.text or ""
                for u in extract_urls(txt):
                    disp = u.replace("https://", "").replace("http://", "")
                    if len(disp) > args.max_reference_url_length:
                        reference_url_length_issues.append(
                            {
                                "slide": i,
                                "shape": nm,
                                "url": u,
                                "display_length": len(disp),
                                "max_allowed": args.max_reference_url_length,
                            }
                        )

        if args.require_no_panel_mode:
            for sh in slide.shapes:
                nm = shape_name(sh)
                if has_prefix(nm, panel_prefixes):
                    panel_mode_issues.append({"slide": i, "shape": nm})

        if args.check_panel_conflicts:
            panel_shapes = [sh for sh in slide.shapes if has_prefix(shape_name(sh), panel_prefixes)]
            for a_idx in range(len(panel_shapes)):
                for b_idx in range(a_idx + 1, len(panel_shapes)):
                    a = panel_shapes[a_idx]
                    b = panel_shapes[b_idx]
                    if intersects(a, b):
                        panel_conflict_pairs.append(
                            {"slide": i, "panel_a": shape_name(a), "panel_b": shape_name(b)}
                        )

        if args.check_table_style:
            table_shapes = [sh for sh in slide.shapes if getattr(sh, "has_table", False)]
            table_count += len(table_shapes)
            for sh in table_shapes:
                table_name = shape_name(sh)
                if table_prefixes and not has_prefix(table_name, table_prefixes):
                    table_style_issues.append(
                        {
                            "slide": i,
                            "shape": table_name,
                            "issue": "table_name_prefix_missing",
                            "required_prefixes": table_prefixes,
                        }
                    )
                table = sh.table
                rows = len(table.rows)
                cols = len(table.columns)
                if rows < args.table_min_rows or cols < args.table_min_cols:
                    table_style_issues.append(
                        {
                            "slide": i,
                            "shape": table_name,
                            "issue": "table_dimensions_too_small",
                            "rows": rows,
                            "cols": cols,
                            "required_min_rows": args.table_min_rows,
                            "required_min_cols": args.table_min_cols,
                        }
                    )
                    continue

                header_fill = None
                body_fill = None
                for c in range(cols):
                    header_cell = table.cell(0, c)
                    header_text = (header_cell.text_frame.text or "").strip()
                    if not header_text:
                        table_style_issues.append(
                            {
                                "slide": i,
                                "shape": table_name,
                                "issue": "header_cell_empty",
                                "row": 0,
                                "col": c,
                            }
                        )
                    h_font = cell_font_pt(header_cell)
                    if h_font is not None and h_font < args.table_header_min_font_pt:
                        table_style_issues.append(
                            {
                                "slide": i,
                                "shape": table_name,
                                "issue": "header_font_too_small",
                                "row": 0,
                                "col": c,
                                "font_pt": round(h_font, 2),
                                "required_min_pt": args.table_header_min_font_pt,
                            }
                        )
                    if header_fill is None:
                        header_fill = solid_fill_rgb(header_cell)
                    if rows > 1 and body_fill is None:
                        body_fill = solid_fill_rgb(table.cell(1, c))

                if header_fill is not None and body_fill is not None and header_fill == body_fill:
                    table_style_issues.append(
                        {
                            "slide": i,
                            "shape": table_name,
                            "issue": "header_fill_not_distinct_from_body",
                            "header_fill_rgb": header_fill,
                            "body_fill_rgb": body_fill,
                        }
                    )

                for r_idx in range(1, rows):
                    for c_idx in range(cols):
                        cell = table.cell(r_idx, c_idx)
                        text = (cell.text_frame.text or "").strip()
                        if not text:
                            continue
                        b_font = cell_font_pt(cell)
                        if b_font is not None and b_font < args.table_body_min_font_pt:
                            table_style_issues.append(
                                {
                                    "slide": i,
                                    "shape": table_name,
                                    "issue": "body_font_too_small",
                                    "row": r_idx,
                                    "col": c_idx,
                                    "font_pt": round(b_font, 2),
                                    "required_min_pt": args.table_body_min_font_pt,
                                }
                            )
                        if args.table_check_numeric_alignment and is_numeric_text(text):
                            align = cell_alignment(cell)
                            if align != PP_ALIGN.RIGHT:
                                table_style_issues.append(
                                    {
                                        "slide": i,
                                        "shape": table_name,
                                        "issue": "numeric_cell_not_right_aligned",
                                        "row": r_idx,
                                        "col": c_idx,
                                        "value": text,
                                    }
                                )

        if args.check_flow_structure:
            flow_markers = [sh for sh in slide.shapes if has_prefix(shape_name(sh), flow_prefixes)]
            if flow_markers:
                flow_slides += 1
                named_nodes = [
                    sh
                    for sh in slide.shapes
                    if has_prefix(shape_name(sh), flow_node_prefixes) and has_nonempty_text(sh)
                ]
                if named_nodes:
                    node_shapes = named_nodes
                else:
                    node_shapes = [
                        sh
                        for sh in slide.shapes
                        if has_nonempty_text(sh) and not has_prefix(shape_name(sh), flow_ignore_text_prefixes)
                    ]

                if len(node_shapes) < args.min_flow_nodes:
                    flow_structure_issues.append(
                        {
                            "slide": i,
                            "issue": "insufficient_flow_nodes",
                            "node_count": len(node_shapes),
                            "required_min_nodes": args.min_flow_nodes,
                        }
                    )

                for node in node_shapes:
                    pt = first_text_font_pt(node)
                    if pt is not None and pt < args.flow_min_node_font_pt:
                        flow_structure_issues.append(
                            {
                                "slide": i,
                                "shape": shape_name(node),
                                "issue": "flow_node_font_too_small",
                                "font_pt": round(pt, 2),
                                "required_min_pt": args.flow_min_node_font_pt,
                            }
                        )

                link_shapes = [
                    sh
                    for sh in slide.shapes
                    if has_prefix(shape_name(sh), flow_link_prefixes) or is_connector_shape(sh) or is_arrow_shape(sh)
                ]
                is_timeline = any("TIMELINE" in shape_name(m).upper() for m in flow_markers)
                required_links = 0 if is_timeline else args.min_flow_links
                if len(link_shapes) < required_links:
                    flow_structure_issues.append(
                        {
                            "slide": i,
                            "issue": "insufficient_flow_links",
                            "link_count": len(link_shapes),
                            "required_min_links": required_links,
                        }
                    )

                if args.check_flow_bounds:
                    for marker in flow_markers:
                        marker_name = shape_name(marker)
                        key = marker_name
                        for prefix in flow_prefixes:
                            if marker_name.startswith(prefix):
                                key = marker_name[len(prefix) :]
                                break
                        m_left = int(marker.left)
                        m_top = int(marker.top)
                        m_right = m_left + int(marker.width)
                        m_bottom = m_top + int(marker.height)
                        for sh in slide.shapes:
                            n = shape_name(sh)
                            if n.startswith(f"FLOW_NODE_{key}_") or n.startswith(f"FLOW_LINK_{key}_"):
                                left = int(sh.left)
                                top = int(sh.top)
                                right = left + int(sh.width)
                                bottom = top + int(sh.height)
                                if left < m_left or top < m_top or right > m_right or bottom > m_bottom:
                                    flow_bounds_issues.append(
                                        {
                                            "slide": i,
                                            "container": marker_name,
                                            "shape": n,
                                            "container_bounds": [m_left, m_top, m_right, m_bottom],
                                            "shape_bounds": [left, top, right, bottom],
                                        }
                                    )

    unique_ratio = (len(set(bg_hashes)) / len(bg_hashes)) if bg_hashes else 0.0
    brightness_issues = [
        m for m in bg_means if m < args.bg_brightness_min or m > args.bg_brightness_max
    ]

    failures = []
    if unique_ratio < args.min_unique_bg_ratio:
        failures.append(
            f"unique background ratio too low: {unique_ratio:.2f} < {args.min_unique_bg_ratio:.2f}"
        )
    if brightness_issues:
        failures.append(
            f"{len(brightness_issues)} slide backgrounds out of brightness range "
            f"[{args.bg_brightness_min}, {args.bg_brightness_max}]"
        )
    if adjacent_repeat > 0 and len(set(bg_hashes)) > 1:
        failures.append(f"{adjacent_repeat} adjacent background repeats detected")
    if contrast_issues:
        failures.append(f"{len(contrast_issues)} text contrast violations detected")
    if args.check_text_overlap and text_overlap_pairs:
        failures.append(f"{len(text_overlap_pairs)} overlapping text shape pairs detected")
    if args.check_layout_lanes and subtitle_body_gap_issues:
        failures.append(f"{len(subtitle_body_gap_issues)} subtitle/body gap violations detected")
    if args.check_layout_lanes and content_callout_overlap_issues:
        failures.append(f"{len(content_callout_overlap_issues)} content/callout overlaps detected")
    if args.check_layout_lanes and reference_note_overlap_issues:
        failures.append(f"{len(reference_note_overlap_issues)} reference column/note overlaps detected")
    if args.check_layout_lanes and footer_collision_issues:
        failures.append(f"{len(footer_collision_issues)} footer collisions detected")
    if args.check_panel_visual_overlap and panel_visual_overlap_issues:
        failures.append(f"{len(panel_visual_overlap_issues)} panel/visual overlaps detected")
    if args.check_text_overflow and text_overflow_issues:
        failures.append(f"{len(text_overflow_issues)} text-overflow risk issues detected")
    if args.check_reference_url_length and reference_url_length_issues:
        failures.append(f"{len(reference_url_length_issues)} overlong reference URLs detected")
    if args.require_no_panel_mode and panel_mode_issues:
        failures.append(f"{len(panel_mode_issues)} panel-mode shapes found while no-panel mode is required")
    if args.check_panel_conflicts and panel_conflict_pairs:
        failures.append(f"{len(panel_conflict_pairs)} overlapping panel container pairs detected")
    if args.check_table_style and table_count == 0:
        failures.append("no table shapes found while --check-table-style is enabled")
    if args.check_table_style and table_style_issues:
        failures.append(f"{len(table_style_issues)} table-style violations detected")
    if args.check_flow_structure and flow_slides < args.min_flow_slides:
        failures.append(
            f"flow slide coverage too low: {flow_slides} < {args.min_flow_slides} slides with FLOW_* markers"
        )
    if args.check_flow_structure and flow_structure_issues:
        failures.append(f"{len(flow_structure_issues)} flow-structure violations detected")
    if args.check_flow_bounds and flow_bounds_issues:
        failures.append(f"{len(flow_bounds_issues)} flow-bounds violations detected")
    if args.check_theme_consistency and theme_consistency_issues:
        failures.append(f"{len(theme_consistency_issues)} theme-consistency violations detected")
    if args.check_decor_text_intrusion and decor_text_intrusion_issues:
        failures.append(f"{len(decor_text_intrusion_issues)} decor/text intrusion violations detected")

    report = {
        "pptx": str(pptx_path),
        "slide_count": slide_count,
        "unique_background_ratio": round(unique_ratio, 3),
        "adjacent_background_repeats": adjacent_repeat,
        "background_mean_brightness": [round(x, 2) for x in bg_means],
        "contrast_issues": contrast_issues,
        "text_overlap_pairs": text_overlap_pairs,
        "subtitle_body_gap_issues": subtitle_body_gap_issues,
        "content_callout_overlap_issues": content_callout_overlap_issues,
        "reference_note_overlap_issues": reference_note_overlap_issues,
        "footer_collision_issues": footer_collision_issues,
        "panel_visual_overlap_issues": panel_visual_overlap_issues,
        "text_overflow_issues": text_overflow_issues,
        "reference_url_length_issues": reference_url_length_issues,
        "panel_mode_issues": panel_mode_issues,
        "panel_conflict_pairs": panel_conflict_pairs,
        "table_count": table_count,
        "flow_slides": flow_slides,
        "table_style_issues": table_style_issues,
        "flow_structure_issues": flow_structure_issues,
        "flow_bounds_issues": flow_bounds_issues,
        "theme_consistency_issues": theme_consistency_issues,
        "decor_text_intrusion_issues": decor_text_intrusion_issues,
        "failures": failures,
        "pass": len(failures) == 0,
    }

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.strict and failures:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
