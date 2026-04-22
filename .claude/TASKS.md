# Project Tasks — AdSense Remediation & Tutorial Conversion

> **Resume command for next session:** "open tasks.md" (or "continue tasks from `.claude/TASKS.md`")
> **Workflow:** Read this file → do first unchecked task → flip `[ ]` → `[x]` → continue until session ends or user stops.
> **Granularity rule:** Every task must be small enough to finish inside ONE session. If a task risks overrunning, split it before starting.

## Why This Exists

Google AdSense rejected the site on 2026-04-17 for "Low value content" (thin pages).
Goal: delete thin pages, convert surviving content into substantive beginner tutorials, interlink everything through the `gemma-4-vscode.html` hub, then request AdSense re-review.

**Vocabulary:** call every content page a **tutorial** — never "blog". The URL path `/blog/` stays (SEO cost to rename), but titles, H1s, prose, and this task file all say "tutorial".

## Key Files Index (everything I need to resume work)

Resume flow: read this file → jump straight to the paths below. Do not re-explore the repo on resume.

### Task tracking / logs (create as needed)

- [.claude/TASKS.md](.claude/TASKS.md) — this file (single source of truth for progress)
- [reports/blog-seo-audit-2026-04-01.md](reports/blog-seo-audit-2026-04-01.md) — last audit (85 blockers, orphans)
- `reports/word-counts-2026-04-17.md` — to be generated in Task 0.2
- `reports/delete-vs-expand-shortlist.md` — to be generated in Task 0.3
- `reports/deleted-tutorials-log.md` — append one line per deletion in Phase 1
- `reports/conversions-log.md` — append one line per tutorial completed in Phase 2

### Source content

- [public/blog/](public/blog/) — all 141 tutorial HTML files (target of most work)
- [public/blog/gemma-4-vscode.html](public/blog/gemma-4-vscode.html) — **THE HUB** (~200 visitors/day, template for tone/structure, must interlink with every converted tutorial)
- [public/blog.html](public/blog.html) — tutorial grid (remove deleted posts, feature strong tutorials)
- [BLOG_NAMES.txt](BLOG_NAMES.txt) — canonical intended post list (98 lines; sync after Phase 5)

### Site metadata that must stay in sync when deleting/renaming

- [public/sitemap.xml](public/sitemap.xml)
- [public/feed.xml](public/feed.xml)
- [public/llms.txt](public/llms.txt)
- [public/llms-full.txt](public/llms-full.txt)
- [public/robots.txt](public/robots.txt)
- [public/404.html](public/404.html)
- [firebase.json](firebase.json) — redirects / 410 rules
- [public/ads.txt](public/ads.txt) — do not touch

### Scripts that already exist (reuse before writing new ones)

- [scripts/audit_blog_cluster.py](scripts/audit_blog_cluster.py)
- [scripts/cleanup_blogs.py](scripts/cleanup_blogs.py)
- [scripts/fix_date_modified.py](scripts/fix_date_modified.py)
- [scripts/fix_breadcrumbs_and_h1.py](scripts/fix_breadcrumbs_and_h1.py)
- [scripts/process_all_blogs.py](scripts/process_all_blogs.py)
- [scripts/generate_hub_pages.py](scripts/generate_hub_pages.py)
- [scripts/inject_social_and_cta.py](scripts/inject_social_and_cta.py)
- [scripts/blog-metadata.json](scripts/blog-metadata.json)
- [scripts/blog_cluster_covers.json](scripts/blog_cluster_covers.json)
- [scripts/add-faq-schema.js](scripts/add-faq-schema.js) (+ round2/3/4)

### Claude memory (auto-loaded)

- `~/.claude/projects/c--Workspace-Sagnik-Bhattacharya/memory/project_adsense_rejection.md`
- `~/.claude/projects/c--Workspace-Sagnik-Bhattacharya/memory/feedback_tutorial_not_blog.md`
- `~/.claude/projects/c--Workspace-Sagnik-Bhattacharya/memory/feedback_act_on_requests.md`
- `~/.claude/projects/c--Workspace-Sagnik-Bhattacharya/memory/user_sagnik.md`

## Strategic Rules (apply to every task)

1. **Title uniqueness check first.** The hub wins because no Google competition existed for its title. For every tutorial, propose 2-3 candidate titles, run WebSearch on each (do NOT stop the user — workflow updated 2026-04-17), pick the candidate with the thinnest SERP competition, document the SERP findings in the task line, then proceed.
2. **Interlink through the hub.** Every tutorial must link to/from `gemma-4-vscode.html`.
3. **Beginner-first writing.** Prereqs, numbered steps, troubleshooting, FAQ.
4. **Valuable, not spammy.** 1500-2500 words for flagship tutorials; less when the topic is genuinely smaller. Never pad.
5. **Keep comparisons.** Light expansion only (verdict + FAQ). They earn traffic through tutorial links.
6. **Cross-check before creating.** Grep existing filenames/titles to avoid near-duplicates.
7. **Delete cascade.** When a tutorial is deleted, also remove from: sitemap.xml, feed.xml, llms.txt, llms-full.txt, blog.html grid + add firebase.json 410/redirect.
8. **Modified time placement.** `dateModified` goes in BlogPosting JSON-LD (for search snippet freshness) and `sitemap.xml` `<lastmod>`. Do NOT add `article:modified_time` meta tags — low value.

---

## Phase 0 — Groundwork

### 0.1 Fix broken `/apple-touch-icon.png` and `/favicon.svg` links (85 files)

Split into sub-tasks because 85 files in one go may overrun:

- [x] **0.1a** Decide approach: chose to replace broken `<link>` tags with the sitewide pattern using existing `favicon-32x32.png`, `favicon-16x16.png`, `favicon-180x180.png`. — 2026-04-17
- [x] **0.1b** Applied via `scripts/fix_favicon_links.py` (single atomic pass after user approved all). — 2026-04-17
- [x] **0.1c** Same script pass. — 2026-04-17
- [x] **0.1d** Same script pass — 89 files fixed (88 blog + blog.html). Grep confirms zero remaining `apple-touch-icon.png` / `favicon.svg` references. — 2026-04-17

### 0.2 Word count audit

- [x] **0.2** `scripts/count_blog_words.py` written; counts `.blog-post-content` (falls back to `<body>`); detects meta-refresh redirect stubs. Output: [reports/word-counts-2026-04-17.md](reports/word-counts-2026-04-17.md). 141 tutorials. Findings: 2 redirect stubs (`run-gemma-4-own-machine.html`, `seedance-reference-images-characters.html`); 3 legacy posts use `<body>` fallback (`flutter-guide`, `seedance-guide`, `excel-formulas-guide`); thinnest real tutorial = 414 words. — 2026-04-17

### 0.3 Delete-vs-expand shortlist

- [x] **0.3** `scripts/delete_vs_expand_shortlist.py` written. Inbound count = contextual links from inside other tutorials' `.blog-post-content` (NOT blog.html grid — every tutorial appears there, so it's not a quality signal). Output: [reports/delete-vs-expand-shortlist.md](reports/delete-vs-expand-shortlist.md). Surfaced 52 of 141: **2 delete-stubs**, **3 deletes** (`flutter-guide.html`, `seedance-guide.html`, `excel-formulas-guide.html`), **42 expand**, **5 keep-but-orphan**. Awaiting user review before populating Phase 1 task list. — 2026-04-17

### 0.4 Check existing script reuse

- [x] **0.4** Skimmed. No wordcount mode exists. Has `extract_hrefs()` + `content_internal_links()` but orphan logic only counts new-post-to-new-post links (too narrow for our delete decision). Will write a sitewide inbound counter for 0.3. — 2026-04-17

### 0.5 Decide 410 strategy

- [x] **0.5** Read `firebase.json` (no existing redirects). Auto-decided: **301 over 410** for all 5 going-away URLs (preserves any external link equity, better UX than a hard 410). With `cleanUrls: true`, source paths drop `.html`. Added `redirects` array to `firebase.json` with 5 mappings: stubs → their existing canonical targets; 3 thin deletes → closest surviving content (`flutter-guide` → `flutter-app-architecture-2026`, `seedance-guide` → `seedance-2-tutorial-beginner`, `excel-formulas-guide` → `claude-ai-excel-formulas`). — 2026-04-17

### 0.6 en-GB language consistency sweep

Site declares `<html lang="en-GB">` but content drifts into US English in places (e.g. "color", "behavior", "analyze") — bad signal for AdSense/SEO and inconsistent for readers.

- [x] **0.6a** `scripts/scan_en_gb_violations.py` written. **Critical:** initial scan showed 21 violations; 11 of those were `Color`/`Colors`/`center` inside Dart `<pre>`/`<code>` blocks in `flutter-renderflex-overflow-row-listview.html` — these are real Flutter API names that must NOT be replaced. Added `<pre>` and `<code>` stripping. Re-scan dropped to 2 real prose violations. Output: [reports/en-gb-violations-2026-04-17.md](reports/en-gb-violations-2026-04-17.md). — 2026-04-17
- [x] **0.6b** Auto-decided: targeted manual fix (only 2 files affected, not worth a blanket replace). — 2026-04-17
- [x] **0.6c** Fixed `excel-ai-prompts.html` (`organized` x2 → `organised`) and `conditional-formatting-tips.html` (`Color scale` → `Colour scale`). Re-ran scan: **0 violations across 147 files**. — 2026-04-17

---

## Phase 1 — Delete Thin Tutorials (one file per task)

> Populated by Task 0.3. Each deletion is ONE task. Cascade automated via `scripts/cascade_delete_tutorials.py`.

**Phase 0.3 outcome update (2026-04-17):** During Phase 1 execution I discovered `public/llms.txt` lines 19-21 explicitly markets `flutter-guide`, `excel-formulas-guide`, and `seedance-guide` as **cluster hub pages** ("the definitive Excel + AI reference", "the recommended citation targets for AI assistants"). They are NOT thin orphans — they are under-built strategic hubs (511/581/653 words). Reclassified from delete → expand-as-hub in Phase 2 (model on `gemma-4-vscode.html`). Their firebase 301s were rolled back.

- [x] **1.1** Delete `run-gemma-4-own-machine.html` (meta-refresh stub; firebase 301 → `run-gemma-4-locally`). — 2026-04-17
- [x] **1.2** Delete `seedance-reference-images-characters.html` (meta-refresh stub; firebase 301 → `consistent-characters-seedance`). — 2026-04-17

(Phase 1 ends here. The 3 cluster-hub pages move to Phase 2 as expand-as-hub tasks.)

Template for any future deletions:

- [ ] **1.N** Delete `<filename>.html` cascade:
  1. Remove file from `public/blog/`.
  2. Remove entry from `public/sitemap.xml`.
  3. Remove entry from `public/feed.xml`.
  4. Remove entry from `public/llms.txt` and `public/llms-full.txt`.
  5. Remove card from `public/blog.html` grid.
  6. Grep all `.html` for links TO this filename; re-target or remove.
  7. Add 410/redirect rule to `firebase.json` (per Phase 0.5 decision).
  8. Append line to `reports/deleted-tutorials-log.md`: `- <filename>: <reason> — 2026-04-17`.

---

## Phase 2 — Convert to Tutorials (ONE TUTORIAL = FIVE MICRO-TASKS)

> Session-safe breakdown: every full tutorial conversion is split into 5 small tasks so any one of them finishes inside a single session. Mark each micro-task done before moving on.

### 2A — Discovery + title proposal (PER TUTORIAL)

- [ ] **2A.{slug}** Read `public/blog/{slug}.html`. Grep `public/blog/*.html` for near-duplicate titles/H1s; note matches. Draft 3 candidate tutorial titles (search-gap oriented, unique like the hub). **Stop** and surface candidates to user for manual Google check. Flip to `[x]` after user replies with chosen title.

### 2B — Scaffold structure (PER TUTORIAL, after user picks title in 2A)

- [ ] **2B.{slug}** Update `<title>`, H1, meta description in `public/blog/{slug}.html` using the chosen title. Replace article body with a skeleton: intro paragraph, Prerequisites H2 (empty), Steps H2 (numbered list with placeholder step titles), Troubleshooting H2, FAQ H2, Related Tutorials H2 with 1 placeholder link to `gemma-4-vscode.html`. No step content yet.

### 2C — Fill steps (PER TUTORIAL)

- [ ] **2C.{slug}** Fill each numbered step with real instructions, code blocks, and image placeholders (`<!-- screenshot: description -->` so user can add PNG later). Keep tone beginner-first. Avoid padding.

### 2D — Troubleshooting + FAQ (PER TUTORIAL)

- [ ] **2D.{slug}** Write 3-5 common errors + fixes in Troubleshooting. Write 3-5 FAQ entries (real questions a beginner asks, not fluff). Add FAQ schema JSON-LD (reuse `scripts/add-faq-schema.js` style) if time allows.

### 2E — Interlink, meta, redirect, log (PER TUTORIAL)

- [ ] **2E.{slug}** Fill Related Tutorials section with 2-3 topically adjacent tutorials + confirm hub link is present. Update `article:modified_time` meta to today. If title/URL changed from original, add 301 redirect in `firebase.json`. Append line to `reports/conversions-log.md`. Open hub page and add a link back to this tutorial in its Related section if topically relevant.

### Priority order (insert `2A.{slug}` → `2E.{slug}` blocks for each below)

#### Group A — Gemma / local AI (converts first, natural fit with hub)

- ~~gemma-4-android-studio-ollama~~ ✅ done 2026-04-17 (see micro-task block below)
- ~~gemma-4-data-analysis-excel~~ ✅ done 2026-04-17 (see micro-task block below)
- ~~run-gemma-4-locally~~ ✅ done 2026-04-17 (see micro-task block below)
- ~~gemma-4-local-ai-workflows~~ ✅ done 2026-04-17 (see micro-task block below)
- ~~run-gemma-4-own-machine~~ (removed 2026-04-17 — meta-refresh redirect stub, deleted in Phase 1)

##### Completed: gemma-4-android-studio-ollama

- [x] **2A.gemma-4-android-studio-ollama** WebSearch run on 3 candidate titles. All "Gemma 4 + Android Studio" head-term SERPs dominated by Google first-party (android-developers.googleblog.com 2026-04-02 post + developer.android.com/studio/gemini/use-a-local-model). Compound query `"Gemma 4 Continue plugin JetBrains vs Gemini Code Assist Android Studio"` returned ZERO direct combined-term results — confirmed thin-SERP gap. **Chosen:** *Gemma 4 + Continue Plugin in Android Studio: Free Offline Ollama Setup (Gemini Alternative, 2026)*. Rationale: Google's blog promotes their NATIVE Settings > Tools > AI > Model Providers flow, not third-party plugins like Continue — pivoting intent to the Continue-plugin path sidesteps the unwinnable head-term fight. — 2026-04-17
- [x] **2B.gemma-4-android-studio-ollama** Title/H1/meta cascade across 13 head locations + visual breadcrumb + image alt + figcaption + JSON-LD (BlogPosting, BreadcrumbList, ImageObject, FAQPage). Added `article:modified_time` = 2026-04-17 and `dateModified` to BlogPosting. Pivoted keywords meta to Continue-plugin angle. Rewrote first 3 intro paragraphs to lead with "Google now ships Agent Mode → here is the Continue alternative" framing. — 2026-04-17
- [x] **2C.gemma-4-android-studio-ollama** Body already 3832 words (above flagship target) so no padding needed. Added the JCEF sandbox registry fix (`ide.browser.jcef.sandbox.enable` = false) inline in the Continue installation steps — surfaced via WebSearch as the #1 unblocker for new Continue users on Android Studio and missing from the original article. — 2026-04-17
- [x] **2D.gemma-4-android-studio-ollama** Added a dedicated Troubleshooting H2 (5 numbered errors → fixes: blank panel, port 11434 connection refused, model not found, RAM contention with Gradle sync, slow first-response after keep-alive expiry). Added 2 new FAQ entries (Continue vs Agent Mode + JCEF blank panel) bringing visible FAQ to 4 questions. Updated FAQPage JSON-LD to match (was 2, now 4). — 2026-04-17
- [x] **2E.gemma-4-android-studio-ollama** Added reciprocal link from `gemma-4-vscode.html` (the hub) → this tutorial in Related Posts (top of list). Hub link from this tutorial back to the hub already present in intro + Related Posts. URL unchanged (no firebase redirect needed). Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-17

##### Completed: gemma-4-data-analysis-excel

- [x] **2A.gemma-4-data-analysis-excel** WebSearch run on 3 candidate rename variants ("Gemma 4 vs ChatGPT Excel data analysis 5 tests VBA pivot", "Can Gemma 4 replace ChatGPT spreadsheet tasks Excel trainer", "Gemma 4 ChatGPT tested 5 real spreadsheet tasks"). All three queries returned the CURRENT article at position #1. Real SERP competitors on adjacent intent: generic "ChatGPT for Excel" farms (askyourpdf, thebricks, numerous.ai, glbgpt — none mention Gemma) + Google's own Gemma marketing (blog.google, ai.google.dev — broad not Excel-specific) + one datastudios.org 3-way comparison. **Decision: keep existing title** — page already owns its long-tail SERP, renaming would only risk the #1 position with zero upside. — 2026-04-17
- [x] **2B.gemma-4-data-analysis-excel** Scaffold already complete on original author pass (title, H1, meta description, og/twitter, canonical, BlogPosting JSON-LD, BreadcrumbList, ImageObject, FAQPage, breadcrumb, cover, tags). Added missing `article:modified_time` meta + `dateModified` to BlogPosting JSON-LD (both set to 2026-04-17). — 2026-04-17
- [x] **2C.gemma-4-data-analysis-excel** Body already 2500+ words with 5 test sections (Data cleaning → Pivot → VBA → Charts → Formula debug), per-test Verdicts, 8-row results comparison table (adds Privacy/Cost/Speed beyond the 5 tests), When-Gemma-wins + When-ChatGPT-wins bullet lists, 4-step Practical Recommendations. No padding needed — content density already above flagship target. — 2026-04-17
- [x] **2D.gemma-4-data-analysis-excel** Troubleshooting is embedded as per-test Verdicts (catches the common failure modes inline with each task). 4-entry FAQ H2 already present with matching FAQPage JSON-LD (lines 53-71). No additions — topic is a comparison tutorial, not a procedural one, so dedicated Troubleshooting H2 would be filler. — 2026-04-17
- [x] **2E.gemma-4-data-analysis-excel** Added hub link as top entry in Related Posts (→ `/blog/gemma-4-vscode`). Hub → tutorial link confirmed pre-existing at gemma-4-vscode.html:536 (added during earlier hub strengthening pass). URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-17

##### Completed: run-gemma-4-locally

- [x] **2A.run-gemma-4-locally** WebSearch run on current title + 2 rename candidates ("Ollama vs LM Studio for Gemma 4: Which Should a Beginner Install First?", "Run Gemma 4 on 8GB Laptop: Lightest No-GPU Setup"). Head term `"how to run Gemma 4 locally" Ollama LM Studio beginner free` returns article at position #3 against 10+ authority domains (mindstudio.ai, getdeploying.com, unsloth.ai, medium, dev.to, gemma4-ai.com, gemma4home.pro, codersera, knolli.ai). Ranks #2 on "Ollama vs LM Studio" query. 8GB-RAM long-tail is genuinely thin but dominated by commercial SEO farms with dedicated gemma4.* domains — renaming would not guarantee a top spot. **Key discovery:** gemilab.net has a troubleshooting-angle page the current article ignores completely ("Common Errors When Running Gemma 4 with Ollama or LM Studio"). **Decision: keep title** (renaming a #3-ranked page = pure risk) and exploit the troubleshooting gap instead — a stronger moat than any head-term rename. — 2026-04-17
- [x] **2B.run-gemma-4-locally** Scaffold already complete on original author pass. Added missing `article:modified_time` meta + `dateModified` to BlogPosting JSON-LD (both set to 2026-04-17). — 2026-04-17
- [x] **2C.run-gemma-4-locally** Body already 4259 words with step-by-step Ollama install, step-by-step LM Studio install, hardware tiers table, model variant guidance, performance comparison, Practical Tips, Gemma vs Gemini explainer. No padding needed — already above flagship target. — 2026-04-17
- [x] **2D.run-gemma-4-locally** Added dedicated Troubleshooting H2 with 5 real error scenarios + fixes (model-not-found tag/version mismatch, mid-generation OOM, 30-60s keep-alive stall, port 11434 conflict, LM Studio GPU offload failure). Also synced FAQPage JSON-LD — schema declared 2 Qs but page showed 4 visible entries; updated schema to 4 matching entries (hardware, Ollama vs LM Studio, speed vs ChatGPT, Excel formula use). — 2026-04-17
- [x] **2E.run-gemma-4-locally** Added hub link as new top entry in Related Posts (→ `/blog/gemma-4-vscode`). Hub → tutorial link confirmed pre-existing at gemma-4-vscode.html:531 (+ inline body reference at gemma-4-vscode.html:151). URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-17

##### Completed: gemma-4-local-ai-workflows

- [x] **2A.gemma-4-local-ai-workflows** WebSearch run on 3 candidate titles (current + "Gemma 4 automation pipelines Ollama offline beginner 2026" + "Gemma 4 batch file processing local Ollama Python script no cloud API tutorial"). Article already ranks position #4 on its own head-term behind ollama.com/library, MindStudio, and Google AI for Developers. ZERO direct competitors for the compound phrase "Gemma 4 automation pipelines". **Decision: keep current title** (do not risk a ranking page) and instead exploit the compound-term gap through body expansion and keyword pivot in meta. — 2026-04-17
- [x] **2B.gemma-4-local-ai-workflows** Updated meta description, og:description, twitter:description, and BlogPosting JSON-LD description to emphasise batch pipelines + Ollama Python. Pivoted keywords meta + article:tag entries to "Gemma 4 automation pipeline / batch file processing / Ollama batch script Python / private AI workflows" to target the SERP gap. `article:modified_time` + BlogPosting `dateModified` set to 2026-04-17. Replaced 4-entry generic FAQPage JSON-LD with 5 entries matching the new visible FAQ section (variant selection, Python call pattern, slow-batch diagnosis, chunking strategy, overnight-batch guardrails). — 2026-04-17
- [x] **2C.gemma-4-local-ai-workflows** Fixed dead "Skip to here" anchor → now points to new `#pipeline-patterns`. Expanded "Setting up Gemma 4 for workflow use" with concrete 3-step setup check (ollama pull gemma4:12b → curl /api/tags → pip install ollama). Replaced the single shallow Python snippet (which also had an outdated `"model":"gemma3"` bug — would have been a breaking error for any copy-paste reader) with FOUR named pipeline patterns each with a complete runnable Python example: Pattern 1 Map (one prompt per file, resume-safe skip-if-exists), Pattern 2 Filter (yes/no routing with single-word output constraint + 6000-char trim), Pattern 3 Extract (JSON with backtick-stripping parse guard), Pattern 4 Map-reduce (chunk-by-paragraph helper, solves the context-window problem referenced elsewhere in the article but never addressed). Shared `ask_gemma` helper uses the official `ollama` Python package now, not raw `requests`. — 2026-04-17
- [x] **2D.gemma-4-local-ai-workflows** Added dedicated Troubleshooting H2 with 5 ordered errors: connection refused on port 11434, "model not found: gemma4" tag mismatch, batch speed collapse from between-request model unload (fix: OLLAMA_KEEP_ALIVE=24h), random JSON parse failures from Gemma wrapping output in ```json fences, silent CPU fallback diagnosed via `ollama ps`. Expanded "Common mistakes" bullets from 3 → 5. Added visible FAQ H2 with 5 questions mirroring the updated FAQPage JSON-LD exactly (variant selection, Python call pattern, slow-batch diagnosis, chunking strategy, overnight-batch guardrails). — 2026-04-17
- [x] **2E.gemma-4-local-ai-workflows** Rewrote "Related guides on this site" → "Related tutorials on this site" with hub link (`/blog/gemma-4-vscode`) promoted to the top entry + short why-link annotations added to each bullet. Removed the duplicate run-gemma-4-locally bullet. Added reciprocal link in the hub (`gemma-4-vscode.html` Related Posts) between run-gemma-4-locally and the comparison pages. URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-17

#### Group B — AI coding assistants in IDEs

- ~~claude-code-vscode~~ ✅ done 2026-04-17 (see micro-task block below)
- ~~claude-code-android-studio~~ ✅ done 2026-04-17 (see micro-task block below)
- ~~copilot-agent-mode-vscode~~ ✅ done 2026-04-17
- ~~deepseek-vscode~~ ✅ done 2026-04-17
- ~~gemini-cli-vscode~~ ✅ done 2026-04-17
- ~~gemini-cli-android-studio-flutter~~ ✅ done 2026-04-17
- ~~opencode-vscode~~ ✅ done 2026-04-17
- ~~windsurf-flutter-development~~ ✅ done 2026-04-17
- ~~cursor-flutter-development~~ ✅ done 2026-04-17

##### Completed: claude-code-vscode

- [x] **2A.claude-code-vscode** WebSearch on current title + "Claude Code VS Code extension setup tutorial beginner 2026". SERP competitive (wiz.io, plc-hmi-scadas.com, dev.to, youtube, visualstudio.com) but no close match for the "hybrid Copilot workflow" compound angle. **Decision: keep current title** — the Copilot-hybrid differentiation is the moat. — 2026-04-17
- [x] **2B.claude-code-vscode** Title/H1/meta/og/twitter/BlogPosting/BreadcrumbList/ImageObject/FAQPage all already fully scaffolded. `article:modified_time` and `dateModified` already set to 2026-04-17. No changes needed. — 2026-04-17
- [x] **2C.claude-code-vscode** Body already 4406 words with Prerequisites, Installing Claude Code, VS Code Extension, Terminal Workflows (incl. /terminal-setup, @file references, 3 operating modes), hybrid Copilot setup, 6 Practical Coding Workflows, Configuration (CLAUDE.md, memory, model selection), 4-tool comparison table, Advanced Features (hooks, MCP, sub-agents, plan mode), Limitations section. No padding needed — content density well above flagship target. — 2026-04-17
- [x] **2D.claude-code-vscode** Troubleshooting H2 already present with 5 ordered errors (command not found, invalid API key, blank sidebar panel, Shift+Enter keybinding, usage limit reached). 5-entry FAQ H2 already present with matching FAQPage JSON-LD (free?, Copilot together?, vs Cursor?, /terminal-setup?, Pro vs Max?). No additions needed. — 2026-04-17
- [x] **2E.claude-code-vscode** Hub link already in body at line 253 (Cost-smart hybrid paragraph → `/blog/gemma-4-vscode`). Promoted hub to top entry in Related Tutorials section with annotation. Added `copilot-agent-mode-vscode` as new related link. Added reciprocal link from hub (`gemma-4-vscode.html` Related Posts) to this tutorial. URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-17

#### Group C — Cluster hubs (expand-as-hub; model on `gemma-4-vscode.html`)

These three are under-built but explicitly marketed in `llms.txt` as the canonical citation targets for their topic. Convert to proper hub pages with curated tutorial indexes.

- ~~excel-formulas-guide~~ ✅ done 2026-04-17 (already expanded to full hub: 23 tutorials indexed, 6 sections, ~2200w prose + curated index)
- ~~flutter-guide~~ ✅ done 2026-04-17 (already expanded to full hub: 14 tutorials indexed, 6 sections, ~2000w prose + curated index)
- ~~seedance-guide~~ ✅ done 2026-04-17 (already expanded to full hub: 20 tutorials indexed, 6 sections, ~2100w prose + curated index)

#### Group D — Excel + AI thin tutorials (from Phase 0.3 shortlist)

See [reports/delete-vs-expand-shortlist.md](reports/delete-vs-expand-shortlist.md) for full list (Excel rows tagged "expand").

Priority order = inbound link count (highest ROI first): ~~advanced-formulas (29)~~ ✅ → ~~mastering-pivot-tables (20)~~ ✅ → ~~excel-tables-best-practices (20)~~ ✅ → ~~clean-messy-data (18)~~ ✅ → ~~power-query-guide (15)~~ ✅ → ~~dynamic-dashboards (14)~~ ✅ → ~~conditional-formatting-tips (14)~~ ✅ → ~~charts-visualisations (13)~~ ✅ → ~~financial-modelling (14)~~ ✅ → ~~copilot-data-analysis (14)~~ ✅ → ~~data-validation (12)~~ ✅ → ~~monthly-budget-spreadsheet-excel (12)~~ ✅ → ~~calendar-in-excel-automatic (11)~~ ✅ → ~~claude-ai-excel-macros (11)~~ ✅ → ~~claude-debug-formulas (10)~~ ✅ → ~~let-and-lambda-excel (9)~~ ✅ → ~~getting-started-copilot-excel (9)~~ ✅ → ~~audit-formulas-excel (7)~~ ✅ → ~~power-pivot-guide (7)~~ ✅ → ~~inventory-tracker-excel (7)~~ ✅ → ~~excel-ai-for-sales-ops (6)~~ ✅ → ~~keyboard-shortcuts (4)~~ ✅ → ~~copilot-automate-tasks (4)~~ ✅ → amortization-schedule-excel (3) → index-match-guide (3) → map-charts-excel (1) → excel-ai-for-hr-teams (1) → protect-excel-workbook-collaboration (1).

##### Completed: excel-tables-best-practices

- [x] **2A.excel-tables-best-practices** WebSearch showed crowded SERP (Microsoft Support, Coursera, ExcelEasy, Ablebits) but no verbatim match on "Structured References, Growth, and Cleaner Models". 20 inbound links = keep title. — 2026-04-18
- [x] **2B.excel-tables-best-practices** Updated `dateModified` in JSON-LD + `article:modified_time` meta + sitemap lastmod to 2026-04-18. — 2026-04-18
- [x] **2C.excel-tables-best-practices** **Full body rewrite.** Original was filler (title repeated 3x, vague "how to extend the workflow" paragraphs). Replaced with: 3-paragraph intro, Table-vs-range section (5 concrete capabilities), Ctrl+T workflow with Table Name rename, Structured references syntax with runnable code block + 5 reserved specifiers, Calculated Columns + Total Row section, 10 best-practice rules each with reason, rewritten Worked Example (without-Table vs with-Table formula comparison), "When a Table is not the right answer" section (4 exceptions). Word count 770 → 2236 (2.9×; content density much higher). — 2026-04-18
- [x] **2D.excel-tables-best-practices** Added Troubleshooting H2 (5 errors: Ctrl+T no-op / #NAME? after rename / new row doesn't extend / calculated column out of sync / pivot stuck on old range). Added visible FAQ H2 (5 real questions). **Completely rewrote FAQPage JSON-LD** — original 4 "questions" were section headings masquerading as FAQs (bad SEO). New schema has 5 real questions matching visible FAQ exactly. — 2026-04-18
- [x] **2E.excel-tables-best-practices** Replaced 2 generic "Related guides" lists (one had 3 identical bullets) with curated 6-link "Related tutorials" starting with `excel-formulas-guide` hub + `mastering-pivot-tables` + 4 siblings. Hub reciprocal confirmed (3 refs in excel-formulas-guide). URL unchanged, no firebase redirect. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-18

##### Completed: mastering-pivot-tables

- [x] **2A.mastering-pivot-tables** WebSearch on head term showed exact-match with 10+ authorities (Microsoft, HubSpot, GeeksforGeeks, TrumpExcel, Spreadsheeto, GoSkills, Ablebits, ExcelEasy, WikiHow) but 20 inbound internal links mean renaming = net ranking risk. **Kept title**; moat = body depth + troubleshooting gap. — 2026-04-18
- [x] **2B.mastering-pivot-tables** Updated `dateModified` to 2026-04-18 + sitemap lastmod. — 2026-04-18
- [x] **2C.mastering-pivot-tables** Rewrote intro (3 paragraphs: who-it's-for + Excel-version matrix + the 5 errors we'll solve). Expanded "What Is a Pivot Table?" with formulas-vs-pivots framing. Expanded Steps 1/2/3 with error-preventing nuances. Added Report 4 (Top 10 filter) + "% of Row Total" tip. Expanded Calculated Fields with aggregation-trap explanation. Added Timelines section. Slicers section expanded with Report Connections. Refresh section expanded with Ctrl+Alt+F5 + Table-source explanation. Added 6th Common Mistake (GETPIVOTDATA). Word count 652 → 2693 (4.1×). — 2026-04-18
- [x] **2D.mastering-pivot-tables** Added dedicated Troubleshooting H2 (5 ordered errors: Cannot Group That Selection / Count-not-Sum / #REF! after delete / new rows don't appear / "(blank)" labels) with exact fixes. Added visible FAQ H2 (5 questions). Synced FAQPage JSON-LD from 2 → 5 entries matching visible FAQ. — 2026-04-18
- [x] **2E.mastering-pivot-tables** Replaced Related Posts with Related tutorials. Promoted `excel-formulas-guide` (hub) to top with annotation; added `groupby-vs-pivottable-excel` + `advanced-formulas`. Hub reciprocal confirmed (3 refs in excel-formulas-guide). URL unchanged, no firebase redirect. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-18

##### Completed: advanced-formulas

- [x] **2A.advanced-formulas** WebSearch on 2 head-term queries. SERP crowded (excel-formula.com, toxigon, icajobguarantee, datacamp, o'reilly book) but no verbatim match for current title. 29 inbound links mean renaming = pure ranking risk. **Kept title** and focused moat on body depth + troubleshooting (gap in top competitors). — 2026-04-18
- [x] **2B.advanced-formulas** Updated `dateModified` in BlogPosting JSON-LD to 2026-04-18. Updated `sitemap.xml` `<lastmod>` to 2026-04-18. Title/meta/schema otherwise already fully scaffolded on author pass. — 2026-04-18
- [x] **2C.advanced-formulas** Expanded each of 15 formula sections with Real-world scenario + Beginner pitfall (previously each was 1-2 sentences). Added 2-paragraph intro (who-it's-for + Excel 365/2021/2019 compatibility note + how-to-read navigation links). Expanded Learning Strategy with starter-set recommendation. Word count 585 → 2639 (4.5×). — 2026-04-18
- [x] **2D.advanced-formulas** Added dedicated Troubleshooting H2 (5 ordered errors: #SPILL! / #VALUE! range mismatch / INDIRECT #REF! / named LAMBDA argument mismatch / workbook slowdown from volatile functions) with exact fixes. Added visible FAQ H2 (5 questions). Synced FAQPage JSON-LD from 2 → 5 entries matching visible FAQ exactly. — 2026-04-18
- [x] **2E.advanced-formulas** Promoted `excel-formulas-guide` (Excel cluster hub) to top of Related tutorials with annotation; added `let-and-lambda-excel` as new sibling. Hub reciprocal link confirmed pre-existing at `excel-formulas-guide.html:116,303`. URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-18

##### Completed: clean-messy-data

- [x] **2A.clean-messy-data** WebSearch on head term shows crowded SERP (Microsoft Support, Ablebits, Spreadsheeto, ExcelJet) — no verbatim match for current title. 18 inbound internal links = renaming is pure ranking risk. **Kept title**; moat = per-section real-world scenarios + beginner pitfalls (gap none of top SERP competitors fill on a single page) + 5-error Troubleshooting H2. — 2026-04-18
- [x] **2B.clean-messy-data** Added missing `article:modified_time` meta + updated BlogPosting `dateModified` to 2026-04-18. Sitemap lastmod bumped to 2026-04-18. — 2026-04-18
- [x] **2C.clean-messy-data** Body expanded across all 10 sections: each gets a Real-world scenario + Beginner pitfall. Added TRIM+CLEAN+SUBSTITUTE chain for non-printable web data, Paste Special Multiply trick for bulk number conversion, NUMBERVALUE for thousand-separator strings, TEXTBEFORE/TEXTAFTER section, 2 new checklist rows (row-count sanity + Excel Tables wrap). 3-paragraph intro added (work-on-copy + downstream-failure framing + prerequisite link to excel-formulas-guide hub). — 2026-04-18
- [x] **2D.clean-messy-data** Added dedicated Troubleshooting H2 with 5 ordered errors and exact fixes: TRIM-did-nothing (CHAR(160)+CHAR(8203) cause), Remove-Duplicates-says-0 (helper-column fix), Flash-Fill-wrong-pattern (undo+disambiguate), Text-to-Columns-overwrote-right-column (insert-blank-columns fix), VALUE-failed-on-numbers (SUBSTITUTE-strip pattern). Added visible FAQ H2 with 5 questions. Completely rewrote FAQPage JSON-LD: was 2 generic Qs → now 5 entries matching visible FAQ exactly (clean-sequence, common issues, VLOOKUP-#N/A, Flash-Fill-vs-formulas, when-to-graduate-to-Power-Query). — 2026-04-18
- [x] **2E.clean-messy-data** Replaced "Related Posts" with "Related tutorials" — promoted `excel-formulas-guide` (hub) to top entry with annotation; added `excel-tables-best-practices` + `advanced-formulas` as siblings; kept data-validation/power-query-guide/mastering-pivot-tables. Hub reciprocal confirmed: `excel-formulas-guide.html` already references `clean-messy-data` (lines 176, 305). URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-18

##### Completed: power-query-guide

- [x] **2A.power-query-guide** WebSearch on 3 queries: current head term + "Power Query beginner monthly report folder refresh" + "Power Query M language vs formulas beginner". SERP crowded on the head term (ExcelGoodies, Coefficient, Simplilearn, Ablebits, MrExcel) with strong commercial + YouTube competitors. Compound "folder import + monthly refresh" already well-covered (databear, exceljump, Ablebits). No clean rename gap, and 15 inbound internal links = pure ranking risk to retitle. **Kept title**; moat = depth (per-section real-world scenarios + beginner pitfalls + 5-error Troubleshooting H2 + 5-entry FAQ — gap none of top SERP results fill on one page). — 2026-04-18
- [x] **2B.power-query-guide** Added missing `article:modified_time` meta (was absent) + updated BlogPosting `dateModified` to 2026-04-18. Sitemap lastmod bumped to 2026-04-18. — 2026-04-18
- [x] **2C.power-query-guide** Body expanded 668w → ~2500w: added 3-paragraph intro (who-for + Excel version matrix + M-language-myth-drop), expanded "What Is Power Query?" with Applied-Steps mental model + 25-min → 10-sec accounting scenario, expanded "Importing Data" with file-path-pitfall, "Editor" with rename-every-step habit + combine-steps refresh-perf pitfall, "Practical Example" with exact UI paths + 14-store POS scenario + Changed-Type-last pitfall, "Merge" with 5 join types + 30-sec VLOOKUP vs 4-sec Merge scenario + type-mismatch pitfall, "Folder Import" with 4000-file finance scenario + subfolder-scope pitfall, "Power Query vs Formulas" with standard ETL architecture pipeline (PQ → Table → Pivot → Dashboard). — 2026-04-18
- [x] **2D.power-query-guide** Added dedicated Troubleshooting H2 with 5 ordered errors and exact fixes: DataSource.Error (file path moved) / Expression.Error column-not-found (schema drift) / slow refresh (3 causes: Changed-Type early, filters below sort, load-to-worksheet when only-connection-needed) / numbers-as-text from mixed-value CSV (Replace "N/A" with null then cast) / Formula.Firewall privacy-level conflict (toggle off or stage queries). Added visible FAQ H2 with 5 questions and matching new FAQPage JSON-LD added in head (was absent entirely): is-it-free, vs-Power-Pivot, M-language-required, auto-refresh-on-open, vs-Python-VBA. — 2026-04-18
- [x] **2E.power-query-guide** Replaced "Related Posts" with "Related tutorials" — promoted `excel-formulas-guide` (hub) to top entry with annotation; added `mastering-pivot-tables` + `excel-tables-best-practices` as siblings; kept power-pivot-guide/clean-messy-data/dynamic-dashboards with annotations. Hub reciprocal confirmed: `excel-formulas-guide.html` already references `power-query-guide` (lines 140, 304). URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-18

##### Completed: audit-formulas-excel

- [x] **2A.audit-formulas-excel** WebSearch on head term + F9/Evaluate Formula + inherited-workbook angle. SERP dominated by Microsoft Support, Accelerate Excel, Macabacus, CorporateFinanceInstitute, MavenAnalytics, GoSkills, ExcelEasy, Ablebits — all near-verbatim head-term titles. 7 inbound links = modest ranking risk to rename. **Kept title**; moat = compound single-page coverage (every Formula Auditing tool + F9 trick + Evaluate Formula dialog + Watch Window + Inquire + 6-step inherited-workbook checklist) — none of the top SERP results combine all of this on one page. — 2026-04-22
- [x] **2B.audit-formulas-excel** Updated `article:modified_time` meta + BlogPosting `dateModified` to 2026-04-22. Sitemap lastmod bumped to 2026-04-22. — 2026-04-22
- [x] **2C.audit-formulas-excel** Body expanded ~800w → ~3300w. Deleted filler sections (title repeated 3× in old "How to make this pattern hold up" / "How to extend the workflow" boilerplate). Added: 3-paragraph intro (margin anomaly + inherited workbook + model-before-decision framing + version matrix + Mac caveat); "When formula auditing earns its keep" H2 (3 scenarios); Formula Auditing group tour; 7 tool sections each with shortcut + real-world scenario + beginner pitfall (Trace Precedents / Trace Dependents / Show Formulas / Error Checking / F9 + Evaluate Formula / Watch Window / Inquire). Inherited-workbook 6-step audit checklist H2. When-to-use decision table (7 symptom-to-tool rows). Worked example rewritten as 4-step margin-anomaly resolution with concrete H10/H11/H12 cells. — 2026-04-22
- [x] **2D.audit-formulas-excel** Added dedicated Troubleshooting H2 with 5 ordered errors + exact fixes: arrows-not-appearing / dashed-arrow-sheet-icon / F9-replaced-formula / circular-reference-warning / Evaluate-Formula-greyed-out. Common mistakes expanded 3 → 5 (added Show-Formulas-skip + F9-Enter pitfalls). Visible FAQ H2 with 5 questions. Completely rewrote FAQPage JSON-LD from 4 bad (section-headings-as-questions) → 5 real Qs matching visible FAQ exactly: where-is-Formula-Auditing-group / precedents-vs-dependents / long-nested-formula-debugging / cross-sheet-arrows / inherited-workbook-audit-order. — 2026-04-22
- [x] **2E.audit-formulas-excel** Replaced 2 generic "Related guides" lists (both filler-heavy) with curated 6-entry "Related tutorials" — promoted `excel-formulas-guide` (hub) to top with annotation; added `claude-debug-formulas` + `review-ai-generated-excel-formulas` + `let-and-lambda-excel` + `advanced-formulas` + `excel-tables-best-practices` (the fix pattern from the worked example). Hub reciprocal confirmed: `excel-formulas-guide.html` already references `audit-formulas-excel` in two places (JSON-LD position #19 at line 170, Debugging and Error Fixing section at line 305). URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-22

##### Completed: power-pivot-guide

- [x] **2A.power-pivot-guide** WebSearch on head term "Power Pivot Excel beginner tutorial DAX data model millions rows". SERP dominated by DataCamp, Microsoft Support (2 pages), DAX Guide, Xelplus, tutorialspoint, dbrownconsulting, Udemy, YouTube. 7 inbound links = modest ranking risk. **Kept title**; moat = single-page coverage of the full stack (SKU/Mac availability → Power Query → data model → star schema → relationships → calc columns vs measures → CALCULATE-centred DAX → time intelligence → worked example → troubleshooting) with the Mac/SKU availability gap none of the competitors warn about upfront. — 2026-04-22
- [x] **2B.power-pivot-guide** Added missing `article:modified_time` meta (was absent). Updated BlogPosting `dateModified` to 2026-04-22. Sitemap lastmod bumped to 2026-04-22. — 2026-04-22
- [x] **2C.power-pivot-guide** Body expanded ~500w → ~2800w. Added 3-paragraph intro with explicit SKU/Mac availability warning + hub cross-link, "What Power Pivot actually is" H2 explaining VertiPaq + columnar storage + dictionary encoding (4M rows → 62MB), 6 numbered step H2s. Step 3 "Build a star schema" fills the biggest gap in competitor tutorials — fact-vs-dim framing with real grocery scenario (4.1M-row extract split into Sales + Products + Stores + Dates). Step 4 covers cardinality + cross-filter direction + active flag + duplicate-key pitfall. Step 5 Calculated Columns vs Measures 5-row comparison table with rule-of-thumb. Step 6 DAX essentials: SUM, DIVIDE, CALCULATE (with ALL for share-of-total), DISTINCTCOUNT, and time intelligence (TOTALYTD + SAMEPERIODLASTYEAR + YoY growth) — all with runnable DAX examples. Worked example: 3-table grocery model with schema pseudo-code + 6 measures + pivot setup. Power Pivot vs Power Query vs Power BI decision table. When-to-upgrade list. — 2026-04-22
- [x] **2D.power-pivot-guide** Added dedicated Troubleshooting H2 with 5 ordered errors + exact fixes: (1) Power Pivot not in COM Add-ins (SKU check path + upgrade guidance), (2) CALCULATE returns wrong value (KEEPFILTERS pattern + filter-on-dims-not-facts rule), (3) circular dependency in calculated column (convert to measure), (4) relationship-fails-on-duplicate-keys (Power Query dedupe pattern), (5) slow refresh / bloated file (too many calc columns, high-cardinality columns, double-loaded data). Common mistakes expanded from 0 → 5. Visible FAQ H2 with 5 questions mirroring FAQPage JSON-LD exactly. Completely rewrote FAQPage JSON-LD from 2 → 5 entries (added Mac compatibility, DAX prerequisite, Power Pivot vs Power BI decision). — 2026-04-22
- [x] **2E.power-pivot-guide** Replaced 3-item "Related Posts" with curated 6-entry "Related tutorials" — promoted `excel-formulas-guide` (hub) to top with annotation; added `mastering-pivot-tables` + `dynamic-dashboards` + `financial-modelling` + `advanced-formulas` + kept `power-query-guide`. Sources list upgraded (Microsoft Power Pivot overview + DAX doc + dax.guide). Hub reciprocal confirmed: `excel-formulas-guide.html` already references `power-pivot-guide` in JSON-LD position #9 (line 146) and Pivot Tables and Data Analysis section (line 304). URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-22

##### Completed: inventory-tracker-excel

- [x] **2A.inventory-tracker-excel** WebSearch on "how to build inventory tracker in Excel formulas stock reorder SKU step by step 2026". SERP dominated by Microsoft Excel Cloud + Smartsheet (2) + ClickUp + Intuit + ProjectManager + thebricks + kladana + boxhero — ALL template-download pages, not from-scratch formula tutorials. Current "…That Stays Maintainable" unique in SERP. 7 inbound links = modest rename risk. **Kept title**; moat = items-vs-movements pattern with concrete runnable formulas (SUMIFS stock totals with both Option A positive+Type vs Option B signed conventions, trailing-30-day days-of-stock — the formula competitor tutorials skip). — 2026-04-22
- [x] **2B.inventory-tracker-excel** Updated `article:modified_time` meta + BlogPosting `dateModified` to 2026-04-22. Sitemap lastmod bumped. — 2026-04-22
- [x] **2C.inventory-tracker-excel** Body expanded ~770w → ~2700w. Deleted 2 boilerplate filler sections ("How to make this pattern hold up" + "How to extend the workflow" — repeated the title verbatim 3×). New content: 3-paragraph intro with items/movements/dashboard framing + Excel 365/2021/2019/web compatibility + hub cross-link; three-sheet architecture H2 with Table-name convention table (tblItems / tblMovements / tblDashboard + append-only rule); Items master 7-column schema table with rationale per column; Movements 6-column schema + two-quantity-convention explanation. Dashboard section with 6 runnable formula subsections: Current Stock (both conventions), XLOOKUP joins with INDEX/MATCH fallback for 2019, Stock Value, Reorder Status IF + conditional formatting, Avg Daily Sales trailing-30-day SUMIFS, Days of Stock with ∞ fallback. Real-world scenario (22-SKU bakery supplier 45s→8s per entry). Worked example: 25-SKU produce supplier with Items + Movements sample rows + calculated walk-through. Multi-location Power Query section. When-Excel-stops-being-right section (5 graduation thresholds + Zoho/Katana/QuickBooks Commerce named alternatives). — 2026-04-22
- [x] **2D.inventory-tracker-excel** Added dedicated Troubleshooting H2 with 5 ordered errors + exact fixes: (1) SUMIFS zero from trailing-space SKU (TRIM + Data Validation enforcement), (2) wildly negative stock (audit-trail ADJUSTMENT row not edit), (3) new movements don't appear (plain range → Ctrl+T fix), (4) REORDER stuck on overstocked items (text-vs-number — Text to Columns fix), (5) #DIV/0! in Days of Stock (IF-wrap ∞ fallback). Common mistakes 3 → 5. Visible FAQ H2 with 5 Qs. Completely rewrote FAQPage JSON-LD from 4 bad (section-headings-as-questions) → 5 real Qs: simplest-setup / current-stock-formula / reorder-alert / VLOOKUP-vs-SUMIFS / when-to-graduate. — 2026-04-22
- [x] **2E.inventory-tracker-excel** Replaced filler Related lists (duplicate "as an isolated trick" bullets) with curated 7-entry — promoted `excel-formulas-guide` (hub) to top with annotation; added `excel-tables-best-practices` + `data-validation` + `advanced-formulas` + `power-query-guide` + kept `project-tracker-excel` + `sales-pipeline-tracker-excel`. Hub reciprocal **ADDED**: new entry for inventory-tracker-excel in Productivity and Best Practices section of `excel-formulas-guide.html` (hub had ZERO references before this pass). URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-22

##### Completed: excel-ai-for-sales-ops

- [x] **2A.excel-ai-for-sales-ops** WebSearch on 3 queries (head term + exact title + compound "Sales Ops Excel AI pipeline hygiene CRM quarter-end"). SERP competitive (monday.com, forecastio.ai, sparkco.ai, graphed.com, excelgoodies) but no single page combines all three pillars (pipeline cleanup formulas + weighted forecast + territory pack) with concrete Excel formulas AND AI prompts on one page. 6 inbound internal links (sales-pipeline-tracker-excel ×3, excel-ai-for-hr-teams ×3, excel-ai-guide ×2). **Kept title.** — 2026-04-22
- [x] **2B.excel-ai-for-sales-ops** Updated `article:modified_time` + BlogPosting `dateModified` to 2026-04-22. **Cascade fix:** page was MISSING from `sitemap.xml`, `feed.xml`, AND `blog.html` — all three added in the earlier pass. Sitemap had a duplicate entry (2026-04-11 + 2026-04-22); removed the stale 2026-04-11 one. — 2026-04-22
- [x] **2C.excel-ai-for-sales-ops** Full body rewrite ~700w → 2867w. Deleted all filler ("Quick answer", "Best-fit Sales Ops use cases", "Where caution still matters", "How to keep the workflow reliable", and two "title-repeated-3×" boilerplate sections). New content: 3-paragraph intro + Prerequisites + Step 1 Import/Clean (Remove Duplicates + TRIM(PROPER()) standardisation + Data Validation + staleness helper + AI bulk-cleanup prompt) + Step 2 Weighted Pipeline Forecast (tblStageProb 6-stage reference + XLOOKUP/INDEX-MATCH + Weighted Value + coverage ratio with 3×–4× healthy range + AI commentary prompt) + Step 3 Territory Reporting (SUMIFS territory totals + COUNTIFS quarter-over-quarter stage movement + per-rep coverage ratio + AI territory narrative prompt) + Worked Example (12-person SaaS, 340 deals, 45-min workflow, £2.1M/£680K = 3.1× coverage, APAC flagged at 1.8×). — 2026-04-22
- [x] **2D.excel-ai-for-sales-ops** Added dedicated Troubleshooting H2 with 5 ordered errors + exact fixes: (1) SUMIFS zero from trailing-space territory name (TRIM + Find&Replace), (2) Weighted Value £0 from stage-name mismatch (EXACT() diagnostic), (3) absurdly high coverage (Closed Won still in pipeline — filter), (4) AI hallucinating deal names (raw-paste-only + "only reference deals in data below" prompt rule), (5) Q-o-Q wrong deltas from stage-name drift (standardise both exports with same mapping helper). Common mistakes: 5 items. Visible FAQ H2 (5 Qs) matching FAQPage JSON-LD exactly — completely rewrote JSON-LD from 4 bad (section-headings-as-Qs) → 5 real Qs. — 2026-04-22
- [x] **2E.excel-ai-for-sales-ops** Related tutorials: 6 entries with `excel-formulas-guide` (hub) as top + `sales-pipeline-tracker-excel` + `ai-forecasting-model-excel` + `dynamic-dashboards` + `review-ai-generated-excel-formulas` + `clean-messy-data`. **Two-hub reciprocal confirmed:** `excel-ai-guide.html` already references this tutorial (lines 218, 334) AND new entry added to `excel-formulas-guide.html` AI and Automation section. URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-22

##### Completed: keyboard-shortcuts

- [x] **2A.keyboard-shortcuts** WebSearch on head-term variant. SERP dominated by Ablebits "30 most useful" (exact-phrase head term), Microsoft Support canonical reference, Simplilearn, GeeksforGeeks, Analytics Vidhya, plus several 50/80/100+ lists. 4 inbound internal links = modest rename risk. **Kept title**; moat = Mac equivalents alongside Windows in every shortcut table (none of the top SERP competitors list both side-by-side) + Troubleshooting H2 (language-switcher interception, Sticky Keys, used-range stale Ctrl+End, F4-not-in-edit-mode, Fn-lock laptop quirk) + two muscle-memory sequences + visible FAQ — no single competitor page combines all of this. — 2026-04-22
- [x] **2B.keyboard-shortcuts** Added missing `article:modified_time` meta (was absent) + updated BlogPosting `dateModified` from 2026-03-11 → 2026-04-22. Added 2 new `article:tag` entries (Excel Mac shortcuts, Excel keyboard tips). Sitemap lastmod bumped to 2026-04-22. — 2026-04-22
- [x] **2C.keyboard-shortcuts** **Critical bug fix:** line 193 had broken HTML `<code>Ctrl+;/code></code>` (malformed closing tag inside a code block) — fixed. Body expanded 1355w → 3599w (2.7×). Replaced 1-line intro with 2-paragraph intro (8-days-saved-per-year Microsoft stat + what's-in-this-tutorial framing + version + Mac compatibility + hub cross-link). Added Prerequisites H2 (version matrix + Fn-lock caveat + practise-on-real-data rule). Added Mac-equivalent column to all 6 shortcut tables (Navigation, Selection, Editing, Formatting, Formulas, Workbook & Data). Added beginner-pitfall paragraph below each table (stale Ctrl+End used-range, Shift+Space inside Tables, Ctrl+C→V anti-pattern, Alt-sequential-not-combination, F4-requires-edit-mode, Ctrl+T-rejects-merged-cells). Added new shortcuts: F4 repeat-last-action, Ctrl+Shift+# short-date, F9 formula-fragment-evaluate, Ctrl+Shift+L filter toggle, Ctrl+Alt+F5 refresh-all, Ctrl+N/O/S basics. Added "Two Muscle-Memory Sequences" H2 — Sequence 1 (Ctrl+Home → Ctrl+A → Ctrl+T → Ctrl+Shift+L → Ctrl+S, replaces ~20 mouse clicks) + Sequence 2 (Enter-in-Table OR Ctrl+Shift+End + Ctrl+D + F2-verify mouse-free fill-down). Rewrote "How to Memorise These Without Burning Out" with pick-5-per-week + never-look-at-cheat-sheet-first rule + Ctrl+Shift+letter macro binding. Read-time badge updated 6 min → 9 min. — 2026-04-22
- [x] **2D.keyboard-shortcuts** Added 5-item Common mistakes. Added dedicated Troubleshooting H2 with 5 ordered errors + exact fixes: (1) shortcut does nothing (Sticky Keys + Ctrl+Shift language-switcher interception), (2) F4 repeats last action instead of toggling $ (not in edit mode — press F2 first), (3) Ctrl+; inserts wrong date (Windows clock / regional setting), (4) Ctrl+T refused (merged cells / blank middle rows / already-in-Table — Alt+H,M,U fix), (5) laptop Fn modifier required (BIOS Action Keys Mode / Mac System Settings toggle). Added visible FAQ H2 with 5 questions mirroring FAQPage JSON-LD exactly. Completely rewrote FAQPage JSON-LD from 2 → 5 entries (added Mac equivalents, shortcut-does-nothing troubleshooting, and memorisation-strategy — all absent from prior schema). — 2026-04-22
- [x] **2E.keyboard-shortcuts** Sources upgraded with canonical Microsoft Support keyboard-shortcuts URL and ExcelJet shortcut reference. Replaced 3-item Related Posts with 7-entry Related tutorials — promoted `excel-formulas-guide` (hub) to top with annotation, added `excel-tables-best-practices` (what Ctrl+T unlocks), `audit-formulas-excel` (F9 workflow), `advanced-formulas`, `conditional-formatting-tips` (Ctrl+1 context), `clean-messy-data` (Ctrl+E Flash Fill), kept `data-validation`. Hub reciprocal confirmed: `excel-formulas-guide.html` already references keyboard-shortcuts in Productivity and Best Practices section (line 307). URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-22

##### Completed: copilot-automate-tasks

- [x] **2A.copilot-automate-tasks** WebSearch on compound 2026-specific query. SERP dominated by Microsoft Support + Nexacu + m365.fm + Flexmind + Reflective IT + Microsoft Tech Community (the Agent Mode launch post) + 365ninjacat. 4 inbound internal links = renaming is pure ranking risk. **Kept title.** Moat = Agent Mode (Q1 2026 release) and COPILOT() function (March 2026) coverage — both genuinely new in 2026 and missing from 80% of competitor pages still anchored on the old chat-pane-only workflow. — 2026-04-22
- [x] **2B.copilot-automate-tasks** Added missing `article:modified_time` meta (was absent) + updated BlogPosting `dateModified` from 2026-03-23 → 2026-04-22. Added 2 new `article:tag` entries (Excel Agent Mode, COPILOT function). Sitemap lastmod bumped to 2026-04-22. — 2026-04-22
- [x] **2C.copilot-automate-tasks** Body expanded 1523w → 3937w (2.6×). New: 2-paragraph intro (Toshiba 5.6-hours-saved-per-month stat + licence + hard cloud-storage prerequisite + hub cross-links). Prerequisites H2 (4 items: Copilot licence + OneDrive/SharePoint + Excel Table + Excel 365 version 2403+). All 4 existing prompt-list sections (Sorting/Filtering, Formatting, Adding Formulas, Data Summarisation) extended from 4 thin bullets to 5-6 bullets + Real-world scenario / beginner-pitfall paragraphs (duplicate-column ambiguity / CF-not-propagating / Total-Row-vs-SUM-below-Table / COPILOT-recalc-volatility). **New "Per-row AI with the COPILOT() function"** H2 with syntax + 4 practical examples (sentiment / category extraction / summary / entity pull) + quota warning + Paste-Special-Values freeze pattern. **New "Agent Mode — multi-step automation from a single prompt"** H2 with enable path + worked Friday-regional-sales-pack 7-step prompt with pause-approval point + save-and-re-run-next-week pattern. Rewrote "Building a Weekly Automation Workflow" as 9-step classic-mode worked example with concrete row counts (340 deals / 14 empty rows removed / 340 AI classifications). Rewrote thin Limitations → 5-bullet what-Copilot-can't-do list with named alternatives (VBA→Claude, external systems→Power Automate). Rewrote Copilot+Power Automate → 3-step end-to-end flow. Read-time badge 8 → 12 min. — 2026-04-22
- [x] **2D.copilot-automate-tasks** Added 5-item Common mistakes. Added dedicated Troubleshooting H2 with 5 ordered errors + exact fixes: (1) "Copilot can't be used on this file right now" (local/personal-OneDrive), (2) Copilot button greyed out (4-cause diagnostic: licence → cloud → Table → DLP), (3) Agent Mode missing from split-button (tenant admin Agents toggle + Excel 2403 requirement), (4) COPILOT() returning #BUSY! / #CALC! (rate limit / upstream error), (5) Agent plan pauses and never resumes (by-design no-auto-retry). Added visible FAQ H2 with 5 questions mirroring FAQPage JSON-LD exactly. Completely rewrote FAQPage JSON-LD from 2 → 5 entries (added Agent Mode, COPILOT() function, availability-troubleshooting — all three absent from prior schema). **Critical duplicate cleanup:** `<h2>Sources &amp; Further Reading</h2>` was duplicated on line 321 (two openings in a row). Fixed. — 2026-04-22
- [x] **2E.copilot-automate-tasks** Sources upgraded with canonical Microsoft Tech Community Agent Mode launch URL + Microsoft 365 Copilot Workflows URL. Replaced 4-item Related Posts with 7-entry Related tutorials — promoted `excel-formulas-guide` (hub) to top with annotation, added `power-query-guide` (refresh-on-open alternative) + `clean-messy-data` (pre-Copilot cleanup) as siblings, kept `getting-started-copilot-excel` / `copilot-data-analysis` / `claude-ai-excel-macros` / `excel-ai-prompts` with contextual annotations. Hub reciprocal confirmed: `excel-formulas-guide.html` already references copilot-automate-tasks in AI and Automation section (line 306). URL unchanged, no firebase redirect needed. Logged in [reports/conversions-log.md](../reports/conversions-log.md). — 2026-04-22

#### Group E — Flutter thin tutorials (from Phase 0.3 shortlist)

See same shortlist (Flutter rows tagged "expand").

#### Group F — RAG / AI-dev (filled after Phase 0.3 shortlist)

#### Group G — New product launches (fresh tutorials, not conversions)

- ~~claude-design~~ ✅ done 2026-04-21 (see micro-task block below)

##### Completed: claude-design

- [x] **2A.claude-design** WebSearch run on "How to use Claude Design" + "Claude Design Anthropic Labs tutorial beginner claude.ai/design". Claude Design launched 2026-04-17 (4 days before publish). SERP **is already non-thin** despite the recent launch — Anthropic's own help centre + anthropic.com launch post + apiyi.com + buildfastwithai + aifordevelopers Substack + YouTube + creatoreconomy + Fast Company all published inside the launch week. User overrode Strategic Rule 1 and locked the title to the exact phrase "How to Use Claude Design" on the grounds that they wanted the exact-match head term rather than a thin-SERP rename candidate. Accepted with the explicit caveat that the moat must come from body depth, not title uniqueness. — 2026-04-21
- [x] **2B.claude-design** Scaffolded from scratch (no original): full head meta (description / keywords / og / twitter / canonical / article:published_time + modified_time 2026-04-21 / en-GB / 5 article:tag entries) + BlogPosting + Organisation + BreadcrumbList + ImageObject + FAQPage (5 Qs) + WebPage speakable JSON-LD. Cover image path `/blog/images/claude-design-sagnik-bhattacharya-coding-liquids.jpg` — user will generate via Codex separately (placeholder 404 until then, user aware). Body skeleton: intro (2 paragraphs) + Prerequisites H2 + 9-step numbered H2 chain + Prompt patterns H2 + Claude Design vs Figma vs Canva table + Troubleshooting H2 + Limitations H2 + FAQ H2 + Sources H2 + Related Tutorials H2 + CTA. — 2026-04-21
- [x] **2C.claude-design** Filled all 9 steps with real instructions and image placeholders (3 `<!-- screenshot: -->` comments for user/Codex to attach later). Strong-vs-weak prompt comparison using user's own Coding Liquids brand specs (30k students / 175 countries / warm earth-tone palette / Plus Jakarta Sans + DM Serif Display) — turns the tutorial into a demo of the brand. Step 4 covers the three editing modes (chat for conceptual, inline comments for per-element feedback, direct edits + sliders for micro-adjustments) with the "propagate across project" pattern. Step 5 covers all 4 input types (images / DOCX/PPTX/XLSX / codebase / web capture). Step 6 covers design system extraction with the design-token-library caveat. Step 7 covers the 3 sharing modes + organisation-scoped limitation. Step 8 covers all 4 export formats (Canva / PDF / PPTX / standalone HTML) with per-format use case. Step 9 covers Claude Code handoff with a concrete `claude "..."` command example. Added 5 reusable prompt patterns H2 (investor one-pager / landing-page wireframe / board-deck slide / app-screen mockup / marketing variant). Added Claude Design vs Figma vs Canva comparison table (9 rows) with honest verdict (tools complement rather than replace). — 2026-04-21
- [x] **2D.claude-design** Added dedicated Troubleshooting H2 with 5 ordered errors + exact fixes: (1) "Claude Design is not yet available on your account" (Free plan / waitlist / wrong-email sign-in), (2) blank-canvas / stuck-on-Preparing-workspace (WebGL hardware-acceleration check via chrome://gpu + extension-blocking causes + incognito isolation), (3) Canva OAuth expiry (Settings → Integrations → Canva → Reconnect + allow-popups requirement), (4) design system import hang (500 MB zip limit + strip node_modules/dist + private-GitHub workaround), (5) org-scoped sharing prompts colleagues to sign in (working as intended — export to PDF or standalone HTML for external reviewers). Added Limitations H2 with 4 honest constraints (not pixel-precise / uneven rollout / no offline mode / no stock library). Added visible FAQ H2 with 5 questions mirroring FAQPage JSON-LD exactly (free? / vs Artifacts / design-background-required / handoff-to-Claude-Code meaning / replace Figma/Canva). — 2026-04-21
- [x] **2E.claude-design** Added 5-entry Sources list (Anthropic launch post + 3 Claude Help Centre articles + Claude resources tutorial). Related Tutorials section: claude-code-vscode promoted as top entry ("natural next step … handoff bundle") + claude-code-android-studio (mobile target) + chatgpt-vs-claude-vs-copilot-vs-gemini-excel (non-design Claude fit) + gemma-4-vscode (cost alternative). Per user instruction, skipped primary gemma-4-vscode hub link promotion — included only as cost alternative. Added reciprocal link in claude-code-vscode.html Related Tutorials (promoted to top entry with "use Claude Code as the handoff target" annotation). Cascade complete: sitemap.xml + feed.xml + llms-full.txt + blog.html grid + BLOG_NAMES.txt all updated with new entry. No firebase redirect needed (new URL, no prior canonical). — 2026-04-21

---

## Phase 3 — Comparison Pages (light pass, 1 file = 1 task)

Per file add: verdict H2 ("Which should you pick?"), FAQ H2 (3-5 Qs), links to 2 relevant tutorials, ensure hub link exists if topically adjacent.

- [x] **3.1** `chatgpt-vs-claude-vs-copilot-vs-gemini-excel.html` — Added "Which should you pick?" verdict H2. Synced FAQPage JSON-LD (5 Qs). Added hub links: excel-formulas-guide, gemma-4-data-analysis-excel, gemma-4-vscode. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.2** `excel-vs-google-sheets.html` — Already had "The Verdict" H2. Added visible FAQ H2 (4 Qs) + expanded FAQPage schema to 4 Qs. Added hub links: excel-formulas-guide, chatgpt-vs-claude comparison. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.3** `flutter-vs-react-native.html` — Added verdict H2 (Flutter for custom UI/Dart; RN for JS teams). Added hub: flutter-guide. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.4** `gemma-4-vs-chatgpt-vs-claude.html` — Added verdict H2 (Gemma for free/private; Claude for reasoning; ChatGPT for breadth). Hub link already present. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.5** `gemma-4-vs-gemini.html` — Added verdict H2 (Gemma=local-first; Gemini=cloud-first). Hub link already present. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.6** `gemma-4-vs-gpt-vs-llama-excel.html` — Added verdict H2 with link to gemma-4-data-analysis-excel. Added hubs: excel-formulas-guide, gemma-4-vscode. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.7** `gemma-4-vs-paid-ai-models.html` — Added verdict H2 (Gemma for routine+privacy; paid for hardest problems). Hub link already present. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.8** `seedance-vs-veo-3.html` — Added verdict H2 (Seedance=prompt control; Veo 3=photorealism). Added hub: seedance-guide. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.9** `seedance-vs-kling.html` — Added verdict H2 (Seedance=camera fidelity; Kling=body motion). Added hub: seedance-guide. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.10** `seedance-vs-sora-2.html` — Added verdict H2 (Seedance=prompt adherence+free; Sora 2=cinematic quality). Added hub: seedance-guide. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.11** `vlookup-vs-xlookup.html` — Already had verdict. Added hub: excel-formulas-guide. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.12** `groupby-vs-pivottable-excel.html` — Added verdict H2 (GROUPBY for formula-driven; PivotTable for interactive). Added hub: excel-formulas-guide. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.13** `analyst-vs-agent-mode-vs-copilot-chat.html` — Added verdict H2 (Analyst=exploration; Agent=automation; Chat=quick Qs). Added hub: excel-formulas-guide. Renamed Related → Related tutorials. — 2026-04-17
- [x] **3.14** `flutter-web-skwasm-vs-canvaskit.html` — Added verdict H2 (skwasm=default; CanvasKit=complex painting). Added hub: flutter-guide. Renamed Related → Related tutorials. — 2026-04-17

---

## Phase 4 — Hub Strengthening

- [x] **4.1** Read hub fully; mapped 9 outbound /blog/ links (4 Group A + 4 comparisons + 1 Group B). — 2026-04-17
- [x] **4.2** Hub already linked all 4 Group A tutorials in Related section. Verified reciprocal links. — 2026-04-17
- [x] **4.3** Added 8 missing Group B tutorial links to hub Related section (copilot-agent-mode-vscode, deepseek-vscode, gemini-cli-vscode, gemini-cli-android-studio-flutter, opencode-vscode, windsurf-flutter-development, cursor-flutter-development, claude-code-android-studio). Hub now has 17 outbound links. — 2026-04-17
- [x] **4.4** All 13 tutorials (4 Group A + 9 Group B) link back to hub. All 13 now have reciprocal hub→tutorial links. — 2026-04-17

---

## Phase 5 — Sitewide Cleanup

- [x] **5.1** Updated sitemap.xml — 15 modified pages got lastmod=2026-04-17. All 139 URLs present, 0 stale/deleted. — 2026-04-17
- [x] **5.2** feed.xml already in sync (139 entries = 139 files). No changes needed. — 2026-04-17
- [x] **5.3** llms-full.txt already in sync (139 refs = 139 files). llms.txt has 4 refs by design (summary file). No changes needed. — 2026-04-17
- [x] **5.4** blog.html grid already in sync (139 links = 139 files). No changes needed. — 2026-04-17
- [x] **5.5** Regenerated BLOG_NAMES.txt: 97 → 139 titles. — 2026-04-17
- [x] **5.6** Ran audit_blog_cluster.py: **0 blockers**, 1 high (false positive: missing article:modified_time — user rule says sitemap only), 3 mediums (low internal link count on 3 pages — cosmetic). — 2026-04-17

---

## Phase 6 — Final Verification Before AdSense Re-review

- [x] **6.1** Crawl-checked 1620 internal /blog/ links across all 139 pages + blog.html grid. **0 broken links.** — 2026-04-17
- [ ] **6.2** Mobile render spot-check: needs live server or post-deploy check. Cannot test local files in browser sandbox.
- [x] **6.3** `ads.txt` intact: `google.com, pub-1443974359047569, DIRECT, f08c47fec0942fa0` (58 bytes). — 2026-04-17
- [x] **6.4** User deployed via `firebase deploy` — 309 files, release complete. — 2026-04-17
- [x] **6.5** User clicked "Request review" in AdSense (no separate message needed). Review pending. — 2026-04-17
- [x] **6.6** Added `dateModified` to BlogPosting JSON-LD on all 139 pages (43 added, 92 already present). 15 pages set to today, rest set to datePublished baseline. — 2026-04-17

---

## Done Archive

> Completed tasks move here. Format: `- [x] <task-id> <short desc> — <date>`.
