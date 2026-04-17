#!/usr/bin/env python3
"""Add dateModified to BlogPosting JSON-LD across all blog pages.
- Pages modified today (Phase 3/4): dateModified = 2026-04-17
- All other pages: dateModified = datePublished (baseline)
- Skips pages that already have dateModified.
"""
import re, os, json

blog_dir = r"c:\Workspace\Sagnik Bhattacharya\public\blog"
today = "2026-04-17"

# Pages we modified today
modified_today = {
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
    "gemma-4-vscode",
}

added = 0
skipped = 0
errors = []

for fname in sorted(os.listdir(blog_dir)):
    if not fname.endswith(".html") or fname == "index.html":
        continue
    
    fp = os.path.join(blog_dir, fname)
    slug = fname.replace(".html", "")
    
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Check if BlogPosting schema exists
    if '"BlogPosting"' not in content:
        continue
    
    # Check if dateModified already exists in BlogPosting context
    # We need to be careful: some pages have dateModified already
    # Look for dateModified near datePublished in BlogPosting schema
    
    # Strategy: find "datePublished" and check if "dateModified" follows nearby
    # Handle both compact (single-line) and pretty-printed (multi-line) JSON-LD
    
    # Pattern 1: Compact single-line JSON-LD
    compact_match = re.search(
        r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})"(\s*,\s*"dateModified")',
        content
    )
    if compact_match:
        skipped += 1
        continue
    
    # Pattern 2: Pretty-printed JSON-LD
    pretty_match = re.search(
        r'"datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})".*?"dateModified"',
        content, re.DOTALL
    )
    # But check this is within the same script block (not crossing into another schema)
    if pretty_match:
        # Verify it's within same BlogPosting block (no </script> between)
        segment = content[pretty_match.start():pretty_match.end()]
        if "</script>" not in segment:
            skipped += 1
            continue
    
    # Need to add dateModified. Find datePublished and insert after it.
    date_pub_match = re.search(
        r'("datePublished"\s*:\s*"(\d{4}-\d{2}-\d{2})")',
        content
    )
    if not date_pub_match:
        errors.append(f"{fname}: no datePublished found")
        continue
    
    pub_date = date_pub_match.group(2)
    mod_date = today if slug in modified_today else pub_date
    
    # Detect format: compact vs pretty
    # Check what comes after datePublished
    after_pos = date_pub_match.end()
    after_text = content[after_pos:after_pos+20]
    
    if after_text.strip().startswith(","):
        # Compact format: "datePublished":"2026-03-17","inLanguage"...
        # Insert after the comma
        comma_pos = content.index(",", after_pos)
        insert = f'"dateModified":"{mod_date}",'
        content = content[:comma_pos+1] + insert + content[comma_pos+1:]
    else:
        # Pretty format: "datePublished":  "2026-03-17",\n    "inLanguage"...
        # Find the end of the line and insert a new line after
        line_end = content.index("\n", after_pos)
        # Get indentation from the datePublished line
        line_start = content.rfind("\n", 0, date_pub_match.start()) + 1
        indent = ""
        for ch in content[line_start:]:
            if ch in " \t":
                indent += ch
            else:
                break
        # Check if there's a trailing comma
        segment = content[after_pos:line_end].strip()
        if segment.endswith(","):
            insert_line = f'\n{indent}"dateModified":  "{mod_date}",'
        else:
            # Add comma to current line first
            content = content[:line_end] + "," + content[line_end:]
            line_end += 1
            insert_line = f'\n{indent}"dateModified":  "{mod_date}",'
        content = content[:line_end] + insert_line + content[line_end:]
    
    with open(fp, "w", encoding="utf-8") as f:
        f.write(content)
    
    label = "TODAY" if slug in modified_today else pub_date
    added += 1
    print(f"  {fname}: dateModified={mod_date} ({label})")

print(f"\nAdded dateModified to {added} pages. Skipped {skipped} (already had it). Errors: {len(errors)}")
for e in errors:
    print(f"  ERROR: {e}")
