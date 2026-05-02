/* OverKill Hill P3 Universe — Shared Front-End Script
   Source of truth shared by:
     - OverKill Hill        (overkillhill.com)
     - Glee-fully Tools     (glee-fully.tools)
     - AskJamie             (askjamie.bot)

   STRUCTURE
     1. GLOBAL — self-initializing modules (run on script parse)
        1a. Site-search lazy loader
        1b. Reading progress bar
        1c. Sticky TOC scroll-follow
     2. GLOBAL — DOM-ready bootstrap (mobile nav, theme, year stamps,
                 scroll reveal, smooth anchor scroll, under-construction overlay)

   No brand-specific JS lives here.  Brand differences are expressed entirely
   through CSS body classes (`.askjamie-main`, `.glee-main`) which the
   scripts below read at runtime to choose the right behaviour
   (e.g. theme toggle is suppressed on subsites; under-construction overlay
   is gated by `.construction-overlay` presence; sticky TOC is gated by
   `#toc-widget` presence).
*/

/* ======================================================================
   1. GLOBAL — self-initializing modules
   ====================================================================== */

/* ── 1a. Site-search lazy loader ─────────────────────────────────────────
   Pulls /assets/js/search.js into <head> exactly once per page.  The
   search module gates itself on a `.search-trigger` element so it's a
   no-op on pages that don't render a trigger.
*/
(function loadSiteSearch() {
  if (window.__askjamieSearchLoaded) return;
  window.__askjamieSearchLoaded = true;
  var s = document.createElement("script");
  s.src = "/assets/js/search.js";
  s.defer = true;
  document.head.appendChild(s);
})();

/* ── 1b. Reading progress bar ────────────────────────────────────────────
   Drives the width of #reading-progress as the user scrolls.  No-op on
   pages that don't render the bar.
*/
(function readingProgress() {
  const bar = document.getElementById("reading-progress");
  if (!bar) return;

  window.addEventListener(
    "scroll",
    function () {
      const scrollTop =
        window.scrollY || document.documentElement.scrollTop;
      const docHeight =
        document.documentElement.scrollHeight -
        document.documentElement.clientHeight;
      const pct = docHeight > 0 ? (scrollTop / docHeight) * 100 : 0;
      bar.style.width = Math.min(pct, 100) + "%";
    },
    { passive: true }
  );
})();

/* ── 1c. Sticky TOC scroll-follow ────────────────────────────────────────
   Smooth-lerp scroll-following for #toc-widget on wide viewports
   (≥1024px).  Stays inside the article column and stops above the
   footer.  No-op on narrow screens or pages without a TOC widget.
*/
(function stickyTOC() {
  if (window.innerWidth < 1024) return;

  var toc    = document.getElementById('toc-widget');
  var footer = document.querySelector('.site-footer');
  if (!toc || !footer) return;

  var lerpedY = 0;
  var targetY = 0;
  var SPEED   = 0.08;
  var NAV_H   = 112;
  var PAD     = 32;

  function lerp(a, b, t) { return a + (b - a) * t; }

  function getNaturalTop(el) {
    var top = 0;
    while (el) { top += el.offsetTop; el = el.offsetParent; }
    return top;
  }

  var tocNaturalTop = getNaturalTop(toc);
  var tocH          = toc.offsetHeight;

  function tick() {
    var scrollY   = window.scrollY;
    var footerTop = footer.offsetTop;

    var centeredOffset = Math.max(NAV_H, (window.innerHeight - tocH) / 2);
    var raw = Math.max(0, scrollY + centeredOffset - tocNaturalTop);
    var max = Math.max(0, footerTop - PAD - tocNaturalTop - tocH);
    targetY = Math.min(raw, max);

    lerpedY = lerp(lerpedY, targetY, SPEED);
    toc.style.transform = 'translateY(' + lerpedY.toFixed(2) + 'px)';

    requestAnimationFrame(tick);
  }

  requestAnimationFrame(tick);

  window.addEventListener('resize', function () {
    toc.style.transform = '';
    if (window.innerWidth >= 1024) {
      tocNaturalTop = getNaturalTop(toc);
      tocH = toc.offsetHeight;
    }
  });
}());

/* ======================================================================
   2. GLOBAL — DOM-ready bootstrap
   ====================================================================== */

document.addEventListener("DOMContentLoaded", () => {
  const header   = document.querySelector(".site-header");
  const navToggle = document.querySelector(".nav-toggle");
  const body     = document.body;
  const yearSpans = document.querySelectorAll(
    "#current-year, #current-year-about, #current-year-manifesto, " +
    "#current-year-projects, #current-year-glee, #current-year-askjamie"
  );

  // ── Mobile nav toggle ────────────────────────────────────────────────
  if (navToggle && header) {
    navToggle.addEventListener("click", () => {
      header.classList.toggle("nav-open");
      const expanded = navToggle.getAttribute("aria-expanded") === "true";
      navToggle.setAttribute("aria-expanded", String(!expanded));
    });
  }

  // ── Header scroll shadow ─────────────────────────────────────────────
  if (header) {
    window.addEventListener("scroll", () => {
      if (window.scrollY > 50) {
        header.classList.add("scrolled");
      } else {
        header.classList.remove("scrolled");
      }
    });
  }

  // ── Year stamps in footer / about / etc. ─────────────────────────────
  const year = new Date().getFullYear();
  yearSpans.forEach((el) => {
    if (el) el.textContent = year;
  });

  // ── Theme toggle ─────────────────────────────────────────────────────
  // Subsites (Glee, AskJamie) are visually committed to their light
  // brand palette — no toggle there.  OKH gets a theme toggle that
  // remembers the user's choice in localStorage under `okh-theme`.
  const brandLocked =
    body.classList.contains("glee-main") ||
    body.classList.contains("askjamie-main");

  if (brandLocked) {
    document.documentElement.setAttribute("data-theme", "light");
  } else {
    const themeToggle = document.createElement("button");
    themeToggle.classList.add("theme-toggle");
    themeToggle.setAttribute("aria-label", "Toggle theme");
    themeToggle.textContent = "🌓";

    if (header && header.querySelector(".container")) {
      header.querySelector(".container").appendChild(themeToggle);
    }

    const savedTheme = localStorage.getItem("okh-theme");
    if (savedTheme === "light" || savedTheme === "dark") {
      document.documentElement.setAttribute("data-theme", savedTheme);
    }

    themeToggle.addEventListener("click", () => {
      const current =
        document.documentElement.getAttribute("data-theme") || "dark";
      const next = current === "dark" ? "light" : "dark";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("okh-theme", next);
    });
  }

  // ── Scroll reveal animations ─────────────────────────────────────────
  const prefersReducedMotion = window.matchMedia(
    "(prefers-reduced-motion: reduce)"
  ).matches;

  if (!prefersReducedMotion && "IntersectionObserver" in window) {
    const revealEls = document.querySelectorAll(".reveal-on-scroll");
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.15 }
    );

    revealEls.forEach((el) => observer.observe(el));
  } else {
    document
      .querySelectorAll(".reveal-on-scroll")
      .forEach((el) => el.classList.add("is-visible"));
  }

  // ── Smooth scroll for internal anchors ───────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    link.addEventListener("click", (e) => {
      const href = link.getAttribute("href");
      if (!href || href === "#") return;
      const target = document.querySelector(href);
      if (!target) return;
      e.preventDefault();
      target.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  // ── Under-construction overlay (Glee + AskJamie work-in-progress) ────
  // Gate: per-page `data-wip-key` lets the user dismiss only one page at
  // a time.  Click the scrim or any [data-wip-dismiss] to dismiss.
  const constructionOverlay = document.querySelector(".construction-overlay");

  if (constructionOverlay) {
    const wipKey =
      constructionOverlay.getAttribute("data-wip-key") ||
      window.location.pathname;
    const storageKey = `glee-wip-dismissed:${wipKey}`;

    // Hide helper — set both `hidden` (the CSS hook in theme.css L1832 keys
    // off `.construction-overlay[hidden]`) and `aria-hidden` (so AT users
    // also see the overlay as removed from the accessibility tree).
    const hideOverlay = () => {
      body.classList.add("construction-dismissed");
      constructionOverlay.setAttribute("hidden", "true");
      constructionOverlay.setAttribute("aria-hidden", "true");
    };

    if (localStorage.getItem(storageKey) === "true") {
      hideOverlay();
    } else {
      const dismissButtons = constructionOverlay.querySelectorAll(
        "[data-wip-dismiss]"
      );

      dismissButtons.forEach((btn) => {
        btn.addEventListener("click", () => {
          hideOverlay();
          localStorage.setItem(storageKey, "true");
        });
      });

      // Clicking the dark scrim (outside the card) also dismisses.
      constructionOverlay.addEventListener("click", (event) => {
        if (event.target === constructionOverlay) {
          const primaryDismiss = constructionOverlay.querySelector(
            "[data-wip-dismiss]"
          );
          if (primaryDismiss) primaryDismiss.click();
        }
      });
    }
  }
});
