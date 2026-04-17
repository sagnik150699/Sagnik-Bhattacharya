"""Build delete-vs-expand shortlist for thin/orphaned tutorials.

Inputs:
  - reports/word-counts-2026-04-17.md  (from count_blog_words.py)
  - public/**/*.html                    (sitewide inbound link scan)

Output:
  - reports/delete-vs-expand-shortlist.md

Recommendation logic:
  - meta-refresh redirect stub        -> delete-stub (replace with firebase 301)
  - in Phase 2 priority list          -> expand (must convert; never delete)
  - comparison page (-vs-, _vs_)      -> keep (handled by Phase 3 light pass)
  - bottom-quartile words AND 0 inbound -> delete
  - bottom-quartile words AND >0 inbound -> expand
  - everything else                   -> keep
"""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
PUBLIC = ROOT / "public"
BLOG = PUBLIC / "blog"
WC_PATH = ROOT / "reports" / f"word-counts-{date.today().isoformat()}.md"
OUT = ROOT / "reports" / "delete-vs-expand-shortlist.md"

# Tutorials in Phase 2 priority groups (must NEVER be marked delete)
PRIORITY_SLUGS = {
    # Group A
    "gemma-4-android-studio-ollama", "gemma-4-data-analysis-excel",
    "run-gemma-4-locally", "run-gemma-4-own-machine",
    "gemma-4-local-ai-workflows",
    # Group B
    "claude-code-vscode", "claude-code-android-studio",
    "copilot-agent-mode-vscode", "deepseek-vscode",
    "gemini-cli-vscode", "gemini-cli-android-studio-flutter",
    "opencode-vscode", "windsurf-flutter-development",
    "cursor-flutter-development",
}

# The hub itself: never touch
HUB = "gemma-4-vscode"

WC_LINE_RE = re.compile(r"^\| \d+ \| (\d+) \| `([^`]+)` \| (.*?) \|$")


def load_word_counts() -> list[tuple[int, str, str]]:
    rows = []
    for line in WC_PATH.read_text(encoding="utf-8").splitlines():
        m = WC_LINE_RE.match(line)
        if m:
            rows.append((int(m.group(1)), m.group(2), m.group(3)))
    return rows


def is_redirect_stub(name: str) -> bool:
    text = (BLOG / name).read_text(encoding="utf-8", errors="replace")
    return bool(re.search(r'<meta[^>]+http-equiv=["\']?refresh', text, re.I))


CONTENT_RE = re.compile(
    r'<div class="blog-post-content">(.*?)</div>\s*</article>', re.S
)


def count_inbound_links() -> dict[str, int]:
    """For each tutorial slug, count contextual inbound links — hrefs to
    /blog/<slug> from inside another tutorial's .blog-post-content body.

    This deliberately excludes:
      - blog.html grid (every tutorial appears there; not a quality signal)
      - sitemap/feed/llms files (mechanical lists)
      - nav/footer links inside other tutorials
    """
    inbound: dict[str, int] = defaultdict(int)
    slugs = {f.stem for f in BLOG.glob("*.html")}

    for html_file in BLOG.glob("*.html"):
        text = html_file.read_text(encoding="utf-8", errors="replace")
        m = CONTENT_RE.search(text)
        if not m:
            continue
        body = m.group(1)
        own_slug = html_file.stem
        for href in re.findall(r'href="([^"]+)"', body):
            href = href.split("#", 1)[0].split("?", 1)[0].rstrip("/")
            tm = re.match(r"^/blog/([\w\-]+)(?:\.html)?$", href)
            if not tm:
                continue
            target = tm.group(1)
            if target in slugs and target != own_slug:
                inbound[target] += 1
    return inbound


def is_comparison(name: str) -> bool:
    stem = name.removesuffix(".html")
    return "-vs-" in stem


def recommend(name: str, words: int, inbound: int, note: str,
              q1_threshold: int) -> tuple[str, str]:
    """Return (recommendation, suggested-angle-or-reason)."""
    slug = name.removesuffix(".html")

    if note == "meta-refresh redirect stub (not a real tutorial)":
        return "delete-stub", "Replace meta-refresh stub with firebase 301; remove .html file"

    if slug == HUB:
        return "keep", "THE HUB — never touch"

    if slug in PRIORITY_SLUGS:
        return "expand", "Phase 2 priority — convert per 2A-2E micro-tasks"

    if is_comparison(name):
        return "keep", "Phase 3 comparison — light pass (verdict + FAQ)"

    if words <= q1_threshold:
        if inbound == 0:
            return "delete", f"Thin ({words}w) AND zero inbound links"
        return "expand", f"Thin ({words}w) but has {inbound} inbound links — propose unique angle"

    return "keep", ""


def suggest_angle(slug: str) -> str:
    """Placeholder unique-title hint — only filled for expand candidates we
    haven't otherwise tagged."""
    keywords = slug.replace("-", " ")
    return f"TBD: search-gap angle around `{keywords}` (user to confirm in Task 2A)"


def main():
    wc_rows = load_word_counts()
    inbound = count_inbound_links()

    # Bottom-quartile threshold (excluding redirect stubs which have words=0)
    real_words = sorted(w for w, _, note in wc_rows if "redirect" not in note)
    q1_idx = max(0, len(real_words) // 4 - 1)
    q1_threshold = real_words[q1_idx]

    # Build shortlist: include all rows where recommendation != keep, OR where
    # recommendation == keep but inbound == 0 (orphan, worth surfacing).
    shortlist = []
    for words, name, note in wc_rows:
        slug = name.removesuffix(".html")
        ib = inbound.get(slug, 0)
        rec, reason = recommend(name, words, ib, note, q1_threshold)
        if rec == "expand" and not reason.startswith("Phase 2") and not reason.startswith("Thin"):
            reason = suggest_angle(slug)
        # Surface candidate if non-keep, OR keep-but-zero-inbound (orphan)
        if rec != "keep" or ib == 0:
            shortlist.append((rec, words, ib, name, reason))

    # Sort: deletes first, then expands by ascending words, then keeps
    rec_order = {"delete-stub": 0, "delete": 1, "expand": 2, "keep": 3}
    shortlist.sort(key=lambda r: (rec_order[r[0]], r[1], r[3]))

    lines = [
        f"# Delete-vs-expand shortlist ({date.today().isoformat()})",
        "",
        f"Bottom-quartile word threshold: **{q1_threshold} words** "
        f"(based on {len(real_words)} non-stub tutorials).",
        "",
        "Inbound link count = number of `<a href=\"/blog/<slug>\">` references "
        "from any HTML file under `public/` (excluding self-links).",
        "",
        "## Legend",
        "- **delete-stub**: meta-refresh redirect; replace with firebase 301 + remove file",
        "- **delete**: thin AND orphaned; cascade per Phase 1 template",
        "- **expand**: thin or priority; convert per Phase 2 micro-tasks",
        "- **keep**: in shortlist only because it has zero inbound links (worth checking)",
        "",
        "| Rec | Words | Inbound | File | Reason / suggested angle |",
        "|---|---:|---:|---|---|",
    ]
    for rec, words, ib, name, reason in shortlist:
        lines.append(f"| **{rec}** | {words} | {ib} | `{name}` | {reason} |")

    # Summary counts
    counts = defaultdict(int)
    for rec, *_ in shortlist:
        counts[rec] += 1
    lines += [
        "",
        "## Summary",
        f"- delete-stub: **{counts['delete-stub']}**",
        f"- delete: **{counts['delete']}**",
        f"- expand: **{counts['expand']}**",
        f"- keep (orphans worth checking): **{counts['keep']}**",
        f"- total surfaced: **{len(shortlist)}** of {len(wc_rows)} tutorials",
    ]

    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)}")
    for k, v in counts.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
