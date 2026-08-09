#!/usr/bin/env python3
"""Build a one-page executive summary for the ranked US synthesis stack."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RANKINGS_JSON = ROOT / "american_rankings.json"
OUT = ROOT / "american-executive-summary.html"


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1160px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.5rem,5vw,4.2rem);line-height:.98;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3{margin:.2em 0 .35em;font-size:1.1rem}.card p{margin:.35em 0 0;color:var(--muted)}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def main() -> None:
    rankings = json.loads(RANKINGS_JSON.read_text())
    top_themes = rankings["top_themes"][:4]
    top_subthemes = rankings["top_subthemes"][:6]
    top_bottlenecks = rankings["top_bottlenecks"][:6]
    top_exposed = rankings["top_exposed_models"][:6]

    theme_cards = "".join(
        f"""<article class="card">
  <div class="meta">{e(theme['lens'])}</div>
  <h3>{e(theme['title'])}</h3>
  <p>{e(theme['thesis'])}</p>
  <div class="chips">{''.join(f'<span class="chip">{e(signal)}</span>' for signal in theme['signals'])}</div>
</article>"""
        for theme in top_themes
    )

    subtheme_items = "".join(
        f"<li><b>{e(item['title'])}</b>: {e(item['summary'])}</li>"
        for item in top_subthemes
    )
    bottleneck_items = "".join(
        f"<li><b>{e(item['title'])}</b>: {e(item['rationale'])}</li>"
        for item in top_bottlenecks
    )
    exposed_items = "".join(
        f"<li><b>{e(item['title'])}</b> <span class=\"chip\">{e(item['theme_title'])}</span></li>"
        for item in top_exposed
    )

    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>American Executive Summary — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="american-synthesis-hub.html">Synthesis hub</a><a href="index.html">Industry briefs</a><a href="american-rankings.html">Rankings</a><a href="american-outlook-2025-2026.html">American outlook</a><a href="american-economy-2025-2026.html">Capstone</a><a href="american-synthesis-playbook.html">Playbook</a><a href="american-implications-memo.html">Implications memo</a></div>
<div class="eyebrow">Executive summary · US · 2025-2026</div>
<h1>American Executive Summary</h1>
<p class="sub">A short plain-English read on the themes that matter most, the subthemes moving fastest, the bottlenecks worth backing, and the business models under the most pressure.</p>
<div class="lead"><p>In 2025-2026, demand is still there. What changed is who can actually keep the margin. The winners usually control the customer relationship, handle the paperwork and proof burden, fit the new consumer mood, or own the physical constraint underneath the market.</p></div>

<section class="section">
  <h2>Top Themes</h2>
  <div class="grid">{theme_cards}</div>
</section>

<section class="section">
  <h2>Fastest-Accelerating Subthemes</h2>
  <div class="card"><ul class="list">{subtheme_items}</ul></div>
</section>

<section class="section">
  <h2>Most Investable Bottlenecks</h2>
  <div class="card"><ul class="list">{bottleneck_items}</ul></div>
</section>

<section class="section">
  <h2>Most Exposed Models</h2>
  <div class="card"><ul class="list">{exposed_items}</ul></div>
</section>

<section class="section">
  <h2>How to Use the Stack</h2>
  <div class="split">
    <div class="card">
      <div class="meta">Operators</div>
      <h3>What to do next</h3>
      <ul class="list">
        <li>Be clear about the chokepoint, workflow, or customer trust layer you actually control.</li>
        <li>Reduce exposure to generic middle positions that only work when demand stays easy.</li>
        <li>Turn macro change into concrete pricing, staffing, workflow, and channel decisions fast.</li>
      </ul>
    </div>
    <div class="card">
      <div class="meta">Investors</div>
      <h3>What to underwrite</h3>
      <ul class="list">
        <li>Back scarce rails, mandatory workflows, and physical choke points.</li>
        <li>Prefer repeatable proof systems over labor-heavy service models.</li>
        <li>Avoid markets where demand is real but the profit pool sits somewhere else.</li>
      </ul>
    </div>
  </div>
</section>

</div></body></html>"""

    OUT.write_text(html_doc, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
