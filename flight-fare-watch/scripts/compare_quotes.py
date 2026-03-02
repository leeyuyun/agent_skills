#!/usr/bin/env python3
"""Compare internal airfare quotes against public fares and emit recommendations."""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, Optional


def pick(row: dict[str, str], keys: Iterable[str], default: str = "") -> str:
    for key in keys:
        value = (row.get(key) or "").strip()
        if value:
            return value
    return default


def as_float(value: str) -> Optional[float]:
    try:
        if value is None:
            return None
        return float(str(value).replace(",", "").strip())
    except ValueError:
        return None


def as_int(value: str, default: int = 2) -> int:
    try:
        return int(float((value or "").strip()))
    except ValueError:
        return default


def parse_hhmm(value: str) -> Optional[int]:
    value = (value or "").strip()
    if not value:
        return None
    for fmt in ("%H:%M", "%H%M"):
        try:
            dt = datetime.strptime(value, fmt)
            return dt.hour * 60 + dt.minute
        except ValueError:
            continue
    return None


def signed_minute_diff(base: Optional[int], target: Optional[int]) -> Optional[int]:
    if base is None or target is None:
        return None
    return target - base


def minute_distance(base: Optional[int], target: Optional[int]) -> Optional[int]:
    diff = signed_minute_diff(base, target)
    if diff is None:
        return None
    return abs(diff)


def normalize_route(value: str) -> str:
    return (value or "").strip().upper()


def normalize_cabin(value: str) -> str:
    return (value or "").strip().lower() or "economy"


def route_key(origin: str, destination: str, depart_date: str, return_date: str, cabin: str) -> str:
    return "|".join(
        [
            normalize_route(origin),
            normalize_route(destination),
            (depart_date or "").strip(),
            (return_date or "").strip(),
            normalize_cabin(cabin),
        ]
    )


@dataclass
class InternalQuote:
    quote_id: str
    trip_id: str
    origin: str
    destination: str
    depart_date: str
    return_date: str
    cabin: str
    internal_price: float
    airline: str
    depart_time: str
    return_time: str
    stops: int
    source: str

    @property
    def key(self) -> str:
        if self.trip_id:
            return f"trip:{self.trip_id}"
        return f"route:{route_key(self.origin, self.destination, self.depart_date, self.return_date, self.cabin)}"


@dataclass
class PublicOffer:
    offer_id: str
    trip_id: str
    origin: str
    destination: str
    depart_date: str
    return_date: str
    cabin: str
    public_price: float
    airline: str
    depart_time: str
    return_time: str
    stops: int
    source: str
    url: str

    @property
    def key(self) -> str:
        if self.trip_id:
            return f"trip:{self.trip_id}"
        return f"route:{route_key(self.origin, self.destination, self.depart_date, self.return_date, self.cabin)}"


def load_internal(path: Path) -> list[InternalQuote]:
    out: list[InternalQuote] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            price = as_float(pick(row, ["internal_price", "quoted_price", "price"]))
            if price is None:
                continue
            out.append(
                InternalQuote(
                    quote_id=pick(row, ["quote_id", "id", "request_id"]),
                    trip_id=pick(row, ["trip_id"]),
                    origin=pick(row, ["origin", "from", "dep_airport"]),
                    destination=pick(row, ["destination", "to", "arr_airport"]),
                    depart_date=pick(row, ["depart_date", "outbound_date"]),
                    return_date=pick(row, ["return_date", "inbound_date"]),
                    cabin=pick(row, ["cabin", "cabin_class"], default="economy"),
                    internal_price=price,
                    airline=pick(row, ["internal_airline", "airline"]),
                    depart_time=pick(row, ["internal_depart_time", "depart_time"]),
                    return_time=pick(row, ["internal_return_time", "return_time"]),
                    stops=as_int(pick(row, ["internal_stops", "stops"], default="2"), default=2),
                    source=pick(row, ["agency", "source"], default="internal"),
                )
            )
    return out


def load_public(path: Path) -> list[PublicOffer]:
    out: list[PublicOffer] = []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        for row in csv.DictReader(f):
            price = as_float(pick(row, ["public_price", "price"]))
            if price is None:
                continue
            out.append(
                PublicOffer(
                    offer_id=pick(row, ["offer_id", "id"]),
                    trip_id=pick(row, ["trip_id"]),
                    origin=pick(row, ["origin", "from", "dep_airport"]),
                    destination=pick(row, ["destination", "to", "arr_airport"]),
                    depart_date=pick(row, ["depart_date", "outbound_date"]),
                    return_date=pick(row, ["return_date", "inbound_date"]),
                    cabin=pick(row, ["cabin", "cabin_class"], default="economy"),
                    public_price=price,
                    airline=pick(row, ["airline"]),
                    depart_time=pick(row, ["depart_time"]),
                    return_time=pick(row, ["return_time"]),
                    stops=as_int(pick(row, ["stops"], default="2"), default=2),
                    source=pick(row, ["source"], default="public"),
                    url=pick(row, ["url", "link"]),
                )
            )
    return out


def quality_score(offer: PublicOffer, internal: InternalQuote) -> int:
    score = 0
    if offer.stops == 0:
        score += 4
    elif offer.stops == 1:
        score += 2

    if internal.stops > offer.stops:
        score += 2

    internal_dep = parse_hhmm(internal.depart_time)
    offer_dep = parse_hhmm(offer.depart_time)
    dep_delta = minute_distance(internal_dep, offer_dep)
    if dep_delta is not None:
        if dep_delta <= 30:
            score += 2
        elif dep_delta <= 120:
            score += 1
        else:
            score -= 1

    internal_ret = parse_hhmm(internal.return_time)
    offer_ret = parse_hhmm(offer.return_time)
    ret_delta = minute_distance(internal_ret, offer_ret)
    if ret_delta is not None:
        if ret_delta <= 30:
            score += 1
        elif ret_delta > 180:
            score -= 1

    if offer.airline and internal.airline and offer.airline.strip().lower() == internal.airline.strip().lower():
        score += 1

    return score


def describe_shift(internal: InternalQuote, offer: PublicOffer) -> str:
    parts: list[str] = []
    dep_diff = signed_minute_diff(parse_hhmm(internal.depart_time), parse_hhmm(offer.depart_time))
    ret_diff = signed_minute_diff(parse_hhmm(internal.return_time), parse_hhmm(offer.return_time))

    if dep_diff is not None:
        direction = "later" if dep_diff > 0 else "earlier"
        parts.append(f"depart {abs(dep_diff)} min {direction}")
    if ret_diff is not None:
        direction = "later" if ret_diff > 0 else "earlier"
        parts.append(f"return {abs(ret_diff)} min {direction}")
    return ", ".join(parts)


def compare(
    internal_quotes: list[InternalQuote],
    public_offers: list[PublicOffer],
    min_save: float,
    min_save_pct: float,
    same_price_band: float,
    quality_gain_threshold: int,
) -> list[dict[str, str]]:
    by_key: dict[str, list[PublicOffer]] = {}
    for offer in public_offers:
        by_key.setdefault(offer.key, []).append(offer)

    rows: list[dict[str, str]] = []
    for internal in internal_quotes:
        offers = by_key.get(internal.key, [])
        if not offers:
            rows.append(
                {
                    "trip_id": internal.trip_id,
                    "quote_id": internal.quote_id,
                    "recommendation_type": "no-data",
                    "internal_price": f"{internal.internal_price:.2f}",
                    "public_price": "",
                    "delta": "",
                    "delta_pct": "",
                    "suggested_airline": "",
                    "suggested_depart_time": "",
                    "suggested_return_time": "",
                    "suggested_stops": "",
                    "source": "",
                    "url": "",
                    "reason": "No comparable public offer for this route/date/cabin.",
                }
            )
            continue

        best_price_offer = min(offers, key=lambda x: x.public_price)
        price_delta = internal.internal_price - best_price_offer.public_price
        threshold = max(min_save, internal.internal_price * min_save_pct)
        delta_pct = (price_delta / internal.internal_price) if internal.internal_price else 0.0

        recommendation_type = "monitor"
        reason = "No strong advantage over internal quote."
        picked = best_price_offer

        if price_delta >= threshold:
            recommendation_type = "save-money"
            reason = f"Cheaper by {price_delta:.2f} ({delta_pct * 100:.1f}%)."
        else:
            internal_ref = PublicOffer(
                offer_id="internal-ref",
                trip_id=internal.trip_id,
                origin=internal.origin,
                destination=internal.destination,
                depart_date=internal.depart_date,
                return_date=internal.return_date,
                cabin=internal.cabin,
                public_price=internal.internal_price,
                airline=internal.airline,
                depart_time=internal.depart_time,
                return_time=internal.return_time,
                stops=internal.stops,
                source=internal.source,
                url="",
            )
            internal_score = quality_score(internal_ref, internal)
            candidates_same_price = [
                offer for offer in offers if abs(offer.public_price - internal.internal_price) <= same_price_band
            ]
            if candidates_same_price:
                best_quality = max(candidates_same_price, key=lambda x: quality_score(x, internal))
                gain = quality_score(best_quality, internal) - internal_score
                if gain >= quality_gain_threshold:
                    recommendation_type = "same-price-better"
                    picked = best_quality
                    reason = (
                        f"Similar price band (+/-{same_price_band:.0f}) with better quality score "
                        f"(+{gain})."
                    )

            if recommendation_type == "monitor":
                shift_candidates: list[PublicOffer] = []
                for offer in offers:
                    dep_dist = minute_distance(parse_hhmm(internal.depart_time), parse_hhmm(offer.depart_time))
                    ret_dist = minute_distance(parse_hhmm(internal.return_time), parse_hhmm(offer.return_time))
                    dep_ok = dep_dist is None or dep_dist <= 120
                    ret_ok = ret_dist is None or ret_dist <= 120
                    if dep_ok and ret_ok and offer.public_price < internal.internal_price:
                        shift_candidates.append(offer)
                if shift_candidates:
                    picked = min(shift_candidates, key=lambda x: x.public_price)
                    shift_delta = internal.internal_price - picked.public_price
                    if shift_delta >= min_save / 2:
                        recommendation_type = "time-shift"
                        reason = f"{describe_shift(internal, picked)}; save {shift_delta:.2f}."

        final_delta = internal.internal_price - picked.public_price
        final_pct = (final_delta / internal.internal_price) if internal.internal_price else 0.0
        rows.append(
            {
                "trip_id": internal.trip_id,
                "quote_id": internal.quote_id,
                "recommendation_type": recommendation_type,
                "internal_price": f"{internal.internal_price:.2f}",
                "public_price": f"{picked.public_price:.2f}",
                "delta": f"{final_delta:.2f}",
                "delta_pct": f"{final_pct * 100:.2f}",
                "suggested_airline": picked.airline,
                "suggested_depart_time": picked.depart_time,
                "suggested_return_time": picked.return_time,
                "suggested_stops": str(picked.stops),
                "source": picked.source,
                "url": picked.url,
                "reason": reason,
            }
        )

    return rows


def write_csv(path: Path, rows: list[dict[str, str]]) -> None:
    fields = [
        "trip_id",
        "quote_id",
        "recommendation_type",
        "internal_price",
        "public_price",
        "delta",
        "delta_pct",
        "suggested_airline",
        "suggested_depart_time",
        "suggested_return_time",
        "suggested_stops",
        "source",
        "url",
        "reason",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    total_saving = 0.0
    for row in rows:
        label = row["recommendation_type"]
        counts[label] = counts.get(label, 0) + 1
        if label in {"save-money", "time-shift"}:
            total_saving += as_float(row["delta"]) or 0.0

    lines: list[str] = []
    lines.append("# Daily Flight Fare Comparison Report")
    lines.append("")
    lines.append(f"- Generated at: {datetime.now().isoformat(timespec='seconds')}")
    lines.append(f"- Total trips analyzed: {len(rows)}")
    lines.append(f"- Potential total saving (material): {total_saving:.2f}")
    lines.append("")
    lines.append("## Recommendation Counts")
    for key in sorted(counts.keys()):
        lines.append(f"- {key}: {counts[key]}")
    lines.append("")
    lines.append("## Top Opportunities")

    sortable = []
    for row in rows:
        sortable.append((as_float(row["delta"]) or 0.0, row))
    sortable.sort(key=lambda x: x[0], reverse=True)

    top = [item[1] for item in sortable[:10]]
    if not top:
        lines.append("- None")
    else:
        for item in top:
            lines.append(
                "- "
                f"trip_id={item['trip_id'] or '-'}, "
                f"type={item['recommendation_type']}, "
                f"save={item['delta']}, "
                f"airline={item['suggested_airline'] or '-'}, "
                f"time={item['suggested_depart_time'] or '-'} / {item['suggested_return_time'] or '-'}"
            )
    lines.append("")
    lines.append("## Notes")
    lines.append("- This report is decision support only.")
    lines.append("- No purchase or approval write-back is performed.")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--internal", required=True, help="Path to internal_quotes.csv")
    parser.add_argument("--public", required=True, help="Path to public_fares.csv")
    parser.add_argument("--out-report", required=True, help="Path to markdown report")
    parser.add_argument("--out-csv", required=True, help="Path to recommendation CSV")
    parser.add_argument("--min-save", type=float, default=500.0, help="Absolute price delta threshold")
    parser.add_argument("--min-save-pct", type=float, default=0.05, help="Relative price delta threshold")
    parser.add_argument("--same-price-band", type=float, default=300.0, help="Same-price comparison band")
    parser.add_argument("--quality-gain-threshold", type=int, default=2, help="Min quality gain for same-price-better")
    args = parser.parse_args()

    internal = load_internal(Path(args.internal))
    public = load_public(Path(args.public))
    results = compare(
        internal_quotes=internal,
        public_offers=public,
        min_save=args.min_save,
        min_save_pct=args.min_save_pct,
        same_price_band=args.same_price_band,
        quality_gain_threshold=args.quality_gain_threshold,
    )
    write_csv(Path(args.out_csv), results)
    write_markdown(Path(args.out_report), results)

    print(f"internal quotes: {len(internal)}")
    print(f"public offers: {len(public)}")
    print(f"recommendations: {len(results)}")
    print(f"csv: {args.out_csv}")
    print(f"report: {args.out_report}")


if __name__ == "__main__":
    main()
