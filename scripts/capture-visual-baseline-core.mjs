import path from "node:path";

export const DEFAULT_OUTPUT_DIR = "assets/audit/visual-baseline";
export const DEFAULT_REPORT_FILE = "capture-readiness.json";
export const READINESS_TIMEOUT_MS = 15000;

export const VIEWPORTS = [
  { name: "desktop", width: 1280, height: 900 },
  { name: "mobile", width: 390, height: 844 },
];

export const SAMPLE_ROUTES = [
  {
    name: "homepage",
    route: "/",
    captureSelector: "body",
    focusSelector: ".askjamie-hero",
  },
  {
    name: "lens-hub",
    route: "/lens-system/",
    captureSelector: "body",
    focusSelector: ".askjamie-hero",
  },
  {
    name: "brandguard-detail",
    route: "/lens-system/okhp3-brandguard/bfs-framing-intelligent-futures/",
    captureSelector: "body",
    focusSelector: ".askjamie-hero",
  },
  {
    name: "universe",
    route: "/universe/",
    captureSelector: "body",
    focusSelector: ".askjamie-mermaid-shell",
  },
];

export function isSameOrAncestor(candidateParent, candidateChild) {
  const relative = path.relative(candidateParent, candidateChild);
  return relative === "" || (!relative.startsWith("..") && !path.isAbsolute(relative));
}

export function validateCaptureDestination({
  repoRoot,
  outputDir,
  reportFile = path.join(outputDir, DEFAULT_REPORT_FILE),
  committedBaselineDir = path.join(repoRoot, DEFAULT_OUTPUT_DIR),
  allowCommittedReplacement = false,
  outputEntries = [],
} = {}) {
  if (!repoRoot || !outputDir) {
    throw new Error("repoRoot and outputDir are required");
  }

  const normalizedRepoRoot = path.resolve(repoRoot);
  const normalizedOutputDir = path.resolve(outputDir);
  const normalizedReportFile = path.resolve(reportFile);
  const normalizedCommittedBaselineDir = path.resolve(committedBaselineDir);

  if (isSameOrAncestor(normalizedOutputDir, normalizedRepoRoot)) {
    throw new Error(
      `Output directory ${normalizedOutputDir} would overwrite the repository root or one of its ancestors`
    );
  }

  if (
    normalizedOutputDir === normalizedCommittedBaselineDir &&
    outputEntries.length > 0 &&
    !allowCommittedReplacement
  ) {
    throw new Error(
      `Output directory ${normalizedOutputDir} already contains committed visual baselines; set allowCommittedReplacement to replace them intentionally`
    );
  }

  return {
    repoRoot: normalizedRepoRoot,
    outputDir: normalizedOutputDir,
    reportFile: normalizedReportFile,
    committedBaselineDir: normalizedCommittedBaselineDir,
    allowCommittedReplacement,
  };
}

export function assessCaptureReadiness({
  imageCount = 0,
  loadedImages = 0,
  responseErrors = [],
  readinessWaitMs = 0,
  animationSettleMs = 0,
  readinessTimeoutMs = READINESS_TIMEOUT_MS,
}) {
  const reasons = [];
  if (responseErrors.length > 0) {
    reasons.push(`failed requests: ${responseErrors.length}`);
  }
  if (imageCount > loadedImages) {
    reasons.push(`incomplete images: ${loadedImages}/${imageCount}`);
  }
  if (readinessWaitMs > readinessTimeoutMs) {
    reasons.push(`readiness timeout exceeded: ${Math.round(readinessWaitMs)}ms`);
  }
  if (animationSettleMs > readinessTimeoutMs) {
    reasons.push(`animation settle timeout exceeded: ${Math.round(animationSettleMs)}ms`);
  }
  return {
    status: reasons.length > 0 ? "fail" : "pass",
    reasons,
  };
}

export function estimateImageScaleRatio({ naturalWidth = 0, renderedWidth = 0 }) {
  if (!naturalWidth || !renderedWidth) {
    return null;
  }
  return Number((naturalWidth / renderedWidth).toFixed(2));
}

export function summarizeImageMetrics(image) {
  const rect = image.getBoundingClientRect();
  return {
    src: image.currentSrc || image.src,
    complete: image.complete,
    naturalWidth: image.naturalWidth,
    naturalHeight: image.naturalHeight,
    renderedWidth: Number(rect.width.toFixed(1)),
    renderedHeight: Number(rect.height.toFixed(1)),
    scaleRatio: estimateImageScaleRatio({
      naturalWidth: image.naturalWidth,
      renderedWidth: rect.width,
    }),
    loading: image.loading || "eager",
    fetchPriority: image.fetchPriority || "auto",
  };
}
