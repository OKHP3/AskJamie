/* OverKill Hill P3 Universe — Shared Front-End Script
   Source of truth shared by:
     - OverKill Hill        (overkillhill.com)
     - Glee-fully Tools     (glee-fully.tools)
     - AskJamie             (askjamie.bot)

   STRUCTURE
     0. ANALYTICS      — GA4 gtag bootstrap (runs immediately on parse)
     1. GLOBAL         — self-initializing modules
        1a. Site search — modal overlay (keyboard shortcuts, lazy index)
        1b. Site search — dedicated /search/ page (category chips, URL sync)
        1c. Reading progress bar
        1d. Sticky TOC scroll-follow
     2. GLOBAL         — DOM-ready bootstrap (mobile nav, theme, year stamps,
                        scroll reveal, smooth anchor scroll,
                        under-construction overlay)

   No brand-specific JS lives here.  Brand differences are expressed entirely
   through CSS body classes (`.askjamie-main`, `.glee-main`) which the
   scripts below read at runtime to choose the right behavior.
*/

/* ======================================================================
   0. ANALYTICS — GA4 gtag bootstrap
   Replaces the separate analytics.js file.  Runs immediately on script
   parse (same timing as the former `defer` analytics.js tag) so the
   dataLayer queue is ready before the async gtag.js library resolves.
   The gtag.js CDN tag stays in each page's <head> as a separate
   `<script async>` — it must be fetched directly from GTM's CDN.
   ====================================================================== */
window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'G-MT9Y10YY0G');

/* ======================================================================
   1. GLOBAL — self-initializing modules
   ====================================================================== */

/* ── 1a. Site search — modal overlay ────────────────────────────────────
   Zero-dependency, static, client-side.
   - Loads /assets/data/search-index.json on first interaction (lazy).
   - Injects a search button into .site-header and a modal into <body>.
   - Keyboard: "/" or Cmd/Ctrl+K opens, ↑↓ navigates, Enter opens, Esc closes.
   - Highlights matched terms in result snippets.
*/
(function () {
  "use strict";

  var INDEX_URL = "/assets/data/search-index.json";
  var MAX_RESULTS = 10;
  var SNIPPET_RADIUS = 80; // chars on either side of a match

  var indexPromise = null;
  var indexCache = null;
  var modal, input, resultsList, statusEl, openButton;
  var currentResults = [];
  var selectedIndex = -1;

  // ────────────────────────────────────────────────────────────
  // Bootstrap
  // ────────────────────────────────────────────────────────────
  function init() {
    injectButton();
    injectModal();
    bindGlobalShortcuts();
  }

  function injectButton() {
    var header = document.querySelector(".site-header .container");
    if (!header) return;

    openButton = document.createElement("button");
    openButton.type = "button";
    openButton.className = "site-search-trigger";
    openButton.setAttribute("aria-label", "Open search");
    openButton.setAttribute("aria-haspopup", "dialog");
    openButton.innerHTML =
      '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' +
      '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
      '<span class="site-search-trigger-label">Search</span>' +
      '<kbd class="site-search-trigger-kbd" aria-hidden="true">/</kbd>';
    openButton.addEventListener("click", openModal);

    // Insert before the nav-toggle so it sits at the right side of the header
    var navToggle = header.querySelector(".nav-toggle");
    if (navToggle) {
      header.insertBefore(openButton, navToggle);
    } else {
      header.appendChild(openButton);
    }
  }

  function injectModal() {
    modal = document.createElement("div");
    modal.className = "site-search-modal";
    modal.setAttribute("role", "dialog");
    modal.setAttribute("aria-modal", "true");
    modal.setAttribute("aria-labelledby", "site-search-title");
    modal.setAttribute("hidden", "");

    modal.innerHTML =
      '<div class="site-search-scrim" data-search-close></div>' +
      '<div class="site-search-panel">' +
        '<div class="site-search-inputrow">' +
          '<svg class="site-search-icon" viewBox="0 0 24 24" width="20" height="20" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' +
            '<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>' +
          '<input type="search" id="site-search-input" class="site-search-input" ' +
            'placeholder="Search AskJamie\u2122 \u2014 pages, BrandGuard cases, services\u2026" ' +
            'autocomplete="off" autocapitalize="off" spellcheck="false" ' +
            'aria-label="Search the site" aria-controls="site-search-results" />' +
          '<button type="button" class="site-search-close" aria-label="Close search" data-search-close>' +
            '<svg viewBox="0 0 24 24" width="18" height="18" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">' +
            '<path d="M6 6 18 18M18 6 6 18"/></svg>' +
          '</button>' +
        '</div>' +
        '<div class="site-search-status" id="site-search-status" aria-live="polite">' +
          '<span class="site-search-hint">Press <kbd>/</kbd> to focus, <kbd>Esc</kbd> to close. Use <kbd>\u2191</kbd><kbd>\u2193</kbd> to navigate.</span>' +
        '</div>' +
        '<ul class="site-search-results" id="site-search-results" role="listbox" aria-label="Search results"></ul>' +
        '<div class="site-search-footer">' +
          '<span id="site-search-title" class="site-search-title">AskJamie\u2122 Site Search</span>' +
          '<span class="site-search-credit">Static index \u00b7 no tracking</span>' +
        '</div>' +
      '</div>';

    document.body.appendChild(modal);

    input = modal.querySelector("#site-search-input");
    resultsList = modal.querySelector("#site-search-results");
    statusEl = modal.querySelector("#site-search-status");

    // Closers
    modal.querySelectorAll("[data-search-close]").forEach(function (el) {
      el.addEventListener("click", closeModal);
    });

    // Live search
    input.addEventListener("input", function () {
      runSearch(input.value);
    });

    // Keyboard navigation inside modal
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        moveSelection(1);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        moveSelection(-1);
      } else if (e.key === "Enter") {
        if (selectedIndex >= 0 && currentResults[selectedIndex]) {
          e.preventDefault();
          window.location.href = currentResults[selectedIndex].url;
        }
      } else if (e.key === "Escape") {
        e.preventDefault();
        closeModal();
      }
    });

    // Focus trap: keep Tab/Shift-Tab inside the modal
    modal.addEventListener("keydown", function (e) {
      if (e.key !== "Tab") return;
      var focusables = modal.querySelectorAll(
        'a[href], button:not([disabled]), input:not([disabled]), [tabindex]:not([tabindex="-1"])'
      );
      if (focusables.length === 0) return;
      var first = focusables[0];
      var last = focusables[focusables.length - 1];
      var active = document.activeElement;
      if (e.shiftKey) {
        if (active === first || !modal.contains(active)) {
          e.preventDefault();
          last.focus();
        }
      } else {
        if (active === last) {
          e.preventDefault();
          first.focus();
        }
      }
    });
  }

  function bindGlobalShortcuts() {
    document.addEventListener("keydown", function (e) {
      // Skip if user is typing in an input/textarea (unless that input is OUR search input)
      var t = e.target;
      var isTyping =
        t &&
        (t.tagName === "INPUT" || t.tagName === "TEXTAREA" || t.isContentEditable) &&
        t.id !== "site-search-input";

      // On the dedicated /search/ page, defer to the page's own input —
      // don't pop the overlay on top of it.
      var onSearchPage = document.body.classList.contains("search-page");

      // Cmd/Ctrl + K = open
      if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
        if (onSearchPage) {
          var pageInput = document.getElementById("search-page-input");
          if (pageInput) { e.preventDefault(); try { pageInput.focus(); } catch (_) {} return; }
        }
        e.preventDefault();
        openModal();
        return;
      }

      // "/" alone = open (when not typing, and no other overlay is active)
      if (e.key === "/" && !isTyping && !e.metaKey && !e.ctrlKey && !e.altKey) {
        if (isAnotherOverlayOpen()) return;
        if (onSearchPage) {
          var pageInput2 = document.getElementById("search-page-input");
          if (pageInput2) { e.preventDefault(); try { pageInput2.focus(); } catch (_) {} return; }
        }
        if (!modal || modal.hasAttribute("hidden")) {
          e.preventDefault();
          openModal();
        }
      }
    });
  }

  // Detect any other site-level modal/overlay that's currently visible,
  // so the search shortcut doesn't fight with it (e.g. construction overlay).
  function isAnotherOverlayOpen() {
    // Construction overlays have been removed from all pages (Task #1, 2026-05).
    // This guard remains in case future modals are added.
    return false;
  }

  // ────────────────────────────────────────────────────────────
  // Modal open/close
  // ────────────────────────────────────────────────────────────
  function openModal() {
    if (!modal) return;
    modal.removeAttribute("hidden");
    document.body.classList.add("site-search-open");
    if (typeof window._gtag_event === "function") window._gtag_event("search_open", { event_category: "search" });
    // Focus a tick later so the browser actually moves caret
    setTimeout(function () {
      input.focus();
      input.select();
    }, 30);
    ensureIndex().then(function () {
      if (input.value) runSearch(input.value);
    });
  }

  function closeModal() {
    if (!modal) return;
    modal.setAttribute("hidden", "");
    document.body.classList.remove("site-search-open");
    if (openButton) openButton.focus();
  }

  // ────────────────────────────────────────────────────────────
  // Index loading
  // ────────────────────────────────────────────────────────────
  function ensureIndex() {
    if (indexCache) return Promise.resolve(indexCache);
    if (indexPromise) return indexPromise;

    setStatus('<span class="site-search-hint">Loading index\u2026</span>');
    indexPromise = fetch(INDEX_URL, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("HTTP " + r.status);
        return r.json();
      })
      .then(function (data) {
        indexCache = data;
        // Prepare lowercased fields once for fast matching
        indexCache.pages.forEach(function (p) {
          p._titleL = (p.title || "").toLowerCase();
          p._descL = (p.description || "").toLowerCase();
          p._h1L = (p.h1 || "").toLowerCase();
          p._headingsL = (p.headings || []).map(function (h) { return h.toLowerCase(); });
          p._bodyL = (p.body || "").toLowerCase();
          p._sectionL = (p.section || "").toLowerCase();
        });
        setStatus(
          '<span class="site-search-hint">Indexed ' +
            indexCache.count +
            ' pages \u00b7 start typing to search.</span>'
        );
        return indexCache;
      })
      .catch(function (err) {
        indexPromise = null;
        setStatus(
          '<span class="site-search-hint site-search-hint--error">Could not load search index (' +
            err.message +
            ').</span>'
        );
        throw err;
      });
    return indexPromise;
  }

  // ────────────────────────────────────────────────────────────
  // Search
  // ────────────────────────────────────────────────────────────
  function runSearch(query) {
    selectedIndex = -1;
    currentResults = [];

    var q = (query || "").trim().toLowerCase();
    if (!q) {
      resultsList.innerHTML = "";
      setStatus(
        '<span class="site-search-hint">Press <kbd>/</kbd> to focus, <kbd>Esc</kbd> to close. Use <kbd>\u2191</kbd><kbd>\u2193</kbd> to navigate.</span>'
      );
      return;
    }

    if (!indexCache) {
      // Index will trigger us again once loaded
      return;
    }

    if (typeof window._gtag_event === "function") window._gtag_event("search_submit", { event_category: "search", event_label: q.length + " chars" });
    var tokens = q.split(/\s+/).filter(Boolean);
    var phrase = tokens.length > 1 ? q : null;

    var scored = [];
    for (var i = 0; i < indexCache.pages.length; i++) {
      var p = indexCache.pages[i];
      var score = scorePage(p, tokens, phrase);
      if (score > 0) {
        scored.push({ page: p, score: score });
      }
    }

    scored.sort(function (a, b) { return b.score - a.score; });
    scored = scored.slice(0, MAX_RESULTS);

    currentResults = scored.map(function (s) { return s.page; });
    renderResults(scored, tokens);

    if (scored.length === 0) {
      setStatus(
        '<span class="site-search-hint">No matches for \u201c' +
          escapeHtml(query) +
          '\u201d. Try a shorter or different term.</span>'
      );
    } else {
      setStatus(
        '<span class="site-search-hint">' +
          scored.length +
          ' result' +
          (scored.length === 1 ? '' : 's') +
          ' for \u201c' +
          escapeHtml(query) +
          '\u201d</span>'
      );
    }
  }

  function scorePage(p, tokens, phrase) {
    var score = 0;
    var allTokensInTitle = true;
    var allTokensInBody = true;

    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i];
      var inTitle = p._titleL.indexOf(t) >= 0;
      var inH1 = p._h1L.indexOf(t) >= 0;
      var inDesc = p._descL.indexOf(t) >= 0;
      var inSection = p._sectionL.indexOf(t) >= 0;
      var inHeadings = p._headingsL.some(function (h) { return h.indexOf(t) >= 0; });
      var inBody = p._bodyL.indexOf(t) >= 0;

      if (inTitle) score += 10;
      else allTokensInTitle = false;

      if (inH1) score += 8;
      if (inDesc) score += 5;
      if (inSection) score += 3;
      if (inHeadings) score += 4;
      if (inBody) score += 1;
      else allTokensInBody = false;

      // Token MUST appear somewhere or we drop the page entirely
      if (!inTitle && !inH1 && !inDesc && !inSection && !inHeadings && !inBody) {
        return 0;
      }
    }

    if (allTokensInTitle) score += 8;
    if (phrase) {
      if (p._titleL.indexOf(phrase) >= 0) score += 12;
      if (p._h1L.indexOf(phrase) >= 0) score += 6;
      if (p._descL.indexOf(phrase) >= 0) score += 4;
      if (p._bodyL.indexOf(phrase) >= 0) score += 2;
    }

    // Slight boost for shorter URLs (top-of-tree pages tend to be more important)
    var depth = (p.url.match(/\//g) || []).length;
    score += Math.max(0, 4 - depth);

    return score;
  }

  function renderResults(scored, tokens) {
    var html = "";
    for (var i = 0; i < scored.length; i++) {
      var p = scored[i].page;
      var snippet = makeSnippet(p, tokens);
      html +=
        '<li class="site-search-result" role="option" data-idx="' + i + '" id="ssr-' + i + '">' +
          '<a href="' + escapeAttr(p.url) + '" class="site-search-result-link">' +
            '<div class="site-search-result-head">' +
              '<span class="site-search-result-section">' + escapeHtml(p.section || '') + '</span>' +
              '<span class="site-search-result-url">' + escapeHtml(p.url) + '</span>' +
            '</div>' +
            '<div class="site-search-result-title">' + highlight(p.title, tokens) + '</div>' +
            (snippet ? '<div class="site-search-result-snippet">' + snippet + '</div>' : '') +
          '</a>' +
        '</li>';
    }
    resultsList.innerHTML = html;

    // Hover = select
    Array.prototype.forEach.call(resultsList.querySelectorAll(".site-search-result"), function (li, idx) {
      li.addEventListener("mouseenter", function () { setSelection(idx); });
    });
  }

  function makeSnippet(p, tokens) {
    var source = p.description || p.body || "";
    if (!source) return "";

    var lower = source.toLowerCase();
    var pos = -1;
    for (var i = 0; i < tokens.length; i++) {
      var idx = lower.indexOf(tokens[i]);
      if (idx >= 0 && (pos < 0 || idx < pos)) pos = idx;
    }
    if (pos < 0) {
      // No body match — use the description verbatim
      var d = source.slice(0, SNIPPET_RADIUS * 2);
      return highlight(d + (source.length > d.length ? "\u2026" : ""), tokens);
    }

    var start = Math.max(0, pos - SNIPPET_RADIUS);
    var end = Math.min(source.length, pos + SNIPPET_RADIUS * 2);
    var snip = (start > 0 ? "\u2026" : "") + source.slice(start, end) + (end < source.length ? "\u2026" : "");
    return highlight(snip, tokens);
  }

  function highlight(text, tokens) {
    var safe = escapeHtml(text);
    if (!tokens || !tokens.length) return safe;
    // Sort tokens longest first to avoid nested-replacement collisions
    var sorted = tokens.slice().sort(function (a, b) { return b.length - a.length; });
    sorted.forEach(function (t) {
      if (!t) return;
      var re = new RegExp("(" + escapeRegex(t) + ")", "ig");
      safe = safe.replace(re, '<mark class="site-search-mark">$1</mark>');
    });
    return safe;
  }

  // ────────────────────────────────────────────────────────────
  // Keyboard selection
  // ────────────────────────────────────────────────────────────
  function moveSelection(delta) {
    if (currentResults.length === 0) return;
    var next = selectedIndex + delta;
    if (next < 0) next = currentResults.length - 1;
    if (next >= currentResults.length) next = 0;
    setSelection(next);
  }

  function setSelection(idx) {
    var prev = resultsList.querySelector(".site-search-result.is-selected");
    if (prev) prev.classList.remove("is-selected");
    selectedIndex = idx;
    var li = resultsList.querySelector('.site-search-result[data-idx="' + idx + '"]');
    if (li) {
      li.classList.add("is-selected");
      input.setAttribute("aria-activedescendant", "ssr-" + idx);
      // Keep the selected item visible in the scroll viewport
      if (li.scrollIntoView) li.scrollIntoView({ block: "nearest" });
    }
  }

  function setStatus(html) {
    if (statusEl) statusEl.innerHTML = html;
  }

  // ────────────────────────────────────────────────────────────
  // Helpers
  // ────────────────────────────────────────────────────────────
  function escapeHtml(s) {
    return String(s == null ? "" : s)
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#39;");
  }
  function escapeAttr(s) { return escapeHtml(s); }
  function escapeRegex(s) { return String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }

  // ────────────────────────────────────────────────────────────
  // Boot
  // ────────────────────────────────────────────────────────────
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();

/* ── 1b. Site search — dedicated /search/ page ───────────────────────────
   Mirrors the OverKill Hill pattern: hero + big input + category chips +
   result cards.  Gates itself on `.search-page` body class so it is a
   no-op on every other page.  Coexists with the overlay above — they share
   the same index but own entirely different DOM.
*/
(function () {
  "use strict";

  if (!document.body.classList.contains("search-page")) return;

  var INDEX_URL = "/assets/data/search-index.json";

  // -------- index loader (cached) --------
  var _indexPromise = null;
  function loadIndex() {
    if (_indexPromise) return _indexPromise;
    _indexPromise = fetch(INDEX_URL, { credentials: "same-origin" })
      .then(function (r) {
        if (!r.ok) throw new Error("Index fetch failed: " + r.status);
        return r.json();
      })
      .then(function (d) {
        // Accept either OKH shape {entries:[...]} or AskJamie shape {pages:[...]}
        var raw = Array.isArray(d.entries) ? d.entries
                : Array.isArray(d.pages)   ? d.pages
                : [];
        // Normalize so renderer can rely on `category` and consistent strings.
        return raw.map(function (e) {
          return {
            url:         e.url || "",
            title:       e.title || e.h1 || e.url || "",
            description: e.description || "",
            category:    e.category || e.section || "Page",
            headings:    Array.isArray(e.headings) ? e.headings : [],
            body:        e.body || ""
          };
        }).filter(function (e) { return e.url && e.title; });
      })
      .catch(function (err) {
        console.warn("[askjamie-search] index load failed:", err);
        return [];
      });
    return _indexPromise;
  }

  // -------- scoring --------
  function tokenize(q) {
    return q.toLowerCase().split(/[^a-z0-9'-]+/i).filter(function (t) { return t.length >= 2; });
  }
  function scoreEntry(entry, tokens) {
    if (!tokens.length) return 0;
    var title    = (entry.title || "").toLowerCase();
    var desc     = (entry.description || "").toLowerCase();
    var headings = (entry.headings || []).join(" ").toLowerCase();
    var body     = (entry.body || "").toLowerCase();
    var url      = (entry.url || "").toLowerCase();

    var score = 0, allHit = true;
    for (var i = 0; i < tokens.length; i++) {
      var t = tokens[i], hit = 0;
      if (title.indexOf(t)    !== -1) hit += 8;
      if (headings.indexOf(t) !== -1) hit += 5;
      if (desc.indexOf(t)     !== -1) hit += 4;
      if (body.indexOf(t)     !== -1) hit += 2;
      if (url.indexOf(t)      !== -1) hit += 1;
      if (hit === 0) allHit = false;
      score += hit;
    }
    var phrase = tokens.join(" ");
    if (phrase.length > 2) {
      if (title.indexOf(phrase) !== -1) score += 10;
      if (desc.indexOf(phrase)  !== -1) score += 6;
      if (body.indexOf(phrase)  !== -1) score += 4;
    }
    return allHit ? score : score * 0.4;
  }
  function searchEntries(entries, q, limit) {
    var tokens = tokenize(q);
    if (!tokens.length) return [];
    var scored = [];
    for (var i = 0; i < entries.length; i++) {
      var s = scoreEntry(entries[i], tokens);
      if (s > 0) scored.push([s, entries[i]]);
    }
    scored.sort(function (a, b) { return b[0] - a[0]; });
    return scored.slice(0, limit || 60).map(function (p) { return { score: p[0], entry: p[1] }; });
  }

  // -------- snippet + highlight --------
  function escapeHtml(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "\"": "&quot;", "'": "&#39;" })[c];
    });
  }
  function escapeRegex(s) { return String(s).replace(/[.*+?^${}()|[\]\\]/g, "\\$&"); }
  function snippetFor(entry, tokens, length) {
    var body = entry.body || entry.description || "";
    if (!body) return "";
    var lower = body.toLowerCase(), bestIdx = -1;
    for (var i = 0; i < tokens.length; i++) {
      var idx = lower.indexOf(tokens[i]);
      if (idx !== -1 && (bestIdx === -1 || idx < bestIdx)) bestIdx = idx;
    }
    var start = 0, len = length || 220;
    if (bestIdx > 80) start = Math.max(0, bestIdx - 60);
    var snip = body.slice(start, start + len);
    if (start > 0) snip = "\u2026" + snip;
    if (start + len < body.length) snip += "\u2026";
    return snip;
  }
  function highlight(text, tokens) {
    var html = escapeHtml(text);
    if (!tokens.length) return html;
    // Sort tokens longest-first so a shorter token doesn't match inside the
    // <mark> tag of a longer one (e.g. "brand" inside "brandguard").
    var ordered = tokens.slice().sort(function (a, b) { return b.length - a.length; });
    var pattern = ordered.map(escapeRegex).filter(Boolean).join("|");
    if (!pattern) return html;
    return html.replace(new RegExp("(" + pattern + ")", "gi"), "<mark>$1</mark>");
  }

  function renderResultHtml(result, tokens) {
    var e = result.entry;
    var snip = snippetFor(e, tokens, 220);
    return (
      '<div class="ajs-result-meta">' +
        '<span class="ajs-result-cat">' + escapeHtml(e.category || "Page") + "</span>" +
        '<span class="ajs-result-url">' + escapeHtml(e.url) + "</span>" +
      "</div>" +
      '<h3 class="ajs-result-title">' + highlight(e.title || e.url, tokens) + "</h3>" +
      (snip ? '<p class="ajs-result-snippet">' + highlight(snip, tokens) + "</p>" : "")
    );
  }

  // -------- page wiring --------
  var input = document.getElementById("search-page-input");
  var list  = document.getElementById("search-results");
  var stats = document.getElementById("search-stats");
  var cats  = document.getElementById("search-categories");
  if (!input || !list) return;

  var entries = [];
  var activeCategory = "all";

  function readQ() {
    try { return new URL(window.location.href).searchParams.get("q") || ""; }
    catch (e) { return ""; }
  }
  function writeQ(q) {
    try {
      var url = new URL(window.location.href);
      if (q) url.searchParams.set("q", q); else url.searchParams.delete("q");
      window.history.replaceState({}, "", url.toString());
    } catch (e) { /* ignore */ }
  }

  function render() {
    var q = input.value.trim();
    writeQ(q);
    if (!q) {
      list.innerHTML = "";
      if (stats) stats.textContent = entries.length
        ? "Type to search " + entries.length + " indexed entries."
        : "Loading index\u2026";
      return;
    }
    var tokens = tokenize(q);
    var results = searchEntries(entries, q, 60);
    if (activeCategory !== "all") {
      results = results.filter(function (r) {
        return (r.entry.category || "").toLowerCase() === activeCategory.toLowerCase();
      });
    }
    if (!results.length) {
      list.innerHTML =
        '<div class="search-empty-state"><p>No matches for <strong>' +
        escapeHtml(q) + "</strong>" +
        (activeCategory !== "all" ? ' in <em>' + escapeHtml(activeCategory) + "</em>" : "") +
        ".</p></div>";
      if (stats) stats.textContent = "0 results";
      return;
    }
    if (stats) {
      stats.textContent = results.length + " result" + (results.length === 1 ? "" : "s") +
        " for \u201c" + q + "\u201d";
    }
    list.innerHTML = results.map(function (r) {
      return '<a class="ajs-result" href="' + escapeHtml(r.entry.url) + '">' +
             renderResultHtml(r, tokens) + "</a>";
    }).join("");
  }

  function buildCategoryChips() {
    if (!cats) return;
    var counts = {};
    for (var i = 0; i < entries.length; i++) {
      var c = entries[i].category || "Page";
      counts[c] = (counts[c] || 0) + 1;
    }
    var ordered = ["all"].concat(Object.keys(counts).sort());
    cats.innerHTML = ordered.map(function (c) {
      var label = (c === "all")
        ? "All (" + entries.length + ")"
        : c + " (" + counts[c] + ")";
      var pressed = (c === activeCategory) ? "true" : "false";
      return '<button type="button" data-cat="' + escapeHtml(c) +
             '" aria-pressed="' + pressed + '">' + escapeHtml(label) + "</button>";
    }).join("");
    cats.querySelectorAll("button").forEach(function (b) {
      b.addEventListener("click", function () {
        activeCategory = b.getAttribute("data-cat") || "all";
        cats.querySelectorAll("button").forEach(function (x) {
          x.setAttribute("aria-pressed", x === b ? "true" : "false");
        });
        render();
      });
    });
  }

  loadIndex().then(function (d) {
    entries = d;
    buildCategoryChips();
    var initial = readQ();
    if (initial) input.value = initial;
    try { input.focus(); } catch (e) { /* ignore */ }
    render();
  });

  input.addEventListener("input", render);
  input.addEventListener("keydown", function (ev) {
    if (ev.key === "Enter") {
      var first = list.querySelector("a.ajs-result");
      if (first) { ev.preventDefault(); window.location.href = first.getAttribute("href"); }
    } else if (ev.key === "Escape") {
      input.value = "";
      render();
    }
  });
})();

/* ── 1c. Reading progress bar ────────────────────────────────────────────
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

/* ── 1d. Sticky TOC scroll-follow ────────────────────────────────────────
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

/* ── 1e. AskJamie color toggle ────────────────────────────────────────────
   Three-state (light → dark → auto) dark/light mode toggle for the
   .askjamie-main subsite.  Runs immediately (script is at end of <body>
   so DOM is already ready).  Shares the `okh-theme` localStorage key with
   the OKH site so user preference travels across sister sites.

   States stored:
     "light" → explicit light   (html[data-theme="light"])
     "dark"  → explicit dark    (html[data-theme="dark"])
     absent  → auto (system)    (effective theme set from prefers-color-scheme)
*/
(function askjamieColorToggle() {
  "use strict";

  if (!document.body || !document.body.classList.contains("askjamie-main")) return;

  var STORAGE_KEY = "okh-theme";
  var CYCLE  = ["light", "dark", "auto"];
  var LABELS = {
    light: "Switch to dark mode",
    dark:  "Switch to system (auto) mode",
    auto:  "Switch to light mode"
  };

  var ICON_SUN  = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>';
  var ICON_MOON = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
  var ICON_AUTO = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M12 3a9 9 0 1 0 0 18V3z" fill="currentColor"/><circle cx="12" cy="12" r="9"/></svg>';

  function getPreferredTheme() {
    return (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches)
      ? "dark" : "light";
  }

  function getStoredState() {
    var v = localStorage.getItem(STORAGE_KEY);
    if (v === "dark" || v === "light") return v;
    return "auto";
  }

  function applyTheme(state) {
    var effective = (state === "auto") ? getPreferredTheme() : state;
    document.documentElement.setAttribute("data-theme", effective);
    if (state === "auto") {
      localStorage.removeItem(STORAGE_KEY);
    } else {
      localStorage.setItem(STORAGE_KEY, state);
    }
  }

  function iconFor(state) {
    if (state === "dark")  return ICON_MOON;
    if (state === "light") return ICON_SUN;
    return ICON_AUTO;
  }

  // ── Restore stored theme immediately (before first paint) ──────────────
  applyTheme(getStoredState());

  // ── Inject toggle button ───────────────────────────────────────────────
  var container = document.querySelector(".site-header .container");
  if (!container) return;

  var btn = document.createElement("button");
  btn.type = "button";
  btn.className = "askjamie-color-toggle";
  var s0 = getStoredState();
  btn.setAttribute("aria-label", LABELS[s0]);
  btn.innerHTML = iconFor(s0);

  btn.addEventListener("click", function () {
    var cur  = getStoredState();
    var next = CYCLE[(CYCLE.indexOf(cur) + 1) % CYCLE.length];
    applyTheme(next);
    btn.innerHTML = iconFor(next);
    btn.setAttribute("aria-label", LABELS[next]);
  });

  // Re-apply when system preference changes and user is in auto mode
  if (window.matchMedia) {
    window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", function () {
      if (getStoredState() === "auto") applyTheme("auto");
    });
  }

  var navToggle = container.querySelector(".nav-toggle");
  if (navToggle) {
    container.insertBefore(btn, navToggle);
  } else {
    container.appendChild(btn);
  }
})();

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
  // AskJamie has its own 3-state toggle handled by the IIFE above (§1e).
  // Glee is visually committed to its light palette — no toggle there.
  // OKH gets the classic 2-state toggle that persists in localStorage.
  const isGlee     = body.classList.contains("glee-main");
  const isAskJamie = body.classList.contains("askjamie-main");

  if (isGlee) {
    document.documentElement.setAttribute("data-theme", "light");
  } else if (!isAskJamie) {
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

  // ── GA4 custom event tracking ─────────────────────────────────────────────
  // Guard: all calls wrapped in _gtag_event() which checks typeof gtag.
  // Events: cta_click | outbound_click | contact_click |
  //         mermaid_affiliate_click | search_open | search_submit
  // (search_open / search_submit are fired from §1a search module below.)
  function _gtag_event(name, params) {
    if (typeof gtag === "function") gtag("event", name, params);
  }
  // Expose so §1a search module can call it.
  window._gtag_event = _gtag_event;

  // Primary CTA clicks
  document.querySelectorAll(".btn-primary, .btn").forEach(function (el) {
    el.addEventListener("click", function () {
      _gtag_event("cta_click", {
        event_category: "engagement",
        event_label: (el.textContent || "").trim().slice(0, 80),
        link_url: el.getAttribute("href") || ""
      });
    });
  });

  // Outbound link clicks (target=_blank)
  document.querySelectorAll("a[target='_blank']").forEach(function (el) {
    var href = el.getAttribute("href") || "";
    var label = href.indexOf("ko-fi.com")     !== -1 ? "ko-fi"
               : href.indexOf("fiverr.com")   !== -1 ? "fiverr"
               : href.indexOf("chatgpt.com")  !== -1 ? "chatgpt_gpt"
               : href.indexOf("mermaidchart") !== -1 ? "mermaid_affiliate"
               : href.indexOf("linkedin.com") !== -1 ? "linkedin"
               : href.indexOf("youtube.com")  !== -1 ? "youtube"
               : href.indexOf("facebook.com") !== -1 ? "facebook"
               : "outbound";
    var eventName = label === "mermaid_affiliate" ? "mermaid_affiliate_click" : "outbound_click";
    el.addEventListener("click", function () {
      _gtag_event(eventName, {
        event_category: "engagement",
        event_label: label,
        link_url: href
      });
    });
  });

  // Mailto contact clicks
  document.querySelectorAll("a[href^='mailto:']").forEach(function (el) {
    el.addEventListener("click", function () {
      _gtag_event("contact_click", {
        event_category: "engagement",
        event_label: el.getAttribute("href") || ""
      });
    });
  });
});
