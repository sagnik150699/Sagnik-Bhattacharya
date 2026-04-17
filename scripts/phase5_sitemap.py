#!/usr/bin/env python3
"""Phase 5 — Sitewide Cleanup: Update sitemap lastmod for pages modified today."""
import re

today = "2026-04-17"
sitemap_file = r"c:\Workspace\Sagnik Bhattacharya\public\sitemap.xml"

# Pages we modified today in Phase 3 and Phase 4
modified_slugs = [
    "chatgpt-vs-claude-vs-copilot-vs-gemini-excel",
    "excel-vs-google-sheets",
    "flutter-vs-react-native",
    "gemma-4-vs-chatgpt-vs-claude",
    "gemma-4-vs-gemini",
    "gemma-4-vs-gpt-vs-llama-excel",
    "gemma-4-vs-paid-ai-models",
    "seedance-vs-veo-3",
    "seedance-vs-kling",
    "seedance-vs-sora-2",
    "vlookup-vs-xlookup",
    "groupby-vs-pivottable-excel",
    "analyst-vs-agent-mode-vs-copilot-chat",
    "flutter-web-skwasm-vs-canvaskit",
    "gemma-4-vscode",  # Phase 4 hub update
]

with open(sitemap_file, "r", encoding="utf-8") as f:
    content = f.read()

changes = 0
for slug in modified_slugs:
    url = f"https://sagnikbhattacharya.com/blog/{slug}"
    # Find <url> block containing this URL and update its <lastmod>
    pattern = re.compile(
        rf'(<url>\s*<loc>{re.escape(url)}</loc>\s*<lastmod>)(\d{{4}}-\d{{2}}-\d{{2}})(</lastmod>)',
        re.DOTALL
    )
    match = pattern.search(content)
    if match:
        old_date = match.group(2)
        if old_date != today:
            content = content[:match.start(2)] + today + content[match.end(2):]
            changes += 1
            print(f"  {slug}: {old_date} -> {today}")
        else:
            print(f"  {slug}: already {today}")
    else:
        print(f"  {slug}: NOT FOUND in sitemap")

if changes > 0:
    with open(sitemap_file, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"\nUpdated {changes} lastmod dates in sitemap.xml")
else:
    print("\nNo changes needed.")
