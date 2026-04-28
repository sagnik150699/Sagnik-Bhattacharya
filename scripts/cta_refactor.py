"""
Move all CTAs in public/blog/*.html into the intro region (above the first <h2>)
and delete duplicates from the body.

Pilot pattern (signed off on attendance-tracker-excel.html):
    P1 -> course card -> P2 -> Instagram -> P3 -> LinkedIn -> [section] -> YouTube -> first <h2>

Surgical regex-only approach — never reparses the whole file, never touches anything
outside the CTA blocks. This preserves the existing whitespace, attribute order, and
self-closing-tag style of every other element in the file.

Run:    python scripts/cta_refactor.py [--dry-run] [--limit N] [--only file.html ...]
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "public" / "blog"
SITEMAP = ROOT / "public" / "sitemap.xml"

# Verbatim CTA snippets, identical to the attendance-tracker pilot.
# `course_card` is the prominent card; `course_hint` is the short one-line tagline.
# Each tutorial uses ONE of them — we preserve whichever it already had, moved to
# the intro region. If the tutorial had neither, the course slot is skipped.
CTA = {
    "course_card": '<div class="blog-inline-course"><div class="blog-inline-course__badge">Coming Soon</div><div class="blog-inline-course__body"><h3 class="blog-inline-course__title">Complete Excel Guide with AI Integration</h3><p class="blog-inline-course__sub">Master formulas, pivot tables, data analysis, and charts — with AI integration.</p><a href="/courses#excel" class="btn-primary blog-inline-course__btn">Learn more <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a></div></div>',
    "course_hint": '<div class="blog-inline-courses-hint"><span class="blog-inline-courses-hint__icon"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/></svg></span><span>I teach Flutter and Excel with AI — <a href="/courses">explore my courses</a> if you want structured learning.</span></div>',
    "insta": '<a href="https://www.instagram.com/sagnikteaches" target="_blank" rel="noopener noreferrer" class="blog-social-nudge blog-social-nudge--insta"><span class="blog-social-nudge__icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="2" width="20" height="20" rx="5" ry="5"/><path d="M16 11.37A4 4 0 1 1 12.63 8 4 4 0 0 1 16 11.37z"/><line x1="17.5" y1="6.5" x2="17.51" y2="6.5"/></svg></span><span class="blog-social-nudge__text">Follow me on Instagram</span><span class="blog-social-nudge__handle">@sagnikteaches</span></a>',
    "linkedin": '<a href="https://www.linkedin.com/in/sagnik-bhattacharya-916b9463/" target="_blank" rel="noopener noreferrer" class="blog-social-nudge blog-social-nudge--linkedin"><span class="blog-social-nudge__icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-4 0v7h-4v-7a6 6 0 0 1 6-6z"/><rect x="2" y="9" width="4" height="12"/><circle cx="4" cy="4" r="2"/></svg></span><span class="blog-social-nudge__text">Connect on LinkedIn</span><span class="blog-social-nudge__handle">Sagnik Bhattacharya</span></a>',
    "youtube": '<a href="https://www.youtube.com/@codingliquids" target="_blank" rel="noopener noreferrer" class="blog-social-nudge blog-social-nudge--youtube"><span class="blog-social-nudge__icon"><svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22.54 6.42a2.78 2.78 0 0 0-1.94-2C18.88 4 12 4 12 4s-6.88 0-8.6.46a2.78 2.78 0 0 0-1.94 2A29 29 0 0 0 1 11.75a29 29 0 0 0 .46 5.33A2.78 2.78 0 0 0 3.4 19.13C5.12 19.56 12 19.56 12 19.56s6.88 0 8.6-.46a2.78 2.78 0 0 0 1.94-2 29 29 0 0 0 .46-5.25 29 29 0 0 0-.46-5.33z"/><polygon points="9.75 15.02 15.5 11.75 9.75 8.48 9.75 15.02"/></svg></span><span class="blog-social-nudge__text">Subscribe on YouTube</span><span class="blog-social-nudge__handle">@codingliquids</span></a>',
}

# Regex patterns for each CTA, designed to match the entire element + surrounding
# blank-line whitespace so removal does not leave double-spaces behind.
RE_COURSE_CARD = re.compile(
    r'\n?[ \t]*<div class="blog-inline-course">.*?</div>\s*</div>\s*</div>[ \t]*\n?',
    re.DOTALL,
)
RE_COURSE_HINT = re.compile(
    r'\n?[ \t]*<div class="blog-inline-courses-hint">.*?</div>[ \t]*\n?',
    re.DOTALL,
)
RE_INSTA = re.compile(
    r'\n?[ \t]*<a [^>]*\bblog-social-nudge--insta\b[^>]*>.*?</a>[ \t]*\n?',
    re.DOTALL,
)
RE_LINKEDIN = re.compile(
    r'\n?[ \t]*<a [^>]*\bblog-social-nudge--linkedin\b[^>]*>.*?</a>[ \t]*\n?',
    re.DOTALL,
)
RE_YOUTUBE = re.compile(
    r'\n?[ \t]*<a [^>]*\bblog-social-nudge--youtube\b[^>]*>.*?</a>[ \t]*\n?',
    re.DOTALL,
)
RE_CTA_BOX = re.compile(
    r'\n?[ \t]*<div class="blog-cta-box"\b.*?</div>[ \t]*\n?',
    re.DOTALL,
)

# Locate the post content region (.blog-post-content opens, closes at </article>).
RE_POST_CONTENT_OPEN = re.compile(r'<div class="blog-post-content">')
RE_ARTICLE_CLOSE = re.compile(r'</article>')


def split_post_region(html: str) -> tuple[str, str, str] | None:
    """Return (head, post_content_inner, tail) split around .blog-post-content.

    Returns None if the markers are not found in the expected order.
    """
    m_open = RE_POST_CONTENT_OPEN.search(html)
    if not m_open:
        return None
    # The closing of .blog-post-content is the </div> just before </article>.
    m_close = RE_ARTICLE_CLOSE.search(html, m_open.end())
    if not m_close:
        return None
    # Walk back from </article> to find the matching </div> for .blog-post-content.
    # Simpler: the structure is consistently "        </div>\n      </article>" — find it.
    region_end_idx = html.rfind("</div>", m_open.end(), m_close.start())
    if region_end_idx == -1:
        return None
    head = html[: m_open.end()]
    inner = html[m_open.end() : region_end_idx]
    tail = html[region_end_idx:]
    return head, inner, tail


def detect_course_variant(post_inner: str) -> str | None:
    """Return 'course_card', 'course_hint', or None for which course-CTA the file uses."""
    if RE_COURSE_CARD.search(post_inner):
        return "course_card"
    if RE_COURSE_HINT.search(post_inner):
        return "course_hint"
    return None


def strip_ctas(post_inner: str) -> str:
    """Remove every CTA from the post content (anywhere — intro or body)."""
    out = post_inner
    out = RE_COURSE_CARD.sub("\n", out)
    out = RE_COURSE_HINT.sub("\n", out)
    out = RE_INSTA.sub("\n", out)
    out = RE_LINKEDIN.sub("\n", out)
    out = RE_YOUTUBE.sub("\n", out)
    out = RE_CTA_BOX.sub("\n", out)
    # Collapse any 3+ consecutive newlines into 2.
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out


def insert_ctas_into_intro(post_inner: str, course_variant: str | None) -> tuple[str, dict]:
    """Walk the intro region (before first <h2>) and interleave CTAs after each <p>.

    Slot order: course (variant preserved) -> insta -> linkedin -> youtube (always
    immediately before the first <h2>).
    Trailing CTAs (those without a matching paragraph) cluster just before <h2>.
    A file with no course CTA originally keeps no course CTA.
    """
    # Build the ordered list of CTAs to place.
    slot_order: list[str] = []
    if course_variant is not None:
        slot_order.append(course_variant)
    slot_order.extend(["insta", "linkedin", "youtube"])

    h2_match = re.search(r"\n[ \t]*<h2[ >]", post_inner)
    if not h2_match:
        # Tutorial has no <h2>. Append all CTAs at the end of post content.
        out = post_inner.rstrip() + "\n\n" + "\n\n".join(CTA[k] for k in slot_order) + "\n"
        return out, {"intro_p_count": 0, "no_h2": True}

    h2_pos = h2_match.start()
    intro = post_inner[:h2_pos]
    body = post_inner[h2_pos:]

    # Find every closing </p> in the intro region — one entry per intro paragraph.
    p_close_positions = [m.end() for m in re.finditer(r"</p>", intro)]
    intro_p_count = len(p_close_positions)

    # All slots EXCEPT youtube go after intro paragraphs. Youtube always sits right
    # before <h2> as the last visible CTA in the intro region.
    paragraph_slots = [k for k in slot_order if k != "youtube"]

    inserts_at_p: list[tuple[int, str]] = []
    for i, key in enumerate(paragraph_slots):
        if i < intro_p_count:
            inserts_at_p.append((p_close_positions[i], "\n\n" + CTA[key]))

    leftover_keys = paragraph_slots[intro_p_count:] + ["youtube"]

    # Apply paragraph-slot inserts from right to left so positions stay valid.
    new_intro = intro
    for pos, snippet in sorted(inserts_at_p, key=lambda x: -x[0]):
        new_intro = new_intro[:pos] + snippet + new_intro[pos:]

    # Trailing CTAs: cluster just before <h2>.
    if leftover_keys:
        trailing = "\n\n" + "\n\n".join(CTA[k] for k in leftover_keys)
        new_intro = new_intro.rstrip() + trailing + "\n"

    return new_intro + body, {"intro_p_count": intro_p_count, "no_h2": False}


def bump_dates(html: str, today: str) -> str:
    """Update dateModified in JSON-LD and article:modified_time meta to `today`."""
    html = re.sub(r'"dateModified"\s*:\s*"[^"]+"', f'"dateModified":"{today}"', html)
    html = re.sub(
        r'<meta\s+property="article:modified_time"\s+content="[^"]+">',
        f'<meta property="article:modified_time" content="{today}">',
        html,
    )
    # Some files use the verbose JSON layout: "dateModified":"YYYY-MM-DD" appears once,
    # already handled above. Some have it on a separate line — covered too.
    return html


def bump_sitemap_lastmod(slugs: list[str], today: str) -> int:
    if not SITEMAP.exists() or not slugs:
        return 0
    text = SITEMAP.read_text(encoding="utf-8")
    n = 0
    for slug in slugs:
        pattern = re.compile(
            rf'(<loc>https://sagnikbhattacharya\.com/blog/{re.escape(slug)}</loc>\s*<lastmod>)[^<]+(</lastmod>)'
        )
        text, count = pattern.subn(rf'\g<1>{today}\g<2>', text)
        n += count
    SITEMAP.write_text(text, encoding="utf-8")
    return n


def process_file(path: Path, today: str, dry_run: bool) -> dict:
    raw = path.read_text(encoding="utf-8")
    split = split_post_region(raw)
    if split is None:
        return {"path": path, "changed": False, "notes": ["no .blog-post-content / </article> markers"]}
    head, inner, tail = split

    # Detect which course-CTA variant the file uses (so we can preserve it).
    course_variant = detect_course_variant(inner)

    # Count pre-state CTAs for reporting.
    pre = {
        "course_card": len(RE_COURSE_CARD.findall(inner)),
        "course_hint": len(RE_COURSE_HINT.findall(inner)),
        "insta": len(RE_INSTA.findall(inner)),
        "linkedin": len(RE_LINKEDIN.findall(inner)),
        "youtube": len(RE_YOUTUBE.findall(inner)),
        "cta_box": len(RE_CTA_BOX.findall(inner)),
    }

    stripped = strip_ctas(inner)
    new_inner, info = insert_ctas_into_intro(stripped, course_variant)

    new_html = head + new_inner + tail
    new_html = bump_dates(new_html, today)

    changed = new_html != raw

    if changed and not dry_run:
        path.write_text(new_html, encoding="utf-8")

    # Verify post-state.
    post_inner_only = new_inner
    post = {
        "course_card": len(RE_COURSE_CARD.findall(post_inner_only)),
        "course_hint": len(RE_COURSE_HINT.findall(post_inner_only)),
        "insta": len(RE_INSTA.findall(post_inner_only)),
        "linkedin": len(RE_LINKEDIN.findall(post_inner_only)),
        "youtube": len(RE_YOUTUBE.findall(post_inner_only)),
        "cta_box": len(RE_CTA_BOX.findall(post_inner_only)),
    }

    return {
        "path": path,
        "changed": changed,
        "pre": pre,
        "post": post,
        "intro_p_count": info.get("intro_p_count", 0),
        "no_h2": info.get("no_h2", False),
        "notes": [],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--only", nargs="*", default=None)
    args = parser.parse_args()

    today = dt.date.today().isoformat()
    files = sorted(BLOG_DIR.glob("*.html"))
    if args.only:
        wanted = set(args.only)
        files = [f for f in files if f.name in wanted]
    if args.limit is not None:
        files = files[: args.limit]

    print(f"Processing {len(files)} files. dry_run={args.dry_run}, today={today}")
    print(f"  pre  = (course/insta/linkedin/youtube/cta_box) anywhere in post")
    print(f"  post = same, after refactor; should be 1/1/1/1/0")

    updated_slugs: list[str] = []
    issues = 0
    for f in files:
        r = process_file(f, today, args.dry_run)
        flag = "CHANGE" if r["changed"] else "noop  "
        pre = r.get("pre", {})
        post = r.get("post", {})
        intro_p = r.get("intro_p_count", "?")
        course_total_pre = pre.get('course_card', 0) + pre.get('course_hint', 0)
        course_total_post = post.get('course_card', 0) + post.get('course_hint', 0)
        line = (
            f"  {flag}  {f.name:<55s}  "
            f"pre={course_total_pre}/{pre.get('insta',0)}/{pre.get('linkedin',0)}/{pre.get('youtube',0)}/{pre.get('cta_box',0)}  "
            f"post={course_total_post}/{post.get('insta',0)}/{post.get('linkedin',0)}/{post.get('youtube',0)}/{post.get('cta_box',0)}  "
            f"introP={intro_p}"
        )
        if r.get("no_h2"):
            line += "  [NO H2]"
        # Flag anomalies. Course is allowed to be 0 if the file never had one.
        max_course_post = 1 if course_total_pre > 0 else 0
        if r["changed"] and (
            course_total_post != max_course_post
            or post.get("insta") != 1
            or post.get("linkedin") != 1
            or post.get("youtube") != 1
            or post.get("cta_box") != 0
        ):
            line += "  !!"
            issues += 1
        print(line)
        if r["notes"]:
            for note in r["notes"]:
                print(f"      note: {note}")
        if r["changed"]:
            updated_slugs.append(f.stem)

    if not args.dry_run and updated_slugs:
        n = bump_sitemap_lastmod(updated_slugs, today)
        print(f"\nsitemap.xml: bumped <lastmod> for {n} entries")

    print(f"\n{len(updated_slugs)} file(s) changed, {issues} anomalies flagged")
    return 0 if issues == 0 else 2


if __name__ == "__main__":
    sys.exit(main())
