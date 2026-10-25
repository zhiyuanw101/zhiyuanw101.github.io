# Zhiyuan's Log

A static blog with the layout of a Hugo + PaperMod site (home cards, archive, tags, search, FAQ, posts with ToC, citation block and references).

```
content/posts/YYYY-MM-DD-slug.html   post body + front-matter comment (title, date, tags)
content/figures/*.html               figure fragments, included in a post with <!--fig:name-->
content/faq.html                     FAQ page body
static/                              CSS / JS copied as-is
tools/figures.py                     regenerates the SVG figures for the linear regression post
tools/build.py                       builds everything into public/
```

Build and preview:

    python3 tools/figures.py
    python3 tools/build.py
    python3 -m http.server 8000 -d public

## Publishing

The site is served by GitHub Pages at https://zhiyuanw101.github.io/. Every push to `master` runs
`.github/workflows/deploy.yml`, which builds the site with `tools/build.py` and deploys `public/`.
The previous Jekyll blog is kept on the `jekyll-archive` branch.

Write a new post by adding another file to `content/posts/` (use `<h1>` for sections, `<h2>`/`<h3>` for subsections,
`$...$` / `$$...$$` for math, and end with `<h1>References</h1>`; the citation block is inserted automatically).
Then commit and `git push`; the post is live a minute or two later.
