"""Cascade-delete tutorials per Phase 1 template in .claude/TASKS.md.

For each slug:
  1. Remove public/blog/<slug>.html
  2. Strip <url>...</url> block from public/sitemap.xml whose <loc> contains the slug
  3. Strip <item>...</item> block from public/feed.xml whose <link> contains the slug
  4. Remove any line from public/llms.txt and public/llms-full.txt mentioning the slug
  5. Strip the post card from public/blog.html (the <article> or grid card containing the slug)
  6. Append a line to reports/deleted-tutorials-log.md

Firebase 301 redirects are configured separately in firebase.json.
"""
from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
BLOG = PUBLIC / "blog"
LOG = ROOT / "reports" / "deleted-tutorials-log.md"


def strip_xml_block(text: str, container_tag: str, slug: str) -> tuple[str, int]:
    """Remove every <container_tag>...</container_tag> block whose contents
    reference /blog/<slug>."""
    pattern = re.compile(
        rf"\s*<{container_tag}>.*?/blog/{re.escape(slug)}(?:\.html)?[^<]*</[^>]+>.*?</{container_tag}>",
        re.S,
    )
    new_text, n = pattern.subn("", text)
    return new_text, n


def strip_lines_with_slug(text: str, slug: str) -> tuple[str, int]:
    needle = f"/blog/{slug}"
    kept = []
    removed = 0
    for line in text.splitlines(keepends=True):
        if needle in line and not line.strip().startswith("#"):
            removed += 1
        else:
            kept.append(line)
    return "".join(kept), removed


def strip_blog_card(text: str, slug: str) -> tuple[str, int]:
    """Remove the article card (top-level <article> or <a class="blog-card">
    or <li>) wrapping a link to /blog/<slug>."""
    # Try <article ...> ... href="/blog/<slug>" ... </article>
    candidates = [
        rf'<article[^>]*>(?:(?!</article>).)*?href="/blog/{re.escape(slug)}"(?:(?!</article>).)*?</article>',
        rf'<a[^>]*class="[^"]*blog-card[^"]*"[^>]*href="/blog/{re.escape(slug)}"[^>]*>.*?</a>',
        rf'<li[^>]*>(?:(?!</li>).)*?href="/blog/{re.escape(slug)}"(?:(?!</li>).)*?</li>',
    ]
    for pat in candidates:
        rx = re.compile(pat, re.S)
        new_text, n = rx.subn("", text)
        if n:
            return new_text, n
    return text, 0


def cascade(slug: str, reason: str) -> dict:
    summary = {"slug": slug, "reason": reason, "actions": []}

    # 1. Delete the .html file
    html_file = BLOG / f"{slug}.html"
    if html_file.exists():
        html_file.unlink()
        summary["actions"].append(f"removed {html_file.relative_to(ROOT)}")
    else:
        summary["actions"].append(f"NOTE: {html_file.relative_to(ROOT)} already absent")

    # 2. sitemap.xml
    sm = PUBLIC / "sitemap.xml"
    text = sm.read_text(encoding="utf-8")
    text, n = strip_xml_block(text, "url", slug)
    if n:
        sm.write_text(text, encoding="utf-8")
        summary["actions"].append(f"sitemap.xml: removed {n} <url> block")

    # 3. feed.xml
    fd = PUBLIC / "feed.xml"
    text = fd.read_text(encoding="utf-8")
    text, n = strip_xml_block(text, "item", slug)
    if n:
        fd.write_text(text, encoding="utf-8")
        summary["actions"].append(f"feed.xml: removed {n} <item> block")

    # 4. llms.txt + llms-full.txt
    for name in ("llms.txt", "llms-full.txt"):
        f = PUBLIC / name
        text = f.read_text(encoding="utf-8")
        text, n = strip_lines_with_slug(text, slug)
        if n:
            f.write_text(text, encoding="utf-8")
            summary["actions"].append(f"{name}: removed {n} line(s)")

    # 5. blog.html grid card
    bh = PUBLIC / "blog.html"
    text = bh.read_text(encoding="utf-8")
    text, n = strip_blog_card(text, slug)
    if n:
        bh.write_text(text, encoding="utf-8")
        summary["actions"].append(f"blog.html: removed {n} card")
    else:
        summary["actions"].append("blog.html: no card matched (slug may not be in grid)")

    return summary


def main():
    targets = [
        ("run-gemma-4-own-machine", "meta-refresh redirect stub; firebase 301 → run-gemma-4-locally"),
        ("seedance-reference-images-characters", "meta-refresh redirect stub; firebase 301 → consistent-characters-seedance"),
    ]

    log_lines = []
    today = date.today().isoformat()
    for slug, reason in targets:
        s = cascade(slug, reason)
        print(f"\n=== {slug} ===")
        for a in s["actions"]:
            print(f"  - {a}")
        log_lines.append(f"- `{slug}.html`: {reason} — {today}")
        log_lines.extend(f"  - {a}" for a in s["actions"])

    # Append to log
    if not LOG.exists():
        LOG.write_text("# Deleted tutorials log\n\n", encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write("\n".join(log_lines) + "\n")
    print(f"\nLogged to {LOG.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
