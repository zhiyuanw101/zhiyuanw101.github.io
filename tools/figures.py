#!/usr/bin/env python3
"""Generate the inline SVG figures for the posts (stdlib only).

Usage:  python3 tools/figures.py     # writes content/figures/*.html (figure fragments)
Colours use currentColor for ink so the figures follow the light/dark theme.
"""

import math
import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "content" / "figures"
BLUE = "#3b7ddd"
ORANGE = "#e8833a"
GREEN = "#3aa17e"
GREY = "#999"
YELLOW = "#c2b866"
PINK = "#d97f9f"
LAVENDER = "#9387cf"


# ---------------------------------------------------------------- tiny linear algebra

def solve(a, b):
	"""Solve a x = b with Gaussian elimination and partial pivoting."""
	n = len(a)
	m = [row[:] + [b[i]] for i, row in enumerate(a)]
	for c in range(n):
		p = max(range(c, n), key=lambda r: abs(m[r][c]))
		m[c], m[p] = m[p], m[c]
		for r in range(c + 1, n):
			f = m[r][c] / m[c][c]
			for k in range(c, n + 1):
				m[r][k] -= f * m[c][k]
	x = [0.0] * n
	for r in range(n - 1, -1, -1):
		x[r] = (m[r][n] - sum(m[r][k] * x[k] for k in range(r + 1, n))) / m[r][r]
	return x


def ols(X, y):
	"""Least squares via the normal equations; returns (beta, fitted values)."""
	p = len(X[0])
	xtx = [[sum(row[i] * row[j] for row in X) for j in range(p)] for i in range(p)]
	xty = [sum(row[i] * yi for row, yi in zip(X, y)) for i in range(p)]
	beta = solve(xtx, xty)
	return beta, [sum(b * v for b, v in zip(beta, row)) for row in X]


def svg(width, height, inner, label):
	return (
		f'<figure>\n<svg viewBox="0 0 {width} {height}" xmlns="http://www.w3.org/2000/svg" '
		f'role="img" aria-label="{label}" font-size="14">\n{inner}\n</svg>\n'
	)


# ---------------------------------------------------------------- figure 1: LS fit with residuals

def fig_ls_fit():
	rng = random.Random(11)
	xs = sorted(rng.uniform(0.5, 9.5) for _ in range(18))
	ys = [1.5 + 0.55 * x + rng.gauss(0, 0.9) for x in xs]
	(b0, b1), fitted = ols([[1, x] for x in xs], ys)

	W, H, L, R, T, B = 640, 340, 60, 20, 20, 50
	sx = lambda x: L + x / 10 * (W - L - R)
	sy = lambda y: H - B - y / 8 * (H - T - B)
	g = []
	g.append(f'<line x1="{L}" y1="{H-B}" x2="{W-R}" y2="{H-B}" stroke="currentColor"/>')
	g.append(f'<line x1="{L}" y1="{H-B}" x2="{L}" y2="{T}" stroke="currentColor"/>')
	for x, y, f in zip(xs, ys, fitted):
		g.append(f'<line x1="{sx(x):.1f}" y1="{sy(y):.1f}" x2="{sx(x):.1f}" y2="{sy(f):.1f}" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="4 3"/>')
	g.append(f'<line x1="{sx(0):.1f}" y1="{sy(b0):.1f}" x2="{sx(10):.1f}" y2="{sy(b0 + 10 * b1):.1f}" stroke="{BLUE}" stroke-width="2.5"/>')
	for x, y in zip(xs, ys):
		g.append(f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="4.5" fill="currentColor" fill-opacity="0.85"/>')
	# legend
	lx, ly = L + 20, T + 14
	g.append(f'<line x1="{lx}" y1="{ly}" x2="{lx + 28}" y2="{ly}" stroke="{BLUE}" stroke-width="2.5"/>')
	g.append(f'<text x="{lx + 36}" y="{ly + 5}" fill="currentColor">fitted line <tspan font-style="italic">ŷ = β̂<tspan baseline-shift="sub" font-size="10">0</tspan> + β̂<tspan baseline-shift="sub" font-size="10">1</tspan>x</tspan></text>')
	g.append(f'<line x1="{lx}" y1="{ly + 24}" x2="{lx + 28}" y2="{ly + 24}" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="4 3"/>')
	g.append(f'<text x="{lx + 36}" y="{ly + 29}" fill="currentColor">residual <tspan font-style="italic">r<tspan baseline-shift="sub" font-size="10">i</tspan> = y<tspan baseline-shift="sub" font-size="10">i</tspan> − ŷ<tspan baseline-shift="sub" font-size="10">i</tspan></tspan></text>')
	g.append(f'<text x="{(L + W - R) / 2}" y="{H - 14}" fill="currentColor" text-anchor="middle" font-style="italic">x</text>')
	g.append(f'<text x="{L - 20}" y="{(T + H - B) / 2}" fill="currentColor" text-anchor="middle" font-style="italic">y</text>')
	return svg(W, H, "\n".join(g), "Least squares line with residuals") + (
		"<figcaption>Least squares picks the line (blue) that minimizes the sum of squared "
		"vertical distances between observations and the line. The dashed orange segments are the residuals.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- figure 2: geometry of least squares

def fig_geometry():
	W, H = 640, 360
	O = (250, 290)
	yhat = (470, 240)
	y = (470, 60)
	x1 = (400, 322)
	x2 = (208, 214)
	plane = [(60, 300), (420, 340), (600, 220), (240, 180)]
	sub = lambda s: f'<tspan baseline-shift="sub" font-size="10">{s}</tspan>'
	g = []
	g.append('<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>')
	pts = " ".join(f"{x},{y}" for x, y in plane)
	g.append(f'<polygon points="{pts}" fill="{BLUE}" fill-opacity="0.12" stroke="{BLUE}" stroke-opacity="0.6"/>')
	g.append(f'<text x="92" y="298" fill="{BLUE}" font-style="italic">𝒞(X)</text>')
	for px, py in (x1, x2):
		g.append(f'<line x1="{O[0]}" y1="{O[1]}" x2="{px}" y2="{py}" stroke="{GREY}" stroke-width="1.8" marker-end="url(#ah)"/>')
	g.append(f'<text x="{x1[0] - 4}" y="{x1[1] + 18}" fill="{GREY}" font-style="italic">X{sub(1)}</text>')
	g.append(f'<text x="{x2[0] + 10}" y="{x2[1] - 6}" fill="{GREY}" font-style="italic">X{sub(2)}</text>')
	g.append(f'<line x1="{O[0]}" y1="{O[1]}" x2="{y[0]}" y2="{y[1]}" stroke="currentColor" stroke-width="2.2" marker-end="url(#ah)"/>')
	g.append(f'<line x1="{O[0]}" y1="{O[1]}" x2="{yhat[0]}" y2="{yhat[1]}" stroke="{BLUE}" stroke-width="2.2" marker-end="url(#ah)"/>')
	g.append(f'<line x1="{yhat[0]}" y1="{yhat[1]}" x2="{y[0]}" y2="{y[1]}" stroke="{ORANGE}" stroke-width="2.2" stroke-dasharray="6 4"/>')
	# right-angle marker at y-hat
	g.append(f'<polyline points="{yhat[0]},{yhat[1] - 14} {yhat[0] + 14},{yhat[1] - 12} {yhat[0] + 14},{yhat[1] + 2}" fill="none" stroke="currentColor" stroke-width="1.2"/>')
	g.append(f'<circle cx="{O[0]}" cy="{O[1]}" r="3" fill="currentColor"/>')
	g.append(f'<text x="{O[0] - 18}" y="{O[1] + 4}" fill="currentColor">0</text>')
	g.append(f'<text x="{y[0] + 10}" y="{y[1] + 4}" fill="currentColor" font-weight="bold" font-style="italic">y</text>')
	g.append(f'<text x="{yhat[0] + 22}" y="{yhat[1] + 18}" fill="{BLUE}" font-style="italic">ŷ = Xβ̂ = Hy</text>')
	g.append(f'<text x="{y[0] + 12}" y="{(y[1] + yhat[1]) / 2 + 5}" fill="{ORANGE}" font-style="italic">r = y − ŷ = (I − H)y</text>')
	return svg(W, H, "\n".join(g), "Least squares as orthogonal projection") + (
		"<figcaption>Least squares as an orthogonal projection. The fitted vector $\\hat{\\mathbf{y}}$ is the point in "
		"the column space $\\mathcal{C}(\\mathbf{X})$ closest to $\\mathbf{y}$, and the residual $\\mathbf{r}$ is "
		"perpendicular to the subspace.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- figure 3: R^2 inflation

def fig_r2():
	rng = random.Random(3)
	n, K = 42, 30
	X = [[1, rng.gauss(0, 1), rng.gauss(0, 1)] for _ in range(n)]
	y = [1 + 1.0 * r[1] - 0.6 * r[2] + rng.gauss(0, 1.5) for r in X]
	noise = [[rng.gauss(0, 1) for _ in range(K)] for _ in range(n)]
	ybar = sum(y) / n
	tss = sum((v - ybar) ** 2 for v in y)
	r2, adj = [], []
	for k in range(K + 1):
		Xk = [row + noise[i][:k] for i, row in enumerate(X)]
		_, f = ols(Xk, y)
		rss = sum((a - b) ** 2 for a, b in zip(y, f))
		p = 2 + k
		r2.append(1 - rss / tss)
		adj.append(1 - (rss / (n - p - 1)) / (tss / (n - 1)))

	W, H, L, R, T, B = 640, 340, 60, 30, 20, 55
	ymin, ymax = -0.2, 1.0
	sx = lambda k: L + k / K * (W - L - R)
	sy = lambda v: H - B - (v - ymin) / (ymax - ymin) * (H - T - B)
	g = []
	for v in (-0.2, 0, 0.2, 0.4, 0.6, 0.8, 1.0):
		g.append(f'<line x1="{L}" y1="{sy(v):.1f}" x2="{W - R}" y2="{sy(v):.1f}" stroke="currentColor" stroke-opacity="{0.5 if v == 0 else 0.12}"/>')
		g.append(f'<text x="{L - 8}" y="{sy(v) + 5:.1f}" fill="currentColor" text-anchor="end" font-size="12">{v:.1f}</text>')
	for k in range(0, K + 1, 5):
		g.append(f'<text x="{sx(k):.1f}" y="{H - B + 20}" fill="currentColor" text-anchor="middle" font-size="12">{k}</text>')
	g.append(f'<line x1="{L}" y1="{H - B}" x2="{W - R}" y2="{H - B}" stroke="currentColor"/>')
	for series, colour in ((r2, BLUE), (adj, ORANGE)):
		pts = " ".join(f"{sx(k):.1f},{sy(v):.1f}" for k, v in enumerate(series))
		g.append(f'<polyline points="{pts}" fill="none" stroke="{colour}" stroke-width="2.5"/>')
		for k, v in enumerate(series):
			g.append(f'<circle cx="{sx(k):.1f}" cy="{sy(v):.1f}" r="2.8" fill="{colour}"/>')
	g.append(f'<text x="{sx(K) - 4:.1f}" y="{sy(r2[-1]) + 22:.1f}" fill="{BLUE}" text-anchor="end">R²</text>')
	g.append(f'<text x="{sx(K) - 4:.1f}" y="{sy(adj[-1]) + 24:.1f}" fill="{ORANGE}" text-anchor="end">adjusted R²</text>')
	g.append(f'<text x="{(L + W - R) / 2}" y="{H - 10}" fill="currentColor" text-anchor="middle">number of pure-noise predictors added</text>')
	return svg(W, H, "\n".join(g), "R squared keeps increasing with noise predictors") + (
		"<figcaption>One simulated data set ($n=42$, two real predictors). Each column of pure noise can only "
		"lower the RSS, so $R^2$ (blue) increases toward 1. The adjusted $R^2$ (orange) charges one degree of "
		"freedom per predictor and decreases.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- figure 4: partial F decomposition

def fig_partial_f():
	W, H = 640, 210
	L, R, y0, h = 30, 610, 70, 44
	tss = R - L
	a, b = L + 0.52 * tss, L + 0.66 * tss  # reduced-model explained | extra by full | RSS_full
	g = []
	g.append(f'<rect x="{L}" y="{y0}" width="{a - L}" height="{h}" fill="{BLUE}" fill-opacity="0.75"/>')
	g.append(f'<rect x="{a}" y="{y0}" width="{b - a}" height="{h}" fill="{GREEN}" fill-opacity="0.85"/>')
	g.append(f'<rect x="{b}" y="{y0}" width="{R - b}" height="{h}" fill="{GREY}" fill-opacity="0.45"/>')
	g.append(f'<text x="{(L + a) / 2}" y="{y0 + 28}" fill="#fff" text-anchor="middle">TSS − RSS<tspan baseline-shift="sub" font-size="10">0</tspan>: explained by reduced model</text>')
	g.append(f'<text x="{(b + R) / 2}" y="{y0 + 28}" fill="currentColor" text-anchor="middle" font-style="italic">RSS<tspan baseline-shift="sub" font-size="10">a</tspan></text>')

	def brace(x1, x2, yb, up, label, colour):
		d = -1 if up else 1
		g.append(f'<path d="M{x1},{yb} q0,{8 * d} 8,{8 * d} L{(x1 + x2) / 2 - 8},{yb + 8 * d} q8,0 8,{8 * d} q0,{-8 * d} 8,{-8 * d} L{x2 - 8},{yb + 8 * d} q8,0 8,{-8 * d}" fill="none" stroke="{colour}" stroke-width="1.5"/>')
		ty = yb + (-26 if up else 36)
		g.append(f'<text x="{(x1 + x2) / 2}" y="{ty}" fill="{colour}" text-anchor="middle" font-style="italic">{label}</text>')

	brace(L, R, y0 - 6, True, 'TSS = Σ<tspan baseline-shift="sub" font-size="10">i</tspan> (y<tspan baseline-shift="sub" font-size="10">i</tspan> − ȳ)²', "currentColor")
	brace(a, R, y0 + h + 6, False, 'RSS<tspan baseline-shift="sub" font-size="10">0</tspan> (reduced model)', GREY)
	g.append(f'<line x1="{(a + b) / 2}" y1="{y0 + h + 4}" x2="{(a + b) / 2}" y2="{y0 + h + 62}" stroke="{GREEN}" stroke-dasharray="3 3"/>')
	g.append(f'<text x="{(a + b) / 2}" y="{y0 + h + 80}" fill="{GREEN}" text-anchor="middle" font-style="italic">RSS<tspan baseline-shift="sub" font-size="10">0</tspan> − RSS<tspan baseline-shift="sub" font-size="10">a</tspan>: extra variation captured by the full model</text>')
	return svg(W, H, "\n".join(g), "Decomposition behind the partial F test") + (
		"<figcaption>The bar is TSS, the total variation of $Y$ around its mean. "
		"Blue: $\\text{TSS} - \\text{RSS}_0$, the part that the reduced model explains. "
		"Green: $\\text{RSS}_0 - \\text{RSS}_a$, the extra part that the full model explains. "
		"Grey: $\\text{RSS}_a$, the part that the full model does not explain. "
		"The partial $F$ test compares green with grey, each scaled by its degrees of freedom.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- figure: binomial null distribution (tests post)

def fig_binomial_test():
	from math import comb
	n, obs = 100, 60
	lo_k, hi_k = 30, 70
	pmf = {k: comb(n, k) / 2 ** n for k in range(lo_k, hi_k + 1)}
	W, H, L, R, T, B = 640, 330, 50, 20, 30, 50
	bw = (W - L - R) / (hi_k - lo_k + 1)
	ymax = 0.085
	sx = lambda k: L + (k - lo_k) * bw
	sy = lambda v: H - B - v / ymax * (H - T - B)
	g = []
	for v in (0, 0.02, 0.04, 0.06, 0.08):
		g.append(f'<line x1="{L}" y1="{sy(v):.1f}" x2="{W - R}" y2="{sy(v):.1f}" stroke="currentColor" stroke-opacity="{0.5 if v == 0 else 0.12}"/>')
		g.append(f'<text x="{L - 8}" y="{sy(v) + 4:.1f}" fill="currentColor" text-anchor="end" font-size="12">{v:.2f}</text>')
	for k, v in pmf.items():
		colour = ORANGE if k >= obs else BLUE
		opacity = 0.9 if k >= obs else 0.45
		g.append(f'<rect x="{sx(k) + 1:.1f}" y="{sy(v):.1f}" width="{bw - 2:.1f}" height="{sy(0) - sy(v):.1f}" fill="{colour}" fill-opacity="{opacity}"/>')
	for k in range(lo_k, hi_k + 1, 5):
		g.append(f'<text x="{sx(k) + bw / 2:.1f}" y="{H - B + 18}" fill="currentColor" text-anchor="middle" font-size="12">{k}</text>')
	tail = sum(comb(n, k) for k in range(obs, n + 1)) / 2 ** n
	g.append(f'<line x1="{sx(obs):.1f}" y1="{T}" x2="{sx(obs):.1f}" y2="{sy(0):.1f}" stroke="{ORANGE}" stroke-width="1.5" stroke-dasharray="5 4"/>')
	g.append(f'<text x="{sx(obs) + 8:.1f}" y="{T + 14}" fill="{ORANGE}">observed: 60 heads</text>')
	g.append(f'<text x="{sx(obs) + 8:.1f}" y="{T + 34}" fill="{ORANGE}">p = P(X ≥ 60) = {tail:.3f}</text>')
	g.append(f'<text x="{(L + W - R) / 2}" y="{H - 10}" fill="currentColor" text-anchor="middle">number of heads in 100 flips of a fair coin</text>')
	return svg(W, H, "\n".join(g), "Binomial null distribution with the p-value tail shaded") + (
		"<figcaption>The null distribution of the number of heads, Binomial(100, 0.5). The p-value is the total "
		"probability of the shaded bars: results at least as extreme as the observed 60 heads.</figcaption>\n</figure>\n"
	)


SUB = lambda s: f'<tspan baseline-shift="sub" font-size="10">{s}</tspan>'
SUP = lambda s: f'<tspan baseline-shift="super" font-size="10">{s}</tspan>'
ARROW_DEFS = ('<defs><marker id="{id}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
	'orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>')


# ---------------------------------------------------------------- pi0 post: architecture

def fig_pi0_architecture():
	W, H = 640, 400
	g = [ARROW_DEFS.format(id="ah-arch")]
	groups = [  # (x0, x1, label, expert)
		(20, 236, "camera images", 0), (242, 394, "command ℓ", 0),
		(404, 456, "state", 1), (462, 620, "noisy actions A" + SUP("τ"), 1),
	]
	colour = (BLUE, ORANGE)
	y0, h = 30, 36
	for x0, x1, label, e in groups:
		g.append(f'<rect x="{x0}" y="{y0}" width="{x1 - x0}" height="{h}" rx="4" fill="{colour[e]}" fill-opacity="0.18" stroke="{colour[e]}"/>')
		g.append(f'<text x="{(x0 + x1) / 2}" y="{y0 + 23}" fill="currentColor" text-anchor="middle">{label}</text>')
	# one layer
	ly0, ly1 = 104, 300
	g.append(f'<rect x="12" y="{ly0}" width="616" height="{ly1 - ly0}" rx="8" fill="none" stroke="currentColor" stroke-opacity="0.45" stroke-dasharray="6 4"/>')
	g.append(f'<text x="22" y="{ly0 + 18}" fill="currentColor" fill-opacity="0.75" font-size="12">one transformer layer (repeated)</text>')
	vx0, vx1, ex0, ex1 = 20, 394, 404, 620
	for row, (yy, hh, left, right) in enumerate((
		(ly0 + 28, 40, "Q, K, V projections (VLM weights)", "Q, K, V (expert)"),
		(ly0 + 82, 40, None, None),
		(ly0 + 136, 50, "output projection + MLP (VLM weights)", "proj. + MLP (expert)"),
	)):
		if left is None:
			g.append(f'<rect x="{vx0}" y="{yy}" width="{ex1 - vx0}" height="{hh}" rx="4" fill="{GREEN}" fill-opacity="0.2" stroke="{GREEN}"/>')
			g.append(f'<text x="{(vx0 + ex1) / 2}" y="{yy + 25}" fill="currentColor" text-anchor="middle">shared self-attention over all tokens (block-causal mask)</text>')
			continue
		for x0, x1, text, c in ((vx0, vx1, left, BLUE), (ex0, ex1, right, ORANGE)):
			g.append(f'<rect x="{x0}" y="{yy}" width="{x1 - x0}" height="{hh}" rx="4" fill="{c}" fill-opacity="0.18" stroke="{c}"/>')
			g.append(f'<text x="{(x0 + x1) / 2}" y="{yy + hh / 2 + 5}" fill="currentColor" text-anchor="middle" font-size="13">{text}</text>')
	for x in ((vx0 + vx1) / 2, (ex0 + ex1) / 2):
		g.append(f'<line x1="{x}" y1="{y0 + h + 4}" x2="{x}" y2="{ly0 + 26}" stroke="currentColor" stroke-opacity="0.6" marker-end="url(#ah-arch)"/>')
	# outputs
	ax = (ex0 + ex1) / 2
	g.append(f'<line x1="{ax}" y1="{ly1}" x2="{ax}" y2="{ly1 + 36}" stroke="{ORANGE}" stroke-width="1.6" marker-end="url(#ah-arch)"/>')
	g.append(f'<text x="{ax}" y="{ly1 + 56}" fill="currentColor" text-anchor="middle">linear → v' + SUB("θ") + '</text>')
	g.append(f'<text x="{(vx0 + vx1) / 2}" y="{ly1 + 30}" fill="currentColor" fill-opacity="0.75" text-anchor="middle" font-size="12">outputs at these positions are not used</text>')
	g.append(f'<text x="{(vx0 + vx1) / 2}" y="{ly1 + 56}" fill="{BLUE}" text-anchor="middle">VLM: initialized from PaliGemma (3B)</text>')
	g.append(f'<text x="{ax}" y="{ly1 + 80}" fill="{ORANGE}" text-anchor="middle">action expert: new, ~300M</text>')
	return svg(W, H, "\n".join(g), "pi0 architecture: one transformer with two sets of weights") + (
		"<figcaption>The $\\pi_0$ model is one transformer over one token sequence. Image and text tokens (blue) use the "
		"VLM weights. State and action tokens (orange) use the smaller action expert. The two sets of weights interact "
		"only inside self-attention (green). The outputs at the action positions form the velocity "
		"$\\mathbf{v}_\\theta$.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- pi0 post: one training pair in 2-D

def fig_fm_path():
	W, H, L, R, T, B = 640, 330, 60, 30, 20, 50
	xmin, xmax, ymin, ymax = -1.9, 2.6, 0.4, 1.9
	sx = lambda x: L + (x - xmin) / (xmax - xmin) * (W - L - R)
	sy = lambda y: H - B - (y - ymin) / (ymax - ymin) * (H - T - B)
	eps, A, tau = (-1.0, 0.8), (2.0, 1.5), 0.5
	pt = tuple(tau * a + (1 - tau) * e for a, e in zip(A, eps))
	vel = tuple(a - e for a, e in zip(A, eps))
	g = [ARROW_DEFS.format(id="ah-fm")]
	g.append(f'<line x1="{L}" y1="{H - B}" x2="{W - R}" y2="{H - B}" stroke="currentColor"/>')
	g.append(f'<line x1="{L}" y1="{H - B}" x2="{L}" y2="{T}" stroke="currentColor"/>')
	for x in (-1, 0, 1, 2):
		g.append(f'<text x="{sx(x):.1f}" y="{H - B + 18}" fill="currentColor" text-anchor="middle" font-size="12">{x}</text>')
	for y in (0.5, 1.0, 1.5):
		g.append(f'<text x="{L - 8}" y="{sy(y) + 4:.1f}" fill="currentColor" text-anchor="end" font-size="12">{y}</text>')
	g.append(f'<line x1="{sx(eps[0]):.1f}" y1="{sy(eps[1]):.1f}" x2="{sx(A[0]):.1f}" y2="{sy(A[1]):.1f}" stroke="currentColor" stroke-opacity="0.5" stroke-dasharray="6 4"/>')
	k = 0.32  # display length of the velocity arrow
	g.append(f'<line x1="{sx(pt[0]):.1f}" y1="{sy(pt[1]):.1f}" x2="{sx(pt[0] + k * vel[0]):.1f}" y2="{sy(pt[1] + k * vel[1]):.1f}" stroke="{ORANGE}" stroke-width="2.4" marker-end="url(#ah-fm)"/>')
	g.append(f'<circle cx="{sx(eps[0]):.1f}" cy="{sy(eps[1]):.1f}" r="6" fill="{GREY}"/>')
	g.append(f'<circle cx="{sx(A[0]):.1f}" cy="{sy(A[1]):.1f}" r="6" fill="{BLUE}"/>')
	g.append(f'<circle cx="{sx(pt[0]):.1f}" cy="{sy(pt[1]):.1f}" r="6" fill="{GREEN}"/>')
	g.append(f'<text x="{sx(eps[0]):.1f}" y="{sy(eps[1]) + 26:.1f}" fill="currentColor" text-anchor="start" dx="-20">noise ε (τ = 0)</text>')
	g.append(f'<text x="{sx(A[0]):.1f}" y="{sy(A[1]) - 16:.1f}" fill="{BLUE}" text-anchor="middle">action chunk A (τ = 1)</text>')
	g.append(f'<text x="{sx(pt[0]) - 10:.1f}" y="{sy(pt[1]) - 14:.1f}" fill="{GREEN}" text-anchor="end">A' + SUP("τ") + '</text>')
	g.append(f'<text x="{sx(pt[0]) + 10:.1f}" y="{sy(pt[1]) + 34:.1f}" fill="{ORANGE}">target velocity A − ε</text>')
	g.append(f'<text x="{(L + W - R) / 2}" y="{H - 12}" fill="currentColor" text-anchor="middle">action coordinate 1</text>')
	g.append(f'<text x="{L - 40}" y="{(T + H - B) / 2}" fill="currentColor" text-anchor="middle" transform="rotate(-90 {L - 40} {(T + H - B) / 2})">action coordinate 2</text>')
	return svg(W, H, "\n".join(g), "One training pair: noise, action chunk, interpolated point and target velocity") + (
		"<figcaption>One training pair in two action coordinates. The point $\\mathbf{A}^\\tau$ moves on the "
		"straight segment from the noise $\\boldsymbol{\\epsilon}$ to the data point $\\mathbf{A}$. Its velocity with "
		"respect to $\\tau$ is $\\mathbf{A} - \\boldsymbol{\\epsilon}$ at every $\\tau$; the arrow is shortened for "
		"display.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- pi0 post: 1-D flows for a two-point data set

def flow_velocity(x, t, modes):
	"""Exact marginal velocity E[A - eps | A^t = x] for the path A^t = t A + (1 - t) eps,
	eps ~ N(0, 1), A uniform on the points in `modes`."""
	s = 1 - t
	logw = [-(x - t * m) ** 2 / (2 * s * s) for m in modes]
	top = max(logw)
	w = [2.718281828459045 ** (lw - top) for lw in logw]
	mean_a = sum(wi * m for wi, m in zip(w, modes)) / sum(w)
	return (mean_a - x) / s


def flow_path(x0, modes, steps=400, t_end=0.998):
	pts, x = [(0.0, x0)], x0
	dt = t_end / steps
	for k in range(steps):
		x += dt * flow_velocity(x, k * dt, modes)
		pts.append(((k + 1) * dt, x))
	pts.append((1.0, x))
	return pts


FLOW_STARTS = [-1.9, -1.35, -1.0, -0.72, -0.45, -0.2, 0.05, 0.3, 0.55, 0.85, 1.2, 1.7]


def flow_panel(g, x0, y0, w, h, title, curves, arrows=None):
	sx = lambda t: x0 + t * w
	sy = lambda v: y0 + h / 2 - v / 3.2 * (h / 2)
	g.append(f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" fill="none" stroke="currentColor" stroke-opacity="0.35"/>')
	for v in (-2, 0, 2):
		g.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + w}" y2="{sy(v):.1f}" stroke="currentColor" stroke-opacity="0.12"/>')
		g.append(f'<text x="{x0 - 6}" y="{sy(v) + 4:.1f}" fill="currentColor" text-anchor="end" font-size="12">{v}</text>')
	g.append(f'<text x="{x0 + w / 2}" y="{y0 - 10}" fill="currentColor" text-anchor="middle">{title}</text>')
	for t in (0, 0.5, 1):
		g.append(f'<text x="{sx(t):.1f}" y="{y0 + h + 16}" fill="currentColor" text-anchor="middle" font-size="12">{t:g}</text>')
	g.append(f'<text x="{x0 + w / 2}" y="{y0 + h + 34}" fill="currentColor" text-anchor="middle" font-style="italic">τ</text>')
	if arrows:
		for t, v, dv in arrows:
			px, py = sx(t), sy(v)
			ddx, ddy = w * 0.05, -dv * 0.05 * (h / 2) / 3.2
			n = (ddx ** 2 + ddy ** 2) ** 0.5
			ddx, ddy = ddx / n * 11, ddy / n * 11
			g.append(f'<line x1="{px:.1f}" y1="{py:.1f}" x2="{px + ddx:.1f}" y2="{py + ddy:.1f}" stroke="{GREY}" stroke-width="1.2" marker-end="url(#ah-flow)"/>')
	for pts, colour in curves:
		d = " ".join(f"{sx(t):.1f},{sy(v):.1f}" for t, v in pts)
		g.append(f'<polyline points="{d}" fill="none" stroke="{colour}" stroke-width="1.6" stroke-opacity="0.85"/>')
		g.append(f'<circle cx="{sx(pts[0][0]):.1f}" cy="{sy(pts[0][1]):.1f}" r="3" fill="{GREY}"/>')
		g.append(f'<circle cx="{sx(pts[-1][0]):.1f}" cy="{sy(pts[-1][1]):.1f}" r="3" fill="{colour}"/>')


def fig_fm_pairs():
	W, H = 640, 330
	modes = (-2.0, 2.0)
	targets = [modes[c == "+"] for c in "+--+-++-+--+"]  # a fixed mixed pairing, one target per start
	pairs = [([(0, e), (1, a)], BLUE if a > 0 else ORANGE) for e, a in zip(FLOW_STARTS, targets)]
	flows = []
	for e in FLOW_STARTS:
		p = flow_path(e, modes)
		flows.append((p, BLUE if p[-1][1] > 0 else ORANGE))
	arrows = [(t, v, flow_velocity(v, t, modes)) for t in (0.1, 0.3, 0.5, 0.7, 0.9) for v in (-2.6, -1.3, 0, 1.3, 2.6)]
	g = ['<defs><marker id="ah-flow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>']
	flow_panel(g, 50, 40, 250, 230, "Training: random pairs", pairs)
	flow_panel(g, 370, 40, 250, 230, "Learned: averaged flow", flows, arrows)
	return svg(W, H, "\n".join(g), "Random training pairs and the averaged flow") + (
		"<figcaption>One-dimensional actions whose data take the values $-2$ and $+2$ with equal probability. "
		"Left: training pairs a random noise value with a random data value, so the straight segments cross. "
		"Right: the averaged velocity field (grey arrows) and the paths that follow it from the same starting points. "
		"The paths do not cross, and each ends at one of the two data values.</figcaption>\n</figure>\n"
	)


def fig_fm_conditions():
	W, H = 640, 300
	g = ['<defs><marker id="ah-flow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="5" markerHeight="5" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="context-stroke"/></marker></defs>']
	for k, (title, modes) in enumerate((("cup on the left", (-2.0,)), ("cup on the right", (2.0,)), ("cups on both sides", (-2.0, 2.0)))):
		curves = []
		for e in FLOW_STARTS:
			p = flow_path(e, modes)
			curves.append((p, BLUE if p[-1][1] > 0 else ORANGE))
		flow_panel(g, 50 + k * 200, 40, 160, 200, title, curves)
	return svg(W, H, "\n".join(g), "The same starting noise under three observations") + (
		"<figcaption>The same twelve noise values under three observations. Orange paths end at $-2$ (reach left) and "
		"blue paths end at $+2$ (reach right). When the observation allows one action, every starting point gives that "
		"action. When it allows two, the starting point selects one of them.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- game-models post, NitroGen: action labels from input overlays

def box(g, x, y, w, h, lines, colour, size=13, opacity=0.15):
	g.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{colour}" fill-opacity="{opacity}" stroke="{colour}"/>')
	top = y + h / 2 - (len(lines) - 1) * (size + 3) / 2 + size / 3
	for k, line in enumerate(lines):
		weight = ' font-weight="bold"' if k == 0 else ""
		g.append(f'<text x="{x + w / 2}" y="{top + k * (size + 3):.1f}" fill="currentColor" text-anchor="middle" font-size="{size}"{weight}>{line}</text>')


def arrow(g, x1, y1, x2, y2, mid, colour="currentColor", dash=False):
	d = ' stroke-dasharray="5 4"' if dash else ""
	g.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{colour}" stroke-opacity="0.7" stroke-width="1.4"{d} marker-end="url(#{mid})"/>')


def fig_ng_pipeline():
	W, H = 640, 300
	g = [ARROW_DEFS.format(id="ah-ng")]
	# a video frame with a gamepad overlay in its corner
	sx, sy, sw, sh = 20, 20, 190, 110
	g.append(f'<rect x="{sx}" y="{sy}" width="{sw}" height="{sh}" rx="4" fill="{GREY}" fill-opacity="0.15" stroke="currentColor" stroke-opacity="0.6"/>')
	g.append(f'<path d="M{sx + 10},{sy + 80} L{sx + 60},{sy + 50} L{sx + 100},{sy + 70} L{sx + 150},{sy + 35} L{sx + 180},{sy + 55}" fill="none" stroke="currentColor" stroke-opacity="0.35" stroke-width="2"/>')
	px, py = sx + 8, sy + sh - 34
	g.append(f'<rect x="{px}" y="{py}" width="56" height="28" rx="12" fill="none" stroke="{ORANGE}" stroke-width="1.8"/>')
	g.append(f'<circle cx="{px + 15}" cy="{py + 14}" r="5" fill="none" stroke="{ORANGE}" stroke-width="1.5"/>')
	for dx, dy, on in ((40, 9, True), (47, 14, False), (40, 19, False), (33, 14, False)):
		g.append(f'<circle cx="{px + dx}" cy="{py + dy}" r="2.6" fill="{ORANGE if on else "none"}" stroke="{ORANGE}"/>')
	g.append(f'<text x="{sx + sw + 16}" y="{sy + 40}" fill="currentColor">Public gameplay video. The creator shows</text>')
	g.append(f'<text x="{sx + sw + 16}" y="{sy + 60}" fill="currentColor">a live picture of the gamepad <tspan fill="{ORANGE}">(orange)</tspan>,</text>')
	g.append(f'<text x="{sx + sw + 16}" y="{sy + 80}" fill="currentColor">so the inputs are visible in the pixels.</text>')
	# stages
	y, h, w, gap, x0 = 175, 74, 140, 13, 20
	stages = [
		(["1. Locate", "template matching", "finds the gamepad"], BLUE),
		(["2. Parse", "read the buttons", "and the sticks"], BLUE),
		(["3. Filter", "remove idle play,", "mask the gamepad"], BLUE),
		(["Training pairs", "frame and", "action chunk"], GREEN),
	]
	for k, (lines, c) in enumerate(stages):
		x = x0 + k * (w + gap)
		box(g, x, y, w, h, lines, c, size=12)
		if k:
			arrow(g, x - gap + 1, y + h / 2, x - 2, y + h / 2, "ah-ng")
	arrow(g, sx + 40, sy + sh + 2, x0 + 40, y - 3, "ah-ng")
	# synthetic training data for the parser
	bx = x0 + (w + gap) + 10
	g.append(f'<text x="{bx + w / 2 - 10}" y="{y - 32}" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="12">trained on synthetic overlays</text>')
	g.append(f'<text x="{bx + w / 2 - 10}" y="{y - 16}" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="12">with known inputs</text>')
	arrow(g, bx + w / 2 - 10, y - 11, bx + w / 2 - 10, y - 3, "ah-ng", dash=True)
	g.append(f'<text x="{W / 2}" y="{H - 14}" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="12">71,000 hours of raw video → 40,000 hours of labeled data from more than 1,000 games</text>')
	return svg(W, H, "\n".join(g), "NitroGen data pipeline: action labels from input overlays") + (
		"<figcaption>The NitroGen data pipeline. Template matching finds the gamepad overlay, a segmentation model "
		"reads the pressed buttons and the stick positions from it, and filtering removes idle segments. The overlay is "
		"then masked, so the policy sees only the game.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- game-models post, NitroGen: model with an attention example

MONO = 'font-family="ui-monospace, SFMono-Regular, Menlo, monospace" font-size="10.5"'


def tok_box(g, cx, y, w, h, text, colour, opacity=0.22, size=12, bold=False):
	g.append(f'<rect x="{cx - w / 2}" y="{y}" width="{w}" height="{h}" rx="5" fill="{colour}" fill-opacity="{opacity}" stroke="{colour}"/>')
	weight = ' font-weight="600"' if bold else ""
	g.append(f'<text x="{cx}" y="{y + h / 2 + size / 3 + 0.5:.1f}" fill="currentColor" text-anchor="middle" font-size="{size}"{weight}>{text}</text>')


def up(g, x, y1, y2, mid="ah-ngm"):
	g.append(f'<line x1="{x}" y1="{y1}" x2="{x}" y2="{y2}" stroke="currentColor" stroke-opacity="0.7" stroke-width="1.2" marker-end="url(#{mid})"/>')


def weight_line(g, d, wgt):
	g.append(f'<path d="{d}" fill="none" stroke="{ORANGE}" stroke-width="{0.8 + 9 * wgt:.2f}" stroke-opacity="{0.35 + 1.3 * wgt:.2f}" stroke-linecap="round"/>')


def fig_ng_model():
	W, H = 640, 556
	g = [ARROW_DEFS.format(id="ah-ngm")]
	vx = [62, 130, 198, 266]      # one tower per frame patch (4 of N_v shown)
	ax = [372, 440, 508, 576]     # one tower per action token (4 of H shown)
	q = 0                         # the example query token a1
	ty, ts = 466, 40              # input row
	tok_y = 250                   # frame tokens
	cy, sy, bh = 352, 262, 28     # cross-attention row, self-attention row
	# ---- inputs: four patches of one game frame, four noisy action tokens
	for k, x in enumerate(vx):
		g.append(f'<rect x="{x - ts / 2}" y="{ty}" width="{ts}" height="{ts}" fill="{GREY}" fill-opacity="0.08" stroke="currentColor" stroke-opacity="0.5"/>')
		if k in (2, 3):
			g.append(f'<rect x="{x - ts / 2}" y="{ty + ts - 9}" width="{ts}" height="9" fill="{GREY}" fill-opacity="0.45"/>')
	g.append(f'<circle cx="{vx[2]}" cy="{ty + 19}" r="8" fill="{GREEN}" fill-opacity="0.9"/>')
	g.append(f'<circle cx="{vx[3]}" cy="{ty + 19}" r="8" fill="{ORANGE}" fill-opacity="0.9"/>')
	for k, name in enumerate(("sky", "sky", "player", "enemy")):
		g.append(f'<text x="{vx[k]}" y="{ty + ts + 16}" fill="currentColor" fill-opacity="0.75" text-anchor="middle" font-size="11">{name}</text>')
	g.append(f'<text x="{(vx[0] + vx[-1]) / 2}" y="{H - 8}" fill="currentColor" text-anchor="middle" font-size="12" font-weight="600">frame patches (4 of 256)</text>')
	for k, x in enumerate(ax):
		tok_box(g, x, ty + 6, 48, 28, "a" + SUB(str(k + 1)), PINK)
	g.append(f'<text x="{(ax[0] + ax[-1]) / 2}" y="{ty + ts + 16}" fill="currentColor" fill-opacity="0.75" text-anchor="middle" font-size="11">noisy actions A' + SUP("τ") + ', one token per step</text>')
	g.append(f'<text x="{(ax[0] + ax[-1]) / 2}" y="{H - 8}" fill="currentColor" text-anchor="middle" font-size="12" font-weight="600">action tokens (4 of 18)</text>')
	# ---- frame encoder: self-attention over all patches, then one frame token per patch
	ex0, ex1, ey, eh = vx[0] - 34, vx[-1] + 34, 360, 64
	g.append(f'<rect x="{ex0}" y="{ey}" width="{ex1 - ex0}" height="{eh}" rx="6" fill="{BLUE}" fill-opacity="0.14" stroke="{BLUE}"/>')
	g.append(f'<text x="{(ex0 + ex1) / 2}" y="{ey + 26}" fill="currentColor" text-anchor="middle" font-size="12" font-weight="600">Image encoder: SigLIP 2 and 4 layers</text>')
	g.append(f'<text x="{(ex0 + ex1) / 2}" y="{ey + 44}" fill="currentColor" fill-opacity="0.75" text-anchor="middle" font-size="11">self-attention over all patches</text>')
	for k, x in enumerate(vx):
		up(g, x, ty - 2, ey + eh + 2)
		up(g, x, ey, tok_y + 11)
		g.append(f'<circle cx="{x}" cy="{tok_y}" r="9" fill="{GREEN}" fill-opacity="0.3" stroke="{GREEN}" stroke-width="1.5"/>')
	g.append(f'<text x="{(vx[0] + vx[-1]) / 2}" y="{tok_y - 36}" fill="{GREEN}" text-anchor="middle" font-size="12" font-weight="600">frame tokens: keys and values</text>')
	# ---- action embedding with the flow time
	for x in ax:
		up(g, x, ty + 6, 454)
		tok_box(g, x, 430, 56, 22, "MLP", PINK, size=11)
	g.append(f'<text x="{ax[-1] + 32}" y="445" fill="currentColor" fill-opacity="0.75" font-size="11">+ τ</text>')
	# ---- DiT: 4 pairs of (cross-attention, self-attention) blocks, drawn once
	top = 196
	g.append(f'<rect x="{ax[0] - 40}" y="{top}" width="{ax[-1] - ax[0] + 80}" height="{cy + bh + 16 - top}" rx="9" fill="{GREY}" fill-opacity="0.08" stroke="{GREY}" stroke-opacity="0.6"/>')
	g.append(f'<text x="{ax[0] - 34}" y="{top + 17}" fill="currentColor" font-size="12" font-weight="600">4×</text>')
	for x in ax:
		up(g, x, 430, cy + bh + 2)
		up(g, x, cy, sy + bh + 2)
		up(g, x, sy, 162)
	# cross-attention of a1: one line to each frame token
	cw = (0.08, 0.12, 0.30, 0.50)
	for k, wgt in enumerate(cw):
		weight_line(g, f"M{ax[q] - 28} {cy + bh / 2} L{vx[k] + 7} {tok_y + 5}", wgt)
		g.append(f'<text x="{vx[k]}" y="{tok_y - 15}" fill="currentColor" fill-opacity="0.85" text-anchor="middle" font-size="10.5">{wgt:.2f}</text>')
	for k, x in enumerate(ax):
		tok_box(g, x, cy, 56, bh, "cross", ORANGE, opacity=0.45 if k == q else 0.2, size=11)
	# self-attention of a1: one arc to each action token
	sw = (0.34, 0.30, 0.22, 0.14)
	for k, wgt in enumerate(sw):
		if k == q:
			weight_line(g, f"M{ax[q] - 12} {sy} C {ax[q] - 24} {sy - 34}, {ax[q] + 24} {sy - 34}, {ax[q] + 12} {sy}", wgt)
			g.append(f'<text x="{ax[q] - 30}" y="{sy - 8}" fill="currentColor" fill-opacity="0.85" text-anchor="end" font-size="10.5">{wgt:.2f}</text>')
			continue
		h = 30 + 14 * k
		weight_line(g, f"M{ax[q] + 14} {sy} C {ax[q] + 14} {sy - h}, {ax[k]} {sy - h}, {ax[k]} {sy}", wgt)
		g.append(f'<text x="{ax[k] + 6}" y="{sy - 5}" fill="currentColor" fill-opacity="0.85" font-size="10.5">{wgt:.2f}</text>')
	for k, x in enumerate(ax):
		tok_box(g, x, sy, 56, bh, "self", ORANGE, opacity=0.45 if k == q else 0.2, size=11)
	# ---- output: one velocity per action token, then the Euler loop
	for k, x in enumerate(ax):
		tok_box(g, x, 134, 56, 26, "v" + SUB(str(k + 1)), LAVENDER, size=12)
	g.append(f'<text x="{(ax[0] + ax[-1]) / 2}" y="118" fill="currentColor" text-anchor="middle" font-size="12" font-weight="600">velocity v' + SUB("θ") + ' for every step of the chunk</text>')
	g.append(f'<path d="M{ax[-1] + 28} 147 H{W - 8} V{ty + 20} H{ax[-1] + 26}" fill="none" stroke="{BLUE}" stroke-width="1.5" stroke-dasharray="6 4" marker-end="url(#ah-ngm)"/>')
	g.append(f'<text x="{W - 14}" y="100" fill="{BLUE}" text-anchor="end" font-size="11">16 Euler steps: A' + SUP("τ") + ' ← A' + SUP("τ") + ' + v' + SUB("θ") + ' / 16</text>')
	# ---- legend for the example
	g.append(f'<text x="20" y="40" fill="currentColor" font-size="12" font-weight="600">Example: token a' + SUB("1") + ' as the query</text>')
	g.append(f'<line x1="20" y1="58" x2="44" y2="58" stroke="{ORANGE}" stroke-width="4" stroke-opacity="0.8" stroke-linecap="round"/>')
	g.append(f'<text x="52" y="62" fill="currentColor" font-size="11">line width = attention weight</text>')
	g.append(f'<text x="20" y="82" fill="currentColor" fill-opacity="0.8" font-size="11">cross: a' + SUB("1") + ' reads the frame tokens</text>')
	g.append(f'<text x="20" y="100" fill="currentColor" fill-opacity="0.8" font-size="11">self: a' + SUB("1") + ' reads the action tokens</text>')
	return svg(W, H, "\n".join(g), "NitroGen model with one tower per token and an attention example") + (
		"<figcaption>The NitroGen model, read from bottom to top, with one tower per token. The frame encoder turns "
		"each 16 × 16 pixel square of the frame into a frame token. Each action token then passes 4 pairs of DiT blocks. In a cross-attention block "
		"it reads the frame tokens, and in a self-attention block it reads the other action tokens. Orange lines show "
		"these reads for $a_1$; every token does the same, and the weights are illustrative. Each block also has a "
		"feed-forward layer and an AdaLN layer that adds the flow time $\\tau$.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- game-models post, NitroGen: transfer to a held-out game

def bar_panel(g, x0, y0, w, h, title, groups, colours=(BLUE, GREY)):
	sy = lambda v: y0 + h - v / 100 * h
	g.append(f'<line x1="{x0}" y1="{y0 + h}" x2="{x0 + w}" y2="{y0 + h}" stroke="currentColor"/>')
	for v in (0, 50, 100):
		g.append(f'<text x="{x0 - 6}" y="{sy(v) + 4:.1f}" fill="currentColor" text-anchor="end" font-size="12">{v}</text>')
		if v:
			g.append(f'<line x1="{x0}" y1="{sy(v):.1f}" x2="{x0 + w}" y2="{sy(v):.1f}" stroke="currentColor" stroke-opacity="0.12"/>')
	if title:
		g.append(f'<text x="{x0 + w / 2}" y="{y0 - 12}" fill="currentColor" text-anchor="middle">{title}</text>')
	gw = w / len(groups)
	n = len(colours)
	bw = gw * 0.6 / n
	for k, (label, *values) in enumerate(groups):
		cx = x0 + gw * (k + 0.5)
		for j, (v, c) in enumerate(zip(values, colours)):
			bx = cx - n * (bw + 4) / 2 + 2 + j * (bw + 4)
			g.append(f'<rect x="{bx:.1f}" y="{sy(v):.1f}" width="{bw:.1f}" height="{h - (sy(v) - y0):.1f}" fill="{c}" fill-opacity="0.8"/>')
			g.append(f'<text x="{bx + bw / 2:.1f}" y="{sy(v) - 5:.1f}" fill="currentColor" text-anchor="middle" font-size="11">{v:g}</text>')
		g.append(f'<text x="{cx:.1f}" y="{y0 + h + 18}" fill="currentColor" text-anchor="middle" font-size="12">{label}</text>')


def fig_ng_transfer():
	W, H = 640, 320
	g = []
	bar_panel(g, 50, 60, 250, 200, "Roguelike: data for the new game", [("60 h", 53.0, 48.1), ("120 h", 65.6, 57.8), ("240 h", 81.0, 76.0)])
	bar_panel(g, 370, 60, 250, 200, "3D action-RPG: 30 h, by task type", [("combat", 73.3, 48.3), ("navigation", 60.0, 48.0), ("game-specific", 66.6, 63.3)])
	g.append(f'<text x="20" y="{60 + 100}" fill="currentColor" text-anchor="middle" font-size="12" transform="rotate(-90 20 160)">task completion (%)</text>')
	for k, (label, c) in enumerate((("fine-tuned from NitroGen", BLUE), ("trained from scratch", GREY))):
		x = 170 + k * 210
		g.append(f'<rect x="{x}" y="{H - 22}" width="12" height="12" fill="{c}" fill-opacity="0.8"/>')
		g.append(f'<text x="{x + 18}" y="{H - 12}" fill="currentColor" font-size="13">{label}</text>')
	return svg(W, H, "\n".join(g), "Fine-tuning from NitroGen versus training from scratch on a held-out game") + (
		"<figcaption>Transfer to a game held out of pre-training, from Fig. 7 of the paper. Both models have the same "
		"architecture, data and compute. Left: an isometric roguelike with 60 to 240 hours of its own data. Right: a 3D "
		"action-RPG with 30 hours, split by task type.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- game-models post, JARVIS-VLA: model and action tokens

def camera_degrees(b, mu=20, maxval=10):
	x = (b - 10) / 10
	return math.copysign(((1 + mu) ** abs(x) - 1) / mu * maxval, x) if x else 0.0


def fig_jv_model():
	W, H = 640, 560
	g = [ARROW_DEFS.format(id="ah-jv")]
	# ---- output: one action as five tokens
	toks = [("[act]", GREY), ("use", GREEN), ("cam 14", BLUE), ("cam 12", BLUE), ("[/act]", GREY)]
	tw, tg = 62, 10
	t0 = W / 2 - (len(toks) * tw + (len(toks) - 1) * tg) / 2 + tw / 2
	tx = [t0 + k * (tw + tg) for k in range(len(toks))]
	g.append(f'<text x="{W / 2}" y="24" fill="currentColor" text-anchor="middle" font-size="12" font-weight="600">output: one action as 5 tokens, generated one at a time</text>')
	for x, (t, c) in zip(tx, toks):
		tok_box(g, x, 36, tw, 26, t, c, size=12)
		up(g, x, 112, 64, mid="ah-jv")
	# ---- language model
	lx0, lx1, ly, lh = 90, 550, 112, 58
	g.append(f'<rect x="{lx0}" y="{ly}" width="{lx1 - lx0}" height="{lh}" rx="6" fill="{ORANGE}" fill-opacity="0.14" stroke="{ORANGE}"/>')
	g.append(f'<text x="{W / 2}" y="{ly + 24}" fill="currentColor" text-anchor="middle" font-size="12" font-weight="600">Language model: Qwen2 7B, 28 layers</text>')
	g.append(f'<text x="{W / 2}" y="{ly + 42}" fill="currentColor" fill-opacity="0.75" text-anchor="middle" font-size="11">next-token prediction over text tokens and action tokens</text>')
	# ---- input tokens: image tokens from the frames, text tokens from the instruction
	iy = 212
	ix = [130, 166, 202, 238, 274]
	for x in ix:
		g.append(f'<circle cx="{x}" cy="{iy}" r="9" fill="{GREEN}" fill-opacity="0.3" stroke="{GREEN}" stroke-width="1.5"/>')
		up(g, x, iy - 11, ly + lh + 2, mid="ah-jv")
	g.append(f'<text x="{ix[-1] + 18}" y="{iy + 4}" fill="currentColor" fill-opacity="0.75" font-size="11">…</text>')
	g.append(f'<text x="{ix[0] - 16}" y="{iy + 4}" fill="{GREEN}" text-anchor="end" font-size="11" font-weight="600">image</text>')
	g.append(f'<text x="{ix[0] - 16}" y="{iy + 18}" fill="{GREEN}" text-anchor="end" font-size="11" font-weight="600">tokens</text>')
	words = ["Craft", "a", "ladder", "."]
	wx = [392, 446, 500, 546]
	for x, w in zip(wx, words):
		tok_box(g, x, iy - 13, 48 if len(w) > 2 else 30, 26, w, PINK, size=12)
		up(g, x, iy - 15, ly + lh + 2, mid="ah-jv")
	g.append(f'<text x="{(wx[0] + wx[-1]) / 2}" y="{iy + 34}" fill="{PINK}" text-anchor="middle" font-size="11" font-weight="600">instruction tokens</text>')
	# ---- vision path: adapter, ViT, frames
	vx0, vx1 = 100, 304
	vc = (vx0 + vx1) / 2
	g.append(f'<rect x="{vx0}" y="250" width="{vx1 - vx0}" height="34" rx="5" fill="{LAVENDER}" fill-opacity="0.18" stroke="{LAVENDER}"/>')
	g.append(f'<text x="{vc}" y="271" fill="currentColor" text-anchor="middle" font-size="12">adapter: MLP</text>')
	up(g, vc, 250, iy + 12, mid="ah-jv")
	g.append(f'<rect x="{vx0}" y="304" width="{vx1 - vx0}" height="50" rx="5" fill="{BLUE}" fill-opacity="0.14" stroke="{BLUE}"/>')
	g.append(f'<text x="{vc}" y="325" fill="currentColor" text-anchor="middle" font-size="12" font-weight="600">ViT: 32 layers</text>')
	g.append(f'<text x="{vc}" y="342" fill="currentColor" fill-opacity="0.75" text-anchor="middle" font-size="11">14 × 14 pixel squares</text>')
	up(g, vc, 304, 286, mid="ah-jv")
	for k, (fx, name) in enumerate(((112, "earlier frame"), (212, "current frame"))):
		g.append(f'<rect x="{fx}" y="376" width="80" height="45" rx="3" fill="{GREY}" fill-opacity="0.12" stroke="currentColor" stroke-opacity="0.55"/>')
		g.append(f'<path d="M{fx + 6},{376 + 34} L{fx + 30},{376 + 20} L{fx + 50},{376 + 28} L{fx + 74},{376 + 14}" fill="none" stroke="currentColor" stroke-opacity="0.35" stroke-width="1.5"/>')
		g.append(f'<text x="{fx + 40}" y="438" fill="currentColor" fill-opacity="0.75" text-anchor="middle" font-size="11">{name}</text>')
		up(g, fx + 40, 376, 356, mid="ah-jv")
	g.append(f'<text x="{(wx[0] + wx[-1]) / 2}" y="330" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="12">frames: 644 × 364 pixels</text>')
	g.append(f'<text x="{(wx[0] + wx[-1]) / 2}" y="348" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="12">no change to the architecture</text>')
	# ---- camera bins on a degree axis
	ax0, ax1, ay = 80, 560, 506
	sc = (ax1 - ax0) / 20
	px = lambda d: W / 2 + d * sc
	g.append(f'<text x="{ax0}" y="470" fill="currentColor" font-size="12" font-weight="600">camera token: 21 bins per axis, turn in degrees</text>')
	g.append(f'<line x1="{ax0}" y1="{ay}" x2="{ax1}" y2="{ay}" stroke="currentColor" stroke-opacity="0.6"/>')
	for b in range(21):
		x = px(camera_degrees(b))
		hl = b in (12, 14)
		g.append(f'<line x1="{x:.1f}" y1="{ay - 8}" x2="{x:.1f}" y2="{ay + 8}" stroke="{BLUE if hl else "currentColor"}" stroke-width="{2 if hl else 1}" stroke-opacity="{1 if hl else 0.6}"/>')
	for b in (0, 5, 10, 15, 20):
		x = px(camera_degrees(b))
		d = camera_degrees(b)
		g.append(f'<text x="{x:.1f}" y="{ay - 14}" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="11">{b}</text>')
		deg = "0" if not d else f"{d:+.1f}".replace(".0", "").replace("-", "−")
		g.append(f'<text x="{x:.1f}" y="{ay + 24}" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="11">{deg}°</text>')
	g.append(f'<text x="{ax0 - 28}" y="{ay - 14}" fill="currentColor" fill-opacity="0.8" text-anchor="end" font-size="11">bin</text>')
	g.append(f'<text x="{ax0 - 28}" y="{ay + 24}" fill="currentColor" fill-opacity="0.8" text-anchor="end" font-size="11">turn</text>')
	return svg(W, H, "\n".join(g), "JARVIS-VLA: a vision-language model that writes actions as tokens") + (
		"<figcaption>The JARVIS-VLA model, read from bottom to top. The ViT and the adapter turn each frame into image tokens. "
		"The language model reads them with the instruction and writes an action as tokens. Bottom: the 21 bins of one camera "
		"token on a scale of degrees. The bins are dense near zero, and the bins of the example, 12 and 14, are blue. "
		"The token format and the bin values come from the released code.</figcaption>\n</figure>\n"
	)


def fig_jv_stages():
	W, H = 640, 330
	g = []
	stages = [
		("Stage I: language", ("LM",), "text", ["text questions and", "answers about", "Minecraft"]),
		("Stage II: vision-language", ("LM", "adapter", "ViT"), "text", ["captions, visual", "questions, grounding", "on Minecraft frames"]),
		("Stage III: actions", ("LM",), "action tokens", ["play with actions:", "humans, agents and", "synthetic crafting"]),
	]
	cw, gap, x0 = 190, 15, 20
	colours = {"LM": ORANGE, "adapter": LAVENDER, "ViT": BLUE}
	for k, (title, trained, out, data) in enumerate(stages):
		x = x0 + k * (cw + gap)
		cx = x + cw / 2
		g.append(f'<text x="{cx}" y="24" fill="currentColor" text-anchor="middle" font-size="13" font-weight="600">{title}</text>')
		g.append(f'<text x="{cx}" y="50" fill="currentColor" fill-opacity="0.75" text-anchor="middle" font-size="11">output: {out}</text>')
		for j, (name, y, h) in enumerate((("LM", 62, 46), ("adapter", 120, 30), ("ViT", 162, 40))):
			on = name in trained
			c = colours[name] if on else GREY
			dash = "" if on else ' stroke-dasharray="4 3"'
			g.append(f'<rect x="{x + 20}" y="{y}" width="{cw - 40}" height="{h}" rx="5" fill="{c}" fill-opacity="{0.25 if on else 0.06}" stroke="{c}"{dash}/>')
			label = {"LM": "language model", "adapter": "adapter", "ViT": "ViT"}[name]
			state = "trained" if on else "frozen"
			g.append(f'<text x="{cx}" y="{y + h / 2 + 4}" fill="currentColor" fill-opacity="{1 if on else 0.6}" text-anchor="middle" font-size="12">{label}: {state}</text>')
		box(g, x + 10, 226, cw - 20, 66, data, GREEN, size=12, opacity=0.1)
		if k:
			arrow(g, x - gap + 1, 132, x - 2, 132, "ah-jvs")
	g.insert(0, ARROW_DEFS.format(id="ah-jvs"))
	g.append(f'<text x="{W / 2}" y="{H - 12}" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="12">then fine-tuning on more than 100 trajectories for each test task</text>')
	return svg(W, H, "\n".join(g), "JARVIS-VLA training stages and the parts each stage trains") + (
		"<figcaption>The three post-training stages of JARVIS-VLA (ActVLP). Colored parts are trained and dashed gray parts "
		"are frozen. Stages I and II use Minecraft text and images without actions, and stage III uses trajectories. All "
		"stages use next-token prediction.</figcaption>\n</figure>\n"
	)


def fig_jv_results():
	W, H = 640, 330
	g = []
	colours = (GREY, YELLOW, LAVENDER, BLUE)
	bar_panel(g, 60, 40, 560, 200, "", [
		("Mine blocks", 67, 79, 75, 88), ("Kill entities", 52, 84, 86, 95),
		("Craft items", 57, 60, 65, 77), ("Smelt items", 33, 7, 29, 70),
	], colours=colours)
	g.append(f'<text x="20" y="140" fill="currentColor" text-anchor="middle" font-size="12" transform="rotate(-90 20 140)">success rate (%)</text>')
	labels = ("best earlier agent", "Qwen2-VL: test-task data only", "Qwen2-VL: stage III, no I or II", "JARVIS-VLA: all stages")
	for k, (label, c) in enumerate(zip(labels, colours)):
		x, y = 70 + (k % 2) * 290, H - 42 + (k // 2) * 22
		g.append(f'<rect x="{x}" y="{y - 11}" width="12" height="12" fill="{c}" fill-opacity="0.8"/>')
		g.append(f'<text x="{x + 18}" y="{y}" fill="currentColor" font-size="13">{label}</text>')
	return svg(W, H, "\n".join(g), "JARVIS-VLA success rates in four groups of Minecraft tasks") + (
		"<figcaption>Average success rate in each task group, from Table 1 of the paper. The best earlier agent is the highest "
		"of VPT, STEVE-1, GROOT and MineDreamer in each group. All Qwen2-VL models are fine-tuned on the same test-task "
		"trajectories.</figcaption>\n</figure>\n"
	)


# ---------------------------------------------------------------- game-models post, CombatVLA: truncated action-of-thought

def fig_cv_aot():
	W, H = 640, 360
	g = [ARROW_DEFS.format(id="ah-cv")]
	# ---- input frames and the model
	for k in range(3):
		x, y = 30 + k * 12, 34 + k * 10
		g.append(f'<rect x="{x}" y="{y}" width="80" height="48" rx="3" fill="{GREY}" fill-opacity="0.18" stroke="currentColor" stroke-opacity="0.55"/>')
	g.append(f'<text x="84" y="120" fill="currentColor" fill-opacity="0.75" text-anchor="middle" font-size="11">3 frames, 1008 × 560</text>')
	arrow(g, 138, 68, 196, 68, "ah-cv")
	box(g, 200, 40, 200, 56, ["Qwen2.5-VL 3B", "one call per step"], ORANGE, size=12)
	# ---- the answer as one token sequence
	ty, th = 168, 34
	parts = [("action: press space", GREEN, 150), ("&lt;TRUNC&gt;", GREY, 84), ("explanation: the enemy is about to attack", PINK, 250), ("&lt;EOS&gt;", GREY, 60)]
	x = 30
	xs = []
	for text, c, w in parts:
		tok_box(g, x + w / 2, ty, w, th, text, c, size=11.5)
		xs.append((x, x + w))
		x += w + 8
	g.append(f'<path d="M300 96 V128 H{xs[0][0] + 75} V{ty - 2}" fill="none" stroke="currentColor" stroke-opacity="0.7" stroke-width="1.4" marker-end="url(#ah-cv)"/>')
	g.append(f'<text x="310" y="122" fill="currentColor" fill-opacity="0.75" font-size="11">answer, one token at a time</text>')
	cut = xs[1][1] + 4
	# ---- training covers the whole answer
	x0, x1 = xs[0][0], xs[-1][1]
	by = ty + th + 18
	g.append(f'<path d="M{x0} {by - 6} V{by} H{x1} V{by - 6}" fill="none" stroke="{BLUE}" stroke-width="1.5"/>')
	g.append(f'<text x="{(cut + x1) / 2}" y="{by + 18}" fill="{BLUE}" text-anchor="middle" font-size="12">training: next-token loss on the whole answer</text>')
	# ---- inference stops at <TRUNC>
	g.append(f'<line x1="{cut}" y1="{ty - 22}" x2="{cut}" y2="{H - 50}" stroke="{ORANGE}" stroke-width="1.6" stroke-dasharray="5 4"/>')
	g.append(f'<text x="{cut + 6}" y="{ty - 10}" fill="{ORANGE}" font-size="11">inference stops here</text>')
	iy = by + 52
	g.append(f'<path d="M{x0} {iy - 6} V{iy} H{xs[1][1]} V{iy - 6}" fill="none" stroke="{ORANGE}" stroke-width="1.5"/>')
	g.append(f'<text x="{(x0 + xs[1][1]) / 2}" y="{iy + 18}" fill="{ORANGE}" text-anchor="middle" font-size="12">inference: generated</text>')
	g.append(f'<text x="{(xs[2][0] + x1) / 2}" y="{iy + 4}" fill="currentColor" fill-opacity="0.6" text-anchor="middle" font-size="12">never generated at play time</text>')
	g.append(f'<text x="{(x0 + xs[1][1]) / 2}" y="{H - 14}" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="12">executor presses the keys</text>')
	arrow(g, (x0 + xs[1][1]) / 2, iy + 24, (x0 + xs[1][1]) / 2, H - 30, "ah-cv")
	return svg(W, H, "\n".join(g), "CombatVLA answer format: action, truncation token, explanation") + (
		"<figcaption>One CombatVLA step. The answer is an action, the token &lt;TRUNC&gt;, and a fixed explanation for "
		"that action type. Training uses the whole answer. At play time, generation stops at &lt;TRUNC&gt;, and an executor "
		"sends the action to the game as keyboard and mouse input.</figcaption>\n</figure>\n"
	)


def fig_cv_latency():
	W, H = 640, 250
	g = []
	ax0, ax1, top = 290, 600, 30
	px = lambda v: ax0 + (ax1 - ax0) * math.log10(v) / 2
	rows = [
		("VARP: 10 GPT-4o calls", 90.23, GREY),
		("Cradle: 5 GPT-4o calls", 61.68, GREY),
		("CombatVLA, full answer", 3.73, LAVENDER),
		("CombatVLA, stop at &lt;TRUNC&gt;", 1.85, BLUE),
	]
	bottom = top + 20 + len(rows) * 40
	for v in (1, 2, 5, 10, 20, 50, 100):
		x = px(v)
		major = v in (1, 10, 100)
		g.append(f'<line x1="{x:.1f}" y1="{top}" x2="{x:.1f}" y2="{bottom}" stroke="currentColor" stroke-opacity="{0.22 if major else 0.09}"/>')
		g.append(f'<text x="{x:.1f}" y="{bottom + 18}" fill="currentColor" fill-opacity="0.8" text-anchor="middle" font-size="11">{v}</text>')
	g.append(f'<text x="{(ax0 + ax1) / 2}" y="{bottom + 38}" fill="currentColor" text-anchor="middle" font-size="12">time per step (s), log scale</text>')
	for k, (label, v, c) in enumerate(rows):
		y = top + 30 + k * 40
		g.append(f'<text x="{ax0 - 16}" y="{y + 4}" fill="currentColor" text-anchor="end" font-size="13">{label}</text>')
		g.append(f'<line x1="{ax0}" y1="{y}" x2="{px(v):.1f}" y2="{y}" stroke="{c}" stroke-width="2" stroke-opacity="0.6"/>')
		g.append(f'<circle cx="{px(v):.1f}" cy="{y}" r="7" fill="{c}" fill-opacity="0.9"/>')
		right = px(v) > ax1 - 60
		tx = px(v) - 12 if right else px(v) + 12
		g.append(f'<text x="{tx:.1f}" y="{y - 10 if right else y + 4}" fill="currentColor" text-anchor="{"end" if right else "start"}" font-size="12" font-weight="600">{v:.2f} s</text>')
	return svg(W, H, "\n".join(g), "CombatVLA time per step against GPT-4o agent frameworks") + (
		"<figcaption>Time from the input frames to the actions for one step, on a log scale. The two framework values are "
		"from Table 3 of the paper, and the two CombatVLA values are from Table 4. Stopping at &lt;TRUNC&gt; halves the "
		"time of one call.</figcaption>\n</figure>\n"
	)


def main():
	OUT.mkdir(parents=True, exist_ok=True)
	for name, fn in (
		("ls-fit", fig_ls_fit), ("ls-geometry", fig_geometry), ("r2-inflation", fig_r2), ("partial-f", fig_partial_f),
		("binomial-test", fig_binomial_test),
		("pi0-architecture", fig_pi0_architecture), ("fm-path", fig_fm_path),
		("fm-pairs", fig_fm_pairs), ("fm-conditions", fig_fm_conditions),
		("ng-pipeline", fig_ng_pipeline), ("ng-model", fig_ng_model),
		("ng-transfer", fig_ng_transfer),
		("jv-model", fig_jv_model), ("jv-stages", fig_jv_stages), ("jv-results", fig_jv_results),
		("cv-aot", fig_cv_aot), ("cv-latency", fig_cv_latency),
	):
		(OUT / f"{name}.html").write_text(fn())
		print("wrote", name)


if __name__ == "__main__":
	main()
