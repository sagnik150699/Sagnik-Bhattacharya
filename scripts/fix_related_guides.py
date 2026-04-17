#!/usr/bin/env python3
"""Replace 'Related guides on this site' with hub-linked 'Related tutorials on this site'."""
import sys

filepath = r"c:\Workspace\Sagnik Bhattacharya\public\blog\chatgpt-vs-claude-vs-copilot-vs-gemini-excel.html"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

old = (
    '<h2>Related guides on this site</h2>'
    '<p>If you want to keep going without opening dead ends, '
    'these are the most useful next reads from this site.</p>'
    '<ul>'
    '<li><a href="/blog/copilot-function-excel">COPILOT Function in Excel: Syntax, Use Cases, Limits, and Risks</a></li>'
    '<li><a href="/blog/agent-mode-in-excel">Agent Mode in Excel: What It Does, What It Can\u2019t, and Who Should Use It</a></li>'
    '<li><a href="/blog/create-lookups-with-copilot-excel">Create Lookups With Copilot in Excel: When It Writes XLOOKUP Well and When It Doesn\u2019t</a></li>'
    '<li><a href="/blog/chatgpt-excel-guide">How to Use ChatGPT to Write Excel Formulas (With Real Examples)</a></li>'
    '</ul>'
)

new = (
    '<h2>Related tutorials on this site</h2>'
    '<p>These are the most useful next reads from this site.</p>'
    '<ul>'
    '<li><a href="/blog/excel-formulas-guide">Excel Formulas: The Complete 2026 Reference</a> \u2014 the hub page indexing every Excel tutorial on this site.</li>'
    '<li><a href="/blog/gemma-4-data-analysis-excel">Gemma 4 for Data Analysis: Can It Replace ChatGPT for Spreadsheet Work?</a> \u2014 a free, local alternative tested on real Excel tasks.</li>'
    '<li><a href="/blog/gemma-4-vscode">Gemma 4 in VS Code: The Complete AI Coding Tools Hub</a> \u2014 if you write VBA or Python scripts for Excel, this covers the IDE-side AI tools.</li>'
    '<li><a href="/blog/copilot-function-excel">COPILOT Function in Excel: Syntax, Use Cases, Limits, and Risks</a></li>'
    '<li><a href="/blog/agent-mode-in-excel">Agent Mode in Excel: What It Does, What It Can\u2019t, and Who Should Use It</a></li>'
    '<li><a href="/blog/chatgpt-excel-guide">How to Use ChatGPT to Write Excel Formulas (With Real Examples)</a></li>'
    '</ul>'
)

if old in content:
    content = content.replace(old, new)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("OK - replaced Related guides with Related tutorials + hub links")
else:
    print("NOT FOUND - target string not in file")
    sys.exit(1)
