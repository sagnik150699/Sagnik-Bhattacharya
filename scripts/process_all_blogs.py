#!/usr/bin/env python3
"""
Comprehensive blog processor for sagnikbhattacharya.com
- Fixes breadcrumbs to consistent design
- Replaces "Complete Guide" with "Complete Course" in CTA boxes
- Ensures ScrollTrigger CDN is loaded
- Fixes missing meta tags
- Updates dateModified ONLY when content actually changes
"""

import os
import re
import json
from datetime import date

BLOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'blog')
TODAY = date.today().isoformat()

# ─── Helpers ────────────────────────────────���────────────────

def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()

def write_file(path, content):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)

def extract_meta(html_str, attr, name):
    """Extract content from a meta tag."""
    pattern = rf'<meta\s+{attr}="{re.escape(name)}"\s+content="([^"]*)"'
    m = re.search(pattern, html_str)
    if not m:
        pattern = rf'<meta\s+content="([^"]*)"\s+{attr}="{re.escape(name)}"'
        m = re.search(pattern, html_str)
    return m.group(1) if m else ''

def extract_title(html_str):
    m = re.search(r'<title>([^<]+)</title>', html_str)
    return m.group(1) if m else ''

def extract_tag(html_str):
    m = re.search(r'<span class="blog-post-tag">([^<]+)</span>', html_str)
    return m.group(1) if m else ''

def extract_slug(filepath):
    return os.path.splitext(os.path.basename(filepath))[0]

def json_escape(s):
    """Escape string for JSON."""
    return json.dumps(s)[1:-1]  # strip outer quotes


def truncate_title(text, max_len=55):
    """Truncate text at a word boundary for breadcrumb display."""
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(' ', 1)[0]
    return cut.rstrip(',:;—-') + '\u2026'


# ─── HTML Modification Functions ──────────────────────────────

def fix_breadcrumb(html_str, title):
    """Unify breadcrumb to: Home / Blog / [truncated title]."""
    short_title = truncate_title(title)

    # Pattern 1: Old breadcrumb
    old_bc = re.search(
        r'<div class="blog-breadcrumb"><a href="/blog">\u2190 Blog</a>\s*<span>/</span>\s*<span>([^<]*)</span></div>',
        html_str
    )
    if old_bc:
        new_bc = f'<nav class="blog-breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/blog">Blog</a><span aria-hidden="true">/</span><span>{short_title}</span></nav>'
        html_str = html_str.replace(old_bc.group(0), new_bc)
        return html_str

    # Pattern 2: Existing nav breadcrumb
    new_bc = re.search(
        r'<nav class="blog-breadcrumb"[^>]*>.*?</nav>',
        html_str, re.DOTALL
    )
    if new_bc:
        replacement = f'<nav class="blog-breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a><span aria-hidden="true">/</span><a href="/blog">Blog</a><span aria-hidden="true">/</span><span>{short_title}</span></nav>'
        html_str = html_str.replace(new_bc.group(0), replacement)

    return html_str


def fix_cta_guide_to_course(html_str):
    """Replace 'Complete Guide' with 'Complete Course' in CTA boxes only."""
    def replace_in_cta(match):
        cta_content = match.group(0)
        cta_content = cta_content.replace('Complete Guide', 'Complete Course')
        cta_content = cta_content.replace('complete guide', 'complete course')
        cta_content = cta_content.replace('Complete Excel Guide', 'Complete Excel Course')
        return cta_content

    html_str = re.sub(
        r'<div class="blog-cta-box">.*?</div>',
        replace_in_cta,
        html_str,
        flags=re.DOTALL
    )
    return html_str


def update_date_modified(html_str, new_date):
    """Update dateModified in JSON-LD and meta tags."""
    from datetime import datetime

    html_str = re.sub(
        r'"dateModified"\s*:\s*"[^"]*"',
        f'"dateModified":"{new_date}"',
        html_str
    )
    html_str = re.sub(
        r'(<meta\s+property="article:modified_time"\s+content=")[^"]*(")',
        rf'\g<1>{new_date}\2',
        html_str
    )

    # Format for display
    dt = datetime.strptime(new_date, '%Y-%m-%d')
    formatted = f'{dt.day} {dt.strftime("%b")} {dt.year}'

    # Update or add visible "Updated" label
    if 'blog-updated-date' in html_str:
        html_str = re.sub(
            r'<span class="blog-updated-date">Updated [^<]*</span>',
            f'<span class="blog-updated-date">Updated {formatted}</span>',
            html_str
        )
    else:
        meta_match = re.search(r'(<span>\d+ min read</span>)\s*(</div>)', html_str)
        if meta_match:
            html_str = html_str.replace(
                meta_match.group(0),
                f'{meta_match.group(1)}\n            <span class="blog-updated-date">Updated {formatted}</span>\n          {meta_match.group(2)}'
            )

    return html_str


def ensure_scrolltrigger(html_str):
    """Ensure ScrollTrigger CDN is loaded alongside GSAP."""
    if 'ScrollTrigger.min.js' in html_str:
        return html_str

    html_str = html_str.replace(
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>',
        '<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>\n  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>'
    )
    return html_str


def fix_missing_meta_tags(html_str, slug):
    """Ensure consistent meta tags across all blogs."""
    title = extract_title(html_str)
    desc = extract_meta(html_str, 'name', 'description')

    if 'twitter:title' not in html_str and 'twitter:card' in html_str:
        html_str = html_str.replace(
            '<meta name="twitter:card" content="summary_large_image">',
            f'<meta name="twitter:card" content="summary_large_image">\n  <meta name="twitter:title" content="{json_escape(title)}">\n  <meta name="twitter:description" content="{json_escape(desc)}">'
        )

    return html_str


# ─── Main Processing ─────────────────────────────────────────

def process_blog(filepath):
    """Process a single blog file. Only updates dateModified when content changes."""
    original = read_file(filepath)
    slug = extract_slug(filepath)
    title = extract_title(original)
    tag = extract_tag(original)

    if not title:
        print(f'  SKIP (no title): {slug}')
        return False

    html_str = original

    # Apply transformations (none of these touch dates)
    html_str = fix_breadcrumb(html_str, title)
    html_str = fix_cta_guide_to_course(html_str)
    html_str = ensure_scrolltrigger(html_str)
    html_str = fix_missing_meta_tags(html_str, slug)

    # Check if anything actually changed (content-wise)
    content_changed = html_str != original

    if content_changed:
        # Only now stamp the date, since we made real edits
        html_str = update_date_modified(html_str, TODAY)
        write_file(filepath, html_str)
        return True

    # No changes — don't touch the file
    return False


def main():
    blog_dir = os.path.normpath(BLOG_DIR)
    files = [f for f in os.listdir(blog_dir) if f.endswith('.html')]
    files.sort()

    print(f'Processing {len(files)} blog files...')
    print(f'Blog directory: {blog_dir}')
    print(f'Date for modified content: {TODAY}')
    print()

    changed = 0
    skipped = 0

    for filename in files:
        filepath = os.path.join(blog_dir, filename)
        slug = os.path.splitext(filename)[0]
        try:
            if process_blog(filepath):
                print(f'  CHANGED: {slug}')
                changed += 1
            else:
                print(f'  OK:      {slug} (no changes)')
                skipped += 1
        except Exception as e:
            print(f'  ERROR:   {slug} - {e}')

    print(f'\nDone: {changed} updated, {skipped} unchanged')


if __name__ == '__main__':
    main()
