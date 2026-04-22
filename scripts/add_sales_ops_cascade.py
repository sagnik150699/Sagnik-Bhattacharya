"""Add excel-ai-for-sales-ops to feed.xml and blog.html (both are missing it)."""
import pathlib

ROOT = pathlib.Path(r"c:\Workspace\Sagnik Bhattacharya\public")

# --- feed.xml: insert after conditional-formatting-tips item (published 2026-03-06) ---
feed = ROOT / "feed.xml"
txt = feed.read_text(encoding="utf-8")

feed_entry = """    <item>
      <title>Excel + AI for Sales Ops: Pipeline Cleanup, Forecasts, and Territory Reporting</title>
      <link>https://sagnikbhattacharya.com/blog/excel-ai-for-sales-ops</link>
      <guid isPermaLink="true">https://sagnikbhattacharya.com/blog/excel-ai-for-sales-ops</guid>
      <description>Learn practical Excel and AI workflows for Sales Ops: pipeline cleanup with SUMIFS and Data Validation, weighted forecasting with coverage ratios, and quarter-end territory reporting with AI-drafted narratives.</description>
      <category>AI + Excel</category>
      <author>sagnik@codingliquids.com (Sagnik Bhattacharya)</author>
      <pubDate>Wed, 05 Mar 2026 00:00:00 +0530</pubDate>
    </item>"""

# Insert before the mastering-pivot-tables item (published date closest)
anchor = "    <item>\n      <title>How to Create a Pivot Table in Excel Step by Step</title>"
anchor_r = anchor.replace("\n", "\r\n")
if anchor_r in txt:
    txt = txt.replace(anchor_r, feed_entry + "\r\n" + anchor_r)
elif anchor in txt:
    txt = txt.replace(anchor, feed_entry + "\n" + anchor)
else:
    # fallback: insert before </channel>
    txt = txt.replace("  </channel>", feed_entry + "\n  </channel>")

feed.write_text(txt, encoding="utf-8")
print("feed.xml: entry added")

# --- blog.html: insert card ---
blog = ROOT / "blog.html"
btxt = blog.read_text(encoding="utf-8")

# Find the conditional-formatting-tips card and insert after it
card = """        <a href="/blog/excel-ai-for-sales-ops" class="blog-card">
          <div class="blog-card-image">
            <img src="/blog/images/excel-ai-for-sales-ops-sagnik-bhattacharya-coding-liquids.jpg" alt="Excel + AI for Sales Ops: Pipeline Cleanup, Forecasts, and Territory Reporting" loading="lazy" width="600" height="315">
          </div>
          <div class="blog-card-content">
            <span class="blog-card-tag">AI + Excel</span>
            <h3>Excel + AI for Sales Ops: Pipeline Cleanup, Forecasts, and Territory Reporting</h3>
            <p>Learn practical Excel and AI workflows for Sales Ops, focused on pipeline cleanup, forecasting support, and territory reporting.</p>
            <span class="blog-card-date">5 Mar 2026</span>
          </div>
        </a>"""

# Insert before the mastering-pivot-tables card
pt_anchor = '<a href="/blog/mastering-pivot-tables"'
if pt_anchor in btxt:
    idx = btxt.index(pt_anchor)
    # Find the start of the preceding whitespace
    line_start = btxt.rfind("\n", 0, idx) + 1
    btxt = btxt[:line_start] + card + "\r\n" + btxt[line_start:]
    blog.write_text(btxt, encoding="utf-8")
    print("blog.html: card added")
else:
    print("blog.html: anchor not found, skipping")

print("Done")
