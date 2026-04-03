#!/usr/bin/env python3
"""
One-time fix script:
1. Adds cache-busting query strings to /style.css and /animations.js in all HTML files.
2. Fixes breadcrumb aria-current="page" on blog posts (removes it from the category tag,
   since the category is not the current page — the article is).
"""

import os
import re
import hashlib
import glob

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'public')
BLOG_DIR = os.path.join(PUBLIC_DIR, 'blog')


def file_hash(path, length=8):
    with open(path, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()[:length]


def add_cache_busting(html, css_ver, js_ver):
    """Add ?v=hash to /style.css and /animations.js references."""
    # Strip any existing query string first, then add fresh one
    html = re.sub(
        r'href="/style\.css(\?[^"]*)?"',
        f'href="/style.css?v={css_ver}"',
        html
    )
    html = re.sub(
        r'src="/animations\.js(\?[^"]*)?"',
        f'src="/animations.js?v={js_ver}"',
        html
    )
    return html


def fix_breadcrumb_aria(html):
    """Remove aria-current="page" from category span in blog breadcrumbs.

    Before: <span aria-current="page">Formulas</span>
    After:  <span>Formulas</span>

    Only targets the last span inside .blog-breadcrumb nav.
    """
    html = re.sub(
        r'(<nav class="blog-breadcrumb"[^>]*>.*?)<span aria-current="page">([^<]+)</span>(</nav>)',
        r'\1<span>\2</span>\3',
        html,
        flags=re.DOTALL
    )
    return html


def main():
    css_ver = file_hash(os.path.join(PUBLIC_DIR, 'style.css'))
    js_ver = file_hash(os.path.join(PUBLIC_DIR, 'animations.js'))
    print(f'Cache versions: style.css?v={css_ver}, animations.js?v={js_ver}\n')

    # Process ALL HTML files in public/ (top-level + blog/)
    html_files = glob.glob(os.path.join(PUBLIC_DIR, '*.html'))
    html_files += glob.glob(os.path.join(BLOG_DIR, '*.html'))
    html_files.sort()

    cache_updated = 0
    bc_updated = 0

    for filepath in html_files:
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()

        html = original

        # Cache busting applies to all HTML files
        html = add_cache_busting(html, css_ver, js_ver)

        # Breadcrumb fix only applies to blog posts
        is_blog = os.path.normpath(BLOG_DIR) in os.path.normpath(os.path.dirname(filepath))
        if is_blog:
            before_bc = html
            html = fix_breadcrumb_aria(html)
            if html != before_bc:
                bc_updated += 1

        if html != original:
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(html)
            cache_updated += 1
            name = os.path.relpath(filepath, PUBLIC_DIR).replace('\\', '/')
            print(f'  FIXED: {name}')

    print(f'\nDone: {cache_updated} files got cache-busting, {bc_updated} blog breadcrumbs fixed.')


if __name__ == '__main__':
    main()
