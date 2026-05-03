/* AskJamie.bot — dedicated /search/ page logic
 * Mirrors the OverKill Hill pattern: hero + big input + category chips + result cards.
 * - Reads /assets/data/search-index.json (shared index used by the overlay too).
 * - Adapts to AskJamie's index shape: { pages: [{url, title, description, section, h1, headings, body}] }.
 *   The `section` field is used as the OKH-style "category".
 * - URL ?q=foo deep-links a query.
 * - Coexists with assets/js/search.js (the overlay) — they share the index but own different DOM.
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
    if (start > 0) snip = "…" + snip;
    if (start + len < body.length) snip += "…";
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
        : "Loading index…";
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
