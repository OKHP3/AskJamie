// Load GA4 after the first page load opportunity without making analytics
// consent-gated. The page-shell gtag stub queues js/config/events immediately;
// this loader only postpones the third-party script's main-thread work.
(() => {
  const loadAnalytics = () => {
    if (document.querySelector('script[data-askjamie-analytics-loaded]')) return;
    const script = document.createElement("script");
    script.async = true;
    script.fetchPriority = "low";
    script.src = "https://www.googletagmanager.com/gtag/js?id=G-MT9Y10YY0G";
    script.dataset.askjamieAnalyticsLoaded = "true";
    document.head.appendChild(script);
  };

  const scheduleAnalytics = () => {
    if (typeof window.requestIdleCallback === "function") {
      window.requestIdleCallback(loadAnalytics, { timeout: 2500 });
    } else {
      window.setTimeout(loadAnalytics, 1000);
    }
  };

  if (document.readyState === "complete") {
    scheduleAnalytics();
  } else {
    window.addEventListener("load", scheduleAnalytics, { once: true });
  }
})();