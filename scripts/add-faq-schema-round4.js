const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, '..', 'public', 'blog');

const faqs = {
  "add-flutter-to-existing-app": [
    { q: "Can I add Flutter to an existing Android or iOS app?", a: "Yes, Flutter supports add-to-app integration. You can embed Flutter as a module in an existing native Android (Kotlin/Java) or iOS (Swift/Objective-C) app. This lets you gradually migrate screens to Flutter without rewriting the entire app. Flutter runs as a FlutterEngine inside your native app and can share data through platform channels." },
    { q: "Should I rewrite my native app in Flutter or add Flutter gradually?", a: "For most teams, adding Flutter gradually is the safer approach. Start with one or two new screens built in Flutter while keeping the existing native code. This lets you evaluate Flutter's performance, developer experience, and maintainability before committing to a full rewrite. A full rewrite is only justified if the existing codebase has severe technical debt." }
  ],
  "ai-forecasting-model-excel": [
    { q: "Can AI build a forecasting model in Excel?", a: "Yes, AI tools like ChatGPT and Claude can help build forecasting models in Excel step by step. They can write moving average formulas, exponential smoothing calculations, trend-based projections, and seasonality adjustments. Describe your data (time period, values, any known patterns) and the AI generates the complete formula-based forecasting model." },
    { q: "What is the best forecasting method in Excel?", a: "The best method depends on your data. For stable trends, linear regression or moving averages work well. For data with seasonality, use the FORECAST.ETS function which handles seasonal patterns automatically. For simple projections, a weighted moving average is effective. Excel's built-in FORECAST.ETS function is the most powerful option for most business forecasting needs." }
  ],
  "ai-power-query-m-code": [
    { q: "Can AI write Power Query M code?", a: "Yes, ChatGPT, Claude, and Gemini can generate Power Query M code for data transformation tasks. Describe your source data, the transformations you need (remove columns, merge tables, pivot, filter, add calculated columns), and the desired output. The AI generates M code you can paste directly into the Power Query Advanced Editor." },
    { q: "How do I fix Power Query errors with AI?", a: "Paste the M code and the error message into ChatGPT or Claude. Describe what the query should do and what data sources it connects to. The AI will diagnose the issue, explain the cause, and provide corrected M code. Common fixes include data type mismatches, missing columns after source changes, and incorrect merge join types." }
  ],
  "amortization-schedule-excel": [
    { q: "How do I create a loan amortization schedule in Excel?", a: "Use PMT to calculate the fixed monthly payment, then for each period: interest = remaining balance times monthly rate, principal = payment minus interest, new balance = old balance minus principal. The key formulas are PMT(rate/12, term, -loan_amount) for the payment, and iterative calculations for each row showing how principal and interest change over time." },
    { q: "How do I add extra payments to an amortization schedule?", a: "Add an Extra Payment column next to the standard payment. In the balance calculation, subtract both the regular principal portion and the extra payment. Add a conditional check: if the remaining balance minus extra payment goes below zero, cap the extra payment at the remaining balance. This shows how extra payments reduce total interest and shorten the loan term." }
  ],
  "attendance-tracker-excel": [
    { q: "How do I create an attendance tracker in Excel?", a: "Create a table with employee names in rows and dates in columns. Use data validation dropdowns for attendance codes like P (present), A (absent), L (leave), H (holiday). Add COUNTIF formulas to calculate total present days, absent days, and attendance percentage per employee. Use conditional formatting to colour-code different attendance statuses for visual clarity." },
    { q: "Can I automate attendance tracking in Excel?", a: "Yes, use data validation for consistent entry, COUNTIF and COUNTIFS for automatic summaries, conditional formatting for visual status indicators, and pivot tables or GROUPBY for department-level reports. You can also add formulas that calculate leave balances, flag excessive absences, and generate monthly attendance reports automatically." }
  ],
  "audit-formulas-excel": [
    { q: "How do I trace formula errors in Excel?", a: "Use the Formula Auditing tools on the Formulas tab. Trace Precedents shows which cells feed into a formula. Trace Dependents shows which formulas use a cell. Evaluate Formula steps through a formula calculation one part at a time. Error Checking scans for common issues. These tools help you follow the chain of calculations to find where an error originates." },
    { q: "How do I find which cells a formula depends on in Excel?", a: "Select the cell with the formula and click Trace Precedents on the Formulas tab. Blue arrows show which cells feed into the formula. Click again to trace another level back. To find all cells that depend on a specific cell, select it and click Trace Dependents. Use Ctrl+[ to select all direct precedent cells, or Ctrl+] to select direct dependent cells." }
  ],
  "calendar-in-excel-automatic": [
    { q: "How do I create an automatic calendar in Excel?", a: "Use a dropdown or cell reference for the month and year. Calculate the first day of the month with DATE(year, month, 1), find its weekday with WEEKDAY, then use a formula grid to fill dates into a 7-column calendar layout. Dates outside the current month can be hidden or greyed out with conditional formatting. The calendar updates automatically when you change the month." },
    { q: "Can I make a calendar in Excel without VBA?", a: "Yes, you can build a fully functional auto-updating calendar using only formulas and conditional formatting. Use DATE, WEEKDAY, and simple arithmetic to place dates in a 7-column grid. Use conditional formatting to highlight today, weekends, and events. Data validation dropdowns let users select the month and year. No VBA or macros required." }
  ],
  "charts-visualisations": [
    { q: "How do I make professional charts in Excel?", a: "Start with clean source data, choose the right chart type for your data story, then customise: remove chart junk like gridlines and default legends, use a consistent colour palette, add direct data labels instead of requiring readers to reference axes, use meaningful titles that state the insight not just the topic, and align fonts with your presentation style." },
    { q: "What is the best chart type for my Excel data?", a: "Use bar or column charts for comparisons across categories. Use line charts for trends over time. Use pie charts only for showing parts of a whole with 5 or fewer categories. Use scatter plots for relationships between two variables. Use combo charts when showing two different scales. Use waterfall charts for showing how values build up or break down." }
  ],
  "clean-messy-data": [
    { q: "How do I clean messy data in Excel?", a: "Start with TRIM to remove extra spaces, CLEAN to remove non-printable characters, and PROPER or UPPER for consistent capitalisation. Use Find and Replace to fix common typos. Use Text to Columns to split combined fields. Remove duplicates with the Remove Duplicates button. Use IFERROR to handle error values. Work on a copy of your data, not the original." },
    { q: "What are the most common data quality issues in Excel?", a: "The most common issues are: extra leading or trailing spaces, inconsistent capitalisation, duplicate records, mixed date formats, numbers stored as text, blank rows splitting data ranges, merged cells breaking formulas, and inconsistent category names. TRIM, CLEAN, PROPER, and Remove Duplicates fix 80% of common data quality problems." }
  ],
  "conditional-formatting-tips": [
    { q: "How do I highlight rows based on cell values in Excel?", a: "Select the entire data range, go to Conditional Formatting and choose New Rule, select Use a formula, then enter a formula that references the first cell of the criteria column with the row locked but not the column. For example, to highlight rows where column D equals 'Late': =$D2='Late'. The dollar sign on D locks the column while the row number adjusts for each row." },
    { q: "Why is my conditional formatting not working in Excel?", a: "Common causes: the formula references are not set correctly (missing dollar signs for column locking), the rule applies to the wrong range, rules are in the wrong priority order (higher rules override lower ones), the formula returns text instead of TRUE/FALSE, or the cell format conflicts with the conditional format. Use Manage Rules to check and reorder your formatting rules." }
  ],
  "data-validation": [
    { q: "How do I add a dropdown list in Excel?", a: "Select the cells where you want the dropdown, go to Data tab then Data Validation, choose List from the Allow dropdown, then enter your options separated by commas or reference a range containing the list items. Using a named range or Excel Table column for the source list makes the dropdown automatically update when you add new items." },
    { q: "How do I create a dependent dropdown list in Excel?", a: "Create named ranges for each primary category's sub-options. Use the first dropdown with a regular list. For the second dropdown, use INDIRECT in the Data Validation source field referencing the first dropdown's value as a named range. For example, if the first dropdown selects a country, the second dropdown shows cities from a named range matching that country name." }
  ],
  "excel-tables-best-practices": [
    { q: "Why should I use Excel Tables instead of plain ranges?", a: "Excel Tables (Ctrl+T) provide automatic expansion when you add new data, structured references that are more readable than cell references, automatic formatting and banding, built-in filter and sort buttons, automatic total rows, and they make formulas auto-fill when you add new rows. Tables also work better with Copilot, Power Query, and pivot tables." },
    { q: "How do structured references work in Excel Tables?", a: "Structured references use column names instead of cell addresses. Instead of =SUM(B2:B100), you write =SUM(Table1[Revenue]). This is more readable, automatically adjusts when rows are added or removed, and does not break when columns are inserted. Use [@Column] to reference the current row's value in a calculated column." }
  ],
  "financial-modelling": [
    { q: "How do I build a financial model in Excel from scratch?", a: "Start with three linked financial statements: income statement, balance sheet, and cash flow statement. Build assumptions on a separate sheet. Use consistent formatting (blue for inputs, black for formulas). Link statements together so changes in assumptions flow through automatically. Add scenario analysis with data tables. Keep formulas simple and auditable." },
    { q: "What are the best practices for financial models in Excel?", a: "Use one formula per row, never hard-code numbers in formulas, colour-code inputs versus calculations, keep each section on a logical sheet, use named ranges for key assumptions, add error checks on every sheet, build in sensitivity analysis, document assumptions clearly, and always have a summary dashboard that shows key outputs. Simplicity and auditability matter more than complexity." }
  ],
  "gantt-chart-excel": [
    { q: "How do I make a Gantt chart in Excel?", a: "Create a table with Task Name, Start Date, Duration, and End Date columns. Insert a stacked bar chart using Start Date and Duration. Format the Start Date series to be invisible (no fill, no border). This leaves only the Duration bars visible, creating a Gantt chart. Add conditional formatting to show progress, and use data validation for task dependencies." },
    { q: "Can I make a Gantt chart in Excel without special software?", a: "Yes, Excel's built-in stacked bar chart can create effective Gantt charts. The trick is using the start date as an invisible base bar and the duration as the visible bar. For small to medium projects with up to 50 tasks, Excel Gantt charts work well. For complex projects with resource levelling and critical path analysis, dedicated project management tools are more suitable." }
  ],
  "inventory-tracker-excel": [
    { q: "How do I build an inventory tracker in Excel?", a: "Create three sheets: Products (master list with SKU, name, reorder point), Transactions (date, SKU, type, quantity for every stock-in and stock-out), and Dashboard (current stock levels calculated from transactions). Use SUMIFS to calculate current stock per product, conditional formatting to flag items below reorder point, and a data entry form with data validation for consistent transaction logging." },
    { q: "Can I track inventory in Excel instead of using special software?", a: "Yes, for small to medium businesses with up to a few hundred products. Excel handles inventory tracking well when structured properly with separate sheets for product master data, transactions, and reporting. The key is disciplined data entry and formula-driven calculations rather than manual updates. For businesses with thousands of SKUs or multiple warehouses, dedicated inventory software is more appropriate." }
  ],
  "keyboard-shortcuts": [
    { q: "What are the most useful Excel keyboard shortcuts?", a: "The most time-saving shortcuts are: Ctrl+T (create Table), Ctrl+Shift+L (toggle filters), Ctrl+1 (format cells), Ctrl+; (insert today's date), F4 (toggle absolute references), Alt+= (auto-sum), Ctrl+D (fill down), Ctrl+Shift+End (select to last cell), Ctrl+Home (go to A1), and F2 (edit cell). Learning just these 10 shortcuts saves hours per week." },
    { q: "How do I get faster at Excel?", a: "Learn keyboard shortcuts for your most frequent actions, use Excel Tables instead of plain ranges, master XLOOKUP and SUMIFS to eliminate manual lookups, build templates for recurring work, use named ranges for clarity, and learn Power Query for repetitive data imports. The biggest time saver is reducing mouse usage — most Excel power users rarely touch the mouse." }
  ],
  "map-charts-excel": [
    { q: "How do I create a map chart in Excel?", a: "Select your data with geographic labels (country names, state names, or postal codes) and values, go to Insert then Charts then Map. Excel creates a filled map chart automatically. Ensure your geographic names match Excel's expected format — use full country names rather than abbreviations, and be consistent with naming conventions for regions and states." },
    { q: "Why is my Excel map chart not showing data correctly?", a: "Common issues: geographic names do not match Excel's expected format (use United States not US), mixed geographic levels in the same column (countries and cities together), missing or misspelled location names, or data that spans too many different geographic levels. Clean your location names first and ensure all values are at the same geographic level." }
  ],
  "monthly-budget-spreadsheet-excel": [
    { q: "How do I create a monthly budget in Excel?", a: "Create categories for income and expenses, add columns for budgeted amounts and actual amounts, and use formulas to calculate the variance (actual minus budget). Group expenses into categories like housing, transport, food, and savings. Add a summary section showing total income, total expenses, and net savings. Use conditional formatting to highlight categories where you exceed the budget." },
    { q: "What is the best budget template for Excel?", a: "The best budget template has: income section at the top, fixed expenses (rent, insurance, subscriptions), variable expenses (food, transport, entertainment), a savings/investment section, and a summary dashboard. Use the 50-30-20 framework as a starting point: 50% needs, 30% wants, 20% savings. Automate calculations with SUMIFS by category and add month-over-month comparison charts." }
  ],
  "power-pivot-guide": [
    { q: "What is Power Pivot in Excel?", a: "Power Pivot is an Excel add-in that lets you analyse millions of rows of data that would be too large for regular Excel worksheets. It uses an in-memory data engine to compress and process large datasets, supports relationships between multiple tables (like a database), and uses DAX formulas for advanced calculations like year-over-year growth, running totals, and time intelligence." },
    { q: "When should I use Power Pivot instead of regular Excel?", a: "Use Power Pivot when your data exceeds 100,000 rows, when you need to combine data from multiple tables with relationships, when you need advanced calculations like year-over-year comparisons or distinct counts, or when regular pivot tables are too slow. For datasets under 100,000 rows with simple analysis needs, regular Excel formulas and pivot tables are sufficient." }
  ],
  "power-query-guide": [
    { q: "What is Power Query in Excel?", a: "Power Query is Excel's built-in data transformation tool. It connects to data sources (files, databases, web APIs), transforms the data (remove columns, filter rows, merge tables, change types, unpivot), and loads clean data into your workbook. The key advantage is that transformations are repeatable — when source data changes, you click Refresh and all transformations re-apply automatically." },
    { q: "When should I use Power Query instead of formulas?", a: "Use Power Query when you repeatedly import and clean data from external sources, when you need to combine data from multiple files or tables, when data cleaning requires many steps (removing columns, filtering, splitting, reshaping), or when the same transformation needs to run weekly or monthly. Power Query records your steps and replays them on new data, eliminating repetitive manual work." }
  ],
  "project-tracker-excel": [
    { q: "How do I build a project tracker in Excel?", a: "Create columns for Task, Owner, Start Date, Due Date, Status, Priority, and Percent Complete. Use data validation dropdowns for Status (Not Started, In Progress, Complete, Blocked) and Priority (High, Medium, Low). Add conditional formatting to highlight overdue tasks and a summary section with COUNTIFS showing tasks by status. Keep it simple — over-engineering project trackers is the main reason they get abandoned." },
    { q: "Is Excel good enough for project management?", a: "For small to medium projects with a single team and up to 50-100 tasks, Excel is perfectly adequate. Its advantages are flexibility, no additional cost, and familiarity. For projects with multiple teams, resource dependencies, critical path analysis, or collaborative real-time updates, dedicated tools like Asana, Jira, or Monday.com are more appropriate." }
  ],
  "protect-excel-workbook-collaboration": [
    { q: "How do I protect an Excel workbook without blocking collaboration?", a: "Use sheet protection (Review tab then Protect Sheet) to lock formulas and structure while leaving input cells unlocked. Select the cells users need to edit, right-click Format Cells, go to Protection, and uncheck Locked before applying sheet protection. This allows collaborative editing of data entry cells while preventing accidental changes to formulas and layout." },
    { q: "Can I protect formulas but allow data entry in Excel?", a: "Yes, unlock the data entry cells first (select them, Format Cells, Protection, uncheck Locked), then protect the sheet. All cells are locked by default when you protect a sheet, so only the explicitly unlocked cells will be editable. This is the standard approach for creating protected templates where users can enter data but cannot modify the formulas or structure." }
  ],
  "py-function-excel": [
    { q: "What is the PY function in Excel?", a: "The PY function lets you run Python code directly in an Excel cell. Type =PY in a cell to open the Python editor, write Python code that can reference Excel data, and the result appears in the cell. Python runs in the cloud on Microsoft's servers, so no local Python installation is needed. It supports pandas, matplotlib, scikit-learn, and other data science libraries." },
    { q: "Do I need to know Python to use the PY function in Excel?", a: "Basic Python knowledge is helpful but not strictly required if you use Copilot to generate the Python code. Copilot can write Python scripts for data analysis, visualisation, and statistical tasks that run inside Excel cells. However, understanding Python basics helps you review, modify, and debug the generated code for more reliable results." }
  ],
  "python-in-excel-beginners": [
    { q: "How do I get started with Python in Excel?", a: "Enable Python in Excel through your Microsoft 365 subscription, click a cell, type =PY to open the Python editor, and start writing Python code. Begin with simple tasks: import pandas, reference Excel ranges as DataFrames, and return calculated results. The first 10 things to learn are: referencing Excel data, pandas basics, filtering, grouping, simple plots, and returning results to cells." },
    { q: "Is Python in Excel free?", a: "Python in Excel is included with Microsoft 365 subscriptions. The Python execution runs in the cloud on Microsoft's infrastructure, so you do not need to install Python locally. There is no additional cost for the Python feature itself, though it requires an active Microsoft 365 subscription." }
  ],
  "sales-pipeline-tracker-excel": [
    { q: "How do I build a sales pipeline tracker in Excel?", a: "Create a table with columns for Deal Name, Company, Contact, Stage (Lead, Qualified, Proposal, Negotiation, Closed Won, Closed Lost), Value, Probability, Expected Close Date, and Owner. Use data validation for Stage and Owner fields. Add calculated columns for weighted value (Value times Probability) and days in stage. Build a summary dashboard with SUMIFS by stage." },
    { q: "Can I manage a sales pipeline in Excel?", a: "Yes, Excel works well for small sales teams tracking up to 100-200 active deals. Use structured tables with data validation, conditional formatting for deal aging, and pivot tables or SUMIFS for pipeline summaries. For larger teams or when you need automated email reminders, shared real-time access, or CRM integrations, dedicated tools like HubSpot or Salesforce are more appropriate." }
  ],
  "text-analysis-excel-with-ai": [
    { q: "Can AI analyse text data in Excel?", a: "Yes, AI tools can analyse survey responses, customer reviews, support tickets, and other text data in Excel. ChatGPT and Claude can write formulas or VBA macros to categorise text, extract sentiment, identify themes, and summarise large volumes of feedback. The COPILOT function in Excel can also process text data directly in cells for classification and summarisation tasks." },
    { q: "How do I categorise survey responses in Excel with AI?", a: "Paste a sample of your responses and categories into ChatGPT or Claude and ask for a classification approach. The AI can generate XLOOKUP or IF-based formulas for keyword matching, or VBA code for more complex pattern matching. Alternatively, use the COPILOT function in Excel to classify each response directly in a formula cell with a prompt like 'Categorise this feedback as positive, negative, or neutral'." }
  ],
  "what-if-analysis": [
    { q: "What is What-If Analysis in Excel?", a: "What-If Analysis lets you test different scenarios by changing input values and seeing how they affect results. Excel offers three tools: Goal Seek (find the input needed to reach a target output), Scenario Manager (save and compare multiple sets of input values), and Data Tables (show results for many input combinations in a grid). These tools help with forecasting, planning, and decision-making." },
    { q: "How do I use Goal Seek in Excel?", a: "Go to Data tab, What-If Analysis, then Goal Seek. Set the Set Cell to the cell containing your result formula, To Value to the target you want to achieve, and By Changing Cell to the input cell Excel should adjust. Excel iterates to find the input value that produces your target result. For example, find the sales volume needed to reach a target profit, or the interest rate that produces a specific monthly payment." }
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
console.log(`\nRound 4 (FINAL) Done. Processed: ${processed}, Skipped: ${skipped}`);
