import { chromium } from "playwright";
import fs from "node:fs/promises";

const baseUrl = process.env.BASE_URL || "http://127.0.0.1:5000";
const outputDir = process.env.OUTPUT_DIR || "assets/audit/visual-baseline";
const viewports = [
  { name: "desktop", width: 1280, height: 900 },
  { name: "mobile", width: 390, height: 844 },
];

await fs.mkdir(outputDir, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext();
await context.addInitScript(() => {
  window.localStorage.setItem("askjamie-analytics-consent", "denied");
  window.localStorage.setItem("okh-theme", "light");
});

async function capturePage(path, selector, filename, viewport) {
  const page = await context.newPage();
  await page.setViewportSize(viewport);
  await page.goto(`${baseUrl}${path}`, { waitUntil: "networkidle" });
  const target = page.locator(selector).first();
  await target.waitFor({ state: "visible", timeout: 15000 });
  await target.scrollIntoViewIfNeeded();
  await target.screenshot({ path: `${outputDir}/${filename}-${viewport.width}.png` });
  await page.close();
}

for (const viewport of viewports) {
  await capturePage("/", "body", `homepage-full-${viewport.name}`, viewport);
  await capturePage("/", ".askjamie-hero", `homepage-hero-${viewport.name}`, viewport);
  await capturePage(
    "/lens-system/okhp3-brandguard/",
    ".brandguard-case-card",
    `brandguard-card-${viewport.name}`,
    viewport
  );
  const page = await context.newPage();
  await page.setViewportSize(viewport);
  await page.goto(`${baseUrl}/universe/`, { waitUntil: "networkidle" });
  const diagram = page.locator(".askjamie-mermaid-shell");
  await diagram.scrollIntoViewIfNeeded();
  await diagram.locator("svg").first().waitFor({ state: "visible", timeout: 20000 });
  await diagram.screenshot({
    path: `${outputDir}/universe-diagram-${viewport.name}-${viewport.width}.png`,
  });
  await page.close();
}

await browser.close();
console.log(`Visual baseline captured in ${outputDir}`);