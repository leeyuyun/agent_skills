# Public Source Playbook

Collect public airfare data conservatively and reproducibly.

## Scope

Use public web information only.
Do not use private airline APIs or approval-system write-back.

## Collection Checklist

1. Fix query dimensions:
- route, date window, cabin, passenger count, stop preference
2. Capture metadata for every offer:
- source site, capture timestamp, currency, URL
3. Keep snapshots:
- save raw rows in `public_fares.csv`
4. Normalize:
- airport codes, date format, currency, time format

## Operational Guardrails

- Respect robots and site terms.
- Avoid high-frequency crawling.
- Use retries with backoff for transient failures.
- Log missing pages or blocking events as data quality warnings.

## Source Notes (for policy design)

- Google Travel: pricing context and tracking concepts  
  https://blog.google/products/travel/google-flights-find-deals/
- Skyscanner Help: price-alert operation pattern  
  https://help.skyscanner.net/hc/en-us/articles/115002499829-How-do-I-set-up-or-cancel-email-price-alerts
- KAYAK Help: alert cadence and significant-change notification pattern  
  https://kayak.ai/help/noguarantee

Use these as behavior references, not as guaranteed fare outcomes.
