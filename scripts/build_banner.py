"""Builds assets/banner.svg: the animated banner of the GitHub profile.

Run: python3 scripts/build_banner.py
Edit the constants below to change the texts or colours.
"""
import pathlib
import random

NAME = "Cécile"
HANDLE = "0xKaniOps"
TAGLINE = "Cybersecurity × Machine Learning"
PROMPT = "SOC work-study · learning ML · leveling up"

BG1, BG2 = "#070B17", "#121A36"
TEAL, VIOLET, AMBER = "#2DD4BF", "#8B5CF6", "#F59E0B"
W, H = 1200, 320

random.seed(7)
layers_x = [96, 206, 316, 426]
layers_n = [4, 6, 6, 3]


def ys(n):
    gap = 210 / (n - 1)
    return [55 + i * gap for i in range(n)]


nodes = [[(x, y) for y in ys(n)] for x, n in zip(layers_x, layers_n)]

edges, pulses = [], []
k = 0
for a, b in zip(nodes, nodes[1:]):
    for (x1, y1) in a:
        for (x2, y2) in b:
            edges.append(f'<line x1="{x1}" y1="{y1:.1f}" x2="{x2}" y2="{y2:.1f}"/>')
            if random.random() < 0.28:
                dur = random.uniform(2.2, 4.2)
                delay = random.uniform(0, 4)
                color = TEAL if random.random() < 0.6 else VIOLET
                pulses.append(
                    f'<line class="p" x1="{x1}" y1="{y1:.1f}" x2="{x2}" y2="{y2:.1f}" '
                    f'stroke="{color}" pathLength="100" '
                    f'style="animation-duration:{dur:.1f}s;animation-delay:-{delay:.1f}s"/>'
                )
            k += 1

circles = []
for li, layer in enumerate(nodes):
    for i, (x, y) in enumerate(layer):
        out = li == len(nodes) - 1
        c = AMBER if out else (TEAL if li % 2 == 0 else VIOLET)
        d = (li * 0.5 + i * 0.3) % 3
        circles.append(
            f'<circle class="glow" cx="{x}" cy="{y:.1f}" r="11" fill="{c}" style="animation-delay:-{d:.1f}s"/>'
            f'<circle cx="{x}" cy="{y:.1f}" r="6" fill="{BG1}" stroke="{c}" stroke-width="2.2"/>'
        )

mono = "'JetBrains Mono','SFMono-Regular',Consolas,'Liberation Mono',Menlo,monospace"
sans = "'Segoe UI','Helvetica Neue',Helvetica,Arial,sans-serif"

svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME} — {TAGLINE}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{BG1}"/><stop offset="1" stop-color="{BG2}"/>
    </linearGradient>
    <linearGradient id="tag" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="{TEAL}"/><stop offset="1" stop-color="{VIOLET}"/>
    </linearGradient>
    <radialGradient id="halo" cx="0.22" cy="0.5" r="0.45">
      <stop offset="0" stop-color="{VIOLET}" stop-opacity="0.22"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/>
    </radialGradient>
    <pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse">
      <path d="M32 0H0V32" fill="none" stroke="#FFFFFF" stroke-opacity="0.04"/>
    </pattern>
    <filter id="blur" x="-1" y="-1" width="3" height="3"><feGaussianBlur stdDeviation="5"/></filter>
    <style>
      .p {{ stroke-width: 2.4; stroke-linecap: round; stroke-dasharray: 6 94; animation: flow linear infinite; }}
      @keyframes flow {{ from {{ stroke-dashoffset: 100; }} to {{ stroke-dashoffset: 0; }} }}
      .glow {{ filter: url(#blur); opacity: .25; animation: breathe 3s ease-in-out infinite; }}
      @keyframes breathe {{ 50% {{ opacity: .7; }} }}
      .cursor {{ animation: blink 1.1s steps(1) infinite; }}
      @keyframes blink {{ 50% {{ opacity: 0; }} }}
      .rise {{ opacity: 0; animation: rise .9s ease-out forwards; }}
      @keyframes rise {{ from {{ opacity: 0; transform: translateY(10px); }} to {{ opacity: 1; transform: none; }} }}
      .scan {{ animation: scan 6s ease-in-out infinite; }}
      @keyframes scan {{ 0%,100% {{ transform: translateX(0); opacity: 0; }} 10% {{ opacity: .5; }} 90% {{ opacity: .5; }} 99% {{ transform: translateX({W - 40}px); opacity: 0; }} }}
    </style>
  </defs>
  <rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/>
  <rect width="{W}" height="{H}" rx="18" fill="url(#grid)"/>
  <rect width="{W}" height="{H}" rx="18" fill="url(#halo)"/>
  <rect class="scan" x="20" y="0" width="2" height="{H}" fill="{TEAL}"/>

  <g stroke="#FFFFFF" stroke-opacity="0.09" stroke-width="1">{''.join(edges)}</g>
  <g fill="none">{''.join(pulses)}</g>
  <g>{''.join(circles)}</g>

  <g font-family="{sans}">
    <text class="rise" x="560" y="98" font-family="{mono}" font-size="18" fill="{TEAL}" style="animation-delay:.1s">~/{HANDLE} $ whoami</text>
    <text class="rise" x="556" y="172" font-size="72" font-weight="800" fill="#F8FAFC" letter-spacing="-1.5" style="animation-delay:.35s">{NAME}</text>
    <text class="rise" x="560" y="216" font-size="28" font-weight="600" fill="url(#tag)" style="animation-delay:.6s">{TAGLINE}</text>
    <text class="rise" x="560" y="262" font-family="{mono}" font-size="17" fill="#94A3B8" style="animation-delay:.85s">&gt; {PROMPT}<tspan class="cursor" fill="{AMBER}"> ▌</tspan></text>
  </g>
  <rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="17" fill="none" stroke="url(#tag)" stroke-opacity="0.35"/>
</svg>
"""

out = pathlib.Path(__file__).resolve().parent.parent / "assets" / "banner.svg"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(svg, encoding="utf-8")
print("written", out)
