#!/usr/bin/env python3
"""Phase 4: Audit hub page outbound links and check reciprocal links from converted tutorials."""
import re
import os
import glob

blog_dir = r"c:\Workspace\Sagnik Bhattacharya\public\blog"
hub_file = os.path.join(blog_dir, "gemma-4-vscode.html")

with open(hub_file, "r", encoding="utf-8") as f:
    hub_content = f.read()

# 1. Map all outbound /blog/ links from hub
links = re.findall(r'href="(/blog/[^"]+)"', hub_content)
unique_links = sorted(set(links))
print(f"=== Hub outbound /blog/ links ({len(unique_links)}) ===")
for l in unique_links:
    print(f"  {l}")

# 2. Check which Group A tutorials link back to hub
group_a = [
    "gemma-4-android-studio-ollama.html",
    "gemma-4-data-analysis-excel.html",
    "run-gemma-4-locally.html",
    "gemma-4-local-ai-workflows.html",
]
group_b = [
    "claude-code-vscode.html",
    "claude-code-android-studio.html",
    "copilot-agent-mode-vscode.html",
    "deepseek-vscode.html",
    "gemini-cli-vscode.html",
    "gemini-cli-android-studio-flutter.html",
    "opencode-vscode.html",
    "windsurf-flutter-development.html",
    "cursor-flutter-development.html",
]

print(f"\n=== Reciprocal link check (tutorials -> hub) ===")
for group_name, group in [("Group A", group_a), ("Group B", group_b)]:
    print(f"\n--- {group_name} ---")
    for fname in group:
        fp = os.path.join(blog_dir, fname)
        if os.path.exists(fp):
            with open(fp, "r", encoding="utf-8") as f:
                c = f.read()
            has_hub_link = "gemma-4-vscode" in c
            slug = fname.replace(".html", "")
            hub_links_to_it = f"/blog/{slug}" in hub_content
            print(f"  {fname}: links→hub={has_hub_link}  hub→it={hub_links_to_it}")
        else:
            print(f"  {fname}: NOT FOUND")

# 3. Check Related Posts section in hub
rel = re.search(r'Related (Posts|tutorials|Tutorials)', hub_content)
if rel:
    # Extract the related section
    start = rel.start()
    end_ul = hub_content.find("</ul>", start)
    if end_ul > 0:
        section = hub_content[start:end_ul+5]
        related_links = re.findall(r'href="(/blog/[^"]+)"', section)
        print(f"\n=== Hub Related section links ({len(related_links)}) ===")
        for l in related_links:
            print(f"  {l}")
else:
    print("\nNo Related section found in hub")
