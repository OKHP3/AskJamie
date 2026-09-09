// Enable optional stylesheets after the document is parsed.
// Critical route CSS paints first with system fallbacks; the full theme and
// branded type settle without waiting for third-party analytics to finish.
const deferredFonts = document.querySelectorAll("link[data-deferred-fonts]");
const deferredStyles = document.querySelectorAll("link[data-deferred-styles]");

if (deferredFonts.length || deferredStyles.length) {
  const enableDeferredStyles = () => {
    deferredFonts.forEach((link) => {
      link.media = "all";
    });
    deferredStyles.forEach((link) => {
      link.media = "all";
    });
  };

  const enableAfterLoad = () => {
    // On mobile, let the critical hero remain stable through the LCP window.
    // Desktop keeps the full theme's existing immediate post-load behavior.
    if (window.matchMedia("(max-width: 899px)").matches) {
      window.setTimeout(enableDeferredStyles, 2000);
    } else {
      enableDeferredStyles();
    }
  };

  if (document.readyState === "complete") {
    enableAfterLoad();
  } else {
    window.addEventListener("load", enableAfterLoad, { once: true });
  }
}