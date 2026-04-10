const fs = require('fs');
const path = require('path');

const blogDir = path.join(__dirname, '..', 'public', 'blog');

const faqs = {
  "cursor-flutter-development": [
    { q: "Is Cursor good for Flutter development?", a: "Yes, Cursor is one of the best AI-powered IDEs for Flutter development in 2026. It offers inline code generation, multi-file editing with Composer, context-aware completions for Dart and Flutter widgets, and deep integration with AI models. It significantly speeds up widget creation, boilerplate generation, and refactoring." },
    { q: "How do I set up Cursor for Flutter?", a: "Install Cursor from cursor.com, then install the Flutter and Dart extensions from the extensions marketplace. Set your Flutter SDK path in settings and configure your preferred AI model. Cursor works with your existing Flutter projects immediately and supports hot reload, DevTools, and all standard Flutter tooling." }
  ],
  "windsurf-flutter-development": [
    { q: "Is Windsurf free for Flutter development?", a: "Yes, Windsurf offers a free tier that includes AI-assisted coding for Flutter and Dart. The free plan includes the Cascade agent for multi-step code generation, inline completions, and chat-based coding assistance. It is one of the best free alternatives to Cursor for Flutter development." },
    { q: "How does Windsurf compare to Cursor for Flutter?", a: "Both are excellent for Flutter. Cursor has more mature AI features and better multi-file editing. Windsurf is free and its Cascade agent handles multi-step Flutter tasks well. For budget-conscious developers, Windsurf is the stronger choice. For maximum AI capability, Cursor has the edge." }
  ],
  "claude-code-vscode": [
    { q: "How do I use Claude Code in VS Code?", a: "Claude Code runs as a terminal-based AI agent that integrates with VS Code. Install it via npm, authenticate with your Anthropic API key, and run it from the integrated terminal. It can read your project files, write code, run commands, and make multi-file edits autonomously. It works particularly well for refactoring and implementing features across multiple files." },
    { q: "Is Claude Code better than GitHub Copilot?", a: "They serve different purposes. GitHub Copilot excels at inline code completions as you type. Claude Code is an autonomous agent that can understand your entire codebase, plan changes across multiple files, and execute them. Copilot is better for line-by-line assistance. Claude Code is better for larger tasks like implementing features, debugging complex issues, or refactoring." }
  ],
  "claude-code-android-studio": [
    { q: "Can I use Claude Code in Android Studio?", a: "Yes, Claude Code works in Android Studio through the integrated terminal. Install it via npm, then run it from Android Studio terminal. It can read your Kotlin, Flutter, Dart, and Gradle files, understand the project structure, and make changes across multiple files. It is particularly useful for Flutter and Kotlin projects in Android Studio." },
    { q: "How does Claude Code work with Flutter in Android Studio?", a: "Claude Code reads your Flutter project structure, understands Dart files, pubspec.yaml, and build configurations. You can ask it to create widgets, implement features, fix bugs, or refactor code. It works through the terminal and can edit multiple files simultaneously, making it effective for feature implementation that spans multiple screens and services." }
  ],
  "gemini-cli-vscode": [
    { q: "How do I set up Gemini CLI in VS Code?", a: "Install Gemini CLI using npm (npm install -g @anthropic-ai/gemini-cli or the official Google package), authenticate with your API key, and run it from the VS Code integrated terminal. It can read your project files, generate code, run tests, and make multi-file edits. It integrates well with VS Code workspace settings." },
    { q: "Is Gemini CLI free to use?", a: "Gemini CLI uses the Gemini API which has a generous free tier. For most individual developer usage, the free tier is sufficient. Heavy usage or team deployments may require a paid plan. The CLI tool itself is free and open source." }
  ],
  "gemini-cli-android-studio-flutter": [
    { q: "Can I use Gemini CLI for Flutter development in Android Studio?", a: "Yes, Gemini CLI works in Android Studio through the integrated terminal and can be configured as an MCP server for deeper integration. It understands Dart, Flutter widgets, pubspec.yaml, and Android build configurations. You can use it for code generation, debugging, refactoring, and implementing features across your Flutter project." },
    { q: "What is MCP server integration with Gemini CLI?", a: "MCP (Model Context Protocol) allows Gemini CLI to integrate more deeply with your IDE. When configured as an MCP server in Android Studio, Gemini CLI can access project context, file trees, and build information more efficiently. This results in better code suggestions that are more aware of your project structure and dependencies." }
  ],
  "gemini-code-assist-android-studio": [
    { q: "Is Gemini Code Assist free in Android Studio?", a: "Yes, Gemini Code Assist is free for individual developers in Android Studio. It provides AI-powered code completions, chat-based coding assistance, and code explanations for Kotlin, Flutter, Dart, Java, and Gradle projects. The free tier includes a generous monthly usage limit." },
    { q: "How does Gemini Code Assist compare to GitHub Copilot?", a: "Both provide inline code completions. Gemini Code Assist is free and has strong Kotlin and Android-specific knowledge since it is built by Google. GitHub Copilot has broader language support and more mature multi-file context. For Android and Flutter development specifically, Gemini Code Assist is a strong free alternative to Copilot." }
  ],
  "copilot-agent-mode-vscode": [
    { q: "What is GitHub Copilot Agent Mode in VS Code?", a: "Agent Mode is Copilot's autonomous coding capability in VS Code. Instead of just completing individual lines, Agent Mode can plan and execute multi-step tasks: create files, implement features across multiple files, run terminal commands, fix errors, and iterate on its own output. It works through the Copilot Chat panel and can handle complex coding tasks with minimal guidance." },
    { q: "How is Copilot Agent Mode different from regular Copilot?", a: "Regular Copilot provides inline code completions as you type, one suggestion at a time. Agent Mode is autonomous: you describe a task in natural language and the agent plans the implementation, creates or modifies multiple files, runs commands, and validates its work. Regular Copilot assists you line by line. Agent Mode can implement entire features independently." }
  ],
  "deepseek-vscode": [
    { q: "How much does DeepSeek cost for VS Code?", a: "DeepSeek is one of the most affordable AI coding assistants. API access costs approximately $2 per month for typical individual developer usage. You can configure it in VS Code using the Continue extension or other compatible AI coding extensions with your DeepSeek API key." },
    { q: "Is DeepSeek good for coding?", a: "Yes, DeepSeek performs well on coding tasks, particularly for Python, JavaScript, TypeScript, and common web frameworks. It offers strong code completion and generation at a fraction of the cost of ChatGPT or Claude. For budget-conscious developers who want AI coding assistance, DeepSeek is an excellent option." }
  ],
  "opencode-vscode": [
    { q: "What is OpenCode and is it free?", a: "OpenCode is a free, open-source AI coding assistant that runs in VS Code. It supports multiple AI model backends including OpenAI, Anthropic, Google, and local models via Ollama. Because it is open source, you have full control over your data and can choose which AI provider to use." },
    { q: "How does OpenCode compare to Cursor or Copilot?", a: "OpenCode is free and open source, while Cursor and Copilot are commercial products. OpenCode offers flexibility in choosing your AI backend and is fully transparent. Cursor and Copilot have more polished UIs and tighter IDE integration. OpenCode is best for developers who value open source, privacy, or want to use their own AI API keys." }
  ],
  "create-with-ai-flutter": [
    { q: "Can I use AI to build Flutter apps?", a: "Yes, in 2026 there are several AI tools specifically designed for Flutter development. Gemini CLI with MCP integration, Claude Code, Cursor, and the Flutter AI Toolkit all support AI-assisted widget creation, feature implementation, and code generation for Dart and Flutter projects. AI can significantly speed up boilerplate creation, layout building, and feature implementation." },
    { q: "What is the Flutter AI Toolkit?", a: "The Flutter AI Toolkit is a set of tools and integrations that enable AI-assisted Flutter development. It includes support for Gemini CLI with MCP servers for IDE integration, AI-powered code generation for Dart, and tooling for connecting Flutter apps to AI backends. It is designed to make building AI-powered Flutter applications easier." }
  ],
  "gemma-4-vs-chatgpt-vs-claude": [
    { q: "How does Gemma 4 compare to ChatGPT and Claude?", a: "Gemma 4 is Google's open-weight model that can run locally for free, while ChatGPT and Claude are cloud-based paid services. For coding tasks, ChatGPT and Claude generally produce better results on complex problems. However, Gemma 4 is surprisingly competitive on standard coding tasks and excels at privacy-sensitive work since your data never leaves your machine." },
    { q: "Is Gemma 4 good enough to replace ChatGPT?", a: "For many common tasks, yes. Gemma 4 handles code generation, formula writing, text summarisation, and Q&A well. It falls short of ChatGPT and Claude on complex multi-step reasoning, very long context tasks, and tasks requiring internet access or file processing. The biggest advantage of Gemma 4 is that it is completely free and runs locally with full privacy." }
  ],
  "gemma-4-vs-gpt-vs-llama-excel": [
    { q: "Which free AI model is best for Excel formulas?", a: "Among free models, Gemma 4 and Llama 4 both handle Excel formulas well. Gemma 4 tends to be slightly more accurate for complex nested formulas and provides clearer explanations. Llama 4 is strong for general formula generation but less consistent on edge cases. For Excel-specific work, Gemma 4 is the better free choice." },
    { q: "Can free AI models write XLOOKUP and SUMIFS formulas?", a: "Yes, both Gemma 4 and Llama 4 can write XLOOKUP, SUMIFS, dynamic array formulas, and other modern Excel functions accurately. They handle most standard formula requests as well as paid models like ChatGPT. For very complex nested formulas with multiple conditions, paid models still have an edge in reliability." }
  ],
  "gemma-4-data-analysis-excel": [
    { q: "Can Gemma 4 do data analysis like ChatGPT?", a: "Gemma 4 can help with data analysis by writing formulas, explaining patterns, and suggesting analysis approaches. However, it cannot open or process Excel files directly like ChatGPT with Code Interpreter. You need to describe your data or paste it as text. For formula-based analysis guidance, Gemma 4 is surprisingly capable for a free local model." },
    { q: "Is Gemma 4 accurate for spreadsheet work?", a: "Yes, Gemma 4 produces accurate results for most standard spreadsheet tasks including VLOOKUP, XLOOKUP, SUMIFS, pivot table guidance, and data cleaning formulas. It occasionally makes errors on very complex nested formulas with multiple criteria, but for the majority of everyday Excel work, its accuracy is comparable to paid alternatives." }
  ],
  "gemma-4-vs-gemini": [
    { q: "What is the difference between Gemma 4 and Gemini?", a: "Gemma 4 is an open-weight model you can download and run locally on your own hardware. Gemini is Google's cloud-based AI service accessed through the web or API. Gemma 4 offers privacy and offline use but has a smaller model size. Gemini is more capable for complex tasks but requires an internet connection and sends your data to Google servers." },
    { q: "Should I use Gemma 4 or Gemini?", a: "Use Gemini when you need the strongest possible AI responses, internet access, or multimodal capabilities like image understanding. Use Gemma 4 when you need privacy, offline access, or want to avoid API costs. For sensitive data that cannot leave your machine, Gemma 4 is the only option. For maximum capability, Gemini is stronger." }
  ],
  "gemma-4-vs-paid-ai-models": [
    { q: "Can Gemma 4 beat paid AI models?", a: "Yes, for certain tasks Gemma 4 matches or beats paid models. It performs particularly well on standard code generation, Excel formula writing, text summarisation, and structured data extraction. Where paid models like ChatGPT and Claude still win is on complex multi-step reasoning, very long documents, and tasks requiring tool use like file processing or web browsing." },
    { q: "What tasks is Gemma 4 best at?", a: "Gemma 4 excels at code generation for common languages, Excel formula writing, text classification and summarisation, translation, and structured Q&A. It is also the best choice for any task involving sensitive or private data since it runs entirely on your local machine with no data leaving your computer." }
  ],
  "gemma-4-vscode": [
    { q: "How do I use Gemma 4 in VS Code?", a: "Install Ollama, download the Gemma 4 model, then configure a VS Code AI extension like Continue or CodeGPT to use the local Ollama endpoint. This gives you AI code completions, chat-based coding assistance, and code generation powered by Gemma 4 running entirely on your machine, with no API costs and full privacy." },
    { q: "Does Gemma 4 work well for code completion in VS Code?", a: "Yes, Gemma 4 provides solid code completions for Python, JavaScript, TypeScript, Dart, and most popular languages. Its completions are not quite as fast or accurate as GitHub Copilot for complex multi-line suggestions, but it is completely free and private. For individual developers who want AI assistance without subscriptions, it is an excellent option." }
  ],
  "gemma-4-android-studio-ollama": [
    { q: "Can I use Gemma 4 locally in Android Studio?", a: "Yes, install Ollama and download the Gemma 4 model, then configure an Android Studio AI plugin to connect to your local Ollama endpoint. This gives you AI-powered code completions and chat assistance for Kotlin, Flutter, Dart, and Gradle projects, all running locally with no API costs or data leaving your machine." },
    { q: "Is local AI coding practical for Android development?", a: "Yes, with 16GB or more RAM and a modern CPU, Gemma 4 via Ollama provides responsive code completions for Kotlin and Flutter development. Response times are slightly slower than cloud-based alternatives but perfectly usable for everyday coding. The main advantages are zero cost, full privacy, and offline availability." }
  ],
  "run-gemma-4-locally": [
    { q: "How do I run Gemma 4 locally for free?", a: "The easiest way is to install Ollama (free, available for Windows, Mac, and Linux), then run 'ollama pull gemma3' (or the latest gemma version) from your terminal. The model downloads once and runs locally. You can also use LM Studio for a graphical interface. Minimum hardware: 8GB RAM for the smaller model, 16GB recommended for the full model." },
    { q: "What hardware do I need to run Gemma 4?", a: "Minimum requirements: 8GB RAM for the smaller Gemma 4 model, 16GB RAM for the full model. A modern CPU with AVX2 support is needed. A GPU is optional but significantly speeds up inference. On a Mac with Apple Silicon (M1 or later), Gemma 4 runs particularly well using unified memory. Most modern laptops from 2020 onwards can run the smaller model." }
  ],
  "flutter-testing-strategy-2026": [
    { q: "What is the best testing strategy for Flutter apps in 2026?", a: "A practical Flutter testing strategy has four layers: unit tests for business logic and state management, widget tests for UI component behaviour, integration tests for critical user flows, and golden tests for visual regression detection. Start with unit tests for your most important business logic, then add widget tests for complex UI components, and integration tests for key user journeys." },
    { q: "Should I use unit tests or widget tests in Flutter?", a: "Use both, but prioritise unit tests for business logic, repository methods, and state management. Widget tests are for verifying UI behaviour like tap handling, form validation, and conditional rendering. Unit tests run faster and are easier to maintain. Widget tests catch visual and interaction bugs that unit tests miss. A good ratio is roughly 60% unit tests, 30% widget tests, and 10% integration tests." }
  ],
  "flutter-performance-2026": [
    { q: "How do I improve Flutter app performance in 2026?", a: "The key strategies for Flutter performance in 2026 are: use Impeller (the new rendering engine) for smoother animations, reduce unnecessary widget rebuilds with const constructors and selective state management, use DevTools to profile and identify bottlenecks, lazy-load images and heavy content, and avoid expensive operations on the main isolate. The Flutter DevTools Performance tab is the best tool for diagnosing issues." },
    { q: "What is Impeller in Flutter?", a: "Impeller is Flutter's new rendering engine that replaces Skia for most platforms. It pre-compiles shaders during build time, eliminating shader compilation jank (stuttering during animations). Impeller is enabled by default on iOS and Android in 2026 and provides significantly smoother animations and faster first-frame rendering compared to the older Skia renderer." }
  ],
  "flutter-web-skwasm-vs-canvaskit": [
    { q: "Should I use skwasm or CanvasKit for Flutter web?", a: "In 2026, skwasm is the recommended renderer for most Flutter web apps. It uses WebAssembly for better performance and smaller bundle sizes compared to CanvasKit. CanvasKit still produces more pixel-perfect rendering for complex custom painting. Use skwasm for general web apps and CanvasKit only when exact rendering fidelity with mobile is critical." },
    { q: "Is Flutter good for web development in 2026?", a: "Flutter web has improved significantly in 2026 with the skwasm renderer and better WebAssembly support. It is a strong choice for web apps that need to share code with mobile (dashboards, admin panels, internal tools). For content-heavy public websites that need SEO, traditional web frameworks like Next.js or Astro are still better choices." }
  ],
  "flutter-form-validation-best-practices": [
    { q: "What is the best way to validate forms in Flutter?", a: "Use the built-in Form and TextFormField widgets with a GlobalKey for form state. Define validation logic in the validator parameter of each field. For complex validation (async checks like username availability), use a state management solution to handle loading states. Always validate on the client side for UX and on the server side for security." },
    { q: "How do I show validation errors in Flutter forms?", a: "TextFormField automatically displays validation errors below the field when the validator returns a non-null string and the form is validated. Customise the error style with the decoration's errorStyle property. For real-time validation, use autovalidateMode: AutovalidateMode.onUserInteraction so errors appear as the user types, not just on submit." }
  ],
  "responsive-flutter-ui-all-screens": [
    { q: "How do I make a Flutter app responsive for all screen sizes?", a: "Use LayoutBuilder and MediaQuery to detect screen dimensions, then adapt your layout using breakpoints (typically 600px for tablet, 1200px for desktop). Use Flexible and Expanded widgets for proportional sizing. For navigation, switch between BottomNavigationBar on mobile and NavigationRail on tablet/desktop. The key pattern is building adaptive layouts that reorganise for each form factor." },
    { q: "Does Flutter support desktop and web responsive design?", a: "Yes, Flutter's layout system supports responsive design across mobile, tablet, desktop, and web. Use MediaQuery for breakpoints, LayoutBuilder for parent-constraint-aware layouts, and conditional widget trees that show different layouts per screen size. Flutter handles window resizing natively on desktop and web, so your layouts can adapt dynamically as the user resizes the window." }
  ],
  "go-router-flutter-deep-linking": [
    { q: "What is go_router in Flutter?", a: "go_router is the recommended routing package for Flutter in 2026. It provides declarative routing with support for deep linking, nested navigation, URL-based routing for web, route guards for authentication, and shell routes for persistent navigation (like a bottom nav bar that stays across screens). It replaces the imperative Navigator.push pattern for most apps." },
    { q: "How do I set up deep linking in Flutter with go_router?", a: "Define your routes using GoRouter with path-based route definitions. go_router automatically handles deep links by matching incoming URLs to your defined routes. For Android, configure intent filters in AndroidManifest.xml. For iOS, set up Associated Domains. For web, it works automatically since go_router uses URL-based navigation. No additional deep linking plugin is needed." }
  ],
  "flutter-widget-previewer": [
    { q: "What is the Flutter Widget Previewer?", a: "The Flutter Widget Previewer allows you to see your widgets rendered in real-time without running the full app. It provides hot-reload-like feedback for individual widgets, making UI iteration much faster. Instead of navigating through your app to reach a specific screen, you can preview any widget in isolation with sample data." },
    { q: "How do I preview Flutter widgets without running the app?", a: "Use the Flutter Widget Previewer extension or tooling that supports isolated widget rendering. Define your widget with sample data, and the previewer renders it in real time as you edit. This is particularly useful for design system components, reusable widgets, and complex layouts where navigating through the full app to see changes slows down development." }
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

  // Try both whitespace patterns for the <style> tag
  let styleIdx = content.indexOf('    <style>');
  if (styleIdx === -1) {
    styleIdx = content.indexOf('  <style>');
  }
  if (styleIdx === -1) {
    styleIdx = content.indexOf('<style>');
  }

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

console.log(`\nRound 2 Done. Processed: ${processed}, Skipped: ${skipped}`);
