// AskJamie-specific analytics events. GA4 itself remains configured by page markup.
window.askJamieTrack = function (eventName, parameters) {
  if (typeof window.gtag !== "function") return;
  window.gtag("event", eventName, parameters || {});
};

function track(eventName, link, extra) {
  window.askJamieTrack(eventName, Object.assign({
    link_url: link.href,
    link_text: (link.textContent || "").trim().slice(0, 100),
    page_path: window.location.pathname,
  }, extra || {}));
}

document.querySelectorAll('a[href*="chatgpt.com/g/"]').forEach((link) => {
  link.addEventListener("click", () => {
    track("gpt_click", link, {
      destination: "chatgpt",
      lens: document.title.replace(/\s*[|—-].*$/, "").trim(),
    });
  });
});

document.querySelectorAll('a[href^="mailto:"]').forEach((link) => {
  link.addEventListener("click", () => {
    const card = link.closest("article, section");
    const heading = card && card.querySelector("h2, h3");
    const subject = new URL(link.href).searchParams.get("subject");
    track("inquiry_click", link, {
      destination: "email",
      inquiry_type: subject || (heading ? heading.textContent.trim() : "general"),
    });
  });
});
