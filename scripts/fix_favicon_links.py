"""Replace broken /favicon.svg + /apple-touch-icon.png links with the
sitewide pattern that uses existing favicon-*.png files."""
from pathlib import Path

OLD = (
    '  <link rel="icon" type="image/svg+xml" href="/favicon.svg">\n'
    '  <link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">\n'
)
NEW = (
    '  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">\n'
    '  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">\n'
    '  <link rel="apple-touch-icon" sizes="180x180" href="/favicon-180x180.png">\n'
)

ROOT = Path(__file__).resolve().parent.parent / "public"
targets = [ROOT / "blog.html"] + sorted((ROOT / "blog").glob("*.html"))

changed = 0
for f in targets:
    text = f.read_text(encoding="utf-8")
    if OLD in text:
        f.write_text(text.replace(OLD, NEW), encoding="utf-8")
        changed += 1
        print(f"fixed: {f.relative_to(ROOT.parent)}")

print(f"\nTotal files fixed: {changed}")
