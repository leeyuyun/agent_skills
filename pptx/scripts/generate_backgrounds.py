from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image, ImageEnhance, ImageFilter


CANVAS = (1920, 1080)
SUPPORTED_EXT = {".jpg", ".jpeg", ".png", ".webp"}


def cover_resize(img: Image.Image, size: tuple[int, int]) -> Image.Image:
    tw, th = size
    sw, sh = img.size
    sr = sw / sh
    tr = tw / th
    if sr > tr:
        nh = th
        nw = int(nh * sr)
    else:
        nw = tw
        nh = int(nw / sr)
    resized = img.resize((nw, nh), Image.Resampling.LANCZOS)
    left = (nw - tw) // 2
    top = (nh - th) // 2
    return resized.crop((left, top, left + tw, top + th))


def resolve_style_params(style_tuple: str) -> dict:
    primary = (style_tuple.split("+")[0] if style_tuple else "A1").strip().upper()
    if primary.startswith("C2") or primary.startswith("F8"):
        return {
            "brightness": 0.92,
            "contrast": 0.86,
            "color": 0.78,
            "blur": 1.6,
            "veil_rgba": (24, 33, 48, 72),
            "left_safe_rgba": (18, 26, 36, 70),
            "profile": "readable-dark",
        }
    if primary.startswith("D") or primary.startswith("F10"):
        return {
            "brightness": 1.12,
            "contrast": 0.80,
            "color": 0.74,
            "blur": 2.0,
            "veil_rgba": (248, 242, 230, 88),
            "left_safe_rgba": (255, 252, 245, 76),
            "profile": "readable-light",
        }
    return {
        "brightness": 1.06,
        "contrast": 0.82,
        "color": 0.72,
        "blur": 1.8,
        "veil_rgba": (245, 240, 230, 84),
        "left_safe_rgba": (255, 252, 246, 74),
        "profile": "readable-balanced",
    }


def build_text_safe_background(src: Path, dst: Path, style_params: dict) -> tuple[str, tuple[int, int]]:
    img = Image.open(src).convert("RGB")
    img = cover_resize(img, CANVAS)
    img = ImageEnhance.Brightness(img).enhance(style_params["brightness"])
    img = ImageEnhance.Contrast(img).enhance(style_params["contrast"])
    img = ImageEnhance.Color(img).enhance(style_params["color"])
    img = img.filter(ImageFilter.GaussianBlur(radius=style_params["blur"]))

    base = Image.alpha_composite(img.convert("RGBA"), Image.new("RGBA", CANVAS, style_params["veil_rgba"]))

    safe = Image.new("RGBA", CANVAS, (255, 255, 255, 0))
    px = safe.load()
    cutoff = int(CANVAS[0] * 0.62)
    for y in range(CANVAS[1]):
        for x in range(cutoff):
            t = x / max(1, cutoff)
            a = int(style_params["left_safe_rgba"][3] * (1 - t) + 10)
            if y < int(CANVAS[1] * 0.34):
                a = min(170, a + 12)
            px[x, y] = (
                style_params["left_safe_rgba"][0],
                style_params["left_safe_rgba"][1],
                style_params["left_safe_rgba"][2],
                a,
            )

    out = Image.alpha_composite(base, safe).convert("RGB")
    dst.parent.mkdir(parents=True, exist_ok=True)
    out.save(dst, quality=90, optimize=True, progressive=True)
    digest = hashlib.sha1(dst.read_bytes()).hexdigest()
    return digest, out.size


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate text-safe scenic backgrounds and output a registry."
    )
    parser.add_argument("--sources-dir", required=True, help="Folder containing source images")
    parser.add_argument("--output-dir", required=True, help="Folder for generated backgrounds")
    parser.add_argument("--count", type=int, default=10, help="Number of background outputs")
    parser.add_argument("--single", action="store_true", help="Use only the first source for all outputs")
    parser.add_argument(
        "--style-tuple",
        default="A1+G13+H1",
        help="Style tuple (A-F/G/H), used to select executable processing params",
    )
    parser.add_argument(
        "--registry",
        default=None,
        help="CSV registry path (default: <output-dir>/background_registry.csv)",
    )
    args = parser.parse_args()

    src_dir = Path(args.sources_dir)
    out_dir = Path(args.output_dir)
    reg_path = Path(args.registry) if args.registry else out_dir / "background_registry.csv"

    if not src_dir.exists():
        raise FileNotFoundError(f"sources-dir not found: {src_dir}")

    sources = sorted(
        [p for p in src_dir.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED_EXT]
    )
    if not sources:
        raise FileNotFoundError(f"No source images found in: {src_dir}")

    style_params = resolve_style_params(args.style_tuple)
    out_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, str]] = []
    for idx in range(1, args.count + 1):
        src = sources[0] if args.single else sources[(idx - 1) % len(sources)]
        dst = out_dir / f"bg-{idx:02d}.jpg"
        digest, size = build_text_safe_background(src, dst, style_params)
        rows.append(
            {
                "created_at_utc": datetime.now(timezone.utc).isoformat(),
                "index": str(idx),
                "source_path": str(src),
                "output_path": str(dst),
                "style_tuple": args.style_tuple,
                "profile": style_params["profile"],
                "size": f"{size[0]}x{size[1]}",
                "sha1": digest,
            }
        )

    with reg_path.open("w", newline="", encoding="utf-8") as fp:
        writer = csv.DictWriter(
            fp,
            fieldnames=[
                "created_at_utc",
                "index",
                "source_path",
                "output_path",
                "style_tuple",
                "profile",
                "size",
                "sha1",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} backgrounds in {out_dir}")
    print(f"Registry: {reg_path}")


if __name__ == "__main__":
    main()
