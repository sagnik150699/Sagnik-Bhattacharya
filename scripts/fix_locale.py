"""Fix locale inconsistency across the site.
Standardizes to lang="en-GB" and og:locale="en_GB".
"""
import os
import glob

PUBLIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'public')
BLOG_DIR = os.path.join(PUBLIC_DIR, 'blog')

def fix_locale(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content

    # Fix HTML lang attribute: lang="en" -> lang="en-GB" (but not lang="en-GB" which is already correct)
    content = content.replace('lang="en"', 'lang="en-GB"')

    # Fix og:locale meta tag
    content = content.replace('content="en_IN"', 'content="en_GB"')

    # Fix inLanguage in JSON-LD (various spacing patterns)
    content = content.replace('"inLanguage":"en"', '"inLanguage":"en-GB"')
    content = content.replace('"inLanguage": "en"', '"inLanguage": "en-GB"')

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

changed = 0

# Process all blog posts
for f in sorted(glob.glob(os.path.join(BLOG_DIR, '*.html'))):
    if fix_locale(f):
        changed += 1
        print(f'  Fixed: {os.path.basename(f)}')

# Process top-level HTML pages
for name in ['index.html', 'about.html', 'courses.html', 'services.html', 'contact.html', 'blog.html']:
    filepath = os.path.join(PUBLIC_DIR, name)
    if os.path.exists(filepath) and fix_locale(filepath):
        changed += 1
        print(f'  Fixed: {name}')

# Process feed.xml (fix casing)
feed_path = os.path.join(PUBLIC_DIR, 'feed.xml')
if os.path.exists(feed_path):
    with open(feed_path, 'r', encoding='utf-8') as f:
        content = f.read()
    original = content
    content = content.replace('<language>en-gb</language>', '<language>en-GB</language>')
    if content != original:
        with open(feed_path, 'w', encoding='utf-8') as f:
            f.write(content)
        changed += 1
        print('  Fixed: feed.xml')

print(f'\nDone. {changed} files updated.')
