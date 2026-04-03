"""
Move breadcrumb from .page-hero into the blog <section>, remove .page-hero wrapper.
New structure:
  </nav>
  <section class="blog-section">
    <div class="container">
      <article class="blog-post">
        <nav class="blog-breadcrumb" ...>...</nav>
        <div class="blog-post-header reveal">
"""
import glob, re, os

blog_dir = os.path.join(os.path.dirname(__file__), '..', 'public', 'blog')
files = glob.glob(os.path.join(blog_dir, '*.html'))

count = 0
for f in sorted(files):
    with open(f, 'r', encoding='utf-8') as fh:
        html = fh.read()

    # Pattern: page-hero div containing breadcrumb, followed by section
    # Match the page-hero block and extract the breadcrumb nav
    pattern = r'<div class="page-hero" style="padding-bottom:20px">\s*<div class="container">\s*(<nav class="blog-breadcrumb"[^<]*(?:<[^>]*>[^<]*)*</nav>)\s*</div>\s*</div>\s*<section style="padding-top:0">\s*<div class="container">\s*<article class="blog-post">'

    match = re.search(pattern, html)
    if not match:
        print(f"SKIP (no match): {os.path.basename(f)}")
        continue

    breadcrumb = match.group(1).strip()

    replacement = f'''<section class="blog-section">
    <div class="container">
      <article class="blog-post">
        {breadcrumb}'''

    html = html[:match.start()] + replacement + html[match.end():]

    with open(f, 'w', encoding='utf-8') as fh:
        fh.write(html)

    count += 1
    print(f"FIXED: {os.path.basename(f)}")

print(f"\nDone: {count} files updated")
