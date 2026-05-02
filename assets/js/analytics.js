/* OverKill Hill P3 Universe — Google Analytics 4 (gtag) bootstrap
   Source of truth shared by:
     - OverKill Hill        (overkillhill.com)
     - Glee-fully Tools     (glee-fully.tools)
     - AskJamie             (askjamie.bot)

   This file replaces the 7-line inline gtag config block that used to
   live in every page's <head>.  HTML pages now load this with:

     <!-- Google tag (gtag.js) -->
     <script async src="https://www.googletagmanager.com/gtag/js?id=G-MT9Y10YY0G"></script>
     <script defer src="/assets/js/analytics.js"></script>

   Benefits of externalisation:
     - One file to update if the GA4 measurement ID ever changes.
     - Browser caches it across pages (smaller per-navigation cost).
     - Survives a strict `script-src 'self' https://www.googletagmanager.com`
       Content Security Policy without per-page nonces or 'unsafe-inline'.
     - Easier to extend with custom events (gtag('event', ...)) later.

   Note: the gtag.js library itself stays as a separate <script async>
   tag in each page's <head> because Google's CDN serves it and it must
   be loaded directly from googletagmanager.com.
*/

window.dataLayer = window.dataLayer || [];
function gtag() { dataLayer.push(arguments); }
gtag('js', new Date());
gtag('config', 'G-MT9Y10YY0G');
