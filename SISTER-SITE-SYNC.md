# Sister-Site Sync Guide — v1.2 (2026-05-27)

Precise, copy-paste-ready patches for applying AskJamie™ changes to the two
sister sites:

| Repo | Domain | Body class |
|------|--------|------------|
| OverKill Hill P³ | overkillhill.com | *(none — default)* |
| Glee-fully Tools | glee-fully.tools | `.glee-main` |

Both `assets/css/theme.css` and `assets/js/app.js` are shared source of truth
for all three sites. The tooling scripts (`scripts/audit-site.py`,
`scripts/build-search-index.py`, `scripts/apply-modern-baseline.py`) are also
shared and must be kept in lock-step. §§ 1–5 cover CSS/JS patches from v0.9
(Task #1). § 6 covers the tooling scripts (Task #5).

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
| `scripts/build-search-index.py` | **Needs per-site edits** — see § 6b |
| `scripts/audit-site.py` | **Needs per-site edits** — see § 6a |
| `scripts/apply-modern-baseline.py` | **Needs per-site edits** — see § 6c |
| All `*.html` files | Site-specific content; do not copy |

---

## 6 · Tooling scripts — per-site sync instructions

The three scripts below are shared tooling but contain AskJamie-specific
constants that **must be updated** before running them on a sister site.
This section documents exactly what to change, what is safe to copy verbatim,
and how to verify the result.

---

### 6a · `scripts/audit-site.py`

**Copy verbatim then edit these constants:**

#### `EXPECTED_THEME_COLOR` and `EXPECTED_BG_COLOR`

```python
# AskJamie values (line ~74):
EXPECTED_THEME_COLOR = "#2c5e6f"   # AskJamie muted teal
EXPECTED_BG_COLOR    = "#f5efe1"   # AskJamie cream
```

Replace with the target site's brand colors. The auditor checks that at least
one `<meta name="theme-color">` tag resolves to `EXPECTED_THEME_COLOR`, so this
**must** match the dark-mode (or single) `theme-color` declared in the site's
HTML.

| Site | `EXPECTED_THEME_COLOR` | `EXPECTED_BG_COLOR` |
|------|----------------------|---------------------|
| AskJamie™ (`askjamie.bot`) | `"#2c5e6f"` | `"#f5efe1"` |
| OverKill Hill P³ (`overkillhill.com`) | *(check OKH HTML `theme-color`)* | *(check OKH CSS `--color-bg`)* |
| Glee-fully Tools (`glee-fully.tools`) | *(check Glee HTML `theme-color`)* | *(check Glee CSS `--color-bg`)* |

To find the correct value for a sister site, search any of its HTML pages for
`name="theme-color"` and copy the `content="..."` value.

#### `EXCLUDE_DIRS`

```python
# AskJamie values (line ~66):
EXCLUDE_DIRS = {".local", ".agents", "attached_assets", "node_modules",
                ".cache", ".git", ".vscode", "templates"}
```

`".agents"` is a Replit-specific directory that may not exist on sister sites
— safe to keep it in the set (the code ignores missing dirs). Add any
site-specific build or vendor directories that should be excluded.

#### `EXCLUDE_FROM_SITEMAP`

```python
# AskJamie values (line ~68):
EXCLUDE_FROM_SITEMAP = {"404.html", "under-construction.html"}
```

Add any additional pages that exist on disk but should not appear in
`sitemap.xml` (e.g. holding pages, staging pages).

#### Mermaid referral-link check

The auditor contains a check: any page with `<pre class="mermaid">` must carry
the OKH affiliate referral link (`mermaidchart.cello.so/UhVlNtC2MlS`) and the
`mermaid-referral-link` CSS class.

- **OverKill Hill:** The OKH site (`overkillhill.com/writings/first-diagram-is-a-liar`)
  uses the same Mermaid affiliate link. Keep the check verbatim — it applies.
- **Glee-fully Tools:** If Glee pages use Mermaid, apply the same convention.
  If no Glee pages will ever embed Mermaid, the check is harmless (it only
  fires when `<pre class="mermaid">` is detected).

#### Everything else

All other checks (title/description length, canonical, OG fields, image
hygiene, CSP/referrer meta, sitemap reconciliation, etc.) are generic HTML
quality gates with no site-specific constants. **Copy verbatim.**

**Verify after copying:**

```bash
python3 scripts/audit-site.py --quiet   # must report 0 issues
```

---

### 6b · `scripts/build-search-index.py`

**Copy verbatim then edit these constants:**

#### `SITE_URL`

```python
# AskJamie value (line ~28):
SITE_URL = "https://askjamie.bot"
```

| Site | Replace with |
|------|-------------|
| OverKill Hill P³ | `"https://overkillhill.com"` |
| Glee-fully Tools | `"https://glee-fully.tools"` |

`SITE_URL` is embedded in the generated `search-index.json` as a metadata
field (`"site": "..."`) and is used by `derive_url_from_path()` to build
canonical URLs. Getting this wrong means all indexed URLs point at the
wrong domain.

#### `strip_brand_suffix()`

```python
# AskJamie values (lines ~195-203):
for suffix in (
    " — AskJamie™",
    " | AskJamie™",
    " — AskJamie",
    " | AskJamie",
):
```

Replace with the target site's brand name as it appears in page `<title>` tags.
For example, if OverKill Hill titles end with `" — OverKill Hill P³™"`, add
that suffix to the list (and remove the AskJamie suffixes).

If a sister site's pages don't append a brand suffix to titles at all, simply
clear the loop body and `return title` directly:

```python
def strip_brand_suffix(title: str) -> str:
    return normalize_text(title)
```

#### `derive_section()`

```python
# AskJamie values (lines ~173-189):
section_map = {
    "about": "About",
    "contact": "Contact",
    "legal": "Legal",
    "universe": "Universe",
    "lens-system": "Lens System",
}
```

Replace with the target site's top-level URL segments and their human-readable
section labels. The section label is shown in search result cards as the
category chip.

#### `EXCLUDE_DIRS` and `EXCLUDE_FILES`

```python
# AskJamie values (lines ~31-32):
EXCLUDE_DIRS  = {".git", ".local", "attached_assets", "tools", "node_modules"}
EXCLUDE_FILES = {"404.html", "under-construction.html"}
```

Add any site-specific directories or files to exclude from indexing (e.g.
template directories, holding pages). Note: `"tools"` is a legacy alias for
`"scripts/"` — kept for backward-compat but safe to remove if the sister site
never had a `tools/` directory.

#### Everything else

`STRIP_TAGS`, `STRIP_CLASSES_CONTAINS`, `VOID_TAGS`, the `TextExtractor`
parser, the `MAX_BODY` cap (4 000 chars/page), and the output format are all
generic and **safe to copy verbatim** across all three sites. The CSS class
names in `STRIP_CLASSES_CONTAINS` (`site-header`, `site-footer`, `primary-nav`,
`skip-link`, `construction-overlay`) are shared by the common `theme.css`
design system, so they apply equally to all three repos.

**After copying and editing, rebuild the index:**

```bash
python3 scripts/build-search-index.py
# → assets/data/search-index.json  (should show > 0 pages indexed)
```

Then verify the auditor still agrees the index is fresh:

```bash
python3 scripts/audit-site.py --quiet   # must report 0 issues
```

---

### 6c · `scripts/apply-modern-baseline.py`

**Copy verbatim then edit these constants:**

#### Theme-color constants

```python
# AskJamie values (lines ~72-79):
THEME_COLOR_LEGACY_RE = re.compile(
    r'<meta\s+name="theme-color"\s+content="#2c5e6f"\s*/?>',
    re.IGNORECASE
)
THEME_COLOR_PAIR = (
    '<meta name="theme-color" content="#f5efe1" media="(prefers-color-scheme: light)" />\n'
    '    <meta name="theme-color" content="#2c5e6f" media="(prefers-color-scheme: dark)" />'
)
```

`THEME_COLOR_LEGACY_RE` matches the old single-value `theme-color` tag so it
can be split into a modern light/dark pair. It is hardcoded to AskJamie's teal
`#2c5e6f`. Update for each site:

| Site | `THEME_COLOR_LEGACY_RE` content value | `THEME_COLOR_PAIR` light | `THEME_COLOR_PAIR` dark |
|------|--------------------------------------|--------------------------|-------------------------|
| AskJamie™ | `#2c5e6f` | `#f5efe1` | `#2c5e6f` |
| OverKill Hill P³ | *(OKH brand color)* | *(OKH light bg)* | *(OKH dark/brand)* |
| Glee-fully Tools | *(Glee brand color)* | *(Glee light bg)* | *(Glee dark/brand)* |

To find the correct values: open any HTML page on the sister site and look for
`<meta name="theme-color">`. Use that value for `THEME_COLOR_LEGACY_RE` and
decide the light/dark split using the site's CSS `--color-bg` (light) and
primary brand color (dark).

#### CSP allow-list

```python
# AskJamie value (lines ~46-58):
CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline' "
    "https://www.googletagmanager.com https://cdn.jsdelivr.net; "
    ...
)
```

All three sister sites use the **same tech stack** (GA4 via GTM, Mermaid ESM
from `cdn.jsdelivr.net`, Google Fonts). The CSP allow-list is **safe to copy
verbatim** — no site-specific domains to add or remove.

If a sister site does not embed Mermaid diagrams, `https://cdn.jsdelivr.net`
can be dropped from `script-src` and the Mermaid `script-src nonce` pattern
can be removed. Otherwise, keep it.

#### Everything else

`EXCLUDE_DIRS`, image-upgrade logic (`upgrade_images()`), and security meta
insertion (`add_security_meta()`) are generic. **Copy verbatim.**

**Run after copying and editing:**

```bash
python3 scripts/apply-modern-baseline.py
# Verify: 0 files modified on re-run (idempotency check)
python3 scripts/apply-modern-baseline.py
# → "Files modified: 0 of N"
```

Then run the auditor to confirm 0 issues:

```bash
python3 scripts/audit-site.py --quiet
```

---

### 6d · `assets/js/analytics.js` — status

`analytics.js` was a separate file on AskJamie through v0.8. In **v0.9
(2026-05-26)** it was consolidated into `§0` of `assets/js/app.js`. The file
no longer exists on AskJamie.

**For sister sites:** check whether `analytics.js` is still a separate file in
the repo.

- **If the sister site has applied the v0.9 `app.js` consolidation** (i.e. the
  §§ 1–2 patches in this guide have been applied): `analytics.js` is no longer
  needed. Delete it and remove the `<script defer src="/assets/js/analytics.js">` 
  tag from every HTML page.
- **If the sister site has not yet applied the v0.9 `app.js` consolidation:**
  keep `analytics.js` as-is until the consolidation is done. The two approaches
  are mutually exclusive — do not mix an unconsolidated `analytics.js` with the
  consolidated `app.js` or GA4 will initialize twice.

---

### 6e · Sync summary table

| Script | Copy verbatim? | Per-site edits required |
|--------|---------------|------------------------|
| `audit-site.py` | ✅ Most of it | `EXPECTED_THEME_COLOR`, `EXPECTED_BG_COLOR` |
| `build-search-index.py` | ✅ Most of it | `SITE_URL`, `strip_brand_suffix()` suffixes, `derive_section()` map |
| `apply-modern-baseline.py` | ✅ Most of it | `THEME_COLOR_LEGACY_RE` pattern, `THEME_COLOR_PAIR` colors |
| `analytics.js` | ❌ Do not copy | Eliminate once v0.9 `app.js` consolidation is applied |

---

## 7 · Execution log

### Task #21 — Tooling scripts staged (2026-05-27)

Three OKH-adapted copies of the tooling scripts have been staged in
`assets/docs/sister-site-sync/okh/` alongside the existing CSS/JS patches.
The OKH sync package is now complete.

| File staged | Per-site changes applied |
|-------------|--------------------------|
| `okh/audit-site.py` | `EXPECTED_THEME_COLOR = "#c46a2c"` (OKH rust-orange); `EXPECTED_BG_COLOR = "#2a2320"` (OKH espresso) |
| `okh/build-search-index.py` | `SITE_URL = "https://overkillhill.com"`; OKH brand suffixes in `strip_brand_suffix()`; OKH section map in `derive_section()` |
| `okh/apply-modern-baseline.py` | `THEME_COLOR_LEGACY_RE` matches `#c46a2c`; `THEME_COLOR_PAIR` light=`#f6f2ee` / dark=`#c46a2c` |

**VERIFY before dropping into the OKH repo:**

1. Open any OKH HTML page and check `name="theme-color"`. If the content value
   is not `#c46a2c`, update `EXPECTED_THEME_COLOR` in `audit-site.py` and
   `THEME_COLOR_LEGACY_RE` in `apply-modern-baseline.py` to match.
2. Check OKH page `<title>` tags for the exact brand suffix used. Update
   `strip_brand_suffix()` in `build-search-index.py` if the suffix strings differ.
3. Confirm the `derive_section()` map covers all top-level OKH directories.
4. Run each script once and verify 0 issues on the second run (idempotency check).

All other logic (HTML parsing, CSP, image attributes, sitemap/index
reconciliation) is verbatim from the AskJamie originals.

---

### Task #4 — CSS and JS patches applied (2026-05-26)

### OverKill Hill (`overkillhill.com` → `OKHP3/OverKill-Hill`)

Both patches applied programmatically to a local clone of the repo.

**CSS** — `assets/css/theme.css`
- ✅ Duplicate `.grid` block removed (was two identical `display:grid;gap:1.75rem` blocks)
- ✅ `.grid-3` breakpoints updated: single `max-width:1024px → 1fr` rule replaced with
  tablet band (`769–1024px → 2 cols`) + mobile rule (`≤768px → 1 col`)
- JS syntax check: **PASS** (Node `--check`)

**JS** — `assets/js/app.js`
- ✅ `_gtag_event()` wrapper + `cta_click`/`outbound_click`/`contact_click` listeners inserted
  before closing `});` of `DOMContentLoaded`
- ✅ `search_open` event wired in `open()` function (OKH search module)
- ✅ `search_submit` event wired in `render()` function (OKH search module)
- Construction overlay code **retained** (OKH still uses it for Glee WIP pages)
- JS syntax check: **PASS** (`node --check`)

**Patched files saved** in this repo for owner reference:
- `assets/docs/sister-site-sync/okh/theme.css` — ready to copy
- `assets/docs/sister-site-sync/okh/app.js` — ready to copy
- `assets/docs/sister-site-sync/okh/theme.css.patch` — unified diff
- `assets/docs/sister-site-sync/okh/app.js.patch` — unified diff

**To apply:** copy the two patched files into the `OKHP3/OverKill-Hill` repo,
commit, and deploy. The unified diffs can also be applied with `git apply`.

---

### Glee-fully Tools (`glee-fully.tools` → `OKHP3/Glee-fullyTools`)

The `OKHP3/Glee-fullyTools` GitHub repo was cloned but contains **no files**
beyond the `.git` directory. There are no `assets/css/theme.css` or
`assets/js/app.js` to patch. The Glee site's front-end files appear to live
elsewhere (possibly in a separate deployment pipeline or are not yet committed).

**No changes possible** until the Glee front-end files are committed to the repo.
When they are, apply the same patches documented in §§ 1–2 above, and apply the
per-site tooling edits documented in § 6.

---

*Updated: 2026-05-27 — § 6 tooling-scripts sync added (Task #5)*
*Originally generated: 2026-05-26 — AskJamie™ Task #4 (sister-site sync)*
