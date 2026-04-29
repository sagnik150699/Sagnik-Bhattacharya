# Step-by-Step Quality Audit — 9 Build-This-Thing Excel Tutorials

Date: 2026-04-29

Bar (per `.claude/TASKS.md` "Definition of Done — Step-By-Step Quality"):

- Numbered `<h2>Step N — ...</h2>` headers covering the full build (typically 6–10 steps).
- Cell-level instructions (specific cell addresses, exact formulas in `<pre><code>`).
- Formula reference table at the end.
- "Common mistakes" section.
- "Variations" / "Customise for your use case" table.

Reference template: [attendance-tracker-excel.html](public/blog/attendance-tracker-excel.html).

## Audit table

| Tutorial | Words | Step headers | Cell-level | Formula ref table | Common mistakes | Variations | Score | Verdict |
| --- | ---: | ---: | :---: | :---: | :---: | :---: | :---: | --- |
| [amortization-schedule-excel](public/blog/amortization-schedule-excel.html) | 2453 | 6 | Y | N | Y | N | 3/5 | LIGHT-EDIT |
| [calendar-in-excel-automatic](public/blog/calendar-in-excel-automatic.html) | 2356 | 0 | Y | N | Y | N | 2/5 | LIGHT-EDIT |
| [dynamic-dashboards](public/blog/dynamic-dashboards.html) | 2634 | 5 | N | N | N | N | 1/5 | FULL-REWRITE |
| [financial-modelling](public/blog/financial-modelling.html) | 2227 | 0 | N | N | N | N | 0/5 | FULL-REWRITE |
| [gantt-chart-excel](public/blog/gantt-chart-excel.html) | 780 | 0 | N | N | Y | N | 1/5 | FULL-REWRITE |
| [inventory-tracker-excel](public/blog/inventory-tracker-excel.html) | 2044 | 0 | Y | N | Y | N | 2/5 | LIGHT-EDIT |
| [monthly-budget-spreadsheet-excel](public/blog/monthly-budget-spreadsheet-excel.html) | 2082 | 0 | Y | N | Y | N | 2/5 | LIGHT-EDIT |
| [project-tracker-excel](public/blog/project-tracker-excel.html) | 800 | 0 | N | N | Y | N | 1/5 | FULL-REWRITE |
| [sales-pipeline-tracker-excel](public/blog/sales-pipeline-tracker-excel.html) | 795 | 0 | N | N | Y | N | 1/5 | FULL-REWRITE |

## Summary

- **0 KEEP.** None of the nine pass the bar without work.
- **4 LIGHT-EDIT** (need numbered Step headers + formula reference table + Variations section, content largely already there):
  - `amortization-schedule-excel` — already has 6 step headers and cell refs; just missing formula table + variations.
  - `calendar-in-excel-automatic` — has cell refs and mistakes; missing step structure.
  - `inventory-tracker-excel` — has cell refs and mistakes; missing step structure.
  - `monthly-budget-spreadsheet-excel` — has cell refs and mistakes; missing step structure.
- **5 FULL-REWRITE** (under-developed or missing the actionable "build with me" backbone):
  - `dynamic-dashboards` — has 5 step headers but no cell-level instructions, no mistakes, no variations.
  - `financial-modelling` — fails every single criterion despite 2227 words.
  - `gantt-chart-excel` — only 780 words, no step structure, almost no concrete instructions.
  - `project-tracker-excel` — only 800 words, very thin.
  - `sales-pipeline-tracker-excel` — only 795 words, very thin.

## Suggested order for rewrites

Highest-traffic / highest-leverage first. Start with the LIGHT-EDIT batch (smaller per-file effort, faster wins), then tackle the FULL-REWRITE set:

1. **LIGHT-EDIT batch (~30 min each):**
   1. `amortization-schedule-excel`
   2. `inventory-tracker-excel`
   3. `monthly-budget-spreadsheet-excel`
   4. `calendar-in-excel-automatic`
2. **FULL-REWRITE batch (~60–90 min each):**
   5. `project-tracker-excel`
   6. `sales-pipeline-tracker-excel`
   7. `gantt-chart-excel`
   8. `dynamic-dashboards`
   9. `financial-modelling`

For every rewrite: also do the Microsoft 365 modernisation pass (Task 6 in TASKS.md) and the fact-check pass (Task 5) in the same session — touching the file once is cheaper than three times.

## Caveats on the audit

- The "cell-level" check is heuristic: ≥8 cell-reference patterns OR ≥5 `<pre><code>` blocks containing `=`. Some tutorials may pass the heuristic without truly being cell-level — eyeball before downgrading the verdict from FULL-REWRITE to LIGHT-EDIT.
- The "formula reference table" check looks for a `<th>Where</th>` or `<th>Formula</th>...does` pattern. None of the nine pass — every rewrite needs to add one.
- The "variations" check looks for a `<h2>Variations</h2>` or `Customise` heading. None pass — every rewrite needs to add one.
- Word counts include nav / footer markup-stripped HTML inside `.blog-post-content`. Treat as relative, not absolute.
