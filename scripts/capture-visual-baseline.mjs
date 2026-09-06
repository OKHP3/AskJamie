import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import {
  SAMPLE_ROUTES,
  VIEWPORTS,
  assessCaptureReadiness,
  estimateImageScaleRatio,
  validateCaptureDestination,
} from "./capture-visual-baseline-core.mjs";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");

const baseUrl = process.env.BASE_URL || "http://127.0.0.1:5000";
const outputDir = process.env.OUTPUT_DIR || "assets/audit/visual-baseline";
const reportFile = process.env.REPORT_FILE || path.join(outputDir, "capture-readiness.json");
const baseOrigin = new URL(baseUrl).origin;
const report = {
  baseUrl,
  conditions: {
    cache: "fresh browser context per sample",
    throttle: "none",
    externalRequests: "blocked to same-origin requests",
    samplesPerViewport: SAMPLE_ROUTES.length,
    deviceScaleFactor: 1,
    viewportEmulation: VIEWPORTS.map((viewport) => `${viewport.width}x${viewport.height}`),
  },
  captures: [],
};

await fs.mkdir(outputDir, { recursive: true });
const outputEntries = await fs.readdir(outputDir).catch(() => []);
const validatedTarget = validateCaptureDestination({
  repoRoot: process.cwd(),
  outputDir,
  reportFile,
  committedBaselineDir: path.join(process.cwd(), "assets/audit/visual-baseline"),
  allowCommittedReplacement: process.env.ALLOW_COMMITTED_BASELINE_REPLACEMENT === "1",
  outputEntries,
});

const browser = await chromium.launch({ headless: true });

async function createContext(viewport) {
  const context = await browser.newContext({
    viewport,
    deviceScaleFactor: 1,
    hasTouch: false,
    colorScheme: "light",
    reducedMotion: "no-preference",
  });
  await context.addInitScript(() => {
    window.localStorage.setItem("askjamie-analytics-consent", "denied");
    window.localStorage.setItem("okh-theme", "light");
  });
  await context.route("**/*", (route) => {
    const requestOrigin = new URL(route.request().url()).origin;
    if (requestOrigin === baseOrigin) {
      route.continue();
      return;
    }
    route.abort();
  });
  return context;
}

async function settleAnimations(page) {
  await page.waitForTimeout(150);
  await page.evaluate(async () => {
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  });
}

async function traverseLazyContent(page) {
  await page.evaluate(async () => {
    const step = Math.max(240, Math.floor(window.innerHeight * 0.8));
    const maxScroll = Math.max(document.body.scrollHeight, document.documentElement.scrollHeight);
    for (let position = 0; position <= maxScroll; position += step) {
      window.scrollTo(0, position);
      await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
    }
    window.scrollTo(0, 0);
    await new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve)));
  });
}

async function waitForReadiness(page, selector, routeName, viewportName) {
  const readinessStarted = Date.now();
  await page.waitForLoadState("domcontentloaded");
  await page.waitForLoadState("networkidle");
  await page.waitForFunction(() => document.readyState === "complete", null, { timeout: 15000 });
  await page.evaluate(async () => {
    if (document.fonts?.ready) {
      try {
        await document.fonts.ready;
      } catch {
        // Continue when a font promise is rejected or unsupported.
      }
    }
  });
  await traverseLazyContent(page);
  const animationSettleStarted = Date.now();
  await settleAnimations(page);
  await page.waitForFunction(() => {
    const reveals = [...document.querySelectorAll(".reveal-on-scroll")];
    return reveals.every((element) => getComputedStyle(element).opacity === "1");
  }, null, { timeout: 15000 });
  const animationSettleMs = Date.now() - animationSettleStarted;

  const target = page.locator(selector).first();
  try {
    await target.waitFor({ state: "visible", timeout: 15000 });
  } catch (error) {
    const diagnostics = await page.evaluate((routeNameValue) => {
      const images = [...document.images].map((image) => ({
        src: image.currentSrc || image.src,
        alt: image.alt || "",
        complete: image.complete,
        naturalWidth: image.naturalWidth,
        naturalHeight: image.naturalHeight,
        renderedWidth: Number(image.getBoundingClientRect().width.toFixed(1)),
        renderedHeight: Number(image.getBoundingClientRect().height.toFixed(1)),
        scaleRatio: Number((image.naturalWidth / Math.max(1, image.getBoundingClientRect().width)).toFixed(2)),
        loading: image.loading || "eager",
      }));
      const resources = performance.getEntriesByType("resource").map((entry) => ({
        name: entry.name,
        initiatorType: entry.initiatorType,
        duration: Number(entry.duration.toFixed(1)),
        transferSize: entry.transferSize,
        encodedBodySize: entry.encodedBodySize,
      }));
      return {
        route: routeNameValue,
        readyState: document.readyState,
        title: document.title,
        scrollHeight: document.documentElement.scrollHeight,
        imageCount: images.length,
        loadedImages: images.filter((image) => image.complete && image.naturalWidth > 0).length,
        requestBytes: {
          transferred: resources.reduce((sum, entry) => sum + (entry.transferSize || 0), 0),
          encoded: resources.reduce((sum, entry) => sum + (entry.encodedBodySize || 0), 0),
        },
        revealCount: document.querySelectorAll(".reveal-on-scroll").length,
        visibleReveals: [...document.querySelectorAll(".reveal-on-scroll")].filter((element) => getComputedStyle(element).opacity === "1").length,
        resourceSummary: resources.reduce((summary, entry) => {
          summary[entry.initiatorType] = (summary[entry.initiatorType] || 0) + 1;
          return summary;
        }, {}),
        resourceSample: resources.slice(0, 8),
        imageSample: images.slice(0, 8),
      };
    }, routeName);
    throw new Error(
      `Readiness failed for ${routeName} at ${viewportName} while waiting for ${selector}: ${error.message}\n${JSON.stringify(diagnostics, null, 2)}`
    );
  }

  await target.evaluate((element) => {
    element.scrollIntoView({ block: "center", inline: "nearest" });
  });
  await settleAnimations(page);
  return {
    readinessWaitMs: Date.now() - readinessStarted,
    animationSettleMs,
  };
}

async function summarizeRequests(page) {
  return page.evaluate(() => {
    const resources = performance.getEntriesByType("resource").map((entry) => ({
      name: entry.name,
      initiatorType: entry.initiatorType,
      duration: Number(entry.duration.toFixed(1)),
      transferSize: entry.transferSize,
      encodedBodySize: entry.encodedBodySize,
    }));
    const images = [...document.images].map((image) => ({
      ...({
        src: image.currentSrc || image.src,
        alt: image.alt || "",
        complete: image.complete,
        naturalWidth: image.naturalWidth,
        naturalHeight: image.naturalHeight,
        renderedWidth: Number(image.getBoundingClientRect().width.toFixed(1)),
        renderedHeight: Number(image.getBoundingClientRect().height.toFixed(1)),
        loading: image.loading || "eager",
        fetchPriority: image.fetchPriority || "auto",
      }),
    }));
    return {
      readyState: document.readyState,
      title: document.title,
      imageCount: images.length,
      loadedImages: images.filter((image) => image.complete && image.naturalWidth > 0).length,
      lazyImages: images.filter((image) => image.loading === "lazy").length,
      resourceSummary: resources.reduce((summary, entry) => {
        summary[entry.initiatorType] = (summary[entry.initiatorType] || 0) + 1;
        return summary;
      }, {}),
      requestBytes: {
        transferred: resources.reduce((sum, entry) => sum + (entry.transferSize || 0), 0),
        encoded: resources.reduce((sum, entry) => sum + (entry.encodedBodySize || 0), 0),
      },
      resourceSample: resources.slice(0, 12),
      imageSample: images.slice(0, 12),
      revealCount: document.querySelectorAll(".reveal-on-scroll").length,
      visibleReveals: [...document.querySelectorAll(".reveal-on-scroll")].filter((element) => getComputedStyle(element).opacity === "1").length,
    };
  });
}

async function captureSample(viewport, sample) {
  const context = await createContext(viewport);
  const page = await context.newPage();
  const requests = [];
  const responses = [];
  page.on("request", (request) => {
    requests.push({
      url: request.url(),
      resourceType: request.resourceType(),
    });
  });
  page.on("response", (response) => {
    if (!response.ok()) {
      responses.push({
        url: response.url(),
        status: response.status(),
      });
    }
  });

  const captureBase = `${sample.name}-${viewport.width}`;
  try {
    await page.goto(`${baseUrl}${sample.route}`, { waitUntil: "domcontentloaded" });
    const readinessTiming = await waitForReadiness(
      page,
      sample.focusSelector,
      sample.name,
      `${viewport.width}x${viewport.height}`
    );

    const captureTarget = page.locator(sample.captureSelector).first();
    await captureTarget.screenshot({
      path: `${outputDir}/${captureBase}.png`,
      animations: "disabled",
      caret: "hide",
    });
    if (sample.focusSelector !== sample.captureSelector) {
      await page.locator(sample.focusSelector).first().screenshot({
        path: `${outputDir}/${captureBase}-focus.png`,
        animations: "disabled",
        caret: "hide",
      });
    }
    const sampleSummary = await summarizeRequests(page);
    sampleSummary.readinessWaitMs = readinessTiming.readinessWaitMs;
    sampleSummary.animationSettleMs = readinessTiming.animationSettleMs;
    sampleSummary.imageSample = sampleSummary.imageSample.map((image) => ({
      ...image,
      scaleRatio: estimateImageScaleRatio(image),
    }));

    report.captures.push({
      route: sample.route,
      name: sample.name,
      viewport: `${viewport.width}x${viewport.height}`,
      screenshot: `${captureBase}.png`,
      focusScreenshot: sample.focusSelector !== sample.captureSelector ? `${captureBase}-focus.png` : null,
      readiness: assessCaptureReadiness({
        imageCount: sampleSummary.imageCount,
        loadedImages: sampleSummary.loadedImages,
        responseErrors: responses,
        readinessWaitMs: sampleSummary.readinessWaitMs,
        animationSettleMs: sampleSummary.animationSettleMs,
      }),
      requestCount: requests.length,
      responseErrors: responses,
      requestSummary: requests.reduce((summary, request) => {
        summary[request.resourceType] = (summary[request.resourceType] || 0) + 1;
        return summary;
      }, {}),
      requestSample: requests.slice(0, 12),
      pageSummary: sampleSummary,
    });
  } catch (error) {
    const failurePath = `${outputDir}/${captureBase}-failure.png`;
    await page.screenshot({ path: failurePath, fullPage: true });
    const diagnostics = {
      route: sample.route,
      name: sample.name,
      viewport: `${viewport.width}x${viewport.height}`,
      error: error.message,
      screenshot: failurePath,
      requestCount: requests.length,
      responseErrors: responses,
      requestSample: requests.slice(0, 12),
      pageSummary: await summarizeRequests(page),
    };
    await fs.writeFile(`${outputDir}/${captureBase}-failure.json`, `${JSON.stringify(diagnostics, null, 2)}\n`);
    throw new Error(`${error.message}\n${JSON.stringify(diagnostics, null, 2)}`);
  } finally {
    await page.close();
    await context.close();
  }
}

for (const viewport of VIEWPORTS) {
  for (const sample of SAMPLE_ROUTES) {
    await captureSample(viewport, sample);
  }
}

await browser.close();
await fs.writeFile(validatedTarget.reportFile, `${JSON.stringify(report, null, 2)}\n`);
console.log(`Visual baseline captured in ${validatedTarget.outputDir}`);
console.log(`Readiness summary written to ${validatedTarget.reportFile}`);
