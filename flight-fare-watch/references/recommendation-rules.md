# Recommendation Rules

Use deterministic labels and numeric thresholds.

## Categories

1. `save-money`
- Condition: `internal_price - best_public_price` is greater than:
- `max(min_save, internal_price * min_save_pct)`
- Default: `min_save=500`, `min_save_pct=0.05`

2. `same-price-better`
- Condition:
- `abs(public_price - internal_price) <= same_price_band`
- quality gain >= `quality_gain_threshold`
- Default: `same_price_band=300`, `quality_gain_threshold=2`

3. `time-shift`
- Condition:
- departure/return shift is within 120 minutes
- shifted offer is cheaper than internal quote
- saving >= `min_save / 2`
- Explain exact shift in minutes.

4. `monitor`
- Condition:
- Comparable offers exist but none meet criteria above.

5. `no-data`
- Condition:
- No comparable public fares for the route/date/cabin.

## Quality Scoring Baseline

Start score at `0`, then:
- Stops:
- nonstop `+4`
- 1 stop `+2`
- 2+ stops `+0`
- Better than internal stops: `+2`
- Departure shift:
- within 30 min `+2`
- within 120 min `+1`
- over 120 min `-1`
- Return shift:
- within 30 min `+1`
- over 180 min `-1`
- Same airline as internal quote: `+1`

## Output Requirements

For each recommendation include:
- recommendation type
- internal/public price
- delta and delta percentage
- suggested airline/times/stops
- source and URL
- machine-readable reason
