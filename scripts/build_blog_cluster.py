from __future__ import annotations

import html
import json
import math
import re
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from typing import Any
import xml.etree.ElementTree as ET


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
BLOG_DIR = PUBLIC / "blog"
SITE_URL = "https://sagnikbhattacharya.com"
AUTHOR_NAME = "Sagnik Bhattacharya"
AUTHOR_URL = SITE_URL
AUTHOR_LINKEDIN = "https://www.linkedin.com/in/sagnik-bhattacharya-916b9463/"
AUTHOR_EMAIL = "sagnik@codingliquids.com"
ORG_NAME = "Coding Liquids"
ORG_URL = "https://codingliquids.com"
ORG_LOGO = "https://www.codingliquids.com/logo.png?v=13"
LICENSE_URL = "https://www.codingliquids.com/termsofuse"
ACQUIRE_LICENSE_URL = f"{SITE_URL}/contact"
HEADSHOT_PATH = "/sagnik-bhattacharya.png"
GA_ID = "G-G88BTBD73Q"
RSS_PATH = "/feed.xml"
BLOG_INDEX_PATH = PUBLIC / "blog.html"
RSS_FILE = PUBLIC / "feed.xml"
SITEMAP_FILE = PUBLIC / "sitemap.xml"
AUDIT_REPORT = ROOT / "reports" / "blog-seo-audit-2026-04-01.md"

BRITISH_REPLACEMENTS = {
    "analyze": "analyse",
    "analyzed": "analysed",
    "analyzing": "analysing",
    "behavior": "behaviour",
    "color": "colour",
    "colors": "colours",
    "customize": "customise",
    "customized": "customised",
    "customizing": "customising",
    "favor": "favour",
    "favorite": "favourite",
    "favorites": "favourites",
    "modeling": "modelling",
    "optimized": "optimised",
    "optimize": "optimise",
    "optimizing": "optimising",
    "organization": "organisation",
    "organizations": "organisations",
    "organize": "organise",
    "organized": "organised",
    "organizing": "organising",
    "summarize": "summarise",
    "summarized": "summarised",
    "summarizing": "summarising",
    "center": "centre",
    "centered": "centred",
    "license": "licence",
}

MOJIBAKE_REPLACEMENTS = {
    "â€”": "—",
    "â€“": "–",
    "â€™": "’",
    "â€˜": "‘",
    "â€œ": "“",
    "â€": "”",
    "Â·": "·",
    "Â©": "©",
    "â˜•": "☕",
    "â†": "←",
    "Ã©": "é",
    "Ã¨": "è",
    "Ã¢": "â",
    "Ã—": "×",
    "Â": "",
}

COURSE_COPY = {
    "Excel": {
        "href": "/courses#excel",
        "heading": "Want to get better at Excel without guessing?",
        "body": "My Complete Excel Guide with AI Integration is built for practical work: formulas, reporting, cleaner models, and AI-assisted workflows.",
        "label": "Explore the Excel course",
    },
    "AI + Excel": {
        "href": "/courses#excel",
        "heading": "Want a structured way to use Excel with AI at work?",
        "body": "My Complete Excel Guide with AI Integration covers spreadsheet fundamentals, prompt design, and review habits that help you work faster without trusting AI blindly.",
        "label": "See the Excel + AI course",
    },
    "Flutter": {
        "href": "/courses",
        "heading": "Need a structured Flutter learning path?",
        "body": "My Flutter and Dart training focuses on production habits, architecture choices, and the practical skills teams need to ship and maintain apps.",
        "label": "Explore Flutter courses",
    },
}

OLD_POST_FALLBACKS = {
    "advanced-formulas": "15 Excel Formulas That Save Hours of Manual Work (With Examples)",
    "charts-visualisations": "How to Make Professional Charts in Excel (Step-by-Step Guide)",
    "chatgpt-excel-guide": "How to Use ChatGPT to Write Excel Formulas (With Real Examples)",
    "claude-ai-excel-formulas": "How to Use Claude AI to Write Excel Formulas Instantly",
    "claude-ai-excel-macros": "How to Use Claude AI to Write Excel Macros and VBA Code",
    "claude-debug-formulas": "How to Fix Excel Formula Errors with Claude AI (Fast)",
    "clean-messy-data": "How to Clean Messy Data in Excel: Step-by-Step Guide",
    "conditional-formatting-tips": "How to Highlight Rows Based on Cell Value in Excel",
    "copilot-automate-tasks": "How to Automate Excel Tasks with Microsoft Copilot",
    "copilot-data-analysis": "How to Use Microsoft Copilot for Data Analysis in Excel",
    "data-validation": "How to Add a Dropdown List in Excel Using Data Validation",
    "dynamic-dashboards": "How to Build an Interactive Dashboard in Excel (No VBA)",
    "excel-ai-prompts": "60 AI Prompts for Excel That Actually Work (Copy, Paste, Get Results)",
    "excel-vs-google-sheets": "Excel vs Google Sheets: Which Is Better for You in 2026?",
    "financial-modelling": "How to Build a Financial Model in Excel From Scratch",
    "flutter-state-management": "Flutter State Management in 2026: Provider vs Riverpod vs BLoC",
    "flutter-vs-react-native": "Flutter vs React Native in 2026: Which Should You Choose?",
    "gemini-ai-excel": "How to Use Google Gemini to Write Excel Formulas for Free",
    "getting-started-copilot-excel": "How to Set Up and Use Microsoft Copilot in Excel (2026)",
    "index-match-guide": "How to Use INDEX MATCH in Excel with Multiple Criteria",
    "keyboard-shortcuts": "30 Excel Keyboard Shortcuts That Save Hours Every Week",
    "mastering-pivot-tables": "How to Create a Pivot Table in Excel Step by Step",
    "power-pivot-guide": "How to Use Power Pivot in Excel to Analyse Millions of Rows",
    "power-query-guide": "How to Use Power Query in Excel to Automate Data Cleaning",
    "vlookup-vs-xlookup": "VLOOKUP vs XLOOKUP: Differences and When to Use Each",
    "what-if-analysis": "How to Use What-If Analysis in Excel: Goal Seek and Scenarios",
}

SECTION_META = {
    "Excel": {
        "section": "Excel",
        "cover_tag": "Excel Guide",
    },
    "AI + Excel": {
        "section": "AI & Automation",
        "cover_tag": "AI + Excel",
    },
    "Flutter": {
        "section": "Flutter",
        "cover_tag": "Flutter",
    },
}

SOURCES = {
    "agent_mode": {"label": "Microsoft Support: Agent Mode in Excel", "url": "https://support.microsoft.com/en-us/office/agent-mode-in-excel-frontier-a2fd6fe4-97ac-416b-b89a-22f4d1357c7a"},
    "claude_agent": {"label": "Microsoft Support: Use Claude with Agent Mode in Excel", "url": "https://support.microsoft.com/en-us/topic/use-claude-with-agent-mode-frontier-in-excel-b2c3b3ec-154b-484b-84d0-914a80df395a"},
    "copilot_function": {"label": "Microsoft Support: COPILOT function", "url": "https://support.microsoft.com/en-us/office/copilot-function-5849821b-755d-4030-a38b-9e20be0cbf62"},
    "format_copilot": {"label": "Microsoft Support: Format data for Copilot in Excel", "url": "https://support.microsoft.com/en-us/topic/format-data-for-copilot-in-excel-1604c8eb-57f1-4db1-8363-d53336228c65"},
    "python_availability": {"label": "Microsoft Support: Python in Excel availability", "url": "https://support.microsoft.com/en-us/office/python-in-excel-availability-781383e6-86b9-4156-84fb-93e786f7cab0"},
    "copilot_excel": {"label": "Microsoft Support: Copilot in Excel", "url": "https://support.microsoft.com/en-us/copilot-excel"},
    "groupby": {"label": "Microsoft Support: GROUPBY function", "url": "https://support.microsoft.com/en-gb/office/groupby-function-5e08ae8c-6800-4b72-b623-c41773611505"},
    "widget_previewer": {"label": "Flutter docs: Widget Previewer", "url": "https://docs.flutter.dev/tools/widget-previewer"},
    "ai_overview": {"label": "Flutter docs: Create with AI", "url": "https://docs.flutter.dev/resources/ai-overview"},
    "web_renderers": {"label": "Flutter docs: Web renderers", "url": "https://docs.flutter.dev/platform-integration/web/renderers"},
    "architecture": {"label": "Flutter docs: App architecture guide", "url": "https://docs.flutter.dev/app-architecture/guide"},
    "navigation": {"label": "Flutter docs: Navigation and routing", "url": "https://docs.flutter.dev/ui/navigation"},
    "validation": {"label": "Flutter docs: Build a form with validation", "url": "https://docs.flutter.dev/cookbook/forms/validation"},
    "testing": {"label": "Flutter docs: Testing overview", "url": "https://docs.flutter.dev/testing"},
}


@dataclass
class Post:
    slug: str
    title: str
    category: str
    description: str
    keywords: list[str]
    body_html: str
    published: date
    modified: date
    read_time: int
    image_src: str
    image_alt: str
    cover_hook: str
    cover_cta: str
    cover_keywords: list[str]
    cover_cue: str
    related_new: list[str]
    related_old: list[str]
    primary_intent: str
    search_type: str
    notes: list[str]
    sources: list[dict[str, str]]
    intro_text: str
    category_section: str
    in_scope: bool

    @property
    def url(self) -> str:
        return f"{SITE_URL}/blog/{self.slug}"

    @property
    def path(self) -> Path:
        return BLOG_DIR / f"{self.slug}.html"

    @property
    def image_url(self) -> str:
        return f"{SITE_URL}{self.image_src}"

    @property
    def display_date(self) -> str:
        return self.published.strftime("%d %b %Y").lstrip("0")

    @property
    def feed_date(self) -> str:
        return self.published.strftime("%a, %d %b %Y 00:00:00 +0530")


def normalise_text(value: str) -> str:
    for bad, good in MOJIBAKE_REPLACEMENTS.items():
        value = value.replace(bad, good)
    return value


def britishise(value: str) -> str:
    def repl(match: re.Match[str]) -> str:
        word = match.group(0)
        replacement = BRITISH_REPLACEMENTS.get(word.lower())
        if not replacement:
            return word
        if word.isupper():
            return replacement.upper()
        if word[0].isupper():
            return replacement.capitalize()
        return replacement

    pattern = re.compile(r"\b(" + "|".join(map(re.escape, sorted(BRITISH_REPLACEMENTS, key=len, reverse=True))) + r")\b", re.I)
    return pattern.sub(repl, value)


def html_escape(value: str) -> str:
    return html.escape(value, quote=True)


def strip_tags(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value)


def tidy_spaces(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def words_in_html(value: str) -> int:
    return len(re.findall(r"\b[\w#@/+\-.]+\b", strip_tags(value)))


def estimate_read_time(body_html: str) -> int:
    return max(3, math.ceil(words_in_html(body_html) / 220))


def render_list(items: list[str]) -> str:
    return "".join(f"<li>{item}</li>" for item in items)


def render_paragraphs(items: list[str]) -> str:
    return "".join(f"<p>{item}</p>" for item in items)


def render_table(headers: list[str], rows: list[list[str]]) -> str:
    head = "".join(f"<th scope=\"col\">{html_escape(h)}</th>" for h in headers)
    body_rows = []
    for row in rows:
        cells = "".join(f"<td>{cell}</td>" for cell in row)
        body_rows.append(f"<tr>{cells}</tr>")
    return (
        "<div class=\"blog-table-wrap\">"
        "<table>"
        f"<thead><tr>{head}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody>"
        "</table>"
        "</div>"
    )


def render_code_block(code: str, language: str = "") -> str:
    info = language.strip()
    class_attr = f' class="language-{info}"' if info else ""
    return f"<pre><code{class_attr}>{html_escape(code)}</code></pre>"


def section_html(title: str, paragraphs: list[str] | None = None, bullets: list[str] | None = None, table: str | None = None, code: str | None = None, code_language: str = "") -> str:
    html_parts = [f"<h2>{title}</h2>"]
    if paragraphs:
        html_parts.append(render_paragraphs(paragraphs))
    if table:
        html_parts.append(table)
    if bullets:
        html_parts.append(f"<ul>{render_list(bullets)}</ul>")
    if code:
        html_parts.append(render_code_block(code, code_language))
    return "".join(html_parts)


def make_notes_box(items: list[str]) -> str:
    if not items:
        return ""
    return "<blockquote>" + "".join(f"<p><strong>Note:</strong> {item}</p>" for item in items) + "</blockquote>"


def slug_title(slug: str) -> str:
    return OLD_POST_FALLBACKS.get(slug, slug.replace("-", " ").title())


def parse_existing_posts() -> dict[str, Post]:
    posts: dict[str, Post] = {}
    for path in sorted(BLOG_DIR.glob("*.html")):
        slug = path.stem
        text = normalise_text(read_utf8(path))
        title_match = re.search(r"<title>(.*?)</title>", text, re.S)
        desc_match = re.search(r'<meta name="description" content="([^"]+)"', text)
        h1_match = re.search(r"<h1[^>]*>(.*?)</h1>", text, re.S)
        tag_match = re.search(r'<span class="blog-post-tag">(.*?)</span>', text, re.S)
        date_match = re.search(r'<meta property="article:published_time" content="([^"]+)"', text)
        image_match = re.search(r'<meta property="og:image" content="([^"]+)"', text)
        alt_match = re.search(r'<meta property="og:image:alt" content="([^"]+)"', text)
        read_time_match = re.search(r'<span>(\d+)\s+min read</span>', text)
        body_match = re.search(r'<div class="blog-post-content">(.*)</div>\s*(?:<div class="blog-cta-box">|</article>)', text, re.S)

        title = tidy_spaces(html.unescape(strip_tags(title_match.group(1)))) if title_match else slug_title(slug)
        title = title.replace(" | Sagnik Bhattacharya", "")
        description = html.unescape(desc_match.group(1)) if desc_match else title
        category = tidy_spaces(html.unescape(strip_tags(tag_match.group(1)))) if tag_match else "Blog"
        published = date.fromisoformat(date_match.group(1)[:10]) if date_match else date(2026, 3, 1)
        image_url = image_match.group(1) if image_match else f"{SITE_URL}/sagnik-bhattacharya.png"
        image_src = image_url.replace(SITE_URL, "")
        image_alt = html.unescape(alt_match.group(1)) if alt_match else title
        body_html = body_match.group(1) if body_match else ""
        read_time = int(read_time_match.group(1)) if read_time_match else estimate_read_time(body_html)
        intro_text = tidy_spaces(strip_tags(h1_match.group(1))) if h1_match else title

        posts[slug] = Post(
            slug=slug,
            title=britishise(title),
            category=category,
            description=britishise(description),
            keywords=[],
            body_html=body_html,
            published=published,
            modified=published,
            read_time=read_time,
            image_src=image_src,
            image_alt=britishise(image_alt),
            cover_hook="",
            cover_cta="",
            cover_keywords=[],
            cover_cue="",
            related_new=[],
            related_old=[],
            primary_intent="legacy",
            search_type="legacy",
            notes=[],
            sources=[],
            intro_text=britishise(intro_text),
            category_section=category,
            in_scope=False,
        )
    return posts


def read_utf8(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def blog_post_schema(post: Post) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "BlogPosting",
        "headline": post.title,
        "description": post.description,
        "datePublished": post.published.isoformat(),
        "dateModified": post.modified.isoformat(),
        "inLanguage": "en-GB",
        "author": {"@type": "Person", "name": AUTHOR_NAME, "url": AUTHOR_URL},
        "publisher": {
            "@type": "Organization",
            "name": ORG_NAME,
            "url": ORG_URL,
            "logo": {"@type": "ImageObject", "url": ORG_LOGO},
        },
        "mainEntityOfPage": {"@type": "WebPage", "@id": post.url},
        "image": {
            "@type": "ImageObject",
            "url": post.image_url,
            "contentUrl": post.image_url,
            "width": 1200,
            "height": 630,
            "caption": f"{post.title} by {AUTHOR_NAME} for {ORG_NAME}",
            "creditText": f"{AUTHOR_NAME} for {ORG_NAME}",
            "license": LICENSE_URL,
            "acquireLicensePage": ACQUIRE_LICENSE_URL,
            "copyrightNotice": f"© {AUTHOR_NAME} and {ORG_NAME}. All rights reserved.",
            "creator": {"@type": "Person", "name": AUTHOR_NAME, "url": AUTHOR_URL},
            "publisher": {"@type": "Organization", "name": ORG_NAME, "url": ORG_URL},
            "copyrightHolder": {"@type": "Organization", "name": ORG_NAME, "url": ORG_URL},
        },
        "keywords": ", ".join(post.keywords[:8]),
        "articleSection": post.category_section,
    }
    return json.dumps(schema, ensure_ascii=False, separators=(",", ":"))


def organisation_schema() -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": ORG_NAME,
        "url": ORG_URL,
        "logo": {"@type": "ImageObject", "url": ORG_LOGO},
        "founder": {"@type": "Person", "name": AUTHOR_NAME, "url": AUTHOR_URL},
    }
    return json.dumps(schema, ensure_ascii=False, separators=(",", ":"))


def breadcrumb_schema(post: Post) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": SITE_URL + "/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": SITE_URL + "/blog"},
            {"@type": "ListItem", "position": 3, "name": post.title, "item": post.url},
        ],
    }
    return json.dumps(schema, ensure_ascii=False, separators=(",", ":"))


def image_schema(post: Post) -> str:
    schema = {
        "@context": "https://schema.org",
        "@type": "ImageObject",
        "name": post.title,
        "url": post.image_url,
        "contentUrl": post.image_url,
        "caption": f"{post.title} by {AUTHOR_NAME} for {ORG_NAME}",
        "creditText": f"{AUTHOR_NAME} for {ORG_NAME}",
        "license": LICENSE_URL,
        "acquireLicensePage": ACQUIRE_LICENSE_URL,
        "copyrightNotice": f"© {AUTHOR_NAME} and {ORG_NAME}. All rights reserved.",
        "creator": {"@type": "Person", "name": AUTHOR_NAME, "url": AUTHOR_URL},
    }
    return json.dumps(schema, ensure_ascii=False, separators=(",", ":"))


def page_head(post: Post) -> str:
    title = html_escape(post.title)
    desc = html_escape(post.description)
    canonical = html_escape(post.url)
    image_alt = html_escape(post.image_alt)
    keywords = html_escape(", ".join(post.keywords[:8]))
    article_tags = "".join(f'  <meta property="article:tag" content="{html_escape(tag)}">\n' for tag in post.keywords[:6])
    return f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <meta name="description" content="{desc}">
  <meta name="keywords" content="{keywords}">
  <meta name="author" content="{AUTHOR_NAME}">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="canonical" href="{canonical}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{desc}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="{canonical}">
  <meta property="og:image" content="{post.image_url}">
  <meta property="og:image:secure_url" content="{post.image_url}">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{image_alt}">
  <meta property="og:locale" content="en_GB">
  <meta property="og:site_name" content="{AUTHOR_NAME}">
  <meta property="article:author" content="{AUTHOR_NAME}">
  <meta property="article:published_time" content="{post.published.isoformat()}">
  <meta property="article:modified_time" content="{post.modified.isoformat()}">
  <meta property="article:section" content="{html_escape(post.category_section)}">
{article_tags}  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{post.image_url}">
  <meta name="twitter:image:alt" content="{image_alt}">
  <link rel="alternate" type="application/rss+xml" title="{AUTHOR_NAME} — Blog" href="{RSS_PATH}">
  <script type="application/ld+json">{blog_post_schema(post)}</script>
  <script type="application/ld+json">{organisation_schema()}</script>
  <script type="application/ld+json">{breadcrumb_schema(post)}</script>
  <script type="application/ld+json">{image_schema(post)}</script>
  <link rel="stylesheet" href="/style.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}");</script>"""


def nav_html(active_blog: bool = True) -> str:
    blog_class = ' class="active"' if active_blog else ""
    return f"""  <nav id="navbar">
    <div class="container">
      <a href="/" class="nav-logo">sagnik<span>.</span></a>
      <ul class="nav-links" id="navLinks">
        <li><a href="/about">About</a></li>
        <li><a href="/courses">Courses</a></li>
        <li><a href="/services">Services</a></li>
        <li><a href="/blog"{blog_class}>Blog</a></li>
        <li><a href="/contact" class="nav-cta">Get in Touch</a></li>
      </ul>
      <button class="hamburger" id="hamburger" aria-label="Menu"><span></span><span></span><span></span></button>
    </div>
  </nav>"""


def footer_html() -> str:
    return """  <footer>
    <div class="container">
      <p>&copy; 2026 Sagnik Bhattacharya · Built with ☕ in Kolkata · <a href="https://codingliquids.com" target="_blank" rel="noopener">Coding Liquids</a></p>
    </div>
  </footer>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js" defer></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js" defer></script>
  <script src="/animations.js" defer></script>
  <script src="/tracking.js" defer></script>"""


def render_cta(category: str) -> str:
    cta = COURSE_COPY[category]
    return (
        '<div class="blog-cta-box">'
        f"<h3>{html_escape(cta['heading'])}</h3>"
        f"<p>{html_escape(cta['body'])}</p>"
        f'<a href="{cta["href"]}" class="btn-primary">{html_escape(cta["label"])} '
        '<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">'
        '<path d="M5 12h14M12 5l7 7-7 7"/></svg></a>'
        "</div>"
    )


def build_related_links(new_lookup: dict[str, dict[str, Any]], old_lookup: dict[str, Post], slugs: list[str]) -> list[tuple[str, str]]:
    links: list[tuple[str, str]] = []
    for slug in slugs:
        if slug in new_lookup:
            links.append((new_lookup[slug]["title"], f"/blog/{slug}"))
        elif slug in old_lookup:
            links.append((old_lookup[slug].title, f"/blog/{slug}"))
        else:
            raise KeyError(f"Unknown related slug: {slug}")
    return links


def render_related_section(post: dict[str, Any], new_lookup: dict[str, dict[str, Any]], old_lookup: dict[str, Post]) -> str:
    links = build_related_links(new_lookup, old_lookup, post["related_new"] + post["related_old"])
    intro = post.get("related_intro") or "If you want to keep going without opening dead ends, these are the most useful next reads from this site."
    items = "".join(f'<li><a href="{href}">{html_escape(title)}</a></li>' for title, href in links)
    return f"<h2>Related guides on this site</h2><p>{intro}</p><ul>{items}</ul>"


def render_post_page(post: Post) -> str:
    breadcrumb = (
        '<nav class="blog-breadcrumb" aria-label="Breadcrumb">'
        '<a href="/">Home</a><span>/</span>'
        '<a href="/blog">Blog</a><span>/</span>'
        f'<span aria-current="page">{html_escape(post.title)}</span>'
        "</nav>"
    )
    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
{page_head(post)}
</head>
<body>
{nav_html(True)}
  <div class="page-hero" style="padding-bottom:20px">
    <div class="container">
      {breadcrumb}
    </div>
  </div>
  <section style="padding-top:0">
    <div class="container">
      <article class="blog-post">
        <div class="blog-post-header">
          <div class="blog-post-tags"><span class="blog-post-tag">{html_escape(post.category)}</span></div>
          <h1 class="blog-post-title">{html_escape(post.title)}</h1>
          <div class="blog-post-meta">
            <a href="{AUTHOR_URL}" class="blog-author-avatar" title="{AUTHOR_NAME}">
              <img src="{HEADSHOT_PATH}" alt="{AUTHOR_NAME}" width="48" height="48">
            </a>
            <span>By <a href="{AUTHOR_LINKEDIN}" target="_blank" rel="noopener noreferrer" class="blog-author-name">{AUTHOR_NAME}</a></span>
            <span>{post.display_date}</span>
            <span>{post.read_time} min read</span>
          </div>
        </div>
        <figure class="blog-cover">
          <img src="{post.image_src}" alt="{html_escape(post.image_alt)}" width="1200" height="630" loading="eager" fetchpriority="high" decoding="async">
          <figcaption class="sr-only">{html_escape(post.image_alt)}</figcaption>
        </figure>
        <div class="blog-post-content">
{post.body_html}
{render_cta(post.category)}
        </div>
      </article>
    </div>
  </section>
{footer_html()}
</body>
</html>
"""


def render_archive_page(all_posts: list[Post]) -> str:
    description = "Useful Excel, Excel with AI, and Flutter guides with practical steps, realistic examples, and clear next actions."
    item_list = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": "Blog by Sagnik Bhattacharya",
        "description": description,
        "url": SITE_URL + "/blog",
        "inLanguage": "en-GB",
        "publisher": {"@type": "Organization", "name": ORG_NAME, "url": ORG_URL},
        "mainEntity": {
            "@type": "ItemList",
            "itemListElement": [
                {"@type": "ListItem", "position": index + 1, "url": post.url, "name": post.title}
                for index, post in enumerate(all_posts)
            ],
        },
    }
    cards = []
    for index, post in enumerate(all_posts):
        loading = "eager" if index < 6 else "lazy"
        cards.append(
            f'<a href="/blog/{post.slug}" class="blog-card reveal">'
            '<div class="blog-card-accent"></div>'
            f'<img src="{post.image_src}" alt="{html_escape(post.title)}" class="blog-card-thumb" loading="{loading}" width="600" height="315" decoding="async">'
            '<div class="blog-card-body">'
            f'<div class="blog-card-tags"><span class="blog-card-tag">{html_escape(post.category)}</span></div>'
            f"<h3>{html_escape(post.title)}</h3>"
            f"<p>{html_escape(post.description)}</p>"
            f'<div class="blog-card-meta"><span>{post.display_date}</span><span class="read-time">{post.read_time} min read</span></div>'
            "</div></a>"
        )

    head = f"""  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Blog | Excel, Excel with AI & Flutter Guides | {AUTHOR_NAME}</title>
  <meta name="description" content="{html_escape(description)}">
  <meta name="keywords" content="Excel blog, Excel with AI, Flutter tutorials, spreadsheet workflows, Copilot in Excel, Sagnik Bhattacharya">
  <meta name="author" content="{AUTHOR_NAME}">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/svg+xml" href="/favicon.svg">
  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
  <link rel="canonical" href="{SITE_URL}/blog">
  <meta property="og:title" content="Blog | Excel, Excel with AI & Flutter Guides | {AUTHOR_NAME}">
  <meta property="og:description" content="{html_escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:url" content="{SITE_URL}/blog">
  <meta property="og:image" content="{SITE_URL}/sagnik-bhattacharya.png">
  <meta property="og:image:width" content="500">
  <meta property="og:image:height" content="500">
  <meta property="og:image:type" content="image/png">
  <meta property="og:image:alt" content="Sagnik Bhattacharya — Excel, Excel with AI, and Flutter blog">
  <meta property="og:locale" content="en_GB">
  <meta property="og:site_name" content="{AUTHOR_NAME}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="Blog | Excel, Excel with AI & Flutter Guides | {AUTHOR_NAME}">
  <meta name="twitter:description" content="{html_escape(description)}">
  <meta name="twitter:image" content="{SITE_URL}/sagnik-bhattacharya.png">
  <link rel="alternate" type="application/rss+xml" title="{AUTHOR_NAME} — Blog" href="/feed.xml">
  <script type="application/ld+json">{json.dumps(item_list, ensure_ascii=False, separators=(",", ":"))}</script>
  <script type="application/ld+json">{organisation_schema()}</script>
  <script type="application/ld+json">{json.dumps({"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":SITE_URL+"/"},{"@type":"ListItem","position":2,"name":"Blog","item":SITE_URL+"/blog"}]}, ensure_ascii=False, separators=(",", ":"))}</script>
  <link rel="stylesheet" href="/style.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","{GA_ID}");</script>"""

    return f"""<!DOCTYPE html>
<html lang="en-GB">
<head>
{head}
</head>
<body>
{nav_html(True)}
  <main>
    <div class="page-hero">
      <div class="container">
        <div class="section-label">Blog</div>
        <h1>Useful guides for Excel, <em>Excel with AI</em>, and Flutter.</h1>
        <p>Practical tutorials for beginners to intermediate readers, with realistic office and small-business examples, current feature notes, and sensible next steps.</p>
      </div>
    </div>
    <section style="padding-top:40px">
      <div class="container">
        <div class="blog-grid">
          {''.join(cards)}
        </div>
      </div>
    </section>
    <div class="cta-banner">
      <div class="container">
        <div class="cta-inner reveal">
          <h2>Need structured Excel or Flutter learning?</h2>
          <p>My courses focus on practical workflows, not vague theory, so you can apply what you learn straight away.</p>
          <a href="/courses" class="btn-primary">Explore courses <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></a>
        </div>
      </div>
    </div>
  </main>
{footer_html()}
</body>
</html>
"""


def render_feed(all_posts: list[Post]) -> str:
    items = []
    for post in all_posts:
        items.append(
            "    <item>\n"
            f"      <title>{html_escape(post.title)}</title>\n"
            f"      <link>{post.url}</link>\n"
            f"      <guid isPermaLink=\"true\">{post.url}</guid>\n"
            f"      <description>{html_escape(post.description)}</description>\n"
            f"      <category>{html_escape(post.category)}</category>\n"
            f"      <author>{AUTHOR_EMAIL} ({AUTHOR_NAME})</author>\n"
            f"      <pubDate>{post.feed_date}</pubDate>\n"
            "    </item>\n"
        )
    last_build = all_posts[0].feed_date if all_posts else datetime.now().strftime("%a, %d %b %Y 00:00:00 +0530")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">\n'
        "  <channel>\n"
        f"    <title>{AUTHOR_NAME} — Blog</title>\n"
        f"    <link>{SITE_URL}/blog</link>\n"
        "    <description>Useful guides on Excel, Excel with AI, and Flutter by Sagnik Bhattacharya.</description>\n"
        "    <language>en-gb</language>\n"
        f"    <lastBuildDate>{last_build}</lastBuildDate>\n"
        f"    <atom:link href=\"{SITE_URL}/feed.xml\" rel=\"self\" type=\"application/rss+xml\"/>\n"
        "    <image>\n"
        f"      <url>{SITE_URL}/sagnik-bhattacharya.png</url>\n"
        f"      <title>{AUTHOR_NAME} — Blog</title>\n"
        f"      <link>{SITE_URL}/blog</link>\n"
        "    </image>\n"
        f"{''.join(items)}"
        "  </channel>\n"
        "</rss>\n"
    )


def update_sitemap(new_posts: list[Post]) -> str:
    existing = []
    if SITEMAP_FILE.exists():
        root = ET.fromstring(read_utf8(SITEMAP_FILE))
        namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        for loc in root.findall("sm:url/sm:loc", namespace):
            if loc.text:
                existing.append(loc.text.strip())
    wanted = existing[:]
    for post in new_posts:
        if post.url not in wanted:
            wanted.append(post.url)
    lines = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for url in wanted:
        lines.append("  <url>")
        lines.append(f"    <loc>{url}</loc>")
        lines.append("  </url>")
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def render_sources(sources: list[dict[str, str]]) -> str:
    if not sources:
        return ""
    items = "".join(
        f'<li><a href="{html_escape(source["url"])}" target="_blank" rel="noopener">{html_escape(source["label"])}</a></li>'
        for source in sources
    )
    return f"<h2>Official references</h2><p>These official references are useful if you need the product or framework documentation alongside this guide.</p><ul>{items}</ul>"


def render_body(post: dict[str, Any], new_lookup: dict[str, dict[str, Any]], old_lookup: dict[str, Post]) -> str:
    html_parts = []
    html_parts.append(render_paragraphs(post["intro"]))
    html_parts.append(make_notes_box(post.get("notes", [])))
    html_parts.append(section_html(post.get("quick_answer_heading", "Quick answer"), [post["quick_answer"]], post.get("use_when", [])))
    for section in post.get("sections", []):
        table_html = ""
        if section.get("table"):
            table = section["table"]
            table_html = render_table(table["headers"], table["rows"])
        html_parts.append(
            section_html(
                section["heading"],
                section.get("paragraphs"),
                section.get("bullets"),
                table_html or None,
                section.get("code"),
                section.get("code_language", ""),
            )
        )
    if post.get("example"):
        example = post["example"]
        table_html = ""
        if example.get("table"):
            table = example["table"]
            table_html = render_table(table["headers"], table["rows"])
        html_parts.append(
            section_html(
                example.get("heading", "Worked example"),
                example.get("paragraphs"),
                example.get("bullets"),
                table_html or None,
                example.get("code"),
                example.get("code_language", ""),
            )
        )
    if post.get("mistakes"):
        html_parts.append(section_html(post.get("mistakes_heading", "Common mistakes"), post.get("mistakes_intro"), post["mistakes"]))
    if post.get("instead"):
        instead = post["instead"]
        html_parts.append(section_html(instead.get("heading", "When to use something else"), instead.get("paragraphs"), instead.get("bullets")))
    for section in build_generated_sections(post, new_lookup, old_lookup):
        table_html = ""
        if section.get("table"):
            table = section["table"]
            table_html = render_table(table["headers"], table["rows"])
        html_parts.append(
            section_html(
                section["heading"],
                section.get("paragraphs"),
                section.get("bullets"),
                table_html or None,
                section.get("code"),
                section.get("code_language", ""),
            )
        )
    html_parts.append(render_sources(post.get("sources", [])))
    html_parts.append(render_related_section(post, new_lookup, old_lookup))
    return "".join(html_parts)


def create_post(post_def: dict[str, Any], new_lookup: dict[str, dict[str, Any]], old_lookup: dict[str, Post], published: date) -> Post:
    body_html = render_body(post_def, new_lookup, old_lookup)
    read_time = post_def.get("read_time") or estimate_read_time(body_html)
    image_src = f"/blog/images/{post_def['slug']}-sagnik-bhattacharya-coding-liquids.jpg"
    category = post_def["category"]
    return Post(
        slug=post_def["slug"],
        title=britishise(post_def["title"]),
        category=category,
        description=britishise(post_def["description"]),
        keywords=[britishise(item) for item in post_def["keywords"]],
        body_html=britishise(body_html),
        published=published,
        modified=published,
        read_time=read_time,
        image_src=image_src,
        image_alt=britishise(post_def["image_alt"]),
        cover_hook=britishise(post_def["cover_hook"]),
        cover_cta=britishise(post_def["cover_cta"]),
        cover_keywords=[britishise(item) for item in post_def["cover_keywords"]],
        cover_cue=britishise(post_def["cover_cue"]),
        related_new=post_def["related_new"],
        related_old=post_def["related_old"],
        primary_intent=post_def["primary_intent"],
        search_type=post_def["search_type"],
        notes=[britishise(item) for item in post_def.get("notes", [])],
        sources=post_def.get("sources", []),
        intro_text=britishise(tidy_spaces(strip_tags(" ".join(post_def["intro"][:1])))),
        category_section=SECTION_META[category]["section"],
        in_scope=True,
    )


NEW_POSTS: list[dict[str, Any]] = [
    {
        "slug": "agent-mode-in-excel",
        "title": "Agent Mode in Excel: What It Does, What It Can’t, and Who Should Use It",
        "category": "AI + Excel",
        "description": "Learn what Agent Mode in Excel actually does, where it saves time, where it still needs human review, and which teams will benefit most.",
        "keywords": ["Agent Mode in Excel", "Excel AI agent", "Copilot in Excel", "Excel automation", "Excel with AI"],
        "primary_intent": "Understand whether Agent Mode in Excel is worth using for real spreadsheet work.",
        "search_type": "trend",
        "intro": [
            "Agent Mode in Excel sounds bigger than another prompt box, and in practical use it is. As of 1 April 2026, Microsoft is positioning it as a guided way to let Excel inspect a workbook, reason through a task, and take several steps on your behalf instead of waiting for one instruction at a time.",
            "That does not mean it can replace spreadsheet judgement. If you still need the basics first, read <a href=\"/blog/getting-started-copilot-excel\">my Copilot in Excel starter guide</a>. This article is for the next question: when Agent Mode is the right tool, when it is not, and how to use it without creating hidden risk."
        ],
        "notes": [
            "Availability, licensing, model access, and exact capabilities can change quickly. Treat this guide as current as of 1 April 2026 and verify the official Microsoft notes before rolling it out widely."
        ],
        "quick_answer": "Agent Mode is most useful when you need Excel to carry out a short sequence of actions across a workbook, such as exploring a dataset, preparing a report, or iterating through a multi-step question. It is less useful for tightly controlled finance models, regulated workbooks, or any sheet where one wrong structural change would be expensive.",
        "use_when": [
            "You need help exploring a workbook, not merely generating one formula.",
            "Your data is already in sensible tables or ranges and you can review the output afterwards.",
            "You want to reduce busywork in weekly reporting, operations tracking, or ad hoc analysis.",
        ],
        "sections": [
            {
                "heading": "What Agent Mode does well",
                "paragraphs": [
                    "In normal chat-style Excel AI, you ask for one outcome and then prompt again for the next one. Agent Mode is better at chained tasks: identify the relevant data, inspect patterns, choose a sensible approach, and produce a result with a bit less hand-holding.",
                    "That makes it attractive for office workflows such as cleaning a sales export, building a first-pass summary, or answering a question from a manager who wants a quick view before a meeting. It overlaps with <a href=\"/blog/analyst-vs-agent-mode-vs-copilot-chat\">Analyst mode and Copilot chat</a>, but the best fit depends on how much step-by-step initiative you want Excel to take."
                ],
                "bullets": [
                    "Workbook exploration when you are new to the file.",
                    "Pattern finding and first-pass summaries.",
                    "Drafting actions across related sheets when the structure is already tidy.",
                ],
            },
            {
                "heading": "Where the limits still matter",
                "paragraphs": [
                    "The biggest risk is over-trust. Agent Mode can still misunderstand headings, work from partial context, or make a structurally valid change that is still the wrong business decision. That is why it should support the analyst, not replace the analyst.",
                    "In practice, teams get the best results when they treat it as a supervised assistant: ask it to explain what it plans to do, let it operate on clean tables, and review any formulas, workbook changes, or narrative summaries before sharing them."
                ],
                "table": {
                    "headers": ["Situation", "Good fit for Agent Mode?", "Why"],
                    "rows": [
                        ["Weekly sales summary from a clean table", "Yes", "The task is bounded and easy to review."],
                        ["Month-end finance model with board reporting", "Usually no", "One silent assumption can change the story."],
                        ["Explaining an inherited workbook", "Often yes", "It can help surface structure quickly before you inspect it."],
                    ],
                },
            },
            {
                "heading": "A safe workflow for real teams",
                "paragraphs": [
                    "Start by asking Agent Mode to describe the workbook and name the tables or ranges it plans to use. Then narrow the job. Instead of saying “fix this workbook”, ask for one outcome such as “summarise regional sales by quarter and explain any obvious outliers”.",
                    "After each result, check the source range, any formula logic, and whether the numbers agree with manual spot checks. If the workbook itself is the problem, <a href=\"/blog/format-data-for-copilot-excel\">formatting the data properly for Copilot</a> often helps more than writing a better prompt."
                ],
                "bullets": [
                    "Ask what data it is using before you ask for conclusions.",
                    "Keep the task narrow enough that you can review it quickly.",
                    "Save or duplicate the workbook before allowing structural edits.",
                ],
            },
        ],
        "example": {
            "heading": "Worked example: an operations report",
            "paragraphs": [
                "Imagine a small business with one workbook for orders, late shipments, refunds, and customer notes. The operations manager needs a Friday summary for the leadership call.",
                "Agent Mode is useful here because the manager is not asking for a perfect model. They need a fast first pass: which categories are slipping, which regions are generating the most refunds, and what changed compared with last week."
            ],
            "bullets": [
                "Step 1: ask Agent Mode to identify the main tables and the date columns.",
                "Step 2: ask for a summary of late shipments by region and product category.",
                "Step 3: ask it to suggest likely causes based on adjacent notes, then verify manually before sharing.",
            ],
        },
        "mistakes": [
            "Using it on messy ranges and expecting the model to infer the structure perfectly.",
            "Letting it change a production workbook before saving a copy.",
            "Treating its explanation as proof instead of checking the workbook logic yourself.",
        ],
        "instead": {
            "heading": "When to use something else",
            "paragraphs": [
                "Use regular Copilot chat for one-off questions and lighter prompting. Use <a href=\"/blog/python-in-excel-beginners\">Python in Excel</a> when you need reproducible analysis rather than conversational exploration. For formula-specific help, a narrower guide such as <a href=\"/blog/generate-single-cell-formulas-copilot-excel\">single-cell formulas with Copilot</a> will usually get you to the answer faster."
            ],
        },
        "related_new": ["analyst-vs-agent-mode-vs-copilot-chat", "format-data-for-copilot-excel", "review-ai-generated-excel-formulas", "claude-agent-mode-excel"],
        "related_old": ["getting-started-copilot-excel"],
        "related_intro": "These next reads help you decide whether Agent Mode is the right AI surface, and how to keep the work reviewable.",
        "cover_hook": "Use workbook-level AI when you need a guided sequence, not just one formula.",
        "cover_cta": "Use Agent Mode Safely",
        "cover_keywords": ["Agent", "Workbook", "Review"],
        "cover_cue": "AI workspace panels, workbook actions, and guided-analysis cues",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Agent Mode in Excel, with workbook action panels and supervised AI workflow cues.",
        "sources": [SOURCES["agent_mode"], SOURCES["copilot_excel"]],
    },
    {
        "slug": "groupby-function-excel",
        "title": "GROUPBY Function in Excel: Formula-Based Summaries Without a Pivot Table",
        "category": "Excel",
        "description": "Learn how GROUPBY works in Excel, when it beats a PivotTable, and how to use it for dynamic summaries that stay close to the source data.",
        "keywords": ["GROUPBY Excel", "GROUPBY function", "Excel dynamic arrays", "Excel summaries", "PivotTable alternative"],
        "primary_intent": "Learn how to use GROUPBY for dynamic formula-based summaries.",
        "search_type": "hot-evergreen",
        "intro": [
            "GROUPBY is one of the most interesting modern Excel functions because it changes where summarising work happens. Instead of jumping straight into a PivotTable, you can stay inside the grid and build a live summary formula that spills results where you want them.",
            "That matters for anyone who likes formula-driven models, reusable templates, or report tabs that need to update automatically. If you already know <a href=\"/blog/mastering-pivot-tables\">PivotTables</a>, think of GROUPBY as a more composable option for lighter summaries."
        ],
        "quick_answer": "Use GROUPBY when you want a summary table that updates with the source data and remains part of your formula model. It is especially useful for dashboards, control sheets, and lightweight reporting where a PivotTable would feel heavy or awkward to position.",
        "use_when": [
            "You want a dynamic summary next to other formulas.",
            "You need the result to spill into a report area automatically.",
            "You prefer one formula over a separate PivotTable object.",
        ],
        "sections": [
            {
                "heading": "How GROUPBY changes the workflow",
                "paragraphs": [
                    "A PivotTable creates a separate reporting object. GROUPBY returns an array result in cells. That sounds like a small distinction, but it changes how easy it is to combine the summary with <a href=\"/blog/choosecols-chooserows-take-drop-excel\">modern array functions</a>, feed it into charts, or layer extra logic around it.",
                    "For small teams, this often means simpler workbooks. You can keep the raw data in one Excel table, write one spill formula on a report sheet, and let the summary refresh itself when the table grows."
                ],
            },
            {
                "heading": "Start with the simplest useful pattern",
                "paragraphs": [
                    "The most common use is grouping one field and aggregating one value field. For example, you might summarise total revenue by region from a sales table.",
                    "The exact syntax can evolve, so use the official help pane in your version of Excel. The underlying habit matters more: reference a clean table, choose a grouping field, choose a value field, and make the aggregation obvious."
                ],
                "code": "=GROUPBY(Sales[Region], Sales[Revenue], SUM)",
                "code_language": "text",
                "bullets": [
                    "Keep the source data in an Excel table so new rows flow into the formula.",
                    "Name the output area clearly so charts and commentary can reference it.",
                    "Use one simple summary first, then layer sorting or extra dimensions afterwards.",
                ],
            },
            {
                "heading": "Where GROUPBY is better than a PivotTable",
                "paragraphs": [
                    "GROUPBY shines when you want the summary to behave like any other formula result. You can nest it, wrap it, sort it, or place it exactly where you need it in a model or dashboard. That makes it easier to combine with <a href=\"/blog/map-scan-reduce-excel\">MAP, SCAN, and REDUCE</a> or feed it into a spill-based reporting layout.",
                    "It is also easier to keep version control over the logic because the summary rule is visible in the formula bar, not hidden behind multiple field settings."
                ],
                "table": {
                    "headers": ["Task", "GROUPBY", "PivotTable"],
                    "rows": [
                        ["Spill summary into a custom dashboard area", "Excellent", "Possible, but less flexible"],
                        ["Fast ad hoc exploration with drag-and-drop", "Fine", "Excellent"],
                        ["Combining with other formulas", "Excellent", "Awkward"],
                    ],
                },
            },
        ],
        "example": {
            "heading": "Worked example: a monthly sales sheet",
            "paragraphs": [
                "A small wholesale team stores every order in one table with columns for month, sales rep, region, revenue, and margin. They want a report sheet that updates itself when fresh orders are pasted into the source table.",
                "GROUPBY lets them summarise revenue by region in one spill formula, then use a second formula to sort the result and a third formula to display only the top regions on the dashboard."
            ],
            "bullets": [
                "Source table on one sheet.",
                "GROUPBY result on the report sheet.",
                "Chart linked to the spill range so the visual updates automatically.",
            ],
        },
        "mistakes": [
            "Using messy ranges instead of a clean Excel table.",
            "Trying to build a complex multi-stage summary before the first simple version works.",
            "Comparing GROUPBY to PivotTables as if one must always replace the other.",
        ],
        "instead": {
            "paragraphs": [
                "Use a PivotTable when you want quick drag-and-drop exploration or more familiar field controls for a wider team. If you want a direct comparison, the next best read is <a href=\"/blog/groupby-vs-pivottable-excel\">GROUPBY vs PivotTable</a>."
            ],
        },
        "related_new": ["groupby-vs-pivottable-excel", "pivotby-function-excel", "choosecols-chooserows-take-drop-excel"],
        "related_old": ["mastering-pivot-tables"],
        "cover_hook": "Build summaries with formulas so reports stay live, flexible, and easier to reuse.",
        "cover_cta": "Use GROUPBY Better",
        "cover_keywords": ["GROUPBY", "Summary", "Spill"],
        "cover_cue": "dynamic summary grids, grouped rows, and formula-led reporting cues",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for the GROUPBY function in Excel, with spill summaries and grouped reporting visuals.",
        "sources": [SOURCES["groupby"]],
    },
    {
        "slug": "flutter-widget-previewer",
        "title": "Flutter Widget Previewer: Real-Time UI Iteration Without Running the Full App",
        "category": "Flutter",
        "description": "Learn what Flutter Widget Previewer is good at, where it saves time, and how to fold it into a production workflow without skipping real testing.",
        "keywords": ["Flutter Widget Previewer", "Flutter preview", "Flutter developer workflow", "Flutter UI iteration", "Flutter tooling"],
        "primary_intent": "Understand how to use Widget Previewer productively in Flutter workflows.",
        "search_type": "trend",
        "intro": [
            "Widget Previewer is one of those tooling improvements that sounds small until you use it for a week. The value is simple: you can iterate on a widget in isolation without constantly rebuilding the whole app or navigating to the screen that contains it.",
            "That saves a surprising amount of friction when you are adjusting spacing, states, copy, or theme behaviour. It does not replace real-device testing, but it can remove a lot of slow feedback loops from day-to-day UI work."
        ],
        "notes": [
            "Tooling details can shift between Flutter and IDE releases. Treat this guide as current as of 1 April 2026 and check the latest Flutter tooling notes if your setup behaves differently."
        ],
        "quick_answer": "Use Widget Previewer to shorten the edit-check-adjust loop for individual widgets and common states. Keep using emulator, device, and integration testing for navigation, lifecycle, performance, accessibility, and cross-screen behaviour.",
        "use_when": [
            "You are tuning layout, state variants, or theme behaviour on one widget.",
            "You want faster visual feedback than a full app run can give you.",
            "You still plan to verify the result in the actual app afterwards.",
        ],
        "sections": [
            {
                "heading": "Why it is useful in real teams",
                "paragraphs": [
                    "The gain is not only speed. It is focus. A preview encourages you to think in states: loading, empty, error, compact, dense, long text, dark theme, accessibility scaling. That is a healthier habit than only checking the happy path on one route.",
                    "It also pairs well with a feature-first structure because isolated widgets become easier to reason about, document, and test. If architecture is your next bottleneck, <a href=\"/blog/flutter-app-architecture-2026\">Flutter app architecture in 2026</a> is the logical follow-up."
                ],
            },
            {
                "heading": "Where Widget Previewer saves the most time",
                "paragraphs": [
                    "The best use cases are the ones that normally force repetitive setup: open the app, navigate, seed data, reach the right state, change one padding value, and repeat. Previewing a widget short-circuits that loop."
                ],
                "bullets": [
                    "Checking how long text wraps on smaller widths.",
                    "Comparing loading, success, and error states side by side.",
                    "Testing dark theme and text scaling without bootstrapping the whole route tree.",
                ],
            },
            {
                "heading": "What it does not replace",
                "paragraphs": [
                    "A preview does not tell you whether navigation works, whether state wiring is correct, or whether the screen still feels right once the full page is assembled. Keep real verification in place.",
                    "Use preview for local iteration, then back it up with widget tests, integration tests, and device checks."
                ],
            },
        ],
        "example": {
            "heading": "Worked example: a reusable order card",
            "paragraphs": [
                "Imagine an order card that appears in a list, in search results, and inside an admin dashboard. Without preview, you keep relaunching just to inspect the same component in slightly different states.",
                "With a preview, you can create states for delayed orders, refunded orders, VIP orders, and very long customer names, then settle spacing and hierarchy before returning to the app."
            ],
        },
        "mistakes": [
            "Treating a neat preview as proof that the feature is finished.",
            "Previewing only the happy path and missing empty or error states.",
            "Skipping device checks for touch targets, performance, and text scaling.",
        ],
        "instead": {
            "paragraphs": [
                "If your main problem is route structure rather than UI iteration, go to <a href=\"/blog/go-router-flutter-deep-linking\">go_router deep linking</a>. If the real pain is broad layout adaptation, <a href=\"/blog/responsive-flutter-ui-all-screens\">responsive Flutter UI</a> is the better next read."
            ],
        },
        "related_new": ["flutter-app-architecture-2026", "responsive-flutter-ui-all-screens", "flutter-testing-strategy-2026", "create-with-ai-flutter"],
        "related_old": ["flutter-state-management"],
        "cover_hook": "Shorten the UI feedback loop without relaunching the whole app every time.",
        "cover_cta": "Preview Widgets Faster",
        "cover_keywords": ["Preview", "Widget", "Speed"],
        "cover_cue": "isolated UI cards, live preview panes, and fast-iteration cues",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Flutter Widget Previewer, with isolated UI previews and rapid-iteration visuals.",
        "sources": [SOURCES["widget_previewer"]],
    },
    {
        "slug": "claude-agent-mode-excel",
        "title": "Use Claude With Agent Mode in Excel: Setup, Limits, and Best Workflows",
        "category": "AI + Excel",
        "description": "A practical guide to using Claude with Agent Mode in Excel, including setup expectations, current limits, and the workflows where it helps most.",
        "keywords": ["Claude Agent Mode Excel", "Claude in Excel", "Agent Mode Claude", "Excel AI workflows", "Claude Excel setup"],
        "primary_intent": "Understand how Claude fits into Agent Mode in Excel and where it is useful.",
        "search_type": "trend",
        "intro": [
            "When people hear that Claude can be used with Agent Mode in Excel, they often assume the hard part is prompt writing. In practice, the hard part is earlier: access, governance, clean data, and choosing the right task.",
            "If those pieces are wrong, the model choice barely matters. This guide focuses on the practical side. If you need the wider context first, start with <a href=\"/blog/agent-mode-in-excel\">Agent Mode in Excel</a>."
        ],
        "notes": [
            "As of 1 April 2026, tenant-level settings and permitted AI providers can affect access. Check with your Microsoft 365 administrators before promising this workflow to a team."
        ],
        "quick_answer": "Claude with Agent Mode is most useful when you need strong reasoning over a clearly structured workbook and you are prepared to review the result. It is not a shortcut around data preparation, policy controls, or workbook review.",
        "use_when": [
            "Your organisation has enabled the relevant provider access.",
            "You need workbook reasoning more than raw formula generation.",
            "You can keep the task grounded in clean, reviewable tables.",
        ],
        "sections": [
            {
                "heading": "Start with access and governance",
                "paragraphs": [
                    "The first check is administrative, not technical. If provider access is not enabled or the workbook is inappropriate for the policy environment, clever prompts will not save the workflow.",
                    "Confirm who can access the feature, which workbooks are in scope, and what review is expected before anything is shared."
                ],
            },
            {
                "heading": "What Claude is good at here",
                "paragraphs": [
                    "Claude tends to be most useful when the workbook question is multi-step and explanation matters. Think: inspect the sales sheet, identify the outlier quarters, compare them with the refund table, then explain likely drivers.",
                    "That makes it a better fit for reasoning and narrative analysis than for blind workbook edits."
                ],
            },
            {
                "heading": "The limits that change the outcome",
                "paragraphs": [
                    "Claude still depends on the workbook context it can interpret. If the data is not in proper tables, if headings are inconsistent, or if the workbook mixes several purposes in one sheet, quality drops quickly.",
                    "That is why <a href=\"/blog/format-data-for-copilot-excel\">formatting data for Copilot</a> is not cosmetic. It is part of the reasoning workflow."
                ],
            },
        ],
        "example": {
            "heading": "Worked example: a customer retention workbook",
            "paragraphs": [
                "A subscription business keeps exports for sign-ups, renewals, cancellations, discounts, and support issues. The operations lead wants a quick explanation of why one region is underperforming.",
                "Claude with Agent Mode can help inspect the tables, surface likely drivers, and produce a first narrative. The analyst still validates the numbers before the story leaves the workbook."
            ],
        },
        "mistakes": [
            "Testing it on badly structured sheets and blaming the model alone.",
            "Ignoring the admin and governance layer.",
            "Using it for high-stakes workbook edits without a saved copy and manual review.",
        ],
        "instead": {
            "paragraphs": [
                "If the workbook question is mostly formula creation, <a href=\"/blog/chatgpt-vs-claude-vs-copilot-vs-gemini-excel\">compare the main AI tools for Excel</a>. If the task is broader workbook action, go back to <a href=\"/blog/agent-mode-in-excel\">the Agent Mode overview</a>."
            ],
        },
        "related_new": ["agent-mode-in-excel", "format-data-for-copilot-excel", "chatgpt-vs-claude-vs-copilot-vs-gemini-excel"],
        "related_old": ["claude-ai-excel-formulas"],
        "cover_hook": "Claude helps most when workbook reasoning matters and the data is already reviewable.",
        "cover_cta": "Use Claude Carefully",
        "cover_keywords": ["Claude", "Reasoning", "Excel"],
        "cover_cue": "AI reasoning panels, workbook summaries, and controlled-analysis cues",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for using Claude with Agent Mode in Excel, with reasoning panels and workbook analysis visuals.",
        "sources": [SOURCES["claude_agent"], SOURCES["agent_mode"]],
    },
    {
        "slug": "pivotby-function-excel",
        "title": "PIVOTBY Function in Excel: Build Pivot-Style Reports With a Formula",
        "category": "Excel",
        "description": "Learn when to use PIVOTBY in Excel, how it differs from PivotTables, and how to create report-style summaries directly in formulas.",
        "keywords": ["PIVOTBY Excel", "PIVOTBY function", "Pivot formula Excel", "Excel report formulas", "dynamic arrays Excel"],
        "primary_intent": "Learn how PIVOTBY works and when it is a better fit than a PivotTable.",
        "search_type": "hot-evergreen",
        "intro": [
            "If GROUPBY feels like the formula replacement for one-dimensional summaries, PIVOTBY is the natural next step for report-style summaries that resemble a PivotTable. It gives you the logic of a cross-tab without forcing you into a separate reporting object.",
            "That matters when you want a formula-driven report tab that updates cleanly and sits comfortably beside the rest of your workbook logic."
        ],
        "quick_answer": "Use PIVOTBY when you want row and column groupings in a dynamic formula output. It is especially useful for compact reporting grids, spill-friendly dashboards, and workbooks where formula transparency matters more than drag-and-drop exploration.",
        "use_when": [
            "You need both row and column groupings in one live formula result.",
            "You want the output to sit exactly where your report template expects it.",
            "You are already comfortable with modern Excel array functions.",
        ],
        "sections": [
            {
                "heading": "Why PIVOTBY is different from a PivotTable",
                "paragraphs": [
                    "A PivotTable is brilliant for exploration. PIVOTBY is better when you already know the reporting question and want the result to behave like part of the model.",
                    "You can place it, reference it, and combine it with other formulas more naturally."
                ],
            },
            {
                "heading": "Think in report questions first",
                "paragraphs": [
                    "The simplest mental model is this: what should appear down the left, what should appear across the top, and what number should sit in the middle of each intersection? Once those three things are clear, the formula becomes much easier to reason about."
                ],
                "bullets": [
                    "Rows: the categories you want to compare.",
                    "Columns: the second dimension you want to break them by.",
                    "Values: the measure you want to aggregate.",
                ],
            },
            {
                "heading": "Where it is especially useful",
                "paragraphs": [
                    "PIVOTBY is ideal for compact reporting tabs: sales by region and month, spend by department and quarter, tickets by priority and team, or stock by warehouse and product family.",
                    "Because the output is a formula result, it is easier to control alongside other spill ranges than a PivotTable would be."
                ],
            },
        ],
        "example": {
            "heading": "Worked example: sales by region and month",
            "paragraphs": [
                "A business development lead wants one sheet that shows monthly revenue across the top and region down the side. The data lives in a single sales table that grows every week.",
                "PIVOTBY lets them create the report grid with one formula, keep the output next to commentary and targets, and link a chart to the result without maintaining a separate PivotTable."
            ],
        },
        "mistakes": [
            "Using untidy source data with inconsistent category values.",
            "Building a huge report grid before testing one small version first.",
            "Assuming it must replace PivotTables rather than complement them.",
        ],
        "instead": {
            "paragraphs": [
                "Use a PivotTable when exploration is the main goal and the audience is more comfortable with field lists than formulas. Use GROUPBY when you only need one grouping dimension rather than a cross-tab."
            ],
        },
        "related_new": ["groupby-function-excel", "groupby-vs-pivottable-excel", "excel-tables-best-practices"],
        "related_old": ["mastering-pivot-tables"],
        "cover_hook": "Create a live cross-tab report without leaving the formula layer.",
        "cover_cta": "Build With PIVOTBY",
        "cover_keywords": ["Cross-tab", "Report", "Formula"],
        "cover_cue": "grid reports, row-column summaries, and formula-based pivot visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for the PIVOTBY function in Excel, with cross-tab report grids and formula-led summary visuals.",
        "sources": [],
    },
    {
        "slug": "create-with-ai-flutter",
        "title": "Create With AI in Flutter: Gemini CLI, MCP, and the AI Toolkit Explained",
        "category": "Flutter",
        "description": "Learn how Flutter’s AI tooling story fits together, including Gemini CLI, MCP, and the AI Toolkit, without turning your app into AI-themed fluff.",
        "keywords": ["Flutter AI toolkit", "Gemini CLI Flutter", "MCP Flutter", "Create with AI Flutter", "Flutter AI workflow"],
        "primary_intent": "Understand Flutter’s current AI tooling story and where each piece fits.",
        "search_type": "trend",
        "intro": [
            "Flutter’s create-with-AI story can feel messy because several pieces show up at once: Gemini CLI, MCP, the AI Toolkit, IDE integrations, and the wider question of whether you are generating code, wiring model calls, or building AI features into the app itself.",
            "The useful way to think about it is to separate three jobs: speeding up developer work, integrating model-backed features into the product, and keeping the result maintainable after the first demo."
        ],
        "notes": [
            "Tool names and recommended workflows in Flutter’s AI documentation are evolving. Treat this overview as current as of 1 April 2026 and verify the latest docs before you standardise a team workflow."
        ],
        "quick_answer": "Use Gemini CLI or comparable tooling to speed up local development tasks, use MCP where you need a cleaner bridge between tools and models, and use Flutter’s AI Toolkit or platform integrations when the app itself needs AI features. Do not treat all three as the same problem.",
        "use_when": [
            "You want faster coding and debugging loops without pretending AI replaces engineering.",
            "You are designing actual product features that use models or agents.",
            "You need a workflow teams can review, test, and maintain.",
        ],
        "sections": [
            {
                "heading": "Separate developer tooling from product architecture",
                "paragraphs": [
                    "This is the mistake most teams make first: they bundle code generation, backend AI integration, and in-app user features into one vague AI strategy. That makes planning worse, not better.",
                    "A healthier split is simple. Developer tooling helps you write or inspect code faster. Product architecture decides how the app talks to models or services. UI and policy decisions shape what the user actually sees."
                ],
            },
            {
                "heading": "Where Gemini CLI and MCP fit",
                "paragraphs": [
                    "Gemini CLI fits the developer-assistance side: local iteration, code scaffolding, debugging, or accelerating routine implementation. MCP matters when you want a clearer tool interface and better boundaries around how model-driven workflows reach project context or external systems."
                ],
                "bullets": [
                    "Developer speed-up: drafts, tests, refactors, and documentation.",
                    "Controlled tool access around model workflows.",
                    "A cleaner path from experimentation to team-level process.",
                ],
            },
            {
                "heading": "What the AI Toolkit is best for",
                "paragraphs": [
                    "The AI Toolkit matters most when you are moving from use AI while coding to ship an app feature that uses AI. It helps you think about the product surface, not merely the engineer surface.",
                    "That distinction matters because shipping AI means handling loading states, error states, abuse cases, privacy, cost, and degraded behaviour."
                ],
            },
        ],
        "example": {
            "heading": "Worked example: adding AI to a support app",
            "paragraphs": [
                "Suppose you are building a support dashboard that suggests draft replies. Gemini CLI can speed up implementation, but the AI Toolkit and your app structure matter more once the feature exists.",
                "You still need prompt inputs, rate limiting, fallbacks, review controls, analytics, and a clean separation between UI, service layer, and data handling."
            ],
        },
        "mistakes": [
            "Treating every AI tool as the same category of decision.",
            "Letting generated code ignore the existing app structure.",
            "Shipping AI features without product-level fallback behaviour.",
        ],
        "instead": {
            "paragraphs": [
                "If your issue is mostly app structure, go to <a href=\"/blog/flutter-app-architecture-2026\">architecture</a>. If your bottleneck is UI speed, <a href=\"/blog/flutter-widget-previewer\">Widget Previewer</a> may help more than another AI tool."
            ],
        },
        "related_new": ["flutter-widget-previewer", "flutter-app-architecture-2026", "flutter-testing-strategy-2026"],
        "related_old": ["flutter-state-management"],
        "cover_hook": "Use AI where it shortens real engineering work, not where it adds vague complexity.",
        "cover_cta": "Ship AI Sensibly",
        "cover_keywords": ["AI Toolkit", "MCP", "Flutter"],
        "cover_cue": "tooling cards, AI workflow nodes, and production-minded Flutter cues",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for creating with AI in Flutter, with tooling nodes and production-minded AI workflow visuals.",
        "sources": [SOURCES["ai_overview"]],
    },
    {
        "slug": "copilot-function-excel",
        "title": "COPILOT Function in Excel: Syntax, Use Cases, Limits, and Risks",
        "category": "AI + Excel",
        "description": "Learn what the COPILOT function in Excel is actually for, where it helps, what its preview limits mean, and how to review the output properly.",
        "keywords": ["COPILOT function Excel", "Excel COPILOT function", "Excel AI formula", "Copilot in Excel", "AI formulas Excel"],
        "primary_intent": "Understand what the COPILOT function does and how to use it carefully.",
        "search_type": "trend",
        "intro": [
            "The COPILOT function is one of the clearest signals that Excel’s AI direction is moving deeper into the grid. Instead of staying only in a side panel, AI can now sit inside worksheet logic itself and produce values directly in cells.",
            "That is powerful, but it also changes the review burden. A side-panel answer is easy to question. A cell result can disappear into a model very quickly if you do not build the right checking habits."
        ],
        "notes": [
            "As of 1 April 2026, COPILOT function behaviour and availability can still depend on channel, licensing, and rollout status. Confirm the current Microsoft documentation before you standardise it for a team."
        ],
        "quick_answer": "The COPILOT function is useful for bounded AI assistance inside worksheet logic, especially when you want a result in a cell rather than a side conversation. It is not a substitute for deterministic formulas in any workflow that must be fully auditable or reproducible.",
        "use_when": [
            "You need AI assistance directly in worksheet output.",
            "The task is advisory, classificatory, or interpretive rather than purely deterministic.",
            "You can review and document where the AI-derived values are being used.",
        ],
        "sections": [
            {
                "heading": "Where it can genuinely help",
                "paragraphs": [
                    "The strongest use cases are the ones where traditional formulas are possible but awkward, or where the task involves interpretation: classifying free-text comments, drafting a short summary, or converting an informal request into a structured answer."
                ],
            },
            {
                "heading": "Why review matters more than syntax",
                "paragraphs": [
                    "If an AI-produced value feeds a metric, a filter, or a business rule, someone needs to know where that value came from and how trustworthy it is.",
                    "Label the column clearly, sample the output, and use a manual review pass before the results affect dashboards or decisions."
                ],
                "bullets": [
                    "Label AI-derived columns clearly.",
                    "Review a sample before filling the function down a whole table.",
                    "Keep the prompt objective and specific enough to reduce drift.",
                ],
            },
            {
                "heading": "The real risks",
                "paragraphs": [
                    "The bigger risk is false confidence. A neat result in a cell feels more official than a paragraph in chat, so teams can accidentally treat it like a normal formula even when it behaves differently."
                ],
            },
        ],
        "example": {
            "heading": "Worked example: classifying support comments",
            "paragraphs": [
                "A support team has 1,200 comments from a customer survey. They want a quick first-pass label for each row: billing, delivery, product quality, or account issue.",
                "The COPILOT function can help create that first label column, but the team should still sample the outputs and avoid treating the result as final without review."
            ],
        },
        "mistakes": [
            "Using AI-derived cell values in a model without labelling them clearly.",
            "Replacing deterministic logic with the COPILOT function simply because it feels faster.",
            "Ignoring availability and rollout caveats in team documentation.",
        ],
        "instead": {
            "paragraphs": [
                "If you need a formula written for you, <a href=\"/blog/generate-single-cell-formulas-copilot-excel\">single-cell formula generation</a> is the better topic. If you need a broader comparison of AI tools for spreadsheet work, go to <a href=\"/blog/chatgpt-vs-claude-vs-copilot-vs-gemini-excel\">the 2026 comparison guide</a>."
            ],
        },
        "related_new": ["generate-single-cell-formulas-copilot-excel", "review-ai-generated-excel-formulas", "chatgpt-vs-claude-vs-copilot-vs-gemini-excel"],
        "related_old": ["copilot-data-analysis"],
        "cover_hook": "Use AI in the grid only when the result stays reviewable and clearly labelled.",
        "cover_cta": "Review COPILOT Outputs",
        "cover_keywords": ["COPILOT", "Cells", "Review"],
        "cover_cue": "spreadsheet cells, AI result cards, and worksheet-review cues",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for the COPILOT function in Excel, with AI-filled cells and review-focused spreadsheet visuals.",
        "sources": [SOURCES["copilot_function"], SOURCES["copilot_excel"]],
    },
    {
        "slug": "groupby-vs-pivottable-excel",
        "title": "GROUPBY vs PivotTable in Excel: When Formula Summaries Beat the Ribbon",
        "category": "Excel",
        "description": "Compare GROUPBY and PivotTables in Excel so you can choose the right summary tool for dashboards, recurring reports, and ad hoc analysis.",
        "keywords": ["GROUPBY vs PivotTable", "Excel summaries", "PivotTable alternative", "GROUPBY Excel", "Excel reporting"],
        "primary_intent": "Choose between GROUPBY and PivotTables for summary work in Excel.",
        "search_type": "evergreen",
        "intro": [
            "This is not a new-versus-old fight. GROUPBY and PivotTables solve overlapping problems, but they shine in different workflows. The right choice depends less on ideology and more on how you build reports, who maintains the workbook, and how much formula control you want.",
            "If you only remember one thing from this guide, remember this: use PivotTables for fast exploration, and lean towards GROUPBY when the summary needs to live inside a formula-driven model."
        ],
        "quick_answer": "PivotTables are usually better for ad hoc analysis and drag-and-drop exploration. GROUPBY is usually better when the result must spill into a report, combine with other formulas, and remain visible as logic in the workbook.",
        "use_when": [
            "Use PivotTables for quick exploration and broad team familiarity.",
            "Use GROUPBY for dynamic, formula-led report tabs.",
            "Use both when exploration happens first and a cleaner formula report comes later.",
        ],
        "sections": [
            {
                "heading": "The biggest practical difference",
                "paragraphs": [
                    "A PivotTable is an object with fields and layout controls. GROUPBY is a formula result. That changes how you maintain the workbook. Formula models are easier to inspect in-line, while PivotTables are easier for many casual Excel users to build from scratch."
                ],
            },
            {
                "heading": "When GROUPBY wins",
                "paragraphs": [
                    "GROUPBY wins when the summary has to sit in a precise place, feed another spill formula, or power a dashboard without extra manual positioning. It is also easier to version conceptually because the rule is visible in the formula bar."
                ],
            },
            {
                "heading": "When PivotTables still win",
                "paragraphs": [
                    "PivotTables still dominate when the question is open-ended. If you want to drag fields around, regroup dimensions quickly, or hand the workbook to someone who knows classic Excel but not modern array formulas, PivotTables remain the safer choice."
                ],
            },
        ],
        "example": {
            "heading": "Worked example: two stages of the same report",
            "paragraphs": [
                "An analyst receives a messy sales export and first uses a PivotTable to explore regional variance, seasonality, and product mix. Once the report question stabilises, they rebuild the final summary with GROUPBY so the output sits neatly inside a template sheet and updates automatically next month."
            ],
        },
        "mistakes": [
            "Choosing one tool as a matter of identity rather than workflow.",
            "Expecting GROUPBY to replace drag-and-drop exploration.",
            "Keeping a fragile manual report when a formula summary would be easier to maintain.",
        ],
        "instead": {
            "paragraphs": [
                "If you already know you want formula-led summaries, read <a href=\"/blog/groupby-function-excel\">the GROUPBY guide</a>. If you need cross-tab output rather than one grouped list, go to <a href=\"/blog/pivotby-function-excel\">PIVOTBY</a>."
            ],
        },
        "related_new": ["groupby-function-excel", "pivotby-function-excel", "excel-tables-best-practices", "fix-spill-errors-excel"],
        "related_old": ["mastering-pivot-tables"],
        "cover_hook": "Choose the summary method that matches the workflow, not the trend.",
        "cover_cta": "Pick The Right Summary Tool",
        "cover_keywords": ["GROUPBY", "PivotTable", "Choice"],
        "cover_cue": "formula summaries, pivot layouts, and side-by-side decision visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for GROUPBY vs PivotTable in Excel, with formula summaries and comparison visuals.",
        "sources": [SOURCES["groupby"]],
    },
    {
        "slug": "flutter-web-skwasm-vs-canvaskit",
        "title": "Flutter Web in 2026: skwasm vs CanvasKit vs WebAssembly Builds",
        "category": "Flutter",
        "description": "A practical guide to Flutter web renderer choices in 2026, including when skwasm, CanvasKit, and WebAssembly builds make sense.",
        "keywords": ["Flutter web 2026", "skwasm vs CanvasKit", "Flutter web renderers", "Flutter WebAssembly", "Flutter web performance"],
        "primary_intent": "Choose the right Flutter web renderer and build approach for a real project.",
        "search_type": "trend",
        "intro": [
            "Flutter web conversations often become vague quickly: WebAssembly is faster, CanvasKit looks better, just use the default. In reality, the right renderer choice depends on what you are shipping, who is using it, and which trade-offs you actually care about.",
            "This guide focuses on the practical decision, not the buzzwords: when skwasm makes sense, when CanvasKit still matters, and how to talk about WebAssembly builds without hand-waving."
        ],
        "notes": [
            "Renderer defaults and recommendations change over time. Treat this guidance as current as of 1 April 2026 and check the current Flutter web renderer documentation for the version you are shipping."
        ],
        "quick_answer": "Choose the renderer based on compatibility, startup profile, graphics demands, and deployment constraints. There is no universal winner. The correct choice is the one that behaves well for your audience and your app’s actual workload.",
        "use_when": [
            "You are deciding renderer strategy before launch or a major migration.",
            "You have a web app with noticeable graphics or performance requirements.",
            "You need a decision that the whole team can understand and maintain.",
        ],
        "sections": [
            {
                "heading": "Start with the app, not the renderer",
                "paragraphs": [
                    "A dashboard with tables and forms is not the same problem as a graphics-heavy design tool. If you begin with the technology label instead of the product shape, you risk optimising the wrong thing."
                ],
            },
            {
                "heading": "Where skwasm is attractive",
                "paragraphs": [
                    "skwasm is attractive when you want strong rendering performance and a modern path aligned with WebAssembly. It is the sort of choice teams reach for when they care about smoother rendering and are comfortable targeting the browser environments that support the path well."
                ],
            },
            {
                "heading": "Where CanvasKit still makes sense",
                "paragraphs": [
                    "CanvasKit is still relevant when you want reliable graphics output and understand its footprint trade-offs. Depending on the product, that trade-off can be acceptable if it produces steadier rendering behaviour for the experience you need."
                ],
            },
        ],
        "example": {
            "heading": "Worked example: an internal analytics dashboard",
            "paragraphs": [
                "An operations team wants a web dashboard with filters, dense tables, and a few interactive charts. The right answer is to test renderer options against the real dashboard, not a toy benchmark.",
                "If the default path already feels solid, forcing a more complex renderer strategy may not buy enough to justify the extra moving parts."
            ],
        },
        "mistakes": [
            "Choosing a renderer from social media opinion alone.",
            "Measuring a demo rather than the real app.",
            "Assuming one renderer fix will solve architecture or layout problems.",
        ],
        "instead": {
            "paragraphs": [
                "If the issue is broad app layout and not renderer choice, read <a href=\"/blog/responsive-flutter-ui-all-screens\">responsive UI</a>. If the app itself is janky beyond web rendering decisions, the better next read is <a href=\"/blog/flutter-performance-2026\">Flutter performance in 2026</a>."
            ],
        },
        "related_new": ["responsive-flutter-ui-all-screens", "flutter-performance-2026", "add-flutter-to-existing-app"],
        "related_old": ["flutter-vs-react-native"],
        "cover_hook": "Pick the renderer that matches the product and browser reality, not the trend label.",
        "cover_cta": "Choose Web Rendering Wisely",
        "cover_keywords": ["skwasm", "CanvasKit", "Web"],
        "cover_cue": "browser render layers, performance graphs, and Flutter web deployment visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Flutter web renderers, with skwasm, CanvasKit, and web performance comparison visuals.",
        "sources": [SOURCES["web_renderers"]],
    },
    {
        "slug": "analyst-vs-agent-mode-vs-copilot-chat",
        "title": "Analyst vs Agent Mode vs Copilot Chat: Which Excel AI Workflow Fits Best?",
        "category": "AI + Excel",
        "description": "Compare Analyst, Agent Mode, and Copilot chat in Excel so you can choose the AI surface that fits the task instead of forcing one tool everywhere.",
        "keywords": ["Analyst vs Agent Mode", "Copilot chat Excel", "Excel AI workflow", "Agent Mode Excel", "Excel AI comparison"],
        "primary_intent": "Choose the right AI surface inside Excel for different kinds of work.",
        "search_type": "trend",
        "intro": [
            "One reason Excel AI feels confusing is that people ask one tool to do every job. But workbook exploration, multi-step action, and conversational help are not the same workflow. Analyst, Agent Mode, and Copilot chat can overlap, yet they are not interchangeable.",
            "If you choose the wrong surface, even a capable model feels disappointing. This guide is about fit: which mode belongs to which kind of spreadsheet task."
        ],
        "quick_answer": "Use Copilot chat for lighter conversational help, Analyst when the job is analytical interpretation, and Agent Mode when you want Excel to take a more guided multi-step role across the workbook. The best result comes from matching the task shape to the tool surface.",
        "use_when": [
            "You want clearer expectations before rolling AI out to a team.",
            "Different users keep picking different AI surfaces for the same workbook.",
            "You need a policy that is practical rather than theoretical.",
        ],
        "sections": [
            {
                "heading": "Copilot chat is the lightest-weight option",
                "paragraphs": [
                    "Copilot chat is usually the easiest entry point because it feels like asking a question in plain language. It works well when the task is narrow: explain this pattern, suggest a formula, summarise this range, or help me get started."
                ],
            },
            {
                "heading": "Analyst is for interpretation-heavy work",
                "paragraphs": [
                    "Analyst-style workflows fit situations where the core value is interpretation rather than action: spotting patterns, exploring trends, framing questions, or identifying unusual changes that deserve a human follow-up."
                ],
            },
            {
                "heading": "Agent Mode is for guided multi-step work",
                "paragraphs": [
                    "Agent Mode becomes attractive when the workbook task is more operational: inspect the workbook, find the relevant ranges, execute several steps, and return a result. It is more ambitious than chat, which is why review matters more."
                ],
            },
        ],
        "example": {
            "heading": "Worked example: a sales workbook with several questions",
            "paragraphs": [
                "A sales manager wants three things: understand which region slipped last quarter, generate a formula for a new margin flag, and prepare a quick workbook summary for the leadership call.",
                "That is three different shapes of work. Analyst helps with the regional interpretation, Copilot chat helps with the formula, and Agent Mode can assist with the broader workbook summary."
            ],
        },
        "mistakes": [
            "Forcing the same AI surface onto every workbook task.",
            "Choosing the tool based on novelty instead of task shape.",
            "Ignoring review just because the interface feels polished.",
        ],
        "instead": {
            "paragraphs": [
                "If you already know you want workbook-level action, go deeper with <a href=\"/blog/agent-mode-in-excel\">Agent Mode in Excel</a>. If the bottleneck is formula quality, read <a href=\"/blog/generate-formula-columns-copilot-excel\">formula columns with Copilot</a> or <a href=\"/blog/review-ai-generated-excel-formulas\">reviewing AI-generated formulas</a>."
            ],
        },
        "related_new": ["agent-mode-in-excel", "generate-formula-columns-copilot-excel", "review-ai-generated-excel-formulas"],
        "related_old": ["copilot-data-analysis"],
        "cover_hook": "Match the AI surface to the workbook task so the tool feels useful instead of noisy.",
        "cover_cta": "Choose The Right Excel AI Mode",
        "cover_keywords": ["Analyst", "Agent", "Chat"],
        "cover_cue": "mode comparison panels, workbook tasks, and decision-making visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Analyst vs Agent Mode vs Copilot Chat in Excel, with AI workflow comparison visuals.",
        "sources": [SOURCES["agent_mode"], SOURCES["copilot_excel"]],
    },
    {
        "slug": "choosecols-chooserows-take-drop-excel",
        "title": "CHOOSECOLS, CHOOSEROWS, TAKE, and DROP in Excel: Slice Data Faster",
        "category": "Excel",
        "description": "Learn how CHOOSECOLS, CHOOSEROWS, TAKE, and DROP help you reshape modern Excel arrays without extra helper columns or manual copying.",
        "keywords": ["CHOOSECOLS Excel", "CHOOSEROWS Excel", "TAKE Excel", "DROP Excel", "Excel dynamic arrays"],
        "primary_intent": "Learn how to slice dynamic arrays and tables with modern Excel functions.",
        "search_type": "hot-evergreen",
        "intro": [
            "These four functions are small, but they fix an annoying problem in modern Excel: once you have a useful spill range, how do you quickly keep only the rows or columns you actually need?",
            "Instead of copying data, hiding columns, or building helper ranges, you can trim the output with formulas and keep the model far cleaner."
        ],
        "quick_answer": "Use CHOOSECOLS and CHOOSEROWS when you want specific positions from a spill result, and use TAKE and DROP when you want the first or last part of a result. They are ideal finishing tools for dynamic-array workflows.",
        "use_when": [
            "You already have a spill formula and want to trim it neatly.",
            "You are building report tabs or dashboards from modern arrays.",
            "You want fewer helper columns and less manual tidying.",
        ],
        "sections": [
            {"heading": "What each function is best at", "paragraphs": ["CHOOSECOLS and CHOOSEROWS are selective. TAKE and DROP are positional. That means you can either pick named parts of a result or trim off the top, bottom, left, or right based on where the useful data sits."]},
            {"heading": "Why these functions matter in real workbooks", "paragraphs": ["They make modern Excel models easier to maintain. Once a source formula returns too much, you no longer need a second manual step. You can shape the result exactly where it lands."]},
            {"heading": "Where they combine well", "paragraphs": ["These functions become especially useful after <a href=\"/blog/groupby-function-excel\">GROUPBY</a>, <a href=\"/blog/pivotby-function-excel\">PIVOTBY</a>, FILTER, UNIQUE, or SORT. They are less about finding data and more about presenting it cleanly."]},
        ],
        "example": {"heading": "Worked example: trimming a report spill range", "paragraphs": ["A report tab spills a wide summary with more columns than stakeholders need. CHOOSECOLS keeps only the customer, region, and revenue fields. TAKE then limits the output to the top ten rows for a compact summary block."]},
        "mistakes": ["Using them to patch messy source data instead of fixing the source table.", "Forgetting that positional slicing can break if the upstream layout changes.", "Overcomplicating a report when a simpler base formula would do."],
        "instead": {"paragraphs": ["If the real problem is grouping and summarising, go back to <a href=\"/blog/groupby-function-excel\">GROUPBY</a>. If the source data itself is awkward, <a href=\"/blog/excel-tables-best-practices\">better table structure</a> often helps more than another formula layer."]},
        "related_new": ["groupby-function-excel", "pivotby-function-excel", "excel-tables-best-practices"],
        "related_old": ["advanced-formulas"],
        "cover_hook": "Trim spill ranges cleanly instead of copying, hiding, or rebuilding them.",
        "cover_cta": "Slice Arrays Faster",
        "cover_keywords": ["TAKE", "DROP", "Arrays"],
        "cover_cue": "trimmed grids, selected columns, and tidy spill-range visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for CHOOSECOLS, CHOOSEROWS, TAKE, and DROP in Excel, with sliced array and report-grid visuals.",
        "sources": [],
    },
    {
        "slug": "flutter-app-architecture-2026",
        "title": "Flutter App Architecture in 2026: A Practical Feature-First Guide",
        "category": "Flutter",
        "description": "A practical guide to Flutter app architecture in 2026, with a feature-first structure that helps teams scale without drowning in folders.",
        "keywords": ["Flutter app architecture", "Flutter architecture 2026", "feature-first Flutter", "Flutter MVVM", "Flutter project structure"],
        "primary_intent": "Choose a practical Flutter app architecture for real production work.",
        "search_type": "evergreen",
        "intro": [
            "The best Flutter architecture is not the one with the most folders. It is the one that helps your team move quickly, test confidently, and keep features understandable six months later.",
            "In 2026, a practical feature-first structure is often the safest default because it keeps screens, state, data rules, and tests close to the feature they belong to."
        ],
        "quick_answer": "Start with a feature-first structure and only add more abstraction when the codebase earns it. That usually means clear feature boundaries, a small shared core, and state, data, and UI decisions that match the app’s complexity instead of copying enterprise patterns too early.",
        "use_when": [
            "You are starting a medium-size Flutter app.",
            "Your existing codebase is becoming hard to navigate.",
            "Several developers need a shared structure that stays readable.",
        ],
        "sections": [
            {"heading": "Why feature-first usually wins", "paragraphs": ["Feature-first structure keeps related code together. Instead of hopping across separate global UI, logic, and data folders for every change, you can work inside one feature boundary and still keep shared code in a small core area."]},
            {"heading": "What good architecture actually protects", "paragraphs": ["Good architecture protects change. It helps you replace a data source, test a view model, split responsibilities, or onboard a new developer without rediscovering the entire app every week."]},
            {"heading": "What to avoid", "paragraphs": ["Avoid huge shared folders too early, over-abstracted service layers, and state solutions that the team does not truly understand. Architecture should remove friction, not create impressive ceremony."]},
        ],
        "example": {"heading": "Worked example: a booking app", "paragraphs": ["A booking app might have home, search, reservation, account, and payments as separate features. Each feature can own its screens, state, repositories, and tests while still sharing network setup, theme, and auth contracts from a core layer."]},
        "mistakes": ["Copying a large-company pattern into a small app.", "Treating architecture as folder design only.", "Choosing state management before clarifying feature boundaries."],
        "instead": {"paragraphs": ["If your bottleneck is route structure, read <a href=\"/blog/go-router-flutter-deep-linking\">go_router</a>. If the problem is testability, the better next read is <a href=\"/blog/flutter-testing-strategy-2026\">Flutter testing strategy</a>."]},
        "related_new": ["go-router-flutter-deep-linking", "flutter-testing-strategy-2026", "flutter-performance-2026"],
        "related_old": ["flutter-state-management"],
        "cover_hook": "Build around features so teams can scale without drowning in global folders.",
        "cover_cta": "Structure Flutter Better",
        "cover_keywords": ["Architecture", "Features", "Flutter"],
        "cover_cue": "feature folders, layered app structure, and production-minded architecture visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Flutter app architecture, with feature-first app structure visuals.",
        "sources": [SOURCES["architecture"]],
    },
    {
        "slug": "format-data-for-copilot-excel",
        "title": "Format Data for Copilot in Excel: Tables, Supported Ranges, and Common Failures",
        "category": "AI + Excel",
        "description": "Learn how to format data for Copilot in Excel so prompts work better, tables stay readable, and common workbook failures stop getting in the way.",
        "keywords": ["Format data for Copilot Excel", "Copilot Excel tables", "Excel AI data prep", "Copilot supported ranges", "Excel data structure"],
        "primary_intent": "Prepare Excel data so Copilot and related AI features can interpret it more reliably.",
        "search_type": "trend",
        "intro": [
            "A lot of Copilot frustration is not really a prompting problem. It is a workbook structure problem. If the data is spread across merged cells, half-labelled columns, decorative totals, and ranges that are not really tables, the AI spends its effort guessing context instead of helping.",
            "That is why this topic deserves its own guide. Clean structure is not a nice extra. It is the base layer for useful Excel AI."
        ],
        "quick_answer": "Put your data in proper Excel tables, give every column one clear heading, avoid decorative layout tricks in the source range, and keep one row equal to one record. Those habits help Copilot far more than clever wording.",
        "use_when": [
            "Copilot keeps misunderstanding what your data represents.",
            "AI features work on one sheet but not another.",
            "You are preparing a shared workbook for team use.",
        ],
        "sections": [
            {"heading": "What good Copilot-ready data looks like", "paragraphs": ["The best source range is boring in the right way: one header row, one record per row, no blank separator rows, no merged cells, and no mixed-purpose columns."]},
            {"heading": "Why tables matter", "paragraphs": ["Excel tables give the workbook a cleaner structure, clearer column identity, and more reliable growth behaviour. They also make later formulas and summaries easier, including <a href=\"/blog/groupby-function-excel\">GROUPBY</a> and <a href=\"/blog/excel-tables-best-practices\">table-driven reporting</a>."]},
            {"heading": "Common failure points", "paragraphs": ["Decorative headings inside the data, totals mixed into source rows, half-empty columns, and inconsistent date formats are some of the biggest reasons Copilot produces weak answers."]},
        ],
        "example": {"heading": "Worked example: a messy sales export", "paragraphs": ["A sales workbook has title rows, blank spacer rows, merged month labels, and revenue stored as text. After converting the core range into one clean table, Copilot can identify fields and answer summary questions much more consistently."]},
        "mistakes": ["Thinking a pretty report layout should also be the source table.", "Leaving several data concepts in one overloaded column.", "Using a prompt to compensate for structural noise."],
        "instead": {"paragraphs": ["If the workbook is already clean and the problem is choosing the right AI surface, go to <a href=\"/blog/analyst-vs-agent-mode-vs-copilot-chat\">Analyst vs Agent Mode vs Copilot Chat</a>. If you need a broader workbook workflow, read <a href=\"/blog/agent-mode-in-excel\">Agent Mode in Excel</a>."]},
        "related_new": ["agent-mode-in-excel", "excel-tables-best-practices", "review-ai-generated-excel-formulas", "ai-power-query-m-code"],
        "related_old": ["clean-messy-data"],
        "cover_hook": "Copilot gets better when the workbook stops making it guess the structure.",
        "cover_cta": "Fix Data Shape First",
        "cover_keywords": ["Tables", "Headers", "Copilot"],
        "cover_cue": "clean tables, structured columns, and workbook-readiness visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for formatting data for Copilot in Excel, with clean table and workbook structure visuals.",
        "sources": [SOURCES["format_copilot"]],
    },
    {
        "slug": "map-scan-reduce-excel",
        "title": "MAP, SCAN, and REDUCE in Excel: Modern Array Logic for Power Users",
        "category": "Excel",
        "description": "Learn how MAP, SCAN, and REDUCE expand modern Excel array logic so you can transform, accumulate, and combine data more elegantly.",
        "keywords": ["MAP Excel", "SCAN Excel", "REDUCE Excel", "Excel array logic", "modern Excel formulas"],
        "primary_intent": "Understand when MAP, SCAN, and REDUCE are useful in practical Excel work.",
        "search_type": "hot-evergreen",
        "intro": [
            "MAP, SCAN, and REDUCE are the kind of functions that make modern Excel feel more like a data language than a spreadsheet toy. They are not the first functions most people should learn, but they become powerful once you already understand dynamic arrays.",
            "The practical win is not cleverness. It is expressing transformation logic more directly and with fewer helper ranges."
        ],
        "quick_answer": "Use MAP when you want to transform each item in an array, SCAN when you want a running result at every step, and REDUCE when you want one accumulated result from many inputs. They are most useful in formula-heavy models where helper columns are getting out of hand.",
        "use_when": [
            "You already work comfortably with dynamic arrays.",
            "A model is collecting too many helper columns.",
            "You want clearer logic around transformations and running calculations.",
        ],
        "sections": [
            {"heading": "What each one is for", "paragraphs": ["MAP changes items, SCAN shows the running journey, and REDUCE gives you the final rolled-up answer. Thinking about them this way is more helpful than memorising syntax alone."]},
            {"heading": "Why they matter in practical models", "paragraphs": ["These functions help you keep logic close to the formula instead of scattering it across a sheet. That can make a model easier to inspect once you are comfortable reading array formulas."]},
            {"heading": "When not to be clever", "paragraphs": ["If your team is uncomfortable maintaining advanced arrays, a helper column may still be the kinder choice. Good spreadsheet work is not about showing off. It is about making the workbook sustainable."]},
        ],
        "example": {"heading": "Worked example: running margin control", "paragraphs": ["A finance analyst wants a running margin view across monthly values. SCAN can produce the running output without a helper column, while REDUCE can produce one overall total from the same logic."]},
        "mistakes": ["Using advanced functions when a simpler formula is easier to maintain.", "Skipping named logic with LET or LAMBDA when formulas become hard to read.", "Assuming power-user functions automatically improve the workbook."],
        "instead": {"paragraphs": ["If you want a more reusable step next, read <a href=\"/blog/let-and-lambda-excel\">LET and LAMBDA</a>. If the real need is summary reporting rather than array transformation, <a href=\"/blog/groupby-function-excel\">GROUPBY</a> may be more relevant."]},
        "related_new": ["let-and-lambda-excel", "groupby-function-excel", "choosecols-chooserows-take-drop-excel"],
        "related_old": ["advanced-formulas"],
        "cover_hook": "Use modern array logic when helper columns start making the workbook heavier than it needs to be.",
        "cover_cta": "Level Up Array Logic",
        "cover_keywords": ["MAP", "SCAN", "REDUCE"],
        "cover_cue": "array flows, running calculations, and formula-logic visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for MAP, SCAN, and REDUCE in Excel, with dynamic-array logic visuals.",
        "sources": [],
    },
    {
        "slug": "go-router-flutter-deep-linking",
        "title": "go_router in Flutter: Deep Linking, Nested Navigation, and Web URLs",
        "category": "Flutter",
        "description": "Learn how go_router helps with deep linking, nested navigation, and cleaner Flutter web URLs without turning routing into a maintenance problem.",
        "keywords": ["go_router Flutter", "Flutter deep linking", "Flutter nested navigation", "Flutter web URLs", "Flutter routing"],
        "primary_intent": "Use go_router effectively for modern Flutter navigation patterns.",
        "search_type": "evergreen",
        "intro": [
            "Routing stops being a small topic the moment your app needs deep links, web URLs, guarded routes, or shells with nested navigation. At that point, go_router is useful because it gives those concerns a clearer home.",
            "The goal is not to make routing feel fancy. It is to make app navigation understandable enough that several developers can work on it without fear."
        ],
        "quick_answer": "Use go_router when your app needs URL-aware navigation, deep links, or nested shells that should stay consistent across mobile and web. Keep the route map readable and avoid turning it into a second business-logic layer.",
        "use_when": [
            "You need deep links or clean browser URLs.",
            "Your app has nested navigation or tab shells.",
            "You want routing decisions to stay explicit and maintainable.",
        ],
        "sections": [
            {"heading": "Why go_router helps", "paragraphs": ["go_router gives navigation concerns a clearer structure, especially once URL state matters. That makes Flutter web, guarded routes, and nested shells easier to reason about than ad hoc route handling."]},
            {"heading": "What teams get wrong", "paragraphs": ["The common mistake is loading too much logic into the route map. Routing should describe navigation shape and light guards, not replace feature state or application services."]},
            {"heading": "How to keep it maintainable", "paragraphs": ["Group routes by feature, keep guards readable, and make route names or paths obvious. If route setup starts feeling magical, future maintenance usually gets worse, not better."]},
        ],
        "example": {"heading": "Worked example: a multi-tab admin app", "paragraphs": ["An admin app has overview, customers, orders, and settings, each with nested detail pages. go_router helps keep deep links, browser navigation, and nested shell behaviour aligned instead of scattering route handling through the widget tree."]},
        "mistakes": ["Putting business rules in the route map.", "Letting route files grow without feature boundaries.", "Ignoring web URL behaviour until late in the build."],
        "instead": {"paragraphs": ["If the bigger issue is overall app structure, read <a href=\"/blog/flutter-app-architecture-2026\">Flutter architecture</a>. If the pain is primarily layout adaptation across devices, <a href=\"/blog/responsive-flutter-ui-all-screens\">responsive UI</a> may help more immediately."]},
        "related_new": ["flutter-app-architecture-2026", "responsive-flutter-ui-all-screens", "add-flutter-to-existing-app"],
        "related_old": ["flutter-state-management"],
        "cover_hook": "Use explicit routing so deep links and web URLs stay understandable as the app grows.",
        "cover_cta": "Route Flutter Cleanly",
        "cover_keywords": ["Routing", "Links", "Flutter"],
        "cover_cue": "route trees, linked screens, and deep-link navigation visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for go_router in Flutter, with nested routes and deep-link visuals.",
        "sources": [SOURCES["navigation"]],
    },
    {
        "slug": "create-lookups-with-copilot-excel",
        "title": "Create Lookups With Copilot in Excel: When It Writes XLOOKUP Well and When It Doesn’t",
        "category": "AI + Excel",
        "description": "Learn when Copilot is genuinely useful for XLOOKUP-style formulas in Excel, and when you should stop prompting and write or review the formula yourself.",
        "keywords": ["Copilot XLOOKUP", "Create lookups with Copilot", "Excel AI lookup formulas", "XLOOKUP with AI", "Copilot Excel formulas"],
        "primary_intent": "Use Copilot effectively for lookup formulas without over-trusting the result.",
        "search_type": "trend",
        "intro": [
            "Lookup formulas are one of the first places people try AI in Excel, and with good reason. A well-written prompt can save a lot of time when you already know the data shape but do not want to remember every argument.",
            "The problem is that lookup errors can look plausible. Copilot can produce a formula that runs and still points to the wrong column, wrong match mode, or wrong range."
        ],
        "quick_answer": "Copilot is useful for lookup formulas when the table structure is clear and you already know what the answer should roughly look like. It is less useful when the workbook is messy or the logic depends on subtle business rules that the prompt does not state clearly.",
        "use_when": [
            "The source and lookup tables are already clean and named clearly.",
            "You can quickly verify whether the formula is using the right columns.",
            "You want a first draft faster than typing the whole formula from scratch.",
        ],
        "sections": [
            {"heading": "Where Copilot helps most", "paragraphs": ["Copilot is strongest when the task is mechanically clear: match customer ID to the master table, return a product category, or pull a price from the latest rate list. In these cases, the main win is speed, not magic."]},
            {"heading": "Where it goes wrong", "paragraphs": ["The common failures are column selection, approximate-versus-exact logic, and ignoring cases such as duplicates or missing keys. These are prompt and review problems, not just AI problems."]},
            {"heading": "How to review the result", "paragraphs": ["Check the lookup column, the return column, the match mode, and the error handling. Then test the formula on rows where you already know the answer before you fill it across the sheet."]},
        ],
        "example": {"heading": "Worked example: customer pricing", "paragraphs": ["A sales sheet needs to pull discount tiers from a master customer table. Copilot can draft the XLOOKUP quickly, but the analyst still checks whether the lookup key is customer ID rather than customer name and whether missing values are handled clearly."]},
        "mistakes": ["Accepting the first formula because it looks syntactically correct.", "Prompting with vague field names such as sheet one and sheet two.", "Skipping test rows before filling the formula down the column."],
        "instead": {"paragraphs": ["If the formula itself is not the problem and you need a narrower lookup skill, <a href=\"/blog/xmatch-function-excel\">XMATCH</a> or <a href=\"/blog/vlookup-vs-xlookup\">VLOOKUP vs XLOOKUP</a> may be the better next reads."]},
        "related_new": ["xmatch-function-excel", "generate-single-cell-formulas-copilot-excel", "review-ai-generated-excel-formulas"],
        "related_old": ["vlookup-vs-xlookup"],
        "cover_hook": "AI can draft lookup formulas quickly, but only if you still review the logic like an analyst.",
        "cover_cta": "Review XLOOKUP Drafts",
        "cover_keywords": ["XLOOKUP", "Copilot", "Review"],
        "cover_cue": "lookup arrows, AI formula drafts, and spreadsheet verification visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for creating lookups with Copilot in Excel, with XLOOKUP and review visuals.",
        "sources": [SOURCES["copilot_excel"]],
    },
    {
        "slug": "let-and-lambda-excel",
        "title": "LET and LAMBDA in Excel: Turn Repeated Formulas Into Reusable Logic",
        "category": "Excel",
        "description": "Learn how LET and LAMBDA make complex Excel formulas easier to read, reuse, and maintain without leaving the workbook.",
        "keywords": ["LET Excel", "LAMBDA Excel", "Excel reusable formulas", "modern Excel functions", "Excel formula design"],
        "primary_intent": "Use LET and LAMBDA to make formula logic more reusable and maintainable.",
        "search_type": "hot-evergreen",
        "intro": [
            "LET and LAMBDA matter because they move Excel away from copy-paste formula habits and towards clearer logic. LET lets you name intermediate values inside a formula. LAMBDA lets you turn logic into a reusable function.",
            "That is useful whenever you keep rewriting the same long formula or explaining the same nested logic to yourself every month."
        ],
        "quick_answer": "Use LET to make long formulas easier to read and calculate once. Use LAMBDA when the same logic appears repeatedly and deserves a reusable workbook-level function.",
        "use_when": [
            "A formula is getting long enough that named parts would improve clarity.",
            "The same business rule appears in many cells.",
            "You want fewer brittle copy-paste formulas across a workbook.",
        ],
        "sections": [
            {"heading": "Why LET is usually the first win", "paragraphs": ["LET improves readability immediately because you can name the pieces of a calculation. That means fewer repeated expressions and a clearer path for anyone reviewing the workbook later."]},
            {"heading": "Where LAMBDA becomes worthwhile", "paragraphs": ["LAMBDA matters once a workbook keeps reusing the same logic. Instead of hiding the rule inside ten separate formulas, you define it once and call it by name."]},
            {"heading": "What this changes in practical models", "paragraphs": ["These functions do not make a workbook clever for the sake of it. They reduce duplication and make advanced logic easier to test, document, and maintain."]},
        ],
        "example": {"heading": "Worked example: revenue quality rule", "paragraphs": ["A finance workbook keeps checking whether revenue rows meet the same quality rule across several sheets. LET makes each formula easier to read, and LAMBDA turns the rule into one named function the whole workbook can reuse."]},
        "mistakes": ["Creating named logic that nobody else can understand.", "Using LAMBDA before the underlying rule is stable.", "Ignoring simpler formulas when the logic is still small."],
        "instead": {"paragraphs": ["If you are still getting comfortable with arrays, <a href=\"/blog/map-scan-reduce-excel\">MAP, SCAN, and REDUCE</a> or <a href=\"/blog/choosecols-chooserows-take-drop-excel\">TAKE and DROP</a> may be easier next steps depending on the problem."]},
        "related_new": ["map-scan-reduce-excel", "choosecols-chooserows-take-drop-excel", "xmatch-function-excel"],
        "related_old": ["advanced-formulas"],
        "cover_hook": "Name logic once so long formulas stop becoming unreadable repeated blocks.",
        "cover_cta": "Make Formulas Reusable",
        "cover_keywords": ["LET", "LAMBDA", "Reuse"],
        "cover_cue": "named formula blocks, reusable logic chips, and cleaner calculation visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for LET and LAMBDA in Excel, with reusable formula logic visuals.",
        "sources": [],
    },
    {
        "slug": "flutter-form-validation-best-practices",
        "title": "Flutter Form Validation Best Practices for Production Apps",
        "category": "Flutter",
        "description": "Learn practical Flutter form validation habits that keep production apps clearer, safer, and less frustrating for users and engineers alike.",
        "keywords": ["Flutter form validation", "Flutter forms", "production Flutter", "Flutter validation best practices", "Flutter UX validation"],
        "primary_intent": "Build better production-ready Flutter form validation flows.",
        "search_type": "evergreen",
        "intro": [
            "Validation is one of those app details users only notice when it goes wrong. Confusing timing, vague messages, and inconsistent rules make forms feel cheap even in otherwise polished products.",
            "The engineering side matters just as much. Good validation keeps rules testable and stops business logic from leaking across widgets."
        ],
        "quick_answer": "Validate as close to the business rule as you reasonably can, keep messages specific, and avoid surprising users with noisy real-time errors too early. The best form validation balances clarity, timing, and maintainable code structure.",
        "use_when": [
            "You are building forms that matter to sign-up, checkout, onboarding, or admin workflows.",
            "Validation logic is spreading across several widgets.",
            "The current form works technically but feels brittle or annoying.",
        ],
        "sections": [
            {"heading": "Timing matters as much as the rule", "paragraphs": ["Users do not need to be punished with red errors while they are still typing. Good timing means validating when the feedback will actually help rather than distract."]},
            {"heading": "Keep business rules out of throwaway UI code", "paragraphs": ["A validator can live near the field, but the rule itself should still be understandable and testable. That makes changes safer when the product team inevitably updates the form requirements."]},
            {"heading": "Messages should tell people what to do next", "paragraphs": ["Specific messages reduce friction. Enter a valid company email is better than invalid input because it gives the user a fix, not merely a warning."]},
        ],
        "example": {"heading": "Worked example: checkout form", "paragraphs": ["A checkout form validates postcode, cardholder name, and VAT number. Instead of showing all errors instantly, the app validates on submit and then more selectively as the user corrects the relevant fields."]},
        "mistakes": ["Showing error states too early.", "Hiding validation logic inside untestable widget code.", "Using generic error text that does not help the user recover."],
        "instead": {"paragraphs": ["If the form problem is actually app structure, go back to <a href=\"/blog/flutter-app-architecture-2026\">architecture</a>. If the issue is UI adaptation, <a href=\"/blog/responsive-flutter-ui-all-screens\">responsive layout</a> may be the better next read."]},
        "related_new": ["flutter-app-architecture-2026", "responsive-flutter-ui-all-screens", "flutter-testing-strategy-2026"],
        "related_old": ["flutter-state-management"],
        "cover_hook": "Good validation improves trust for users and reduces brittle rules for engineers.",
        "cover_cta": "Validate Forms Better",
        "cover_keywords": ["Forms", "Validation", "Flutter"],
        "cover_cue": "form fields, validation states, and production-ready mobile UI visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Flutter form validation best practices, with mobile form and validation-state visuals.",
        "sources": [SOURCES["validation"]],
    },
    {
        "slug": "generate-formula-columns-copilot-excel",
        "title": "Generate Formula Columns With Copilot in Excel: Best Prompts and Review Steps",
        "category": "AI + Excel",
        "description": "Learn how to use Copilot for full formula columns in Excel, including the prompt patterns and review steps that stop bad logic spreading down the sheet.",
        "keywords": ["Generate formula columns Copilot Excel", "Copilot Excel columns", "Excel AI formulas", "Copilot prompt Excel", "review AI formulas"],
        "primary_intent": "Use Copilot for formula columns safely and efficiently.",
        "search_type": "trend",
        "intro": [
            "Generating one formula is useful. Generating a whole column is where AI starts to save serious time, because many real workbooks are not blocked by one cell. They are blocked by a repetitive derived field that someone needs to build quickly and fill across thousands of rows.",
            "The risk is obvious too: one bad formula pattern multiplied down the table is still a bad model."
        ],
        "quick_answer": "Copilot is helpful for formula columns when the business rule is clear, the source table is clean, and you review the first few rows before accepting the whole fill. Good prompts describe the rule, the relevant columns, and the expected edge cases.",
        "use_when": [
            "You need a derived field across many rows.",
            "The logic is consistent enough to describe clearly in plain English.",
            "You can review sample outputs before committing to the whole column.",
        ],
        "sections": [
            {"heading": "What a good prompt includes", "paragraphs": ["Name the table or columns, explain the rule, and mention the edge cases you care about. Telling Copilot what to do when values are blank or missing is often the difference between a usable column and a noisy one."]},
            {"heading": "Why review must happen at the top of the column", "paragraphs": ["If the first few rows are wrong, filling the whole column only spreads the problem faster. Review the first outputs, compare them with known examples, and confirm the column references before you trust the bulk result."]},
            {"heading": "Where this works best", "paragraphs": ["This is strongest for flags, buckets, due-date labels, discount bands, or tidy business rules. It is weaker when the rule is ambiguous or changes by hidden context that the prompt does not capture."]},
        ],
        "example": {"heading": "Worked example: overdue payment status", "paragraphs": ["An accounts sheet needs a new status column based on invoice date, due date, payment date, and amount outstanding. Copilot can draft the formula column quickly, but the analyst still checks rows for unpaid, paid-late, and paid-on-time cases before filling the full table."]},
        "mistakes": ["Describing the rule vaguely.", "Ignoring blanks and missing values.", "Letting one unreviewed formula pattern fill thousands of rows."],
        "instead": {"paragraphs": ["If you only need one formula and not a whole column, <a href=\"/blog/generate-single-cell-formulas-copilot-excel\">single-cell formula generation</a> is the better match. If the job is really data preparation, <a href=\"/blog/format-data-for-copilot-excel\">fix the table structure first</a>."]},
        "related_new": ["generate-single-cell-formulas-copilot-excel", "review-ai-generated-excel-formulas", "format-data-for-copilot-excel"],
        "related_old": ["copilot-automate-tasks"],
        "cover_hook": "AI can save time on repeated derived fields if you review the logic before it spreads.",
        "cover_cta": "Build Better Formula Columns",
        "cover_keywords": ["Columns", "Prompts", "Review"],
        "cover_cue": "column fills, AI prompts, and spreadsheet review visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for generating formula columns with Copilot in Excel, with prompt and column-fill visuals.",
        "sources": [SOURCES["copilot_excel"]],
    },
    {
        "slug": "xmatch-function-excel",
        "title": "XMATCH in Excel: Smarter Lookups, Reverse Searches, and Binary Search Use Cases",
        "category": "Excel",
        "description": "Learn how XMATCH improves lookup logic in Excel, including reverse searches and scenarios where binary search can make sense.",
        "keywords": ["XMATCH Excel", "Excel reverse lookup", "XMATCH function", "Excel binary search", "modern Excel lookups"],
        "primary_intent": "Understand what XMATCH is good at and where it belongs in modern Excel lookup work.",
        "search_type": "hot-evergreen",
        "intro": [
            "XMATCH is easy to overlook because it sounds like a supporting actor next to XLOOKUP. But it solves a useful part of the lookup problem on its own, especially when you need position, reverse search, or tighter control over match behaviour.",
            "It becomes more valuable once you stop treating lookup work as one-size-fits-all."
        ],
        "quick_answer": "Use XMATCH when you need the position of a match rather than the returned value, when you want reverse searches, or when you need more control over the lookup mechanics than MATCH gives you.",
        "use_when": [
            "You need the position of a result, not just the value.",
            "You want to search from the end of a list.",
            "You are building more precise modern lookup logic."
        ],
        "sections": [
            {"heading": "Why XMATCH matters", "paragraphs": ["XMATCH gives you a cleaner way to control lookup position and search direction. That opens up patterns that feel awkward with older lookup tools."]},
            {"heading": "Where it fits best", "paragraphs": ["It is useful in dynamic models, advanced INDEX combinations, reverse searches, and any setup where the position itself drives a later formula."]},
            {"heading": "Why it is not just MATCH with a new name", "paragraphs": ["The practical difference is control. Search mode and match handling make XMATCH far more useful once you move beyond the simplest left-to-right lookup questions."]}
        ],
        "example": {"heading": "Worked example: latest matching record", "paragraphs": ["An operations sheet needs the latest matching record for a customer rather than the first one. XMATCH can search from the bottom of the list and return the position the later formula needs."]},
        "mistakes": [
            "Using it when XLOOKUP already solves the problem more directly.",
            "Ignoring sort assumptions for any binary-search style pattern.",
            "Forgetting that position and value are different outputs."
        ],
        "instead": {
            "paragraphs": [
                "If you need the returned value directly, XLOOKUP may still be simpler. If you want to compare older and newer lookup approaches, <a href=\"/blog/vlookup-vs-xlookup\">VLOOKUP vs XLOOKUP</a> remains useful background."
            ]
        },
        "related_new": ["create-lookups-with-copilot-excel", "let-and-lambda-excel", "review-ai-generated-excel-formulas"],
        "related_old": ["vlookup-vs-xlookup"],
        "cover_hook": "Use modern lookup control when position and search direction matter more than a basic match.",
        "cover_cta": "Use XMATCH Smarter",
        "cover_keywords": ["XMATCH", "Lookup", "Position"],
        "cover_cue": "reverse-search arrows, lookup positions, and modern formula visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for XMATCH in Excel, with reverse-search and lookup-position visuals.",
        "sources": []
    },
    {
        "slug": "flutter-performance-2026",
        "title": "Flutter Performance in 2026: Impeller, DevTools, and Rebuild Reduction",
        "category": "Flutter",
        "description": "A practical Flutter performance guide for 2026, covering what to measure, where jank usually starts, and how to reduce rebuild and startup pain.",
        "keywords": ["Flutter performance 2026", "Flutter jank", "Impeller Flutter", "Flutter DevTools", "reduce rebuilds Flutter"],
        "primary_intent": "Improve Flutter app performance with practical measurement and reduction habits.",
        "search_type": "trend",
        "intro": [
            "Performance advice becomes useless very quickly when it turns into folklore. You do not ship faster apps by memorising random micro-optimisations. You ship faster apps by measuring the real bottleneck and fixing the part that is actually burning time or frames.",
            "In Flutter, that usually means paying attention to rebuild scope, image cost, layout depth, startup work, and how your state changes ripple through the tree."
        ],
        "quick_answer": "Measure first with DevTools, reduce unnecessary rebuilds, keep startup work honest, and fix the expensive parts that show up in your real app rather than a tutorial benchmark. Performance work is mostly about discipline, not tricks.",
        "use_when": [
            "The app feels janky or slow in real usage.",
            "Developers are guessing instead of measuring.",
            "The app is growing and performance debt is becoming visible.",
        ],
        "sections": [
            {"heading": "Start with measurement", "paragraphs": ["DevTools should guide the conversation. Find out whether the issue is layout, paint, image decoding, startup, or state churn before you refactor anything."]},
            {"heading": "Rebuild reduction matters because scope matters", "paragraphs": ["Many Flutter apps lose smoothness not because Flutter is slow, but because too much of the tree rebuilds too often. Smarter widget boundaries and state placement usually matter more than heroically clever code."]},
            {"heading": "Startup deserves the same scrutiny", "paragraphs": ["If startup work is bloated with unnecessary initialisation, users feel it before they see any polish. Delay what is not needed immediately and measure the actual impact."]},
        ],
        "example": {"heading": "Worked example: a dashboard screen", "paragraphs": ["A dashboard stutters when filters change. Profiling shows that several heavy widgets rebuild even when only one chart actually needs new data. Splitting rebuild scope improves the interaction more than any cosmetic tweak."]},
        "mistakes": ["Optimising before measuring.", "Blaming Flutter when the app structure is the real problem.", "Treating performance as a one-off late-stage task."],
        "instead": {"paragraphs": ["If the issue is renderer or browser behaviour on web, see <a href=\"/blog/flutter-web-skwasm-vs-canvaskit\">Flutter web renderers</a>. If the broader code structure is the real cause, go back to <a href=\"/blog/flutter-app-architecture-2026\">architecture</a>."]},
        "related_new": ["flutter-app-architecture-2026", "responsive-flutter-ui-all-screens", "flutter-testing-strategy-2026"],
        "related_old": ["flutter-state-management"],
        "cover_hook": "Measure the real bottleneck, then cut rebuild and startup waste where it actually hurts.",
        "cover_cta": "Improve Flutter Performance",
        "cover_keywords": ["Performance", "DevTools", "Flutter"],
        "cover_cue": "performance graphs, rebuild heat, and mobile app profiling visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Flutter performance in 2026, with profiling and rebuild visuals.",
        "sources": [SOURCES["web_renderers"]],
    },
    {
        "slug": "generate-single-cell-formulas-copilot-excel",
        "title": "Generate Single-Cell Formulas With Copilot in Excel: Fast Wins and Failure Modes",
        "category": "AI + Excel",
        "description": "Learn when Copilot is useful for one-off Excel formulas, how to prompt it cleanly, and how to catch the failure modes before you trust the result.",
        "keywords": ["Single-cell formulas Copilot Excel", "Copilot Excel formula", "Excel AI formulas", "prompt Copilot Excel", "review formula AI"],
        "primary_intent": "Use Copilot for one-off formulas with better prompting and review.",
        "search_type": "trend",
        "intro": [
            "Single-cell formulas are often the best entry point for Excel AI because the task is small enough to review quickly. You describe the outcome, Copilot drafts the formula, and you can test whether the result makes sense without touching the whole workbook.",
            "That is also why this topic is worth separating from full formula columns. The review surface is smaller, so the prompt and checking habits can be simpler."
        ],
        "quick_answer": "Copilot is useful for one-off formulas when the required logic is clear and the columns are named sensibly. It becomes less reliable when the workbook is messy, the rule is ambiguous, or the prompt leaves out important edge cases.",
        "use_when": [
            "You need one formula quickly and can review it immediately.",
            "The business rule can be stated clearly in one sentence.",
            "You are happy to test the result against a few known rows.",
        ],
        "sections": [
            {"heading": "What a good prompt sounds like", "paragraphs": ["A good prompt names the relevant columns, explains the rule, and states the expected output. Clarity beats cleverness."]},
            {"heading": "Why this is a fast-win workflow", "paragraphs": ["Because the result is one cell, you can validate it quickly. That makes single-cell formulas one of the safest ways to use Excel AI productively."]},
            {"heading": "Where it still fails", "paragraphs": ["Copilot can still choose the wrong columns, misread blanks, or ignore subtle business rules. The formula looking tidy is not the same as the formula being right."]},
        ],
        "example": {"heading": "Worked example: revenue band label", "paragraphs": ["A report needs one formula to label revenue as low, medium, or high based on thresholds in the brief. Copilot can draft it quickly, then the analyst checks a few obvious cases before reusing the logic elsewhere."]},
        "mistakes": ["Prompting vaguely.", "Skipping row-level checks because the formula looks professional.", "Assuming AI-generated logic handles blanks exactly the way you need."],
        "instead": {"paragraphs": ["If you need the logic across a full table, go to <a href=\"/blog/generate-formula-columns-copilot-excel\">formula columns with Copilot</a>. If the task is a traditional lookup, <a href=\"/blog/create-lookups-with-copilot-excel\">lookups with Copilot</a> is the better match."]},
        "related_new": ["generate-formula-columns-copilot-excel", "create-lookups-with-copilot-excel", "review-ai-generated-excel-formulas"],
        "related_old": ["copilot-data-analysis"],
        "cover_hook": "Single-cell AI formulas are useful when the prompt is clear and the check is immediate.",
        "cover_cta": "Draft One Formula Faster",
        "cover_keywords": ["Formula", "Prompt", "Review"],
        "cover_cue": "single-cell formulas, prompt cards, and quick-check spreadsheet visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for generating single-cell formulas with Copilot in Excel, with prompt and formula visuals.",
        "sources": [SOURCES["copilot_excel"]],
    },
    {
        "slug": "excel-tables-best-practices",
        "title": "Excel Tables Best Practices: Structured References, Growth, and Cleaner Models",
        "category": "Excel",
        "description": "Learn practical Excel table habits that make reports easier to maintain, formulas easier to read, and AI or dashboard workflows far more reliable.",
        "keywords": ["Excel tables best practices", "structured references Excel", "Excel tables", "cleaner Excel models", "Excel reporting"],
        "primary_intent": "Use Excel tables more effectively in everyday reporting and modelling.",
        "search_type": "evergreen",
        "intro": [
            "Excel tables are one of the highest-leverage habits most users still underuse. They make formulas clearer, source ranges easier to grow, and reporting workflows less fragile.",
            "They also happen to make modern Excel and Excel AI much easier to work with, because the data shape becomes more explicit."
        ],
        "quick_answer": "Put source data in proper Excel tables, keep headings clean, avoid decorative clutter inside the table, and let formulas, summaries, and charts reference the table rather than fragile manual ranges.",
        "use_when": [
            "A sheet grows every week or month.",
            "Several formulas or charts depend on the same source data.",
            "You want a workbook that survives handover better.",
        ],
        "sections": [
            {"heading": "Why tables help so much", "paragraphs": ["Tables give your data a stable identity. That makes structured references, dynamic growth, and summary formulas far easier to manage than ad hoc ranges."]},
            {"heading": "What good table design looks like", "paragraphs": ["One header row, one record per row, no blank separators, and no decorative totals inside the source area. The table should be built for work, not for presentation."]},
            {"heading": "Where tables unlock other skills", "paragraphs": ["Tables pair naturally with <a href=\"/blog/groupby-function-excel\">GROUPBY</a>, <a href=\"/blog/pivotby-function-excel\">PIVOTBY</a>, dashboard work, and Copilot-ready data preparation."]},
        ],
        "example": {"heading": "Worked example: monthly operations tracker", "paragraphs": ["An operations tracker receives new rows every day. Once the source becomes a table, summaries, charts, and status formulas all update more reliably because every downstream step references the same growing structure."]},
        "mistakes": ["Mixing titles, totals, and source data in one table.", "Leaving inconsistent headings across similar sheets.", "Building reports off manual cell ranges when the source already deserves a table."],
        "instead": {"paragraphs": ["If the source data is already clean and you need summary logic, move to <a href=\"/blog/groupby-function-excel\">GROUPBY</a> or <a href=\"/blog/pivotby-function-excel\">PIVOTBY</a>. If the source itself is messy, <a href=\"/blog/format-data-for-copilot-excel\">data formatting for Copilot</a> is a good companion guide."]},
        "related_new": ["groupby-function-excel", "pivotby-function-excel", "format-data-for-copilot-excel"],
        "related_old": ["data-validation"],
        "cover_hook": "Good tables make formulas, dashboards, and AI workflows more reliable before you add anything fancy.",
        "cover_cta": "Fix Table Design First",
        "cover_keywords": ["Tables", "Structure", "Excel"],
        "cover_cue": "structured references, clean headers, and stable table-growth visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Excel tables best practices, with clean table and structured-reference visuals.",
        "sources": [],
    },
    {
        "slug": "responsive-flutter-ui-all-screens",
        "title": "Responsive Flutter UI for Mobile, Tablet, Desktop, and Web",
        "category": "Flutter",
        "description": "Learn how to build responsive Flutter interfaces that hold up across mobile, tablet, desktop, and web without relying on brittle one-off layouts.",
        "keywords": ["Responsive Flutter UI", "Flutter tablet layout", "Flutter desktop layout", "Flutter web UI", "responsive Flutter"],
        "primary_intent": "Build more adaptable Flutter interfaces across screen sizes.",
        "search_type": "evergreen",
        "intro": [
            "Responsive Flutter UI is not about adding a couple of width checks at the end. It is about deciding what should stay consistent, what should adapt, and how the information hierarchy should change as space increases.",
            "The strongest layouts feel intentional on every screen size rather than squeezed on mobile and stretched on desktop."
        ],
        "quick_answer": "Treat responsiveness as a content and layout decision, not only a breakpoint decision. Build adaptable spacing, panel structure, and information hierarchy so the UI still feels designed on each screen size.",
        "use_when": [
            "Your Flutter app targets more than one class of device.",
            "A screen feels cramped on mobile or empty on desktop.",
            "You want fewer one-off layout hacks late in the build.",
        ],
        "sections": [
            {"heading": "Start with layout intent", "paragraphs": ["Ask what the user needs to see first on each device class. The answer should shape panel count, density, and arrangement before you start sprinkling breakpoints through the code."]},
            {"heading": "Keep components adaptable", "paragraphs": ["Cards, forms, and lists should stretch or compress gracefully. When components are responsive in isolation, full screens become easier to manage."]},
            {"heading": "Test the information hierarchy, not just the pixels", "paragraphs": ["A screen can technically fit and still feel wrong. Check whether the primary action, scan pattern, and interaction rhythm still make sense on every target size."]},
        ],
        "example": {"heading": "Worked example: admin overview", "paragraphs": ["On mobile, the admin overview stacks filters above results. On tablet, the filters shift into a side panel. On desktop, summary cards and tables can coexist without hiding the main action path."]},
        "mistakes": ["Treating desktop as mobile with more padding.", "Hard-coding layout decisions too early.", "Testing only one happy-path width per platform."],
        "instead": {"paragraphs": ["If your main pain is navigation structure, <a href=\"/blog/go-router-flutter-deep-linking\">go_router</a> may help more. If the UI feels slow rather than cramped, see <a href=\"/blog/flutter-performance-2026\">Flutter performance</a>."]},
        "related_new": ["go-router-flutter-deep-linking", "flutter-performance-2026", "add-flutter-to-existing-app"],
        "related_old": ["flutter-vs-react-native"],
        "cover_hook": "Responsive design is about hierarchy and structure, not just a couple of breakpoints.",
        "cover_cta": "Design Across Screens",
        "cover_keywords": ["Responsive", "Layouts", "Flutter"],
        "cover_cue": "multi-device layouts, adaptive panels, and cross-screen UI visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for responsive Flutter UI across mobile, tablet, desktop, and web.",
        "sources": [],
    },
    {
        "slug": "create-charts-with-copilot-excel",
        "title": "Create Charts With Copilot in Excel: What Works, What Needs Manual Cleanup",
        "category": "AI + Excel",
        "description": "Learn when Copilot helps with charts in Excel, where it still needs manual cleanup, and how to review the result before sharing it widely.",
        "keywords": ["Create charts with Copilot", "Copilot Excel charts", "Excel AI charts", "Copilot chart review", "Excel chart prompts"],
        "primary_intent": "Use Copilot for chart creation in Excel without over-trusting the result.",
        "search_type": "evergreen",
        "intro": [
            "Chart creation looks like a perfect AI task because much of it is repetitive: choose a visual, map the fields, apply a title, and show the first draft quickly. Copilot can help with that first pass.",
            "The catch is that a technically correct chart can still be a bad chart. Review is not optional just because the bars appear."
        ],
        "quick_answer": "Use Copilot to draft charts quickly when the data is already clean and the reporting question is simple. Expect to do manual cleanup around chart choice, titles, labels, sorting, and the story you actually want the chart to tell.",
        "use_when": [
            "You need a quick first chart from a clean table.",
            "The reporting question is clear and bounded.",
            "You are happy to refine the result manually afterwards.",
        ],
        "sections": [
            {"heading": "What works well", "paragraphs": ["Copilot is useful for getting from blank sheet to first chart faster. That is especially helpful when you need an initial visual for discussion rather than a final presentation-ready asset."]},
            {"heading": "Where manual cleanup still matters", "paragraphs": ["Chart type, title quality, sorting, clutter, axis decisions, and annotation still need human judgement. Those are communication choices, not merely software actions."]},
            {"heading": "How to review the first draft", "paragraphs": ["Ask whether the chart answers the actual business question, whether the scale is honest, and whether a stakeholder could misread it. Then tidy the copy and formatting before sharing."]},
        ],
        "example": {"heading": "Worked example: monthly revenue variance", "paragraphs": ["A finance lead wants a quick chart of revenue variance by month. Copilot creates the first visual, then the analyst changes the title, reorders the months correctly, and adds one annotation so the key movement is obvious."]},
        "mistakes": ["Accepting the first chart type without thinking.", "Ignoring sorting or date-order issues.", "Sharing a draft chart as if AI chose the best narrative automatically."],
        "instead": {"paragraphs": ["If you need stronger charting fundamentals, <a href=\"/blog/charts-visualisations\">professional charts in Excel</a> is still the better foundation. If the real problem is data structure, <a href=\"/blog/format-data-for-copilot-excel\">format the source properly first</a>."]},
        "related_new": ["format-data-for-copilot-excel", "review-ai-generated-excel-formulas", "chatgpt-vs-claude-vs-copilot-vs-gemini-excel", "text-analysis-excel-with-ai", "map-charts-excel"],
        "related_old": ["charts-visualisations"],
        "cover_hook": "AI can draft a chart quickly, but it still needs human judgement before it tells the right story.",
        "cover_cta": "Refine Chart Drafts",
        "cover_keywords": ["Charts", "Copilot", "Story"],
        "cover_cue": "chart drafts, AI panels, and presentation-cleanup visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for creating charts with Copilot in Excel, with chart-draft and review visuals.",
        "sources": [SOURCES["copilot_excel"]],
    },
    {
        "slug": "fix-spill-errors-excel",
        "title": "How to Fix #SPILL! Errors in Excel and Prevent Them in Dynamic Array Models",
        "category": "Excel",
        "description": "Learn the practical causes of #SPILL! errors in Excel and how to fix and prevent them in dynamic-array workbooks.",
        "keywords": ["#SPILL Excel", "fix spill errors Excel", "dynamic array errors Excel", "Excel spill ranges", "Excel troubleshooting"],
        "primary_intent": "Fix #SPILL! errors and understand why they happen.",
        "search_type": "evergreen",
        "intro": [
            "The good news about a #SPILL! error is that Excel is telling you something useful: the formula wants to return more than one value, but something is blocking the result. The bad news is that the blocker is not always obvious at first glance.",
            "Once you understand the common causes, spill errors become much easier to diagnose and prevent."
        ],
        "quick_answer": "A #SPILL! error usually means the output range is blocked, the formula is trying to spill in a context that does not allow it, or the source logic is producing an array shape Excel cannot place cleanly.",
        "use_when": [
            "A dynamic-array formula suddenly stops returning results.",
            "A workbook mixes new array functions with older layout habits.",
            "You are building reports that depend on spill ranges behaving consistently.",
        ],
        "sections": [
            {"heading": "The most common blocker", "paragraphs": ["The most common reason is simply that cells in the intended spill area are not empty. The formula is fine, but the output has nowhere to land."]},
            {"heading": "Other causes worth checking", "paragraphs": ["Tables, merged cells, legacy layout habits, or formulas that create awkward result shapes can also trigger spill problems. The error is often about workbook design as much as formula logic."]},
            {"heading": "How to prevent repeat issues", "paragraphs": ["Give spill formulas room, avoid placing stray values next to them, and design report tabs so dynamic outputs have a clear landing zone."]},
        ],
        "example": {"heading": "Worked example: filtered report section", "paragraphs": ["A FILTER formula is meant to spill customer rows into a report area, but an old note still sits below the first output cell. Clearing that blocker removes the error immediately."]},
        "mistakes": ["Debugging the formula first when the spill range itself is blocked.", "Mixing decorative layout habits with dynamic-array outputs.", "Forgetting that spill results may grow when source data grows."],
        "instead": {"paragraphs": ["If the issue is more about slicing arrays than fixing errors, <a href=\"/blog/choosecols-chooserows-take-drop-excel\">TAKE, DROP, CHOOSECOLS, and CHOOSEROWS</a> are the better next tools."]},
        "related_new": ["choosecols-chooserows-take-drop-excel", "groupby-function-excel", "excel-tables-best-practices"],
        "related_old": ["advanced-formulas"],
        "cover_hook": "Most spill errors are easier to fix once you stop treating them like mysterious formula bugs.",
        "cover_cta": "Clear Spill Errors Faster",
        "cover_keywords": ["#SPILL!", "Arrays", "Fix"],
        "cover_cue": "blocked ranges, dynamic arrays, and troubleshooting visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for fixing #SPILL! errors in Excel, with dynamic-array troubleshooting visuals.",
        "sources": [],
    },
    {
        "slug": "add-flutter-to-existing-app",
        "title": "Add Flutter to an Existing App: Mobile and Web Integration Patterns",
        "category": "Flutter",
        "description": "Learn practical patterns for adding Flutter to an existing product without turning the integration into a long-term maintenance burden.",
        "keywords": ["Add Flutter to existing app", "Flutter integration", "embed Flutter", "Flutter migration", "Flutter in existing product"],
        "primary_intent": "Integrate Flutter into an existing app or product more cleanly.",
        "search_type": "evergreen",
        "intro": [
            "Not every Flutter decision starts with a blank project. Sometimes the better business move is to introduce Flutter into an existing app or product surface where it can add value without rewriting the world.",
            "That path can work well, but only if you treat integration as architecture, not just as a build trick."
        ],
        "quick_answer": "Add Flutter to an existing app when you have a clear boundary for the new experience, a sensible integration contract, and a plan for ownership after launch. The goal is a maintainable seam, not a flashy demo.",
        "use_when": [
            "You want to modernise part of a product without a full rewrite.",
            "One feature area is a stronger candidate for Flutter than the whole app.",
            "You need a migration path that reduces risk.",
        ],
        "sections": [
            {"heading": "Start with the seam", "paragraphs": ["The most important decision is where Flutter begins and ends. A clear feature boundary makes integration easier to reason about and easier to undo or expand later."]},
            {"heading": "Think about ownership early", "paragraphs": ["Who owns the integration, shared models, release cadence, and bug flow after launch? The technical integration is only half the work if teams are unclear about responsibility."]},
            {"heading": "Keep communication contracts clean", "paragraphs": ["The more disciplined the boundary between Flutter and the host app, the easier long-term maintenance becomes. Treat it like a product contract, not a temporary hack."]},
        ],
        "example": {"heading": "Worked example: onboarding flow", "paragraphs": ["A company keeps its legacy app intact but rebuilds a complex onboarding flow in Flutter. The Flutter boundary stays limited to that flow, with clearly defined inputs, outputs, and analytics events."]},
        "mistakes": ["Adding Flutter without a clear feature boundary.", "Treating integration details as a later problem.", "Letting ownership become fuzzy between teams."],
        "instead": {"paragraphs": ["If you are choosing a stack for a greenfield app instead, <a href=\"/blog/flutter-vs-react-native\">Flutter vs React Native</a> may be the better starting point."]},
        "related_new": ["flutter-app-architecture-2026", "responsive-flutter-ui-all-screens", "go-router-flutter-deep-linking"],
        "related_old": ["flutter-vs-react-native"],
        "cover_hook": "Integrate Flutter where it adds value, but keep the seam clean enough to maintain afterwards.",
        "cover_cta": "Integrate Flutter Cleanly",
        "cover_keywords": ["Integration", "Flutter", "Migration"],
        "cover_cue": "host-app seams, embedded screens, and migration visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for adding Flutter to an existing app, with integration and migration visuals.",
        "sources": [],
    },
    {
        "slug": "text-analysis-excel-with-ai",
        "title": "Text Analysis in Excel With AI: Survey Comments, Reviews, and Open Feedback",
        "category": "AI + Excel",
        "description": "Learn how to use AI with Excel to analyse survey comments, product reviews, and open-text feedback without turning the process into a black box.",
        "keywords": ["text analysis Excel AI", "survey comments Excel AI", "review analysis Excel", "Excel feedback analysis", "AI Excel workflow"],
        "primary_intent": "Use AI to analyse open-text data in Excel more effectively and safely.",
        "search_type": "evergreen",
        "intro": [
            "Open-text feedback is where spreadsheets often start to creak. Comments, reviews, and survey responses can be rich, but they are slow to categorise consistently by hand.",
            "AI helps because it can draft labels, themes, and summaries quickly. The important word is draft. Review and sampling still matter if you want a result you can trust."
        ],
        "quick_answer": "Use AI to accelerate theme extraction, draft categorisation, and first-pass summarisation of text data in Excel. Keep the workflow grounded by sampling outputs, checking edge cases, and documenting how the labels were produced.",
        "use_when": [
            "You have too many comments to code manually in a reasonable time.",
            "You need themes or categories quickly for a report.",
            "You can still review a representative sample before relying on the output.",
        ],
        "sections": [
            {"heading": "Where AI helps most", "paragraphs": ["AI is strongest when the task is repetitive interpretation at scale: grouping similar complaints, drafting sentiment-style labels, or producing a first-pass summary of what people keep mentioning."]},
            {"heading": "Why sampling is not optional", "paragraphs": ["You need to know whether the labels hold up on real examples, edge cases, sarcasm, and domain-specific wording. Sampling keeps the workflow honest."]},
            {"heading": "How to keep the process reviewable", "paragraphs": ["Label the AI-generated columns clearly, keep the prompt or method documented, and separate raw text from interpreted outputs so you can revisit the logic later."]},
        ],
        "example": {"heading": "Worked example: post-purchase survey comments", "paragraphs": ["An e-commerce team receives 4,000 survey comments in a quarter. AI helps draft categories such as delivery speed, packaging, fit, returns, and customer support. The analyst then samples each category before using it in the presentation."]},
        "mistakes": ["Treating first-pass categories as final truth.", "Skipping sample review because the totals look tidy.", "Mixing raw comments and interpreted labels without documenting the method."],
        "instead": {"paragraphs": ["If the text needs to stay in a workbook but the real bottleneck is AI-generated formula safety, go to <a href=\"/blog/review-ai-generated-excel-formulas\">reviewing AI formulas</a>. If the next step is turning the themes into a presentation-ready output, <a href=\"/blog/create-charts-with-copilot-excel\">charts with Copilot</a> is the closest follow-up in this batch."]},
        "related_new": ["create-charts-with-copilot-excel", "review-ai-generated-excel-formulas", "format-data-for-copilot-excel"],
        "related_old": ["excel-ai-prompts"],
        "cover_hook": "AI can speed up open-text analysis if you still sample the labels before trusting the summary.",
        "cover_cta": "Analyse Text More Reliably",
        "cover_keywords": ["Feedback", "Themes", "AI"],
        "cover_cue": "survey comments, category tags, and text-analysis workflow visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for text analysis in Excel with AI, with survey-comment and theme-tag visuals.",
        "sources": [],
    },
    {
        "slug": "audit-formulas-excel",
        "title": "How to Audit Formulas in Excel: Trace Precedents, Dependents, and Error Sources",
        "category": "Excel",
        "description": "Learn how to audit formulas in Excel so you can trace errors faster, understand dependencies, and reduce hidden spreadsheet risk.",
        "keywords": ["audit formulas Excel", "trace precedents Excel", "trace dependents Excel", "Excel error tracing", "Excel auditing"],
        "primary_intent": "Audit Excel formulas more effectively and systematically.",
        "search_type": "evergreen",
        "intro": [
            "Formula auditing matters because spreadsheet problems rarely announce themselves clearly. By the time a number looks wrong in a report, the real cause may be several references away.",
            "A good audit habit helps you find the source faster and reduces the chance of fixing the symptom instead of the underlying logic."
        ],
        "quick_answer": "Audit formulas by tracing where values come from, where they flow next, and which assumptions are easiest to break. Excel’s precedent and dependent tools help, but the bigger skill is thinking through the calculation path deliberately.",
        "use_when": [
            "A report looks wrong and you do not trust the chain behind it.",
            "You inherited a workbook from someone else.",
            "A model is becoming too important to leave unexamined.",
        ],
        "sections": [
            {"heading": "Start with the visible symptom", "paragraphs": ["Find the first result that is clearly wrong, then trace backwards. Jumping randomly through the workbook usually wastes time."]},
            {"heading": "Use precedents and dependents deliberately", "paragraphs": ["Precedents show what feeds a cell. Dependents show what a cell affects next. Together they help you map the risk path rather than inspecting cells blindly."]},
            {"heading": "Think about assumptions, not only references", "paragraphs": ["A formula can reference the right cells and still be wrong because the rule, threshold, or business assumption is wrong. Auditing is partly mathematical and partly contextual."]},
        ],
        "example": {"heading": "Worked example: margin report anomaly", "paragraphs": ["A margin percentage looks too high on the dashboard. Tracing precedents reveals that the revenue cell is fine but the cost range excludes one new cost category that was added later."]},
        "mistakes": ["Checking too many unrelated cells at once.", "Assuming the formula is wrong when the assumption is wrong.", "Fixing one display cell without tracing where the value flows next."],
        "instead": {"paragraphs": ["If the workbook issue is AI-generated logic specifically, read <a href=\"/blog/review-ai-generated-excel-formulas\">reviewing AI-generated formulas</a>. If you need faster formula construction, <a href=\"/blog/let-and-lambda-excel\">LET and LAMBDA</a> may help reduce future audit pain."]},
        "related_new": ["review-ai-generated-excel-formulas", "let-and-lambda-excel", "project-tracker-excel"],
        "related_old": ["claude-debug-formulas"],
        "cover_hook": "Audit the calculation path so you fix the source of the problem, not just the symptom.",
        "cover_cta": "Trace Errors Better",
        "cover_keywords": ["Audit", "Precedents", "Errors"],
        "cover_cue": "formula traces, dependency arrows, and spreadsheet-audit visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for auditing formulas in Excel, with dependency-trace and error-source visuals.",
        "sources": [],
    },
    {
        "slug": "flutter-testing-strategy-2026",
        "title": "Flutter Testing Strategy in 2026: Unit, Widget, Integration, and Goldens",
        "category": "Flutter",
        "description": "Learn how to choose the right mix of unit, widget, integration, and golden tests in Flutter without building a slow test suite no one trusts.",
        "keywords": ["Flutter testing strategy", "Flutter widget tests", "Flutter integration tests", "Flutter golden tests", "Flutter unit tests"],
        "primary_intent": "Build a balanced Flutter testing strategy for production apps.",
        "search_type": "evergreen",
        "intro": [
            "A bad test strategy creates two opposite failures: either you have too few tests and ship fearfully, or you have a slow unreliable suite that everyone learns to ignore.",
            "The practical goal is not maximum test count. It is confidence per minute of effort."
        ],
        "quick_answer": "Use unit tests for pure logic, widget tests for UI behaviour in isolation, integration tests for end-to-end journeys, and goldens when visual stability genuinely matters. The strongest strategy balances coverage, speed, and trust.",
        "use_when": [
            "Your app is growing and test decisions feel ad hoc.",
            "Teams are arguing over where each type of test belongs.",
            "You want better confidence without an unusable pipeline.",
        ],
        "sections": [
            {"heading": "Start with the cheapest trustworthy test", "paragraphs": ["The right first test is usually the cheapest one that can genuinely catch the failure you care about. That keeps the suite faster and the feedback loop more useful."]},
            {"heading": "Widget tests are often the workhorse", "paragraphs": ["In many Flutter apps, widget tests carry a lot of value because they can verify behaviour with less cost than full integration flows."]},
            {"heading": "Use integration and goldens selectively", "paragraphs": ["Integration tests and goldens are powerful, but they are also easier to overuse. Reach for them when the risk really justifies the cost and maintenance."]},
        ],
        "example": {"heading": "Worked example: checkout feature", "paragraphs": ["A checkout feature might use unit tests for pricing rules, widget tests for form validation and UI states, one or two integration tests for the main purchase flow, and goldens for high-value visual components that must stay stable."]},
        "mistakes": ["Using end-to-end tests for problems a widget test could catch faster.", "Keeping flaky tests that nobody trusts.", "Chasing coverage numbers without thinking about risk."],
        "instead": {"paragraphs": ["If the real issue is architecture and testability, go back to <a href=\"/blog/flutter-app-architecture-2026\">architecture</a>. If the UI is still changing heavily, <a href=\"/blog/flutter-widget-previewer\">Widget Previewer</a> can speed iteration before you lock in more visual tests."]},
        "related_new": ["flutter-app-architecture-2026", "flutter-widget-previewer", "flutter-form-validation-best-practices"],
        "related_old": ["flutter-state-management"],
        "cover_hook": "Choose the test that buys real confidence instead of the most impressive test label.",
        "cover_cta": "Test Flutter Wisely",
        "cover_keywords": ["Tests", "Widget", "Flutter"],
        "cover_cue": "test pyramids, device flows, and UI verification visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Flutter testing strategy in 2026, with testing-layer visuals.",
        "sources": [SOURCES["testing"]],
    },
    {
        "slug": "python-in-excel-beginners",
        "title": "Python in Excel for Beginners: The First 10 Things Worth Learning",
        "category": "AI + Excel",
        "description": "Learn the first practical things worth understanding about Python in Excel so you can move beyond hype and decide where it genuinely helps.",
        "keywords": ["Python in Excel beginners", "Python in Excel", "Excel Python guide", "Python Excel basics", "Excel analytics"],
        "primary_intent": "Get a practical beginner-friendly start with Python in Excel.",
        "search_type": "trend",
        "intro": [
            "Python in Excel is one of those features that attracts both excitement and confusion. Beginners often hear that it changes everything, while experienced spreadsheet users wonder whether it is worth the extra complexity.",
            "The sensible answer is to start with the few use cases where it clearly adds value, rather than trying to use Python for everything from day one."
        ],
        "notes": [
            "Availability can vary by version and channel. Treat this guide as current as of 1 April 2026 and check the Microsoft availability notes for your environment."
        ],
        "quick_answer": "Start with practical uses such as descriptive analysis, cleaning, plotting, and lightweight modelling where Python is obviously stronger than formulas. Keep ordinary Excel work in formulas and tables when that is already the better tool.",
        "use_when": [
            "You are comfortable with Excel and curious about where Python genuinely helps.",
            "You want practical starter use cases rather than theory.",
            "You need analytical power, not just a new feature to play with.",
        ],
        "sections": [
            {"heading": "Think in strengths, not in novelty", "paragraphs": ["Python is useful when the problem suits code-based analysis: richer statistics, more flexible data reshaping, plotting, or modelling. It is less useful when a simple Excel formula already solves the job cleanly."]},
            {"heading": "The first skills worth learning", "paragraphs": ["Start with reading data, filtering it, summarising it, plotting a result, and understanding how Python cells interact with workbook data. Those habits create far more value than memorising obscure syntax early on."]},
            {"heading": "Why beginners should stay practical", "paragraphs": ["Python in Excel becomes powerful when it complements a workbook. It becomes frustrating when you turn a clear spreadsheet task into an unnecessary coding exercise."]},
        ],
        "example": {"heading": "Worked example: a churn analysis starter", "paragraphs": ["A customer-success team wants a first look at churn patterns across segments. Excel tables store the source data, while Python handles a quick grouped analysis and a simple visual that would be slower to build with formulas alone."]},
        "mistakes": ["Trying to replace every formula with Python.", "Ignoring availability constraints in your Excel environment.", "Skipping basic table hygiene before sending data into Python."],
        "instead": {"paragraphs": ["If you need AI help more than code, go to <a href=\"/blog/copilot-excel-python-analysis\">Copilot in Excel with Python</a>. If you want to understand the in-grid Python surface itself, <a href=\"/blog/py-function-excel\">the PY function guide</a> is the next logical step."]},
        "related_new": ["py-function-excel", "copilot-excel-python-analysis", "format-data-for-copilot-excel"],
        "related_old": ["copilot-data-analysis"],
        "cover_hook": "Learn the small set of Python-in-Excel skills that actually create value before adding more complexity.",
        "cover_cta": "Start Python In Excel",
        "cover_keywords": ["Python", "Excel", "Starter"],
        "cover_cue": "Python cells, data tables, and beginner-friendly analytics visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Python in Excel for beginners, with Python cell and analytics visuals.",
        "sources": [SOURCES["python_availability"]],
    },
    {
        "slug": "protect-excel-workbook-collaboration",
        "title": "Protect an Excel Workbook Without Breaking Collaboration and Shared Editing",
        "category": "Excel",
        "description": "Learn how to protect an Excel workbook sensibly so formulas and structure stay safer without making collaboration more painful than necessary.",
        "keywords": ["protect Excel workbook", "Excel collaboration", "shared editing Excel", "protect formulas Excel", "Excel workbook security"],
        "primary_intent": "Protect Excel workbooks while keeping collaboration workable.",
        "search_type": "evergreen",
        "intro": [
            "Workbook protection often gets handled in one of two bad ways: either nothing is protected and important logic gets damaged, or everything is locked down so tightly that ordinary collaboration becomes painful.",
            "The practical goal is selective protection: keep high-risk logic safer while still letting the team update the parts they actually need."
        ],
        "quick_answer": "Protect what is costly to break, not everything indiscriminately. Lock formula and structure areas deliberately, keep input areas clear, and design the workbook so collaborators know what is safe to edit.",
        "use_when": [
            "Several people update the same workbook.",
            "Key formulas or structure keep getting overwritten.",
            "You want fewer accidental breakages without turning the file into a maze.",
        ],
        "sections": [
            {"heading": "Think about risk zones", "paragraphs": ["Input areas, calculations, summaries, and reference tables do not carry the same risk. Design the workbook so each zone is obvious, then protect the zones that are expensive to damage."]},
            {"heading": "Protection works best with clarity", "paragraphs": ["People collaborate better when the workbook makes edit boundaries visible. Good labels, input styling, and a sensible sheet structure reduce errors before protection settings even matter."]},
            {"heading": "Avoid over-protection", "paragraphs": ["If simple updates require constant unlocking or awkward workarounds, the workbook will train people to bypass the process entirely. Protection should reduce friction overall, not create new hidden workflows."]},
        ],
        "example": {"heading": "Worked example: a monthly budget workbook", "paragraphs": ["A finance workbook locks formula sheets and summary logic but leaves expense-entry tables open. Team members can update the data they own without risking the calculations that power the final report."]},
        "mistakes": ["Locking everything instead of designing clearer edit zones.", "Using protection as a substitute for workbook structure.", "Forgetting to communicate what collaborators can and cannot edit."],
        "instead": {"paragraphs": ["If the workbook is breaking because formulas are hard to understand rather than merely exposed, <a href=\"/blog/audit-formulas-excel\">formula auditing</a> and <a href=\"/blog/let-and-lambda-excel\">clearer formula design</a> may be the better next step."]},
        "related_new": ["audit-formulas-excel", "monthly-budget-spreadsheet-excel", "excel-tables-best-practices"],
        "related_old": ["data-validation"],
        "cover_hook": "Protect the logic that is costly to break, but keep the workbook usable for the people doing the work.",
        "cover_cta": "Protect Without Friction",
        "cover_keywords": ["Protect", "Workbook", "Collab"],
        "cover_cue": "locked logic zones, editable input areas, and collaboration-safe workbook visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for protecting an Excel workbook without breaking collaboration, with lock and collaboration visuals.",
        "sources": [],
    },
    {
        "slug": "py-function-excel",
        "title": "PY Function in Excel: What It Is, How It Works, and When to Use It",
        "category": "AI + Excel",
        "description": "Learn what the PY function in Excel is for, how it fits into Python in Excel workflows, and when it is worth using instead of ordinary formulas.",
        "keywords": ["PY function Excel", "Excel PY function", "Python in Excel function", "Excel Python", "use PY in Excel"],
        "primary_intent": "Understand what the PY function does in practical Excel work.",
        "search_type": "trend",
        "intro": [
            "The PY function matters because it makes Python feel more native inside Excel. Instead of treating Python like a distant add-on, you can work with it in a way that feels closer to the rest of the workbook.",
            "That does not mean every workbook should suddenly become Python-heavy. The useful question is where the PY function earns its place."
        ],
        "quick_answer": "Use the PY function when Python gives you a clearly better analytical or transformation path than standard Excel formulas. Keep ordinary spreadsheet logic in formulas when that remains the simpler and more transparent choice.",
        "use_when": [
            "A task is easier in Python than in formulas.",
            "The workbook already has a sensible table structure.",
            "You can still explain the result to colleagues who may not write Python themselves.",
        ],
        "sections": [
            {"heading": "Why the PY function is useful", "paragraphs": ["It lowers the friction between spreadsheet work and Python-based analysis. That helps when you want richer data handling without leaving the workbook environment."]},
            {"heading": "Where it earns its place", "paragraphs": ["The PY function is strongest for analysis, transformation, and calculations that would be awkward or brittle in formulas. It is weaker when a plain formula is already readable and stable."]},
            {"heading": "How to keep it team-friendly", "paragraphs": ["Use Python where the gain is obvious, document what it is doing, and avoid turning an otherwise simple workbook into a puzzle for the next person."]},
        ],
        "example": {"heading": "Worked example: grouping and plotting", "paragraphs": ["A workbook needs a grouped analysis with a quick visual. The PY function helps pull the table into Python logic for the analysis step, then returns the result in a way the rest of the workbook can still use."]},
        "mistakes": ["Using PY to show technical cleverness.", "Skipping workbook documentation around what the Python logic is doing.", "Ignoring whether colleagues can support the workbook later."],
        "instead": {"paragraphs": ["If you want the broader entry point first, start with <a href=\"/blog/python-in-excel-beginners\">Python in Excel for beginners</a>. If you need AI help on top of Python workflows, <a href=\"/blog/copilot-excel-python-analysis\">Copilot in Excel with Python</a> is the next step."]},
        "related_new": ["python-in-excel-beginners", "copilot-excel-python-analysis", "ai-forecasting-model-excel"],
        "related_old": ["copilot-data-analysis"],
        "cover_hook": "Use Python in the workbook when it adds clear analytical value, not simply because it is available.",
        "cover_cta": "Use The PY Function Wisely",
        "cover_keywords": ["PY", "Python", "Workbook"],
        "cover_cue": "Python cells, workbook returns, and analysis workflow visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for the PY function in Excel, with Python-in-workbook visuals.",
        "sources": [SOURCES["python_availability"]],
    },
    {
        "slug": "calendar-in-excel-automatic",
        "title": "How to Create a Calendar in Excel That Updates Automatically Every Month",
        "category": "Excel",
        "description": "Learn how to build an Excel calendar that updates automatically so you can reuse it for schedules, planning, and lightweight team coordination.",
        "keywords": ["calendar in Excel automatic", "Excel calendar", "automatic calendar Excel", "Excel planning calendar", "monthly calendar Excel"],
        "primary_intent": "Build a reusable Excel calendar that updates automatically.",
        "search_type": "evergreen",
        "intro": [
            "A reusable calendar is one of those spreadsheet projects that looks simple until you want it to stay useful month after month. The moment the calendar has to update cleanly, handle dates properly, and support planning work, the structure matters.",
            "The good news is that modern Excel makes this much easier than the old copy-and-edit approach."
        ],
        "quick_answer": "Build the calendar from a real month input and date logic rather than a hard-coded grid. Once the calendar is driven by dates, it becomes far easier to reuse for planning, attendance, or team scheduling.",
        "use_when": [
            "You need a reusable monthly planning layout.",
            "You want to avoid rebuilding the calendar by hand each month.",
            "You want a base sheet that later supports tracking or scheduling.",
        ],
        "sections": [
            {"heading": "Start with the month input", "paragraphs": ["A reusable calendar begins with one input that defines the month and year. Everything else should flow from date logic, not manual typing."]},
            {"heading": "Why date logic matters", "paragraphs": ["Once the grid is driven by real dates, you can format, highlight weekends, add events, or connect the calendar to attendance or project workflows more cleanly."]},
            {"heading": "Keep the calendar usable", "paragraphs": ["A calendar is not only a date exercise. It also needs space for notes, events, or markers, depending on the planning job it supports."]},
        ],
        "example": {"heading": "Worked example: a simple team planner", "paragraphs": ["A small team uses one calendar sheet to mark leave days, launches, and monthly reminders. The month changes from one input cell, and the calendar updates without rebuilding the layout."]},
        "mistakes": ["Hard-coding dates into the grid.", "Treating a one-off month view as if it were reusable.", "Ignoring what the calendar needs to support once the dates are correct."],
        "instead": {"paragraphs": ["If you need the calendar for a more specific workflow, the next best reads might be <a href=\"/blog/attendance-tracker-excel\">attendance tracking</a> or <a href=\"/blog/project-tracker-excel\">project tracking</a>."]},
        "related_new": ["attendance-tracker-excel", "project-tracker-excel", "monthly-budget-spreadsheet-excel"],
        "related_old": ["data-validation"],
        "cover_hook": "Build the calendar from date logic once so you stop rebuilding it manually every month.",
        "cover_cta": "Automate Calendar Updates",
        "cover_keywords": ["Calendar", "Dates", "Excel"],
        "cover_cue": "monthly grid, date logic, and planning-sheet visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for creating an automatic calendar in Excel, with date-grid and planning visuals.",
        "sources": [],
    },
    {
        "slug": "copilot-excel-python-analysis",
        "title": "Copilot in Excel With Python: Forecasting, Risk Analysis, and Deeper Reasoning",
        "category": "AI + Excel",
        "description": "Learn how Copilot and Python in Excel can work together for deeper analysis, and where you still need human judgement before trusting the result.",
        "keywords": ["Copilot Excel Python", "Python in Excel Copilot", "Excel forecasting AI", "Excel risk analysis AI", "Excel deeper reasoning"],
        "primary_intent": "Understand how Copilot and Python in Excel complement one another in analytical work.",
        "search_type": "trend",
        "intro": [
            "Copilot and Python in Excel are not rivals. In many analytical workflows, they solve different layers of the problem. Copilot can help frame, explore, or draft, while Python can handle richer analysis that would be awkward in formulas alone.",
            "The opportunity is real, but so is the risk of over-trusting a polished narrative that still needs analytical checking."
        ],
        "quick_answer": "Use Copilot to accelerate exploratory thinking and framing, then use Python in Excel where the analysis itself benefits from code-driven methods. Review both layers carefully before the result influences real decisions.",
        "use_when": [
            "You want both conversational assistance and deeper analytical power.",
            "The workbook already has clean tables and sensible inputs.",
            "You can review the assumptions behind the output before sharing it.",
        ],
        "sections": [
            {"heading": "Why the combination is useful", "paragraphs": ["Copilot helps shorten the route from question to draft approach. Python helps when the analysis itself needs more than ordinary formulas can deliver cleanly."]},
            {"heading": "Where the review burden increases", "paragraphs": ["When both AI assistance and coded analysis are involved, it becomes even more important to separate data quality, analytical method, and narrative interpretation rather than trusting the stack because it looks sophisticated."]},
            {"heading": "Best-fit use cases", "paragraphs": ["Forecasting, scenario work, richer descriptive analysis, and exploratory risk-style questions can benefit from the combination when the data is prepared well."]},
        ],
        "example": {"heading": "Worked example: demand forecast review", "paragraphs": ["A planning team uses Copilot to frame questions about demand volatility, then uses Python in Excel to run a deeper look at the historical pattern. The final forecast still gets a human review before it affects inventory planning."]},
        "mistakes": ["Treating Copilot output as proof of analytical quality.", "Skipping workbook preparation before adding Python.", "Combining two advanced tools without documenting the process."],
        "instead": {"paragraphs": ["If you are just starting, go to <a href=\"/blog/python-in-excel-beginners\">Python in Excel for beginners</a>. If the question is mainly about the Python surface in the sheet, <a href=\"/blog/py-function-excel\">the PY function guide</a> is more focused."]},
        "related_new": ["python-in-excel-beginners", "py-function-excel", "ai-forecasting-model-excel"],
        "related_old": ["copilot-data-analysis"],
        "cover_hook": "Use Copilot for framing and Python for deeper analysis, but keep judgement over the final decision.",
        "cover_cta": "Combine Copilot And Python",
        "cover_keywords": ["Copilot", "Python", "Analysis"],
        "cover_cue": "AI guidance, Python analysis, and forecasting visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Copilot in Excel with Python, with analysis and forecasting visuals.",
        "sources": [SOURCES["python_availability"], SOURCES["copilot_excel"]],
    },
    {
        "slug": "gantt-chart-excel",
        "title": "How to Make a Gantt Chart in Excel for Real Project Planning",
        "category": "Excel",
        "description": "Learn how to build a practical Gantt chart in Excel that is useful for real project planning rather than just looking like a template.",
        "keywords": ["Gantt chart Excel", "project planning Excel", "Excel Gantt chart", "project schedule Excel", "Excel planning"],
        "primary_intent": "Build a practical Excel Gantt chart for project planning.",
        "search_type": "evergreen",
        "intro": [
            "A Gantt chart in Excel can be either genuinely useful or quietly painful. The difference is not the chart itself. It is whether the underlying task structure, dates, and dependencies are clear enough to make the visual worth maintaining.",
            "If the sheet is only a pretty bar chart with unstable dates behind it, it will not help the project much."
        ],
        "quick_answer": "Build the plan as structured task data first, then create the Gantt view from that data. Excel works well for straightforward project plans when the schedule is not too dynamic and the team understands the limits.",
        "use_when": [
            "You need a simple project timeline in a tool everyone already has.",
            "The project is structured enough to define tasks and dates clearly.",
            "You want a visual schedule without extra software overhead.",
        ],
        "sections": [
            {"heading": "Start with task data, not bars", "paragraphs": ["A useful Gantt chart begins with tasks, owners, start dates, end dates, and status. The visual is only the output of that structure."]},
            {"heading": "Why Excel can work well enough", "paragraphs": ["For lightweight planning, Excel is familiar, easy to share, and good enough when the schedule does not need full project-software complexity."]},
            {"heading": "Know the limits", "paragraphs": ["If the project has heavy dependencies, resource planning, or constant re-sequencing, Excel may stop being the right tool before the chart itself looks wrong."]},
        ],
        "example": {"heading": "Worked example: website relaunch plan", "paragraphs": ["A small team tracks design, content, QA, and launch tasks in one table. The Gantt view gives stakeholders a clean timeline while the source sheet holds the editable task data."]},
        "mistakes": ["Building the visual before the task data is sound.", "Ignoring status and owner fields in the underlying plan.", "Treating Excel as full project-management software when the project is too complex."],
        "instead": {"paragraphs": ["If you need a broader planning workbook rather than a timeline view alone, <a href=\"/blog/project-tracker-excel\">project tracker in Excel</a> is the better next read."]},
        "related_new": ["project-tracker-excel", "sales-pipeline-tracker-excel", "calendar-in-excel-automatic"],
        "related_old": ["what-if-analysis"],
        "cover_hook": "Build the schedule data properly first so the Gantt chart stays useful instead of decorative.",
        "cover_cta": "Plan Projects Visually",
        "cover_keywords": ["Gantt", "Project", "Timeline"],
        "cover_cue": "timeline bars, task rows, and project-planning visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for making a Gantt chart in Excel, with project-timeline visuals.",
        "sources": [],
    },
    {
        "slug": "chatgpt-vs-claude-vs-copilot-vs-gemini-excel",
        "title": "ChatGPT vs Claude vs Copilot vs Gemini for Excel in 2026",
        "category": "AI + Excel",
        "description": "A practical comparison of ChatGPT, Claude, Copilot, and Gemini for Excel work in 2026, focused on task fit rather than brand hype.",
        "keywords": ["ChatGPT vs Claude vs Copilot vs Gemini Excel", "best AI for Excel", "Excel AI comparison", "Copilot vs ChatGPT Excel", "Claude Gemini Excel"],
        "primary_intent": "Choose the AI tool that best fits a specific Excel task.",
        "search_type": "trend",
        "intro": [
            "There is no single best AI for Excel because the task matters more than the brand. Formula drafting, workbook help, narration, in-product integration, and enterprise governance do not all point to the same winner.",
            "The honest comparison is not who wins on a poster. It is which tool fits which spreadsheet job with the least friction."
        ],
        "quick_answer": "Copilot wins when native Excel integration matters. ChatGPT and Claude are strong when you want flexible prompting outside the workbook. Gemini can be useful for general spreadsheet help and lighter AI-assisted work. The right answer depends on task fit, review needs, and access constraints.",
        "use_when": [
            "You want to pick one default tool for a team or workflow.",
            "Several AI tools seem capable and the differences feel fuzzy.",
            "You care about practical task fit more than marketing claims.",
        ],
        "sections": [
            {"heading": "When Copilot stands out", "paragraphs": ["Copilot’s biggest advantage is native Excel context. When in-workbook assistance matters, that integration can outweigh model-level differences."]},
            {"heading": "When ChatGPT or Claude fit better", "paragraphs": ["Outside the workbook, flexible prompting, longer explanations, and iterative reasoning can make ChatGPT or Claude attractive depending on the task and team preference."]},
            {"heading": "Where Gemini fits", "paragraphs": ["Gemini can still be useful for spreadsheet help, especially for users who already work in the wider Google ecosystem or want another general-purpose AI option for formula and analysis tasks."]},
        ],
        "example": {"heading": "Worked example: four common Excel jobs", "paragraphs": ["For one-off formulas, several tools may be good enough. For in-workbook charting or workbook actions, Copilot has the advantage. For long explanations of inherited logic, Claude or ChatGPT may feel more natural depending on the prompt style you prefer."]},
        "mistakes": ["Choosing purely on hype.", "Ignoring native integration and admin constraints.", "Using one tool for every job because the team is familiar with it."],
        "instead": {"paragraphs": ["If you already know you want native workbook help, go straight to <a href=\"/blog/agent-mode-in-excel\">Agent Mode</a> or <a href=\"/blog/copilot-function-excel\">the COPILOT function</a>."]},
        "related_new": ["copilot-function-excel", "agent-mode-in-excel", "create-lookups-with-copilot-excel"],
        "related_old": ["chatgpt-excel-guide"],
        "cover_hook": "Choose the AI tool that matches the spreadsheet job instead of looking for one universal winner.",
        "cover_cta": "Pick The Right Excel AI Tool",
        "cover_keywords": ["ChatGPT", "Claude", "Copilot"],
        "cover_cue": "AI tool comparison cards, spreadsheet tasks, and decision visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for ChatGPT vs Claude vs Copilot vs Gemini for Excel, with AI comparison visuals.",
        "sources": [SOURCES["copilot_excel"]],
    },
    {
        "slug": "inventory-tracker-excel",
        "title": "How to Build an Inventory Tracker in Excel That Stays Maintainable",
        "category": "Excel",
        "description": "Learn how to build an inventory tracker in Excel that stays clean, maintainable, and useful instead of becoming a brittle stock spreadsheet.",
        "keywords": ["inventory tracker Excel", "inventory sheet Excel", "stock tracker Excel", "Excel inventory management", "maintainable Excel tracker"],
        "primary_intent": "Build a practical Excel inventory tracker that remains maintainable.",
        "search_type": "evergreen",
        "intro": [
            "Inventory trackers often start as simple stock lists and then collapse under their own shortcuts. Duplicate rows, inconsistent item names, unclear units, and manual adjustments make the sheet hard to trust very quickly.",
            "A maintainable tracker starts with structure, not with colourful conditional formatting."
        ],
        "quick_answer": "Keep one clear items table, one movement or transactions table, and logic that makes stock position traceable. Excel can handle a lightweight inventory workflow well if the model stays disciplined.",
        "use_when": [
            "You need a straightforward inventory system without specialised software.",
            "The business is small enough that Excel still fits the workflow.",
            "You want the sheet to stay explainable to the next person.",
        ],
        "sections": [
            {"heading": "Separate items from movements", "paragraphs": ["A clean tracker usually needs an item master and a movement log. That makes stock levels traceable instead of relying on one frequently overwritten number."]},
            {"heading": "What makes the tracker maintainable", "paragraphs": ["Consistent item IDs, clear units, structured tables, and simple reporting views all matter more than decorative dashboard polish at the start."]},
            {"heading": "Know when Excel is enough", "paragraphs": ["Excel works well for lighter inventory needs, but once complexity, concurrency, or audit demands rise too far, it stops being the right system."]},
        ],
        "example": {"heading": "Worked example: small warehouse stock sheet", "paragraphs": ["A warehouse team tracks incoming, outgoing, and adjusted quantities in one movement table and keeps item details in a separate master. Summary formulas then calculate the current position without hiding the transaction history."]},
        "mistakes": ["Using one editable stock number with no transaction history.", "Leaving item names inconsistent across sheets.", "Trying to scale Excel beyond what the process can support."],
        "instead": {"paragraphs": ["If you need a more generic operational workbook, <a href=\"/blog/project-tracker-excel\">project tracking</a> or <a href=\"/blog/sales-pipeline-tracker-excel\">sales pipeline tracking</a> may be closer to your use case."]},
        "related_new": ["project-tracker-excel", "sales-pipeline-tracker-excel", "excel-tables-best-practices"],
        "related_old": ["clean-messy-data"],
        "cover_hook": "Track stock with a structure that explains quantity changes instead of hiding them.",
        "cover_cta": "Build Better Inventory Sheets",
        "cover_keywords": ["Inventory", "Stock", "Excel"],
        "cover_cue": "stock tables, movement logs, and warehouse-tracking visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for building an inventory tracker in Excel, with stock and movement visuals.",
        "sources": [],
    },
    {
        "slug": "review-ai-generated-excel-formulas",
        "title": "How to Review AI-Generated Excel Formulas Before You Trust Them",
        "category": "AI + Excel",
        "description": "Learn a practical review process for AI-generated Excel formulas so you can catch bad logic before it reaches the workbook or the report.",
        "keywords": ["review AI-generated Excel formulas", "Excel AI formula review", "Copilot formula review", "ChatGPT Excel formulas", "AI spreadsheet risk"],
        "primary_intent": "Review AI-generated formulas more safely before trusting them.",
        "search_type": "evergreen",
        "intro": [
            "The problem with AI-generated formulas is rarely syntax alone. The dangerous formulas are the ones that run, return a value, and quietly apply the wrong business logic.",
            "That is why formula review needs its own workflow. The right question is not did AI generate a formula, but can I prove this formula is doing what the workbook actually needs."
        ],
        "quick_answer": "Review the references, logic, blanks handling, edge cases, and known sample rows before you trust an AI-generated formula. Treat it like junior draft work that still needs a human check.",
        "use_when": [
            "AI drafted a formula that will influence reporting or decisions.",
            "The formula touches several columns or business rules.",
            "You want a repeatable review habit rather than one-off guesswork.",
        ],
        "sections": [
            {"heading": "Check the reference logic first", "paragraphs": ["The first review step is whether the formula points to the right columns, ranges, and match rules. A tidy formula can still be wrong if the references are wrong."]},
            {"heading": "Then test business cases", "paragraphs": ["Use a few rows where you already know the expected answer. That makes silent logic errors much easier to catch than reading the syntax in the abstract."]},
            {"heading": "Keep AI in the draft role", "paragraphs": ["The healthiest workflow is to let AI draft faster and let a human confirm fit. That mindset reduces the urge to trust output because it arrived quickly."]},
        ],
        "example": {"heading": "Worked example: commission formula", "paragraphs": ["AI drafts a commission formula that looks sensible, but review shows it ignores one special commission band. A quick test against known sample rows catches the issue before the formula reaches the monthly report."]},
        "mistakes": ["Reviewing only syntax.", "Skipping sample rows because the formula returns values.", "Treating AI speed as a reason to relax review standards."],
        "instead": {"paragraphs": ["If the task is wider workbook diagnosis, <a href=\"/blog/audit-formulas-excel\">formula auditing</a> is the better lens. If you are still at the prompt stage, <a href=\"/blog/generate-formula-columns-copilot-excel\">formula columns with Copilot</a> may help you reduce bad drafts in the first place."]},
        "related_new": ["generate-formula-columns-copilot-excel", "generate-single-cell-formulas-copilot-excel", "audit-formulas-excel"],
        "related_old": ["claude-debug-formulas"],
        "cover_hook": "Treat AI formulas like junior drafts and review the business logic before they reach the report.",
        "cover_cta": "Review Formula Logic",
        "cover_keywords": ["Review", "AI", "Formulas"],
        "cover_cue": "formula checks, review marks, and spreadsheet-risk visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for reviewing AI-generated Excel formulas, with formula-check and risk visuals.",
        "sources": [],
    },
    {
        "slug": "attendance-tracker-excel",
        "title": "How to Create an Attendance Tracker in Excel for Teams, Schools, or Training",
        "category": "Excel",
        "description": "Learn how to create an attendance tracker in Excel that stays clear and reusable for teams, schools, workshops, or training cohorts.",
        "keywords": ["attendance tracker Excel", "attendance sheet Excel", "team attendance Excel", "training attendance Excel", "Excel tracker"],
        "primary_intent": "Build a reusable attendance tracker in Excel.",
        "search_type": "evergreen",
        "intro": [
            "Attendance trackers are simple until they are not. Once you need monthly reuse, leave codes, totals, or different audiences such as teams and training groups, the sheet can become messy quickly.",
            "A good tracker stays simple because the structure is deliberate from the start."
        ],
        "quick_answer": "Build the tracker from a clear roster, a clean date structure, and a small set of attendance codes that the team actually understands. Keep the source sheet tidy and let summaries sit on top rather than mixing everything together.",
        "use_when": [
            "You need a reusable attendance sheet in Excel.",
            "The process is small enough that a spreadsheet still fits.",
            "You want a tracker that can later feed summaries or charts.",
        ],
        "sections": [
            {"heading": "Start with the roster", "paragraphs": ["A clear roster with stable IDs or names makes the tracker easier to reuse. The attendance grid should not also be the place where identity gets cleaned up."]},
            {"heading": "Keep codes simple", "paragraphs": ["Use a small code set such as present, absent, leave, or late if those are the states you actually need. The simpler the code system, the more reliable the data entry tends to be."]},
            {"heading": "Separate entry from summary", "paragraphs": ["The entry sheet should stay uncluttered. Totals, percentages, and charts belong on a summary view rather than inside the core attendance grid."]},
        ],
        "example": {"heading": "Worked example: workshop cohort tracker", "paragraphs": ["A training provider keeps one roster sheet and one monthly attendance grid. Summary formulas then calculate overall attendance by participant and by session without making the entry sheet harder to update."]},
        "mistakes": ["Mixing too many codes and notes into the entry grid.", "Using the same sheet for raw entry and all summaries.", "Changing participant naming conventions midstream."],
        "instead": {"paragraphs": ["If your tracker is becoming more like a planner, <a href=\"/blog/calendar-in-excel-automatic\">an automatic calendar</a> may help. If it is becoming more operational than attendance-specific, <a href=\"/blog/project-tracker-excel\">project tracking</a> could be closer."]},
        "related_new": ["calendar-in-excel-automatic", "project-tracker-excel", "monthly-budget-spreadsheet-excel", "protect-excel-workbook-collaboration", "excel-ai-for-hr-teams"],
        "related_old": ["data-validation"],
        "cover_hook": "Keep attendance tracking simple enough to update consistently and structured enough to summarise cleanly.",
        "cover_cta": "Track Attendance Better",
        "cover_keywords": ["Attendance", "Tracker", "Excel"],
        "cover_cue": "attendance grids, roster sheets, and summary visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for creating an attendance tracker in Excel, with roster and attendance-grid visuals.",
        "sources": [],
    },
    {
        "slug": "ai-power-query-m-code",
        "title": "Use AI to Write and Fix Power Query M Code for Excel",
        "category": "AI + Excel",
        "description": "Learn how AI can help with Power Query M code in Excel, where it saves time, and how to review the result before trusting the transformation logic.",
        "keywords": ["AI Power Query M code", "Power Query AI Excel", "write M code with AI", "fix Power Query M code", "Excel Power Query AI"],
        "primary_intent": "Use AI to accelerate Power Query M code work more safely.",
        "search_type": "evergreen",
        "intro": [
            "Power Query M is powerful, but it can feel verbose and opaque when you do not write it every day. That makes it a strong candidate for AI assistance, especially when you want a first draft or help debugging a stubborn step.",
            "The trap is obvious: transformation code can look plausible while quietly changing the data in the wrong way."
        ],
        "quick_answer": "Use AI to draft or troubleshoot M code faster, but review each transformation step against the intended data outcome. The most reliable workflow is to let AI help you write or explain the query, not to trust the final transformation blindly.",
        "use_when": [
            "You know the transformation you want but do not want to write the M from scratch.",
            "A query step is failing and you need help diagnosing it.",
            "You can compare the transformed output with the intended result.",
        ],
        "sections": [
            {"heading": "Where AI helps most", "paragraphs": ["AI is particularly useful when translating plain-English transformation intent into first-pass M code or explaining what an existing step is doing."]},
            {"heading": "Why output review still matters", "paragraphs": ["The real check is not whether the code compiles. It is whether the transformed table still matches the intended business meaning after each step."]},
            {"heading": "A sensible workflow", "paragraphs": ["Describe the source and target clearly, ask AI for the draft or fix, then inspect both the query steps and the resulting table before the query becomes part of production reporting."]},
        ],
        "example": {"heading": "Worked example: cleaning a monthly export", "paragraphs": ["An analyst needs to remove header noise, split one combined field, standardise dates, and filter cancelled rows. AI can draft the M steps quickly, but the analyst still checks the output table against the original brief."]},
        "mistakes": ["Trusting code because it runs.", "Failing to describe the target output clearly in the prompt.", "Skipping result review because the query preview looks tidy."],
        "instead": {"paragraphs": ["If the data problem can be solved with regular Excel structure, <a href=\"/blog/excel-tables-best-practices\">better tables</a> may be simpler. If the problem is broader data cleaning, <a href=\"/blog/power-query-guide\">Power Query fundamentals</a> still matter."]},
        "related_new": ["format-data-for-copilot-excel", "review-ai-generated-excel-formulas", "inventory-tracker-excel"],
        "related_old": ["power-query-guide"],
        "cover_hook": "AI can draft M code faster, but the transformed data still needs a human who knows what correct looks like.",
        "cover_cta": "Review M Code Carefully",
        "cover_keywords": ["Power Query", "M Code", "AI"],
        "cover_cue": "query steps, transformed tables, and AI-assisted code visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for using AI to write and fix Power Query M code in Excel, with query-step visuals.",
        "sources": [],
    },
    {
        "slug": "project-tracker-excel",
        "title": "How to Build a Project Tracker in Excel Without Turning It Into a Mess",
        "category": "Excel",
        "description": "Learn how to build a practical project tracker in Excel that stays maintainable instead of collapsing into status clutter and hidden logic.",
        "keywords": ["project tracker Excel", "Excel project tracker", "project management Excel", "maintainable project tracker", "Excel planning tracker"],
        "primary_intent": "Build a maintainable project tracker in Excel.",
        "search_type": "evergreen",
        "intro": [
            "Project trackers go bad slowly. They begin as a helpful list, then attract extra columns, inconsistent statuses, manual colour signals, and unclear ownership until nobody is quite sure what the sheet is actually telling them.",
            "A useful tracker is not the one with the most fields. It is the one that keeps project status clear with the least confusion."
        ],
        "quick_answer": "Build the tracker around a stable task list, sensible status values, clear owners, dates that mean something, and summaries that sit on top of the source rather than inside it. Keep the system simple enough that people will actually update it consistently.",
        "use_when": [
            "A team needs a lightweight project tracker in a familiar tool.",
            "The work is structured enough to define owners and statuses clearly.",
            "You want useful visibility without full project software overhead.",
        ],
        "sections": [
            {"heading": "What the source table should hold", "paragraphs": ["Core task, owner, status, start date, due date, and one or two priority fields are usually enough. If every task needs five notes columns, the tracker is already drifting."]},
            {"heading": "Why status discipline matters", "paragraphs": ["In progress, blocked, done, and not started often work better than a clever taxonomy. A smaller status system usually produces more honest updates."]},
            {"heading": "Keep summaries separate", "paragraphs": ["Use formulas or charts above the tracker rather than mixing summary logic into the entry rows. That keeps data entry cleaner and the reporting view easier to change."]},
        ],
        "example": {"heading": "Worked example: content launch plan", "paragraphs": ["A marketing team tracks blog, design, review, and publishing tasks in one source table. A summary section then shows items due this week, blocked tasks, and completion by owner."]},
        "mistakes": ["Tracking too many fields that nobody updates consistently.", "Using vague status labels that mean different things to different people.", "Mixing reporting formulas into the raw task table."],
        "instead": {"paragraphs": ["If you need a visual schedule, <a href=\"/blog/gantt-chart-excel\">a Gantt chart</a> may be the better presentation layer. If the workflow is sales-specific, <a href=\"/blog/sales-pipeline-tracker-excel\">a pipeline tracker</a> will fit better."]},
        "related_new": ["gantt-chart-excel", "sales-pipeline-tracker-excel", "calendar-in-excel-automatic"],
        "related_old": ["what-if-analysis"],
        "cover_hook": "Track only what the team will genuinely maintain, then build reporting on top of that clean core.",
        "cover_cta": "Build Cleaner Project Trackers",
        "cover_keywords": ["Project", "Tracker", "Excel"],
        "cover_cue": "task boards, due dates, and tracker-summary visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for building a project tracker in Excel, with task and status visuals.",
        "sources": [],
    },
    {
        "slug": "ai-forecasting-model-excel",
        "title": "Build a Forecasting Model in Excel With AI Assistance Step by Step",
        "category": "AI + Excel",
        "description": "Learn how AI can help you build an Excel forecasting model faster while still keeping the assumptions and logic reviewable.",
        "keywords": ["AI forecasting model Excel", "Excel forecast AI", "build forecasting model Excel", "AI Excel planning", "Excel modelling with AI"],
        "primary_intent": "Use AI to speed up forecasting-model work in Excel without losing control of assumptions.",
        "search_type": "evergreen",
        "intro": [
            "AI can help you build a forecasting model faster, but speed only matters if the assumptions stay reviewable. Forecasting work breaks when the model looks polished but the business logic underneath is unclear or weak.",
            "The right use of AI is to accelerate structure, scenario framing, and repetitive setup while a human still owns the assumptions."
        ],
        "quick_answer": "Use AI to accelerate the mechanics of forecasting models, not to replace judgement over drivers, assumptions, and scenario logic. The model becomes useful when the structure is clear enough to defend, not when it merely appears complete quickly.",
        "use_when": [
            "You need to build a first-pass forecast more quickly.",
            "The main uncertainty is around drivers and scenarios, not spreadsheet mechanics alone.",
            "You can still review every major assumption before using the output.",
        ],
        "sections": [
            {"heading": "Where AI genuinely helps", "paragraphs": ["AI is useful for outlining model sections, suggesting formula patterns, drafting scenario tables, and helping you think about which drivers to test."]},
            {"heading": "What must stay human-owned", "paragraphs": ["Revenue assumptions, seasonality judgement, risk adjustments, and business context must still be owned by the analyst or operator using the model."]},
            {"heading": "How to keep the model reviewable", "paragraphs": ["Separate assumptions, calculations, and outputs. Label the scenarios clearly and avoid burying AI-generated logic where stakeholders cannot inspect it."]},
        ],
        "example": {"heading": "Worked example: demand planning model", "paragraphs": ["A small retailer wants a first-pass demand forecast for the next quarter. AI helps draft scenario sections and formula structure, while the planner still decides the growth, seasonality, and downside assumptions."]},
        "mistakes": ["Treating AI-generated assumptions as if they were evidence.", "Combining assumptions and calculations on one messy sheet.", "Skipping scenario definitions because the draft model looks detailed enough."],
        "instead": {"paragraphs": ["If you need the Python side of deeper analysis, read <a href=\"/blog/copilot-excel-python-analysis\">Copilot in Excel with Python</a>. If you need stronger finance-model basics first, <a href=\"/blog/financial-modelling\">financial modelling in Excel</a> is still relevant."]},
        "related_new": ["copilot-excel-python-analysis", "review-ai-generated-excel-formulas", "monthly-budget-spreadsheet-excel"],
        "related_old": ["financial-modelling"],
        "cover_hook": "Use AI to speed up model setup, but keep the assumptions visible enough to defend.",
        "cover_cta": "Model Forecasts Better",
        "cover_keywords": ["Forecast", "Model", "AI"],
        "cover_cue": "forecast curves, scenario tables, and reviewable model visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for building a forecasting model in Excel with AI assistance, with forecast and scenario visuals.",
        "sources": [],
    },
    {
        "slug": "sales-pipeline-tracker-excel",
        "title": "How to Build a Sales Pipeline Tracker in Excel for Small Teams",
        "category": "Excel",
        "description": "Learn how to build a simple sales pipeline tracker in Excel that small teams can maintain without turning it into a CRM lookalike.",
        "keywords": ["sales pipeline tracker Excel", "pipeline sheet Excel", "Excel sales tracker", "small team sales pipeline", "Excel CRM alternative"],
        "primary_intent": "Build a small-team sales pipeline tracker in Excel.",
        "search_type": "evergreen",
        "intro": [
            "A sales pipeline tracker in Excel works best when it stays honest about what it is. It is a lightweight visibility tool, not a full CRM. That is good news for small teams, because the simpler the structure, the more likely it is to stay updated.",
            "The aim is clarity around stage, owner, value, next step, and close timing without burying the team in admin."
        ],
        "quick_answer": "Keep the tracker centred on deals, stages, owners, values, expected close dates, and the next action. If you try to turn Excel into a full CRM, the sheet usually becomes bloated faster than it becomes useful.",
        "use_when": [
            "A small team needs quick pipeline visibility.",
            "The workflow is too light to justify heavier software right now.",
            "You want a tracker that supports action, not just reporting.",
        ],
        "sections": [
            {"heading": "What the pipeline really needs", "paragraphs": ["A practical pipeline tracker usually needs one row per deal, a clear stage, one owner, expected value, expected close date, and one next-step field."]},
            {"heading": "Why stage discipline matters", "paragraphs": ["Stages should represent genuine movement, not vague optimism. If stages are too fuzzy, the tracker stops helping forecast quality very quickly."]},
            {"heading": "Keep follow-up visible", "paragraphs": ["The next action and date matter because a pipeline is not only a reporting tool. It should also help the team decide what to do next."]},
        ],
        "example": {"heading": "Worked example: a five-person sales team", "paragraphs": ["A small B2B team keeps one deal table in Excel with stage, owner, next action, close month, and expected value. A summary sheet then shows stage totals and deals with no follow-up date set."]},
        "mistakes": ["Turning the tracker into a mini-CRM with too many fields.", "Using stages that are too vague to forecast from.", "Forgetting that a pipeline should prompt next action, not only totals."],
        "instead": {"paragraphs": ["If the tracking need is broader operations rather than sales-specific, <a href=\"/blog/project-tracker-excel\">project tracking</a> may be closer. If the need is more strategic sales operations, <a href=\"/blog/excel-ai-for-sales-ops\">Excel + AI for Sales Ops</a> is the better companion guide."]},
        "related_new": ["project-tracker-excel", "excel-ai-for-sales-ops", "inventory-tracker-excel"],
        "related_old": ["dynamic-dashboards"],
        "cover_hook": "Track stages and next actions clearly enough that the pipeline drives behaviour, not just a report.",
        "cover_cta": "Build A Better Pipeline Sheet",
        "cover_keywords": ["Pipeline", "Sales", "Excel"],
        "cover_cue": "deal stages, action dates, and pipeline-summary visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for building a sales pipeline tracker in Excel, with deal-stage visuals.",
        "sources": [],
    },
    {
        "slug": "excel-ai-for-accountants",
        "title": "Excel + AI for Accountants: Reconciliations, Variance Reviews, and Close Prep",
        "category": "AI + Excel",
        "description": "Learn practical Excel and AI workflows for accountants, focused on reconciliations, variance review, and close preparation rather than vague automation claims.",
        "keywords": ["Excel AI for accountants", "AI reconciliations Excel", "variance analysis Excel AI", "close prep Excel AI", "accounting Excel workflows"],
        "primary_intent": "Use Excel and AI together in accounting workflows more practically.",
        "search_type": "evergreen",
        "intro": [
            "Accountants do not need AI hype. They need workflows that reduce review time without weakening control. That is why the best Excel-and-AI use cases in accounting are not flashy. They are practical: reconcile faster, explain variances more quickly, and prepare close work with fewer avoidable manual steps.",
            "The test is simple: does the workflow save time while keeping the review trail clear enough for real accounting work?"
        ],
        "quick_answer": "AI is most useful in accounting when it helps frame checks, summarise patterns, draft first-pass explanations, or accelerate repetitive preparation. It is least useful where deterministic control and auditability must remain absolute.",
        "use_when": [
            "You want to reduce preparation or review time without relaxing control.",
            "The workbook is already structured and reviewable.",
            "You are using AI as an assistant, not as the final approver.",
        ],
        "sections": [
            {"heading": "Where AI fits cleanly", "paragraphs": ["Reconciliation support, variance narration, anomaly triage, and close-prep checklists are strong candidates because they still leave the accountant in control of the actual sign-off."]},
            {"heading": "Where caution rises sharply", "paragraphs": ["Anything that depends on strict deterministic logic, formal audit evidence, or complex accounting treatment still needs human review and often a more traditional workflow."]},
            {"heading": "How to keep the review trail clear", "paragraphs": ["Label AI-assisted outputs, keep the underlying numbers separate from the commentary layer, and document the prompts or review steps that produced the first-pass output."]},
        ],
        "example": {"heading": "Worked example: month-end variance pack", "paragraphs": ["A finance team uses Excel to compare actuals with budget and prior month. AI helps draft first-pass commentary on unusual movements, but the team still reviews the drivers and edits the final narrative before circulation."]},
        "mistakes": ["Treating AI commentary as final accounting judgement.", "Mixing reviewed and unreviewed outputs in one sheet without labels.", "Using AI to hide weak workbook structure."],
        "instead": {"paragraphs": ["If you need a broader forecasting workflow, <a href=\"/blog/ai-forecasting-model-excel\">AI forecasting models</a> may be relevant. If the issue is formula reliability, <a href=\"/blog/review-ai-generated-excel-formulas\">review AI-generated formulas</a> is the safer next step."]},
        "related_new": ["ai-forecasting-model-excel", "review-ai-generated-excel-formulas", "copilot-excel-python-analysis"],
        "related_old": ["financial-modelling"],
        "cover_hook": "Use AI where it shortens accounting review work without weakening the control trail.",
        "cover_cta": "Use AI More Carefully In Accounting",
        "cover_keywords": ["Accountants", "Variance", "Close"],
        "cover_cue": "close packs, reconciliation sheets, and finance-review visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Excel and AI for accountants, with reconciliation and close-prep visuals.",
        "sources": [],
    },
    {
        "slug": "monthly-budget-spreadsheet-excel",
        "title": "How to Build a Monthly Budget Spreadsheet in Excel From Scratch",
        "category": "Excel",
        "description": "Learn how to build a monthly budget spreadsheet in Excel from scratch so it stays useful, readable, and easy to update month after month.",
        "keywords": ["monthly budget spreadsheet Excel", "budget sheet Excel", "Excel budget template", "personal budget Excel", "business budget Excel"],
        "primary_intent": "Build a practical monthly budget spreadsheet in Excel.",
        "search_type": "evergreen",
        "intro": [
            "A budget spreadsheet only helps if it is simple enough to update honestly. The best budget sheet is not the one with the most tabs. It is the one that makes income, fixed costs, variable costs, and remaining cash easy to understand at a glance.",
            "That is why building from scratch can be better than copying a complicated template you never fully understand."
        ],
        "quick_answer": "Start with clear income and expense categories, keep one month view understandable, and separate the data-entry area from the summary area. Good budgets are driven by clarity and consistency, not by over-engineering.",
        "use_when": [
            "You want a budget you can genuinely maintain.",
            "Existing templates feel cluttered or opaque.",
            "You need a base sheet that can later support analysis or forecasting.",
        ],
        "sections": [
            {"heading": "Start with categories you will actually use", "paragraphs": ["The best category list is not the longest one. It is the one that reflects how you or the team really track money."]},
            {"heading": "Separate entry from summary", "paragraphs": ["Enter transactions or monthly amounts in one clear area, then let totals and remaining balances sit in a separate summary view."]},
            {"heading": "Why simplicity wins", "paragraphs": ["A budget that is easy to update will usually outperform a fancy budget that nobody keeps current after two weeks."]},
        ],
        "example": {"heading": "Worked example: small-business monthly budget", "paragraphs": ["A small business tracks sales income, payroll, software, marketing, rent, and variable delivery costs in one clean table. Summary formulas then show planned versus actual and the remaining monthly cushion."]},
        "mistakes": ["Using categories nobody can remember to update.", "Mixing calculations directly into raw entry rows.", "Chasing polish before the structure is stable."],
        "instead": {"paragraphs": ["If you need a more finance-specific planning model, <a href=\"/blog/financial-modelling\">financial modelling</a> may be more suitable. If you want loan planning specifically, <a href=\"/blog/amortization-schedule-excel\">an amortisation schedule</a> is the better next read."]},
        "related_new": ["amortization-schedule-excel", "calendar-in-excel-automatic", "project-tracker-excel"],
        "related_old": ["financial-modelling"],
        "cover_hook": "Build the budget clearly enough that updating it every month feels possible, not exhausting.",
        "cover_cta": "Create A Clear Budget Sheet",
        "cover_keywords": ["Budget", "Monthly", "Excel"],
        "cover_cue": "budget rows, summary totals, and monthly cash visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for building a monthly budget spreadsheet in Excel, with budget and cashflow visuals.",
        "sources": [],
    },
    {
        "slug": "excel-ai-for-hr-teams",
        "title": "Excel + AI for HR Teams: Hiring Trackers, Attrition Analysis, and Reporting",
        "category": "AI + Excel",
        "description": "Learn practical Excel and AI workflows for HR teams, focused on hiring trackers, attrition analysis, and reporting that still needs human judgement.",
        "keywords": ["Excel AI HR", "HR reporting Excel AI", "attrition analysis Excel AI", "hiring tracker Excel AI", "HR workflow AI"],
        "primary_intent": "Use Excel and AI together in practical HR workflows.",
        "search_type": "evergreen",
        "intro": [
            "HR work is full of spreadsheet-heavy reporting, but it also involves sensitive interpretation. That means AI can be useful, yet it should be used carefully and transparently rather than as a hidden decision engine.",
            "The strongest Excel-and-AI HR workflows speed up preparation and pattern review while keeping people decisions firmly human."
        ],
        "quick_answer": "Use AI in HR spreadsheets for first-pass summaries, tracker cleanup, pattern spotting, and reporting support. Keep human review central anywhere interpretation could affect real people decisions.",
        "use_when": [
            "The team spends too much time on repetitive spreadsheet preparation.",
            "You need first-pass insight from structured HR data.",
            "You can keep review, sensitivity, and privacy expectations clear.",
        ],
        "sections": [
            {"heading": "Where AI fits well in HR spreadsheets", "paragraphs": ["Hiring trackers, interview status summaries, attrition reporting, and first-pass reporting commentary are often workable AI-assisted tasks because they still leave final judgement to the HR team."]},
            {"heading": "Where caution matters most", "paragraphs": ["Anything close to candidate judgement, employee-sensitive interpretation, or policy-driven decisions needs stronger review and clear boundaries."]},
            {"heading": "How to keep the workflow responsible", "paragraphs": ["Use structured tables, label AI-assisted outputs, and make sure managers understand which fields are draft support and which are reviewed conclusions."]},
        ],
        "example": {"heading": "Worked example: quarterly attrition review", "paragraphs": ["An HR team uses Excel to compare attrition by department, tenure band, and month. AI helps draft the first narrative about visible patterns, but the team reviews the data and wording before it reaches leadership."]},
        "mistakes": ["Letting AI commentary sound more certain than the data supports.", "Using unlabelled AI outputs in sensitive HR reporting.", "Skipping privacy and governance checks because the workflow feels internal."],
        "instead": {"paragraphs": ["If the main task is operational reporting rather than people reporting, <a href=\"/blog/excel-ai-for-sales-ops\">Sales Ops workflows</a> or <a href=\"/blog/excel-ai-for-accountants\">accounting workflows</a> may be better comparisons."]},
        "related_new": ["attendance-tracker-excel", "excel-ai-for-sales-ops", "review-ai-generated-excel-formulas"],
        "related_old": ["excel-ai-prompts"],
        "cover_hook": "Use AI to reduce reporting drag in HR, but keep people decisions and sensitive interpretation clearly human.",
        "cover_cta": "Use AI Carefully In HR",
        "cover_keywords": ["HR", "Attrition", "Reporting"],
        "cover_cue": "hiring trackers, reporting sheets, and HR-analysis visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Excel and AI for HR teams, with hiring and reporting visuals.",
        "sources": [],
    },
    {
        "slug": "amortization-schedule-excel",
        "title": "How to Create an Amortization Schedule in Excel With Extra Payment Scenarios",
        "category": "Excel",
        "description": "Learn how to create an amortisation schedule in Excel, including extra payment scenarios that make the sheet more useful for real planning.",
        "keywords": ["amortization schedule Excel", "amortisation schedule Excel", "loan schedule Excel", "extra payments Excel", "Excel loan planning"],
        "primary_intent": "Build an amortisation schedule in Excel that supports extra-payment scenarios.",
        "search_type": "evergreen",
        "intro": [
            "An amortisation schedule is one of the clearest examples of Excel being useful for real planning. Once you can see how interest, principal, and balance behave over time, the loan stops feeling abstract.",
            "The schedule becomes much more practical when you can test extra-payment scenarios rather than only the default repayment path."
        ],
        "quick_answer": "Build the schedule from the loan inputs, calculate each period clearly, and keep extra-payment logic explicit rather than hidden. That makes the model more useful and easier to trust when you test scenarios.",
        "use_when": [
            "You want to understand loan repayment behaviour in detail.",
            "You need to test one or more extra-payment scenarios.",
            "You want a transparent planning sheet rather than a black-box calculator.",
        ],
        "sections": [
            {"heading": "Start with the core loan inputs", "paragraphs": ["Principal, rate, term, frequency, and payment calculation should be visible and easy to change. Hidden assumptions make the schedule harder to trust."]},
            {"heading": "Why extra payments should stay explicit", "paragraphs": ["Extra-payment logic is where the schedule becomes useful for planning. Keep that input visible so the user understands how and why the loan finishes earlier."]},
            {"heading": "What makes the schedule trustworthy", "paragraphs": ["Clear period calculations, running balance checks, and obvious scenario inputs make the model easier to validate than a sheet with buried shortcuts."]},
        ],
        "example": {"heading": "Worked example: mortgage overpayment plan", "paragraphs": ["A borrower models a monthly mortgage payment and then tests an additional fixed monthly overpayment. The schedule shows how the balance falls faster and how total interest changes over time."]},
        "mistakes": ["Hiding key assumptions.", "Hard-coding scenario values into the calculation area.", "Using a schedule you cannot explain line by line."],
        "instead": {"paragraphs": ["If the broader need is monthly cash planning, <a href=\"/blog/monthly-budget-spreadsheet-excel\">a monthly budget spreadsheet</a> may help more."]},
        "related_new": ["monthly-budget-spreadsheet-excel", "calendar-in-excel-automatic", "ai-forecasting-model-excel"],
        "related_old": ["financial-modelling"],
        "cover_hook": "Make loan repayment visible enough that extra-payment choices become easier to understand and compare.",
        "cover_cta": "Model Loan Paydown Clearly",
        "cover_keywords": ["Amortisation", "Loan", "Excel"],
        "cover_cue": "loan tables, declining balances, and extra-payment visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for creating an amortisation schedule in Excel, with loan and paydown visuals.",
        "sources": [],
    },
    {
        "slug": "excel-ai-for-sales-ops",
        "title": "Excel + AI for Sales Ops: Pipeline Cleanup, Forecasts, and Territory Reporting",
        "category": "AI + Excel",
        "description": "Learn practical Excel and AI workflows for Sales Ops, focused on pipeline cleanup, forecasting support, and territory reporting.",
        "keywords": ["Excel AI Sales Ops", "pipeline cleanup AI Excel", "territory reporting Excel AI", "sales forecast Excel AI", "Sales Ops workflows"],
        "primary_intent": "Use Excel and AI together in practical Sales Ops workflows.",
        "search_type": "evergreen",
        "intro": [
            "Sales Ops teams rarely need AI theatre. They need cleaner pipeline data, faster reporting, better first-pass forecasting support, and fewer manual cycles in territory or inspection work.",
            "That makes Excel plus AI a practical combination when the workbook is already the working surface and the team still reviews the outputs carefully."
        ],
        "quick_answer": "AI helps most in Sales Ops when it speeds up pipeline cleanup, first-pass commentary, tracker review, or reporting preparation. It helps least where the process needs disciplined ownership, not merely faster prose.",
        "use_when": [
            "Pipeline hygiene and reporting prep consume too much time.",
            "The workbook structure is good enough to support reviewable outputs.",
            "The team wants faster first drafts rather than unreviewed automation.",
        ],
        "sections": [
            {"heading": "Best-fit Sales Ops use cases", "paragraphs": ["Pipeline cleanup, stage review, forecast commentary, territory report preparation, and anomaly spotting are often useful AI-assisted tasks because they still leave the team in control of the final output."]},
            {"heading": "Where caution still matters", "paragraphs": ["AI should not replace clear sales-process ownership. If the pipeline stages are messy or the underlying data is inconsistent, AI only speeds up the confusion."]},
            {"heading": "How to keep the workflow reliable", "paragraphs": ["Clean tables, labelled AI outputs, and simple review routines matter far more than fancy prompts once the process becomes recurring."]},
        ],
        "example": {"heading": "Worked example: quarter-end territory pack", "paragraphs": ["A Sales Ops analyst uses Excel to compile territory totals, stage movement, and forecast risks. AI helps draft the first narrative and flag suspicious pipeline gaps, but the analyst still checks the deal data before the pack is final."]},
        "mistakes": ["Using AI on an already messy pipeline.", "Treating first-pass forecast commentary as final guidance.", "Letting workflow labels blur between draft and reviewed output."],
        "instead": {"paragraphs": ["If the need is team-level deal tracking, <a href=\"/blog/sales-pipeline-tracker-excel\">the sales pipeline tracker</a> is the better operational sheet. If the focus is finance review, <a href=\"/blog/excel-ai-for-accountants\">accounting workflows</a> may be the more relevant comparison."]},
        "related_new": ["sales-pipeline-tracker-excel", "ai-forecasting-model-excel", "review-ai-generated-excel-formulas"],
        "related_old": ["dynamic-dashboards"],
        "cover_hook": "Use AI to reduce reporting drag in Sales Ops, but keep pipeline ownership and review firmly with the team.",
        "cover_cta": "Use AI Carefully In Sales Ops",
        "cover_keywords": ["Sales Ops", "Forecasts", "Territory"],
        "cover_cue": "pipeline sheets, forecast reports, and territory-summary visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for Excel and AI for Sales Ops, with pipeline and forecast visuals.",
        "sources": [],
    },
    {
        "slug": "map-charts-excel",
        "title": "Map Charts in Excel: When to Use Them, Data Prep, and Common Mistakes",
        "category": "Excel",
        "description": "Learn when map charts in Excel are useful, how to prepare the location data properly, and the mistakes that make them misleading.",
        "keywords": ["map charts Excel", "Excel map chart", "Excel location data", "geographic chart Excel", "Excel chart mistakes"],
        "primary_intent": "Use Excel map charts more effectively and avoid common errors.",
        "search_type": "evergreen",
        "intro": [
            "Map charts are appealing because they turn location data into something immediately visual. But they are also easy to misuse. A map can look sophisticated while still being unclear, over-general, or built on inconsistent geography labels.",
            "That is why map charts work best when the location question is genuinely geographic and the source data is prepared carefully."
        ],
        "quick_answer": "Use map charts when geography itself is part of the story. Prepare the location data carefully, keep the metric simple, and make sure the chart is actually easier to understand than a table or bar chart would be.",
        "use_when": [
            "Location is central to the question, not just decorative context.",
            "Your geography labels are consistent and specific enough to resolve cleanly.",
            "You want a quick visual by country, region, or other geographic unit.",
        ],
        "sections": [
            {"heading": "What makes a map chart useful", "paragraphs": ["A map chart works when place matters to the story: regional performance, country spread, delivery concentration, or geographic imbalance."]},
            {"heading": "Why data preparation matters", "paragraphs": ["Inconsistent geography names, mixed levels of detail, or missing location context make map charts weaker very quickly. Good location data is the real foundation."]},
            {"heading": "When another chart is better", "paragraphs": ["If the viewer mainly needs rank order or precise comparison, a bar chart often beats a map chart even when the data is geographic."]},
        ],
        "example": {"heading": "Worked example: regional revenue view", "paragraphs": ["A business wants to compare revenue by country. A clean country field and a simple metric make the map chart useful as a quick overview, while a supporting table still handles the precise numbers."]},
        "mistakes": ["Using a map when geography is not central to the question.", "Ignoring ambiguous or inconsistent location labels.", "Expecting the map alone to communicate precise comparisons clearly."],
        "instead": {"paragraphs": ["If the visual story depends more on precise ranking or change over time, <a href=\"/blog/charts-visualisations\">traditional charting</a> is often clearer."]},
        "related_new": ["create-charts-with-copilot-excel", "excel-tables-best-practices", "inventory-tracker-excel"],
        "related_old": ["charts-visualisations"],
        "cover_hook": "Use map charts when place is genuinely part of the question, not just because the visual looks impressive.",
        "cover_cta": "Map Data More Clearly",
        "cover_keywords": ["Map", "Charts", "Excel"],
        "cover_cue": "geographic charts, location data, and comparison visuals",
        "image_alt": "Coding Liquids blog cover featuring Sagnik Bhattacharya for map charts in Excel, with geographic chart visuals.",
        "sources": [],
    },
]


ANCHOR_BLUEPRINTS: dict[str, dict[str, Any]] = {}

ANCHOR_BLUEPRINTS.update(
    {
        "agent-mode-in-excel": {
            "audience": "analysts, finance leads, operations managers, and spreadsheet owners who need faster answers without losing workbook control",
            "value_case": "Agent Mode changes the unit of work from one reply to a short chain of workbook actions, which means the real challenge is supervision, not only prompting.",
            "prerequisites": [
                "The source workbook already uses clear table headers, clean ranges, and descriptive sheet names.",
                "You can duplicate the workbook or work inside a safe review copy before structural edits happen.",
                "Someone on the team can manually check formulas, filters, and totals after each run.",
                "The business has agreed which outputs are draft support and which still need human sign-off.",
            ],
            "decision_points": [
                "Is the task exploratory and reviewable, or does one wrong change distort a board-level number?",
                "Do you want Agent Mode to explain, to draft, or to edit the workbook directly?",
                "Will the user know enough about the workbook to catch a subtle mistake quickly?",
                "Is the current workbook structured well enough that the assistant can see the same logic a human would see?",
            ],
            "workflow_steps": [
                "Ask Agent Mode to map the workbook, name the tables, and explain what it thinks the data represents before requesting conclusions.",
                "Narrow the task to one bounded output such as a first-pass summary, anomaly explanation, or draft report structure.",
                "Review every changed formula, filter scope, and sheet edit before using the result elsewhere.",
                "Log the useful prompt wording and the review checks if the task will repeat weekly or monthly.",
                "Promote successful prompt sequences into a written operating routine instead of improvising from scratch every cycle.",
            ],
            "standards": [
                "Separate safe working copies from approved reporting outputs.",
                "Use consistent names for dates, regions, metrics, and status columns so the assistant sees stable structure.",
                "Keep a lightweight review checklist for totals, filters, outliers, and formulas touched.",
                "Decide in advance which workbook actions may be automated and which must stay recommendation-only.",
            ],
            "scenario_title": "Scenario: month-end revenue commentary for an operations review",
            "scenario_paragraphs": [
                "An operations lead inherits one workbook with bookings, cancellations, refunds, discount codes, and regional notes. The question from leadership sounds simple: explain what changed this month and whether one region needs intervention. That is exactly the sort of request that tempts teams to over-trust Agent Mode, because the question spans several sheets and feels bigger than one formula.",
                "A safer pattern is to split the work into stages. First the assistant describes the workbook and names the tables it plans to use. Then it summarises revenue, cancellations, and discount trends by region. Only after that does it draft commentary about where the change appears to be coming from. Each stage creates a reviewable checkpoint instead of jumping straight from raw workbook to polished answer.",
                "By the time the commentary reaches leadership, the human owner has checked the date range, validated the totals against the finance view, confirmed that outliers are real rather than filtered artefacts, and rewritten any wording that sounded more certain than the data deserved. That makes Agent Mode a speed tool inside a governed workflow rather than a hidden analyst replacement.",
            ],
            "metrics": [
                "How often the assistant identifies the right tables and ranges without human correction.",
                "Time saved between receiving the workbook and producing a reviewed draft summary.",
                "Number of structural or logic issues caught during review before results are shared.",
                "How often successful runs can be converted into a repeatable documented process.",
            ],
            "faq": [
                (
                    "Should teams allow Agent Mode to edit a live workbook by default?",
                    "Only if the workbook is low-risk and the reviewer can inspect every change quickly. For high-stakes models, explanation-first and draft-first workflows are usually safer.",
                ),
                (
                    "Is Agent Mode better than Copilot chat for every task?",
                    "No. It is better when the work involves several workbook-aware steps. Simple formula help or a one-off explanation can still fit standard chat perfectly well.",
                ),
                (
                    "What is the main implementation mistake?",
                    "Treating a plausible answer as proof. The expensive failures usually come from skipped review, weak source structure, or unclear task boundaries.",
                ),
                (
                    "How do you know it is ready for repeat use?",
                    "When the same task can be run on a clean workbook copy with stable prompts, stable review checks, and a human owner who knows what good output looks like.",
                ),
                (
                    "Who should own the workflow once it is in use?",
                    "A real workbook owner, not the tool. Someone has to own the prompts, the review step, and the business interpretation when edge cases appear.",
                ),
            ],
        },
        "chatgpt-vs-claude-vs-copilot-vs-gemini-excel": {
            "audience": "Excel users, team leads, and consultants trying to choose the right AI assistant for a specific spreadsheet job rather than chasing the loudest demo",
            "value_case": "Tool comparison pages only become useful when they help readers decide what to use for formula writing, workbook explanation, automation support, and narrative analysis under real constraints.",
            "prerequisites": [
                "You know the actual job to be done: formula drafting, debugging, workbook interpretation, reporting, or automation support.",
                "You understand whether the work happens inside Excel, beside Excel, or across a wider process.",
                "You have one or two realistic sample tasks for testing instead of comparing tools in the abstract.",
                "You can separate marketing claims from the behaviour you actually need in your own environment.",
            ],
            "decision_points": [
                "Does the task need tight Excel integration or just strong reasoning beside the workbook?",
                "Is the reader optimising for speed, explanation quality, enterprise governance, or multi-step analysis?",
                "Will the answer be reviewed by one person or passed into a team workflow?",
                "How expensive would a confident but wrong answer be in this context?",
            ],
            "workflow_steps": [
                "Choose three representative Excel tasks and run them across the candidate tools.",
                "Score the outputs for correctness, clarity, editability, and review effort instead of judging only speed.",
                "Separate direct workbook features from strong external assistants that still need copy-paste or context staging.",
                "Standardise which tool the team uses for each job type so quality does not vary wildly by person.",
                "Review the decision quarterly because product capabilities and licensing can move quickly.",
            ],
            "standards": [
                "Keep a shared evaluation sheet with the prompts, sample data, and scored outcomes.",
                "Document which tool is preferred for formula generation, explanation, analysis, and macro or code support.",
                "Do not let one strong personal preference become an untested default for the whole team.",
                "Treat pricing, governance, and workflow fit as first-class criteria rather than afterthoughts.",
            ],
            "scenario_title": "Scenario: choosing one default AI stack for a spreadsheet-heavy team",
            "scenario_paragraphs": [
                "A team of analysts and ops leads all use Excel heavily, but they are split across different assistants. One person loves Copilot because it lives closer to the workbook. Another prefers ChatGPT for explanations. A third finds Claude stronger for structured reasoning. Without a shared decision model, results become inconsistent and people waste time arguing tool philosophy instead of solving work problems.",
                "The team runs a practical bake-off with four task types: write a lookup formula, explain a messy inherited workbook, draft a variance summary from an export, and suggest a clean-up approach for categorising open-text comments. They score each tool on correctness, editability, review burden, and how much context staging is needed before the answer becomes useful.",
                "The final result is not one winner for everything. Instead the team ends up with a task map: one default for workbook-native help, one for deeper reasoning, and one for fast external drafting when Excel integration matters less. That kind of conclusion is much more durable than a generic headline about which AI is “best”.",
            ],
            "metrics": [
                "Reduction in time spent choosing a tool for repeat tasks.",
                "Consistency of output quality across different team members.",
                "Review effort required before sharing AI-assisted workbook outputs.",
                "How often the chosen tool map still holds up when capabilities change.",
            ],
            "faq": [
                (
                    "Is there one best AI for Excel overall?",
                    "Not in a durable sense. The better question is which tool best fits formula help, workbook-native actions, deeper reasoning, or organisation-wide governance in your context.",
                ),
                (
                    "Why do comparisons age badly?",
                    "Because product capabilities, integrations, and pricing change. A good comparison explains the criteria well enough that readers can re-run the judgement when features move.",
                ),
                (
                    "Should small teams still standardise on one tool?",
                    "Usually yes, at least by task type. Standardisation reduces review chaos and makes it easier to document what “good” output looks like.",
                ),
                (
                    "What is the most overlooked criterion?",
                    "Review burden. Two tools can both feel fast, but the one that produces cleaner, easier-to-check answers often wins in real work.",
                ),
                (
                    "Can external tools still beat Excel-native ones?",
                    "Absolutely. Strong external reasoning can be more valuable than shallow native integration if the team knows how to stage context and review the output carefully.",
                ),
            ],
        },
        "format-data-for-copilot-excel": {
            "audience": "spreadsheet users who want Copilot or related AI features to produce fewer misreads and more reviewable results",
            "value_case": "Most failures blamed on prompting are really structure failures, so this topic is foundational for everything that sits on top of workbook AI.",
            "prerequisites": [
                "You can identify the source range that should become the trustworthy base table.",
                "Each row represents one record and each column has one clear meaning.",
                "Decorative layout choices can be separated from the analytical source data.",
                "Someone can define what a clean output from Copilot should look like before the prompt is written.",
            ],
            "decision_points": [
                "Should this sheet remain a presentation layer, or become a clean data layer first?",
                "Which fields are essential for the question you want AI to answer?",
                "Do headers reflect business meaning clearly enough for a new reader to understand them?",
                "Would a human reviewer notice quickly if Copilot grouped or interpreted the data incorrectly?",
            ],
            "workflow_steps": [
                "Move the operational data into one clean table before asking Copilot for analysis.",
                "Rename vague columns, remove merged cells, and isolate totals or notes outside the source range.",
                "Run one simple question first to confirm the tool is reading the right grain of data.",
                "Only then ask for summaries, formulas, categorisation, or chart suggestions.",
                "Save the working structure as the default pattern for the next dataset instead of cleaning from scratch every time.",
            ],
            "standards": [
                "Use one header row and avoid duplicate or ambiguous field names.",
                "Keep calculations, notes, and decorative formatting outside the raw source table when possible.",
                "Document the table grain in plain language so reviewers know what one row represents.",
                "Build a small pre-AI clean-up checklist that every workbook owner can run quickly.",
            ],
            "scenario_title": "Scenario: turning a messy monthly export into a Copilot-ready reporting table",
            "scenario_paragraphs": [
                "A sales operations lead receives an export with blank rows, repeated subheadings, merged cells, and several columns whose names make sense only to the person who built the report two years ago. Copilot can still respond to prompts on that sheet, but the answers swing between partial and misleading because the underlying structure does not tell a consistent story.",
                "The turnaround comes from rebuilding the source as one proper table. Region, owner, stage, amount, close date, and product line each get their own clear column. Totals and commentary move out of the data layer. The team asks Copilot a small question first, such as summarising count and value by region, just to confirm it now sees the same grain the analyst sees.",
                "Once that foundation is in place, later tasks become much easier: chart drafting, formula suggestions, pipeline commentary, anomaly spotting, and even text categorisation for notes. The lesson is simple but powerful. Workbook AI is downstream of structure, not a substitute for it.",
            ],
            "metrics": [
                "How often Copilot answers on the correct row and column grain after clean-up.",
                "Reduction in prompt retries caused by vague headers or mixed data layers.",
                "Time spent preparing a workbook before AI-assisted work begins.",
                "Number of repeat workflows that can use the same clean table pattern.",
            ],
            "faq": [
                (
                    "Can good prompting rescue bad structure?",
                    "Sometimes it can reduce confusion, but it rarely fixes the core problem. If the data layer is ambiguous, the assistant has to guess where humans should not.",
                ),
                (
                    "Do I always need an Excel Table object?",
                    "A proper table is usually the cleanest path because it reinforces headers, growth, and structured references, but the bigger point is consistent row-column structure.",
                ),
                (
                    "What is the quickest quality check?",
                    "Ask one narrow summary question first. If the answer groups the data correctly, you know the structure is at least readable before you request bigger outputs.",
                ),
                (
                    "Should totals stay inside the same range?",
                    "Usually no. Totals, commentary, and presentation elements are better kept outside the analytical source layer so the tool reads the data cleanly.",
                ),
                (
                    "Why does this deserve anchor-page depth?",
                    "Because nearly every Excel AI workflow gets stronger or weaker based on data structure. Fixing that upstream lever improves the whole cluster, not just one article.",
                ),
            ],
        },
    }
)

ANCHOR_BLUEPRINTS.update(
    {
        "flutter-performance-2026": {
            "audience": "Flutter developers who need a repeatable way to diagnose and improve performance instead of collecting isolated optimisation tricks",
            "value_case": "Performance work only becomes valuable when it is measured, prioritised, and tied back to user-visible problems rather than intuition alone.",
            "prerequisites": [
                "You can reproduce the performance issue on a screen, flow, or device profile that matters.",
                "The team is willing to measure before and after changes instead of guessing.",
                "There is enough codebase clarity to isolate rendering, state, image, or data causes separately.",
                "You know whether the goal is smoothness, startup, memory, or interaction responsiveness.",
            ],
            "decision_points": [
                "Is the bottleneck in rebuild patterns, rendering, image handling, layout, or data work?",
                "Which user journeys deserve optimisation first because users actually feel the pain there?",
                "Can the issue be solved structurally rather than with scattered micro-tweaks?",
                "What evidence will prove the change helped instead of merely moving code around?",
            ],
            "workflow_steps": [
                "Start with a reproducible performance case and capture a baseline with the right tooling.",
                "Narrow the issue to one screen, flow, or component before changing implementation details.",
                "Fix the highest-leverage cause first, then remeasure before touching secondary issues.",
                "Record what changed and which metric improved so the team learns from the work.",
                "Turn repeated findings into code review heuristics and performance guardrails.",
            ],
            "standards": [
                "Measure before optimising and measure again afterwards.",
                "Prefer structural fixes over scattered micro-optimisations.",
                "Keep user-visible performance goals explicit so the team knows what success means.",
                "Share performance findings so the next feature avoids repeating the same problem.",
            ],
            "scenario_title": "Scenario: a critical Flutter dashboard feels smooth in demos but janky in daily use",
            "scenario_paragraphs": [
                "A team demos a dashboard that looks fine on a fast machine, but users in daily work start reporting lag when filters change and charts redraw. The danger is reacting with random tweaks: caching here, one refactor there, a new widget pattern somewhere else. Without a measurement-led process, performance work quickly becomes superstition.",
                "The team picks one user flow, captures a baseline, and isolates where the cost is actually coming from. They discover that a broad rebuild pattern is forcing expensive sections to update unnecessarily. Fixing that structural cause gives a larger gain than the minor tweaks they were originally debating.",
                "After the improvement, the team records the before-and-after evidence and updates its review habits. That prevents performance from being treated as a heroic cleanup phase at the end. Instead it becomes part of how the codebase is designed and reviewed during normal delivery.",
            ],
            "metrics": [
                "Measured improvement in frame stability or interaction responsiveness on the target flow.",
                "Reduction in unnecessary rebuilds or expensive rendering work after structural fixes.",
                "Time required to diagnose the next performance issue using the documented process.",
                "How often new features meet the team’s performance baseline without late firefighting.",
            ],
            "faq": [
                (
                    "What is the first optimisation step?",
                    "Measurement. Until the team can reproduce and observe the issue clearly, optimisation work is mostly guesswork.",
                ),
                (
                    "Are micro-optimisations useless?",
                    "No, but they are secondary. They help most after the team has already found and addressed the larger structural cause.",
                ),
                (
                    "How do you make performance work sustainable?",
                    "Turn recurring findings into patterns the team can review for early, instead of relying on one performance hero to rescue the app later.",
                ),
                (
                    "Why do some fixes feel good but not last?",
                    "Because they treat symptoms rather than the source. If rebuild scope, rendering cost, or data flow remains weak, the pain returns under real usage.",
                ),
                (
                    "Why does this deserve anchor-page depth?",
                    "Because performance is not one trick. It is a workflow of diagnosis, prioritisation, remediation, verification, and team learning.",
                ),
            ],
        },
        "flutter-testing-strategy-2026": {
            "audience": "Flutter teams trying to build a balanced test strategy that catches real failures without freezing delivery velocity",
            "value_case": "Testing strategy matters because the wrong balance makes teams either slow and brittle or fast and unsafe, and both problems compound as the app grows.",
            "prerequisites": [
                "You know the main failure modes in the product rather than treating all tests as equal.",
                "The team can distinguish cheap feedback from high-confidence coverage.",
                "Architecture and dependency boundaries are clear enough that tests have sensible seams.",
                "Developers agree that test value should be judged by risk reduction, not by badge counts alone.",
            ],
            "decision_points": [
                "Which behaviours deserve unit, widget, integration, or golden coverage based on risk?",
                "What failures are expensive enough that slower tests still make sense?",
                "How much confidence can be achieved earlier in the pipeline with cheaper tests?",
                "Where is the current suite generating noise instead of insight?",
            ],
            "workflow_steps": [
                "Map the product’s key failure risks before adding or removing tests.",
                "Choose the cheapest trustworthy test for each meaningful risk.",
                "Keep the fast feedback loop healthy so developers still use the suite during normal work.",
                "Reserve slower end-to-end coverage for behaviour that truly needs cross-layer confidence.",
                "Review the strategy as the product and architecture evolve instead of freezing it forever.",
            ],
            "standards": [
                "Tie tests to risk, not to abstract coverage goals.",
                "Keep ownership of flaky or low-value tests visible until they are fixed or removed.",
                "Make the fast path easy so developers actually run the suite often.",
                "Use architecture boundaries that support focused tests instead of forcing everything into integration scope.",
            ],
            "scenario_title": "Scenario: a Flutter team wants confidence without drowning in slow or brittle tests",
            "scenario_paragraphs": [
                "A product team has grown past the stage where manual checking is enough, but its test suite is sending mixed signals. Some failures are useful. Others are flaky or so slow that developers stop trusting them. That is a strategy problem, not only a tooling problem.",
                "The team starts by identifying the failures that would genuinely hurt users or release confidence. It then chooses the cheapest test shape that can catch each one well. Many UI and state risks can be handled earlier than teams expect, which preserves faster feedback without giving up real confidence.",
                "The result is not maximal testing. It is intelligent testing. The suite becomes easier to explain, easier to maintain, and more aligned with how the app actually fails in the real world. That is what makes a testing strategy durable.",
            ],
            "metrics": [
                "Speed of the developer feedback loop on the core test path.",
                "Rate of meaningful failure detection compared with flaky or low-value failures.",
                "Confidence in releases without excessive manual regression effort.",
                "How easily the team can explain why each major test layer exists.",
            ],
            "faq": [
                (
                    "Should teams aim for a target coverage number?",
                    "Coverage can be informative, but on its own it is a weak goal. The stronger question is whether the suite catches the failures that would materially hurt users or releases.",
                ),
                (
                    "What usually makes test suites unhealthy?",
                    "Poor risk mapping, unclear architecture seams, and letting flaky tests remain normal for too long.",
                ),
                (
                    "How do you balance speed and confidence?",
                    "By using the cheapest trustworthy test for each risk and reserving slower tests for behaviour that truly crosses layers.",
                ),
                (
                    "When should a team revisit the strategy?",
                    "Whenever product scope, architecture, or release risk changes enough that the old balance no longer reflects reality.",
                ),
                (
                    "Why is this an anchor topic?",
                    "Because testing strategy touches architecture, developer workflow, release confidence, and the long-term maintainability of the whole app.",
                ),
            ],
        },
        "responsive-flutter-ui-all-screens": {
            "audience": "Flutter developers building interfaces that need to behave well across mobile, tablet, desktop, and web without becoming a pile of one-off breakpoints",
            "value_case": "Responsive UI pays off when teams move from ad hoc resizing tricks to deliberate layout systems and content priorities.",
            "prerequisites": [
                "You know which screen classes and usage modes the product actually needs to support.",
                "The team can separate layout decisions from business logic cleanly.",
                "Content hierarchy is clear enough that bigger screens can add value instead of only adding empty space.",
                "Design and engineering are aligned on how the experience should adapt across form factors.",
            ],
            "decision_points": [
                "Which parts of the UI should stretch, reflow, split, or remain fixed across screen sizes?",
                "Is the experience primarily touch-first, pointer-first, or mixed?",
                "Do larger screens need more density, more simultaneous context, or simply more breathing room?",
                "How will navigation, forms, and long data views behave when space changes dramatically?",
            ],
            "workflow_steps": [
                "Start by defining the content priorities and interaction goals for each screen class.",
                "Build layout patterns that can flex structurally rather than relying on scattered breakpoint hacks.",
                "Test the same key journeys across mobile, tablet, desktop, and web views early.",
                "Capture reusable layout decisions so later screens inherit the same responsive logic.",
                "Refine the system as real usage reveals where density or interaction changes are needed.",
            ],
            "standards": [
                "Treat responsive behaviour as a layout system, not as a late patch.",
                "Keep navigation and content hierarchy explicit across screen sizes.",
                "Design for interaction mode as well as width and height.",
                "Reuse responsive shells and layout primitives instead of rewriting behaviour screen by screen.",
            ],
            "scenario_title": "Scenario: the same Flutter product must serve field users on mobile and operators on desktop",
            "scenario_paragraphs": [
                "A Flutter product starts on mobile, where a simple stacked flow feels natural. Then the same product needs to support internal operators on desktop and tablet. Suddenly the design problem changes. The app cannot simply stretch every mobile screen wider and call that responsive. Larger screens need more context, faster navigation, and better information density. Desktop operators often need split views, denser tables, and fewer navigation hops than mobile users.",
                "The team responds by designing layout systems rather than isolated breakpoint rules. Navigation shifts, content regions adapt, and certain workflows expose side-by-side context that would never fit on a phone. Because the patterns are deliberate, new screens can follow the same logic instead of inventing responsive behaviour anew each time.",
                "That is the deeper lesson of responsive Flutter work. Success is not that the UI technically renders on every screen. Success is that the product feels intentionally designed for the way people use it on each class of device.",
            ],
            "metrics": [
                "How well key journeys complete across target screen classes without workaround behaviour.",
                "Reuse rate of responsive shells, components, and layout patterns across features.",
                "Reduction in screen-specific bugs caused by ad hoc breakpoint logic.",
                "User or stakeholder satisfaction with information density and usability on larger screens.",
            ],
            "faq": [
                (
                    "Is responsiveness just about width breakpoints?",
                    "No. Width matters, but interaction mode, content priority, and workflow shape matter just as much.",
                ),
                (
                    "When should desktop behaviour diverge from mobile?",
                    "When the extra space can create a genuinely better workflow, such as showing more context or reducing navigation hops, rather than only enlarging the same mobile layout.",
                ),
                (
                    "What is the biggest team mistake?",
                    "Treating each screen as a unique responsive problem instead of building reusable layout principles and shells.",
                ),
                (
                    "How do you test responsive quality well?",
                    "Use real journeys across the main screen classes early, not only static screenshots or isolated widgets in ideal states.",
                ),
                (
                    "Why does this deserve anchor depth?",
                    "Because responsive Flutter UI sits at the intersection of layout systems, navigation, content hierarchy, and product design decisions across platforms.",
                ),
            ],
        },
    }
)

ANCHOR_BLUEPRINTS.update(
    {
        "excel-ai-for-accountants": {
            "audience": "accountants, finance teams, and close-process owners who want AI assistance without weakening control, traceability, or professional judgement",
            "value_case": "Accounting workflows are full of repetitive analytical work, but the value of AI depends on keeping sign-off, evidence, and judgement visibly human-owned.",
            "prerequisites": [
                "The team can separate draft assistance from final accounting conclusions.",
                "Source reconciliations and close schedules already have a stable structure.",
                "Sensitive data handling and governance rules are understood before AI is introduced.",
                "There is an agreed reviewer for any AI-assisted commentary, anomaly callout, or reconciliation support.",
            ],
            "decision_points": [
                "Is the task low-risk drafting support or a judgement-heavy accounting conclusion?",
                "Will the workflow improve evidence gathering, or only create faster but less clear commentary?",
                "Can the AI-assisted step be traced back to the underlying source data easily?",
                "Would a mistake slow the close, create rework, or undermine stakeholder confidence?",
            ],
            "workflow_steps": [
                "Identify repeatable finance tasks where AI can accelerate first-pass work without owning the decision.",
                "Prepare the workbook or export so source evidence stays visible and auditable.",
                "Use AI for draft summaries, anomaly triage, or checklist support, then review the result against the source.",
                "Capture the useful prompt and review steps if the workflow supports monthly close or recurring reconciliations.",
                "Refine the pattern after each cycle based on where review found overstatements, omissions, or weak wording.",
            ],
            "standards": [
                "Keep sign-off with the accountant, not with the generated output.",
                "Preserve the link between commentary and source evidence.",
                "Label AI-assisted narrative or categorisation so reviewers know what they are checking.",
                "Use repeatable close or reconciliation checklists to keep review consistent across periods.",
            ],
            "scenario_title": "Scenario: AI-supported close commentary for a monthly variance review",
            "scenario_paragraphs": [
                "A finance team wants to reduce the time spent drafting monthly close commentary. The actual pain is not the calculations themselves, but the repetitive effort of comparing variances, checking whether exceptions look material, and writing the first-pass explanation for business partners. AI can help here, but only if the team preserves clear evidence paths back to the workbook.",
                "The team prepares a clean variance table with current period, prior period, budget, and materiality flags. AI drafts the first narrative about what changed, but the accountant still checks the numbers, confirms whether the variance is explainable, and rewrites any wording that sounds more certain than the evidence supports. The model accelerates the pass; it does not replace the accounting conclusion.",
                "Over time, the workflow becomes stronger because the team standardises the source table shape, the prompt pattern, and the review checklist. That is what makes AI genuinely helpful in accounting contexts: not speed alone, but speed inside a controlled process.",
            ],
            "metrics": [
                "Time saved during variance review and commentary drafting.",
                "Number of AI-drafted observations that survive review with only light editing.",
                "Strength of the evidence trail between generated commentary and source numbers.",
                "Reduction in repetitive manual narrative work during close cycles.",
            ],
            "faq": [
                (
                    "Where does AI fit cleanly in accounting work?",
                    "It fits best in first-pass summaries, anomaly triage, checklist support, and preparation work that still leaves the final accounting conclusion to a professional reviewer.",
                ),
                (
                    "Where should teams be most careful?",
                    "Any place where wording could imply certainty beyond the evidence, or where a classification error could distort a financial conclusion.",
                ),
                (
                    "Can AI help with reconciliations?",
                    "Yes, especially for surfacing differences and drafting first-pass explanations, but the reconciliation itself still needs evidence-based human review.",
                ),
                (
                    "What makes this workflow scale safely?",
                    "Clean source tables, consistent prompts, explicit review ownership, and a documented checklist for what must be verified each cycle.",
                ),
                (
                    "Why should this be an anchor page?",
                    "Because accountants need a governance-aware operating model, not just isolated prompt tips. The surrounding controls matter as much as the feature itself.",
                ),
            ],
        },
        "create-with-ai-flutter": {
            "audience": "Flutter developers and tech leads trying to place Gemini CLI, MCP, and the AI Toolkit into a practical build workflow rather than a novelty demo",
            "value_case": "The real decision is not whether AI can help Flutter work, but where it should sit in architecture, iteration speed, and code review habits.",
            "prerequisites": [
                "You already know the product feature or workflow you are trying to accelerate.",
                "The codebase has enough structure that generated changes can be reviewed meaningfully.",
                "The team has a normal code review and testing habit rather than treating AI output as self-validating.",
                "Developers understand the difference between idea generation, scaffolding, and production readiness.",
            ],
            "decision_points": [
                "Do you need fast ideation, local code assistance, design-to-code help, or workflow orchestration?",
                "How much of the task touches app architecture rather than isolated UI code?",
                "Will the generated output be easy to test and maintain after the first draft lands?",
                "Which tool fits local developer loops versus broader team workflows?",
            ],
            "workflow_steps": [
                "Use AI first for scoped ideation or scaffolding, not for hidden architectural decisions.",
                "Keep the codebase structure explicit so generated output lands in the right feature and layer.",
                "Run the normal review and test steps even when the draft looked correct at first glance.",
                "Capture the prompts or agent flows that repeatedly save time on similar tasks.",
                "Evolve the workflow based on what genuinely reduced cycle time rather than what felt impressive in demos.",
            ],
            "standards": [
                "Treat AI as a draft partner inside an existing engineering process.",
                "Keep ownership of architecture, state boundaries, and production constraints with the team.",
                "Prefer small reviewable changes over large magical rewrites.",
                "Measure whether the workflow shortens iteration time or only creates cleanup later.",
            ],
            "scenario_title": "Scenario: adding an AI-assisted feature to a support dashboard",
            "scenario_paragraphs": [
                "A team building a support dashboard wants to add AI-assisted reply suggestions. Several tools can help: one can scaffold parts of the feature, another can improve iteration speed, and another can support local workflow orchestration. The temptation is to search for one tool that does everything. In practice, the workflow works better when each tool has a clearly bounded role.",
                "The team first uses AI to sketch the interaction model and scaffold the outer feature shell. Then the developers place the code inside the existing Flutter architecture, wire the dependencies properly, and run the same review and testing habits they would use for hand-written code. That preserves the health of the app while still capturing the speed advantage.",
                "After a few cycles, the team knows which prompts and workflows genuinely save time and which ones only create noisy diffs. That is the useful maturity point for Flutter AI workflows: not excitement about generation, but a repeatable path from idea to reviewable code.",
            ],
            "metrics": [
                "Reduction in time from feature idea to first reviewable draft.",
                "Code review churn caused by generated changes versus hand-written baselines.",
                "How often AI-assisted output survives testing and architectural review with limited cleanup.",
                "Clarity of ownership around prompts, tooling choices, and reviewed implementation patterns.",
            ],
            "faq": [
                (
                    "Is one Flutter AI tool enough for the whole workflow?",
                    "Usually no. Teams often mix idea support, code assistance, and architecture-aware review rather than expecting one surface to cover every job well.",
                ),
                (
                    "What should never be outsourced to AI?",
                    "Core product judgement, architecture boundaries, security assumptions, and the final decision that a change is ready for production.",
                ),
                (
                    "How do you know the workflow is helping?",
                    "When the team reaches a reviewable first draft faster without increasing cleanup, architectural drift, or flaky tests afterwards.",
                ),
                (
                    "Where do teams overuse AI in Flutter?",
                    "In large rewrites and hidden architecture decisions. The best gains usually come from scoped drafts and faster iteration loops.",
                ),
                (
                    "Why does this topic deserve anchor-page treatment?",
                    "Because readers need the surrounding process: where the tools fit, how they change iteration speed, and how to keep code quality intact after the first draft lands.",
                ),
            ],
        },
        "flutter-app-architecture-2026": {
            "audience": "Flutter developers and leads choosing a maintainable project structure that can survive feature growth, onboarding, and release pressure",
            "value_case": "Architecture matters because it turns isolated coding choices into a codebase that either gets easier or harder to change over time.",
            "prerequisites": [
                "You know the app size, team size, and expected pace of feature growth.",
                "State, navigation, and data boundaries are being discussed explicitly rather than emerging by accident.",
                "The team can agree on folder, naming, and ownership conventions early enough to avoid churn.",
                "You are willing to optimise for maintainability, not only for the next sprint.",
            ],
            "decision_points": [
                "Will the app stay small, or is it likely to grow across multiple feature teams?",
                "How much separation do you need between UI, domain logic, and data access?",
                "What architecture choices help testing and refactoring rather than making them harder?",
                "Which conventions will still make sense when a new developer joins six months later?",
            ],
            "workflow_steps": [
                "Choose the smallest architecture that still protects the codebase from foreseeable growth.",
                "Define feature boundaries, data flow, and ownership rules before the project becomes crowded.",
                "Use early features to prove the architecture under real delivery pressure, not only in diagrams.",
                "Refine conventions when they create friction, but avoid stylistic churn with every new idea.",
                "Keep architecture documentation lightweight and close to the code so it remains useful.",
            ],
            "standards": [
                "Agree on feature-first boundaries and layer responsibilities explicitly.",
                "Keep routing, state, and data access choices aligned with the architecture rather than bolted on later.",
                "Optimise for onboarding clarity and testability, not only initial coding speed.",
                "Review architectural exceptions intentionally instead of letting them accumulate by default.",
            ],
            "scenario_title": "Scenario: a Flutter app grows from one product team to several streams of work",
            "scenario_paragraphs": [
                "A Flutter product starts with one small team and a manageable set of screens. In that stage almost any structure feels acceptable because the original developers still hold the whole app in their heads. The real architecture test begins once new features arrive in parallel, specialists join the team, and the code needs to support changes made by people who were not present at the beginning.",
                "A feature-first architecture with clear boundaries gives the team somewhere to put new work without constant negotiation. UI, domain logic, and data access still need to collaborate, but they no longer blur into one giant directory of convenience code. That makes testing, onboarding, and debugging much more predictable.",
                "The goal is not theoretical purity. It is to keep change cheap as the app grows. Teams feel the benefit when a new feature can be added without hunting through unrelated screens, when a new developer can trace ownership quickly, and when architectural conversations become specific rather than vague.",
            ],
            "metrics": [
                "Time required for a new developer to navigate to the right feature and layer.",
                "Change surface when adding a new feature or refactoring an old one.",
                "Ease of testing and reasoning about code ownership.",
                "Frequency of architectural exceptions that create recurring maintenance pain.",
            ],
            "faq": [
                (
                    "Is feature-first always the right answer?",
                    "Not automatically, but it is often a strong default once the app is expected to grow. The real question is how the structure handles change, ownership, and onboarding pressure.",
                ),
                (
                    "How much architecture is too much?",
                    "If the structure makes simple features slower without protecting against real complexity, it is probably overbuilt. The best architecture is proportionate to the app’s likely growth.",
                ),
                (
                    "Should state management be chosen first?",
                    "Usually architecture and state decisions inform each other. Picking state in isolation can push the project toward a structure that is harder to sustain.",
                ),
                (
                    "What is the most common failure mode?",
                    "Convenience-driven drift, where the team has a diagrammed architecture on paper but keeps adding exceptions under delivery pressure.",
                ),
                (
                    "Why is this an anchor page?",
                    "Because architecture decisions shape everything else in the Flutter cluster: routing, testing, performance, team onboarding, and the cost of future change.",
                ),
            ],
        },
    }
)

ANCHOR_BLUEPRINTS.update(
    {
        "ai-power-query-m-code": {
            "audience": "Excel users and analysts who already use Power Query and want AI to accelerate M code work without making refresh logic harder to trust",
            "value_case": "AI can help with M code drafting and debugging, but the durable gain comes from using it inside a transparent transformation workflow rather than as a blind fixer.",
            "prerequisites": [
                "You understand the business transformation you want, even if you do not know the exact M syntax yet.",
                "The source data and expected final table shape are both clear enough to test.",
                "You can refresh the query on sample data and inspect the result step by step.",
                "The workbook owner is willing to keep the transformation readable for later support.",
            ],
            "decision_points": [
                "Do you need AI to draft a new query step, explain an error, or refactor a messy existing query?",
                "Would changing the source structure reduce the problem more than rewriting M code?",
                "Can the resulting query be understood by the next analyst who inherits it?",
                "Are you solving a one-off clean-up or building a refreshable pipeline?",
            ],
            "workflow_steps": [
                "Define the desired before-and-after table shape before asking AI for M code help.",
                "Request one step or one fix at a time so the query remains inspectable.",
                "Test the result on representative sample data and confirm edge cases like blanks, duplicates, and changed headers.",
                "Rename query steps clearly so later reviewers can follow the transformation path.",
                "Keep a reviewed version of the query once the logic is stable and useful.",
            ],
            "standards": [
                "Prefer clear step names over anonymous transformation chains.",
                "Store expected output examples so query changes can be judged quickly.",
                "Ask AI to explain the proposed step, not only to generate it.",
                "Treat refresh reliability as more important than clever one-line transformations.",
            ],
            "scenario_title": "Scenario: AI helps untangle a brittle monthly Power Query workflow",
            "scenario_paragraphs": [
                "A reporting analyst inherits a monthly Power Query process that used to work only because the export never changed. Then a source column gets renamed, another column arrives out of order, and the refresh starts failing. AI feels attractive here because the analyst wants faster help with the M code, but the risk is swapping one opaque query for another.",
                "The cleaner approach is to define the required output table first, then ask AI for help on one failing step at a time. The analyst confirms whether the proposed fix actually handles missing columns, type changes, and row anomalies on sample data. That keeps the repair visible instead of magical.",
                "Once the refresh becomes stable again, the analyst renames the steps, documents the expected output, and keeps the AI-assisted changes as part of a readable query chain. The best outcome is not merely a working refresh today. It is a transformation pipeline the next reviewer can still reason about next month.",
            ],
            "metrics": [
                "Time saved when debugging or drafting Power Query transformations.",
                "Refresh reliability after AI-assisted changes are reviewed and documented.",
                "Ease with which another analyst can follow the query steps.",
                "Reduction in brittle manual clean-up outside the query pipeline.",
            ],
            "faq": [
                (
                    "Can AI write whole Power Query pipelines safely?",
                    "It can draft a lot, but whole-pipeline trust is risky unless you already know the target shape and can validate each step against sample data.",
                ),
                (
                    "What is the best way to ask for help?",
                    "Describe the source table, the desired output, and the exact failing step or transformation need. That gives AI something concrete instead of forcing it to guess the business intent.",
                ),
                (
                    "Should I accept compact clever code?",
                    "Only if it remains readable. In Power Query, clarity often matters more than showing off brevity.",
                ),
                (
                    "How do I know the fix is trustworthy?",
                    "Refresh the query on representative data, inspect the changed rows, and verify that edge cases and schema shifts behave as expected.",
                ),
                (
                    "Why does this topic deserve anchor depth?",
                    "Because readers need more than syntax help. They need a repeatable way to define transformations, review query changes, and keep refresh logic maintainable over time.",
                ),
            ],
        },
        "ai-forecasting-model-excel": {
            "audience": "analysts, planners, and finance teams who want AI assistance while building forecasting models without outsourcing the model judgement itself",
            "value_case": "Forecasting gains come from faster structuring and scenario support, but the model remains only as strong as its assumptions, review, and interpretation.",
            "prerequisites": [
                "You have a clear business question, forecast horizon, and decision to support.",
                "Historical data is clean enough to inspect for trend, seasonality, and anomalies.",
                "Assumptions can be written down in plain language before they are turned into formulas or model steps.",
                "Someone owns the final model sign-off and can explain the forecast to stakeholders.",
            ],
            "decision_points": [
                "Is the model for rough planning, operating review, budgeting, or external reporting support?",
                "Which assumptions deserve manual control rather than AI suggestion?",
                "How much explanation will stakeholders need before they trust the forecast?",
                "What baseline or benchmark will you compare the AI-assisted model against?",
            ],
            "workflow_steps": [
                "Frame the forecast question, inputs, and success criteria before asking AI for formulas or model ideas.",
                "Use AI to accelerate structure, scenario framing, or documentation rather than to skip assumption thinking.",
                "Validate the model against history and a simpler baseline before sharing new scenarios widely.",
                "Separate assumptions, mechanics, and outputs so reviewers can inspect the model cleanly.",
                "Update the model with documented learning after each forecast cycle instead of treating it as a one-off artefact.",
            ],
            "standards": [
                "Keep assumption cells visible and explained in plain language.",
                "Show a baseline forecast alongside the richer model so reviewers have context.",
                "Document where AI suggested structure or wording and where humans locked the logic.",
                "Review model outputs for sensitivity to a few critical assumptions before presenting them.",
            ],
            "scenario_title": "Scenario: an AI-assisted demand forecast for the next planning cycle",
            "scenario_paragraphs": [
                "A planning team needs a demand view for the next two quarters and wants to move faster than its usual manual spreadsheet build. AI can help shape the model structure, suggest scenario labels, and draft some of the first-pass formulas. But if the team hands over the real modelling judgement too early, the forecast becomes polished guesswork rather than useful planning support.",
                "The better route is to lock the question first: what business decision will this forecast influence, what data is in scope, what baseline will be compared, and which assumptions are intentionally manual. AI then accelerates the build, but the team still validates the outputs against history and tests whether the model behaves sensibly when major assumptions move.",
                "When the forecast goes to leadership, the planners can explain both the number and the pathway: where the model came from, what assumptions matter most, and how the result changes across plausible scenarios. That is what turns an AI-assisted spreadsheet into a credible planning tool.",
            ],
            "metrics": [
                "Time saved in building or refreshing the forecast structure.",
                "Forecast accuracy relative to the baseline or previous approach.",
                "Reviewer confidence in the visibility of assumptions and scenario logic.",
                "How quickly the team can update the model after new data arrives.",
            ],
            "faq": [
                (
                    "Can AI build a full forecast model for me?",
                    "It can accelerate a lot of the setup, but the most valuable part of forecasting is still assumption judgement and interpretation. That remains a human responsibility.",
                ),
                (
                    "What is the safest use of AI here?",
                    "Use it for structure, draft formulas, scenario framing, and first-pass narrative support while keeping assumptions and validation firmly in human hands.",
                ),
                (
                    "How do I avoid trusting the model too quickly?",
                    "Compare it against history and a simpler baseline, then test how the outputs react to a few critical assumption changes.",
                ),
                (
                    "Should the model stay in one sheet?",
                    "Usually no. Separating assumptions, calculations, and outputs makes review and maintenance much easier.",
                ),
                (
                    "Why is this a pillar topic?",
                    "Because forecasting pulls together structure, formulas, scenarios, review, and stakeholder communication. Readers usually need the whole operating model, not a short tip.",
                ),
            ],
        },
        "text-analysis-excel-with-ai": {
            "audience": "teams working with survey comments, reviews, and open-text feedback who want AI speed without losing auditability",
            "value_case": "Open-text analysis gets messy quickly, so the winning workflow is not only about classification prompts but about sampling, review, and presentation discipline.",
            "prerequisites": [
                "The comment dataset is cleaned enough that one row truly equals one response or one analysable unit.",
                "You know what type of output matters: themes, sentiment, categories, summaries, or escalations.",
                "The team can review sampled outputs before publishing conclusions widely.",
                "Sensitive or people-impacting conclusions still have an accountable human reviewer.",
            ],
            "decision_points": [
                "Do you need broad themes, fine-grained labels, or just a quick first-pass summary?",
                "How much inconsistency can the business tolerate in the categorisation?",
                "Is the text sensitive enough that privacy or governance changes the workflow?",
                "Will the result drive reporting, operational action, or only exploratory understanding?",
            ],
            "workflow_steps": [
                "Start by defining the categories or analysis questions in plain language before prompting.",
                "Run a first-pass AI classification on a sample, not on the whole dataset immediately.",
                "Review edge cases, sarcasm, mixed comments, and off-topic responses before scaling up.",
                "Aggregate the reviewed labels into counts, trends, and representative examples inside Excel.",
                "Document where the labels were drafted by AI and how sampling or manual review corrected them.",
            ],
            "standards": [
                "Keep one source sheet for raw comments and another for reviewed labels or themes.",
                "Use sampling as a formal review step, not as optional polish.",
                "Avoid presenting AI-generated categories as if they were objective truth without caveats.",
                "Retain example comments for each theme so reports stay grounded in real language.",
            ],
            "scenario_title": "Scenario: quarterly customer feedback analysis for a product team",
            "scenario_paragraphs": [
                "A product team has thousands of feedback comments and wants a fast read on the biggest themes before the quarterly review. AI is clearly useful here because manual reading alone is slow and inconsistent. The problem is that open text contains sarcasm, mixed intent, domain-specific language, and comments that fit more than one category at once.",
                "The strongest workflow starts with a sample. The team asks AI to draft categories and labels a subset first, then reviews whether the themes hold up on ambiguous or important edge cases. Only after that do they scale the workflow to the full dataset and turn the labels into counts, charts, and narrative summaries.",
                "By the time the report reaches leadership, the team is not merely repeating what the model said. It can explain how the themes were defined, what review happened, where ambiguity remained, and which example comments support the most important conclusions. That is what makes the analysis operationally useful.",
            ],
            "metrics": [
                "Time saved in producing a first-pass thematic view of the dataset.",
                "Agreement rate between sampled manual review and AI-generated labels.",
                "Clarity of downstream reporting once comments have been grouped into reviewed themes.",
                "How often the same taxonomy can be reused across future surveys or review cycles.",
            ],
            "faq": [
                (
                    "Can AI sentiment alone replace theme analysis?",
                    "Usually no. Sentiment is often too blunt for operational decisions. Teams usually need themes, drivers, and representative examples, not only positive or negative scoring.",
                ),
                (
                    "How much sampling is enough?",
                    "Enough to cover obvious edge cases and verify that the category set is behaving sensibly. The right amount depends on risk, but zero sampling is rarely acceptable.",
                ),
                (
                    "Should the categories be fixed in advance?",
                    "Sometimes a draft taxonomy can emerge from the data, but it still needs human review before it becomes the reporting framework.",
                ),
                (
                    "Where does Excel still add value here?",
                    "Excel is excellent for cleaning, aggregating, pivoting, charting, and presenting the reviewed outcomes once the label workflow is under control.",
                ),
                (
                    "Why is this page stronger as an anchor?",
                    "Because readers need the full pipeline: row structure, taxonomy design, sampling, review, aggregation, and communication of uncertain results.",
                ),
            ],
        },
    }
)

ANCHOR_BLUEPRINTS.update(
    {
        "review-ai-generated-excel-formulas": {
            "audience": "Excel users who already use AI for formula help and now need a dependable way to catch bad assumptions before they spread",
            "value_case": "Formula review is where the value of AI-generated spreadsheet work is either locked in or destroyed, especially once the result feeds a report, dashboard, or business decision.",
            "prerequisites": [
                "You can state in plain language what the formula is supposed to do before you inspect the syntax.",
                "The source cells, ranges, and expected edge cases are known to the reviewer.",
                "There is at least one manual spot-check or sample row that can confirm behaviour.",
                "The workbook is structured clearly enough that dependencies are visible.",
            ],
            "decision_points": [
                "Does the formula change a visible business metric or only a convenience output?",
                "Is the risk in the lookup logic, the filter logic, the date logic, or the error handling?",
                "Would a simpler formula be easier for the team to support later?",
                "Does the reviewer need a one-off answer or a pattern that can survive workbook growth?",
            ],
            "workflow_steps": [
                "Translate the requirement into plain English before reading the formula itself.",
                "Check inputs, expected outputs, and failure cases using a few representative rows.",
                "Inspect lookups, date handling, criteria logic, and spill behaviour separately rather than all at once.",
                "Rewrite clever but brittle output into simpler logic when maintainability matters more than compactness.",
                "Record any approved reusable pattern so later AI suggestions can be judged against it.",
            ],
            "standards": [
                "Review formulas against examples, not only against syntax.",
                "Prefer formulas the next analyst can explain without heroic effort.",
                "Document known edge cases such as blanks, duplicates, missing matches, or changing date windows.",
                "Treat AI-generated formulas as drafts until one human has verified the business logic.",
            ],
            "scenario_title": "Scenario: an AI-written margin formula starts feeding the leadership dashboard",
            "scenario_paragraphs": [
                "An analyst uses AI to generate a formula for margin by product family and region. The result looks impressive and seems to work on the first few rows, so it is copied across the reporting sheet. The real danger begins at that exact moment because the formula is now feeding a number that leaders will trust without seeing the underlying logic.",
                "A good review process breaks the risk apart. The analyst checks whether the lookup keys are unique, whether excluded returns are really excluded, whether blanks turn into zeros incorrectly, and whether the date filter matches the dashboard period. That is slower than blind trust, but far faster than explaining a wrong number after it has already circulated.",
                "Once the formula passes that review, the team documents why it is approved and what test rows validated it. The next time AI suggests a similar pattern, the analyst can compare it against a known good standard instead of starting the judgement from zero.",
            ],
            "metrics": [
                "Number of formula issues caught before outputs reach a stakeholder-facing sheet.",
                "Time required to review a new AI-generated formula against known test cases.",
                "How often approved formula patterns can be reused instead of revalidated from scratch.",
                "Reduction in workbook fragility caused by opaque or overly clever formulas.",
            ],
            "faq": [
                (
                    "What is the best first review question?",
                    "Ask what business rule the formula is supposed to encode. If that is unclear, syntax inspection will not save you.",
                ),
                (
                    "Should I prefer shorter formulas?",
                    "Not automatically. The better rule is understandable formulas. Sometimes a slightly longer formula is much easier to trust and maintain.",
                ),
                (
                    "How many sample rows should I test?",
                    "Enough to cover the normal path and the obvious edge cases. One happy-path row is rarely enough for meaningful review.",
                ),
                (
                    "When is AI formula help most dangerous?",
                    "When users copy a plausible-looking result into a high-visibility model without checking hidden assumptions around lookups, blanks, and time windows.",
                ),
                (
                    "Can this process be standardised?",
                    "Yes. The strongest teams use short review checklists and a library of known-good patterns so judgement becomes faster and more consistent.",
                ),
            ],
        },
        "python-in-excel-beginners": {
            "audience": "Excel-first analysts and curious professionals who want a practical starting point with Python in Excel rather than a programming detour",
            "value_case": "Python in Excel only creates durable value when readers understand where it complements worksheet formulas and where it adds needless complexity.",
            "prerequisites": [
                "You already know the spreadsheet problem you want to solve better, not merely that Python looks powerful.",
                "The workbook owner can explain the data source, expected outputs, and refresh rhythm.",
                "You are willing to keep the first use case narrow and reviewable.",
                "Colleagues who inherit the workbook will know that Python exists inside it and what it is doing.",
            ],
            "decision_points": [
                "Would a standard Excel formula or Power Query step solve this more simply?",
                "Is the job exploratory analysis, repeatable transformation, modelling support, or visualisation?",
                "Will the workbook be shared with colleagues who can support Python-based logic later?",
                "Does the extra analytical power justify the added support surface?",
            ],
            "workflow_steps": [
                "Start with one contained use case such as summary statistics, quick modelling, or exploratory transformation.",
                "Keep the Python cell close to the input table and document the expected output in plain language.",
                "Check the answer against a simpler Excel method on a small sample before trusting the bigger result.",
                "Separate exploratory notebooks-in-cells from the logic that genuinely belongs in the production workbook.",
                "Only expand the Python footprint after the first small use case has proved maintainable.",
            ],
            "standards": [
                "Explain what each Python block is for and what data it depends on.",
                "Avoid burying core business logic in opaque code cells no one else can review.",
                "Keep one workbook section for inputs, one for Python outputs, and one for reviewed presentation results.",
                "Document how a future owner should validate the Python result after changes.",
            ],
            "scenario_title": "Scenario: using Python in Excel for a first-pass risk analysis",
            "scenario_paragraphs": [
                "A finance analyst wants to compare several demand scenarios with more statistical flexibility than standard worksheet formulas offer. Python in Excel is attractive because it sits closer to the workbook than a separate notebook, but that convenience only helps if the use case stays understandable to the rest of the team.",
                "The analyst starts small: clean input table, one Python block, one reviewed output area, and one comparison against a simpler manual calculation. That gives the team confidence that the new layer is extending the workbook rather than hiding it behind code theatre.",
                "Once the pattern proves itself, Python can take on richer analysis. But the key discipline remains the same: the workbook still needs to be readable by humans who did not write the original code, and the result still needs a business owner who knows how to judge whether it makes sense.",
            ],
            "metrics": [
                "Time saved on analyses that were previously awkward with formulas alone.",
                "How often Python outputs match reviewed expectations on sample checks.",
                "Ease with which another teammate can understand and support the workbook.",
                "Number of use cases where Python genuinely improved clarity or capability rather than adding novelty.",
            ],
            "faq": [
                (
                    "Should beginners start with the PY function or broader Python workflows?",
                    "Start with the smallest practical use case that teaches the boundary between Excel-native logic and Python-assisted analysis. The goal is judgement, not feature collection.",
                ),
                (
                    "What is the biggest beginner mistake?",
                    "Using Python to prove sophistication rather than to solve a clear spreadsheet problem more cleanly.",
                ),
                (
                    "Does Python in Excel replace formulas?",
                    "No. It complements them. Formula logic is often still the best choice for transparent, maintainable workbook behaviour.",
                ),
                (
                    "How do I keep the workbook supportable?",
                    "Document inputs, outputs, and validation steps. If a teammate cannot tell what the Python cell does, the workbook is already too fragile.",
                ),
                (
                    "What makes this topic anchor-worthy?",
                    "It sits at a major decision boundary for modern Excel users: when to stay formula-first, when to add Python, and how to do it without losing workbook clarity.",
                ),
            ],
        },
        "copilot-excel-python-analysis": {
            "audience": "Excel users who want to combine Copilot and Python thoughtfully for deeper analysis without turning a workbook into a confusing black box",
            "value_case": "The strength of this topic is in the hand-off between natural-language assistance and analytical depth, not in treating AI and Python as interchangeable magic.",
            "prerequisites": [
                "The workbook already has a clean analytical base with clear tables and known assumptions.",
                "You can say which part of the job is better handled by guidance and which part needs explicit computation.",
                "Review ownership is clear once Copilot suggests an approach or Python produces a result.",
                "The team understands that deeper analysis increases the need for documentation, not the opposite.",
            ],
            "decision_points": [
                "Should Copilot help frame the question, prepare the workbook, or explain the result?",
                "What part of the analysis genuinely needs Python rather than a standard formula or chart?",
                "How will you validate the Python output before it informs a decision?",
                "Will the result remain readable to someone who did not build the original workflow?",
            ],
            "workflow_steps": [
                "Use Copilot first to structure the workbook question and identify the relevant data tables.",
                "Move into Python only for the deeper modelling or analytical step that benefits from it.",
                "Bring the result back into a clear worksheet layer that a reviewer can inspect quickly.",
                "Compare the analytical output against a simpler baseline or manual spot check.",
                "Document the boundary between what Copilot suggested and what Python computed.",
            ],
            "standards": [
                "Keep the explanatory layer, the analytical layer, and the presentation layer visibly separate.",
                "Label AI-assisted and Python-derived outputs so reviewers know what they are looking at.",
                "Retain a simpler baseline calculation whenever practical for confidence checks.",
                "Write down the assumptions and validation steps with the workbook, not in someone’s head.",
            ],
            "scenario_title": "Scenario: forecasting with natural-language framing and Python-backed analysis",
            "scenario_paragraphs": [
                "A planner wants to forecast demand for the next two quarters and explain the risk to leadership. Copilot is useful early because it can help frame the workbook question, summarise the available fields, and suggest what variables or scenarios the planner should compare. But Copilot is not the final analytical engine in that workflow.",
                "The deeper step happens in Python, where the analyst tests several assumptions, compares scenarios, and produces structured outputs that would be awkward to build with formulas alone. Even then, the real work is not finished. Those results need to come back into a worksheet area with clear labels, supporting notes, and spot checks against simpler expectations.",
                "When the planner presents the conclusion, the team can point to both the reasoning path and the computational path. That is the real advantage of combining Copilot and Python well: faster framing, deeper analysis, and a result that is still explainable to humans.",
            ],
            "metrics": [
                "Reduction in time spent framing complex analytical questions before modelling begins.",
                "Confidence level of reviewers when reading the final workbook outputs.",
                "Number of cases where Python added real analytical value instead of unnecessary complexity.",
                "How often the workflow can be rerun with fresh data and the same documented checks.",
            ],
            "faq": [
                (
                    "Should Copilot or Python come first?",
                    "Usually Copilot comes first for framing, structure, and explanation, while Python handles the deeper computation that deserves explicit code and validation.",
                ),
                (
                    "What breaks these workflows most often?",
                    "Messy source data and undocumented hand-offs. If reviewers cannot see where Copilot ended and Python began, trust falls quickly.",
                ),
                (
                    "Can small teams still use this well?",
                    "Yes, if they keep the use case narrow and the validation obvious. The size of the team matters less than the clarity of the workflow.",
                ),
                (
                    "How do you avoid analysis theatre?",
                    "By keeping the computation tied to a real decision and by showing how the result compares with a simpler baseline or expectation.",
                ),
                (
                    "Why is this stronger as an anchor than as a short post?",
                    "Because readers need the surrounding operating model: data preparation, task framing, analytical boundaries, validation, and presentation discipline.",
                ),
            ],
        },
    }
)

CATEGORY_REALITY: dict[str, dict[str, Any]] = {
    "AI + Excel": {
        "stack": "data shape, prompting, review steps, and stakeholder trust around the workbook output",
        "support_heading": "How to use this without turning AI into a black box",
        "support_bullets": [
            "Keep one reliable source table or range before you ask the model for interpretation.",
            "Treat AI output as draft support until a human has checked the logic and the business meaning.",
            "Capture the prompt and the review step when the task becomes repeatable.",
        ],
    },
    "Excel": {
        "stack": "table structure, formula clarity, edge cases, and what the workbook has to support next",
        "support_heading": "How to make this pattern hold up in a real workbook",
        "support_bullets": [
            "Check the data shape first, because most workbook pain starts upstream of the formula or feature.",
            "Prefer patterns that another analyst can still read and support later.",
            "Test the technique on one real edge case before you spread it across the model.",
        ],
    },
    "Flutter": {
        "stack": "architecture boundaries, developer workflow, testing discipline, and the release pressure around the code",
        "support_heading": "How to apply this in a production Flutter codebase",
        "support_bullets": [
            "Use the idea inside your existing architecture instead of letting one feature create a parallel pattern.",
            "Keep changes reviewable, measurable, and easy to test before you scale them.",
            "Turn the useful part of the lesson into a team convention so the next feature starts from a stronger baseline.",
        ],
    },
}


def build_generated_sections(post: dict[str, Any], new_lookup: dict[str, dict[str, Any]], old_lookup: dict[str, Post]) -> list[dict[str, Any]]:
    sections = build_support_sections(post, new_lookup, old_lookup)
    profile = ANCHOR_BLUEPRINTS.get(post["slug"])
    if profile:
        sections.extend(build_anchor_sections(post, profile, new_lookup, old_lookup))
    return sections


def build_support_sections(post: dict[str, Any], new_lookup: dict[str, dict[str, Any]], old_lookup: dict[str, Post]) -> list[dict[str, Any]]:
    lens = CATEGORY_REALITY[post["category"]]
    title = post["title"]
    related_links = build_related_links(new_lookup, old_lookup, post["related_new"] + post["related_old"])[:3]
    next_bullets = [
        f'Go next to <a href="{href}">{html_escape(link_title)}</a> if you want to deepen the surrounding workflow instead of treating {html_escape(title)} as an isolated trick.'
        for link_title, href in related_links
    ]
    return [
        {
            "heading": lens["support_heading"],
            "paragraphs": [
                f"{title} becomes much more useful once it is tied to the rest of the workflow around it. In real work, the result depends on {lens['stack']}, not only on following one local tip correctly.",
                "That is why the biggest win rarely comes from one clever move in isolation. It comes from making the surrounding process easier to review, easier to repeat, and easier to hand over when another person inherits the workbook or codebase later.",
            ],
            "bullets": lens["support_bullets"],
        },
        {
            "heading": "How to extend the workflow after this guide",
            "paragraphs": [
                "Once the core technique works, the next leverage usually comes from standardising it. That might mean naming inputs more clearly, keeping one review checklist, or pairing this page with neighbouring guides so the process becomes repeatable rather than person-dependent.",
                f"The follow-on guides below are the most natural next steps from {title}. They help move the reader from one useful page into a stronger connected system.",
            ],
            "bullets": next_bullets,
        },
    ]


def build_anchor_sections(
    post: dict[str, Any],
    profile: dict[str, Any],
    new_lookup: dict[str, dict[str, Any]],
    old_lookup: dict[str, Post],
) -> list[dict[str, Any]]:
    title = post["title"]
    related_links = build_related_links(new_lookup, old_lookup, post["related_new"] + post["related_old"])[:4]
    cluster_bullets = [
        f'Use <a href="{href}">{html_escape(link_title)}</a> when you are ready to deepen the next connected skill in the same workflow.'
        for link_title, href in related_links
    ]
    failure_bullets = list(post.get("mistakes", []))
    category_extra = {
        "AI + Excel": "Treating a confident answer as proof instead of as a draft that still needs human judgement.",
        "Excel": "Solving today’s example without checking whether the pattern will survive workbook growth or messy data.",
        "Flutter": "Letting one successful implementation turn into a local convention before the team has tested it under real delivery pressure.",
    }[post["category"]]
    if category_extra not in failure_bullets:
        failure_bullets.append(category_extra)

    faq_paragraphs = [
        "The deeper guides in this cluster tend to create implementation questions once readers move from curiosity to repeatable use. These are the follow-up issues that matter most in practice."
    ]
    for question, answer in profile["faq"]:
        faq_paragraphs.append(f"<strong>{html_escape(question)}</strong> {answer}")

    return [
        {
            "heading": "What changes when this has to work in real life",
            "paragraphs": [
                f"{title} often looks simpler in demos than it feels inside real delivery. The moment the topic becomes part of actual work for {profile['audience']}, the question expands beyond surface tactics. {profile['value_case']}",
                "That is why this page works best as an anchor rather than a thin explainer. The durable value comes from understanding the surrounding operating model: what has to be true before the technique works well, how the workflow should be reviewed, and what needs to be standardised once more than one person depends on the result.",
            ],
        },
        {
            "heading": "Prerequisites that make the guidance hold up",
            "paragraphs": [
                "Most execution pain does not come from the feature or technique alone. It comes from weak inputs, fuzzy ownership, or unclear expectations about what “good” looks like. When those foundations are missing, even a promising tactic turns into noise.",
                "If the team fixes the prerequisites first, the later steps become much easier to trust. Review becomes faster, hand-offs become clearer, and the surrounding workflow stops fighting the technique at every turn.",
            ],
            "bullets": profile["prerequisites"],
        },
        {
            "heading": "Decision points before you commit",
            "paragraphs": [
                "A lot of wasted effort comes from using the right tactic in the wrong situation. The best teams slow down long enough to answer a few decision questions before they scale a pattern or recommend it to others.",
                "Those decisions do not need a workshop. They just need to be explicit. Once the team knows the stakes, the owner, and the likely failure modes, the technique can be used far more confidently.",
            ],
            "bullets": profile["decision_points"],
        },
        {
            "heading": "A workflow that scales past one-off use",
            "paragraphs": [
                "The first successful result is not the finish line. The real test is whether the same approach can be rerun next week, by another person, on slightly messier inputs, and still produce something reviewable. That is where lightweight process beats isolated cleverness.",
                "A scalable workflow keeps the high-value judgement human and makes the repeatable parts easier to execute. It also creates checkpoints where the next reviewer can tell quickly whether the output is still behaving as intended.",
            ],
            "bullets": profile["workflow_steps"],
        },
        {
            "heading": "Where teams get bitten once the workflow repeats",
            "paragraphs": [
                "The failure modes usually become visible only after repetition. A workflow that feels fine once can become fragile when fresh data arrives, when another teammate runs it, or when the result starts feeding something more important downstream.",
                "That is why recurring failure patterns deserve explicit attention. Seeing them early is often the difference between a useful system and a trusted-looking mess that creates rework later.",
            ],
            "bullets": failure_bullets,
        },
        {
            "heading": "What to standardise if more than one person will use this",
            "paragraphs": [
                "If a workflow is genuinely valuable, it will not stay personal for long. Other people will copy it, inherit it, or depend on its outputs. Standardisation is how the team keeps that growth from turning into inconsistency.",
                "The good news is that the standards do not need to be heavy. A few clear conventions around inputs, review, naming, and ownership can remove a surprising amount of friction.",
            ],
            "bullets": profile["standards"],
        },
        {
            "heading": "How to review this when time is short",
            "paragraphs": [
                "Real teams rarely get the luxury of a perfect slow review every time. The better pattern is a compact review sequence that can still catch the most expensive mistakes under delivery pressure. That is especially important once the topic feeds reporting, production code, or anything another stakeholder will treat as trustworthy by default.",
                "A strong short-form review does not try to inspect everything equally. It focuses on the few checks that are most likely to expose a wrong boundary, a wrong assumption, or an output that sounds more confident than the evidence allows. Over time those checks become muscle memory and make the whole workflow safer without making it heavy.",
            ],
            "bullets": [
                "Confirm the exact input boundary before reviewing the output itself.",
                "Check one representative happy path and one realistic edge case before wider rollout.",
                "Ask what a wrong answer would look like here, then look for that failure directly.",
                "Keep one reviewer accountable for the final call even when several people touched the process.",
            ],
        },
        {
            "heading": profile["scenario_title"],
            "paragraphs": profile["scenario_paragraphs"],
        },
        {
            "heading": "Metrics that show the change is actually helping",
            "paragraphs": [
                "Longer guides are only worth it if they improve action. Teams should know what evidence would show the workflow is getting healthier, faster, or more trustworthy rather than assuming improvement because the process feels more sophisticated.",
                "Good metrics are practical and observable. They do not need to be elaborate. They just need to reveal whether the new pattern is reducing confusion, review effort, or delivery friction in the places that matter most.",
            ],
            "bullets": profile["metrics"],
        },
        {
            "heading": "How to hand this off without losing context",
            "paragraphs": [
                "Anchor pages become genuinely valuable once somebody else can use the pattern without sitting beside the original author. Handoff is where fragile workflows are exposed. If the next person cannot tell what the inputs are, what good output looks like, or what the review step is supposed to catch, the process is not yet mature enough for broader use.",
                "The simplest fix is to leave behind more operational context than most people expect: one example, one approved pattern, one list of checks, and one owner for questions. That is often enough to keep the workflow useful after staff changes, deadline pressure, or a fresh batch of data arrives.",
            ],
            "bullets": [
                "Document the input shape, the output expectation, and the owner in plain language.",
                "Keep one approved example or screenshot that shows what a good result looks like.",
                "Store the review checklist close to the workflow instead of burying it in chat history.",
                "Note which parts are fixed standards and which parts still require human judgement each run.",
            ],
        },
        {
            "heading": "Questions readers usually ask next",
            "paragraphs": faq_paragraphs,
        },
        {
            "heading": "A practical 30-60-90 day adoption path",
            "paragraphs": [
                "The cleanest way to adopt a workflow like this is in stages. Trying to jump straight from curiosity to team-wide standard usually creates avoidable resistance, because the process has not yet proved itself on live work. Short staged rollout keeps the learning visible and prevents false confidence.",
                "In the first month, the goal is proof on one bounded use case. In the second, the goal is repeatability and documentation. By the third, the workflow should either be strong enough to standardise or honest enough to reveal that it still needs redesign. That discipline is what turns a promising topic into a dependable operating habit.",
            ],
            "bullets": [
                "Days 1-30: prove the workflow on one repeated task with one accountable owner.",
                "Days 31-60: capture the prompt, inputs, review checks, and a known-good example.",
                "Days 61-90: decide whether the process is ready for wider rollout, needs tighter guardrails, or should stay a specialist pattern.",
                "After 90 days: review what changed in accuracy, speed, and team confidence before scaling further.",
            ],
        },
        {
            "heading": "How to explain the result so other people trust it for the right reasons",
            "paragraphs": [
                "A strong implementation still fails if the surrounding explanation is weak. Stakeholders do not simply need an output. They need enough context to understand what the result means, what it does not mean, and which parts were accelerated by process rather than proved by certainty. That is especially important when the work touches AI assistance, complex workbook logic, or engineering choices that are not obvious to non-specialists.",
                "The safest communication style is specific, bounded, and evidence-aware. Show what inputs were used, what review happened, and where human judgement still mattered. People trust workflows more when the explanation makes the quality controls visible instead of hiding them behind confident language.",
            ],
            "bullets": [
                "State the scope of the input and the date or environment the result applies to.",
                "Name the review or validation step that turned the draft into something shareable.",
                "Call out the key assumption or limitation instead of hoping nobody notices it later.",
                "Keep one example, comparison, or baseline nearby so the output feels grounded rather than magical.",
            ],
        },
        {
            "heading": "Signals that this should stay a specialist pattern, not a default",
            "paragraphs": [
                "Not every promising workflow deserves full standardisation. Some patterns are powerful precisely because they are handled by someone with enough context to judge nuance, exceptions, or downstream consequences. Teams save themselves a lot of friction when they can recognise that boundary early instead of trying to force every useful tactic into a universal operating rule.",
                "A good anchor page should therefore tell readers when to stop scaling. If the inputs stay unstable, if the review burden remains high, or if the business risk changes faster than the pattern can be documented, it may be smarter to keep the workflow specialist-owned while the rest of the team uses a simpler, safer default.",
            ],
            "bullets": [
                "The workflow still depends heavily on one person’s tacit judgement to stay safe.",
                "Fresh data or changing context breaks the process often enough that the checklist cannot keep up yet.",
                "Review takes almost as long as doing the work manually, so the promised leverage never really appears.",
                "Stakeholders need more certainty than the current workflow can honestly provide without extra controls.",
            ],
        },
        {
            "heading": "How this anchor connects to the rest of the workflow",
            "paragraphs": [
                "Anchor pages matter most when they help readers navigate the next layer with intention. Once this page is clear, the surrounding workflow usually becomes the next bottleneck rather than the topic itself.",
                f"That is why this guide links outward into neighbouring pages in the cluster. Used together, the pages below help turn {title} from a single insight into a broader repeatable capability. They also make it easier to sequence learning so readers build confidence in the right order instead of collecting disconnected tips.",
            ],
            "bullets": cluster_bullets,
        },
    ]


def main() -> None:
    if not NEW_POSTS:
        raise SystemExit("NEW_POSTS is empty.")
    existing = parse_existing_posts()
    new_lookup = {post["slug"]: post for post in NEW_POSTS}
    existing = {slug: post for slug, post in existing.items() if slug not in new_lookup}
    start = date(2026, 4, 1)
    rendered_posts: list[Post] = []
    for index, post_def in enumerate(NEW_POSTS):
        published = start.fromordinal(start.toordinal() - index)
        rendered_posts.append(create_post(post_def, new_lookup, existing, published))

    for post in rendered_posts:
        post.path.write_text(render_post_page(post), encoding="utf-8", newline="\n")

    all_posts = sorted(list(existing.values()) + rendered_posts, key=lambda item: (item.published, item.slug), reverse=True)
    BLOG_INDEX_PATH.write_text(render_archive_page(all_posts), encoding="utf-8", newline="\n")
    RSS_FILE.write_text(render_feed(all_posts), encoding="utf-8", newline="\n")
    SITEMAP_FILE.write_text(update_sitemap(rendered_posts), encoding="utf-8", newline="\n")

    cover_payload = []
    for post in rendered_posts:
        cover_payload.append(
            {
                "slug": post.slug,
                "title": post.title,
                "tag": post.category,
                "hook": post.cover_hook,
                "cta": post.cover_cta,
                "keywords": post.cover_keywords,
                "cue": post.cover_cue,
                "category": post.category,
                "imageAlt": post.image_alt,
            }
        )
    (ROOT / "scripts" / "blog_cluster_covers.json").write_text(
        json.dumps(cover_payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
        newline="\n",
    )
    anchor_count = sum(1 for post in rendered_posts if post.slug in ANCHOR_BLUEPRINTS)
    print(
        f"Built {len(rendered_posts)} new posts, including {anchor_count} anchor pages, "
        "updated blog index, feed, sitemap, and cover manifest."
    )


if __name__ == "__main__":
    main()
