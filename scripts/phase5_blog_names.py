#!/usr/bin/env python3
"""Phase 5.5: Regenerate BLOG_NAMES.txt from all blog HTML files."""
import re, os

blog_dir = r"c:\Workspace\Sagnik Bhattacharya\public\blog"
output_file = r"c:\Workspace\Sagnik Bhattacharya\BLOG_NAMES.txt"

titles = []
for fname in sorted(os.listdir(blog_dir)):
    if not fname.endswith(".html") or fname == "index.html":
        continue
    fp = os.path.join(blog_dir, fname)
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    m = re.search(r"<title>([^<]+)</title>", content)
    if m:
        title = m.group(1).strip()
        # Remove trailing site name
        title = re.sub(r"\s*[\|—\-]\s*(Sagnik Bhattacharya|Coding Liquids).*$", "", title)
        titles.append(title)
    else:
        titles.append(f"??? ({fname})")

with open(output_file, "w", encoding="utf-8") as f:
    for t in titles:
        f.write(t + "\n")

print(f"Wrote {len(titles)} titles to BLOG_NAMES.txt")
