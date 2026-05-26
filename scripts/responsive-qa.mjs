#!/usr/bin/env node
/**
 * AskJamie™ responsive QA script (Task #1, 2026)
 *
 * Visits each public page at 8 viewport widths and checks:
 *   - No horizontal overflow (scrollWidth > innerWidth)
 *   - No JS console errors
 *   - All images loaded (no broken img src)
 *   - CSS and JS assets load (no 404 on critical resources)
 *
 * Usage:
 *   node scripts/responsive-qa.mjs [--base http://localhost:5000]
 *
 * Requires: playwright (npm install -D playwright && npx playwright install chromium)
 * Falls back to a lightweight static analysis if playwright is not available.
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { resolve, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const __filename = fileURLToPath(import.meta.url);
const __dirname  = dirname(__filename);
const ROOT       = resolve(__dirname, '..');

const BASE_URL   = process.argv.find(a => a.startsWith('--base='))?.split('=')[1]
                 ?? 'http://localhost:5000';

const VIEWPORTS = [
  { name: 'mobile-360',  width: 360,  height: 780  },
  { name: 'mobile-390',  width: 390,  height: 844  },
  { name: 'mobile-430',  width: 430,  height: 932  },
  { name: 'tablet-768',  width: 768,  height: 1024 },
  { name: 'desktop-1024',width: 1024, height: 768  },
  { name: 'desktop-1280',width: 1280, height: 800  },
  { name: 'desktop-1440',width: 1440, height: 900  },
  { name: 'desktop-1920',width: 1920, height: 1080 },
];

const PUBLIC_PATHS = [
  '/',
  '/about/',
  '/contact/',
  '/legal/',
  '/universe/',
  '/search/',
  '/lens-system/',
  '/lens-system/resume-representative/',
  '/lens-system/professional-portfolio/',
  '/lens-system/enterprise-sleuth/',
  '/lens-system/okhp3-brandguard/',
  '/lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/',
  '/lens-system/okhp3-brandguard/lego/',
  '/lens-system/okhp3-brandguard/starbucks/',
  '/lens-system/okhp3-brandguard/brooks-running/',
  '/lens-system/okhp3-brandguard/ping/',
  '/lens-system/okhp3-brandguard/costco/',
  '/lens-system/okhp3-brandguard/hershey/',
  '/lens-system/okhp3-brandguard/lvmh/',
  '/lens-system/okhp3-brandguard/dollar-general/',
  '/lens-system/okhp3-brandguard/coca-cola/',
  '/lens-system/okhp3-brandguard/discount-tire/',
  '/lens-system/okhp3-brandguard/scheels/',
  '/lens-system/okhp3-brandguard/mathews-archery/',
];

const RESULTS_DIR = resolve(ROOT, 'assets/docs/responsive-qa');
const RESULTS_FILE = resolve(RESULTS_DIR, 'results.json');
const SCREENSHOTS_DIR = resolve(RESULTS_DIR, 'screenshots');

async function runWithPlaywright() {
  let pw;
  try {
    const require = createRequire(import.meta.url);
    pw = require('playwright');
  } catch {
    return null; // playwright not available
  }

  mkdirSync(RESULTS_DIR, { recursive: true });
  mkdirSync(SCREENSHOTS_DIR, { recursive: true });

  const browser = await pw.chromium.launch({ headless: true });
  const results = [];
  let totalFails = 0;

  for (const path of PUBLIC_PATHS) {
    for (const vp of VIEWPORTS) {
      const url = BASE_URL + path;
      const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
      const page = await context.newPage();

      const consoleErrors = [];
      page.on('console', msg => { if (msg.type() === 'error') consoleErrors.push(msg.text()); });

      const failed404s = [];
      page.on('response', resp => {
        if (resp.status() === 404 && resp.url().match(/\.(css|js|json)$/)) {
          failed404s.push(resp.url());
        }
      });

      try {
        await page.goto(url, { waitUntil: 'networkidle', timeout: 15000 });
      } catch (err) {
        results.push({ url, viewport: vp.name, pass: false, errors: ['navigation timeout: ' + err.message] });
        totalFails++;
        await context.close();
        continue;
      }

      const overflow = await page.evaluate(() =>
        document.documentElement.scrollWidth > window.innerWidth
      );

      const brokenImages = await page.evaluate(() => {
        const imgs = Array.from(document.querySelectorAll('img'));
        return imgs.filter(i => !i.complete || i.naturalWidth === 0).map(i => i.src);
      });

      const errors = [
        ...(overflow ? [`OVERFLOW: scrollWidth > ${vp.width}px`] : []),
        ...consoleErrors.slice(0, 5).map(e => 'CONSOLE: ' + e),
        ...brokenImages.slice(0, 5).map(s => 'BROKEN IMG: ' + s),
        ...failed404s.slice(0, 5).map(u => '404: ' + u),
      ];

      const pass = errors.length === 0;
      if (!pass) {
        totalFails++;
        const ssFile = `${path.replace(/\//g, '_')}_${vp.name}.png`;
        await page.screenshot({ path: resolve(SCREENSHOTS_DIR, ssFile) });
        console.log(`  FAIL  ${vp.name.padEnd(14)} ${path}`);
        errors.forEach(e => console.log(`         → ${e}`));
      }

      results.push({ url, viewport: vp.name, width: vp.width, pass, errors });
      await context.close();
    }
    process.stdout.write(`  done  ${path}\n`);
  }

  await browser.close();
  writeFileSync(RESULTS_FILE, JSON.stringify({ generated: new Date().toISOString(), base: BASE_URL, results }, null, 2));

  console.log(`\nTotal: ${PUBLIC_PATHS.length * VIEWPORTS.length} checks — ${totalFails} failures`);
  console.log(`Results: ${RESULTS_FILE}`);
  return { results, totalFails };
}

async function staticAnalysis() {
  console.log('Playwright not available — running static HTML analysis instead.\n');
  const { globSync } = await import('fs').then(() => import('glob')).catch(() => null);
  
  const issues = [];
  const htmlFiles = [];

  // Find all public HTML files
  for (const path of PUBLIC_PATHS) {
    const fsPath = resolve(ROOT, path.replace(/^\//, ''), 'index.html');
    if (existsSync(fsPath)) {
      htmlFiles.push({ path, fsPath });
    } else {
      const direct = resolve(ROOT, path.replace(/^\//, '').replace(/\/$/, '') + '.html');
      if (existsSync(direct)) htmlFiles.push({ path, fsPath: direct });
    }
  }

  for (const { path, fsPath } of htmlFiles) {
    const html = readFileSync(fsPath, 'utf-8');

    // Check for imgs missing width/height (layout shift risk on mobile)
    const imgMissingDims = (html.match(/<img(?![^>]*width)[^>]*>/gi) || []).length;
    if (imgMissingDims > 0) {
      issues.push({ page: path, check: 'img-missing-dimensions', count: imgMissingDims });
    }

    // Check for horizontal-scroll risk: fixed-width elements > 320px
    const fixedWidths = (html.match(/width:\s*[4-9]\d{2,}px/gi) || []);
    if (fixedWidths.length > 0) {
      issues.push({ page: path, check: 'fixed-width-risk', samples: fixedWidths.slice(0, 3) });
    }

    // Check viewport meta is present
    if (!html.includes('name="viewport"')) {
      issues.push({ page: path, check: 'missing-viewport-meta', severity: 'critical' });
    }

    // Check for construction-overlay (must be absent)
    if (html.includes('construction-overlay')) {
      issues.push({ page: path, check: 'construction-overlay-present', severity: 'blocker' });
    }
  }

  mkdirSync(RESULTS_DIR, { recursive: true });
  const report = {
    generated: new Date().toISOString(),
    mode: 'static-analysis',
    pages_checked: htmlFiles.length,
    issues
  };
  writeFileSync(RESULTS_FILE, JSON.stringify(report, null, 2));

  console.log(`Static analysis: ${htmlFiles.length} pages checked`);
  console.log(`Issues found: ${issues.length}`);
  issues.forEach(i => console.log(`  [${i.severity || 'warn'}] ${i.page} — ${i.check}`));
  console.log(`Results: ${RESULTS_FILE}`);
  return report;
}

// Main
(async () => {
  console.log('AskJamie™ Responsive QA\n' + '='.repeat(40));
  console.log(`Base URL: ${BASE_URL}`);
  console.log(`Pages: ${PUBLIC_PATHS.length} | Viewports: ${VIEWPORTS.length}\n`);

  const pwResult = await runWithPlaywright();
  if (!pwResult) {
    await staticAnalysis();
  }
})();
