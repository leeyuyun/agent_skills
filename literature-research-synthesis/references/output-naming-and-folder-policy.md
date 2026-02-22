# Output Naming and Folder Policy

Apply this policy on every run.

## 1. Required Variables

1. `report_slug`: topic normalized to kebab-case.
2. `run_date`: current date in `YYYYMMDD`.
3. `output_dir`: `outputs/{report_slug}-{run_date}/`.
4. `basename`: `{report_slug}-literature-review-{run_date}`.

## 2. File Naming Rules

Use exactly one basename:
1. `{basename}.md`
2. `{basename}.docx` (if required by decision tree)
3. `{basename}.pdf` (if required by decision tree)

Do not mix names like `report.md`, `final.md`, or ad hoc file names.

## 3. Folder Rules

1. Create `output_dir` before export.
2. Place all run artifacts in `output_dir`.
3. Keep intermediate files in the same folder when possible.
4. Avoid writing report artifacts to project root.

## 4. Suggested Example

If topic is `optical transceiver` and date is `20260222`:
1. Folder: `outputs/optical-transceiver-20260222/`
2. Files:
- `optical-transceiver-literature-review-20260222.md`
- `optical-transceiver-literature-review-20260222.docx`
- `optical-transceiver-literature-review-20260222.pdf`

## 5. Validation

1. Confirm all expected files exist in one folder.
2. Confirm same basename across all generated formats.
