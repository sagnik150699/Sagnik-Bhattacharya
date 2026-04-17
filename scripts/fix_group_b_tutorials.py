"""
Batch fix Group B tutorials:
1. Sync FAQPage JSON-LD to match visible FAQ (add missing 3rd entry)
2. Rename "Related Posts" → "Related Tutorials"
3. Add claude-code-vscode link if missing
4. Add gemma-4-vscode hub link if missing (with annotation)
"""

import re, json, os
from bs4 import BeautifulSoup

BLOG_DIR = r"C:\Workspace\Sagnik Bhattacharya\public\blog"

FILES = [
    "deepseek-vscode",
    "gemini-cli-vscode",
    "gemini-cli-android-studio-flutter",
    "opencode-vscode",
    "windsurf-flutter-development",
    "cursor-flutter-development",
]

# Annotations for the hub link per tutorial
HUB_ANNOTATIONS = {
    "deepseek-vscode": "the free local AI coding alternative",
    "gemini-cli-vscode": "the free local Ollama-based alternative",
    "gemini-cli-android-studio-flutter": "the free local AI coding setup for VS Code",
    "opencode-vscode": "the free local AI coding alternative",
    "windsurf-flutter-development": "the free local AI coding alternative for VS Code",
    "cursor-flutter-development": "the free local AI coding alternative for VS Code",
}

CLAUDE_CODE_ANNOTATIONS = {
    "deepseek-vscode": "the strongest agentic coding tool for VS Code",
    "gemini-cli-vscode": "the strongest agentic coding tool for VS Code",
    "gemini-cli-android-studio-flutter": "the strongest agentic terminal coding tool",
    "opencode-vscode": "the strongest agentic coding tool for VS Code",
    "windsurf-flutter-development": "the paid agentic alternative for complex refactoring",
    "cursor-flutter-development": "the terminal-based agentic alternative",
}

def get_visible_faqs(soup):
    """Extract visible FAQ Q&A pairs from the HTML."""
    faqs = []
    for h2 in soup.find_all("h2"):
        text = h2.get_text(strip=True)
        if "Frequently Asked" in text or "FAQ" in text:
            for sib in h2.find_next_siblings():
                if sib.name == "h2":
                    break
                if sib.name == "h3":
                    q = sib.get_text(strip=True)
                    ans_p = sib.find_next_sibling("p")
                    a = ans_p.get_text(strip=True) if ans_p else ""
                    faqs.append((q, a))
    return faqs


def fix_faq_schema(html, visible_faqs):
    """Replace FAQPage JSON-LD to match visible FAQs."""
    # Find existing FAQPage script
    pattern = r'<script type="application/ld\+json">\s*\{[^}]*"@type"\s*:\s*"FAQPage".*?\}\s*</script>'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        return html

    # Build new FAQPage with all visible entries
    entries = []
    for q, a in visible_faqs:
        # Escape for JSON
        q_esc = q.replace('"', '\\"').replace("\n", " ")
        a_esc = a.replace('"', '\\"').replace("\n", " ")
        entries.append(f'''    {{
      "@type": "Question",
      "name": "{q_esc}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{a_esc}"
      }}
    }}''')

    new_schema = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
''' + ",\n".join(entries) + '''
  ]
}
  </script>'''

    return html[:match.start()] + new_schema + html[match.end():]


def fix_related_section(html, slug):
    """Replace Related Posts with Related Tutorials, adding hub + claude-code links."""
    has_hub = "gemma-4-vscode" in html
    has_claude = "claude-code-vscode" in html

    # Find the Related Posts/Tutorials section
    pattern = r'<h2>Related (?:Posts|Tutorials)</h2>\s*<ul>(.*?)</ul>'
    match = re.search(pattern, html, re.DOTALL)
    if not match:
        return html

    existing_lis = match.group(1)

    # Parse existing links
    existing_links = re.findall(r'<li>.*?</li>', existing_lis, re.DOTALL)

    # Build new list
    new_lis = []

    # Add hub link if missing
    if not has_hub:
        ann = HUB_ANNOTATIONS.get(slug, "the free local AI coding alternative")
        new_lis.append(f'  <li><a href="/blog/gemma-4-vscode">How to Use Gemma 4 in VS Code: Setup, Extensions, and Coding Workflows</a> \u2014 {ann}</li>')

    # Add claude-code-vscode if missing
    if not has_claude:
        ann = CLAUDE_CODE_ANNOTATIONS.get(slug, "the strongest agentic coding tool")
        new_lis.append(f'  <li><a href="/blog/claude-code-vscode">Claude Code in VS Code: Extension Setup + Hybrid Workflow with Copilot (2026)</a> \u2014 {ann}</li>')

    # Keep existing links (skip if they're the hub link we just added)
    for li in existing_links:
        li_stripped = li.strip()
        if li_stripped:
            new_lis.append(f"  {li_stripped}")

    new_section = '<h2>Related Tutorials</h2>\r\n<ul>\r\n' + '\r\n'.join(new_lis) + '\r\n</ul>'

    return html[:match.start()] + new_section + html[match.end():]


def process_file(slug):
    path = os.path.join(BLOG_DIR, f"{slug}.html")
    html = open(path, "r", encoding="utf-8").read()
    soup = BeautifulSoup(html, "html.parser")

    visible_faqs = get_visible_faqs(soup)
    print(f"\n{slug}: {len(visible_faqs)} visible FAQs")

    # 1. Fix FAQ schema
    html = fix_faq_schema(html, visible_faqs)

    # 2. Fix Related section
    html = fix_related_section(html, slug)

    # Write back
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)

    # Verify
    verify_soup = BeautifulSoup(html, "html.parser")
    faq_count = 0
    for script in verify_soup.find_all("script", type="application/ld+json"):
        try:
            d = json.loads(script.string)
            if d.get("@type") == "FAQPage":
                faq_count = len(d.get("mainEntity", []))
        except:
            pass
    has_hub = "gemma-4-vscode" in html
    has_claude = "claude-code-vscode" in html
    has_related_tutorials = "Related Tutorials" in html
    print(f"  faq_schema={faq_count} hub={has_hub} claude={has_claude} related_tutorials={has_related_tutorials}")


if __name__ == "__main__":
    for slug in FILES:
        process_file(slug)
    print("\nDone!")
