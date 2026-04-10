const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, '..', 'public', 'blog');

const faqs = {
  "flutter-state-management": [
    { q: "Should I use Provider, Riverpod, or BLoC for Flutter state management in 2026?", a: "For new projects in 2026, Riverpod is the recommended choice. It offers compile-time safety, auto-dispose, and built-in async support. Use Provider for small apps with simple state needs and teams new to Flutter. Use BLoC for large-scale enterprise apps with 5+ developers that need enforced event-state patterns and enterprise-grade traceability." },
    { q: "Can you mix Provider, Riverpod, and BLoC in one Flutter app?", a: "Yes, many production apps mix them. A common pattern is Riverpod for dependency injection and simple state (theme, auth, feature flags) and BLoC for complex feature modules (checkout flows, real-time chat, form wizards). The key rule is to be consistent within a feature module." },
    { q: "What is the best Flutter state management solution for beginners?", a: "Provider has the lowest learning curve and is the easiest to start with. If you understand the widget tree, you understand Provider. However, if you are starting a new project and want the best long-term foundation, Riverpod is worth the slightly steeper initial learning curve because it prevents runtime errors and scales better." }
  ],
  "flutter-vs-react-native": [
    { q: "Is Flutter or React Native better in 2026?", a: "Flutter offers better performance through its Skia/Impeller rendering engine, a single codebase for mobile, web, and desktop, and strong typing with Dart. React Native leverages the JavaScript ecosystem and is better if your team already knows React. Flutter is the stronger choice for new cross-platform projects in 2026, but React Native remains viable for teams heavily invested in JavaScript." },
    { q: "Should I learn Flutter or React Native first?", a: "If you are starting fresh with no prior mobile experience, Flutter is the better choice in 2026. It has stronger tooling, faster hot reload, and a more consistent cross-platform experience. If you already know React and JavaScript well, React Native lets you leverage that knowledge immediately." },
    { q: "Which has better performance, Flutter or React Native?", a: "Flutter generally delivers better raw performance because it compiles to native machine code and renders directly via its own engine (Impeller in 2026), bypassing the platform UI components. React Native uses a bridge to communicate with native components, which can introduce overhead. For most apps, both are fast enough, but Flutter has the edge for complex animations and custom UIs." }
  ],
  "vlookup-vs-xlookup": [
    { q: "What is the difference between VLOOKUP and XLOOKUP in Excel?", a: "XLOOKUP is the modern replacement for VLOOKUP. Key differences: XLOOKUP can look in any direction (left, right, up, down), returns exact matches by default, supports multiple return values, and does not require a column index number. VLOOKUP only looks right, defaults to approximate match, and breaks if you insert columns. XLOOKUP is available in Microsoft 365 and Excel 2021+." },
    { q: "Should I use VLOOKUP or XLOOKUP in Excel?", a: "Use XLOOKUP whenever possible. It is simpler, more flexible, and less error-prone than VLOOKUP. The only reason to use VLOOKUP is if you need backward compatibility with Excel 2019 or earlier versions that do not support XLOOKUP." },
    { q: "Does XLOOKUP replace VLOOKUP?", a: "Yes, XLOOKUP is designed as a complete replacement for both VLOOKUP and HLOOKUP. It handles everything they do plus additional capabilities like reverse lookups, multiple return columns, and built-in error handling with the if_not_found parameter." }
  ],
  "chatgpt-excel-guide": [
    { q: "How do I use ChatGPT to write Excel formulas?", a: "Describe your data layout and what you want to calculate in plain English. For example: I have sales data in column A with dates and column B with amounts, write a SUMIFS formula to total sales for March 2026. ChatGPT works best when you specify the exact columns, data types, and desired output. Always review and test the generated formula before relying on it." },
    { q: "Can ChatGPT create complex Excel formulas?", a: "Yes, ChatGPT can generate complex nested formulas including XLOOKUP, INDEX-MATCH, dynamic arrays, LAMBDA functions, and multi-criteria SUMIFS. It handles nested IF statements, array formulas, and even VBA macros. However, complex formulas should always be reviewed against your actual data since ChatGPT may make assumptions about your data structure." },
    { q: "What are the best ChatGPT prompts for Excel?", a: "The best prompts include your data context. Instead of write a VLOOKUP formula, describe your exact layout: I have a product list in Sheet1 A2:C100 with columns Product ID, Name, Price. In Sheet2 I have Order ID in A2:A50 and Product ID in B2:B50. Write a formula in Sheet2 C2 to pull the Price from Sheet1 using the Product ID. Specific prompts with column references produce far better results." }
  ],
  "claude-ai-excel-formulas": [
    { q: "Can Claude AI write Excel formulas?", a: "Yes, Claude AI is excellent at writing Excel formulas. It handles everything from simple SUM and VLOOKUP to complex nested formulas, dynamic arrays, LAMBDA functions, and array-based calculations. Claude tends to provide clear explanations of how each formula works, making it particularly good for learning." },
    { q: "Is Claude better than ChatGPT for Excel formulas?", a: "Both are strong for Excel formulas. Claude tends to be more precise with complex nested logic and provides better explanations of formula behaviour. ChatGPT has an edge with Code Interpreter for actually running Excel files. For formula writing and debugging, Claude is often the better choice. For end-to-end data analysis with file uploads, ChatGPT may be more practical." }
  ],
  "gemini-ai-excel": [
    { q: "Can I use Google Gemini for Excel formulas for free?", a: "Yes, Google Gemini is free to use and can generate Excel formulas including XLOOKUP, SUMIFS, INDEX-MATCH, dynamic arrays, and more. Simply describe your data layout and what you need in plain English. Gemini is a strong free alternative to ChatGPT for Excel formula generation." },
    { q: "How does Google Gemini compare to ChatGPT for Excel?", a: "Both handle standard Excel formulas well. ChatGPT has an advantage with its Code Interpreter that can actually open and process Excel files. Gemini is free and handles formula generation, explanation, and debugging effectively. For formula writing alone, both produce comparable results. Gemini also integrates with Google Sheets natively." }
  ],
  "excel-ai-prompts": [
    { q: "What are the best AI prompts for Excel?", a: "The most effective AI prompts for Excel include your data context: column headers, sample data, and desired output. For example: My data has columns Date, Region, Product, Revenue in A1:D500. Write a formula to find the top 3 products by total revenue per region. Context-rich prompts produce accurate formulas most of the time, while vague prompts like write a sales formula often produce unusable results." },
    { q: "How should I prompt ChatGPT or Claude for Excel formulas?", a: "Follow this structure: 1) Describe your data layout with column letters and headers, 2) Specify the cell where the formula should go, 3) Explain the expected output clearly, 4) Mention any constraints like avoiding VBA or needing backward compatibility. Specific prompts with column references produce far better results than generic requests." },
    { q: "Can AI write VLOOKUP and XLOOKUP formulas for me?", a: "Yes, all major AI tools including ChatGPT, Claude, Gemini, and Copilot can write VLOOKUP and XLOOKUP formulas accurately. They can also suggest which lookup function is best for your use case, convert VLOOKUP formulas to XLOOKUP, and handle complex multi-criteria lookups. Always test the formula with your actual data before applying it widely." }
  ],
  "chatgpt-vs-claude-vs-copilot-vs-gemini-excel": [
    { q: "Which AI is best for Excel in 2026?", a: "It depends on the task. Microsoft Copilot is best for in-app Excel automation since it works directly inside Excel. ChatGPT is best for end-to-end analysis with file uploads via Code Interpreter. Claude is best for complex formula logic, debugging, and clear explanations. Google Gemini is the best free option for formula generation. For most users, ChatGPT or Claude for formula writing plus Copilot for in-app tasks is the strongest combination." },
    { q: "Is ChatGPT or Claude better for Excel formulas?", a: "Both are excellent. Claude tends to be more precise with deeply nested formulas and provides clearer step-by-step explanations. ChatGPT has the advantage of Code Interpreter, which can open .xlsx files and run formulas directly. For pure formula writing and review, Claude has a slight edge. For file-based analysis, ChatGPT is more practical." },
    { q: "Should I use Microsoft Copilot or ChatGPT for Excel?", a: "Use both for different tasks. Microsoft Copilot works inside Excel and can directly add formula columns, create charts, format data, and analyse tables in your workbook. ChatGPT works outside Excel but can process uploaded files, write complex formulas, generate VBA macros, and provide detailed explanations. Copilot is better for quick in-app tasks. ChatGPT is better for complex formula writing and learning." }
  ],
  "flutter-app-architecture-2026": [
    { q: "What is the best Flutter app architecture in 2026?", a: "The recommended Flutter app architecture in 2026 is a feature-first structure with clean separation of concerns. Each feature gets its own folder containing data (repositories, API clients), domain (models, entities), and presentation (screens, widgets, state management) layers. This scales cleanly from small apps to large codebases and works with both Riverpod and BLoC." },
    { q: "Should I use feature-first or layer-first architecture in Flutter?", a: "Feature-first is recommended for most Flutter apps in 2026. In feature-first architecture, code is organised by feature (auth, cart, products) with each feature containing its own data, domain, and presentation layers. Layer-first (all repositories in one folder, all screens in another) becomes hard to maintain as apps grow. Feature-first keeps related code together and makes features independently testable and maintainable." }
  ],
  "index-match-guide": [
    { q: "How do I use INDEX MATCH in Excel with multiple criteria?", a: "For multiple criteria, use an array-based INDEX-MATCH formula: =INDEX(return_range, MATCH(1, (criteria1_range=criteria1)*(criteria2_range=criteria2), 0)). Press Ctrl+Shift+Enter in older Excel versions to make it an array formula. In Microsoft 365, it works as a regular formula with dynamic arrays. This approach is more flexible than VLOOKUP because it supports multiple conditions and can look in any direction." },
    { q: "Is INDEX MATCH better than VLOOKUP in Excel?", a: "INDEX-MATCH is more flexible than VLOOKUP because it can look left, handle column insertions without breaking, and supports multiple criteria. However, XLOOKUP has largely replaced both for new formulas in Microsoft 365. If you are on Microsoft 365 or Excel 2021+, use XLOOKUP. If you need backward compatibility with older Excel versions, INDEX-MATCH is the superior alternative to VLOOKUP." }
  ],
  "mastering-pivot-tables": [
    { q: "How do I create a pivot table in Excel?", a: "Select your data range ensuring it has headers, go to Insert then PivotTable, choose where to place it, then drag fields into the Rows, Columns, Values, and Filters areas. The key to good pivot tables: use Excel Tables as your source so new data is automatically included, keep your source data clean with no blank rows or merged cells, and use one row per record." },
    { q: "When should I use a pivot table instead of formulas in Excel?", a: "Use pivot tables when you need to quickly summarise, group, or cross-tabulate large datasets without writing formulas. Pivot tables are best for exploratory analysis when you want to slice data by different dimensions interactively. Use formulas like SUMIFS, GROUPBY, and PIVOTBY when you need the output to be formula-driven, auto-updating, and part of a structured report or dashboard." }
  ],
  "dynamic-dashboards": [
    { q: "How do I build an interactive dashboard in Excel without VBA?", a: "Use a combination of Excel Tables, pivot tables or dynamic array formulas like FILTER, SORT, and GROUPBY, data validation dropdowns for interactivity, and charts linked to the filtered data. Slicers connected to pivot tables provide point-and-click filtering. Use named ranges or structured table references so everything updates automatically when new data is added." },
    { q: "Can I create a professional dashboard in Excel without coding?", a: "Yes. Excel built-in features including pivot tables, slicers, charts, conditional formatting, data validation dropdowns, and sparklines are enough to build professional, interactive dashboards without any VBA or coding. The key is clean data structure, consistent formatting, and linking charts to filtered or summarised data ranges." }
  ],
  "excel-vs-google-sheets": [
    { q: "Is Excel or Google Sheets better in 2026?", a: "Excel is better for power users who need advanced formulas like LAMBDA, GROUPBY, and PIVOTBY, Power Query, Power Pivot, VBA macros, large datasets with over one million rows, and desktop performance. Google Sheets is better for real-time collaboration, simplicity, free access, and web-native workflows. For professional data analysis and financial modelling, Excel is the stronger choice. For team collaboration on simpler spreadsheets, Google Sheets wins." },
    { q: "Should I use Excel or Google Sheets for work?", a: "If your work involves complex data analysis, financial models, large datasets, or automation with macros, use Excel. If your work is primarily collaborative like shared trackers, simple reports, and team templates, and your organisation uses Google Workspace, use Google Sheets. Many professionals use both: Google Sheets for shared lightweight work and Excel for heavy analysis." }
  ],
  "agent-mode-in-excel": [
    { q: "What is Agent Mode in Excel?", a: "Agent Mode is an advanced AI capability in Microsoft Excel that allows Copilot to perform multi-step, autonomous actions on your workbook. Unlike basic Copilot Chat which answers questions, Agent Mode can chain together multiple operations like cleaning data, applying formulas, creating charts, and formatting in a single supervised workflow. It requires Microsoft 365 Copilot licensing." },
    { q: "How is Agent Mode different from Copilot in Excel?", a: "Standard Copilot in Excel handles single-step tasks: write one formula, create one chart, answer one question. Agent Mode handles multi-step workflows autonomously: it can analyse your data, identify issues, clean it, add calculated columns, and build a summary, all from a single prompt. Agent Mode operates with supervision, showing each proposed action for your approval before executing." },
    { q: "What can Agent Mode do in Excel that Copilot cannot?", a: "Agent Mode can chain multiple operations together autonomously. For example, it can clean messy data, standardise formats, add formula columns, create pivot summaries, and build charts all in one workflow. Regular Copilot handles these as separate, individual requests. Agent Mode also has better contextual understanding of multi-sheet workbooks and can reason across related data." }
  ],
  "flutter-renderflex-overflow-row-listview": [
    { q: "How do I fix RenderFlex overflowed in Flutter?", a: "The most common fix is to wrap the overflowing child inside a Flexible or Expanded widget, which tells Flutter to constrain the child to the available space. If the overflow happens in a Row inside a ListView, wrap the Row text or wide children with Flexible and set overflow to TextOverflow.ellipsis on the Text widget. Other fixes include using Wrap instead of Row, adding SingleChildScrollView, or constraining with SizedBox." },
    { q: "Why does my Flutter Row overflow inside a ListView?", a: "A Row inside a ListView has unbounded width from the Row children but constrained width from the ListView. If the Row children, especially Text widgets, try to take more horizontal space than available, Flutter cannot lay them out and throws a RenderFlex overflow error. The fix is to wrap wide children with Flexible or Expanded to make them respect the available width." }
  ]
};

let processed = 0;
let skipped = 0;

for (const [slug, faqList] of Object.entries(faqs)) {
  const filePath = path.join(blogDir, `${slug}.html`);

  if (!fs.existsSync(filePath)) {
    console.log(`SKIP: ${slug}.html not found`);
    skipped++;
    continue;
  }

  let content = fs.readFileSync(filePath, 'utf8');

  if (content.includes('FAQPage')) {
    console.log(`SKIP: ${slug}.html already has FAQPage schema`);
    skipped++;
    continue;
  }

  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": faqList.map(f => ({
      "@type": "Question",
      "name": f.q,
      "acceptedAnswer": {
        "@type": "Answer",
        "text": f.a
      }
    }))
  };

  const jsonBlock = JSON.stringify(faqSchema, null, 2);
  const scriptBlock = `  <script type="application/ld+json">\n${jsonBlock}\n  </script>`;

  // Find the first <style> tag and insert the FAQ schema before it
  const styleIdx = content.indexOf('    <style>');
  if (styleIdx === -1) {
    console.log(`SKIP: ${slug}.html - no <style> tag found`);
    skipped++;
    continue;
  }

  content = content.substring(0, styleIdx) + scriptBlock + '\n' + content.substring(styleIdx);

  fs.writeFileSync(filePath, content, 'utf8');
  processed++;
  console.log(`OK: ${slug}.html - added ${faqList.length} FAQs`);
}

console.log(`\nDone. Processed: ${processed}, Skipped: ${skipped}`);
