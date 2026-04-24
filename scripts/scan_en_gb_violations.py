"""Sitewide en-GB consistency scan.

Reuses american_spellings() logic from audit_blog_cluster.py + the
BRITISH_REPLACEMENTS map from build_blog_cluster.py. Strips <script>
and <style> blocks before scanning so CSS color/optimize tokens don't
generate false positives.

Output: reports/en-gb-violations-2026-04-17.md
"""
from __future__ import annotations

import html as html_module
import re
import sys
from collections import Counter
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from build_blog_cluster import BRITISH_REPLACEMENTS  # noqa: E402

PUBLIC = ROOT / "public"
OUT = ROOT / "reports" / f"en-gb-violations-{date.today().isoformat()}.md"

AMERICAN_WORDS = tuple(sorted(BRITISH_REPLACEMENTS.keys(), key=len, reverse=True))
PATTERN = re.compile(r"\b(" + "|".join(map(re.escape, AMERICAN_WORDS)) + r")\b", re.I)
UI_LABEL_EXCEPTIONS = (
    "Trust Center",
    "Merge & Center",
    "Center Across Selection",
)


def strip_invisible(html: str) -> str:
    """Remove script/style blocks, code/pre blocks, AND attribute values
    so we only scan VISIBLE PROSE — never code where words like `Color`
    or `analyze` are real API names that must not be normalised."""
    html = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<style[^>]*>.*?</style>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<pre[^>]*>.*?</pre>", " ", html, flags=re.S | re.I)
    html = re.sub(r"<code[^>]*>.*?</code>", " ", html, flags=re.S | re.I)
    # Drop everything inside tag brackets (incl. attribute values)
    html = re.sub(r"<[^>]+>", " ", html)
    html = html_module.unescape(html)
    for label in UI_LABEL_EXCEPTIONS:
        html = re.sub(re.escape(label), " ", html, flags=re.I)
    return re.sub(r"\s+", " ", html).strip()


def scan(path: Path) -> Counter:
    text = path.read_text(encoding="utf-8", errors="replace")
    visible = strip_invisible(text)
    return Counter(m.group(1).lower() for m in PATTERN.finditer(visible))


def main():
    targets = sorted(PUBLIC.glob("blog/*.html")) + sorted(
        p for p in PUBLIC.glob("*.html") if p.name != "404.html"
    )

    rows = []
    for f in targets:
        violations = scan(f)
        if violations:
            rows.append((sum(violations.values()), f.relative_to(PUBLIC).as_posix(), violations))

    rows.sort(reverse=True)

    word_totals = Counter()
    for _, _, c in rows:
        word_totals.update(c)

    lines = [
        f"# en-GB consistency violations ({date.today().isoformat()})",
        "",
        f"Files scanned: {len(targets)}  ",
        f"Files with violations: {len(rows)}  ",
        f"Total American spellings detected in visible prose: {sum(word_totals.values())}",
        "",
        "## Most common offending words",
        "",
        "| US spelling | GB replacement | Total occurrences |",
        "|---|---|---:|",
    ]
    for word, count in word_totals.most_common():
        lines.append(f"| `{word}` | `{BRITISH_REPLACEMENTS[word]}` | {count} |")

    lines += [
        "",
        "## Per-file violations (worst first)",
        "",
        "| Total | File | Words found |",
        "|---:|---|---|",
    ]
    for total, name, c in rows:
        words = ", ".join(f"`{w}`x{n}" for w, n in c.most_common())
        lines.append(f"| {total} | `{name}` | {words} |")

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    print(f"  files w/ violations: {len(rows)} / {len(targets)}")
    print(f"  total occurrences: {sum(word_totals.values())}")
    print(f"  top 5 words: {word_totals.most_common(5)}")


if __name__ == "__main__":
    main()
