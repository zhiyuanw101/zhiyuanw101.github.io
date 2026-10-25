#!/usr/bin/env python3
"""Tiny static-site generator that mirrors the layout of a Hugo + PaperMod blog.

Usage:  python3 tools/build.py          # writes the site into ./public

Content lives in ./content:
  posts/<YYYY-MM-DD-slug>.html   post body (HTML fragment) with a front-matter comment on top
  figures/<name>.html            figure fragments, referenced from a post as <!--fig:name-->
  faq.html                       body of the FAQ page
Static files (css, js, images) are copied from ./static.
"""

import hashlib
import html
import json
import math
import re
import shutil
from datetime import datetime
from email.utils import format_datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTENT = ROOT / "content"
STATIC = ROOT / "static"
OUT = ROOT / "public"

SITE = {
	"title": "Zhiyuan's Log",
	"author": "Zhiyuan Wang",
	"author_last": "Wang",
	"author_first": "Zhiyuan",
	"base_url": "https://zhiyuanw101.github.io/",  # used for citations, share links and RSS
	"description": "Document my learning notes.",
	"welcome_title": "👋 Welcome to Zhiyuan's Log",
	"welcome_text": "Hi, this is Zhiyuan. I'm documenting my learning notes in this blog.",
	"github": "https://github.com/zhiyuanw101",
}

MENU = [
	("Posts", ""),
	("Archive", "archives/"),
	("Search", "search/"),
	("Tags", "tags/"),
	("FAQ", "faq/"),
]

ICONS = {
	"rss": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M4 11a9 9 0 0 1 9 9" /><path d="M4 4a16 16 0 0 1 16 16" /><circle cx="5" cy="19" r="1" /></svg>',
	"github": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>',
	"twitter": '<svg version="1.1" viewBox="0 0 512 512" xml:space="preserve"><path d="M449.446,0c34.525,0 62.554,28.03 62.554,62.554l0,386.892c0,34.524 -28.03,62.554 -62.554,62.554l-386.892,0c-34.524,0 -62.554,-28.03 -62.554,-62.554l0,-386.892c0,-34.524 28.029,-62.554 62.554,-62.554l386.892,0Zm-253.927,424.544c135.939,0 210.268,-112.643 210.268,-210.268c0,-3.218 0,-6.437 -0.153,-9.502c14.406,-10.421 26.973,-23.448 36.935,-38.314c-13.18,5.824 -27.433,9.809 -42.452,11.648c15.326,-9.196 26.973,-23.602 32.49,-40.92c-14.252,8.429 -30.038,14.56 -46.896,17.931c-13.487,-14.406 -32.644,-23.295 -53.946,-23.295c-40.767,0 -73.87,33.104 -73.87,73.87c0,5.824 0.613,11.494 1.992,16.858c-61.456,-3.065 -115.862,-32.49 -152.337,-77.241c-6.284,10.881 -9.962,23.601 -9.962,37.088c0,25.594 13.027,48.276 32.95,61.456c-12.107,-0.307 -23.448,-3.678 -33.41,-9.196l0,0.92c0,35.862 25.441,65.594 59.311,72.49c-6.13,1.686 -12.72,2.606 -19.464,2.606c-4.751,0 -9.348,-0.46 -13.946,-1.38c9.349,29.426 36.628,50.728 68.965,51.341c-25.287,19.771 -57.164,31.571 -91.8,31.571c-5.977,0 -11.801,-0.306 -17.625,-1.073c32.337,21.15 71.264,33.41 112.95,33.41Z" /></svg>',
	"linkedin": '<svg version="1.1" viewBox="0 0 512 512" xml:space="preserve"><path d="M449.446,0c34.525,0 62.554,28.03 62.554,62.554l0,386.892c0,34.524 -28.03,62.554 -62.554,62.554l-386.892,0c-34.524,0 -62.554,-28.03 -62.554,-62.554l0,-386.892c0,-34.524 28.029,-62.554 62.554,-62.554l386.892,0Zm-288.985,423.278l0,-225.717l-75.04,0l0,225.717l75.04,0Zm270.539,0l0,-129.439c0,-69.333 -37.018,-101.586 -86.381,-101.586c-39.804,0 -57.634,21.891 -67.617,37.266l0,-31.958l-75.021,0c0.995,21.181 0,225.717 0,225.717l75.02,0l0,-126.056c0,-6.748 0.486,-13.492 2.474,-18.315c5.414,-13.475 17.767,-27.434 38.494,-27.434c27.135,0 38.007,20.707 38.007,51.037l0,120.768l75.024,0Zm-307.552,-334.556c-25.674,0 -42.448,16.879 -42.448,39.002c0,21.658 16.264,39.002 41.455,39.002l0.484,0c26.165,0 42.452,-17.344 42.452,-39.002c-0.485,-22.092 -16.241,-38.954 -41.943,-39.002Z" /></svg>',
	"facebook": '<svg version="1.1" viewBox="0 0 512 512" xml:space="preserve"><path d="M449.446,0c34.525,0 62.554,28.03 62.554,62.554l0,386.892c0,34.524 -28.03,62.554 -62.554,62.554l-106.468,0l0,-192.915l66.6,0l12.672,-82.621l-79.272,0l0,-53.617c0,-22.603 11.073,-44.636 46.58,-44.636l36.042,0l0,-70.34c0,0 -32.71,-5.582 -63.982,-5.582c-65.288,0 -107.96,39.569 -107.96,111.204l0,62.971l-72.573,0l0,82.621l72.573,0l0,192.915l-191.104,0c-34.524,0 -62.554,-28.03 -62.554,-62.554l0,-386.892c0,-34.524 28.029,-62.554 62.554,-62.554l386.892,0Z" /></svg>',
	"search": '<svg xmlns="http://www.w3.org/2000/svg" width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"></circle><line x1="21" y1="21" x2="16.65" y2="16.65"></line></svg>',
	"top": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 6" fill="currentColor"><path d="M12 6H0l6-6z" /></svg>',
}

MATHJAX = """<script>
	MathJax = {
		tex: {
			inlineMath: [['$', '$'], ['\\\\(', '\\\\)']],
			displayMath: [['$$', '$$'], ['\\\\[', '\\\\]']],
			processEscapes: true,
			processEnvironments: true
		},
		options: { skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre'] }
	};
</script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3.2.2/es5/tex-mml-chtml.js"></script>"""

HLJS = '<script defer src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>'

DARK_STYLE = """<style>
	#theme-toggle, .top-link { display: none; }
</style>
<style>
	@media (prefers-color-scheme: dark) {
		:root {
			--theme: rgb(29, 30, 32);
			--entry: rgb(46, 46, 51);
			--primary: rgb(218, 218, 219);
			--secondary: rgb(155, 156, 157);
			--tertiary: rgb(65, 66, 68);
			--content: rgb(196, 196, 197);
			--hljs-bg: rgb(46, 46, 51);
			--code-bg: rgb(55, 56, 62);
			--border: rgb(51, 51, 51);
		}
		.list { background: var(--theme); }
	}
	/* Inline SVG figures follow the page colours. */
	.post-content figure svg { display: block; width: 100%; height: auto; color: var(--primary); }
	.post-content figure svg text { font-family: inherit; }
	.post-content table.notation td:first-child { white-space: nowrap; }
	/* The fixed logo sits left of the text column; keep it in the header when there is no room for that. */
	@media (max-width: 1100px) { .logo { position: static; } }
</style>"""

DARK_INIT = """<script>
	try {
		if (localStorage.getItem("pref-theme") === "dark") {
			document.body.classList.add('dark');
		} else if (localStorage.getItem("pref-theme") === "light") {
			document.body.classList.remove('dark');
		} else if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
			document.body.classList.add('dark');
		}
	} catch (e) {
		if (window.matchMedia('(prefers-color-scheme: dark)').matches) document.body.classList.add('dark');
	}
</script>"""

WPM = 213  # Hugo's reading-time constant
SUMMARY_WORDS = 70


# ---------------------------------------------------------------- helpers

def asset(path):
	"""Asset path with a short content hash so browsers pick up changes."""
	digest = hashlib.sha256((STATIC / path).read_bytes()).hexdigest()[:8]
	return f"{path}?v={digest}"


def esc(s):
	return html.escape(s, quote=True)


def strip_tags(s):
	s = re.sub(r"<(script|style|svg)\b.*?</\1>", " ", s, flags=re.S)
	s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
	s = re.sub(r"<[^>]+>", " ", s)
	return html.unescape(re.sub(r"\s+", " ", s)).strip()


def slugify(text):
	text = strip_tags(text).lower()
	text = re.sub(r"\\[a-z]+", "", text)  # drop TeX commands such as \mathbf
	text = re.sub(r"[^\w\s-]", "", text)
	return re.sub(r"\s+", "-", text.strip())


def tag_slug(tag):
	return re.sub(r"[^\w-]", "", tag.strip().lower().replace(" ", "-"))


def fmt_date(d):
	return f"{d:%B} {d.day}, {d.year}"


def post_meta(post):
	return (
		f"Date: {fmt_date(post['date'])}&nbsp;|&nbsp;"
		f"Estimated Reading Time: {post['minutes']} min&nbsp;|&nbsp;Author: {esc(SITE['author'])}"
	)


# ---------------------------------------------------------------- layout

def page(title, body, root, *, body_class="", description=None, math=False, code=False, active=None):
	full_title = title if title == SITE["title"] else f"{title} | {SITE['title']}"
	head_extra = []
	if math:
		head_extra.append(MATHJAX)
	if code:
		head_extra.append(HLJS)
	active_attr = ' class="active"'
	menu = "\n".join(
		f'\t\t\t<li><a href="{root}{href}" title="{name}"><span{active_attr if name == active else ""}>{name}</span></a></li>'
		for name, href in MENU
	)
	head_extra = "\n".join(head_extra)
	return f"""<!DOCTYPE html>
<html lang="en" dir="auto">
<head>
<meta charset="utf-8">
<meta http-equiv="X-UA-Compatible" content="IE=edge">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
<meta name="robots" content="index, follow">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(description or SITE['description'])}">
<meta name="author" content="{esc(SITE['author'])}">
<link rel="stylesheet" href="{root}{asset('assets/css/stylesheet.css')}">
<link rel="alternate" type="application/rss+xml" href="{root}index.xml" title="{esc(SITE['title'])}">
{DARK_STYLE}
{head_extra}
</head>

<body class="{body_class}" id="top">
{DARK_INIT}

<header class="header">
	<nav class="nav">
		<div class="logo">
			<a href="{root}" accesskey="h" title="{esc(SITE['title'])} (Alt + H)">{esc(SITE['title'])}</a>
		</div>
		<ul id="menu">
{menu}
		</ul>
	</nav>
</header>
<main class="main">
{body}
</main>

<footer class="footer">
	<span>&copy; {datetime.now().year} <a href="{root}">{esc(SITE['title'])}</a></span>
	<span>
		Theme inspired by
		<a href="https://git.io/hugopapermod" rel="noopener" target="_blank">PaperMod</a>
	</span>
</footer>
<a href="#top" aria-label="go to top" title="Go to Top (Alt + G)" class="top-link" id="top-link" accesskey="g">{ICONS['top']}</a>
<script src="{root}{asset('assets/js/main.js')}"></script>
</body>
</html>
"""


def post_entry(post, root, extra_class=""):
	cls = f"post-entry {extra_class}".strip()
	return f"""<article class="{cls}">
	<header class="entry-header">
		<h2>{esc(post['title'])}</h2>
	</header>
	<section class="entry-content">
		<p>{esc(post['summary'])}...</p>
	</section>
	<footer class="entry-footer">{post_meta(post)}</footer>
	<a class="entry-link" aria-label="post link to {esc(post['title'])}" href="{root}{post['url']}"></a>
</article>"""


# ---------------------------------------------------------------- posts

def parse_front_matter(text):
	m = re.match(r"\s*<!--(.*?)-->", text, flags=re.S)
	if not m:
		raise ValueError("post is missing its front-matter comment")
	meta = {}
	for line in m.group(1).strip().splitlines():
		if ":" in line:
			key, value = line.split(":", 1)
			meta[key.strip()] = value.strip()
	return meta, text[m.end():]


def inline_figures(body):
	def repl(m):
		return (CONTENT / "figures" / f"{m.group(1)}.html").read_text()
	return re.sub(r"<!--fig:([\w-]+)-->", repl, body)


def add_heading_anchors(body):
	"""Give h1-h3 ids + hover anchors and collect them for the table of contents."""
	toc, seen = [], {}

	def repl(m):
		level, attrs, inner = int(m.group(1)), m.group(2), m.group(3)
		idm = re.search(r'id="([^"]+)"', attrs)
		hid = idm.group(1) if idm else slugify(inner)
		if hid in seen:
			seen[hid] += 1
			hid = f"{hid}-{seen[hid]}"
		else:
			seen[hid] = 0
		toc.append((level, hid, inner.strip()))
		return (
			f'<h{level} id="{hid}">{inner}'
			f'<a hidden class="anchor" aria-hidden="true" href="#{hid}">#</a></h{level}>'
		)

	body = re.sub(r"<h([1-3])((?:\s[^>]*)?)>(.*?)</h\1>", repl, body, flags=re.S)
	return body, toc


def render_toc(toc):
	if not toc:
		return ""
	base = min(level for level, _, _ in toc)
	out, depth = [], base - 1
	for level, hid, inner in toc:
		label = esc(strip_tags(inner))
		if level > depth:
			out.append("<ul>" * (level - depth))
		else:
			out.append("</li>" + "</ul></li>" * (depth - level))
		out.append(f'<li><a href="#{hid}" aria-label="{label}">{inner}</a>')
		depth = level
	out.append("</li>" + "</ul></li>" * (depth - base) + "</ul>")
	return f"""<div class="toc">
	<details>
		<summary accesskey="c" title="(Alt + C)"><span class="details">Table of Contents</span></summary>
		<div class="inner">{"".join(out)}</div>
	</details>
</div>"""


def citation_block(post):
	d = post["date"]
	url = SITE["base_url"] + post["url"]
	first_word = re.sub(r"[^a-z]", "", post["title"].split()[0].lower())
	key = post.get("cite_key") or f"{SITE['author_last'].lower()}{d.year}{first_word}"
	return f"""<h1>Citation</h1>
<p>Cited as:</p>
<blockquote>
<p>{esc(SITE['author_last'])}, {esc(SITE['author_first'])}. ({d:%b} {d.year}). {esc(post['title'])}. {esc(SITE['title'])}. {esc(url)}.</p>
</blockquote>
<p>Or</p>
<pre tabindex="0"><code class="language-bibtex">@article{{{key},
  title   = &#34;{esc(post['title'])}&#34;,
  author  = &#34;{esc(SITE['author_last'])}, {esc(SITE['author_first'])}&#34;,
  journal = &#34;{esc(SITE['base_url'].split('//')[-1].rstrip('/'))}&#34;,
  year    = &#34;{d.year}&#34;,
  month   = &#34;{d:%b}&#34;,
  url     = &#34;{esc(url)}&#34;
}}
</code></pre>
"""


def load_posts():
	posts = []
	for path in sorted((CONTENT / "posts").glob("*.html")):
		meta, body = parse_front_matter(path.read_text())
		post = {
			"slug": path.stem,
			"title": meta["title"],
			"date": datetime.strptime(meta["date"], "%Y-%m-%d"),
			"tags": [t.strip() for t in meta.get("tags", "").split(",") if t.strip()],
			"cite_key": meta.get("cite_key"),
			"url": f"posts/{path.stem}/",
		}
		body = inline_figures(body)
		plain = strip_tags(re.sub(r"<figure\b.*?</figure>", " ", body, flags=re.S))
		words = plain.split()
		post["minutes"] = max(1, math.ceil(len(words) / WPM))
		post["summary"] = meta.get("summary") or " ".join(words[:SUMMARY_WORDS])
		post["plain"] = plain
		cite = citation_block(post)
		if "<h1>References</h1>" in body:
			body = body.replace("<h1>References</h1>", cite + "<h1>References</h1>", 1)
		else:
			body += cite
		post["body"], post["toc"] = add_heading_anchors(body)
		posts.append(post)
	posts.sort(key=lambda p: p["date"], reverse=True)
	return posts


def render_post(post, newer, older):
	root = "../../"
	tags = "\n".join(
		f'\t\t<li><a href="{root}tags/{tag_slug(t)}/">{esc(t)}</a></li>' for t in post["tags"]
	)
	nav = ""
	if newer or older:
		nav = '<nav class="paginav">\n'
		if newer:
			nav += f'\t<a class="prev" href="{root}{newer["url"]}"><span class="title">« </span><br><span>{esc(newer["title"])}</span></a>\n'
		if older:
			nav += f'\t<a class="next" href="{root}{older["url"]}"><span class="title"> »</span><br><span>{esc(older["title"])}</span></a>\n'
		nav += "</nav>"
	from urllib.parse import quote
	u, t = quote(SITE["base_url"] + post["url"], safe=""), quote(post["title"], safe="")
	share = f"""<div class="share-buttons">
	<a target="_blank" rel="noopener noreferrer" aria-label="share {esc(post['title'])} on twitter" href="https://twitter.com/intent/tweet/?text={t}&amp;url={u}">{ICONS['twitter']}</a>
	<a target="_blank" rel="noopener noreferrer" aria-label="share {esc(post['title'])} on linkedin" href="https://www.linkedin.com/shareArticle?mini=true&amp;url={u}&amp;title={t}">{ICONS['linkedin']}</a>
	<a target="_blank" rel="noopener noreferrer" aria-label="share {esc(post['title'])} on facebook" href="https://facebook.com/sharer/sharer.php?u={u}">{ICONS['facebook']}</a>
</div>"""
	body = f"""<article class="post-single">
	<header class="post-header">
		<h1 class="post-title">{esc(post['title'])}</h1>
		<div class="post-meta">{post_meta(post)}</div>
	</header>
	{render_toc(post['toc'])}
	<div class="post-content">{post['body']}</div>
	<footer class="post-footer">
		<ul class="post-tags">
{tags}
		</ul>
{nav}
{share}
	</footer>
</article>"""
	return page(post["title"], body, root, description=post["summary"], math=True, code="<pre" in post["body"])


# ---------------------------------------------------------------- list pages

def render_home(posts):
	root = ""
	social = f'<a href="index.xml" target="_blank" rel="noopener noreferrer me" title="Rss">{ICONS["rss"]}</a>'
	if SITE["github"]:
		social += f'\n<a href="{SITE["github"]}" target="_blank" rel="noopener noreferrer me" title="Github">{ICONS["github"]}</a>'
	intro = f"""<article class="first-entry home-info">
	<header class="entry-header">
		<h1>{esc(SITE['welcome_title'])}</h1>
	</header>
	<section class="entry-content">
		<p>{esc(SITE['welcome_text'])}</p>
	</section>
	<footer class="entry-footer">
		<div class="social-icons">{social}</div>
	</footer>
</article>"""
	entries = "\n".join(post_entry(p, root) for p in posts)
	return page(SITE["title"], intro + "\n" + entries, root, body_class="list", math=True, active="Posts")


def render_archives(posts):
	root = "../"
	out = ['<header class="page-header"><h1>Archive</h1></header>']
	years = {}
	for p in posts:
		years.setdefault(p["date"].year, {}).setdefault(p["date"].month, []).append(p)
	for year, months in years.items():
		count = sum(len(v) for v in months.values())
		out.append(f'<div class="archive-year">\n<h2 class="archive-year-header">{year}<sup class="archive-count">&nbsp;&nbsp;{count}</sup></h2>')
		for month, items in months.items():
			name = items[0]["date"].strftime("%B")
			out.append(f'<div class="archive-month">\n<h3 class="archive-month-header">{name}<sup class="archive-count">&nbsp;&nbsp;{len(items)}</sup></h3>\n<div class="archive-posts">')
			for p in items:
				out.append(f"""<div class="archive-entry">
	<h3 class="archive-entry-title">{esc(p['title'])}</h3>
	<div class="archive-meta">{post_meta(p)}</div>
	<a class="entry-link" aria-label="post link to {esc(p['title'])}" href="{root}{p['url']}"></a>
</div>""")
			out.append("</div>\n</div>")
		out.append("</div>")
	return page("Archive", "\n".join(out), root, body_class="list", active="Archive")


def render_tags(posts):
	tags = {}
	for p in posts:
		for t in p["tags"]:
			tags.setdefault(tag_slug(t), [t, []])[1].append(p)
	pages = {}
	items = "\n".join(
		f'\t<li><a href="{slug}/">{esc(name.lower())} <sup><strong><sup>{len(ps)}</sup></strong></sup> </a></li>'
		for slug, (name, ps) in sorted(tags.items())
	)
	pages["tags/index.html"] = page(
		"Tags",
		f'<header class="page-header"><h1>Tags</h1></header>\n<ul class="terms-tags">\n{items}\n</ul>',
		"../", body_class="list", active="Tags",
	)
	for slug, (name, ps) in tags.items():
		root = "../../"
		entries = "\n".join(post_entry(p, root, "tag-entry") for p in ps)
		pages[f"tags/{slug}/index.html"] = page(
			name, f'<header class="page-header"><h1>{esc(name)}</h1></header>\n{entries}',
			root, body_class="list", math=True, active="Tags",
		)
	return pages


def render_search():
	body = f"""<header class="page-header">
	<h1>Search {ICONS['search']}</h1>
	<div class="post-meta"></div>
</header>
<div id="searchbox">
	<input id="searchInput" data-root="../" autofocus placeholder="Search ↵" aria-label="search" type="search" autocomplete="off">
	<ul id="searchResults" aria-label="search results"></ul>
</div>"""
	return page("Search", body, "../", body_class="list", active="Search")


def render_faq():
	content = (CONTENT / "faq.html").read_text()
	body = f'<header class="page-header"><h1>FAQ</h1></header>\n<div class="post-content">\n{content}\n</div>'
	return page("FAQ", body, "../", active="FAQ")


def render_rss(posts):
	items = "\n".join(
		f"""<item>
	<title>{esc(p['title'])}</title>
	<link>{SITE['base_url']}{p['url']}</link>
	<pubDate>{format_datetime(p['date'].astimezone())}</pubDate>
	<guid>{SITE['base_url']}{p['url']}</guid>
	<description>{esc(p['summary'])}...</description>
</item>"""
		for p in posts
	)
	return f"""<?xml version="1.0" encoding="utf-8" standalone="yes"?>
<rss version="2.0">
<channel>
	<title>{esc(SITE['title'])}</title>
	<link>{SITE['base_url']}</link>
	<description>{esc(SITE['description'])}</description>
	<language>en</language>
{items}
</channel>
</rss>
"""


# ---------------------------------------------------------------- main

def main():
	if OUT.exists():
		shutil.rmtree(OUT)
	shutil.copytree(STATIC, OUT)
	posts = load_posts()
	files = {
		"index.html": render_home(posts),
		"archives/index.html": render_archives(posts),
		"search/index.html": render_search(),
		"faq/index.html": render_faq(),
		"index.xml": render_rss(posts),
		"index.json": json.dumps(
			[{"title": p["title"], "permalink": p["url"], "tags": p["tags"], "content": p["plain"]} for p in posts],
			ensure_ascii=False,
		),
		**render_tags(posts),
	}
	for i, p in enumerate(posts):
		newer = posts[i - 1] if i > 0 else None
		older = posts[i + 1] if i + 1 < len(posts) else None
		files[f"{p['url']}index.html"] = render_post(p, newer, older)
	for rel, text in files.items():
		dest = OUT / rel
		dest.parent.mkdir(parents=True, exist_ok=True)
		dest.write_text(text)
	print(f"Built {len(posts)} post(s), {len(files)} files -> {OUT.relative_to(ROOT)}/")


if __name__ == "__main__":
	main()
