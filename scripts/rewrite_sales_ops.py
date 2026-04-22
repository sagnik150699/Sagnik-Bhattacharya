"""Replace the body content of excel-ai-for-sales-ops.html with substantive tutorial content."""
import re, pathlib

fp = pathlib.Path(r"c:\Workspace\Sagnik Bhattacharya\public\blog\excel-ai-for-sales-ops.html")
html = fp.read_text(encoding="utf-8")

OLD_BODY_START = '<div class="blog-post-content">'
OLD_BODY_END = '<div class="blog-cta-box">'

start_i = html.index(OLD_BODY_START)
end_i = html.index(OLD_BODY_END)

new_body = r'''<div class="blog-post-content">
<p>Every Sales Ops team runs on spreadsheets, even when a CRM exists. The CRM holds the record; Excel holds the analysis, the cleanup, and the quarter-end pack that leadership actually reads. This tutorial shows how to combine Excel formulas with AI prompts to speed up the three tasks that consume most of a Sales Ops analyst's week: pipeline cleanup, weighted forecasting, and territory reporting.</p>
<p>The approach works with any AI assistant that accepts pasted tabular data — Copilot in Excel, ChatGPT, Claude, or <a href="/blog/gemma-4-vscode">Gemma 4 running locally</a>. The formulas work on Excel 365, 2021, and 2019. For the broader Excel learning path see the <a href="/blog/excel-formulas-guide">Excel Formulas Guide</a> hub.</p>
<p>If you need a deal-level operational tracker rather than an analytical workflow, see <a href="/blog/sales-pipeline-tracker-excel">the sales pipeline tracker</a> instead.</p>
<div class="blog-inline-course"><div class="blog-inline-course__badge">Coming Soon</div><div class="blog-inline-course__body"><h3 class="blog-inline-course__title">Complete Excel Guide with AI Integration</h3><p class="blog-inline-course__sub">Master formulas, pivot tables, data analysis, and charts — with AI integration.</p><a href="/courses#excel" class="btn-primary blog-inline-course__btn">Learn more <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a></div></div>

<h2>Prerequisites</h2>
<ul>
<li>A CRM export in CSV or XLSX with at minimum: Deal Name, Stage, Owner, Value, Close Date, Last Activity Date.</li>
<li>Excel 365 / 2021 / 2019 (SUMIFS, COUNTIFS, and conditional formatting are universal; Forecast Sheet requires 365/2021).</li>
<li>Access to an AI assistant — Copilot in Excel, ChatGPT, Claude, or a local model via <a href="/blog/gemma-4-vscode">Gemma 4 in VS Code</a>.</li>
</ul>

<h2>Step 1 — Import and clean the CRM export</h2>
<p>Download the pipeline extract from your CRM. Open it in Excel and immediately convert to a Table (Ctrl + T). Name it <code>tblPipeline</code>. This matters — structured references make every formula self-documenting and auto-extending.</p>
<h3>Remove duplicates</h3>
<p>Data → Remove Duplicates → select the Deal ID column. A 4,000-row Salesforce export typically drops 40–120 rows here — merge artefacts, re-imported records, and test deals that were never deleted.</p>
<h3>Standardise stage names</h3>
<p>Free-text stage fields are the single biggest source of forecast error. Add a helper column:</p>
<pre><code>=TRIM(PROPER([@Stage]))</code></pre>
<p>Then use Data Validation (Data → Validation → List) sourced from a clean reference range to lock future entries to your canonical stages: Prospecting, Discovery, Proposal, Negotiation, Closed Won, Closed Lost.</p>
<h3>Flag stale deals</h3>
<pre><code>=TODAY()-[@[Last Activity Date]]</code></pre>
<p>Any deal over 30 days without activity is probably stuck. Add conditional formatting (Home → Conditional Formatting → Greater Than → 30 → red fill) to surface them instantly.</p>
<p><strong>AI assist.</strong> Paste the 20 worst rows (highest staleness, messiest stage names) into your AI assistant with this prompt: <em>"Standardise these deal records. Map each Stage value to one of: Prospecting, Discovery, Proposal, Negotiation, Closed Won, Closed Lost. Flag any row where the Close Date is in the past but Stage is not Closed Won or Closed Lost."</em> Review the output before pasting back — AI occasionally merges two deals that share a company name.</p>

<a href="https://www.instagram.com/sagnikteaches" target="_blank" rel="noopener noreferrer" class="blog-social-nudge blog-social-nudge--insta"><span class="blog-social-nudge__icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></span><span class="blog-social-nudge__text">Follow me on Instagram</span><span class="blog-social-nudge__handle">@sagnikteaches</span></a>

<h2>Step 2 — Build a weighted pipeline forecast</h2>
<p>Raw pipeline value is meaningless without win-rate weighting. Add two columns to <code>tblPipeline</code>:</p>
<h3>Win probability by stage</h3>
<p>Create a reference table (<code>tblStageProb</code>) mapping each stage to its historical win rate:</p>
<table>
<thead><tr><th>Stage</th><th>Win Probability</th></tr></thead>
<tbody>
<tr><td>Prospecting</td><td>10%</td></tr>
<tr><td>Discovery</td><td>25%</td></tr>
<tr><td>Proposal</td><td>50%</td></tr>
<tr><td>Negotiation</td><td>75%</td></tr>
<tr><td>Closed Won</td><td>100%</td></tr>
<tr><td>Closed Lost</td><td>0%</td></tr>
</tbody>
</table>
<p>Look it up in the pipeline:</p>
<pre><code>=XLOOKUP([@Stage], tblStageProb[Stage], tblStageProb[Win Probability], 0)</code></pre>
<p>For Excel 2019: <code>=INDEX(tblStageProb[Win Probability], MATCH([@Stage], tblStageProb[Stage], 0))</code></p>
<h3>Weighted value</h3>
<pre><code>=[@Value] * [@[Win Probability]]</code></pre>
<h3>Coverage ratio</h3>
<p>In a summary cell:</p>
<pre><code>=SUM(tblPipeline[Weighted Value]) / B1</code></pre>
<p>where B1 holds the team quota. A healthy ratio is 3× to 4× depending on your segment. Below 2.5× and the quarter is at risk; above 5× and the pipeline is probably bloated with zombie deals.</p>
<p><strong>AI assist.</strong> Paste the stage-level summary (stage name, deal count, total value, weighted value) and the coverage ratio into your AI assistant: <em>"Write a 3-paragraph forecast commentary for leadership. Note any stage where deal count dropped vs last quarter. Flag if coverage is below 3×. Use cautious language — this is a draft for analyst review."</em></p>

<a href="https://www.linkedin.com/in/sagnik-bhattacharya-916b9463/" target="_blank" rel="noopener noreferrer" class="blog-social-nudge blog-social-nudge--linkedin"><span class="blog-social-nudge__icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></span><span class="blog-social-nudge__text">Connect on LinkedIn</span><span class="blog-social-nudge__handle">Sagnik Bhattacharya</span></a>

<h2>Step 3 — Territory reporting</h2>
<p>Quarter-end territory packs typically need three views: territory totals, stage movement, and rep-level pipeline health. All three can be built from the same <code>tblPipeline</code> table.</p>
<h3>Territory totals</h3>
<pre><code>=SUMIFS(tblPipeline[Value], tblPipeline[Territory], "EMEA")
=SUMIFS(tblPipeline[Weighted Value], tblPipeline[Territory], "EMEA")
=COUNTIFS(tblPipeline[Territory], "EMEA", tblPipeline[Stage], "<>Closed Won", tblPipeline[Stage], "<>Closed Lost")</code></pre>
<h3>Stage movement (quarter-over-quarter)</h3>
<p>If you keep last quarter's export as <code>tblPipelineQ3</code>, compare deal counts per stage:</p>
<pre><code>=COUNTIFS(tblPipeline[Stage], "Negotiation") - COUNTIFS(tblPipelineQ3[Stage], "Negotiation")</code></pre>
<p>Positive = pipeline progressing. Negative = deals stalling or being disqualified faster than new ones enter.</p>
<h3>Rep-level pipeline health</h3>
<pre><code>=SUMIFS(tblPipeline[Weighted Value], tblPipeline[Owner], "Jane Smith") / XLOOKUP("Jane Smith", tblQuotas[Rep], tblQuotas[Quota])</code></pre>
<p>This gives a per-rep coverage ratio. Flag anyone below 2× in the territory pack.</p>
<p><strong>AI assist.</strong> Paste the territory summary table and prompt: <em>"Draft a territory narrative for the EMEA section of our QBR deck. Highlight the top 3 deals by weighted value, flag any territory where coverage dropped below 2.5×, and note the stage with the largest quarter-over-quarter decline. Keep it to 150 words."</em></p>

<a href="https://www.youtube.com/@codingliquids" target="_blank" rel="noopener noreferrer" class="blog-social-nudge blog-social-nudge--youtube"><span class="blog-social-nudge__icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19.13C5.12 19.56 12 19.56 12 19.56s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/></svg></span><span class="blog-social-nudge__text">Subscribe on YouTube</span><span class="blog-social-nudge__handle">@codingliquids</span></a>

<h2>Worked example — quarter-end territory pack</h2>
<p>A 12-person SaaS sales team exports 340 deals from HubSpot. The Sales Ops analyst runs the three-step workflow above in 45 minutes:</p>
<ol>
<li><strong>Cleanup:</strong> Remove Duplicates drops 18 rows. Stage standardisation catches 9 "Qualified" entries that should be "Discovery" and 4 blank stages. Staleness filter surfaces 23 deals untouched for 30+ days — analyst emails reps for status.</li>
<li><strong>Forecast:</strong> Weighted pipeline = £2.1M against a £680K quota → 3.1× coverage (healthy). AI drafts commentary noting that Negotiation count dropped from 14 to 9 vs Q3 — analyst adds context (two enterprise deals slipped to Q2).</li>
<li><strong>Territory pack:</strong> Three territories (EMEA, APAC, Americas). APAC coverage = 1.8× (below threshold). AI flags it; analyst adds a recruitment note. Pack is reviewed and sent to VP Sales before 3 PM.</li>
</ol>
<p>Before this workflow, the same pack took two days of manual compilation. The AI did not make any decisions — it drafted narratives and flagged numbers. The analyst owned every word that left the spreadsheet.</p>

<h2>Troubleshooting</h2>
<ol>
<li><strong>SUMIFS returns 0 for a territory that clearly has deals.</strong> Territory name has a trailing space in the CRM export. Fix: wrap the criteria in TRIM — <code>=SUMIFS(tblPipeline[Value], TRIM(tblPipeline[Territory]), "EMEA")</code> — or better, clean the source column with Find &amp; Replace (find " " at end, replace with nothing).</li>
<li><strong>Weighted Value column shows £0 for every row.</strong> The Win Probability lookup is returning 0 because Stage names don't match the reference table exactly. Check for capitalisation differences ("negotiation" vs "Negotiation") or leading/trailing spaces. Use <code>=EXACT([@Stage], XLOOKUP([@Stage], tblStageProb[Stage], tblStageProb[Stage]))</code> to diagnose.</li>
<li><strong>Coverage ratio is absurdly high (10×+).</strong> Closed Won deals are still in the pipeline table, inflating the total. Filter out Closed Won and Closed Lost before calculating: <code>=SUMIFS(tblPipeline[Weighted Value], tblPipeline[Stage], "&lt;&gt;Closed Won", tblPipeline[Stage], "&lt;&gt;Closed Lost") / quota</code>.</li>
<li><strong>AI-drafted commentary contains made-up deal names.</strong> The AI hallucinated details not in the pasted data. Always paste the raw table, never summarise it verbally before prompting. Include the instruction "Only reference deals that appear in the data below" in your prompt.</li>
<li><strong>Quarter-over-quarter comparison shows wrong deltas.</strong> The Q3 export uses different stage names (e.g. "Qualified" instead of "Discovery"). Standardise both tables with the same stage-mapping helper column before comparing.</li>
</ol>

<h2>Common mistakes</h2>
<ul>
<li>Running AI on a pipeline that hasn't been deduplicated — the AI counts duplicates as real deals.</li>
<li>Treating AI forecast commentary as final guidance without checking deal-level accuracy.</li>
<li>Using raw (unweighted) pipeline value in the coverage ratio — overstates health by 2–4×.</li>
<li>Letting stage definitions drift between CRM and Excel — forecast becomes unreliable within one quarter.</li>
<li>Sending AI-drafted territory narratives to leadership without analyst review — tone and accuracy both need a human pass.</li>
</ul>

<h2>Frequently asked questions</h2>
<h3>Which Sales Ops tasks benefit most from AI in Excel?</h3>
<p>Pipeline cleanup (deduplicating, standardising stages, flagging stale deals), weighted forecast first-drafts, territory summary narratives, and anomaly detection across CRM exports. All four produce a reviewable draft rather than a final decision, which keeps the human in control.</p>
<h3>How do I build a weighted pipeline forecast in Excel?</h3>
<p>Create a Pipeline table with columns for Deal, Stage, Value, and Win Probability. Add a Weighted Value column: <code>=[@Value]*[@[Win Probability]]</code>. Summarise with <code>=SUMIFS(tblPipeline[Weighted Value], tblPipeline[Stage], stage_name)</code> per stage. AI can then generate commentary on the coverage ratio and flag deals whose Days in Stage exceeds the historical median.</p>
<h3>What is pipeline coverage ratio and why does it matter?</h3>
<p>Coverage ratio = Total Weighted Pipeline ÷ Quota. A ratio of 3× means you need three pounds of pipeline for every pound of quota, based on your historical win rate. If coverage drops below your target, the forecast is at risk regardless of what individual reps commit.</p>
<h3>Can AI replace a Sales Ops analyst for quarter-end reporting?</h3>
<p>No. AI can draft territory summaries, flag anomalies, and generate first-pass commentary, but the analyst must verify deal-level accuracy, apply business context (e.g. contract timing, procurement cycles), and own the narrative before it reaches leadership. Treat AI output as a draft, not a deliverable.</p>
<h3>How do I clean a messy CRM pipeline export in Excel?</h3>
<p>Format as an Excel Table (Ctrl + T), then: 1) Remove Duplicates on the deal-ID column, 2) use Data Validation dropdowns for Stage to prevent free-text drift, 3) add a helper column <code>=TODAY()-[@[Last Activity Date]]</code> to surface stale deals, 4) use TRIM and CLEAN to strip whitespace from text fields.</p>

<h2>Related tutorials</h2>
<ul>
<li><a href="/blog/excel-formulas-guide">Excel Formulas Guide</a> — the Excel cluster hub; start here for the full tutorial index.</li>
<li><a href="/blog/sales-pipeline-tracker-excel">How to Build a Sales Pipeline Tracker in Excel for Small Teams</a> — the operational deal tracker that feeds this analytical workflow.</li>
<li><a href="/blog/ai-forecasting-model-excel">Build a Forecasting Model in Excel With AI Assistance Step by Step</a> — deeper forecasting beyond the weighted pipeline approach.</li>
<li><a href="/blog/dynamic-dashboards">How to Build an Interactive Dashboard in Excel (No VBA)</a> — turn territory summaries into interactive sliceable views.</li>
<li><a href="/blog/review-ai-generated-excel-formulas">How to Review AI-Generated Excel Formulas Before You Trust Them</a> — the review discipline that keeps AI-assisted workflows safe.</li>
<li><a href="/blog/clean-messy-data">How to Clean Messy Data in Excel Before It Breaks Everything Downstream</a> — the data-prep foundation for every pipeline cleanup.</li>
</ul>
'''

html_new = html[:start_i] + new_body + html[end_i:]
fp.write_text(html_new, encoding="utf-8")
print("Done — body replaced.")
