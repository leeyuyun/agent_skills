# Formula Guidelines

Preserve formula integrity unless the user explicitly asks to convert formulas to values.

## 1. Before Editing

1. Detect formula-heavy sheets from profile output.
2. Identify anchor cells and totals rows.
3. Confirm whether absolute/relative references should remain unchanged.

## 2. During Editing

1. Insert/delete rows with care near formula ranges.
2. Avoid replacing formula cells with raw values by accident.
3. If restructuring columns, update references deterministically.
4. Re-check named ranges after structural edits.

## 3. After Editing Validation

1. Compare row counts before/after.
2. Recompute key totals and checkpoints.
3. Spot-check formulas in first/middle/last data blocks.
4. Report all formula-impacting changes in final output notes.

## 4. Common Function Families

Use official Excel semantics for:
- Lookup: `XLOOKUP`, `INDEX/MATCH`, `VLOOKUP` (legacy compatibility).
- Conditional aggregate: `SUMIFS`, `COUNTIFS`, `AVERAGEIFS`.
- Dynamic arrays: `FILTER`, `SORT`, `UNIQUE`.
- Date and time: `DATE`, `EOMONTH`, `NETWORKDAYS`.

## Source

- Official Excel function reference:
  `https://support.microsoft.com/en-us/office/excel-functions-alphabetical-b3944572-255d-4efb-bb96-c6d90033e188`
