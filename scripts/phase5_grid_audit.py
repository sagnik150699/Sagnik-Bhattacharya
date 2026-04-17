#!/usr/bin/env python3
"""Audit blog.html grid for missing posts."""
import re, os

with open(r"c:\Workspace\Sagnik Bhattacharya\public\blog.html", "r", encoding="utf-8") as f:
    content = f.read()

links = re.findall(r'href="/blog/([^"]+)"', content)
unique = set(links)
print(f"blog.html unique /blog/ links: {len(unique)}")

blog_dir = r"c:\Workspace\Sagnik Bhattacharya\public\blog"
blog_slugs = set(f.replace(".html", "") for f in os.listdir(blog_dir) if f.endswith(".html") and f != "index.html")

missing = blog_slugs - unique
print(f"Missing from blog.html grid: {len(missing)}")
for s in sorted(missing):
    print(f"  {s}")

extra = unique - blog_slugs
print(f"In grid but no file: {len(extra)}")
for s in sorted(extra):
    print(f"  {s}")
