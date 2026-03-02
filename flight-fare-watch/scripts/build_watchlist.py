#!/usr/bin/env python3
"""Build a daily airfare watchlist from internal quotes."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


def _pick(row: dict[str, str], keys: Iterable[str], default: str = "") -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return default


@dataclass(frozen=True)
class WatchKey:
    trip_id: str
    origin: str
    destination: str
    depart_date: str
    return_date: str
    cabin: str


def load_internal_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return [dict(row) for row in reader]


def normalize_key(row: dict[str, str]) -> WatchKey:
    return WatchKey(
        trip_id=_pick(row, ["trip_id", "request_id"]),
        origin=_pick(row, ["origin", "from", "dep_airport"]).upper(),
        destination=_pick(row, ["destination", "to", "arr_airport"]).upper(),
        depart_date=_pick(row, ["depart_date", "outbound_date"]),
        return_date=_pick(row, ["return_date", "inbound_date"]),
        cabin=_pick(row, ["cabin", "cabin_class"], default="economy").lower(),
    )


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--internal", required=True, help="Path to internal_quotes.csv")
    parser.add_argument("--out", required=True, help="Path to output watchlist.csv")
    parser.add_argument("--currency", default="TWD", help="Default currency code")
    parser.add_argument("--max-stops", default="1", help="Default max stops")
    args = parser.parse_args()

    internal_path = Path(args.internal)
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    rows = load_internal_rows(internal_path)
    seen: set[WatchKey] = set()
    watch_rows: list[dict[str, str]] = []

    for row in rows:
        key = normalize_key(row)
        if not key.origin or not key.destination or not key.depart_date:
            continue
        if key in seen:
            continue
        seen.add(key)

        watch_rows.append(
            {
                "watch_id": f"{key.origin}-{key.destination}-{key.depart_date}-{key.cabin}",
                "trip_id": key.trip_id,
                "origin": key.origin,
                "destination": key.destination,
                "depart_date": key.depart_date,
                "return_date": key.return_date,
                "cabin": key.cabin,
                "preferred_depart_time": _pick(row, ["internal_depart_time", "depart_time_pref"]),
                "preferred_return_time": _pick(row, ["internal_return_time", "return_time_pref"]),
                "max_stops": args.max_stops,
                "target_currency": args.currency,
                "notes": "",
            }
        )

    fields = [
        "watch_id",
        "trip_id",
        "origin",
        "destination",
        "depart_date",
        "return_date",
        "cabin",
        "preferred_depart_time",
        "preferred_return_time",
        "max_stops",
        "target_currency",
        "notes",
    ]
    with out_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(watch_rows)

    print(f"watchlist rows: {len(watch_rows)}")
    print(f"output: {out_path}")


if __name__ == "__main__":
    main()
