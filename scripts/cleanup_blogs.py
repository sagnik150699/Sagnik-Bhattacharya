#!/usr/bin/env python3
"""
One-time cleanup script for blog HTML files.
Removes:
  1. FAQPage JSON-LD schema blocks
  2. Visible "Frequently asked questions" HTML sections
  3. Inflated dateModified (reverts to datePublished)
  4. "Updated ..." date labels
  5. "reveal" class from core content wrappers (header, cover, content, CTA)
  6. Fixes broken CTA text on Flutter pages and "course course" redundancy
"""

import os
import re
import glob

BLOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'blog')


def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


def write_file(path, content):
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(content)


def remove_faq_schema(html):
    """Remove the FAQPage JSON-LD script block."""
    return re.sub(
        r'\s*<script type="application/ld\+json">\s*\{[^<]*"FAQPage"[^<]*\}</script>',
        '',
        html
    )


def remove_faq_html(html):
    """Remove the visible 'Frequently asked questions' section."""
    # Pattern: <h2>Frequently asked questions</h2> followed by <p> blocks until the next <div or end
    html = re.sub(
        r'\n*<h2>Frequently asked questions</h2>\n*(?:<p>.*?</p>\n*)+',
        '',
        html,
        flags=re.DOTALL
    )
    return html


def revert_date_modified(html):
    """Set dateModified back to datePublished and remove Updated label."""
    # Extract datePublished
    pub_match = re.search(r'"datePublished"\s*:\s*"([^"]*)"', html)
    if not pub_match:
        return html
    pub_date = pub_match.group(1)

    # Revert dateModified in JSON-LD
    html = re.sub(
        r'"dateModified"\s*:\s*"[^"]*"',
        f'"dateModified":"{pub_date}"',
        html
    )

    # Revert article:modified_time meta tag
    html = re.sub(
        r'(<meta\s+property="article:modified_time"\s+content=")[^"]*(")',
        rf'\g<1>{pub_date}\2',
        html
    )

    # Remove the "Updated ..." span
    html = re.sub(
        r'\s*<span class="blog-updated-date">Updated [^<]*</span>',
        '',
        html
    )

    return html


def remove_reveal_from_content(html):
    """Remove 'reveal' class from blog content wrappers only."""
    # blog-post-header reveal -> blog-post-header
    html = html.replace('blog-post-header reveal', 'blog-post-header')
    # blog-cover reveal -> blog-cover
    html = html.replace('blog-cover reveal', 'blog-cover')
    # blog-post-content reveal -> blog-post-content
    html = html.replace('blog-post-content reveal', 'blog-post-content')
    # blog-cta-box reveal -> blog-cta-box
    html = html.replace('blog-cta-box reveal', 'blog-cta-box')
    return html


def is_flutter_article(html):
    """Check if this is a Flutter/Dart article."""
    tag_match = re.search(r'<span class="blog-post-tag">([^<]+)</span>', html)
    if tag_match:
        tag = tag_match.group(1).lower()
        if 'flutter' in tag or 'dart' in tag:
            return True
    title_match = re.search(r'<title>([^<]+)</title>', html)
    if title_match:
        title = title_match.group(1).lower()
        if 'flutter' in title or 'dart' in title:
            return True
    return False


def fix_ctas(html):
    """Fix CTA issues: Flutter articles with Excel CTAs, and double 'course' text."""
    flutter = is_flutter_article(html)

    if flutter:
        # Fix Flutter articles that wrongly promote Excel course
        html = html.replace(
            'Explore the Excel + AI course',
            'Explore The Complete Flutter Guide'
        )
        html = html.replace(
            'href="/courses#excel"',
            'href="/courses#flutter"'
        )
        html = re.sub(
            r'(<div class="blog-cta-box[^"]*">.*?<a[^>]*href=")/courses(" class="btn-primary">)',
            r'\1/courses#flutter\2',
            html,
            flags=re.DOTALL
        )
        # Fix CTA body text for Flutter articles
        html = re.sub(
            r'(<div class="blog-cta-box[^"]*">.*?<p>)The Complete Excel Course with AI Integration[^<]*(</p>)',
            r'\1The Complete Flutter Guide: Build Android, iOS and Web apps takes you from basics to production-ready apps, with real projects and modern patterns.\2',
            html,
            flags=re.DOTALL
        )
        html = re.sub(
            r'(<div class="blog-cta-box[^"]*">.*?<p>)My Complete Excel Course with AI Integration[^<]*(</p>)',
            r'\1The Complete Flutter Guide: Build Android, iOS and Web apps takes you from basics to production-ready apps, with real projects and modern patterns.\2',
            html,
            flags=re.DOTALL
        )
        html = re.sub(
            r'(<div class="blog-cta-box[^"]*">.*?<p>)My Complete Flutter Course[^<]*(</p>)',
            r'\1The Complete Flutter Guide: Build Android, iOS and Web apps takes you from zero to building production-ready Android, iOS, and web apps.\2',
            html,
            flags=re.DOTALL
        )
        html = html.replace(
            'Explore the Flutter + Dart course',
            'Explore The Complete Flutter Guide'
        )

    # Fix "Complete Excel Course with AI Integration course" -> remove redundant "course"
    html = html.replace(
        'Complete Excel Course with AI Integration course',
        'Complete Excel Course with AI Integration'
    )

    return html


def process_file(filepath):
    html = read_file(filepath)
    original = html

    html = remove_faq_schema(html)
    html = remove_faq_html(html)
    html = revert_date_modified(html)
    html = remove_reveal_from_content(html)
    html = fix_ctas(html)

    if html != original:
        write_file(filepath, html)
        return True
    return False


def main():
    blog_dir = os.path.normpath(BLOG_DIR)
    files = sorted(glob.glob(os.path.join(blog_dir, '*.html')))

    print(f'Cleaning {len(files)} blog files in {blog_dir}...\n')

    changed = 0
    for filepath in files:
        slug = os.path.splitext(os.path.basename(filepath))[0]
        if process_file(filepath):
            print(f'  FIXED: {slug}')
            changed += 1
        else:
            print(f'  SKIP:  {slug} (no changes needed)')

    print(f'\nDone: {changed}/{len(files)} files updated.')


if __name__ == '__main__':
    main()
