// Keep Mermaid strict. Add navigation only from the generated ordinary links.
const groups = document.querySelectorAll(".universe-map-group");
function linkNodes(group) {
  for (const link of group.querySelectorAll("a[data-universe-node]")) {
    const id = link.dataset.universeNode;
    if (!/^n[0-9a-f]{16}$/.test(id)) continue;
    const url = new URL(link.getAttribute("href"), location.origin);
    if (url.origin !== location.origin || !url.pathname.startsWith("/") || url.search) continue;
    const node = group.querySelector(`svg .node[id*="flowchart-${id}-"]`);
    if (!node || node.parentElement.localName === "a") continue;
    const anchor = document.createElementNS("http://www.w3.org/2000/svg", "a");
    anchor.setAttribute("href", url.pathname + url.hash);
    anchor.setAttribute("tabindex", "-1");
    node.before(anchor);
    anchor.append(node);
  }
}
for (const group of groups) {
  const observer = new MutationObserver(() => {
    if (!group.querySelector("svg .node")) return;
    observer.disconnect();
    linkNodes(group);
  });
  observer.observe(group, { childList: true, subtree: true });
  linkNodes(group);
}
