---
name: excel-workbook
description: Create, clean, analyze, and automate Excel workbook workflows for `.xlsx`, `.xlsm`, and `.csv` inputs with reproducible outputs. Use when requests involve profiling workbook structure, normalizing headers, preserving formulas while editing data, generating summary sheets, preparing chart-ready exports, or converting manual spreadsheet steps into deterministic script-based operations.
---

# Excel Workbook

Execute Excel tasks with deterministic scripts and explicit data-safety rules.
Prefer reproducible transformations over manual ad-hoc edits.

## 1. Lock Workbook Contract

Capture before editing:
1. Source files and target output format.
2. Sheets to read or modify.
3. Formula preservation requirement (`strict` or `best-effort`).
4. Header policy (keep as-is or normalize).
5. Row-level operations (filter, aggregate, dedupe, split, merge).
6. Whether macros must remain (`.xlsm` with VBA).
7. Ask whether the user can provide a reference template workbook (optional).

Suggested prompt:
- "If you have a reference template workbook, please share it so I can align structure/style. If not, I will proceed with best-practice defaults."

If any requirement is ambiguous, default to non-destructive output in a new file.
If no reference template is provided, continue with explicit assumptions and document them in the final summary.

## 2. Choose Engine From References

Read:
- `references/tool-selection.md`
- `references/formula-guidelines.md`

Read when needed:
- `references/report-recipes.md` for report-style workbook outputs.

Engine defaults:
1. Use `openpyxl` for workbook-preserving edits, formulas, and sheet-level operations.
2. Use `pandas` for table transforms and joins.
3. Use `xlsxwriter` when producing fresh report workbooks with charts.

## 3. Run Deterministic Steps

### 3.1 Profile first
Run:
`python scripts/workbook_profile.py <input.xlsx> --out <profile.json>`

Use profile results to confirm:
- Actual sheet names.
- Estimated data region and formula density.
- Candidate header row.

### 3.2 Normalize headers when requested
Run:
`python scripts/normalize_headers.py <input.xlsx> --sheet "<SheetName>" --row 1 --out <normalized.xlsx>`

### 3.3 Apply requested edits
Follow strict order:
1. Duplicate source to working output.
2. Apply structural edits (sheet create/delete/rename).
3. Apply data edits (insert/update/filter/aggregate).
4. Validate formulas and key totals after edits.

## 4. Formula and Safety Rules

1. Never overwrite original workbook unless explicitly requested.
2. Preserve formula cells unless user asks for value materialization.
3. When editing `.xlsm`, keep macro content intact unless user requests removal.
4. Record changed sheets and changed column names in the final summary.
5. If formula references break, report exact impacted sheet/range and provide fix options.

## 5. Output Contract

Return:
1. Output file path(s).
2. Short change log (sheet-level and column-level).
3. Validation notes (formulas, row counts, duplicate checks).
4. Any unresolved risk with concrete next action.

## 6. Included Scripts

1. `scripts/workbook_profile.py`
- Inspects workbook metadata and sheet statistics.

2. `scripts/normalize_headers.py`
- Converts a selected header row into deterministic snake_case names.

Run scripts before custom coding whenever they satisfy the request.
