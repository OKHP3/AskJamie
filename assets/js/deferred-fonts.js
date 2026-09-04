// Enable the optional Google Fonts stylesheet after the first page load.
// The route's local stylesheet can paint immediately with system fallbacks;
// branded type still settles in for the rest of the visit.
const deferredFonts = document.querySelectorAll("link[data-deferred-fonts]");

if (deferredFonts.length) {
  const enableFonts = () => {
    requestAnimationFrame(() => {
      deferredFonts.forEach((link) => {
        link.media = "all";
      });
    });
  };

  if (document.readyState === "complete") {
    setTimeout(enableFonts, 0);
  } else {
    window.addEventListener("load", enableFonts, { once: true });
  }
}