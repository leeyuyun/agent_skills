# Tool Selection

Choose tools by operation, not preference.

## 1. `openpyxl` First For Workbook-Fidelity Edits

Use when:
- Editing existing `.xlsx` or `.xlsm`.
- Preserving formulas, sheet structure, and cell-level metadata.
- Managing named ranges and per-cell operations.

Notes:
- For macro workbooks, open with `keep_vba=True` when macro retention is required.
- Prefer writing to a new output file by default.

## 2. `pandas` For Table-Style Transforms

Use when:
- Filtering, grouping, joining, pivot-like summaries, deduplication.
- Schema-level cleanup and data quality checks.
- Exporting curated tables to workbook tabs.

Notes:
- Validate dtype coercion after `read_excel`.
- Avoid silent date parsing assumptions.

## 3. `xlsxwriter` For New Report Outputs

Use when:
- Building fresh report workbooks from structured data.
- Adding charts and styled summary tables from scratch.
- Reproducible executive report generation.

Notes:
- Best for new files; not intended for in-place edit of existing workbooks.

## 4. Practical Decision Rule

1. Existing workbook + fidelity needed -> `openpyxl`.
2. Heavy data reshape -> `pandas` (then export).
3. Presentation-focused new workbook -> `xlsxwriter`.
4. Mixed workflow -> `pandas` transform + `openpyxl` integration.

## Sources

- Office Scripts fundamentals:
  `https://learn.microsoft.com/en-us/office/dev/scripts/develop/scripting-fundamentals`
- SpreadsheetML structure:
  `https://learn.microsoft.com/en-us/office/open-xml/spreadsheet/structure-of-a-spreadsheetml-document`
- pandas API:
  `https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html`
  `https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.to_excel.html`
- openpyxl docs:
  `https://openpyxl.readthedocs.io/en/stable/`
- XlsxWriter docs:
  `https://xlsxwriter.readthedocs.io/`
