# Mobile render spot-check (2026-04-25)

Base URL: `http://127.0.0.1:4173`  
Viewports: `narrow 360x800`, `iphone 390x844`  
Pages checked: 8

## Summary

- Checked 16 page/viewport combinations.
- Actionable overflow / clipped-element candidates: 0.
- CSS transforms and animations are neutralised during measurement so intentional entrance animations are not counted as layout defects.
- Contained code/table overflow means content is inside a scrollable/clipped block, not leaking into the page layout.
- Screenshots saved under `.claude/responsive-checks/screenshots/2026-04-25/`.

## Results

| Viewport | Page | scrollWidth | Offenders | Contained code/table overflow | Screenshot |
|---|---|---:|---:|---:|---|
| narrow | Home | 360 | 0 | 0 | `.claude/responsive-checks/screenshots/2026-04-25/narrow-home.png` |
| narrow | Tutorial grid | 360 | 0 | 0 | `.claude/responsive-checks/screenshots/2026-04-25/narrow-tutorial-grid.png` |
| narrow | Excel hub | 360 | 0 | 0 | `.claude/responsive-checks/screenshots/2026-04-25/narrow-excel-hub.png` |
| narrow | HR tutorial | 418 | 0 | 12 | `.claude/responsive-checks/screenshots/2026-04-25/narrow-hr-tutorial.png` |
| narrow | Workbook protection tutorial | 466 | 0 | 1 | `.claude/responsive-checks/screenshots/2026-04-25/narrow-workbook-protection-tutorial.png` |
| narrow | Long Flutter tutorial | 385 | 0 | 18 | `.claude/responsive-checks/screenshots/2026-04-25/narrow-long-flutter-tutorial.png` |
| narrow | Long AI tutorial | 681 | 0 | 3 | `.claude/responsive-checks/screenshots/2026-04-25/narrow-long-ai-tutorial.png` |
| narrow | Seedance tutorial | 360 | 0 | 0 | `.claude/responsive-checks/screenshots/2026-04-25/narrow-seedance-tutorial.png` |
| iphone | Home | 390 | 0 | 0 | `.claude/responsive-checks/screenshots/2026-04-25/iphone-home.png` |
| iphone | Tutorial grid | 390 | 0 | 0 | `.claude/responsive-checks/screenshots/2026-04-25/iphone-tutorial-grid.png` |
| iphone | Excel hub | 390 | 0 | 0 | `.claude/responsive-checks/screenshots/2026-04-25/iphone-excel-hub.png` |
| iphone | HR tutorial | 418 | 0 | 12 | `.claude/responsive-checks/screenshots/2026-04-25/iphone-hr-tutorial.png` |
| iphone | Workbook protection tutorial | 465 | 0 | 1 | `.claude/responsive-checks/screenshots/2026-04-25/iphone-workbook-protection-tutorial.png` |
| iphone | Long Flutter tutorial | 390 | 0 | 18 | `.claude/responsive-checks/screenshots/2026-04-25/iphone-long-flutter-tutorial.png` |
| iphone | Long AI tutorial | 682 | 0 | 3 | `.claude/responsive-checks/screenshots/2026-04-25/iphone-long-ai-tutorial.png` |
| iphone | Seedance tutorial | 390 | 0 | 0 | `.claude/responsive-checks/screenshots/2026-04-25/iphone-seedance-tutorial.png` |
