from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
from pathlib import Path

from pptx import Presentation


def count_pdf_pages(pdf_path: Path) -> int:
    data = pdf_path.read_bytes()
    matches = re.findall(rb"/Type\s*/Page(?!s)", data)
    return len(matches)


def convert_with_soffice(pptx_path: Path, pdf_path: Path) -> bool:
    candidates = [
        shutil.which("soffice"),
        r"C:\Program Files\LibreOffice\program\soffice.exe",
        r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
    ]
    for exe in candidates:
        if not exe:
            continue
        p = Path(exe)
        if not p.exists():
            continue
        res = subprocess.run(
            [
                str(p),
                "--headless",
                "--convert-to",
                "pdf",
                "--outdir",
                str(pdf_path.parent),
                str(pptx_path),
            ],
            capture_output=True,
            text=True,
        )
        if res.returncode == 0 and pdf_path.exists():
            return True
    return False


def convert_with_powerpoint_com(pptx_path: Path, pdf_path: Path) -> bool:
    ps = (
        "$ErrorActionPreference='Stop'; "
        f"$in='{pptx_path}'; $out='{pdf_path}'; "
        "$ppt = New-Object -ComObject PowerPoint.Application; "
        "$ppt.Visible = 1; "
        "$pres = $ppt.Presentations.Open($in,$false,$false,$false); "
        "$pres.SaveAs($out,32); "
        "$pres.Close(); $ppt.Quit(); "
        "Write-Output 'OK';"
    )
    res = subprocess.run(
        ["powershell", "-NoProfile", "-Command", ps],
        capture_output=True,
        text=True,
    )
    return res.returncode == 0 and pdf_path.exists()


def main() -> None:
    parser = argparse.ArgumentParser(description="Export PPTX to PDF and verify consistency.")
    parser.add_argument("pptx", help="Input PPTX")
    parser.add_argument("--output", default=None, help="Output PDF path")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero when checks fail")
    parser.add_argument("--json-out", default=None, help="Write report JSON")
    args = parser.parse_args()

    pptx_path = Path(args.pptx)
    if not pptx_path.exists():
        raise FileNotFoundError(f"PPTX not found: {pptx_path}")
    pdf_path = Path(args.output) if args.output else pptx_path.with_suffix(".pdf")

    slide_count = len(Presentation(str(pptx_path)).slides)

    method = None
    if convert_with_soffice(pptx_path, pdf_path):
        method = "soffice"
    elif convert_with_powerpoint_com(pptx_path, pdf_path):
        method = "powerpoint_com"
    else:
        raise RuntimeError("Failed to export PDF (soffice + PowerPoint COM both failed)")

    pdf_pages = count_pdf_pages(pdf_path)
    ts_ok = pdf_path.stat().st_mtime >= pptx_path.stat().st_mtime
    page_ok = pdf_pages == slide_count

    report = {
        "pptx": str(pptx_path),
        "pdf": str(pdf_path),
        "method": method,
        "pptx_slides": slide_count,
        "pdf_pages": pdf_pages,
        "timestamp_ok": ts_ok,
        "page_count_ok": page_ok,
        "pass": ts_ok and page_ok,
    }

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.strict and not report["pass"]:
        raise SystemExit(2)


if __name__ == "__main__":
    main()
