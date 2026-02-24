# Report Recipes

Use these recipes for repeatable Excel outputs.

## Recipe A: Clean Dataset Workbook

1. Profile source workbook.
2. Normalize headers on target sheet.
3. Apply dedupe + null handling rules.
4. Save to `<name>.cleaned.xlsx`.
5. Return change log with impacted columns.

## Recipe B: Summary Sheet Add-On

1. Keep original data sheet intact.
2. Create a new `Summary` sheet.
3. Write grouped metrics and totals.
4. Add validation rows for grand totals.
5. Save as new output file.

## Recipe C: Chart-Ready Report Workbook

1. Transform data with `pandas`.
2. Export curated tables.
3. Build report workbook with `xlsxwriter`.
4. Add charts and notes sheet.
5. Include run metadata (`source`, `date`, `filters`).

## Quality Checklist

1. Figure/table titles are clear.
2. Units are explicit.
3. Totals are auditable.
4. Workbook opens without repair warnings.
5. Final file path and sheet map are reported.
