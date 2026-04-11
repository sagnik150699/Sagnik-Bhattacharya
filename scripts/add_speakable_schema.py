"""Inject SpeakableSpecification schema into every blog post that lacks it.

This signals to voice assistants and AI citation tools which page regions are the
canonical citable summaries. We point at the post title plus the first two body
paragraphs, which already function as the lead/summary in every post template.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "public" / "blog"

HUB_SLUGS = {"excel-ai-guide", "excel-formulas-guide", "flutter-guide", "seedance-guide"}

updated = 0
skipped = 0
hub_skipped = 0

for path in sorted(BLOG.glob("*.html")):
    if path.stem in HUB_SLUGS:
        hub_skipped += 1
        continue
    html = path.read_text(encoding="utf-8")
    if "SpeakableSpecification" in html:
        skipped += 1
        continue

    slug = path.stem
    canonical_match = re.search(r'rel="canonical"\s+href="([^"]+)"', html)
    canonical = canonical_match.group(1) if canonical_match else f"https://sagnikbhattacharya.com/blog/{slug}"

    speakable = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": canonical,
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": [
                ".blog-post-title",
                ".blog-post-content > p:nth-of-type(1)",
                ".blog-post-content > p:nth-of-type(2)",
                ".blog-post-content h2",
            ],
        },
    }
    block = (
        '  <script type="application/ld+json">\n'
        + json.dumps(speakable, indent=2)
        + "\n  </script>\n"
    )

    if "</head>" not in html:
        print(f"NO HEAD {path.name}")
        continue
    new_html = html.replace("</head>", block + "</head>", 1)
    path.write_text(new_html, encoding="utf-8")
    updated += 1

print(f"Updated: {updated}")
print(f"Already had speakable: {skipped}")
print(f"Hub pages skipped: {hub_skipped}")
