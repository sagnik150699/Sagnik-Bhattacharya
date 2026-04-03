#!/usr/bin/env python3
"""
One-time fix script:
1. Replaces breadcrumb last item with truncated article title (from <title> tag).
2. Updates <h1> to match <title> on pages where they differ.
"""

import os
import re
import glob

BLOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'blog')
TRUNCATE_LEN = 55


def truncate(text, max_len=TRUNCATE_LEN):
    """Truncate text at a word boundary, adding ellipsis if needed."""
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(' ', 1)[0]
    return cut.rstrip(',:;—-') + '\u2026'


def extract_title(html):
    m = re.search(r'<title>([^<]+)</title>', html)
    return m.group(1).strip() if m else ''


def extract_h1(html):
    m = re.search(r'<h1[^>]*>([^<]+)</h1>', html)
    return m.group(1).strip() if m else ''


def fix_breadcrumb(html, title):
    """Replace the last breadcrumb span with a truncated version of the title."""
    short = truncate(title)
    # Match the current breadcrumb nav and replace the last <span>...</span></nav>
    html = re.sub(
        r'(<nav class="blog-breadcrumb"[^>]*>.*?<a href="/blog">Blog</a><span aria-hidden="true">/</span>)<span>[^<]*</span>(</nav>)',
        rf'\1<span>{short}</span>\2',
        html,
        flags=re.DOTALL
    )
    return html


def fix_h1(html, title):
    """Update <h1> text to match <title>."""
    h1 = extract_h1(html)
    if not h1 or h1 == title:
        return html, False

    # Replace the h1 content, preserving the tag attributes
    html = re.sub(
        r'(<h1[^>]*>)[^<]+(</h1>)',
        rf'\g<1>{title}\2',
        html
    )
    return html, True


def main():
    blog_dir = os.path.normpath(BLOG_DIR)
    files = sorted(glob.glob(os.path.join(blog_dir, '*.html')))

    print(f'Fixing {len(files)} blog files...\n')

    bc_fixed = 0
    h1_fixed = 0

    for filepath in files:
        slug = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath, 'r', encoding='utf-8') as f:
            original = f.read()

        html = original
        title = extract_title(html)
        if not title:
            continue

        # Fix breadcrumb
        html = fix_breadcrumb(html, title)

        # Fix h1 mismatch
        html, h1_changed = fix_h1(html, title)

        if html != original:
            with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
                f.write(html)

            changes = []
            if html != original:
                changes.append('breadcrumb')
            if h1_changed:
                changes.append('h1')
                h1_fixed += 1
            bc_fixed += 1
            print(f'  FIXED ({", ".join(changes)}): {slug}')

    print(f'\nDone: {bc_fixed} breadcrumbs updated, {h1_fixed} h1 tags synced to title.')


if __name__ == '__main__':
    main()
