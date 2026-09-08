// Enable the optional Google Fonts stylesheet after the document is parsed.
// The route's local stylesheet can paint immediately with system fallbacks;
// branded type settles without waiting for third-party analytics to finish.
const deferredFonts = document.querySelectorAll("link[data-deferred-fonts]");

if (deferredFonts.length) {
  const enableFonts = () => {
    requestAnimationFrame(() => {
      deferredFonts.forEach((link) => {
        link.media = "all";
      });
    });
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", enableFonts, { once: true });
  } else {
    enableFonts();
  }
}