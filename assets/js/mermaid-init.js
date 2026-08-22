// Mermaid initialization — shared module across overkillhill.com,
// glee-fully.tools, and askjamie.bot.
// Relies on YAML front-matter in each diagram for theme/look (theme: neutral, look: neo).
// initialize() intentionally omits themeVariables to avoid overriding the YAML config.
//
// Performance: on pages with many diagrams (e.g. the v0.3 article) we use
// IntersectionObserver to defer rendering until each diagram approaches the
// viewport. Falls back to immediate render where the API is unavailable.
import mermaid from "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs";

mermaid.initialize({
  startOnLoad: false,
  securityLevel: "loose",
  flowchart: {
    curve: "basis",
    nodeSpacing: 55,
    rankSpacing: 65,
    htmlLabels: true,
  },
});

const diagrams = Array.from(document.querySelectorAll(".mermaid"));

function enhanceMermaidLinks(node) {
  node.querySelectorAll("svg a").forEach((link) => {
    const href =
      link.getAttribute("href") ||
      link.getAttribute("xlink:href") ||
      link.getAttributeNS("http://www.w3.org/1999/xlink", "href");
    if (href) link.setAttribute("href", href);

    if (link.getAttribute("target") === "_blank") {
      link.setAttribute("rel", "noopener noreferrer");
    }

    const label =
      link.getAttribute("aria-label") ||
      link.querySelector("[title]")?.getAttribute("title") ||
      link.querySelector("title")?.textContent?.trim();
    if (label) link.setAttribute("aria-label", label);
    if (href) link.setAttribute("role", "link");

    // The Universe diagram is an orientation graphic, not a second navigation
    // surface. aria-hidden alone does not remove SVG anchors from Chromium's
    // sequential focus order, so keep generated links visible but unfocusable.
    link.setAttribute("tabindex", "-1");
  });
}

function renderOne(node) {
  if (node.dataset.mermaidRendered === "1") return;
  node.dataset.mermaidRendered = "1";
  mermaid
    .run({ nodes: [node] })
    .then(() => enhanceMermaidLinks(node))
    .catch((err) => {
      console.warn("[mermaid-init] render error:", err);
    });
}

function scheduleRender(node) {
  if (typeof requestIdleCallback === "function") {
    requestIdleCallback(() => renderOne(node), { timeout: 1200 });
  } else {
    setTimeout(() => renderOne(node), 0);
  }
}

// If only a few diagrams, or no IntersectionObserver, render immediately.
if (diagrams.length <= 2 || typeof IntersectionObserver === "undefined") {
  diagrams.forEach(scheduleRender);
} else {
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          scheduleRender(entry.target);
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: "400px 0px", threshold: 0.01 }
  );
  diagrams.forEach((node) => io.observe(node));
}
