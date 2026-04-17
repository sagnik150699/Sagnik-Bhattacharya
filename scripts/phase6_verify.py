#!/usr/bin/env python3
"""Phase 6.1: Crawl-check all internal links — no broken /blog/ references."""
import re, os

blog_dir = r"c:\Workspace\Sagnik Bhattacharya\public\blog"
public_dir = r"c:\Workspace\Sagnik Bhattacharya\public"

# Build set of all valid blog slugs
valid_slugs = set()
for f in os.listdir(blog_dir):
    if f.endswith(".html"):
        valid_slugs.add(f.replace(".html", ""))

# Also check for other valid paths
valid_paths = set()
for root, dirs, files in os.walk(public_dir):
    for f in files:
        rel = os.path.relpath(os.path.join(root, f), public_dir).replace("\\", "/")
        # Remove .html extension for clean URLs
        if rel.endswith(".html"):
            valid_paths.add("/" + rel.replace(".html", ""))
        valid_paths.add("/" + rel)

broken = []
total_links = 0

for fname in sorted(os.listdir(blog_dir)):
    if not fname.endswith(".html"):
        continue
    fp = os.path.join(blog_dir, fname)
    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find all internal /blog/ links
    links = re.findall(r'href="(/blog/[^"#]+)"', content)
    for link in links:
        total_links += 1
        slug = link.replace("/blog/", "").rstrip("/")
        if slug not in valid_slugs:
            broken.append((fname, link))

# Also check blog.html grid
with open(os.path.join(public_dir, "blog.html"), "r", encoding="utf-8") as f:
    grid = f.read()
grid_links = re.findall(r'href="(/blog/[^"#]+)"', grid)
for link in grid_links:
    total_links += 1
    slug = link.replace("/blog/", "").rstrip("/")
    if slug not in valid_slugs:
        broken.append(("blog.html", link))

print(f"Total internal /blog/ links checked: {total_links}")
print(f"Broken links: {len(broken)}")
for src, link in broken:
    print(f"  {src} -> {link}")

# Check ads.txt
ads_txt = os.path.join(public_dir, "ads.txt")
if os.path.exists(ads_txt):
    with open(ads_txt, "r", encoding="utf-8") as f:
        ads_content = f.read().strip()
    if "google.com" in ads_content and "pub-" in ads_content:
        print(f"\nads.txt: OK ({len(ads_content)} bytes, contains google.com pub-ID)")
    else:
        print(f"\nads.txt: WARNING - may be incomplete")
    print(f"  Content: {ads_content[:200]}")
else:
    print(f"\nads.txt: NOT FOUND")
