#!/usr/bin/env python3
"""Generate the inline SVG figures for the linear regression post (stdlib only).

Usage:  python3 tools/figures.py     # writes content/figures/*.html (figure fragments)
Colours use currentColor for ink so the figures follow the light/dark theme.
"""

import random
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "content" / "figures"
BLUE = "#3b7ddd"
ORANGE = "#e8833a"
GREEN = "#3aa17e"
GREY = "#999"


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


def main():
	OUT.mkdir(parents=True, exist_ok=True)
	for name, fn in (
		("ls-fit", fig_ls_fit), ("ls-geometry", fig_geometry), ("r2-inflation", fig_r2), ("partial-f", fig_partial_f),
		("binomial-test", fig_binomial_test),
	):
		(OUT / f"{name}.html").write_text(fn())
		print("wrote", name)


if __name__ == "__main__":
	main()
