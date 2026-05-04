#!/usr/bin/env python3
"""Phase 3 batch processor for all remaining comparison pages.
For each file: adds verdict H2 if missing, adds hub link in Related section, renames to Related tutorials.
Does NOT touch article:modified_time (user rule: sitemap only)."""

import os
import re
import sys

blog_dir = r"c:\Workspace\Sagnik Bhattacharya\public\blog"

# Config per page: (filename, verdict_text, hub_links, faq_entries_if_missing)
# hub_links: list of (href, title, annotation) tuples to prepend to Related section
# verdict: HTML to insert as <h2>Which should you pick?</h2> block

pages = {
    "flutter-vs-react-native.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>If you are building a <strong>single codebase for iOS and Android</strong> with a focus on custom UI, smooth animations, and long-term widget control \u2014 choose <strong>Flutter</strong>. '
            'If your team already knows <strong>JavaScript/TypeScript</strong> and values a massive npm ecosystem with native module access \u2014 choose <strong>React Native</strong>. '
            'For greenfield projects in 2026 where the team has no prior mobile experience, Flutter\u2019s widget model and Dart\u2019s type safety make it the faster path to a polished app.</p>'
        ),
        "hubs": [
            ("/blog/flutter-guide", "Flutter Development Guide 2026", "the hub page indexing every Flutter tutorial on this site."),
        ],
    },
    "gemma-4-vs-chatgpt-vs-claude.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>If you need <strong>free, private, offline</strong> AI that runs on your own hardware \u2014 <strong>Gemma 4</strong>. '
            'If you need the strongest general reasoning and are comfortable with a paid API \u2014 <strong>Claude</strong> for structured analysis or <strong>ChatGPT</strong> for broad conversational tasks. '
            'Gemma 4 wins on privacy and cost; the cloud models win on raw capability and context window size.</p>'
        ),
        "hubs": [],  # already has hub link
    },
    "gemma-4-vs-gemini.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>If you want AI that <strong>runs locally with zero cloud dependency</strong> and full data privacy \u2014 <strong>Gemma 4</strong>. '
            'If you want the most capable Google AI with the largest context window and multimodal features \u2014 <strong>Gemini</strong>. '
            'Gemma is a local-first tool; Gemini is a cloud-first service. They solve fundamentally different problems.</p>'
        ),
        "hubs": [],  # already has hub link
    },
    "gemma-4-vs-gpt-vs-llama-excel.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>For <strong>Excel formula generation on your own machine</strong> with no data leaving your laptop \u2014 <strong>Gemma 4</strong> via Ollama. '
            'For the <strong>highest accuracy on complex formulas</strong> when you can send data to the cloud \u2014 <strong>GPT-4</strong>. '
            'For an <strong>open-source middle ground</strong> with strong coding ability \u2014 <strong>Llama</strong>. '
            'See <a href="/blog/gemma-4-data-analysis-excel">Gemma 4 vs ChatGPT for real Excel tasks</a> for head-to-head test results.</p>'
        ),
        "hubs": [
            ("/blog/excel-formulas-guide", "Excel Formulas: The Complete 2026 Reference", "the hub page for all Excel tutorials."),
            ("/blog/gemma-4-vscode", "AI Coding Tools Hub", "if you want to use these models inside your IDE."),
        ],
    },
    "gemma-4-vs-paid-ai-models.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>If <strong>privacy, cost, and offline access</strong> matter more than peak performance \u2014 <strong>Gemma 4</strong>. '
            'If you need <strong>maximum capability</strong> and can afford API costs \u2014 stick with paid models (Claude, GPT-4, Gemini Pro). '
            'The practical answer for most developers: use Gemma 4 for routine tasks and private data, switch to a paid model for the hardest problems.</p>'
        ),
        "hubs": [],  # already has hub link
    },
    "seedance-vs-veo-3.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>For <strong>precise prompt adherence and camera control</strong> in short-form video \u2014 <strong>Seedance 2.0</strong>. '
            'For <strong>raw photorealism and cinematic quality</strong> when prompt control matters less \u2014 <strong>Veo 3</strong>. '
            'Seedance gives you more directorial control; Veo 3 gives you prettier output with less steering.</p>'
        ),
        "hubs": [
            ("/blog/ai-guide", "The Complete AI Tools and AI Development Guide 2026", "the hub page indexing every AI tutorial, including Seedance."),
        ],
    },
    "seedance-vs-kling.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>For <strong>camera movement fidelity and prompt adherence</strong> \u2014 <strong>Seedance 2.0</strong>. '
            'For <strong>realistic human motion and longer clips</strong> \u2014 <strong>Kling</strong>. '
            'Seedance excels at cinematic camera work; Kling excels at natural body movement and facial expressions.</p>'
        ),
        "hubs": [
            ("/blog/ai-guide", "The Complete AI Tools and AI Development Guide 2026", "the hub page indexing every AI tutorial, including Seedance."),
        ],
    },
    "seedance-vs-sora-2.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>For <strong>prompt control, free credits, and consistent output</strong> \u2014 <strong>Seedance 2.0</strong>. '
            'For <strong>cinematic quality and OpenAI ecosystem integration</strong> (if you have a ChatGPT Plus subscription) \u2014 <strong>Sora 2</strong>. '
            'Seedance is the better choice for iterative workflows where prompt adherence matters more than raw visual fidelity.</p>'
        ),
        "hubs": [
            ("/blog/ai-guide", "The Complete AI Tools and AI Development Guide 2026", "the hub page indexing every AI tutorial, including Seedance."),
        ],
    },
    "vlookup-vs-xlookup.html": {
        "verdict": None,  # already has verdict
        "hubs": [
            ("/blog/excel-formulas-guide", "Excel Formulas: The Complete 2026 Reference", "the hub page for all Excel tutorials."),
        ],
    },
    "groupby-vs-pivottable-excel.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>If you need <strong>formula-driven summaries that auto-update</strong> and you are on Microsoft 365 \u2014 <strong>GROUPBY</strong>. '
            'If you need <strong>interactive filtering, drill-down, and slicers</strong> for stakeholder dashboards \u2014 <strong>PivotTable</strong>. '
            'For most analysts: learn PivotTables first (they work everywhere), then add GROUPBY for the cases where a formula is cleaner than a pivot.</p>'
        ),
        "hubs": [
            ("/blog/excel-formulas-guide", "Excel Formulas: The Complete 2026 Reference", "the hub page for all Excel tutorials."),
        ],
    },
    "analyst-vs-agent-mode-vs-copilot-chat.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>For <strong>exploratory data analysis with natural language</strong> \u2014 <strong>Analyst</strong> (if available in your M365 tier). '
            'For <strong>multi-step workbook automation</strong> (formatting, chart creation, formula writing in sequence) \u2014 <strong>Agent Mode</strong>. '
            'For <strong>quick one-off questions</strong> about your data \u2014 <strong>Copilot Chat</strong>. '
            'They are three layers of the same Copilot stack, not competitors.</p>'
        ),
        "hubs": [
            ("/blog/excel-formulas-guide", "Excel Formulas: The Complete 2026 Reference", "the hub page for all Excel tutorials."),
        ],
    },
    "flutter-web-skwasm-vs-canvaskit.html": {
        "verdict": (
            '<h2>Which should you pick?</h2>'
            '<p>For <strong>content-heavy web apps where SEO and load time matter</strong> \u2014 <strong>skwasm</strong> (smaller bundle, faster paint). '
            'For <strong>pixel-perfect rendering and complex custom painting</strong> \u2014 <strong>CanvasKit</strong> (full Skia engine). '
            'For most Flutter web projects in 2026, skwasm is the default recommendation unless you have specific rendering requirements that only CanvasKit can meet.</p>'
        ),
        "hubs": [
            ("/blog/flutter-guide", "Flutter Development Guide 2026", "the hub page indexing every Flutter tutorial."),
        ],
    },
}

total_changes = 0

for filename, config in pages.items():
    fp = os.path.join(blog_dir, filename)
    if not os.path.exists(fp):
        print(f"SKIP {filename}: file not found")
        continue

    with open(fp, "r", encoding="utf-8") as f:
        content = f.read()

    file_changes = 0

    # 1. Add verdict if needed
    if config["verdict"] and not re.search(r'<h2[^>]*>Which [Ss]hould [Yy]ou [Pp]ick', content):
        # Insert before the first Related/Sources section near the end
        # Find last </ul> before blog-cta-box or footer, insert verdict before Related Posts/guides
        # Strategy: insert before the Related Posts/guides/tutorials heading
        related_match = re.search(r'<h2>Related (Posts|guides|tutorials|Tutorials)[^<]*</h2>', content)
        sources_match = re.search(r'<h2>Sources', content)
        official_match = re.search(r'<h2>Official references', content)

        insert_point = None
        for m in [related_match, sources_match, official_match]:
            if m:
                insert_point = m.start()
                break

        if insert_point:
            content = content[:insert_point] + config["verdict"] + "\n" + content[insert_point:]
            file_changes += 1
            print(f"  {filename}: Added verdict H2")
        else:
            # fallback: insert before blog-cta-box
            cta_match = re.search(r'<div class="blog-cta-box">', content)
            if cta_match:
                content = content[:cta_match.start()] + config["verdict"] + "\n" + content[cta_match.start():]
                file_changes += 1
                print(f"  {filename}: Added verdict H2 (before CTA)")
            else:
                print(f"  {filename}: WARNING - could not find insertion point for verdict")

    # 2. Add hub links to Related section
    if config["hubs"]:
        # Find Related Posts/guides/tutorials section and prepend hub links
        related_pattern = re.compile(
            r'(<h2>Related (?:Posts|guides|tutorials|Tutorials)[^<]*</h2>\s*(?:<p>[^<]*</p>\s*)?<ul>\s*)'
        )
        m = related_pattern.search(content)
        if m:
            hub_items = ""
            for href, title, annotation in config["hubs"]:
                if href not in content.split("Related")[1] if "Related" in content else href not in content:
                    # Only add if not already linked in Related section
                    hub_items += f'<li><a href="{href}">{title}</a> \u2014 {annotation}</li>\n'
            if hub_items:
                content = content[:m.end()] + hub_items + content[m.end():]
                file_changes += 1
                print(f"  {filename}: Added {len(config['hubs'])} hub link(s)")

    # 3. Rename "Related Posts" or "Related guides" to "Related tutorials"
    if "<h2>Related Posts</h2>" in content:
        content = content.replace("<h2>Related Posts</h2>", '<h2>Related tutorials on this site</h2>')
        file_changes += 1
        print(f"  {filename}: Renamed Related Posts -> Related tutorials")
    elif "<h2>Related guides on this site</h2>" in content:
        content = content.replace("<h2>Related guides on this site</h2>", '<h2>Related tutorials on this site</h2>')
        file_changes += 1
        print(f"  {filename}: Renamed Related guides -> Related tutorials")

    if file_changes > 0:
        with open(fp, "w", encoding="utf-8") as f:
            f.write(content)
        total_changes += file_changes
        print(f"  {filename}: {file_changes} changes saved")
    else:
        print(f"  {filename}: no changes needed")

print(f"\nTotal: {total_changes} changes across all files.")
