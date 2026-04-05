"""Remove dateModified from blog posts where it equals datePublished.
Handles both indented (older) and minified (newer) JSON-LD formats.
Also removes article:modified_time meta tag when redundant.
"""
import os
import re
import json
import glob

BLOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'public', 'blog')

def fix_date_modified(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Extract datePublished
    pub_match = re.search(r'"datePublished"\s*:\s*"([^"]*)"', content)
    if not pub_match:
        return False
    pub_date = pub_match.group(1)

    # Check if dateModified equals datePublished
    mod_match = re.search(r'"dateModified"\s*:\s*"([^"]*)"', content)
    if not mod_match or mod_match.group(1) != pub_date:
        return False

    # Remove dateModified from JSON-LD
    # Pattern 1: ,"dateModified":"YYYY-MM-DD" (at end, comma before)
    content = re.sub(r',\s*"dateModified"\s*:\s*"[^"]*"(?=\s*[,}])', '', content)
    # Pattern 2: "dateModified":"YYYY-MM-DD", (comma after, on same line or own line)
    content = re.sub(r'"dateModified"\s*:\s*"[^"]*"\s*,\s*', '', content)
    # Pattern 3: standalone on its own line (indented, no comma issues remaining)
    content = re.sub(r'\s*"dateModified"\s*:\s*"[^"]*"', '', content)

    # Remove article:modified_time meta tag if value equals datePublished
    content = re.sub(
        r'\s*<meta\s+property="article:modified_time"\s+content="' + re.escape(pub_date) + r'"\s*/?>',
        '',
        content
    )

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

changed = 0
errors = []

for f in sorted(glob.glob(os.path.join(BLOG_DIR, '*.html'))):
    basename = os.path.basename(f)
    if fix_date_modified(f):
        changed += 1
        print(f'  Fixed: {basename}')

# Validate JSON-LD in all modified files
print('\nValidating JSON-LD...')
for f in sorted(glob.glob(os.path.join(BLOG_DIR, '*.html'))):
    with open(f, 'r', encoding='utf-8') as fh:
        content = fh.read()
    for match in re.finditer(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL):
        try:
            json.loads(match.group(1))
        except json.JSONDecodeError as e:
            errors.append(f'{os.path.basename(f)}: {e}')

if errors:
    print(f'\nJSON-LD ERRORS ({len(errors)}):')
    for err in errors:
        print(f'  {err}')
else:
    print('All JSON-LD valid.')

print(f'\nDone. {changed} files updated.')
