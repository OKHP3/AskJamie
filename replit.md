# AskJamie™ — OverKill Hill P³™

## Project Overview

A static marketing and documentation website for **AskJamie™**, an AI persona and "thinking partner" platform by OverKill Hill P³™ (OKHP). It showcases the AskJamie™ AI helpdesk concept, the Lens System portfolio case studies, and BrandGuard™ integrations.

## Tech Stack

- **Frontend:** Vanilla HTML5, CSS3 (CSS custom properties/variables), JavaScript
- **Diagramming:** Mermaid.js (via CDN)
- **Fonts:** Google Fonts (Baloo 2, Open Sans, Kalam, Alfa Slab One)
- **No build system** — pure static files served directly

## Project Layout

```
/                     # Root: index.html, 404.html, under-construction.html
assets/
  css/theme.css        # Main stylesheet (3500+ lines, multi-brand theming)
  js/app.js            # Main JS (scroll reveals, theme toggles, reading progress)
  js/mermaid-init.js   # Mermaid diagram initialization
  img/                 # Brand assets, avatars, case study images
about/                 # About page
contact/               # Contact page
legal/                 # Legal pages
universe/              # Universe/ecosystem overview
lens-system/           # Portfolio case studies
  enterprise-sleuth/
  okhp3-brandguard/    # BrandGuard case studies (Coca-Cola, Lego, Starbucks, etc.)
  professional-portfolio/
  resume-representative/
```

## Development Server

- **Workflow:** "Start application"
- **Command:** `python3 -m http.server 5000 --bind 0.0.0.0`
- **Port:** 5000

## Deployment

- **Type:** Static site
- **Public directory:** `.` (project root)
