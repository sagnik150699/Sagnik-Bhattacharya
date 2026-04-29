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
| 4 | [dynamic-dashboards](public/blog/dynamic-dashboards.html) | ✅ 5 numbered steps (verify quality) | [ ] | [ ] | [ ] |
| 5 | [financial-modelling](public/blog/financial-modelling.html) | ⚠️ 0 step headers — re-audit | [ ] | [ ] | [ ] |
| 6 | [gantt-chart-excel](public/blog/gantt-chart-excel.html) | ⚠️ 0 step headers — re-audit | [ ] | [ ] | [ ] |
| 7 | [inventory-tracker-excel](public/blog/inventory-tracker-excel.html) | ⚠️ 0 step headers — re-audit | [ ] | [ ] | [ ] |
| 8 | [monthly-budget-spreadsheet-excel](public/blog/monthly-budget-spreadsheet-excel.html) | ⚠️ 0 step headers — re-audit | [ ] | [ ] | [ ] |
| 9 | [project-tracker-excel](public/blog/project-tracker-excel.html) | ⚠️ 0 step headers — re-audit | [ ] | [ ] | [ ] |
| 10 | [sales-pipeline-tracker-excel](public/blog/sales-pipeline-tracker-excel.html) | ⚠️ 0 step headers — re-audit | [ ] | [ ] | [ ] |

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
- [ ] Show the user the rendered result and confirm the layout before applying to the other 9. ← **awaiting sign-off**

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

### Task 1b — Pilot investigation before mass-apply

- [ ] Run `python scripts/cta_refactor.py --dry-run --only attendance-tracker-excel.html`. If `pre=0` for the course slot, inspect `RE_COURSE_CARD` against the actual markup at line ~109. Tweak the regex if needed (most likely the multi-`</div>` close or surrounding whitespace differs from what I assumed).
- [ ] Re-run sample dry-runs across 6 files: 2 Excel, 2 Seedance, 1 Flutter, 1 hub. Aim for 0 anomalies.
- [ ] Apply for real to ONE non-pilot file. `git diff` it: only the intro region and the date stamps should differ. If anything else moves, stop and fix the script.
- [ ] Mass-apply: `python scripts/cta_refactor.py`. Save the stdout to `reports/cta-refactor-run-2026-04-29.log` for the audit trail.
- [ ] Spot-check 5 random files in the browser at `localhost:5000/blog/<slug>`. Confirm CTAs sit in the first screen, not in the body.

### Task 2 — Step-by-step audit, all 10 tutorials

- [ ] Read each tutorial fully (not just header counts) and grade it against "Definition of Done — Step-By-Step Quality" above.
- [ ] For each, write one row in `reports/step-by-step-audit-2026-04-29.md` (create the file) with:
  - filename
  - current word count
  - has numbered Step headers? Y/N
  - has cell-level instructions? Y/N
  - has formula reference table? Y/N
  - has Common mistakes? Y/N
  - has Variations table? Y/N
  - verdict: KEEP / LIGHT-EDIT / FULL-REWRITE
- [ ] Surface the audit table to the user before starting Task 3.

### Task 3 — Rewrite tutorials marked LIGHT-EDIT

- [ ] One file per session. Add missing numbered Steps, missing cell references, missing formula reference table.
- [ ] Keep existing prose where it works. Only restructure what is missing.
- [ ] Update `dateModified` in JSON-LD and bump `<lastmod>` in `public/sitemap.xml`.

### Task 4 — Rewrite tutorials marked FULL-REWRITE

- [ ] One file per session. Use attendance-tracker as the structural template.
- [ ] Keep the existing slug, title, image, and JSON-LD. Replace only the body (`.blog-post-content`).
- [ ] Update `dateModified` in JSON-LD and bump `<lastmod>` in `public/sitemap.xml`.
- [ ] Per the hub-sync rule: if the tutorial title changes meaningfully, also update `scripts/generate_hub_pages.py` and re-run it.

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
