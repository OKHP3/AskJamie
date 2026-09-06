import { chromium } from "playwright";
import assert from "node:assert/strict";
import fs from "node:fs/promises";

const base = process.env.BASE_URL || "http://127.0.0.1:5000";
const browser = await chromium.launch({ headless: true });
try {
  const report = await (await fetch(`${base}/assets/data/universe-map.json`)).json();
  for (const width of [390, 1280]) {
    for (const theme of ["light", "dark"]) {
      const page = await browser.newPage({ viewport: { width, height: 900 }, colorScheme: theme });
      const errors = [];
      page.on("pageerror", error => errors.push(error.message));
      page.on("console", message => { if (/render error/i.test(message.text())) errors.push(message.text()); });
      await page.addInitScript(value => localStorage.setItem("askjamie-color-scheme", value), theme);
      await page.goto(`${base}/universe/`);
      const groups = page.locator(".universe-map-group");
      assert.equal(await groups.count(), report.diagrams.length);
      for (let i = 0; i < await groups.count(); i++) {
        const group = groups.nth(i);
        await group.locator("summary").click();
        await group.locator(".mermaid").scrollIntoViewIfNeeded();
        await group.locator("svg .node").first().waitFor({ timeout: 20000 });
        await page.waitForFunction(element => element.querySelectorAll("svg a[href]").length === element.querySelectorAll("a[data-universe-node]").length, await group.elementHandle());
        assert.equal(await group.locator("svg .node").count(), report.diagrams[i].nodes.length);
        const labels = await group.locator(".nodeLabel").allTextContents();
        const expectedLabels = report.diagrams[i].nodes.map(id => {
          const node = report.nodes.find(item => item.id === id);
          return `${node.title} (${node.status})`.replace(/\s+/g, " ").trim();
        });
        assert.deepEqual(labels.map(value => value.replace(/\s+/g, " ").trim()).sort(), expectedLabels.sort(), "Mermaid must decode titles and symbols exactly");
        const colors = await group.locator(".nodeLabel p").first().evaluate(e => [getComputedStyle(e).color, getComputedStyle(e.closest(".node").querySelector("rect")).fill]);
        assert.notEqual(colors[0], "rgb(0, 0, 0)", "Node text must use the brand foreground");
        assert.notEqual(colors[0], colors[1], "Node text must differ from its surface");
        assert.equal(await group.locator("svg a[href^='/']").count(), report.diagrams[i].nodes.length);
        if (i === 0 && process.env.OUTPUT_DIR) {
          await fs.mkdir(process.env.OUTPUT_DIR, { recursive: true });
          await group.screenshot({ path: `${process.env.OUTPUT_DIR}/universe-detail-${width}-${theme}.png` });
        }
        await group.locator("summary").click();
      }
      const urls = await page.locator("a[data-universe-node]").evaluateAll(links => [...new Set(links.map(link => link.href.replace(location.origin, "https://askjamie.bot")))].sort());
      assert.deepEqual(urls, report.nodes.filter(node => node.indexed).map(node => node.url).sort());
      assert.ok(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), "Page overflows viewport");
      assert.deepEqual(errors, []);
      await page.close();
    }
  }
  const noJs = await browser.newPage({ javaScriptEnabled: false });
  await noJs.goto(`${base}/universe/`);
  await noJs.locator(".universe-map-group summary").first().click();
  assert.ok(await noJs.locator(".universe-map-group[open] a[data-universe-node]").first().isVisible());
  assert.equal(await noJs.locator(".universe-map-group[open] .mermaid").first().evaluate(e => getComputedStyle(e).visibility), "hidden", "Raw diagram syntax must stay hidden without JavaScript");
  await noJs.locator(".universe-map-group[open] .mermaid").first().evaluate(e => e.setAttribute("data-processed", "true"));
  assert.equal(await noJs.locator(".universe-map-group[open] .mermaid").first().evaluate(e => getComputedStyle(e).visibility), "hidden", "Mermaid's early processed flag must not expose source before SVG insertion");
  const keyboard = await browser.newPage();
  await keyboard.goto(`${base}/universe/`);
  await keyboard.locator(".universe-map-group summary").first().focus();
  await keyboard.keyboard.press("Enter");
  assert.equal(await keyboard.locator(".universe-map-group[open]").count(), 1);
  console.log(`Universe browser checks passed: ${report.nodes.length} indexed pages, ${report.diagrams.length} diagrams, two widths, both themes, keyboard and no-JavaScript links.`);
} finally {
  await browser.close();
}
