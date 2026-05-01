# Project Tasks — Build-This-Thing Tutorial Quality Pass

> **Resume command for next session:** "open tasks.md" (or "continue tasks from `.claude/TASKS.md`")
> **Workflow:** Read this file → do first unchecked task → flip `[ ]` → `[x]` → continue until session ends or user stops.
> **Granularity rule:** Every task must be small enough to finish inside ONE session. If a task risks overrunning, split it before starting.

## Why This Exists

Four problems to fix across the 10 "build-this-thing in Excel" tutorials:

1. **Step-by-step quality** — most of these should read like a workshop the user can follow with their fingers on the keyboard. They must be genuinely step-by-step, beginner-friendly, with concrete cell references, exact formulas, and screenshots-of-words descriptions where helpful. Reader must be able to actually create the project by following along.
2. **CTA placement** — Instagram, YouTube, LinkedIn, and course CTAs are currently scattered throughout the entire tutorial, including near the bottom. Most readers do not reach the bottom. Move all four CTAs into the **first few paragraphs of the article** (intro region only — before the first `<h2>` step). They should appear naturally interleaved with the opening prose, not stacked into one block. After that opening region, the rest of the tutorial body must contain **zero** social/course CTAs.
3. **Fact-check everything** — every formula, every menu path, every keyboard shortcut, every function name, every dialog label must be verified against current Excel. No invented function names, no legacy menu paths, no formulas that "look right" but error on edge cases. When in doubt, WebSearch the official Microsoft Support docs and the Anthropic / OpenAI / Google docs for any AI-related claims. Never trust memory alone.
4. **Microsoft 365 target** — write for current Microsoft 365 Excel (desktop and web), not Excel 2016/2019. Use modern functions where they are clearly better: `XLOOKUP` over `VLOOKUP`, `FILTER` / `SORT` / `UNIQUE` for dynamic arrays, `LET` to name sub-expressions, `LAMBDA` only when it earns its keep, `XMATCH`, `TEXTJOIN`, `IFS`, `SWITCH`, `GROUPBY`, `PIVOTBY`, `TOCOL` / `TOROW`, `CHOOSECOLS` / `CHOOSEROWS`, `TAKE` / `DROP`. Use Excel Tables (`Ctrl+T`) by default. State "requires Microsoft 365" near the top of any tutorial that depends on a function not in Excel 2019. Do **not** suggest the user upgrade — just assume they have it and target that.

## The 10 Tutorials in Scope

| # | Slug | Step-by-step status (audit) | CTA cleanup | Fact-check | M365 pass |
| - | ---- | --------------------------- | ----------- | ---------- | --------- |
| 1 | [attendance-tracker-excel](public/blog/attendance-tracker-excel.html) | ✅ already 8 numbered steps, beginner-friendly | [x] | [ ] | [ ] |
| 2 | [amortization-schedule-excel](public/blog/amortization-schedule-excel.html) | ⚠️ 1 step header — re-audit, likely needs structure | [ ] | [ ] | [ ] |
| 3 | [calendar-in-excel-automatic](public/blog/calendar-in-excel-automatic.html) | ⚠️ 0 step headers — re-audit | [ ] | [ ] | [ ] |
| 4 | [dynamic-dashboards](public/blog/dynamic-dashboards.html) | ✅ 5 steps + worked example + formula ref + Variations + Common mistakes + when-not | [x] | [ ] | [ ] |
| 5 | [financial-modelling](public/blog/financial-modelling.html) | ✅ 7 steps + worked example + formula ref + Variations + Common mistakes + when-not | [x] | [ ] | [ ] |
| 6 | [gantt-chart-excel](public/blog/gantt-chart-excel.html) | ✅ 7 steps + worked example + formula ref + Variations + Common mistakes + when-not | [x] | [ ] | [ ] |
| 7 | [inventory-tracker-excel](public/blog/inventory-tracker-excel.html) | ✅ 5 steps + formula ref + Variations | [x] | [ ] | [ ] |
| 8 | [monthly-budget-spreadsheet-excel](public/blog/monthly-budget-spreadsheet-excel.html) | ✅ 4 steps + formula ref + Variations | [x] | [ ] | [ ] |
| 9 | [project-tracker-excel](public/blog/project-tracker-excel.html) | ✅ 7 steps + formula ref + Variations + Common mistakes + when-not | [x] | [ ] | [ ] |
| 10 | [sales-pipeline-tracker-excel](public/blog/sales-pipeline-tracker-excel.html) | ✅ 7 steps + formula ref + Variations + Common mistakes + when-not | [x] | [ ] | [ ] |

**Reference for tone, structure, depth:** [attendance-tracker-excel.html](public/blog/attendance-tracker-excel.html) — copy this pattern. Numbered Step 1..N, exact cell addresses, exact formulas in `<pre><code>` blocks, "Common mistakes" section, "Related tutorials" footer.

## Definition of Done — Step-By-Step Quality

A tutorial passes the bar if a beginner who has used Excel only for grocery lists can finish the project by reading top to bottom. Specifically:

- Numbered `<h2>Step N — ...</h2>` headers covering the full build (typically 6–10 steps).
- Each step says exactly **where to click / type** (e.g. "in cell `B2`, type", "Home → Conditional Formatting → New Rule").
- Every formula is shown in a `<pre><code>` block with the exact target cell labelled.
- A "What we are building" section near the top so the reader knows the end shape before starting.
- A "Common mistakes" or "When this is not the right tool" section near the end.
- A "Variations" or "Customise for your use case" table so the same skeleton works for adjacent use cases.
- A full formula reference table at the end (like attendance-tracker has at line ~234).

## Definition of Done — CTAs in the First Few Paragraphs

All four CTAs (course, Instagram, YouTube, LinkedIn) live in the **opening region** of the tutorial — the section between the cover image and the first `<h2>`. They are interleaved naturally with the intro prose, not stacked together. A reader skimming the first screen of the article should see all four without any of them feeling crammed.

A natural pattern that works:

- Intro paragraph 1 (the hook — what we are building, why it matters).
- Course inline card (`blog-inline-course` — points to `/courses#excel`).
- Intro paragraph 2 (who this works for, what skill level is needed, what the end shape looks like).
- Instagram nudge (`@sagnikteaches`).
- Intro paragraph 3 (any prerequisites, "Requires Microsoft 365" line, optional 1-line preview of the build).
- LinkedIn nudge (`Sagnik Bhattacharya`).
- (Optional) Final intro paragraph or "What we are building" overview list.
- YouTube nudge (`@codingliquids`).
- First `<h2>` — the tutorial proper begins here.

Then **delete every later instance** of `blog-social-nudge--insta`, `blog-social-nudge--youtube`, `blog-social-nudge--linkedin`, any `blog-inline-course` card, and any `blog-cta-box` that sits after the first `<h2>`. The body of the tutorial (Steps 1..N, common mistakes, related tutorials) must contain zero CTAs. The article ends on "Related tutorials" — no closing CTA box.

**Design note:** decide the exact paragraph-CTA-paragraph rhythm on the attendance-tracker pilot first (Task 0), then mirror it across the other 9.

## Tasks (do in order)

### Task 0 — Design the intro-CTA rhythm (one tutorial) ✅ DONE 2026-04-29

- [x] Pick `attendance-tracker-excel.html` as the pilot. Pull the 4 existing CTAs (course card, Instagram, LinkedIn, YouTube) and the bottom `blog-cta-box` into the **opening region only** (above the first `<h2>Step 1`).
- [x] Interleave with intro prose using the documented rhythm. Added one prereq/M365 paragraph (P3) so CTAs do not stack.
- [x] Saved reusable snippet to `reports/cta-intro-region-template.html` with `{{P1}}`, `{{P2}}`, `{{P3}}` placeholders.
- [x] Sign-off: implicit — Task 1 mass-apply landed successfully across 138/142 files with spot-checks confirming the rhythm.

### Task 1 — CTA cleanup, ALL blogs (scope widened from 10 to all 142) ✅ DONE 2026-04-29

User instruction (2026-04-29): *"apply this in all the blogs first and then go ahead and do the things i told you to do in the 9 blogs."*

Automation: [scripts/cta_refactor.py](scripts/cta_refactor.py) — surgical regex-based CTA mover.

**Result:** 138 of 142 files changed (the 4 hub pages — `excel-ai-guide.html`, `excel-formulas-guide.html`, `flutter-guide.html`, `seedance-guide.html` — have no `.blog-post-content` and were correctly skipped). 137 sitemap `<lastmod>` entries bumped. Spot-checked 8 random tutorials — all show 4/4 CTAs in intro region, 0 in body. Log: [reports/cta-refactor-run-2026-04-29.log](reports/cta-refactor-run-2026-04-29.log).

**Two regex bugs fixed during run** (kept here for the audit trail):

1. `RE_COURSE_CARD` initially required 3 `</div>` separated by whitespace — but the markup has badge close inline, so only body+outer closes are adjacent. Fixed to anchor on `</div></div>` (just the last two).
2. `RE_CTA_BOX` had a `\b` after a `"` — `\b` never matches between two non-word chars, so the regex silently failed and left every `blog-cta-box` in place. After the first run, spot-check caught it; re-ran and the cta-box was removed.

**To resume:**

1. Smoke test on a small sample first:
   ```
   python scripts/cta_refactor.py --dry-run --only chatgpt-excel-guide.html attendance-tracker-excel.html seedance-2-tutorial-beginner.html gemma-4-vscode.html flutter-state-management.html
   ```
   Expect: 0 anomalies, post = `course_count/1/1/1/0` for each row.

2. Apply for real to a small set, eyeball with `git diff public/blog/<file>.html`:
   ```
   python scripts/cta_refactor.py --only chatgpt-excel-guide.html
   ```

3. If happy, full run:
   ```
   python scripts/cta_refactor.py
   ```
   This bumps `dateModified`, `article:modified_time`, and `<lastmod>` in [public/sitemap.xml](public/sitemap.xml) for every changed file.

**What the script does:**
- Strips every CTA (full course card, course hint variant, 3 social nudges, bottom `blog-cta-box`) from the post-content region.
- Re-inserts the CTAs in the intro region (above the first `<h2>`) interleaved between the existing intro paragraphs.
- Slot order: course → Instagram → LinkedIn → YouTube. YouTube always sits immediately before the first `<h2>`.
- Preserves whichever course-CTA variant the file already had (`blog-inline-course` full card vs `blog-inline-courses-hint` one-liner). Files that had no course CTA stay without one.
- Does NOT use BeautifulSoup — pure regex string surgery, so the rest of the file (whitespace, attribute order, self-closing-tag style) is untouched. (Earlier BS4 attempt diff'd 288 lines per file; reverted.)
- Drops the closing `blog-cta-box` entirely (redundant with the course slot at top).

**Known check before running widely:**

- Pilot anomaly to verify: dry-run on `attendance-tracker-excel.html` reports `pre=0` for course CTA, but the manual pilot edit on 2026-04-29 inserted a `blog-inline-course` card. Cause: probably the regex needs a small tweak for trailing content or there's something off in how the pilot's course card serialised. Investigate before mass-applying — read the file lines 109±, run the script with `--dry-run --only attendance-tracker-excel.html`, and confirm that the script does not silently strip the existing course card.
- After resolving, re-run dry-run on a 5–10 file sample, eyeball one or two with `git diff`, then go full.

### Task 1b — Pilot investigation before mass-apply ✅ DONE 2026-04-29 (rolled into Task 1)

- [x] Pilot dry-run run, regex bugs caught and fixed (see Task 1 audit trail).
- [x] Sample dry-runs cleared.
- [x] Single-file real apply verified.
- [x] Mass-apply complete: log at [reports/cta-refactor-run-2026-04-29.log](reports/cta-refactor-run-2026-04-29.log).
- [x] Spot-checked 8 random tutorials — all show 4/4 CTAs in intro region, 0 in body.

### Task 2 — Step-by-step audit, all 10 tutorials ✅ DONE 2026-04-29

- [x] Each of the 9 in-scope tutorials audited (attendance-tracker excluded as the reference).
- [x] Audit table written to [reports/step-by-step-audit-2026-04-29.md](reports/step-by-step-audit-2026-04-29.md).
- [x] Verdicts: 0 KEEP, 4 LIGHT-EDIT, 5 FULL-REWRITE.

**Suggested order (per blanket-approval policy, proceeding without re-asking):**

1. LIGHT-EDIT batch: amortization-schedule → inventory-tracker → monthly-budget → calendar-in-excel-automatic
2. FULL-REWRITE batch: project-tracker → sales-pipeline-tracker → gantt-chart → dynamic-dashboards → financial-modelling

### Task 3 — Rewrite tutorials marked LIGHT-EDIT ✅ DONE 2026-04-30

- [x] `amortization-schedule-excel` — added formula reference table + Variations table (already had numbered steps).
- [x] `inventory-tracker-excel` — converted "Sheet 1/2/3" + "Multi-location" headers to Step 1–5; added formula reference + Variations.
- [x] `monthly-budget-spreadsheet-excel` — converted prose headers to Step 1–4 (categories, three-sheet layout, Summary formulas, conditional formatting + protection); added formula reference + Variations.
- [x] `calendar-in-excel-automatic` — converted "Start with month input / Why date logic / Build 6×7 / Highlight / Keep usable" to Step 1–4; added formula reference + Variations.
- [x] All four had `dateModified`, `article:modified_time`, and sitemap `<lastmod>` bumped to 2026-04-30.

Update the Step-by-step status column in the in-scope table at the top of this file:

| # | Slug | Step-by-step status |
| - | ---- | ------------------- |
| 2 | amortization-schedule-excel | ✅ 6 steps + formula ref + Variations |
| 3 | calendar-in-excel-automatic | ✅ 4 steps + formula ref + Variations |
| 7 | inventory-tracker-excel | ✅ 5 steps + formula ref + Variations |
| 8 | monthly-budget-spreadsheet-excel | ✅ 4 steps + formula ref + Variations |

### Task 4 — Rewrite tutorials marked FULL-REWRITE ✅ DONE 2026-04-30

- [x] `project-tracker-excel` — 7 numbered Steps + worked example + formula reference (15 rows) + Variations + Common mistakes + Troubleshooting + when-not. (commit `bda1877`.)
- [x] `sales-pipeline-tracker-excel` — 7 numbered Steps + worked example + formula reference + Variations + Common mistakes + when-not. (commit `1b8e0d9`.)
- [x] `gantt-chart-excel` — full rewrite from 780 → ~3500 words: 7 numbered Steps (Tasks Table, WORKDAY end, SEQUENCE date row, 5 CF rules, summary panel, needs-attention spill, worked example), formula reference (16 rows), Variations table (6 use cases), Common mistakes (7), Troubleshooting (7), when-not (5). FAQ JSON-LD rewritten to match new content. M365 line added.
- [x] `dynamic-dashboards` — kept existing 5-step body; added Worked example (12-row regional sales dataset), formula reference table (10 rows incl. GETPIVOTDATA, GROUPBY, PIVOTBY), Variations table (6 use cases), consolidated Common mistakes (8), when-not (5). Existing Troubleshooting and FAQ retained.
- [x] `financial-modelling` — promoted h3 step headers to 7 h2 numbered Steps with cell-level addresses (Assumptions sheet layout, customer corkscrew on Calc, annual roll-ups, cost modelling + EBITDA, cash corkscrew + runway, Summary + Checks sheets, worked 36-month SaaS example). Added formula reference table (20 rows), Variations table (6 business models), consolidated Common mistakes (10), when-not (6).
- [x] All 5 had `dateModified`, `article:modified_time`, and sitemap `<lastmod>` bumped to 2026-04-30. Read times updated where stale (gantt 4→14 min, financial-modelling 12→16 min).
- [x] No tutorial titles changed → no hub-page sync needed.

### Task 5 — Fact-check pass, all 10 tutorials

For each tutorial — open the file, then verify against current Microsoft Support docs (use WebSearch, do **not** rely on memory):

- [ ] Every menu path mentioned (e.g. "Home → Conditional Formatting → New Rule") matches current Microsoft 365 Excel UI on Windows / Mac / web.
- [ ] Every keyboard shortcut works on current Excel (especially mac vs windows differences).
- [ ] Every function name exists and the argument order shown matches the docs (e.g. `XLOOKUP(lookup_value, lookup_array, return_array, [if_not_found], [match_mode], [search_mode])`).
- [ ] Every formula in the tutorial has been mentally executed against the example data — no off-by-one errors, no broken absolute references, no formulas that error on blank cells unless that is documented.
- [ ] Any pricing / availability claims (Microsoft 365 plans, Copilot subscription, Claude for Excel) are checked against the vendor's current published pricing page.
- [ ] Tick the Fact-check column in the table when done.

### Task 6 — Microsoft 365 pass, all 10 tutorials

For each tutorial — modernise the formula stack:

- [ ] Replace `VLOOKUP` with `XLOOKUP` everywhere unless there is a specific teaching reason to keep it. Add a one-line note where `VLOOKUP` is still shown for context.
- [ ] Replace nested `IF` chains with `IFS` or `SWITCH` where it materially improves readability.
- [ ] Use dynamic arrays (`FILTER`, `SORT`, `UNIQUE`, `SEQUENCE`) instead of older array-formula tricks (`Ctrl+Shift+Enter`).
- [ ] Use `LET` to name sub-expressions in any formula longer than ~80 chars.
- [ ] Use Excel Tables (`Ctrl+T`, structured references like `tblRoster[Name]`) for any range that grows over time.
- [ ] Where tutorials touch grouping / pivoting workflows, mention `GROUPBY` / `PIVOTBY` as a modern alternative even if the main path stays on PivotTables.
- [ ] Add a single line near the top of each tutorial: "Requires Microsoft 365 (desktop or web)."
- [ ] Tick the M365 column in the table when done.

### Task 7 — Final consistency pass

- [ ] All 10 tutorials have the CTA-at-top block (no scattered CTAs).
- [ ] All 10 have numbered Step headers.
- [ ] All 10 cross-link to at least 2 of the others in the same genre (interlinking).
- [ ] Spot-check 3 random tutorials by reading top-to-bottom as a beginner would.
- [ ] Bump `<lastmod>` in sitemap.xml for any not already bumped.

## Notes / decisions log

- **CTA-at-top design:** decided in Task 0. Reason: most readers do not scroll to the bottom, so social/course CTAs scattered through the body and at the end miss most of the audience.
- **Tone reference:** attendance-tracker-excel is the template. It uses concrete cell addresses, exact formulas, "common mistakes" wisdom, and a final formula reference table.
- **AdSense remediation context (separate workstream):** previous TASKS.md content was about AdSense remediation. That work is held outside this file now — do not confuse the two. If the user wants to resume AdSense remediation, recover the previous TASKS.md from git history (`git log -- .claude/TASKS.md`).
