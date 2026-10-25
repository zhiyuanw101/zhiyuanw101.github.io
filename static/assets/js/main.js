// Site behaviour, adapted from Hugo PaperMod (MIT License).

// Smooth-scroll for in-page anchors (ToC, footnotes, "back to top").
document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
	anchor.addEventListener("click", function (e) {
		const id = decodeURIComponent(this.getAttribute("href").substr(1));
		const target = document.querySelector(`[id='${id}']`);
		if (!target) return;
		e.preventDefault();
		const smooth = !window.matchMedia("(prefers-reduced-motion: reduce)").matches;
		target.scrollIntoView(smooth ? { behavior: "smooth" } : undefined);
		if (id === "top") {
			history.replaceState(null, null, " ");
		} else {
			history.pushState(null, null, `#${id}`);
		}
	});
});

// Keep the horizontal scroll position of the menu on narrow screens.
const menu = document.getElementById("menu");
if (menu) {
	try {
		menu.scrollLeft = localStorage.getItem("menu-scroll-position");
		menu.onscroll = () => localStorage.setItem("menu-scroll-position", menu.scrollLeft);
	} catch (e) {}
}

// "Copy" button on code blocks.
document.querySelectorAll("pre > code").forEach((codeblock) => {
	const button = document.createElement("button");
	button.classList.add("copy-code");
	button.innerText = "copy";
	button.addEventListener("click", () => {
		const done = () => {
			button.innerText = "copied!";
			setTimeout(() => (button.innerText = "copy"), 2000);
		};
		if ("clipboard" in navigator) {
			navigator.clipboard.writeText(codeblock.textContent).then(done);
			return;
		}
		const range = document.createRange();
		range.selectNodeContents(codeblock);
		const selection = window.getSelection();
		selection.removeAllRanges();
		selection.addRange(range);
		try {
			document.execCommand("copy");
			done();
		} catch (e) {}
		selection.removeRange(range);
	});
	codeblock.parentNode.appendChild(button);
});

// Syntax highlighting (highlight.js is loaded with defer, so it is ready by DOMContentLoaded).
document.addEventListener("DOMContentLoaded", () => {
	if (window.hljs) {
		document.querySelectorAll("pre > code").forEach((el) => window.hljs.highlightElement(el));
	}
});

// Search page: plain substring matching over the generated index.json.
const searchInput = document.getElementById("searchInput");
if (searchInput) {
	const results = document.getElementById("searchResults");
	const root = searchInput.dataset.root || "../";
	let index = [];
	fetch(root + "index.json")
		.then((r) => r.json())
		.then((data) => (index = data));

	const escapeHtml = (s) =>
		s.replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[c]);

	searchInput.addEventListener("input", () => {
		const q = searchInput.value.trim().toLowerCase();
		results.innerHTML = "";
		if (!q) return;
		const terms = q.split(/\s+/);
		const hits = index.filter((p) => {
			const hay = (p.title + " " + p.tags.join(" ") + " " + p.content).toLowerCase();
			return terms.every((t) => hay.includes(t));
		});
		for (const p of hits) {
			const li = document.createElement("li");
			li.className = "post-entry";
			li.innerHTML =
				`<header class="entry-header">${escapeHtml(p.title)}&nbsp;»</header>` +
				`<a href="${root}${p.permalink}" aria-label="${escapeHtml(p.title)}"></a>`;
			results.appendChild(li);
		}
	});

	searchInput.addEventListener("keydown", (e) => {
		if (e.key === "Enter") {
			const first = results.querySelector("a");
			if (first) first.click();
		} else if (e.key === "Escape") {
			searchInput.value = "";
			results.innerHTML = "";
		}
	});
}

// Floating "back to Table of Contents" button on posts.
const toc = document.getElementById("toc");
const tocLink = document.getElementById("toc-link");
if (toc && tocLink) {
	const update = () => tocLink.classList.toggle("visible", toc.getBoundingClientRect().bottom < 0);
	window.addEventListener("scroll", update, { passive: true });
	update();
	// Re-open the ToC if the reader collapsed it, before the smooth-scroll handler above runs.
	tocLink.addEventListener("click", () => (toc.querySelector("details").open = true), { capture: true });
}

// Background-knowledge cards: a "Card N" citation opens its card and briefly highlights it.
const openCard = (id) => {
	const card = document.getElementById(id);
	if (!card || !card.classList.contains("side-card")) return;
	card.querySelector("details").open = true;
	card.classList.add("flash");
	setTimeout(() => card.classList.remove("flash"), 1600);
};
document.querySelectorAll("a.card-ref").forEach((a) => {
	a.addEventListener("click", () => openCard(a.hash.slice(1)), { capture: true });
});
if (location.hash.startsWith("#card-")) openCard(location.hash.slice(1));
