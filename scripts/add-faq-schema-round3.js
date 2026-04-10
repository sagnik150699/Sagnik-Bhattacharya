const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, '..', 'public', 'blog');

const faqs = {
  "advanced-formulas": [
    { q: "What are the most useful Excel formulas to learn?", a: "The most impactful Excel formulas to learn are XLOOKUP for data retrieval, SUMIFS for conditional totalling, IF with nested logic for decision-making, INDEX-MATCH for flexible lookups, COUNTIFS for conditional counting, TEXT for formatting, and dynamic array functions like FILTER, SORT, UNIQUE, and SEQUENCE. These 15 formulas cover the vast majority of real-world Excel work." },
    { q: "What Excel formulas save the most time?", a: "XLOOKUP saves the most time for anyone doing data lookups. SUMIFS and COUNTIFS eliminate manual filtering and counting. FILTER and SORT automate report generation that used to require pivot tables. TEXT and CONCAT save hours of manual formatting. Learning these formulas well can reduce repetitive spreadsheet work by 50% or more." }
  ],
  "groupby-function-excel": [
    { q: "What is the GROUPBY function in Excel?", a: "GROUPBY is a dynamic array function in Excel that groups data by one or more columns and applies an aggregation function like SUM, AVERAGE, or COUNT. It creates summary tables directly from raw data using a formula, without needing a pivot table. The syntax is GROUPBY(row_fields, values, function). It is available in Microsoft 365." },
    { q: "Is GROUPBY better than a pivot table?", a: "GROUPBY is better when you need formula-driven summaries that update automatically, live inside your worksheet, and can be referenced by other formulas. Pivot tables are better for interactive exploration with slicers, drill-down, and quick layout changes. Use GROUPBY for automated reports and dashboards. Use pivot tables for ad-hoc analysis." }
  ],
  "groupby-vs-pivottable-excel": [
    { q: "When should I use GROUPBY instead of a PivotTable in Excel?", a: "Use GROUPBY when you need a formula-based summary that auto-updates, integrates with other formulas, and stays in your worksheet layout. Use PivotTable when you need interactive slicers, drill-down, calculated fields, or are exploring data without a fixed layout. GROUPBY is better for automated reports. PivotTable is better for exploratory analysis." },
    { q: "Can GROUPBY replace PivotTables?", a: "For simple summaries, yes. GROUPBY can group, aggregate, and sort data entirely with formulas. However, PivotTables offer features GROUPBY cannot match: slicers for interactive filtering, calculated fields, timeline filters, drill-down, and percentage-of-total calculations. For most users, both tools complement each other rather than one replacing the other." }
  ],
  "pivotby-function-excel": [
    { q: "What is the PIVOTBY function in Excel?", a: "PIVOTBY is a dynamic array function that creates pivot-style cross-tabulation reports using a formula. Unlike GROUPBY which only groups by rows, PIVOTBY groups by both rows and columns, producing a matrix layout similar to a pivot table. The syntax is PIVOTBY(row_fields, col_fields, values, function). It is available in Microsoft 365." },
    { q: "How is PIVOTBY different from GROUPBY?", a: "GROUPBY produces a one-dimensional grouped summary with rows only. PIVOTBY produces a two-dimensional cross-tabulation with both row and column groupings, like a traditional pivot table layout. Use GROUPBY for simple aggregations by category. Use PIVOTBY when you need to see values broken down by two dimensions simultaneously." }
  ],
  "let-and-lambda-excel": [
    { q: "What is LAMBDA in Excel?", a: "LAMBDA lets you create custom reusable functions in Excel without VBA. You define parameters and a formula, then name it in the Name Manager. Once created, you can use your custom function like any built-in function. For example, you could create a TAX function that applies your company's tax rate calculation, then use =TAX(amount) in any cell." },
    { q: "What is the LET function in Excel?", a: "LET allows you to define named variables inside a formula to avoid repeating calculations. Instead of writing the same sub-expression multiple times, you assign it a name with LET and reference that name. This makes complex formulas shorter, faster to calculate, and much easier to read and debug." }
  ],
  "map-scan-reduce-excel": [
    { q: "What are MAP, SCAN, and REDUCE in Excel?", a: "MAP applies a LAMBDA function to each element in an array and returns the results. SCAN applies a LAMBDA cumulatively across an array, returning a running result at each step. REDUCE applies a LAMBDA cumulatively and returns a single final value. Together they bring functional programming patterns to Excel formulas, enabling complex array transformations without VBA." },
    { q: "When should I use MAP instead of regular formulas in Excel?", a: "Use MAP when you need to apply a custom transformation to every element in an array that cannot be done with simple arithmetic. For example, applying conditional logic, text manipulation, or multi-step calculations to each row. MAP is cleaner than nested IF statements and more flexible than helper columns for array-based transformations." }
  ],
  "choosecols-chooserows-take-drop-excel": [
    { q: "What do CHOOSECOLS, CHOOSEROWS, TAKE, and DROP do in Excel?", a: "CHOOSECOLS extracts specific columns from a range by column number. CHOOSEROWS extracts specific rows. TAKE returns the first or last N rows or columns from a range. DROP removes the first or last N rows or columns. Together they let you slice and reshape data arrays with formulas, eliminating the need for helper columns or complex INDEX formulas." },
    { q: "How do I extract specific columns from a table in Excel?", a: "Use CHOOSECOLS(table, col1, col2, ...) to extract specific columns by their position numbers. For example, CHOOSECOLS(A1:E100, 1, 3, 5) returns only the first, third, and fifth columns. You can also use negative numbers to count from the right. This is much simpler than the old INDEX-based methods for column extraction." }
  ],
  "xmatch-function-excel": [
    { q: "What is XMATCH in Excel?", a: "XMATCH is the modern replacement for MATCH. It returns the position of a value in a range, with support for exact match, wildcard match, and binary search. Unlike MATCH, XMATCH can search from bottom to top (reverse search), does not require sorted data for approximate matches, and supports wildcard characters by default." },
    { q: "When should I use XMATCH instead of MATCH?", a: "Use XMATCH whenever possible since it is more capable and less error-prone. XMATCH defaults to exact match (MATCH defaults to approximate), supports reverse search to find the last occurrence, and has cleaner syntax. The only reason to use MATCH is backward compatibility with Excel versions before Microsoft 365." }
  ],
  "fix-spill-errors-excel": [
    { q: "How do I fix a #SPILL error in Excel?", a: "The #SPILL error occurs when a dynamic array formula cannot expand because cells in the spill range are not empty. To fix it: clear all cells in the range where the formula needs to spill, check for merged cells in the spill area and unmerge them, remove any hidden characters or spaces in seemingly empty cells, and ensure no other formulas or data occupy the spill range." },
    { q: "What causes #SPILL errors in Excel?", a: "The main causes are: non-empty cells in the spill range blocking the output, merged cells in the spill area, the spill range extending beyond the worksheet edge, another spilling formula conflicting with the range, or hidden characters like spaces in cells that appear empty. Use Find and Replace to search for spaces in the spill area if cells look empty but still cause errors." }
  ],
  "claude-debug-formulas": [
    { q: "Can Claude AI fix broken Excel formulas?", a: "Yes, Claude is excellent at debugging Excel formulas. Paste the broken formula along with a description of your data layout and the error you see. Claude can diagnose issues like circular references, incorrect range references, mismatched parentheses, wrong XLOOKUP arguments, and logic errors in nested IF statements. It also explains why the error occurs and how to prevent it." },
    { q: "How do I use Claude to debug Excel errors?", a: "Provide Claude with three things: the formula that is not working, the error message or unexpected result you see, and a description of your data layout including column headers and sample values. Claude will analyse the formula, identify the error, provide a corrected version, and explain what went wrong. This works for all common Excel errors including #VALUE, #REF, #N/A, #SPILL, and logic errors." }
  ],
  "claude-ai-excel-macros": [
    { q: "Can Claude write VBA macros for Excel?", a: "Yes, Claude can generate VBA macros for Excel including data processing routines, formatting automation, report generation, file operations, and user form creation. Describe what you want the macro to do in plain English and Claude will produce clean, commented VBA code that you can paste directly into the VBA editor. It handles both simple and complex automation tasks." },
    { q: "How do I use Claude to automate Excel with VBA?", a: "Describe your automation task to Claude in detail: what data do you have, what processing steps are needed, and what the output should look like. Claude will generate a complete VBA Sub or Function with error handling and comments. Copy the code into the VBA editor in Excel (Alt+F11), paste it into a module, and run it. Always review the code before running it on important data." }
  ],
  "claude-agent-mode-excel": [
    { q: "What is Claude Agent Mode for Excel?", a: "Claude's agent mode allows it to perform multi-step Excel tasks autonomously. Instead of answering one question at a time, Claude can plan a complete workflow: analyse your data structure, write formulas, debug issues, and suggest next steps, all in a single conversation turn. It is particularly effective for complex data transformation tasks that require multiple coordinated actions." },
    { q: "How is Claude Agent Mode different from regular Claude for Excel?", a: "Regular Claude responds to individual prompts one at a time. Agent Mode plans and executes multi-step workflows: it can analyse your data, write a formula, check if it gives expected results, revise if needed, and then move to the next task. This is more efficient for complex Excel work that involves multiple related steps." }
  ],
  "copilot-automate-tasks": [
    { q: "How do I automate Excel tasks with Copilot?", a: "Type your request in the Copilot panel inside Excel. You can ask Copilot to add formula columns, sort and filter data, create summary tables, format cells, generate charts, and highlight data patterns. Copilot reads your table structure and applies changes directly to your workbook. Start with clear, specific requests like 'Add a column that calculates the year-over-year growth rate'." },
    { q: "What can Microsoft Copilot automate in Excel?", a: "Copilot can automate: adding calculated formula columns, creating charts and pivot tables, formatting and conditional formatting, sorting and filtering data, generating summaries and insights, creating data validation rules, and answering questions about your data. It works best with data formatted as Excel Tables and handles most common spreadsheet automation tasks." }
  ],
  "copilot-data-analysis": [
    { q: "Can Copilot analyse data in Excel?", a: "Yes, Copilot can analyse data directly in Excel. Ask questions like 'What are the top 5 products by revenue' or 'Show me the trend in monthly sales'. Copilot reads your table, performs the analysis, and presents results as text summaries, charts, or new calculated columns. It is particularly effective for quick insights without writing formulas." },
    { q: "How do I use Copilot for data analysis in Excel?", a: "Format your data as an Excel Table, open the Copilot panel, and ask questions in natural language. Effective prompts include: 'What are the key trends in this data', 'Which category has the highest growth rate', 'Create a chart showing monthly revenue by region', or 'Highlight outliers in the sales column'. Copilot works best with clean, well-structured data." }
  ],
  "copilot-excel-python-analysis": [
    { q: "Can Copilot write Python code in Excel?", a: "Yes, when Python in Excel is enabled, Copilot can generate Python code that runs directly in your workbook cells using the PY function. This enables advanced analysis like statistical modelling, forecasting, clustering, and complex visualisations using Python libraries, all triggered through natural language prompts to Copilot." },
    { q: "What can Python in Excel with Copilot do that formulas cannot?", a: "Python in Excel with Copilot enables: machine learning predictions, time series forecasting, advanced statistical tests, complex data visualisations with matplotlib and seaborn, web API data integration, text analysis with NLP libraries, and Monte Carlo simulations. These tasks are either impossible or extremely difficult with Excel formulas alone." }
  ],
  "copilot-function-excel": [
    { q: "What is the COPILOT function in Excel?", a: "The COPILOT function is a cell formula that calls AI directly. You write =COPILOT('summarise this text') or reference a cell range, and AI-generated results appear in the cell. It is useful for text tasks like categorisation, summarisation, sentiment analysis, and entity extraction. Results are dynamic and update when source data changes." },
    { q: "Is the COPILOT function reliable for calculations?", a: "The COPILOT function is not designed for precise numerical calculations. Use traditional formulas like SUM, AVERAGE, and XLOOKUP for numbers. The COPILOT function excels at text processing tasks: categorising feedback, summarising paragraphs, extracting names or dates from unstructured text, and generating descriptions. For numerical work, stick to standard Excel formulas." }
  ],
  "create-charts-with-copilot-excel": [
    { q: "Can Copilot create charts in Excel?", a: "Yes, Copilot can create charts directly in your workbook. Ask something like 'Create a bar chart showing sales by region' or 'Make a line chart of monthly revenue trends'. Copilot selects appropriate chart types, sets up axes, and adds titles. However, the charts often need manual cleanup for formatting, colours, and labels to match professional standards." },
    { q: "How good are Copilot-generated charts in Excel?", a: "Copilot-generated charts are a solid starting point but rarely production-ready. It correctly identifies appropriate chart types and data ranges about 80% of the time. The main issues are: default formatting that needs polish, occasional wrong axis selections, and missing labels. Plan to spend a few minutes cleaning up Copilot charts before using them in presentations." }
  ],
  "create-lookups-with-copilot-excel": [
    { q: "Can Copilot write XLOOKUP formulas in Excel?", a: "Yes, Copilot can generate XLOOKUP, VLOOKUP, and INDEX-MATCH formulas. Ask something like 'Look up the price for each product ID from the Products table'. Copilot reads your table headers and generates the appropriate lookup formula. It handles simple lookups well but sometimes makes errors on multi-criteria lookups or nested formulas that need manual review." },
    { q: "How accurate are Copilot lookup formulas?", a: "For simple single-criteria lookups, Copilot is about 85% accurate. For multi-criteria lookups or nested formulas, accuracy drops to around 60-70%. Common issues include referencing wrong columns, using approximate match when exact is needed, or creating formulas that work for the first row but break when copied down. Always test Copilot formulas on a few rows before applying broadly." }
  ],
  "format-data-for-copilot-excel": [
    { q: "How do I format data for Copilot in Excel?", a: "Copilot works best with data formatted as Excel Tables (Ctrl+T). Ensure your data has clear header row labels, no merged cells, no blank rows within the data, consistent data types per column, and no mixed content in cells. Avoid multi-level headers or complex nested layouts. The cleaner and simpler your data structure, the better Copilot performs." },
    { q: "Why is Copilot not working on my Excel data?", a: "The most common reasons: your data is not formatted as an Excel Table, there are merged cells in the range, blank rows split the data into multiple regions, headers are missing or span multiple rows, or the data contains mixed types in a single column. Convert your data to an Excel Table (Ctrl+T) and clean up any structural issues first." }
  ],
  "generate-formula-columns-copilot-excel": [
    { q: "How do I use Copilot to add formula columns in Excel?", a: "Select your data table, open Copilot, and describe the calculation you need. For example: 'Add a column that calculates profit margin as (Revenue - Cost) / Revenue'. Copilot generates the formula and fills the entire column. It works well for straightforward calculations. For complex formulas, describe the logic step by step for better results." },
    { q: "What are the best prompts for Copilot formula columns?", a: "Be specific about inputs and outputs. Good prompt: 'Add a column called Status that shows Late if the Due Date is before today and the Complete column is No, otherwise shows On Track'. Bad prompt: 'Add a status column'. Include column names as they appear in your headers, specify conditions clearly, and describe the expected output format." }
  ],
  "generate-single-cell-formulas-copilot-excel": [
    { q: "Can Copilot write formulas for a single cell in Excel?", a: "Yes, use Copilot to generate single-cell formulas like SUMIFS, COUNTIFS, AVERAGEIFS, and other aggregation formulas. Describe what you want: 'Calculate the total revenue for the North region in Q1'. Copilot generates the formula and places it in a cell. This is faster than writing complex formulas manually, especially for multi-criteria aggregations." },
    { q: "How reliable are Copilot single-cell formulas?", a: "For simple aggregations like SUM, AVERAGE, and COUNT with one or two criteria, Copilot is very reliable. For complex formulas with multiple criteria, nested logic, or array operations, reliability drops. Common failures include referencing wrong ranges, using incorrect criteria logic, or producing formulas that work on sample data but fail on edge cases. Always verify the result against a manual check." }
  ],
  "getting-started-copilot-excel": [
    { q: "How do I set up Copilot in Excel?", a: "Copilot requires a Microsoft 365 subscription with Copilot add-on. Once licensed, Copilot appears in the ribbon. Format your data as an Excel Table (Ctrl+T), click the Copilot button, and start typing requests. Copilot reads your table structure and can add formulas, create charts, analyse data, and format your workbook." },
    { q: "Do I need a special subscription for Copilot in Excel?", a: "Yes, Copilot in Excel requires a Microsoft 365 Copilot subscription, which is an add-on to your existing Microsoft 365 plan. The base Microsoft 365 subscription alone does not include Copilot. Check with your IT administrator or Microsoft account to add the Copilot license." }
  ],
  "analyst-vs-agent-mode-vs-copilot-chat": [
    { q: "What is the difference between Analyst Mode, Agent Mode, and Copilot Chat in Excel?", a: "Copilot Chat answers individual questions and performs single tasks. Analyst Mode provides deeper data analysis with statistical insights and trend identification. Agent Mode chains multiple operations together autonomously to complete complex multi-step workflows. Chat is for quick tasks, Analyst is for understanding data, and Agent is for automating multi-step processes." },
    { q: "Which Excel AI workflow should I use?", a: "Use Copilot Chat for quick one-off tasks like adding a formula or creating a chart. Use Analyst Mode when you want to explore and understand your data with deeper statistical analysis. Use Agent Mode when you have a complex task that requires multiple steps like cleaning data, adding calculations, and building a summary report. Most users start with Chat and graduate to Agent Mode as they get comfortable." }
  ],
  "excel-ai-for-accountants": [
    { q: "How can accountants use AI with Excel?", a: "Accountants can use AI to automate reconciliation matching, generate variance analysis formulas, write audit trail queries, create month-end close checklists with automated status tracking, build financial statement templates with formula-driven calculations, and flag anomalies in transaction data. AI tools like ChatGPT and Claude can write complex accounting formulas in seconds." },
    { q: "Can AI help with bank reconciliation in Excel?", a: "Yes, AI can write XLOOKUP and fuzzy matching formulas to match bank statement entries against ledger records, flag unmatched items, calculate running balances, and identify duplicate entries. Describe your reconciliation layout to ChatGPT or Claude and they will generate the matching logic. AI significantly speeds up the matching process for large transaction volumes." }
  ],
  "excel-ai-for-hr-teams": [
    { q: "How can HR teams use AI with Excel?", a: "HR teams can use AI to build hiring pipeline trackers with automated stage calculations, create attrition analysis dashboards with trend formulas, generate headcount reports with dynamic filtering, automate leave balance calculations, and build compensation analysis models. AI writes the formulas and creates the template structure. HR professionals provide the business logic." },
    { q: "Can AI automate HR reporting in Excel?", a: "Yes, AI can generate formulas for turnover rate calculations, tenure analysis, department headcount summaries, diversity metrics, and compensation band analysis. Describe your HR data structure and reporting needs to ChatGPT or Claude, and they will create the formulas, conditional formatting rules, and chart recommendations for your HR dashboard." }
  ],
  "excel-ai-for-sales-ops": [
    { q: "How can sales teams use AI with Excel?", a: "Sales operations teams can use AI to build pipeline trackers with automated stage progression, create forecast models with probability-weighted calculations, generate territory reports with dynamic assignment formulas, automate commission calculations, and build win/loss analysis dashboards. AI writes the complex formulas while sales ops professionals define the business rules." },
    { q: "Can AI help with sales forecasting in Excel?", a: "Yes, AI can write forecasting formulas including weighted pipeline calculations, moving averages, trend-based projections, and scenario analysis models. Describe your sales data structure, pipeline stages, and forecasting methodology to ChatGPT or Claude. They will generate the formulas for probability-weighted forecasts, historical trend analysis, and quota attainment tracking." }
  ],
  "review-ai-generated-excel-formulas": [
    { q: "How do I check if an AI-generated Excel formula is correct?", a: "Follow these steps: 1) Read the formula and understand what each part does. 2) Test it on a few rows where you know the expected result and verify it manually. 3) Check edge cases: what happens with blank cells, zeros, text in number columns, or dates at month boundaries. 4) Verify the cell references point to the correct columns. 5) Test with both small and large values to catch overflow issues." },
    { q: "Are AI-generated Excel formulas safe to use?", a: "AI-generated formulas are generally accurate for standard patterns but should always be reviewed before deploying on important data. Common issues include: wrong column references, incorrect match types in lookups, logic errors in nested conditions, and formulas that work on sample data but fail on edge cases. The risk is low for simple formulas but increases significantly for complex nested logic. Always test before trusting." }
  ]
};

let processed = 0;
let skipped = 0;

for (const [slug, faqList] of Object.entries(faqs)) {
  const filePath = path.join(blogDir, `${slug}.html`);
  if (!fs.existsSync(filePath)) { console.log(`SKIP: ${slug}.html not found`); skipped++; continue; }
  let content = fs.readFileSync(filePath, 'utf8');
  if (content.includes('FAQPage')) { console.log(`SKIP: ${slug}.html already has FAQPage`); skipped++; continue; }
  const faqSchema = { "@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faqList.map(f => ({ "@type": "Question", "name": f.q, "acceptedAnswer": { "@type": "Answer", "text": f.a } })) };
  const scriptBlock = `  <script type="application/ld+json">\n${JSON.stringify(faqSchema, null, 2)}\n  </script>`;
  let styleIdx = content.indexOf('    <style>');
  if (styleIdx === -1) styleIdx = content.indexOf('  <style>');
  if (styleIdx === -1) styleIdx = content.indexOf('<style>');
  if (styleIdx === -1) { console.log(`SKIP: ${slug}.html - no <style> tag`); skipped++; continue; }
  content = content.substring(0, styleIdx) + scriptBlock + '\n' + content.substring(styleIdx);
  fs.writeFileSync(filePath, content, 'utf8');
  processed++;
  console.log(`OK: ${slug}.html - added ${faqList.length} FAQs`);
}
console.log(`\nRound 3 Done. Processed: ${processed}, Skipped: ${skipped}`);
