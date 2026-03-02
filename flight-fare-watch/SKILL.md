---
name: flight-fare-watch
description: Daily flight-fare intelligence for business travel. Use when users need to survey current public airfare, compare it with internal or agency quotes, and generate recommendation-ready outputs (save-money alternatives, same-price better-flight options, and time-shift suggestions). Trigger on requests about pre-approval trip pricing checks, fare gap analysis, route/date watchlists, or daily airfare report generation from CSV data.
---

# Flight Fare Watch

## Overview

Run a repeatable daily workflow for airfare monitoring and quote comparison.
Use public web prices for decision support without integrating approval systems or airline private APIs.

## Input Contract (Read First)

Read `references/data-contract.md` before processing files.
Use CSV as the default exchange format:
- `internal_quotes.csv`: company or agency quoted fares
- `public_fares.csv`: externally collected current fares
- `watchlist.csv`: routes and travel windows to monitor daily

## Daily Survey Workflow

1. Normalize scope for today:
- Confirm routes, dates, cabin class, stop constraints, and traveler preferences.
- Exclude approval-state writes. This skill is read-and-recommend only.

2. Build or refresh watchlist:
- Use `scripts/build_watchlist.py` from internal quote files.
- Keep one row per route/date/cabin combination.

3. Collect public fares:
- Use browser-based collection (for example with local `playwright` skill) or user-provided exports.
- Store findings in `public_fares.csv` with source URL and timestamp.
- Follow `references/public-source-playbook.md`.

4. Compare with internal quotes:
- Run `scripts/compare_quotes.py`.
- Produce recommendation CSV + markdown summary.

5. Generate recommendations:
- Use policy from `references/recommendation-rules.md`.
- Always report recommendation type and measurable reason (price delta, schedule shift, stop count).

6. Publish daily report:
- Include route-level status: `save-money`, `same-price-better`, `time-shift`, `monitor`, or `no-data`.
- Include concrete alternative offer link and expected saving.

## Recommendation Categories

Use exactly these categories:
- `save-money`: Public fare is materially cheaper than internal quote.
- `same-price-better`: Price is similar but quality is better (airline/stops/time window).
- `time-shift`: Small departure or return time shift gives meaningful savings.
- `monitor`: No strong alternative now; keep tracking.
- `no-data`: Missing comparable public data.

## Command Patterns

If Python is not globally available, run scripts with `uv`:

```bash
uv run --python 3.11 scripts/build_watchlist.py \
  --internal data/internal_quotes.csv \
  --out data/watchlist.csv
```

```bash
uv run --python 3.11 scripts/compare_quotes.py \
  --internal data/internal_quotes.csv \
  --public data/public_fares.csv \
  --out-report outputs/daily-fare-report.md \
  --out-csv outputs/recommendations.csv
```

## Report Contract

Return:
1. Output file paths.
2. Count by recommendation category.
3. Top opportunities by saving amount.
4. Data quality warnings (missing fields, unmatched routes, stale collection time).
5. Explicit non-goals (no purchase action, no approval write-back).

## Guardrails

- Respect target site terms and robots guidance.
- Avoid aggressive crawling or bypass behavior.
- Keep recommendation language advisory, not guaranteed outcomes.
- Prefer reproducible runs from saved CSV snapshots.
