#!/usr/bin/env python3
"""Phase 3 light pass for excel-vs-google-sheets.html.
Adds: visible FAQ H2, hub links, expanded FAQPage schema.
NOTE: article:modified_time / dateModified NOT added per user rule — those go in sitemap only."""

filepath = r"c:\Workspace\Sagnik Bhattacharya\public\blog\excel-vs-google-sheets.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

changes = 0

# 1. Add visible FAQ H2 after The Verdict section, before Sources
old1 = '      <h2>Sources &amp; Further Reading</h2>'
faq_html = """      <h2>Frequently asked questions</h2>
<p><strong>Is Excel or Google Sheets better in 2026?</strong> Excel is better for power users who need advanced formulas like LAMBDA, GROUPBY, and PIVOTBY, Power Query, Power Pivot, VBA macros, large datasets with over one million rows, and desktop performance. Google Sheets is better for real-time collaboration, simplicity, free access, and web-native workflows.</p>
<p><strong>Should I use Excel or Google Sheets for work?</strong> If your work involves complex data analysis, financial models, large datasets, or automation with macros, use Excel. If your work is primarily collaborative \u2014 shared trackers, simple reports, team templates \u2014 and your organisation uses Google Workspace, use Google Sheets. Many professionals use both.</p>
<p><strong>Can Google Sheets handle large datasets?</strong> Google Sheets struggles above 100,000 rows. For datasets beyond that, Excel with Power Pivot or Power Query is the practical choice. Google offers Connected Sheets with BigQuery for enterprise-scale data, but it requires a Workspace subscription.</p>
<p><strong>Which has better AI features \u2014 Excel Copilot or Google Sheets with Gemini?</strong> Excel Copilot is currently more powerful for deep data analysis, chart creation, and formula generation, but requires a paid add-on. Gemini in Google Sheets is included with Workspace and handles simpler tasks well. For a deeper comparison of AI tools for Excel, see <a href="/blog/chatgpt-vs-claude-vs-copilot-vs-gemini-excel">ChatGPT vs Claude vs Copilot vs Gemini for Excel</a>.</p>
      <h2>Sources &amp; Further Reading</h2>"""
if old1 in content:
    content = content.replace(old1, faq_html)
    changes += 1
    print("1. Added visible FAQ H2 (4 questions)")

# 2. Expand FAQPage schema from 2 to 4 questions
old2 = """  ]
}
  </script>
    <style>"""
new2 = """    ,
    {
      "@type": "Question",
      "name": "Can Google Sheets handle large datasets?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Google Sheets struggles above 100,000 rows. For datasets beyond that, Excel with Power Pivot or Power Query is the practical choice. Google offers Connected Sheets with BigQuery for enterprise-scale data, but it requires a Workspace subscription."
      }
    },
    {
      "@type": "Question",
      "name": "Which has better AI features, Excel Copilot or Google Sheets with Gemini?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Excel Copilot is currently more powerful for deep data analysis, chart creation, and formula generation, but requires a paid add-on. Gemini in Google Sheets is included with Workspace and handles simpler tasks well."
      }
    }
  ]
}
  </script>
    <style>"""
if old2 in content:
    content = content.replace(old2, new2)
    changes += 1
    print("2. Updated FAQPage schema to 4 questions")

# 3. Replace Related Posts with hub-linked Related tutorials
old3 = """<h2>Related Posts</h2>
<ul>
  <li><a href="/blog/keyboard-shortcuts">30 Excel Keyboard Shortcuts That Save Hours</a></li>
  <li><a href="/blog/conditional-formatting-tips">Excel Conditional Formatting Tips and Tricks</a></li>
  <li><a href="/blog/copilot-data-analysis">Excel Copilot for Data Analysis \u2014 A Practical Guide</a></li>
</ul>"""
new3 = """<h2>Related tutorials on this site</h2>
<ul>
  <li><a href="/blog/excel-formulas-guide">Excel Formulas: The Complete 2026 Reference</a> \u2014 the hub page indexing every Excel tutorial on this site.</li>
  <li><a href="/blog/chatgpt-vs-claude-vs-copilot-vs-gemini-excel">ChatGPT vs Claude vs Copilot vs Gemini for Excel in 2026</a> \u2014 which AI assistant fits which spreadsheet job.</li>
  <li><a href="/blog/keyboard-shortcuts">30 Excel Keyboard Shortcuts That Save Hours</a></li>
  <li><a href="/blog/conditional-formatting-tips">Excel Conditional Formatting Tips and Tricks</a></li>
  <li><a href="/blog/copilot-data-analysis">Excel Copilot for Data Analysis \u2014 A Practical Guide</a></li>
</ul>"""
if old3 in content:
    content = content.replace(old3, new3)
    changes += 1
    print("3. Added hub links to Related tutorials")

if changes > 0:
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\nDone - {changes} changes applied.")
else:
    print("No changes applied - check target strings.")
