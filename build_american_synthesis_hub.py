#!/usr/bin/env python3
"""Build a dedicated landing page for the American synthesis stack."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RANKINGS_JSON = ROOT / "american_rankings.json"
OUT = ROOT / "american-synthesis-hub.html"


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1200px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.6rem,5vw,4.3rem);line-height:.98;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:940px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3{margin:.2em 0 .35em;font-size:1.1rem}.card p{margin:.35em 0 0;color:var(--muted)}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def main() -> None:
    rankings = json.loads(RANKINGS_JSON.read_text())
    top_themes = rankings["top_themes"][:4]
    top_bottlenecks = rankings["top_bottlenecks"][:4]

    stack_cards = [
        ("Executive summary", "american-executive-summary.html", "The shortest decision-grade entry point."),
        ("Rankings", "american-rankings.html", "The ordered layer for themes, subthemes, bottlenecks, and exposed models."),
        ("Playbook", "american-synthesis-playbook.html", "The direct end-state read on what to do and what to underwrite."),
        ("Implications memo", "american-implications-memo.html", "The polished long-form societal, cultural, consumer, and industrial memo."),
        ("American outlook", "american-outlook-2025-2026.html", "The four-lens macro interpretation."),
        ("Capstone", "american-economy-2025-2026.html", "The full end-to-end economic argument."),
        ("Theme memos", "american-theme-memos.html", "Applied theme-level operator and investor translation."),
        ("Sector memos", "sector-memos.html", "Sector expression of the synthesis layer."),
        ("Company memos", "company-memos.html", "Named evidence and company-level judgment."),
    ]

    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>American Synthesis Hub — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="american-rankings.html">Rankings</a><a href="american-executive-summary.html">Executive summary</a><a href="american-implications-memo.html">Implications memo</a></div>
<div class="eyebrow">Synthesis hub · US · 2025-2026</div>
<h1>American Synthesis Hub</h1>
<p class="sub">The front door for the 2025-2026 US synthesis stack: ranked themes, decision surfaces, macro interpretation, and derivative briefing formats built from the 1,491-industry corpus.</p>
<div class="lead"><p>The stack now has three distinct uses: understand the system, prioritize what matters, and communicate the implications in operator, investor, or board-ready form.</p></div>

<section class="section">
  <h2>Start Here</h2>
  <div class="grid">{"".join(f'<article class="card"><div class="meta">{e(label)}</div><h3><a href="{e(href)}">{e(label)}</a></h3><p>{e(body)}</p></article>' for label, href, body in stack_cards[:4])}</div>
</section>

<section class="section">
  <h2>Top Themes Right Now</h2>
  <div class="grid">{"".join(f'<article class="card"><div class="meta">{e(theme["lens"])}</div><h3>{e(theme["title"])}</h3><p>{e(theme["thesis"])}</p><div class="chips">{"".join(f"<span class=\"chip\">{e(signal)}</span>" for signal in theme["signals"])}</div></article>' for theme in top_themes)}</div>
</section>

<section class="section">
  <h2>Best Bottlenecks To Underwrite</h2>
  <div class="card"><ul class="list">{"".join(f'<li><b>{e(item["title"])}</b>: {e(item["rationale"])}</li>' for item in top_bottlenecks)}</ul></div>
</section>

<section class="section">
  <h2>Full Stack</h2>
  <div class="grid">{"".join(f'<article class="card"><div class="meta">{e(label)}</div><h3><a href="{e(href)}">{e(label)}</a></h3><p>{e(body)}</p></article>' for label, href, body in stack_cards[4:])}</div>
</section>

</div></body></html>"""
    OUT.write_text(html_doc, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
