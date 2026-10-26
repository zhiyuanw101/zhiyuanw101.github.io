#!/usr/bin/env python3
"""Writing-style checks based on ASD-STE100 Simplified Technical English.

Usage:  python3 tools/style_lint.py [files...]   # defaults to content/posts/*.html and content/faq.html
tools/build.py runs the same checks and stops on any error.

Checked (prose only: math, code, SVG and the References section are skipped):
  - descriptive sentences have at most 25 words (a formula counts as one word)
  - paragraphs have at most 6 sentences
  - no emotive words, intensifiers, idioms or filler (BANNED below)
"""

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MAX_SENTENCE_WORDS = 25
MAX_PARAGRAPH_SENTENCES = 6

# Words and phrases that express feeling or emphasis instead of information, or are idioms.
# Matched case-insensitively on word boundaries. Extend this list when you find more.
BANNED = [
	# intensifiers and hedges
	"perfectly", "at all", "really", "very", "simply", "just", "quite", "actually", "basically",
	"essentially", "literally", "obviously", "clearly", "of course", "totally", "extremely",
	"incredibly", "highly", "hugely", "truly", "surely", "certainly", "definitely", "pretty",
	# feelings and value judgments
	"beautiful", "beautifully", "nice", "nicely", "elegant", "elegantly", "amazing", "remarkable",
	"remarkably", "surprising", "surprisingly", "interesting", "interestingly", "insidious",
	"unfortunately", "fortunately", "hopefully", "sadly", "happily", "familiar", "classic",
	"famous", "powerful", "magic", "magical", "trick", "tricks", "neat", "cool", "awesome",
	"painful", "annoying", "dangerous", "scary", "damage", "harm", "misbehave", "misbehaves",
	# idioms and figurative verbs
	"in disguise", "for free", "blows up", "blow up", "marches", "kills", "playground",
	"the whole point", "at the end of the day", "boils down", "under the hood", "a lot of",
	"lots of", "big picture", "goes wrong", "never quite", "window onto", "patch",
	# filler and signposting
	"let us", "let's", "worth", "keep in mind", "it turns out", "needless to say",
	"in other words", "as we can see", "note that", "it is easy to see", "first encounter",
	"to keep things concrete",
]
BANNED_RE = re.compile(r"\b(" + "|".join(re.escape(w) for w in sorted(BANNED, key=len, reverse=True)) + r")\b", re.I)

ABBREVIATIONS = ["e.g.", "i.e.", "vs.", "et al.", "Fig.", "cf.", "etc.", "approx.", "resp.", "ed.", "No."]
BLOCK_TAGS = r"p|li|td|th|figcaption|summary|h[1-6]|blockquote|div"


def prose_blocks(text):
	"""Yield (line_number, plain_text) for every block of prose in an HTML fragment."""
	refs = re.search(r"<h1>References</h1>", text)
	if refs:
		text = text[:refs.start()]
	text = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group().count("\n"), text, flags=re.S)
	for tag in ("pre", "svg", "script", "style"):
		text = re.sub(rf"<{tag}\b.*?</{tag}>", lambda m: "\n" * m.group().count("\n"), text, flags=re.S)
	for m in re.finditer(rf"<({BLOCK_TAGS})\b[^>]*>(.*?)</\1>", text, flags=re.S):
		inner = m.group(2)
		if re.search(rf"<({BLOCK_TAGS})\b", inner):
			continue  # container: its children are checked on their own
		line = text.count("\n", 0, m.start()) + 1
		inner = re.sub(r"\$\$.*?\$\$", " FORMULA ", inner, flags=re.S)
		inner = re.sub(r"\$[^$]+\$", "FORMULA", inner)
		plain = html.unescape(re.sub(r"<[^>]+>", " ", inner))
		plain = re.sub(r"\s+", " ", plain).strip()
		if plain:
			yield line, plain, m.group(1)


def sentences(plain):
	protected = plain
	for abbr in ABBREVIATIONS:
		# whole tokens only, so "ed." does not match "included."
		protected = re.sub(r"(?<!\w)" + re.escape(abbr), abbr.replace(".", "․"), protected)
	parts = re.split(r"(?<=[.!?])\s+(?=[A-Z(\"“]|FORMULA)", protected)
	return [p.replace("․", ".").strip() for p in parts if p.strip()]


def lint(text, source):
	errors = []
	for line, plain, tag in prose_blocks(text):
		for m in BANNED_RE.finditer(plain):
			errors.append(f"{source}:{line}: avoid \"{m.group(1)}\" (emotive, intensifier, idiom or filler): ...{plain[max(0, m.start() - 30):m.end() + 30]}...")
		sents = sentences(plain)
		if tag == "p" and len(sents) > MAX_PARAGRAPH_SENTENCES:
			errors.append(f"{source}:{line}: paragraph has {len(sents)} sentences (max {MAX_PARAGRAPH_SENTENCES}): {plain[:70]}...")
		for s in sents:
			n = len(re.findall(r"[A-Za-z0-9][\w'’-]*", s))
			if n > MAX_SENTENCE_WORDS:
				errors.append(f"{source}:{line}: sentence has {n} words (max {MAX_SENTENCE_WORDS}): {s[:90]}...")
	return errors


def main(paths):
	if not paths:
		paths = sorted((ROOT / "content" / "posts").glob("*.html")) + [ROOT / "content" / "faq.html"]
	errors = []
	for p in map(Path, paths):
		errors += lint(p.read_text(), p.relative_to(ROOT) if p.is_absolute() else p)
	print("\n".join(errors) if errors else "style: OK")
	return 1 if errors else 0


if __name__ == "__main__":
	sys.exit(main(sys.argv[1:]))
