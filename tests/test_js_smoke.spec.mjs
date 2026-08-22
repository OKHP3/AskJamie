import { chromium } from "playwright";

const baseUrl = process.env.BASE_URL || "http://127.0.0.1:5000";
const failures = [];

function check(condition, message) {
  if (!condition) failures.push(message);
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext();
const page = await context.newPage();

try {
  await page.goto(`${baseUrl}/universe/`, { waitUntil: "domcontentloaded" });
  await page.locator(".askjamie-mermaid-shell svg").first().waitFor({
    state: "attached",
    timeout: 15000,
  });
  check(
    (await page.locator(".askjamie-mermaid-shell svg").count()) > 0,
    "Universe Mermaid diagram did not render an SVG"
  );

  const noJsContext = await browser.newContext({ javaScriptEnabled: false });
  const noJsPage = await noJsContext.newPage();
  await noJsPage.goto(`${baseUrl}/universe/`, { waitUntil: "domcontentloaded" });
  check(
    await noJsPage.locator(".mermaid-noscript").isVisible(),
    "Universe static fallback is not visible without JavaScript"
  );
  check(
    (await noJsPage.locator('.mermaid-noscript a[href="/contact/"]').count()) === 1,
    "Universe static fallback is missing its contact link"
  );
  await noJsContext.close();

  await page.goto(baseUrl, { waitUntil: "domcontentloaded" });
  const searchTrigger = page.locator(".okh-search-trigger");
  await searchTrigger.waitFor({ state: "visible", timeout: 5000 });
  await searchTrigger.click();
  const overlay = page.locator(".okh-search-overlay");
  await overlay.waitFor({ state: "visible", timeout: 5000 });
  const searchInput = overlay.locator(".okh-search-input");
  await searchInput.fill("BrandGuard");
  check(
    (await searchInput.inputValue()) === "BrandGuard",
    "Search overlay input did not accept keyboard text"
  );
  check(
    (await overlay.getAttribute("data-open")) === "true",
    "Search overlay did not open"
  );
  await page.keyboard.press("Escape");

  await page.addInitScript(() => window.localStorage.setItem("okh-theme", "light"));
  await page.goto(`${baseUrl}/about/`, { waitUntil: "domcontentloaded" });
  const themeToggle = page.locator(".theme-toggle");
  await themeToggle.waitFor({ state: "visible", timeout: 5000 });
  await themeToggle.click();
  check(
    (await page.locator("html").getAttribute("data-theme")) === "dark",
    "Theme toggle did not set data-theme to dark"
  );
} catch (error) {
  failures.push(error.message);
} finally {
  await browser.close();
}

if (failures.length) {
  console.error("JavaScript smoke tests failed:");
  failures.forEach((failure) => console.error(`  - ${failure}`));
  process.exit(1);
}

console.log("JavaScript smoke tests passed: Mermaid, search overlay, and dark mode.");