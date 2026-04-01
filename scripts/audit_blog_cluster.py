from __future__ import annotations

import re
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urljoin, urlparse

import build_blog_cluster as cluster


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
SITE_URL = cluster.SITE_URL
REPORT_PATH = ROOT / "reports" / "blog-seo-audit-2026-04-01.md"
MOJIBAKE_MARKERS = ("â€”", "â€“", "â€™", "â€œ", "â€", "Â·", "Â©", "â˜•")
AMERICAN_WORDS = tuple(sorted(cluster.BRITISH_REPLACEMENTS.keys(), key=len, reverse=True))
AMERICAN_PATTERN = re.compile(r"\b(" + "|".join(map(re.escape, AMERICAN_WORDS)) + r")\b", re.I)


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", " ", value)


def tidy(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def route_for_path(path: Path) -> str:
    rel = path.relative_to(PUBLIC).as_posix()
    if rel == "index.html":
        return "/"
    if rel == "blog.html":
        return "/blog"
    if rel.endswith(".html"):
        rel = rel[:-5]
    return "/" + rel


def resolve_internal_target(source_route: str, href: str) -> Path | None:
    href = href.strip()
    if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
        return None
    absolute = urljoin(SITE_URL + source_route, href)
    parsed = urlparse(absolute)
    if parsed.scheme not in {"http", "https"}:
        return None
    if parsed.netloc and parsed.netloc != urlparse(SITE_URL).netloc:
        return None
    path = parsed.path or "/"
    if path == "/":
        return PUBLIC / "index.html"

    direct = PUBLIC / path.lstrip("/")
    if direct.exists():
        return direct

    if not Path(path).suffix:
        html_candidate = PUBLIC / (path.lstrip("/") + ".html")
        if html_candidate.exists():
            return html_candidate
    return direct


def extract_hrefs(text: str) -> list[str]:
    return re.findall(r'href="([^"]+)"', text)


def find_title(text: str) -> str:
    match = re.search(r"<title>(.*?)</title>", text, re.S)
    return tidy(strip_tags(match.group(1))) if match else ""


def find_h1(text: str) -> str:
    match = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S)
    return tidy(strip_tags(match.group(1))) if match else ""


def find_meta(text: str, name: str) -> str:
    match = re.search(rf'<meta [^>]*(?:name|property)="{re.escape(name)}" content="([^"]*)"', text)
    return match.group(1).strip() if match else ""


def broken_internal_links(path: Path, text: str) -> list[str]:
    source_route = route_for_path(path)
    broken: list[str] = []
    for href in extract_hrefs(text):
        target = resolve_internal_target(source_route, href)
        if target is None:
            continue
        if not target.exists():
            broken.append(href)
    return sorted(set(broken))


def content_internal_links(text: str) -> list[str]:
    match = re.search(r'<div class="blog-post-content">(.*)</div>\s*</article>', text, re.S)
    if not match:
        return []
    return [
        href
        for href in extract_hrefs(match.group(1))
        if href.startswith("/") and not href.startswith("/blog/images/")
    ]


def american_spellings(text: str) -> list[str]:
    visible = re.sub(r"<script[^>]*>.*?</script>", " ", text, flags=re.S | re.I)
    visible = re.sub(r"<style[^>]*>.*?</style>", " ", visible, flags=re.S | re.I)
    visible = tidy(strip_tags(visible))
    found = {match.group(1).lower() for match in AMERICAN_PATTERN.finditer(visible)}
    return sorted(found)


def main() -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    new_defs = {post["slug"]: post for post in cluster.NEW_POSTS}
    new_slugs = list(new_defs)
    new_urls = [f"{SITE_URL}/blog/{slug}" for slug in new_slugs]
    new_paths = [PUBLIC / "blog" / f"{slug}.html" for slug in new_slugs]
    old_paths = sorted(path for path in (PUBLIC / "blog").glob("*.html") if path.stem not in new_defs)
    blog_index = PUBLIC / "blog.html"
    feed_path = PUBLIC / "feed.xml"
    sitemap_path = PUBLIC / "sitemap.xml"

    blockers: list[str] = []
    highs: list[str] = []
    mediums: list[str] = []
    out_of_scope: list[str] = []

    titles = Counter()
    descriptions = Counter()
    inbound_from_new = Counter()
    total_internal_links_checked = 0

    for slug, path in zip(new_slugs, new_paths):
        if not path.exists():
            blockers.append(f"`{path.as_posix()}` is missing.")
            continue
        text = read_text(path)
        title = find_title(text)
        h1 = find_h1(text)
        desc = find_meta(text, "description")
        canonical = re.search(r'<link rel="canonical" href="([^"]+)"', text)
        modified = find_meta(text, "article:modified_time")
        og_image = find_meta(text, "og:image")
        twitter_image = find_meta(text, "twitter:image")
        image_path = resolve_internal_target(route_for_path(path), og_image.replace(SITE_URL, "")) if og_image else None
        broken = broken_internal_links(path, text)
        content_links = content_internal_links(text)
        american = american_spellings(text)
        total_internal_links_checked += len(extract_hrefs(text))

        if not title:
            blockers.append(f"`{path.name}` is missing a `<title>`.")
        if not h1:
            blockers.append(f"`{path.name}` is missing an `<h1>`.")
        if title and h1 and title != h1:
            blockers.append(f"`{path.name}` has a title/H1 mismatch: `{title}` vs `{h1}`.")
        if not desc:
            highs.append(f"`{path.name}` is missing a meta description.")
        if not canonical or canonical.group(1) != f"{SITE_URL}/blog/{slug}":
            blockers.append(f"`{path.name}` has the wrong canonical URL.")
        if not modified:
            highs.append(f"`{path.name}` is missing `article:modified_time`.")
        if not og_image or not twitter_image:
            highs.append(f"`{path.name}` is missing social image metadata.")
        if og_image and twitter_image and og_image != twitter_image:
            mediums.append(f"`{path.name}` uses different Open Graph and Twitter image URLs.")
        if og_image and (image_path is None or not image_path.exists()):
            blockers.append(f"`{path.name}` points to a missing cover image: `{og_image}`.")
        if "tracking.js" not in text:
            highs.append(f"`{path.name}` is missing `tracking.js`.")
        if broken:
            blockers.append(f"`{path.name}` has broken internal links: {', '.join(f'`{item}`' for item in broken)}.")
        unique_content_links = sorted(set(content_links))
        if len(unique_content_links) < 5:
            mediums.append(f"`{path.name}` has only {len(unique_content_links)} internal links inside the article body.")
        for href in unique_content_links:
            if href.startswith("/blog/"):
                target_slug = href.removeprefix("/blog/").split("#", 1)[0].split("?", 1)[0]
                if target_slug in new_defs and target_slug != slug:
                    inbound_from_new[target_slug] += 1
        if any(marker in text for marker in MOJIBAKE_MARKERS):
            blockers.append(f"`{path.name}` still contains mojibake characters.")
        if american:
            mediums.append(f"`{path.name}` still contains American spellings in visible copy: {', '.join(f'`{word}`' for word in american)}.")

        titles[title] += 1
        descriptions[desc] += 1

    for value, count in titles.items():
        if value and count > 1:
            blockers.append(f"Duplicate new-post title detected: `{value}` appears {count} times.")
    for value, count in descriptions.items():
        if value and count > 1:
            highs.append(f"Duplicate new-post meta description detected: `{value}` appears {count} times.")

    for slug in new_slugs:
        if inbound_from_new[slug] == 0:
            highs.append(f"`{slug}` has no inbound link from another new post.")

    if blog_index.exists():
        blog_text = read_text(blog_index)
        total_internal_links_checked += len(extract_hrefs(blog_text))
        index_broken = broken_internal_links(blog_index, blog_text)
        if index_broken:
            blockers.append(f"`public/blog.html` has broken internal links: {', '.join(f'`{item}`' for item in index_broken)}.")
        if any(marker in blog_text for marker in MOJIBAKE_MARKERS):
            blockers.append("`public/blog.html` still contains mojibake characters.")
        for slug in new_slugs:
            if f'/blog/{slug}"' not in blog_text:
                blockers.append(f"`public/blog.html` is missing the new post link for `{slug}`.")
    else:
        blockers.append("`public/blog.html` is missing.")

    if feed_path.exists():
        feed_text = read_text(feed_path)
        if any(marker in feed_text for marker in MOJIBAKE_MARKERS):
            blockers.append("`public/feed.xml` still contains mojibake characters.")
        items = re.findall(r"<item>.*?<link>(https://sagnikbhattacharya\\.com/blog/[^<]+)</link>.*?</item>", feed_text, re.S)
        for url in new_urls:
            if url not in feed_text:
                blockers.append(f"`public/feed.xml` is missing `{url}`.")
    else:
        blockers.append("`public/feed.xml` is missing.")

    if sitemap_path.exists():
        sitemap_text = read_text(sitemap_path)
        locs = re.findall(r"<loc>([^<]+)</loc>", sitemap_text)
        duplicate_locs = [url for url, count in Counter(locs).items() if count > 1]
        if duplicate_locs:
            highs.append(f"`public/sitemap.xml` has duplicate `<loc>` values: {', '.join(f'`{url}`' for url in duplicate_locs[:8])}.")
        for url in new_urls:
            if url not in locs:
                blockers.append(f"`public/sitemap.xml` is missing `{url}`.")
    else:
        blockers.append("`public/sitemap.xml` is missing.")

    for path in old_paths:
        text = read_text(path)
        legacy_issues: list[str] = []
        title = find_title(text).replace(" | Sagnik Bhattacharya", "")
        h1 = find_h1(text)
        if title and h1 and title != h1:
            legacy_issues.append("title/H1 mismatch")
        if not find_meta(text, "article:modified_time"):
            legacy_issues.append("missing article:modified_time")
        if "acquireLicensePage" not in text or "creditText" not in text:
            legacy_issues.append("missing newer image-licence metadata")
        if any(marker in text for marker in MOJIBAKE_MARKERS):
            legacy_issues.append("contains mojibake")
        broken = broken_internal_links(path, text)
        if broken:
            legacy_issues.append("broken internal link(s)")
        if legacy_issues:
            out_of_scope.append(f"`{path.name}`: {', '.join(legacy_issues)}.")

    summary = [
        "# Blog SEO Audit",
        "",
        f"- Audit date: `2026-04-01`",
        f"- New posts audited: `{len(new_slugs)}`",
        f"- Legacy posts inspected: `{len(old_paths)}`",
        f"- Internal links checked across in-scope HTML: `{total_internal_links_checked}`",
        f"- In-scope blockers: `{len(blockers)}`",
        f"- In-scope high findings: `{len(highs)}`",
        f"- In-scope medium findings: `{len(mediums)}`",
        "",
        "## In-Scope Findings",
        "",
        "### Blocker",
    ]

    if blockers:
        summary.extend(f"- {item}" for item in blockers)
    else:
        summary.append("- None.")

    summary.extend(["", "### High", ""])
    if highs:
        summary.extend(f"- {item}" for item in highs)
    else:
        summary.append("- None.")

    summary.extend(["", "### Medium", ""])
    if mediums:
        summary.extend(f"- {item}" for item in mediums)
    else:
        summary.append("- None.")

    summary.extend(["", "## Out-of-Scope Legacy Blog Findings", ""])
    if out_of_scope:
        summary.extend(f"- {item}" for item in out_of_scope)
    else:
        summary.append("- None detected in the sampled checks.")

    REPORT_PATH.write_text("\n".join(summary) + "\n", encoding="utf-8", newline="\n")
    print(REPORT_PATH)
    print(f"blockers={len(blockers)} highs={len(highs)} mediums={len(mediums)}")


if __name__ == "__main__":
    main()
