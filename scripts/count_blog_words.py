"""Word count audit for public/blog/*.html article bodies.

Strips HTML, isolates the .blog-post-content container, removes
<script>/<style>/<nav>/<footer>, then counts whitespace tokens.
Sorts ascending so the thinnest tutorials are at the top.

Output: reports/word-counts-2026-04-17.md
"""
from pathlib import Path
from datetime import date
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "public" / "blog"
OUT = ROOT / "reports" / f"word-counts-{date.today().isoformat()}.md"


def count_words(html: str) -> tuple[int, str]:
    soup = BeautifulSoup(html, "html.parser")

    # Detect redirect stubs (meta-refresh) — not real tutorials
    meta_refresh = soup.find("meta", attrs={"http-equiv": re.compile(r"^refresh$", re.I)})
    if meta_refresh is not None:
        return 0, "redirect-stub"

    container = soup.select_one(".blog-post-content")
    fallback = container is None
    if container is None:
        container = soup.body or soup
    for tag in container.select("script, style, nav, footer, .nav, .site-nav, .breadcrumbs"):
        tag.decompose()
    text = container.get_text(" ", strip=True)
    words = re.findall(r"\b[\w'-]+\b", text)
    return len(words), "fallback" if fallback else "ok"


def main():
    rows = []
    for f in sorted(BLOG.glob("*.html")):
        html = f.read_text(encoding="utf-8")
        wc, mode = count_words(html)
        rows.append((wc, f.name, mode))

    rows.sort()

    lines = [
        f"# Blog word counts ({date.today().isoformat()})",
        "",
        f"Total tutorials: {len(rows)}  ",
        f"Container probed: `.blog-post-content` (fallback to `<body>` if missing)",
        "",
        "| # | Words | File | Note |",
        "|---|------:|------|------|",
    ]
    note_map = {
        "ok": "",
        "fallback": "no .blog-post-content (used <body>)",
        "redirect-stub": "meta-refresh redirect stub (not a real tutorial)",
    }
    for i, (wc, name, mode) in enumerate(rows, 1):
        lines.append(f"| {i} | {wc} | `{name}` | {note_map[mode]} |")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({len(rows)} tutorials)")
    print(f"Thinnest 5: {rows[:5]}")


if __name__ == "__main__":
    main()
