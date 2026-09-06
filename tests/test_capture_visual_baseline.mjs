import assert from "node:assert/strict";
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
