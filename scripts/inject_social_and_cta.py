#!/usr/bin/env python3
"""
Inject social media nudges and course CTAs into blog posts.

Categories (from article:section meta tag):
  - Flutter: section contains "Flutter", "Mobile", "Cross-Platform"
  - AI: section contains "AI"
  - Excel/Other: everything else

What gets injected:
  - Social nudges (Instagram, LinkedIn, YouTube) distributed across h2 sections
  - Course card near top for Flutter & Excel posts
  - "Explore courses" hint near top for AI posts

Idempotent: skips files that already have injected content.
Usage: python inject_social_and_cta.py [--dry-run]
"""

import os
import re
import sys
import html as html_mod

BLOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'blog')

# ─── Social nudge HTML ─────────────────────────────────────────

SOCIAL_HTML = {
    'insta': (
        '<a href="https://www.instagram.com/sagnikteaches" target="_blank" rel="noopener noreferrer" class="blog-social-nudge blog-social-nudge--insta">'
        '<span class="blog-social-nudge__icon">'
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<rect x="2" y="2" width="20" height="20" rx="5" ry="5"/>'
        '<path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/>'
        '<line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></span>'
        '<span class="blog-social-nudge__text">Follow me on Instagram</span>'
        '<span class="blog-social-nudge__handle">@sagnikteaches</span>'
        '</a>'
    ),
    'linkedin': (
        '<a href="https://www.linkedin.com/in/sagnik-bhattacharya-916b9463/" target="_blank" rel="noopener noreferrer" class="blog-social-nudge blog-social-nudge--linkedin">'
        '<span class="blog-social-nudge__icon">'
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/>'
        '<rect x="2" y="9" width="4" height="12"/>'
        '<circle cx="4" cy="4" r="2"/></svg></span>'
        '<span class="blog-social-nudge__text">Connect on LinkedIn</span>'
        '<span class="blog-social-nudge__handle">Sagnik Bhattacharya</span>'
        '</a>'
    ),
    'youtube': (
        '<a href="https://www.youtube.com/@codingliquids" target="_blank" rel="noopener noreferrer" class="blog-social-nudge blog-social-nudge--youtube">'
        '<span class="blog-social-nudge__icon">'
        '<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19.13C5.12 19.56 12 19.56 12 19.56s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/>'
        '<polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/></svg></span>'
        '<span class="blog-social-nudge__text">Subscribe on YouTube</span>'
        '<span class="blog-social-nudge__handle">@codingliquids</span>'
        '</a>'
    ),
}

SOCIAL_ORDER = ['insta', 'linkedin', 'youtube']

# ─── Course card HTML ───────────────────────────────────────────

FLUTTER_COURSE_CARD = (
    '<div class="blog-inline-course">'
    '<img src="/images/the-complete-flutter-guide-build-android-ios-and-web-apps.jpg" '
    'alt="The Complete Flutter Guide" width="280" height="147" loading="lazy">'
    '<div class="blog-inline-course__body">'
    '<h3 class="blog-inline-course__title">The Complete Flutter Guide: Build Android, iOS and Web Apps</h3>'
    '<p class="blog-inline-course__sub">Flutter 2026: Build fast, production-grade apps for Android, iOS &amp; Web with Flutter &amp; Dart</p>'
    '<a href="https://www.udemy.com/course/flutter-the-guide-to-build-android-ios-and-web-apps/'
    '?referralCode=0895EF14011CB08E80A0" target="_blank" rel="noopener noreferrer" '
    'class="btn-primary blog-inline-course__btn">Enroll on Udemy '
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M5 12h14M12 5l7 7-7 7"/></svg></a>'
    '</div></div>'
)

EXCEL_COURSE_CARD = (
    '<div class="blog-inline-course">'
    '<div class="blog-inline-course__badge">Coming Soon</div>'
    '<div class="blog-inline-course__body">'
    '<h3 class="blog-inline-course__title">Complete Excel Guide with AI Integration</h3>'
    '<p class="blog-inline-course__sub">Master formulas, pivot tables, data analysis, and charts \u2014 with AI integration.</p>'
    '<a href="/courses#excel" class="btn-primary blog-inline-course__btn">Learn more '
    '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
    '<path d="M5 12h14M12 5l7 7-7 7"/></svg></a>'
    '</div></div>'
)

AI_COURSES_HINT = (
    '<div class="blog-inline-courses-hint">'
    '<span class="blog-inline-courses-hint__icon">'
    '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/>'
    '<path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></span>'
    '<span>I teach Flutter and Excel with AI \u2014 '
    '<a href="/courses">explore my courses</a> if you want structured learning.</span>'
    '</div>'
)

# ─── Boilerplate h2 keywords (skip injection here) ──────────────

BOILERPLATE_KEYWORDS = [
    'sources', 'further reading', 'related posts', 'related guides',
    'official references',
]


def detect_category(html_str):
    """Detect blog category from article:section meta tag and title."""
    title_m = re.search(r'<title>([^<]*)</title>', html_str)
    title = title_m.group(1).lower() if title_m else ''
    if 'flutter' in title or 'android studio' in title or 'dart' in title:
        return 'flutter'

    m = re.search(r'article:section"\s+content="([^"]*)"', html_str)
    if not m:
        return 'other'
    section = html_mod.unescape(m.group(1)).lower()
    if 'flutter' in section or 'mobile' in section or 'cross-platform' in section:
        return 'flutter'
    if 'ai' in section:
        return 'ai'
    return 'other'


def is_boilerplate_h2(h2_text):
    """Check if an h2 title is a boilerplate section."""
    lower = h2_text.lower()
    return any(kw in lower for kw in BOILERPLATE_KEYWORDS)


def split_at_h2(content):
    """Split content into sections at <h2> boundaries.

    Returns a list where:
      - parts[0] = content before the first <h2> (intro paragraphs)
      - parts[1..N] = each starts with <h2>
    """
    parts = re.split(r'(?=<h2[ >])', content)
    return parts


def extract_h2_title(section):
    """Extract the text content of the first <h2> in a section."""
    m = re.search(r'<h2[^>]*>(.*?)</h2>', section, re.DOTALL)
    if m:
        # Strip HTML tags from the title
        return re.sub(r'<[^>]+>', '', m.group(1)).strip()
    return ''


def inject_into_file(filepath, dry_run=False):
    """Process a single blog file. Returns (changed, category, stats)."""
    with open(filepath, 'r', encoding='utf-8') as f:
        html_str = f.read()

    # Idempotency: skip if already fully injected
    has_nudges = 'blog-social-nudge' in html_str
    has_courses = 'blog-inline-course' in html_str or 'blog-inline-courses-hint' in html_str
    if has_nudges and has_courses:
        return False, None, {}
    skip_courses = has_courses

    category = detect_category(html_str)

    # Find blog-post-content boundaries
    content_start = html_str.find('<div class="blog-post-content">')
    if content_start == -1:
        return False, category, {}

    # Find the content between blog-post-content and blog-cta-box
    cta_pos = html_str.find('<div class="blog-cta-box">', content_start)
    if cta_pos == -1:
        # No CTA box - find closing </div> of blog-post-content
        # This is trickier; use the content up to </article>
        article_end = html_str.find('</article>', content_start)
        if article_end == -1:
            return False, category, {}
        cta_pos = article_end

    # The actual content to process
    content_tag_end = content_start + len('<div class="blog-post-content">')
    content = html_str[content_tag_end:cta_pos]

    # Split at h2 boundaries
    parts = split_at_h2(content)

    if len(parts) < 2:
        # No h2 sections found
        return False, category, {}

    # Classify sections: find content vs boilerplate h2 indices
    content_indices = []
    boilerplate_indices = []
    for i in range(1, len(parts)):
        title = extract_h2_title(parts[i])
        if is_boilerplate_h2(title):
            boilerplate_indices.append(i)
        else:
            content_indices.append(i)

    n = len(content_indices)
    if n == 0:
        return False, category, {}

    # Determine injection points
    injections = {}  # index -> html to append after that part

    # Course card / courses hint: after first content h2 section
    course_idx = content_indices[0]
    if not skip_courses:
        if category == 'flutter':
            injections[course_idx] = FLUTTER_COURSE_CARD
        elif category == 'ai':
            injections[course_idx] = AI_COURSES_HINT
        else:
            injections[course_idx] = EXCEL_COURSE_CARD

    # Social nudges: distribute across remaining content sections
    available = [i for i in content_indices[1:] if i not in boilerplate_indices]
    # Remove last content section (too close to CTA)
    if len(available) > 1:
        available = available[:-1]

    if n <= 4:
        social_count = min(1, len(available))
    elif n <= 7:
        social_count = min(2, len(available))
    else:
        social_count = min(3, len(available))

    social_indices = []
    if social_count > 0 and len(available) > 0:
        step = max(1, len(available) // social_count)
        for j in range(social_count):
            idx = j * step
            if idx < len(available):
                social_indices.append(available[idx])

    for j, idx in enumerate(social_indices):
        platform = SOCIAL_ORDER[j]
        social_html = SOCIAL_HTML[platform]
        if idx in injections:
            injections[idx] += social_html
        else:
            injections[idx] = social_html

    if not injections:
        return False, category, {}

    # Reconstruct content
    new_parts = []
    for i, part in enumerate(parts):
        new_parts.append(part)
        if i in injections:
            new_parts.append(injections[i])

    new_content = ''.join(new_parts)
    new_html = html_str[:content_tag_end] + new_content + html_str[cta_pos:]

    stats = {
        'socials': len(social_indices),
        'social_platforms': [SOCIAL_ORDER[j] for j in range(len(social_indices))],
        'course_type': category,
        'content_h2s': n,
    }

    if not dry_run:
        with open(filepath, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_html)

    return True, category, stats


def main():
    dry_run = '--dry-run' in sys.argv

    if dry_run:
        print("=== DRY RUN MODE (no files will be written) ===\n")

    files = sorted([
        f for f in os.listdir(BLOG_DIR)
        if f.endswith('.html')
    ])

    counts = {'flutter': 0, 'ai': 0, 'other': 0, 'skipped': 0, 'no_change': 0}
    total_socials = 0

    for filename in files:
        filepath = os.path.join(BLOG_DIR, filename)
        changed, category, stats = inject_into_file(filepath, dry_run=dry_run)

        if changed:
            counts[category] += 1
            total_socials += stats['socials']
            if dry_run:
                print(f"  [{category:>7}] {filename} "
                      f"| {stats['content_h2s']} h2s "
                      f"| socials: {', '.join(stats['social_platforms']) or 'none'}")
        elif category is None:
            counts['skipped'] += 1
            if dry_run:
                print(f"  [SKIP   ] {filename} (already injected)")
        else:
            counts['no_change'] += 1
            if dry_run:
                print(f"  [NOCHANGE] {filename}")

    print(f"\n{'DRY RUN ' if dry_run else ''}Summary:")
    print(f"  Flutter course cards: {counts['flutter']}")
    print(f"  AI courses hints:     {counts['ai']}")
    print(f"  Excel course cards:   {counts['other']}")
    print(f"  Total social nudges:  {total_socials}")
    print(f"  Skipped (already):    {counts['skipped']}")
    print(f"  No change:            {counts['no_change']}")
    print(f"  Total files:          {len(files)}")


if __name__ == '__main__':
    main()
