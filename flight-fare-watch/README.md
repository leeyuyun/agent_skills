# flight-fare-watch

Daily business-travel fare intelligence skill for Codex-style agents.

## What It Does

- Builds/refreshes a route-date-cabin `watchlist.csv` from internal quote exports.
- Compares public fares against internal or agency quotes with deterministic rules.
- Produces recommendation outputs with actionable categories:
  - `save-money`
  - `same-price-better`
  - `time-shift`
  - `monitor`
  - `no-data`

## Included Files

- `SKILL.md`: workflow, constraints, and output contract.
- `agents/openai.yaml`: interface metadata.
- `references/`: data contract, public source playbook, and recommendation policy.
- `scripts/build_watchlist.py`: create deduplicated watchlist rows.
- `scripts/compare_quotes.py`: scoring + recommendation generation.

## Typical Commands

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

## Notes

- Advisory workflow only; no booking or approval write-back.
- Public data collection should respect site terms and robots guidance.
- Prefer repeatable runs from saved CSV snapshots.
