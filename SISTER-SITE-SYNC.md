# Sister-Site Sync Guide — v0.9 (2026-05-26)

Precise, copy-paste-ready patches for applying the Task #1 changes from the
**AskJamie™** (`askjamie.bot`) repo to the two sister sites:

| Repo | Domain | Body class |
|------|--------|------------|
| OverKill Hill P³ | overkillhill.com | *(none — default)* |
| Glee-fully Tools | glee-fully.tools | `.glee-main` |

Both files (`assets/css/theme.css` and `assets/js/app.js`) are shared source
of truth for all three sites. Apply every patch below to each sister repo.

---

## 1 · `assets/css/theme.css` — Two changes

### 1a · Remove duplicate `.grid` declaration

Open `theme.css` and search for `.grid {`. There should be **two** adjacent
blocks that are identical. Keep the first; delete the second.

**Old (two blocks — delete the second):**
```css
.grid {
  display: grid;
  gap: 1.75rem;
}

.grid {
  display: grid;
  gap: 1.75rem;
}
```

**Correct (one block only):**
```css
.grid {
  display: grid;
  gap: 1.75rem;
}
```

If only one `.grid` block exists, this change was already clean — skip to 1b.

---

### 1b · Fix `.grid-3` breakpoints (tablet 2-column layout)

Search for `.grid-3` in `theme.css`. Find the full `.grid-3` section and its
`@media` rules, then replace the entire block with the version below.

**Replace everything from the `.grid-3` comment/rule through its last `@media`
block with:**

```css
/* Define .grid-3 once.  Uses auto-fill with a min of 220px so columns shrink
   gracefully before the explicit breakpoints kick in. */
.grid-3 {
  grid-template-columns: repeat(auto-fill, minmax(min(100%, 220px), 1fr));
}

/* Tablet (769-1024px): show 2 columns. */
@media (max-width: 1024px) and (min-width: 769px) {
  .grid-3 {
    grid-template-columns: repeat(2, 1fr);
  }
}

/* Mobile (<=768px): collapse to 1 column. */
@media (max-width: 768px) {
  .grid-3 {
    grid-template-columns: 1fr;
  }
}
```

**Why:** The old rule collapsed `.grid-3` to a single column at ≤1024 px,
meaning tablet-size screens (769–1024 px) got 1 column instead of 2. The fix
adds a `min-width: 769px` lower bound so the explicit 2-column rule only fires
in the tablet band. Mobile (≤768 px) stays at 1 column unchanged.

---

## 2 · `assets/js/app.js` — Two changes

### 2a · Add GA4 custom event tracking

Open `app.js` and find the end of the `DOMContentLoaded` bootstrap handler.
It ends with:

```js
  // ── Smooth scroll for internal anchors ───────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach((link) => {
    ...
  });

});   // ← closing brace of the DOMContentLoaded listener
```

Insert the following block **between the smooth-scroll block and the closing
`});`** (the final line of the file):

```js
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
```

---

### 2b · Wire `search_open` and `search_submit` events in §1a

The GA events above expose `window._gtag_event`. Two calls also need to be
added inside the §1a search module so the search modal fires its own events.

**`search_open` — inside `openModal()`:**

Find the `openModal()` function in §1a (search for `function openModal`).
Add the `_gtag_event` line immediately after `modal.removeAttribute("hidden")`:

```js
  function openModal() {
    if (!modal) return;
    modal.removeAttribute("hidden");
    document.body.classList.add("site-search-open");
    if (typeof window._gtag_event === "function") window._gtag_event("search_open", { event_category: "search" });
    // Focus a tick later so the browser actually moves caret
    setTimeout(function () {
      input.focus();
```

**`search_submit` — inside `runSearch()`:**

Find `function runSearch` in §1a. Add the `_gtag_event` line immediately
before the tokenisation step, guarded by the index-loaded check:

```js
    if (!indexCache) {
      // Index will trigger us again once loaded
      return;
    }

    if (typeof window._gtag_event === "function") window._gtag_event("search_submit", { event_category: "search", event_label: q.length + " chars" });
    var tokens = q.split(/\s+/).filter(Boolean);
```

---

### 2c · Update `isAnotherOverlayOpen()` stub

Search for `function isAnotherOverlayOpen` in §1a. If the sister site no
longer uses construction overlays, replace its body with the no-op stub used
in AskJamie:

```js
  // Detect any other site-level modal/overlay that's currently visible,
  // so the search shortcut doesn't fight with it (e.g. construction overlay).
  function isAnotherOverlayOpen() {
    // Construction overlays have been removed from all pages (Task #1, 2026-05).
    // This guard remains in case future modals are added.
    return false;
  }
```

**If the sister site still has active `.construction-overlay` pages** (i.e.
WIP pages still show the blocking modal), keep the original implementation
that checks `document.querySelector('.construction-overlay.is-visible')`.
Only switch to the no-op once all overlays have been removed from that site's
HTML files.

---

## 3 · GA measurement IDs

**Do not** copy the `gtag('config', ...)` line from AskJamie's `app.js` into
the sister repos. Each site has its own GA4 Measurement ID:

| Site | Measurement ID | Where set |
|------|---------------|-----------|
| AskJamie | `G-MT9Y10YY0G` | `assets/js/app.js` line 34 |
| OverKill Hill | *(see OKH `app.js` line ~34)* | OKH `app.js` |
| Glee-fully Tools | *(see Glee `app.js` line ~34)* | Glee `app.js` |

The GA events code (§2a above) uses the global `gtag()` function which is
already initialised with each site's own ID — no ID changes needed in the
event code itself.

---

## 4 · Verification checklist

After applying both patches to each sister repo:

- [ ] Open the site in a browser. Check for JS errors in the console.
- [ ] Click a `.btn` or `.btn-primary` → verify `cta_click` fires in GA4 DebugView.
- [ ] Click an outbound link → verify `outbound_click` fires.
- [ ] Press `/` to open search → verify `search_open` fires.
- [ ] Type a query and wait for results → verify `search_submit` fires.
- [ ] On a tablet (769–1024 px wide), confirm `.grid-3` sections show 2 columns.
- [ ] Run the site's own audit script: `python3 scripts/audit-site.py --quiet`
- [ ] Confirm 0 issues reported.

---

## 5 · Files that are NOT shared

These files were added or changed on AskJamie but should **not** be blindly
copied to sister repos (they contain AskJamie-specific content or URLs):

| File | Reason |
|------|--------|
| `llms.txt` | URL list is AskJamie-specific; each site needs its own |
| `sitemap.xml` | Page inventory is AskJamie-specific |
| `assets/data/search-index.json` | Generated from AskJamie's HTML; must be rebuilt per-site |
| `scripts/build-search-index.py` | Safe to copy — but run it per-site after copying |
| `scripts/audit-site.py` | Safe to copy — check `THEME_COLOR` constant matches each site's brand |
| All `*.html` files | Site-specific content; do not copy |

---

*Generated: 2026-05-26 — AskJamie™ Task #4 (sister-site sync)*
