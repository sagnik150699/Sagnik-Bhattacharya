"""Generate 4 cluster hub pages for sagnikbhattacharya.com."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "blog"

HUBS = {
    "excel-ai-guide": {
        "title": "The Complete Guide to Excel with AI in 2026",
        "description": "Comprehensive guide to using ChatGPT, Claude, Microsoft Copilot, Gemini, and Gemma for Excel formulas, analysis, macros, and automation — tested on real workbooks.",
        "h1": "Excel with AI: The Complete 2026 Guide",
        "intro": [
            "This is the complete hub for using AI tools inside Excel. It covers ChatGPT, Claude, Microsoft Copilot, Google Gemini, and open-weight models like Gemma 4 — across formula writing, data analysis, macro generation, forecasting, text analysis, and industry-specific workflows. Every linked tutorial is written from hands-on testing inside real workbooks, not abstract summaries.",
            "If you are deciding which AI tool fits your Excel work, the comparison guides at the top establish a baseline. If you already know which tool you use, jump straight to its section. Each post inside the hub is standalone but designed to compose into a coherent workflow — pick the parts you need and ignore the rest.",
            "The guide is maintained by Sagnik Bhattacharya, a Udemy instructor with 30,000+ students and the founder of Coding Liquids. It is updated as new AI features land inside Excel and as the underlying models change.",
        ],
        "key_takeaways": [
            "ChatGPT, Claude, and Gemini handle general Excel formula writing well; Microsoft Copilot is the only tool with first-party access to live workbook context.",
            "For VBA macros and formula debugging, Claude currently produces the most reliable output across tested workloads.",
            "Always review AI-generated formulas against a sample of your real data before trusting them at scale — the review process is part of the workflow, not optional.",
            "Copilot's Agent Mode, Analyst Mode, and Copilot Chat solve different problems; picking the wrong mode wastes credits and produces worse results.",
            "Gemma 4 and other open-weight models are viable for local, privacy-sensitive Excel workflows and cost nothing to run.",
        ],
        "sections": [
            ("AI Tool Overviews and Comparisons", [
                ("best-ai-tools-for-excel-2026", "7 Best AI Tools for Excel in 2026 (Tested and Ranked)", "Head-to-head ranking of ChatGPT, Claude, Gemini, Copilot, and Gemma 4 on real spreadsheet tasks."),
                ("chatgpt-vs-claude-vs-copilot-vs-gemini-excel", "ChatGPT vs Claude vs Copilot vs Gemini for Excel in 2026", "Direct comparison on formulas, macros, data analysis, and error fixing."),
                ("excel-ai-prompts", "60 AI Prompts for Excel That Actually Work", "Copy-paste prompt library grouped by task type."),
                ("review-ai-generated-excel-formulas", "How to Review AI-Generated Excel Formulas Before You Trust Them", "The verification workflow that prevents silent errors in AI-generated formulas."),
            ]),
            ("ChatGPT for Excel", [
                ("chatgpt-excel-guide", "How to Use ChatGPT to Write Excel Formulas (With Real Examples)", "Prompt patterns, formula generation, and the limitations to watch for."),
            ]),
            ("Claude for Excel", [
                ("claude-ai-excel-formulas", "How to Use Claude AI to Write Excel Formulas Instantly", "Claude's Excel formula generation workflow end to end."),
                ("claude-ai-excel-macros", "How to Use Claude AI to Write Excel Macros and VBA Code", "Generating production-ready VBA without knowing VBA."),
                ("claude-debug-formulas", "How to Fix Excel Formula Errors with Claude AI (Fast)", "Debugging #REF, #VALUE, #NAME, and #SPILL errors with Claude."),
                ("claude-agent-mode-excel", "Use Claude With Agent Mode in Excel: Setup, Limits, and Best Workflows", "When Claude's agent mode outperforms direct prompting."),
            ]),
            ("Microsoft Copilot for Excel", [
                ("getting-started-copilot-excel", "How to Set Up and Use Microsoft Copilot in Excel (2026)", "First-time setup, licensing, and what to try on day one."),
                ("agent-mode-in-excel", "Agent Mode in Excel: What It Does, What It Can't, and Who Should Use It", "Honest scope assessment for Copilot Agent Mode."),
                ("analyst-vs-agent-mode-vs-copilot-chat", "Analyst vs Agent Mode vs Copilot Chat: Which Excel AI Workflow Fits Best?", "Choosing the right Copilot mode for the task."),
                ("copilot-function-excel", "COPILOT Function in Excel: Syntax, Use Cases, Limits, and Risks", "The new native COPILOT() function explained."),
                ("copilot-automate-tasks", "How to Automate Excel Tasks with Microsoft Copilot", "Task automation patterns inside Copilot."),
                ("copilot-data-analysis", "How to Use Microsoft Copilot for Data Analysis in Excel", "Building reports and insights with Copilot."),
                ("copilot-excel-python-analysis", "Copilot in Excel With Python: Forecasting, Risk Analysis, and Deeper Reasoning", "Combining Copilot with Python in Excel."),
                ("format-data-for-copilot-excel", "Format Data for Copilot in Excel: Tables, Supported Ranges, and Common Failures", "Data shapes Copilot handles well vs badly."),
                ("create-charts-with-copilot-excel", "Create Charts With Copilot in Excel: What Works, What Needs Manual Cleanup", "Copilot chart generation and its blind spots."),
                ("create-lookups-with-copilot-excel", "Create Lookups With Copilot in Excel: When It Writes XLOOKUP Well and When It Doesn't", "Copilot's lookup formula strengths and weaknesses."),
                ("generate-formula-columns-copilot-excel", "Generate Formula Columns With Copilot in Excel: Best Prompts and Review Steps", "Bulk formula generation patterns."),
                ("generate-single-cell-formulas-copilot-excel", "Generate Single-Cell Formulas With Copilot in Excel: Fast Wins and Failure Modes", "Single-cell Copilot prompts that work reliably."),
            ]),
            ("Google Gemini and Gemma for Excel", [
                ("gemini-ai-excel", "How to Use Google Gemini to Write Excel Formulas for Free", "Free Gemini workflow for spreadsheet formulas."),
                ("gemma-4-data-analysis-excel", "Gemma 4 for Data Analysis: Can It Replace ChatGPT for Spreadsheet Work?", "Open-weight Gemma 4 tested on real analysis tasks."),
                ("gemma-4-vs-gpt-vs-llama-excel", "Gemma 4 vs GPT-4o vs Llama 4: Which Free AI Model Is Best for Excel Formulas?", "Free model comparison for Excel use cases."),
            ]),
            ("Industry-Specific AI Workflows", [
                ("excel-ai-for-accountants", "Excel + AI for Accountants: Reconciliations, Variance Reviews, and Close Prep", "Accounting-specific AI workflows inside Excel."),
                ("excel-ai-for-hr-teams", "Excel + AI for HR Teams: Hiring Trackers, Attrition Analysis, and Reporting", "HR-specific AI workflows."),
                ("excel-ai-for-sales-ops", "Excel + AI for Sales Ops: Pipeline Cleanup, Forecasts, and Territory Reporting", "Sales operations AI automation."),
            ]),
            ("AI-Assisted Analysis and Automation", [
                ("ai-forecasting-model-excel", "Build a Forecasting Model in Excel With AI Assistance Step by Step", "End-to-end AI-assisted forecasting."),
                ("ai-power-query-m-code", "Use AI to Write and Fix Power Query M Code for Excel", "AI-assisted M-code generation."),
                ("text-analysis-excel-with-ai", "Text Analysis in Excel With AI: Survey Comments, Reviews, and Open Feedback", "Sentiment and theme extraction from unstructured text."),
            ]),
        ],
    },
    "excel-formulas-guide": {
        "title": "Complete Excel Formulas Guide: From VLOOKUP to LAMBDA",
        "description": "The complete Excel formulas reference — lookups, dynamic arrays, LAMBDA, Power Query, pivot tables, and advanced techniques with real examples.",
        "h1": "Excel Formulas: The Complete 2026 Reference",
        "intro": [
            "This hub covers every major Excel formula topic with step-by-step tutorials, real examples, and honest trade-offs. It spans classic lookup functions like VLOOKUP and INDEX MATCH, the modern dynamic array functions (GROUPBY, PIVOTBY, MAP, SCAN, REDUCE), LAMBDA for reusable logic, and the productivity skills around them — pivot tables, Power Query, Power Pivot, dashboards, and error debugging.",
            "Start with the lookup section if you are comparing VLOOKUP and XLOOKUP. Jump to the dynamic array section if you are on Microsoft 365 and want to replace pivot tables with formulas. Use the debugging section when formulas break in production.",
            "Every linked post is written from hands-on workshop experience — these are the same techniques taught in corporate Excel training sessions delivered to teams across India.",
        ],
        "key_takeaways": [
            "XLOOKUP replaces VLOOKUP in most cases but INDEX MATCH still wins on multi-criteria and non-standard layouts.",
            "Dynamic array functions (GROUPBY, PIVOTBY, MAP, SCAN, REDUCE) let you rebuild pivot-style reports as formulas that auto-update.",
            "LAMBDA turns repeated formula logic into named, reusable functions — the closest Excel gets to programming.",
            "Most #SPILL! errors come from obstructed ranges, not formula logic — clearing the spill range fixes them faster than rewriting the formula.",
            "Excel Tables with structured references are more maintainable than A1:Z100 ranges in every practical workbook.",
        ],
        "sections": [
            ("Lookup Functions", [
                ("vlookup-vs-xlookup", "VLOOKUP vs XLOOKUP: Differences and When to Use Each", "The definitive comparison with version requirements."),
                ("index-match-guide", "How to Use INDEX MATCH in Excel with Multiple Criteria", "Multi-criteria lookups that VLOOKUP cannot handle."),
                ("xmatch-function-excel", "XMATCH in Excel: Smarter Lookups, Reverse Searches, and Binary Search Use Cases", "XMATCH's advantages over MATCH."),
            ]),
            ("Dynamic Array Functions", [
                ("groupby-function-excel", "GROUPBY Function in Excel: Formula-Based Summaries Without a Pivot Table", "Replacing pivot tables with GROUPBY formulas."),
                ("pivotby-function-excel", "PIVOTBY Function in Excel: Build Pivot-Style Reports With a Formula", "Cross-tab reports as a single formula."),
                ("groupby-vs-pivottable-excel", "GROUPBY vs PivotTable in Excel: When Formula Summaries Beat the Ribbon", "When each approach wins."),
                ("map-scan-reduce-excel", "MAP, SCAN, and REDUCE in Excel: Modern Array Logic for Power Users", "Functional array logic in modern Excel."),
                ("choosecols-chooserows-take-drop-excel", "CHOOSECOLS, CHOOSEROWS, TAKE, and DROP in Excel: Slice Data Faster", "Data slicing with modern array functions."),
            ]),
            ("Advanced and Reusable Formulas", [
                ("let-and-lambda-excel", "LET and LAMBDA in Excel: Turn Repeated Formulas Into Reusable Logic", "LET for readability, LAMBDA for reusability."),
                ("advanced-formulas", "15 Excel Formulas That Save Hours of Manual Work (With Examples)", "The essential advanced formula library."),
                ("py-function-excel", "PY Function in Excel: What It Is, How It Works, and When to Use It", "Python formulas inside Excel cells."),
                ("python-in-excel-beginners", "Python in Excel for Beginners: The First 10 Things Worth Learning", "Python in Excel starting point."),
            ]),
            ("Pivot Tables and Data Analysis", [
                ("mastering-pivot-tables", "How to Create a Pivot Table in Excel Step by Step", "Pivot tables from scratch to advanced."),
                ("power-query-guide", "How to Use Power Query in Excel to Automate Data Cleaning", "Data transformation without formulas."),
                ("power-pivot-guide", "How to Use Power Pivot in Excel to Analyse Millions of Rows", "Large-scale data analysis in Excel."),
                ("dynamic-dashboards", "How to Build an Interactive Dashboard in Excel (No VBA)", "Dashboards with pure formulas and slicers."),
                ("charts-visualisations", "How to Make Professional Charts in Excel (Step-by-Step Guide)", "Chart selection and formatting."),
            ]),
            ("Debugging and Error Fixing", [
                ("fix-spill-errors-excel", "How to Fix #SPILL! Errors in Excel and Prevent Them in Dynamic Array Models", "Spill error causes and fixes."),
                ("audit-formulas-excel", "How to Audit Formulas in Excel: Trace Precedents, Dependents, and Error Sources", "Formula debugging and tracing."),
                ("clean-messy-data", "How to Clean Messy Data in Excel: Step-by-Step Guide", "Cleaning imported data at scale."),
            ]),
            ("Productivity and Best Practices", [
                ("excel-tables-best-practices", "Excel Tables Best Practices: Structured References, Growth, and Cleaner Models", "Why every data range should be a Table."),
                ("keyboard-shortcuts", "30 Excel Keyboard Shortcuts That Save Hours Every Week", "The shortcut set that matters."),
                ("excel-vs-google-sheets", "Excel vs Google Sheets: Which Is Better for You in 2026?", "Platform comparison for decision makers."),
            ]),
        ],
    },
    "flutter-guide": {
        "title": "Flutter Development Guide 2026: Architecture, State, Testing",
        "description": "The complete Flutter development hub — architecture, state management, performance, testing, responsive UI, and navigation with production patterns.",
        "h1": "Flutter Development: The Complete 2026 Guide",
        "intro": [
            "This hub collects the most important Flutter tutorials on the site. It covers app architecture, state management comparisons, performance optimisation, testing strategy, responsive UI, navigation with go_router, and the AI toolkit for Flutter development. Every post is written from production Flutter experience — not example-app level code.",
            "The guide is maintained by Sagnik Bhattacharya, author of 'The Complete Flutter Guide' on Udemy with 30,000+ students and a published Flutter instructor since the early days of the framework. It reflects the patterns used in real client codebases, not abstract ideals.",
            "If you are choosing a state management solution, start with the comparison post. If you are planning an app's folder structure, start with the architecture post. If you are debugging layout issues, jump to the UI section.",
        ],
        "key_takeaways": [
            "Feature-first folder structure scales better than layer-first for teams of 2+ engineers on non-trivial apps.",
            "Riverpod is the default recommendation for new Flutter apps in 2026; BLoC still wins on teams already invested in it; Provider is viable for small apps.",
            "Impeller is the rendering default for iOS and Android — performance tuning in 2026 is about rebuild reduction and DevTools profiling, not engine selection.",
            "go_router is the recommended navigation library for any app that needs deep linking, nested navigation, or web URL support.",
            "Widget tests + integration tests cover 80% of the value; golden tests are worth adding only for visual-critical components.",
        ],
        "sections": [
            ("Architecture and Patterns", [
                ("flutter-app-architecture-2026", "Flutter App Architecture in 2026: A Practical Feature-First Guide", "Production folder structure and separation patterns."),
                ("add-flutter-to-existing-app", "Add Flutter to an Existing App: Mobile and Web Integration Patterns", "Embedding Flutter into native and web apps."),
                ("create-with-ai-flutter", "Create With AI in Flutter: Gemini CLI, MCP, and the AI Toolkit Explained", "AI-assisted Flutter development stack."),
            ]),
            ("State Management", [
                ("flutter-state-management", "Flutter State Management in 2026: Provider vs Riverpod vs BLoC", "Head-to-head comparison with code samples."),
            ]),
            ("Performance and Testing", [
                ("flutter-performance-2026", "Flutter Performance in 2026: Impeller, DevTools, and Rebuild Reduction", "Profiling, Impeller, and rebuild optimisation."),
                ("flutter-testing-strategy-2026", "Flutter Testing Strategy in 2026: Unit, Widget, Integration, and Goldens", "The complete testing pyramid for Flutter."),
            ]),
            ("Web and Navigation", [
                ("flutter-web-skwasm-vs-canvaskit", "Flutter Web in 2026: skwasm vs CanvasKit vs WebAssembly Builds", "Web renderer comparison and selection."),
                ("go-router-flutter-deep-linking", "go_router in Flutter: Deep Linking, Nested Navigation, and Web URLs", "Modern Flutter routing end to end."),
            ]),
            ("UI, Forms, and Layout", [
                ("responsive-flutter-ui-all-screens", "Responsive Flutter UI for Mobile, Tablet, Desktop, and Web", "Breakpoint patterns and adaptive layouts."),
                ("flutter-form-validation-best-practices", "Flutter Form Validation Best Practices for Production Apps", "Form validation patterns that scale."),
                ("flutter-widget-previewer", "Flutter Widget Previewer: Real-Time UI Iteration Without Running the Full App", "Faster UI iteration with previewer."),
                ("flutter-renderflex-overflow-row-listview", "How to Fix RenderFlex Overflowed in Flutter Row inside ListView", "Debugging the most common Flutter layout error."),
            ]),
            ("Comparisons and Learning", [
                ("flutter-vs-react-native", "Flutter vs React Native in 2026: Which Should You Choose?", "Framework comparison for decision makers."),
                ("best-flutter-courses-2026", "Best Flutter Courses in 2026: What to Learn and Where to Start", "Course recommendations and learning roadmap."),
            ]),
        ],
    },
    "seedance-guide": {
        "title": "Complete Seedance 2.0 Guide: Prompts, Settings, Video Generation",
        "description": "The complete Seedance 2.0 hub — setup, prompts, settings, camera movement, consistent characters, use cases, and model comparisons.",
        "h1": "Seedance 2.0: The Complete Guide",
        "intro": [
            "Seedance 2.0 is one of the most capable AI video models available in 2026, and this hub collects every Seedance tutorial on the site. It covers first-time setup, pricing, core settings (resolution, motion intensity, export formats), prompt techniques, use-case-specific workflows (marketing videos, YouTube Shorts, product ads, anime, talking heads), and head-to-head comparisons against Sora 2, Kling, and Veo 3.",
            "If you are brand new to Seedance, start with the beginner tutorial and setup guide. If you are refining output quality, jump to the prompt techniques and motion intensity sections. If you are evaluating Seedance against other video models, use the comparison posts at the bottom.",
            "Every tutorial is written from hands-on testing inside the Dreamina interface — not generic AI video advice. The workflows are the ones that have produced reliable, repeatable output in real content pipelines.",
        ],
        "key_takeaways": [
            "Seedance 2.0 weights the earlier parts of a prompt more heavily — put subject, motion, and camera direction in the first 15 words.",
            "Motion intensity 40-60 produces natural movement for most scenes; under 30 reads as static, over 75 introduces warping and artefacts.",
            "For consistent characters across multiple clips, reference images beat text description alone — it is the single biggest reliability fix.",
            "Seedance outperforms Sora 2 on prompt adherence but trails on raw photorealism; it outperforms Kling on camera movement fidelity.",
            "Generate at draft resolution first, iterate the prompt, then re-render at full quality — it saves credits and time.",
        ],
        "sections": [
            ("Getting Started", [
                ("seedance-2-tutorial-beginner", "Seedance 2.0 Tutorial: The Complete Beginner's Guide", "End-to-end first-time user walkthrough."),
                ("how-to-setup-seedance", "How to Set Up Seedance 2.0: Account, Access, First Video", "Account creation, access, and first generation."),
                ("seedance-2-pricing-credits", "Seedance 2.0 Pricing, Credits, and Free Tier Explained", "Credit economics and free-tier limits."),
                ("seedance-dreamina-guide", "How to Use Seedance 2.0 in Dreamina Step by Step", "Dreamina interface walkthrough."),
            ]),
            ("Settings and Technical Controls", [
                ("seedance-2-resolution-export-settings", "Seedance 2.0 Resolution, Aspect Ratio, and Export Settings", "Resolution and export format selection."),
                ("seedance-2-motion-intensity-settings", "Seedance 2.0 Motion Intensity Settings 0–100 Explained", "Motion intensity across the full slider."),
            ]),
            ("Prompt Techniques", [
                ("better-prompts-seedance", "How to Write Better Prompts for Seedance 2.0", "Prompt structure and keyword strategies."),
                ("seedance-cinematic-camera-movement", "How to Use Seedance 2.0 for Cinematic Camera Movement Prompts", "Camera movement prompt patterns."),
                ("seedance-audio-prompts", "How to Use Seedance 2.0 With Audio Prompts Step by Step", "Audio-driven video generation."),
                ("seedance-image-to-video", "How to Use Seedance 2.0 for Image to Video Prompts", "Image-to-video workflow."),
                ("consistent-characters-seedance", "How to Use Seedance 2.0 With Reference Images for Consistent Characters", "Reference image workflow for character consistency."),
            ]),
            ("Use Cases", [
                ("seedance-marketing-videos", "How to Use Seedance 2.0 for AI Marketing Videos", "Marketing-specific video generation patterns."),
                ("seedance-youtube-shorts", "How to Use Seedance 2.0 for YouTube Shorts Creation", "Vertical short-form video workflow."),
                ("seedance-product-ad-videos", "How to Use Seedance 2.0 for Product Ad Videos", "Product advertising video patterns."),
                ("seedance-anime-video", "How to Use Seedance 2.0 for Anime Style Video Generation", "Anime aesthetic prompts and style control."),
                ("seedance-2-lip-sync-talking-head", "How to Create Lip-Sync and Talking-Head Videos in Seedance 2.0", "Lip-sync and talking-head workflow."),
            ]),
            ("Consistency and Troubleshooting", [
                ("consistent-characters-seedance", "How to Make Consistent Characters in Seedance 2.0", "Character consistency across multiple clips."),
                ("fix-bad-motion-seedance", "How to Fix Bad Motion in Seedance 2.0 Videos", "Motion artefact debugging."),
            ]),
            ("Comparisons", [
                ("seedance-vs-sora-2", "Seedance 2.0 vs Sora 2 for Prompt Control", "Prompt adherence head-to-head."),
                ("seedance-vs-kling", "Seedance 2.0 vs Kling for Realistic Motion", "Motion realism comparison."),
                ("seedance-vs-veo-3", "Seedance 2.0 vs Veo 3 for Short AI Videos", "Short-form video comparison."),
            ]),
        ],
    },
}


TEMPLATE = """<!DOCTYPE html>
<html lang="en-GB">
<head>
  <meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="google-adsense-account" content="ca-pub-1443974359047569">
  <title>{title} | Sagnik Bhattacharya</title>
  <meta name="description" content="{description}">
  <meta name="author" content="Sagnik Bhattacharya">
  <meta name="robots" content="index, follow">
  <link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
  <link rel="apple-touch-icon" sizes="180x180" href="/favicon-180x180.png">
  <link rel="canonical" href="https://sagnikbhattacharya.com/blog/{slug}">
  <link rel="manifest" href="/site.webmanifest">
  <meta name="theme-color" content="#3E2723">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{description}">
  <meta property="og:type" content="article">
  <meta property="og:url" content="https://sagnikbhattacharya.com/blog/{slug}">
  <meta property="og:image" content="https://sagnikbhattacharya.com/sagnik-bhattacharya.png">
  <meta property="og:locale" content="en_GB">
  <meta property="og:site_name" content="Sagnik Bhattacharya">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{title}">
  <meta name="twitter:description" content="{description}">
  <meta name="twitter:image" content="https://sagnikbhattacharya.com/sagnik-bhattacharya.png">
  <link rel="alternate" type="application/rss+xml" title="Sagnik Bhattacharya — Blog" href="/feed.xml">
  <script type="application/ld+json">
{collection_jsonld}
  </script>
  <script type="application/ld+json">
{breadcrumb_jsonld}
  </script>
  <script type="application/ld+json">
{speakable_jsonld}
  </script>
  <style>
    @font-face{{font-family:'DM Serif Display';font-style:normal;font-weight:400;font-display:swap;src:url('/fonts/dm-serif-display-normal-latin.woff2') format('woff2')}}
    @font-face{{font-family:'Plus Jakarta Sans';font-style:normal;font-weight:400 700;font-display:swap;src:url('/fonts/plus-jakarta-sans-latin.woff2') format('woff2')}}
    :root{{--warm-500:#E8852E;--warm-700:#8B4513;--earth-800:#3E2723;--cream:#FDF8F0;--text-primary:#2C1810;--text-secondary:#6B5344;--text-light:#9A8578}}
    *{{margin:0;padding:0;box-sizing:border-box}}html{{scroll-behavior:smooth;scroll-padding-top:80px}}body{{font-family:'Plus Jakarta Sans',sans-serif;color:var(--text-primary);background:var(--cream);line-height:1.7;-webkit-font-smoothing:antialiased;overflow-x:hidden}}h1,h2,h3{{font-family:'DM Serif Display',serif;line-height:1.2;font-weight:400;color:var(--earth-800)}}a{{color:var(--warm-700);text-decoration:none}}a:hover{{text-decoration:underline}}.container{{max-width:960px;margin:0 auto;padding:0 24px}}
    nav{{position:fixed;top:0;left:0;right:0;z-index:100;background:rgba(253,248,240,0.85);backdrop-filter:blur(20px);border-bottom:1px solid rgba(44,24,16,0.06)}}nav .container{{display:flex;align-items:center;justify-content:space-between;height:72px}}.nav-logo{{font-family:'DM Serif Display',serif;font-size:1.35rem;color:var(--earth-800)}}.nav-logo span{{color:var(--warm-500)}}.nav-links{{display:flex;gap:32px;list-style:none}}.nav-links a{{font-size:.9rem;font-weight:500;color:var(--text-secondary)}}.nav-cta{{background:var(--earth-800)!important;color:#FFF3E0!important;padding:10px 22px;border-radius:50px;font-size:.85rem!important;font-weight:600!important}}
    .hub-hero{{padding:140px 0 40px}}.hub-hero h1{{font-size:2.8rem;letter-spacing:-.5px;margin-bottom:16px}}.hub-hero .lead{{font-size:1.15rem;color:var(--text-secondary);max-width:720px}}.hub-breadcrumb{{font-size:.88rem;color:var(--text-light);margin-bottom:24px}}.hub-intro{{padding:10px 0 30px}}.hub-intro p{{font-size:1.05rem;margin-bottom:18px;color:var(--text-primary)}}.hub-takeaways{{background:#fff;border:1px solid rgba(44,24,16,0.08);border-radius:16px;padding:28px 32px;margin:30px 0;box-shadow:0 4px 16px rgba(44,24,16,0.04)}}.hub-takeaways h2{{font-size:1.4rem;margin-bottom:14px}}.hub-takeaways ul{{padding-left:20px}}.hub-takeaways li{{margin-bottom:10px;line-height:1.6}}.hub-section{{margin:40px 0 10px}}.hub-section h2{{font-size:1.7rem;margin-bottom:18px;border-bottom:2px solid var(--warm-500);padding-bottom:8px;display:inline-block}}.hub-post-list{{list-style:none;padding:0}}.hub-post-list li{{padding:14px 0;border-bottom:1px solid rgba(44,24,16,0.08)}}.hub-post-list a{{font-weight:600;font-size:1.05rem;color:var(--earth-800)}}.hub-post-list p{{margin-top:4px;color:var(--text-secondary);font-size:.95rem}}
    footer{{padding:50px 0 30px;color:var(--text-light);font-size:.9rem;text-align:center;border-top:1px solid rgba(44,24,16,0.08);margin-top:80px}}
    @media(max-width:768px){{.nav-links{{display:none}}.hub-hero{{padding:110px 0 30px}}.hub-hero h1{{font-size:2rem}}}}
  </style>
  <link rel="stylesheet" href="/style.css" media="print" onload="this.media='all'">
  <noscript><link rel="stylesheet" href="/style.css"></noscript>
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-G88BTBD73Q"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag("js",new Date());gtag("config","G-G88BTBD73Q");</script>
</head>
<body>
  <nav id="navbar"><div class="container"><a href="/" class="nav-logo">sagnik<span>.</span></a><ul class="nav-links"><li><a href="/about">About</a></li><li><a href="/courses">Courses</a></li><li><a href="/services">Services</a></li><li><a href="/blog">Blog</a></li><li><a href="/contact" class="nav-cta">Get in Touch</a></li></ul></div></nav>
  <main>
    <section class="hub-hero">
      <div class="container">
        <nav class="hub-breadcrumb" aria-label="Breadcrumb"><a href="/">Home</a> / <a href="/blog">Blog</a> / <span>{h1}</span></nav>
        <h1>{h1}</h1>
        <p class="lead">{description}</p>
      </div>
    </section>
    <section class="hub-intro">
      <div class="container">
        <article>
          {intro_html}
          <div class="hub-takeaways" id="key-takeaways">
            <h2>Key takeaways</h2>
            <ul>
              {takeaways_html}
            </ul>
          </div>
          {sections_html}
        </article>
      </div>
    </section>
  </main>
  <footer><div class="container"><p>&copy; 2026 Sagnik Bhattacharya &middot; Built with &#9749; in Kolkata &middot; <a href="https://codingliquids.com" target="_blank" rel="noopener">Coding Liquids</a></p></div></footer>
</body>
</html>
"""


def render(slug, hub):
    intro_html = "\n          ".join(f"<p>{p}</p>" for p in hub["intro"])
    takeaways_html = "\n              ".join(f"<li>{t}</li>" for t in hub["key_takeaways"])
    sections_html_parts = []
    item_position = 0
    list_items = []
    for section_title, posts in hub["sections"]:
        s = [f'<section class="hub-section"><h2>{section_title}</h2><ul class="hub-post-list">']
        for post_slug, post_title, post_desc in posts:
            item_position += 1
            s.append(
                f'<li><a href="/blog/{post_slug}">{post_title}</a><p>{post_desc}</p></li>'
            )
            list_items.append({
                "@type": "ListItem",
                "position": item_position,
                "url": f"https://sagnikbhattacharya.com/blog/{post_slug}",
                "name": post_title,
            })
        s.append("</ul></section>")
        sections_html_parts.append("".join(s))
    sections_html = "\n          ".join(sections_html_parts)

    collection = {
        "@context": "https://schema.org",
        "@type": "CollectionPage",
        "name": hub["title"],
        "description": hub["description"],
        "url": f"https://sagnikbhattacharya.com/blog/{slug}",
        "inLanguage": "en-GB",
        "author": {"@type": "Person", "name": "Sagnik Bhattacharya", "url": "https://sagnikbhattacharya.com"},
        "publisher": {"@type": "Organization", "name": "Coding Liquids", "url": "https://codingliquids.com"},
        "mainEntity": {"@type": "ItemList", "itemListElement": list_items},
    }
    breadcrumb = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": [
            {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://sagnikbhattacharya.com/"},
            {"@type": "ListItem", "position": 2, "name": "Blog", "item": "https://sagnikbhattacharya.com/blog"},
            {"@type": "ListItem", "position": 3, "name": hub["h1"], "item": f"https://sagnikbhattacharya.com/blog/{slug}"},
        ],
    }
    speakable = {
        "@context": "https://schema.org",
        "@type": "WebPage",
        "url": f"https://sagnikbhattacharya.com/blog/{slug}",
        "speakable": {
            "@type": "SpeakableSpecification",
            "cssSelector": ["#key-takeaways", ".hub-hero h1", ".hub-hero .lead"],
        },
    }

    return TEMPLATE.format(
        title=hub["title"],
        description=hub["description"],
        slug=slug,
        h1=hub["h1"],
        intro_html=intro_html,
        takeaways_html=takeaways_html,
        sections_html=sections_html,
        collection_jsonld=json.dumps(collection, indent=2),
        breadcrumb_jsonld=json.dumps(breadcrumb, indent=2),
        speakable_jsonld=json.dumps(speakable, indent=2),
    )


def main():
    for slug, hub in HUBS.items():
        html = render(slug, hub)
        path = OUT / f"{slug}.html"
        path.write_text(html, encoding="utf-8")
        print(f"Wrote {path} ({len(html)} bytes)")


if __name__ == "__main__":
    main()
