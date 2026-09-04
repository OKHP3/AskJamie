// Mermaid initialization — shared module across overkillhill.com,
// glee-fully.tools, and askjamie.bot.
// Relies on YAML front-matter in each diagram for theme/look (theme: neutral, look: neo).
// initialize() intentionally omits themeVariables to avoid overriding the YAML config.
//
// Performance: on pages with many diagrams (e.g. the v0.3 article) we use
// IntersectionObserver to defer rendering until each diagram approaches the
// viewport. Falls back to immediate render where the API is unavailable.
const diagrams = Array.from(document.querySelectorAll(".mermaid"));
let mermaidPromise = null;

function loadMermaid() {
  if (!mermaidPromise) {
    mermaidPromise = import("/assets/vendor/mermaid/mermaid.esm.min.mjs").then(
      ({ default: mermaid }) => {
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
        return mermaid;
      }
    );
  }
  return mermaidPromise;
}

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

async function renderOne(node) {
  if (node.dataset.mermaidRendered === "1") return;
  node.dataset.mermaidRendered = "1";
  loadMermaid()
    .then((mermaid) => mermaid.run({ nodes: [node] }))
    .then(() => enhanceMermaidLinks(node))
    .catch((err) => {
      console.warn("[mermaid-init] render error:", err);
    });
}

function scheduleRender(node) {
  if (typeof requestIdleCallback === "function") {
    requestIdleCallback(() => renderOne(node), { timeout: 2500 });
  } else {
    setTimeout(() => renderOne(node), 1500);
  }
}

// On small screens the Universe diagram follows a substantial text block and
// is normally below the first viewport. Avoid importing and evaluating the
// large Mermaid bundle until the diagram is actually approached. Desktop
// retains a generous prefetch margin so the side-by-side hero stays seamless.
if (typeof IntersectionObserver === "undefined") {
  diagrams.forEach(scheduleRender);
} else {
  const isSmallScreen =
    typeof matchMedia === "function" && matchMedia("(max-width: 768px)").matches;
  const io = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          scheduleRender(entry.target);
          io.unobserve(entry.target);
        }
      });
    },
    { rootMargin: isSmallScreen ? "0px" : "400px 0px", threshold: 0.01 }
  );
  diagrams.forEach((node) => io.observe(node));
}
