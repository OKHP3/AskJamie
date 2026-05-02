/* AskJamie.bot — internal site search
 * Zero-dependency, static, client-side.
 * - Loads /assets/data/search-index.json on first interaction (lazy).
 * - Injects a search button into .site-header and a modal into <body>.
 * - Keyboard: "/" or Cmd/Ctrl+K opens, ↑↓ navigates, Enter opens, Esc closes.
 * - Highlights matched terms in result snippets.
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
            'placeholder="Search AskJamie\u2122 — pages, BrandGuard cases, services\u2026" ' +
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

      // Cmd/Ctrl + K = open
      if ((e.metaKey || e.ctrlKey) && (e.key === "k" || e.key === "K")) {
        e.preventDefault();
        openModal();
        return;
      }

      // "/" alone = open (when not typing, and no other overlay is active)
      if (e.key === "/" && !isTyping && !e.metaKey && !e.ctrlKey && !e.altKey) {
        if (isAnotherOverlayOpen()) return;
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
    var overlay = document.querySelector(".construction-overlay");
    if (overlay && !overlay.hasAttribute("hidden")) {
      var dismissed = document.body.classList.contains("construction-dismissed");
      if (!dismissed) return true;
    }
    return false;
  }

  // ────────────────────────────────────────────────────────────
  // Modal open/close
  // ────────────────────────────────────────────────────────────
  function openModal() {
    if (!modal) return;
    modal.removeAttribute("hidden");
    document.body.classList.add("site-search-open");
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
