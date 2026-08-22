import { chromium } from "playwright";

const baseUrl = process.env.BASE_URL || "http://127.0.0.1:5000";
const failures = [];

function check(condition, message) {
  if (!condition) failures.push(message);
}

async function waitFor(locator, options, path, description) {
  try {
    await locator.waitFor(options);
  } catch (error) {
    throw new Error(`${path}: ${description}: ${error.message}`);
  }
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext();
const page = await context.newPage();
page.on("requestfailed", (request) => {
  const failure = request.failure();
  if (failure?.errorText === "net::ERR_ABORTED") return;
  failures.push(
    `request failed: ${request.url()}${failure ? ` (${failure.errorText})` : ""}`
  );
});
page.on("console", (message) => {
  if (message.type() === "error") {
    failures.push(`browser console error: ${message.text()}`);
  }
});

try {
  const universePath = "/universe/";
  try {
    await page.goto(`${baseUrl}${universePath}`, { waitUntil: "domcontentloaded" });
  } catch (error) {
    throw new Error(`${universePath}: ${error.message}`);
  }
  await waitFor(page.locator(".askjamie-mermaid-shell svg").first(), {
    state: "attached",
    timeout: 15000,
  }, universePath, "Mermaid SVG did not load");
  check(
    (await page.locator(".askjamie-mermaid-shell svg").count()) > 0,
    "Universe Mermaid diagram did not render an SVG"
  );

  const noJsContext = await browser.newContext({ javaScriptEnabled: false });
  const noJsPage = await noJsContext.newPage();
  await noJsPage.goto(`${baseUrl}${universePath}`, { waitUntil: "domcontentloaded" });
  check(
    await noJsPage.locator(".mermaid-noscript").isVisible(),
    "Universe static fallback is not visible without JavaScript"
  );
  check(
    (await noJsPage.locator('.mermaid-noscript a[href="/contact/"]').count()) === 1,
    "Universe static fallback is missing its contact link"
  );
  await noJsContext.close();

  try {
    await page.goto(baseUrl, { waitUntil: "domcontentloaded" });
  } catch (error) {
    throw new Error("/: " + error.message);
  }
  const searchTrigger = page.locator(".okh-search-trigger");
  await waitFor(searchTrigger, { state: "visible", timeout: 5000 }, "/", "Search trigger unavailable");
  await searchTrigger.click();
  const overlay = page.locator(".okh-search-overlay");
  await waitFor(overlay, { state: "visible", timeout: 5000 }, "/", "Search overlay unavailable");
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
  const aboutPath = "/about/";
  try {
    await page.goto(`${baseUrl}${aboutPath}`, { waitUntil: "domcontentloaded" });
  } catch (error) {
    throw new Error(`${aboutPath}: ${error.message}`);
  }
  const themeToggle = page.locator(".theme-toggle");
  await waitFor(themeToggle, { state: "visible", timeout: 5000 }, aboutPath, "Theme toggle unavailable");
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