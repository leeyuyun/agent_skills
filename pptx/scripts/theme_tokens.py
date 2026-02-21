from __future__ import annotations

import argparse
import json
from pathlib import Path


DEFAULT_THEME_TOKENS = {
    "name": "hakka-warm-fabric",
    "version": 1,
    "colors": {
        "ink_light": [250, 243, 230],
        "ink_mid": [239, 225, 203],
        "ink_dark": [92, 44, 40],
        "panel": [93, 40, 50],
        "panel_soft": [112, 54, 64],
        "panel_line": [212, 170, 114],
        "accent_gold": [232, 190, 123],
        "accent_green": [118, 152, 93],
        "card_bg": [244, 228, 201],
        "card_line": [181, 120, 91],
    },
}


def is_rgb_triplet(v: object) -> bool:
    if not isinstance(v, list) or len(v) != 3:
        return False
    for x in v:
        if not isinstance(x, int) or x < 0 or x > 255:
            return False
    return True


def validate_tokens(data: dict) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["token file must be a JSON object"]
    if "colors" not in data or not isinstance(data["colors"], dict):
        return ["missing `colors` object"]
    for key, value in data.get("colors", {}).items():
        if not is_rgb_triplet(value):
            errors.append(f"invalid RGB triplet for colors.{key}: {value}")
    return errors


def main() -> None:
    parser = argparse.ArgumentParser(description="Manage PPTX theme token JSON files.")
    parser.add_argument("--write-default", default=None, help="Write default token JSON to this path")
    parser.add_argument("--validate", default=None, help="Validate token JSON file")
    parser.add_argument("--print-default", action="store_true", help="Print default token JSON")
    args = parser.parse_args()

    if args.write_default:
        out = Path(args.write_default)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(DEFAULT_THEME_TOKENS, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Wrote default theme tokens: {out}")

    if args.validate:
        path = Path(args.validate)
        data = json.loads(path.read_text(encoding="utf-8"))
        errors = validate_tokens(data)
        if errors:
            for err in errors:
                print(f"[ERROR] {err}")
            raise SystemExit(2)
        print(f"Theme token file OK: {path}")

    if args.print_default:
        print(json.dumps(DEFAULT_THEME_TOKENS, ensure_ascii=False, indent=2))

    if not (args.write_default or args.validate or args.print_default):
        parser.print_help()


if __name__ == "__main__":
    main()
