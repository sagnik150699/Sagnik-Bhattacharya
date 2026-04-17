#!/usr/bin/env python3
"""Phase 4: Add missing Group B tutorial links to gemma-4-vscode hub page."""
import re
import os

hub_file = r"c:\Workspace\Sagnik Bhattacharya\public\blog\gemma-4-vscode.html"

with open(hub_file, "r", encoding="utf-8") as f:
    content = f.read()

# The hub has a Related section. We need to add Group B tutorials that are missing.
# Currently only has claude-code-vscode from Group B.
# Missing: claude-code-android-studio, copilot-agent-mode-vscode, deepseek-vscode,
#          gemini-cli-vscode, gemini-cli-android-studio-flutter, opencode-vscode,
#          windsurf-flutter-development, cursor-flutter-development

# Find the Related tutorials section and add Group B links
# Strategy: find the </ul> that closes the Related section and insert before it

# The related section currently ends with gemma-4-data-analysis-excel link
target = '<li><a href="/blog/gemma-4-data-analysis-excel">'
idx = content.find(target)
if idx < 0:
    print("Could not find target link in Related section")
    exit(1)

# Find the </ul> after this link
end_ul = content.find("</ul>", idx)
if end_ul < 0:
    print("Could not find closing </ul>")
    exit(1)

# Build the new Group B section to insert before </ul>
group_b_links = """<li><a href="/blog/copilot-agent-mode-vscode">Copilot Agent Mode in VS Code</a> \u2014 Microsoft\u2019s AI coding agent inside the editor.</li>
<li><a href="/blog/deepseek-vscode">DeepSeek in VS Code</a> \u2014 open-weight alternative for code completion.</li>
<li><a href="/blog/gemini-cli-vscode">Gemini CLI in VS Code</a> \u2014 Google\u2019s terminal-first AI coding tool.</li>
<li><a href="/blog/gemini-cli-android-studio-flutter">Gemini CLI for Android Studio and Flutter</a> \u2014 using Gemini CLI in mobile development workflows.</li>
<li><a href="/blog/opencode-vscode">OpenCode in VS Code</a> \u2014 open-source AI coding assistant.</li>
<li><a href="/blog/windsurf-flutter-development">Windsurf for Flutter Development</a> \u2014 agentic IDE for Flutter projects.</li>
<li><a href="/blog/cursor-flutter-development">Cursor for Flutter Development</a> \u2014 AI-first editor for Flutter apps.</li>
<li><a href="/blog/claude-code-android-studio">Claude Code in Android Studio</a> \u2014 Anthropic\u2019s coding agent for mobile dev.</li>
"""

content = content[:end_ul] + group_b_links + content[end_ul:]

with open(hub_file, "w", encoding="utf-8") as f:
    f.write(content)

print("Added 8 Group B tutorial links to hub Related section.")
