import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";
import test from "node:test";
import {
  assessCaptureReadiness,
  estimateImageScaleRatio,
  validateCaptureDestination,
} from "../scripts/capture-visual-baseline-core.mjs";

test("capture destination safety rejects repository roots and committed baseline replacement", () => {
  assert.throws(
    () =>
      validateCaptureDestination({
        repoRoot: "/repo/askjamie",
        outputDir: "/repo/askjamie",
      }),
    /overwrite the repository root/
  );

  assert.throws(
    () =>
      validateCaptureDestination({
        repoRoot: "/repo/askjamie",
        outputDir: "/repo",
      }),
    /overwrite the repository root or one of its ancestors/
  );

  assert.throws(
    () =>
      validateCaptureDestination({
        repoRoot: "/repo/askjamie",
        outputDir: "/repo/askjamie/assets/audit/visual-baseline",
        outputEntries: ["homepage-1280.png"],
      }),
    /already contains committed visual baselines/
  );

  const safe = validateCaptureDestination({
    repoRoot: "/repo/askjamie",
    outputDir: "/tmp/askjamie-captures",
    reportFile: "/tmp/askjamie-captures/capture-readiness.json",
  });
  assert.equal(safe.outputDir, "/tmp/askjamie-captures");
  assert.equal(safe.reportFile, "/tmp/askjamie-captures/capture-readiness.json");
});

test("capture readiness flags incomplete images, failed requests, and timeout conditions", () => {
  assert.deepEqual(
    assessCaptureReadiness({
      imageCount: 4,
      loadedImages: 4,
      responseErrors: [],
      readinessWaitMs: 75,
      animationSettleMs: 42,
    }),
    { status: "pass", reasons: [] }
  );

  const incomplete = assessCaptureReadiness({
    imageCount: 4,
    loadedImages: 3,
    responseErrors: [],
    readinessWaitMs: 75,
    animationSettleMs: 42,
  });
  assert.equal(incomplete.status, "fail");
  assert.match(incomplete.reasons.join(" | "), /incomplete images: 3\/4/);

  const failed = assessCaptureReadiness({
    imageCount: 4,
    loadedImages: 4,
    responseErrors: [{ url: "/broken.png", status: 404 }],
    readinessWaitMs: 75,
    animationSettleMs: 42,
  });
  assert.equal(failed.status, "fail");
  assert.match(failed.reasons.join(" | "), /failed requests: 1/);

  const timedOut = assessCaptureReadiness({
    imageCount: 4,
    loadedImages: 4,
    responseErrors: [],
    readinessWaitMs: 16001,
    animationSettleMs: 42,
    readinessTimeoutMs: 15000,
  });
  assert.equal(timedOut.status, "fail");
  assert.match(timedOut.reasons.join(" | "), /readiness timeout exceeded/);
});

test("image scale ratio highlights a large source used in a small rendered box", () => {
  assert.equal(estimateImageScaleRatio({ naturalWidth: 1024, renderedWidth: 40 }), 25.6);
  assert.equal(estimateImageScaleRatio({ naturalWidth: 0, renderedWidth: 40 }), null);
});

test("public logo blocks use the nav-only 80px avatar asset", () => {
  const repoRoot = fileURLToPath(new URL("..", import.meta.url));
  const files = execFileSync(
    "rg",
    [
      "--files",
      "-g",
      "*.html",
      ".",
    ],
    { cwd: repoRoot, encoding: "utf8" }
  )
    .trim()
    .split("\n")
    .filter(Boolean)
    .map((file) => file.replace(/^\.\//, ""))
    .filter((file) => {
      return [
        "assets/templates/",
        "about/",
        "contact/",
        "how-askjamie-works/",
        "legal/",
        "lens-system/",
        "search/",
        "universe/",
        "index.html",
      ].some((prefix) => file === prefix || file.startsWith(prefix));
    });

  assert.ok(files.length > 0);
  for (const relative of files) {
    const file = path.join(repoRoot, relative);
    if (!fs.existsSync(file)) {
      continue;
    }
    const text = fs.readFileSync(file, "utf8");
    const match = text.match(/<div class="logo">[\s\S]*?<\/div>/);
    if (!match) {
      continue;
    }
    assert.doesNotMatch(
      match[0],
      /askjamie-avatar-tall-left-square-1024\.png/,
      `nav logo still points at the large avatar in ${relative}`
    );
    assert.match(
      match[0],
      /askjamie-avatar-tall-left-square-80\.png/,
      `nav logo does not use the nav-only avatar in ${relative}`
    );
  }
});
