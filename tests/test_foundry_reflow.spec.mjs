import { chromium } from "playwright";
import assert from "node:assert/strict";

const base = process.env.BASE_URL || "http://127.0.0.1:5000";
const browser = await chromium.launch({ headless: true });
try {
  for (const width of [320, 390, 768, 1280]) {
    for (const fontSize of [16, 32]) {
      const page = await browser.newPage({ viewport: { width, height: 900 } });
      await page.route("**/*", route => new URL(route.request().url()).origin === new URL(base).origin ? route.continue() : route.abort());
      await page.goto(`${base}/found-ry/`);
      await page.evaluate(size => {
        document.documentElement.style.fontSize = `${size}px`;
        document.body.style.fontSize = `${size}px`;
      }, fontSize);
      const check = async label => {
        const dimensions = await page.evaluate(() => ({
          viewport: innerWidth,
          document: document.documentElement.scrollWidth,
          content: [...document.querySelectorAll("main p, main h1, main h2, main h3, main a, .site-footer a")].filter(e => {
            const rect = e.getBoundingClientRect();
            return rect.width > 0 && (rect.right > innerWidth + 1 || rect.left < -1 || (e.clientWidth > 0 && e.scrollWidth > e.clientWidth + 1));
          }).map(e => e.textContent.trim().slice(0, 70)),
        }));
        assert.ok(dimensions.document <= dimensions.viewport + 1, `${width}px/${fontSize}px ${label}: document overflow`);
        assert.deepEqual(dimensions.content, [], `${width}px/${fontSize}px ${label}: content is clipped`);
      };
      await check("navigation closed");
      const menu = page.locator(".nav-toggle");
      if (await menu.isVisible()) {
        await menu.click();
        await check("navigation open");
        assert.equal(await menu.getAttribute("aria-expanded"), "true");
      }
      console.log(`PASS Found-Ry ${width}px viewport, ${fontSize}px root/body text`);
      await page.close();
    }
  }
} finally {
  await browser.close();
}
