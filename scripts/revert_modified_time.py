#!/usr/bin/env python3
"""Revert modified_time additions from task 3.1 + apply Phase 3 to flutter-vs-react-native.html."""
import sys

# 1. Revert modified_time from chatgpt-vs-claude-vs-copilot-vs-gemini-excel.html
fp1 = r"c:\Workspace\Sagnik Bhattacharya\public\blog\chatgpt-vs-claude-vs-copilot-vs-gemini-excel.html"
with open(fp1, "r", encoding="utf-8") as f:
    c = f.read()

reverts = 0
# Remove article:modified_time meta
old = '  <meta property="article:modified_time" content="2026-04-17">\r\n'
if old in c:
    c = c.replace(old, '')
    reverts += 1
# Also try without \r\n
old2 = '  <meta property="article:modified_time" content="2026-04-17">\n'
if old2 in c:
    c = c.replace(old2, '')
    reverts += 1

# Revert dateModified in BlogPosting
if '"dateModified":"2026-04-17",' in c:
    c = c.replace('"dateModified":"2026-04-17",', '')
    reverts += 1

if reverts > 0:
    with open(fp1, "w", encoding="utf-8") as f:
        f.write(c)
    print(f"Reverted {reverts} modified_time changes from chatgpt-vs-claude-vs-copilot-vs-gemini-excel.html")
else:
    print("No modified_time to revert in chatgpt-vs-claude-vs-copilot-vs-gemini-excel.html")
