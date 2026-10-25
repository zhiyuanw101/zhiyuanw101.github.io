---
name: blog-maintain
description: Write, update, fix or publish posts on Zhiyuan's Log (this repo's Lil'Log-style blog). Use when asked to turn a source (course chapter, paper, blog, notes) into a new post, revise or extend an existing post, add or fix a figure, change the site's layout or config, or publish/deploy the blog. Posts are always written in English, whatever language the request is in.
---

# Blog maintenance

Read [`AGENTS.md`](../../../AGENTS.md) first: it holds the repo layout, the hard rules (English only,
own words, correctness), the post markup and the writing style. This skill is the workflow.

## A. New post from a source

1. **Read the whole source.** Course notes are often split across sub-pages; fetch every section, not
   just the landing page. Note the running example, the key results and any errors.
2. **Outline in the Lil'Log shape**: motivation paragraphs, Notation table (if math-heavy), `<h1>`
   sections that follow the logic (not necessarily the source's order), Quick Summary, References.
   Plan the figures: which ideas need a picture (geometry, a simulation, a decomposition).
3. **Create the file** `content/posts/<today>-<short-slug>.html` with the front-matter comment
   (`title`, `date`, `tags`; reuse existing tags where they fit, e.g. `Statistics`, `Math-Heavy`).
4. **Write the body in English**, in your own words, with derivations filled in. Cite the source as
   [1] and add standard textbooks or papers only when you are sure of the reference.
5. **Figures**: add one function per figure to `tools/figures.py`, register it in `main()`, run
   `python3 tools/figures.py`, and place each with `<!--fig:name-->`. Refer to them as "(Fig. N)" in
   order of appearance.
6. **Build and verify** (section D), then **publish** (section E).

## B. Update an existing post

- Edit the post file; keep its date and URL unchanged.
- For a substantive change, add an update note as the first paragraph of the body:
  `<p><span class="update">[Updated on YYYY-MM-DD: Added a section on ridge regression.]</span></p>`
  (multiple notes are separated with `<br/>` inside one `<p>`). Typos need no note.
- Build, verify and publish.

## C. Site or layout changes

- Site name, author, `base_url`, menu and templates live in `tools/build.py` (`SITE`, `MENU`, `page()`).
- CSS overrides go in the `DARK_STYLE` block in `tools/build.py`; don't edit the upstream stylesheet.
- Check the change on the home page, a post, Archive, Tags, Search and FAQ, at widths of 375, 1100
  and 1440 px, in light and dark mode.

## D. Verify

```bash
python3 tools/build.py                 # must print "Built N post(s)"; fails on non-English text
python3 -m http.server 8765 -d public
```

In a browser at http://localhost:8765:

- The post opens from the home page card, the Archive and its tag pages, and Search finds it.
- MathJax renders with no errors: `document.querySelectorAll('mjx-merror').length === 0`.
- Every in-page link resolves:
  `[...document.querySelectorAll('.post-content a[href^="#"]')].filter(a => !document.getElementById(decodeURIComponent(a.hash.slice(1))))`
  returns an empty list.
- Figures render, labels don't overlap, and figure numbers match the "(Fig. N)" references.
- No horizontal scrolling at phone width; text is readable in dark mode.
- Reread the text once for English, accuracy and tone.

## E. Publish

```bash
git add -A
git commit -m "Add post: <title>"
git push origin master
gh run list -R zhiyuanw101/zhiyuanw101.github.io --limit 1     # wait for "completed success"
```

Then open `https://zhiyuanw101.github.io/posts/<slug>/` and spot-check it. If the run fails, read
`gh run view <id> --log-failed`, fix, and push again. Never commit `public/` or force-push `master`.
