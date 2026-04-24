const fs = require('fs');
const http = require('http');
const path = require('path');
const { spawn } = require('child_process');

const ROOT = path.resolve(__dirname, '..');
const BASE_URL = process.env.MOBILE_CHECK_BASE_URL || 'http://127.0.0.1:4173';
const CHROME = process.env.CHROME_PATH || 'C:/Program Files/Google/Chrome/Application/chrome.exe';
const DEBUG_PORT = Number(process.env.CHROME_DEBUG_PORT || 9222);
const now = new Date();
const DATE = process.env.MOBILE_CHECK_DATE || [
  now.getFullYear(),
  String(now.getMonth() + 1).padStart(2, '0'),
  String(now.getDate()).padStart(2, '0'),
].join('-');
const OUT_DIR = path.join(ROOT, '.claude', 'responsive-checks', 'screenshots', DATE);
const REPORT = path.join(ROOT, 'reports', `mobile-render-${DATE}.md`);

const PAGES = [
  ['Home', '/index.html'],
  ['Tutorial grid', '/blog.html'],
  ['Excel hub', '/blog/excel-formulas-guide.html'],
  ['HR tutorial', '/blog/excel-ai-for-hr-teams.html'],
  ['Workbook protection tutorial', '/blog/protect-excel-workbook-collaboration.html'],
  ['Long Flutter tutorial', '/blog/flutter-renderflex-overflow-row-listview.html'],
  ['Long AI tutorial', '/blog/run-gemma-4-locally.html'],
  ['Seedance tutorial', '/blog/seedance-youtube-shorts.html'],
];

const VIEWPORTS = [
  ['narrow', 360, 800],
  ['iphone', 390, 844],
];

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function requestJson(url, options = {}) {
  return new Promise((resolve, reject) => {
    const req = http.request(url, options, res => {
      let body = '';
      res.setEncoding('utf8');
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(body));
        } catch (err) {
          reject(new Error(`Bad JSON from ${url}: ${err.message}\n${body.slice(0, 200)}`));
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
}

async function waitForChrome() {
  const deadline = Date.now() + 15000;
  while (Date.now() < deadline) {
    try {
      return await requestJson(`http://127.0.0.1:${DEBUG_PORT}/json/version`);
    } catch (_) {
      await sleep(250);
    }
  }
  throw new Error('Chrome DevTools endpoint did not become ready');
}

function cdp(wsUrl) {
  const ws = new WebSocket(wsUrl);
  let id = 0;
  const pending = new Map();
  const events = [];

  ws.onmessage = msg => {
    const payload = JSON.parse(msg.data);
    if (payload.id && pending.has(payload.id)) {
      const { resolve, reject } = pending.get(payload.id);
      pending.delete(payload.id);
      if (payload.error) reject(new Error(JSON.stringify(payload.error)));
      else resolve(payload.result);
    } else if (payload.method) {
      events.push(payload);
    }
  };

  const ready = new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });

  return {
    ready,
    send(method, params = {}) {
      const callId = ++id;
      ws.send(JSON.stringify({ id: callId, method, params }));
      return new Promise((resolve, reject) => pending.set(callId, { resolve, reject }));
    },
    waitForEvent(method, timeout = 10000) {
      return new Promise((resolve, reject) => {
        const existing = events.findIndex(e => e.method === method);
        if (existing >= 0) return resolve(events.splice(existing, 1)[0]);
        const timer = setTimeout(() => {
          ws.removeEventListener('message', handler);
          reject(new Error(`Timed out waiting for ${method}`));
        }, timeout);
        const handler = msg => {
          const payload = JSON.parse(msg.data);
          if (payload.method === method) {
            clearTimeout(timer);
            ws.removeEventListener('message', handler);
            resolve(payload);
          }
        };
        ws.addEventListener('message', handler);
      });
    },
    close() {
      ws.close();
    }
  };
}

function slugify(input) {
  return input.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function checkExpression() {
  return `(() => {
    const width = window.innerWidth;
    const height = window.innerHeight;
    const doc = document.documentElement;
    const body = document.body;
    const selector = 'body *';
    const offenders = [];
    const contained = [];
    const hasOverflowBoundary = (el) => {
      let node = el.parentElement;
      while (node && node !== document.body && node !== document.documentElement) {
        const style = getComputedStyle(node);
        const clipsX = /auto|scroll|hidden|clip/.test(style.overflowX);
        if (clipsX) {
          const rect = node.getBoundingClientRect();
          if (rect.left >= -2 && rect.right <= width + 2) return true;
        }
        node = node.parentElement;
      }
      return false;
    };
    for (const el of document.querySelectorAll(selector)) {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      if (!rect.width || !rect.height) continue;
      if (style.display === 'none' || style.visibility === 'hidden') continue;
      if (style.position === 'fixed' && rect.top < -height) continue;
      const tooWide = rect.width > width + 2;
      const leaksLeft = rect.left < -2;
      const leaksRight = rect.right > width + 2;
      if (tooWide || leaksLeft || leaksRight) {
        const text = (el.innerText || el.getAttribute('aria-label') || el.getAttribute('alt') || '').trim().replace(/\\s+/g, ' ').slice(0, 120);
        const row = {
          tag: el.tagName.toLowerCase(),
          className: String(el.className || '').slice(0, 120),
          id: el.id || '',
          text,
          transform: style.transform === 'none' ? '' : style.transform,
          left: Math.round(rect.left),
          right: Math.round(rect.right),
          width: Math.round(rect.width),
        };
        if (hasOverflowBoundary(el)) contained.push(row);
        else offenders.push(row);
      }
    }
    const clickable = [...document.querySelectorAll('a,button,input,textarea,select,[role="button"]')]
      .filter(el => {
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return rect.width && rect.height && style.display !== 'none' && style.visibility !== 'hidden';
      })
      .map(el => {
        const rect = el.getBoundingClientRect();
        return { tag: el.tagName.toLowerCase(), text: (el.innerText || el.getAttribute('aria-label') || '').trim().replace(/\\s+/g, ' ').slice(0, 80), width: Math.round(rect.width), height: Math.round(rect.height) };
      })
      .filter(x => x.width < 32 || x.height < 32)
      .slice(0, 8);
    return {
      title: document.title,
      innerWidth: width,
      scrollWidth: doc.scrollWidth,
      bodyScrollWidth: body ? body.scrollWidth : 0,
      documentHeight: Math.max(doc.scrollHeight, body ? body.scrollHeight : 0),
      offenders: offenders.slice(0, 12),
      offenderCount: offenders.length,
      containedOverflowCount: contained.length,
      smallTargets: clickable,
      navOpen: !!document.querySelector('.nav-links.active, #navLinks.active'),
      hasHorizontalOverflow: offenders.length > 0,
    };
  })()`;
}

function waitForStylesExpression() {
  return `new Promise(resolve => {
    const deadline = Date.now() + 4000;
    const check = () => {
      const links = [...document.querySelectorAll('link[rel="stylesheet"]')];
      const ready = links.every(link => {
        const media = (link.media || '').toLowerCase();
        return link.sheet && media !== 'print';
      });
      if (ready || Date.now() > deadline) resolve({ ready, links: links.map(link => ({ href: link.href, media: link.media || '', hasSheet: !!link.sheet })) });
      else setTimeout(check, 100);
    };
    check();
  })`;
}

async function evaluatePage(client, pageLabel, route, viewportLabel, width, height) {
  await client.send('Emulation.setDeviceMetricsOverride', {
    width,
    height,
    deviceScaleFactor: 2,
    mobile: true,
    screenWidth: width,
    screenHeight: height,
  });
  await client.send('Emulation.setTouchEmulationEnabled', { enabled: true });
  await client.send('Emulation.setEmulatedMedia', {
    features: [{ name: 'prefers-reduced-motion', value: 'reduce' }],
  });
  await client.send('Page.navigate', { url: `${BASE_URL}${route}` });
  try {
    await client.waitForEvent('Page.loadEventFired', 15000);
  } catch (_) {
    // Some pages wait on third-party scripts; DOM checks still work after a short settle.
  }
  await client.send('Runtime.evaluate', {
    expression: waitForStylesExpression(),
    returnByValue: true,
    awaitPromise: true,
  });
  await sleep(900);
  await client.send('Runtime.evaluate', {
    expression: `document.documentElement.style.scrollBehavior='auto';
      const mobileCheckStyle = document.createElement('style');
      mobileCheckStyle.textContent = '*{transform:none!important;translate:none!important;rotate:none!important;scale:none!important;animation:none!important;transition:none!important} .reveal,.js-ready footer{opacity:1!important}';
      document.head.appendChild(mobileCheckStyle);
      window.scrollTo(0, 0);`,
    returnByValue: true,
  });
  const result = await client.send('Runtime.evaluate', {
    expression: checkExpression(),
    returnByValue: true,
    awaitPromise: true,
  });
  const metrics = result.result.value;

  const shot = await client.send('Page.captureScreenshot', {
    format: 'png',
    captureBeyondViewport: true,
    fromSurface: true,
  });
  const filename = `${viewportLabel}-${slugify(pageLabel)}.png`;
  fs.writeFileSync(path.join(OUT_DIR, filename), Buffer.from(shot.data, 'base64'));
  metrics.screenshot = path.join('.claude', 'responsive-checks', 'screenshots', DATE, filename).replace(/\\/g, '/');
  metrics.pageLabel = pageLabel;
  metrics.route = route;
  metrics.viewportLabel = viewportLabel;
  return metrics;
}

function markdown(results) {
  const lines = [
    `# Mobile render spot-check (${DATE})`,
    '',
    `Base URL: \`${BASE_URL}\`  `,
    `Viewports: ${VIEWPORTS.map(([name, w, h]) => `\`${name} ${w}x${h}\``).join(', ')}  `,
    `Pages checked: ${PAGES.length}`,
    '',
    '## Summary',
    '',
  ];
  const failing = results.filter(r => r.hasHorizontalOverflow);
  lines.push(`- Checked ${results.length} page/viewport combinations.`);
  lines.push(`- Actionable overflow / clipped-element candidates: ${failing.length}.`);
  lines.push('- CSS transforms and animations are neutralised during measurement so intentional entrance animations are not counted as layout defects.');
  lines.push('- Contained code/table overflow means content is inside a scrollable/clipped block, not leaking into the page layout.');
  lines.push(`- Screenshots saved under \`.claude/responsive-checks/screenshots/${DATE}/\`.`);
  lines.push('');
  lines.push('## Results');
  lines.push('');
  lines.push('| Viewport | Page | scrollWidth | Offenders | Contained code/table overflow | Screenshot |');
  lines.push('|---|---|---:|---:|---:|---|');
  for (const r of results) {
    lines.push(`| ${r.viewportLabel} | ${r.pageLabel} | ${r.scrollWidth} | ${r.offenderCount} | ${r.containedOverflowCount} | \`${r.screenshot}\` |`);
  }
  if (failing.length) {
    lines.push('');
    lines.push('## Overflow candidates');
    lines.push('');
    for (const r of failing) {
      lines.push(`### ${r.viewportLabel} / ${r.pageLabel}`);
      for (const o of r.offenders) {
        const name = [o.tag, o.id ? `#${o.id}` : '', o.className ? `.${o.className.split(/\\s+/).filter(Boolean).join('.')}` : ''].join('');
        lines.push(`- \`${name}\` left ${o.left}, right ${o.right}, width ${o.width}${o.transform ? `, transform ${o.transform}` : ''}${o.text ? ` — ${o.text}` : ''}`);
      }
      lines.push('');
    }
  }
  return lines.join('\n') + '\n';
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true });
  fs.mkdirSync(path.dirname(REPORT), { recursive: true });

  const chrome = spawn(CHROME, [
    '--headless=new',
    `--remote-debugging-port=${DEBUG_PORT}`,
    `--user-data-dir=${path.join(ROOT, '.claude', 'responsive-checks', 'chrome-profile')}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-gpu',
    '--hide-scrollbars',
    'about:blank',
  ], { stdio: 'ignore', detached: false });

  try {
    await waitForChrome();
    const target = await requestJson(`http://127.0.0.1:${DEBUG_PORT}/json/new?about:blank`, { method: 'PUT' });
    const client = cdp(target.webSocketDebuggerUrl);
    await client.ready;
    await client.send('Page.enable');
    await client.send('Runtime.enable');

    const results = [];
    for (const viewport of VIEWPORTS) {
      const [viewportLabel, width, height] = viewport;
      for (const [pageLabel, route] of PAGES) {
        process.stdout.write(`Checking ${viewportLabel} ${pageLabel}... `);
        const row = await evaluatePage(client, pageLabel, route, viewportLabel, width, height);
        results.push(row);
        console.log(row.hasHorizontalOverflow ? `overflow candidates=${row.offenderCount}` : 'ok');
      }
    }

    fs.writeFileSync(REPORT, markdown(results), 'utf8');
    console.log(`Wrote ${path.relative(ROOT, REPORT)}`);
    client.close();
  } finally {
    chrome.kill();
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
