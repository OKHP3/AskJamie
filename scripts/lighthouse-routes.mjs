#!/usr/bin/env node
/**
 * Run the same Lighthouse pass against the four public routes and compare the
 * compact results with the committed 2026-08-22 baseline.
 *
 * The static server is intentionally kept separate so this command can be
 * used against the Replit preview, a local server, or a hosted preview:
 *
 *   node scripts/lighthouse-routes.mjs
 *   node scripts/lighthouse-routes.mjs --preset=mobile
 *   node scripts/lighthouse-routes.mjs --preset=mobile --controlled
 *   node scripts/lighthouse-routes.mjs --base-url=https://askjamie.bot
 */
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";
import { execFileSync } from "node:child_process";

const root = resolve(import.meta.dirname, "..");
const baselinePath = resolve(root, "assets/audit/lighthouse-baseline-2026-08-22.json");
const defaultBaseUrl = process.env.LIGHTHOUSE_BASE_URL || "http://127.0.0.1:5000";
const baseUrlArg = process.argv.find((arg) => arg.startsWith("--base-url="));
const baseUrl = (baseUrlArg ? baseUrlArg.slice("--base-url=".length) : defaultBaseUrl).replace(/\/+$/, "");
const presetArg = process.argv.find((arg) => arg.startsWith("--preset="));
const preset = presetArg ? presetArg.slice("--preset=".length) : "desktop";
if (!["desktop", "mobile"].includes(preset)) {
  console.error(`Unsupported Lighthouse preset: ${preset}. Use desktop or mobile.`);
  process.exit(1);
}
const dateArg = process.argv.find((arg) => arg.startsWith("--date="));
const date = dateArg ? dateArg.slice("--date=".length) : new Date().toISOString().slice(0, 10);
const controlled = process.argv.includes("--controlled");
if (controlled && preset !== "mobile") {
  console.error("The controlled third-party isolation mode is only supported with --preset=mobile.");
  process.exit(1);
}
const outputSuffix = `${preset === "mobile" ? "-mobile" : ""}${controlled ? "-controlled" : ""}`;
const outputDir = resolve(root, "assets/audit", `lighthouse-${date}${outputSuffix}`);
const routes = {
  homepage: "/",
  brandguard: "/lens-system/okhp3-brandguard/",
  universe: "/universe/",
  search: "/search/",
};
const baseline = JSON.parse(readFileSync(baselinePath, "utf8"));
const lighthouseBin = resolve(root, "node_modules/.bin/lighthouse");
const controlledBlockedUrlPatterns = [
  "https://fonts.googleapis.com/*",
  "https://fonts.gstatic.com/*",
  "https://www.googletagmanager.com/*",
  "https://www.google-analytics.com/*",
  "https://*.google-analytics.com/*",
];
const chromePath = process.env.CHROME_PATH || (() => {
  try {
    return execFileSync(process.execPath, ["-e", "process.stdout.write(require('playwright').chromium.executablePath())"], {
      cwd: root,
      encoding: "utf8",
    }).trim();
  } catch {
    return "";
  }
})();

if (!existsSync(lighthouseBin)) {
  console.error("Lighthouse is not installed. Run: npm install");
  process.exit(1);
}
if (!chromePath) {
  console.error("Chromium was not found. Set CHROME_PATH or install Playwright browsers.");
  process.exit(1);
}

mkdirSync(outputDir, { recursive: true });
const summary = {
  schemaVersion: 1,
  capturedAt: date,
  tool: "Lighthouse 12.8.2",
  environment: controlled
    ? "Local or supplied static server, controlled mobile preset"
    : `Local or supplied static server, ${preset} preset`,
  property: baseUrl,
  baseline: "assets/audit/lighthouse-baseline-2026-08-22.json",
  controls: controlled
    ? {
        thirdPartyFonts: "blocked",
        analytics: "blocked",
        interpretation: "Controlled lab measurement only. Not field data.",
      }
    : {
        thirdPartyFonts: "in flight",
        analytics: "in flight",
        interpretation: "No third-party isolation applied.",
      },
  pages: {},
};

for (const [name, path] of Object.entries(routes)) {
  const reportPath = resolve(outputDir, `${name}.json`);
  const url = `${baseUrl}${path}`;
  console.log(`Running ${name}: ${url}`);
  execFileSync(lighthouseBin, [
    url,
    "--output=json",
    `--output-path=${reportPath}`,
    ...(preset === "desktop" ? ["--preset=desktop"] : ["--form-factor=mobile"]),
    ...(controlled
      ? controlledBlockedUrlPatterns.map((pattern) => `--blocked-url-patterns=${pattern}`)
      : []),
    "--chrome-flags=--headless --no-sandbox --disable-dev-shm-usage",
    "--quiet",
  ], { cwd: root, stdio: "inherit", env: { ...process.env, CHROME_PATH: chromePath } });

  const report = JSON.parse(readFileSync(reportPath, "utf8"));
  const audits = report.audits;
  const page = baseline.pages[name] || {};
  const metric = (id) => audits[id]?.numericValue ?? null;
  const lcpElement = audits["largest-contentful-paint-element"]?.details?.items?.[0]?.items?.[0]?.node;
  summary.pages[name] = {
    path,
    performance: Math.round((report.categories.performance?.score || 0) * 100),
    accessibility: Math.round((report.categories.accessibility?.score || 0) * 100),
    bestPractices: Math.round((report.categories["best-practices"]?.score || 0) * 100),
    seo: Math.round((report.categories.seo?.score || 0) * 100),
    lcpMs: Math.round(metric("largest-contentful-paint")),
    cls: Number(metric("cumulative-layout-shift")?.toFixed(6)),
    tbtMs: Math.round(metric("total-blocking-time")),
    fcpMs: Math.round(metric("first-contentful-paint")),
    lcpElement: lcpElement?.selector || null,
    deltaPerformance: Math.round((report.categories.performance?.score || 0) * 100) - (page.performance ?? 0),
    deltaLcpMs: Math.round(metric("largest-contentful-paint")) - (page.lcpMs ?? 0),
  };
}

const summaryPath = resolve(outputDir, "summary.json");
writeFileSync(summaryPath, `${JSON.stringify(summary, null, 2)}\n`);
console.log(`\nWrote ${summaryPath}`);
console.table(Object.fromEntries(Object.entries(summary.pages).map(([name, page]) => [
  name,
  { performance: page.performance, delta: page.deltaPerformance, lcpMs: page.lcpMs, deltaLcpMs: page.deltaLcpMs, cls: page.cls, tbtMs: page.tbtMs },
])));