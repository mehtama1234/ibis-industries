#!/usr/bin/env python3
"""Build a polished long-form memo from the ranked synthesis layer."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RANKINGS_JSON = ROOT / "american_rankings.json"
OUT = ROOT / "american-implications-memo.html"


MEMO_SECTIONS = [
    {
        "title": "Societal implications",
        "body": [
            "The social story is that more of American life now sits inside systems that are hard to navigate casually. Aging households need assistance, families need coordination, and work is less likely to provide a stable institutional wrapper around benefits, training, or career progression.",
            "That means the country is becoming more managed even when it is not becoming more formally planned. The important question is no longer only what people need. It is which operators can absorb the staffing, reimbursement, credential, and documentation burden without breaking the economics.",
        ],
        "theme_slugs": ["aging-care-and-the-assistance-economy", "work-without-the-old-firm", "regulated-software-and-admin-state", "space-housing-and-local-friction"],
    },
    {
        "title": "Cultural implications",
        "body": [
            "Culture is moving dollars before policy catches up. Wellness, moderation, affiliation, and experience are reclassifying categories from the inside. What looks respectable, prudent, healthy, or identity-bearing is changing faster than many companies update their category strategy.",
            "The businesses that win are the ones that help consumers feel competent, modern, and legible to themselves or to others. The ones that lose are still describing their market with old permission structures.",
        ],
        "theme_slugs": ["wellness-recodes-daily-life", "experience-status-and-community", "barbelled-consumer-america"],
    },
    {
        "title": "Consumer implications",
        "body": [
            "The consumer is not collapsing. The consumer is ranking. Households are more deliberate about where they save, where they trade down, where they pay for convenience, and where they still buy premium identity or reliability.",
            "That change is why the middle keeps weakening. Broad mid-market offers no longer get paid just for existing; they need either obvious value, obvious quality, or genuine time-saving convenience.",
        ],
        "theme_slugs": ["barbelled-consumer-america", "wellness-recodes-daily-life", "experience-status-and-community"],
    },
    {
        "title": "Industrial implications",
        "body": [
            "The industrial story is that more sectors now depend on physical and institutional realities that used to be treated as background conditions. Power, land, cooling, transmission, domestic capability, compliance, and ownership topology are now first-order selectors.",
            "AI sharpens this rather than softening it. The digital upside increasingly rides on heavy physical constraints, and many of the best economics sit under the interface rather than inside it.",
        ],
        "theme_slugs": ["physical-reindustrialization-and-infrastructure", "machine-intelligence-and-compute-buildout", "scale-financialization-and-the-owned-economy", "regulated-software-and-admin-state"],
    },
]


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.66}.wrap{max-width:1100px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.5rem,5vw,4.2rem);line-height:.98;margin:.18em 0 .22em;max-width:13ch}h2{font-size:1.55rem;margin:0 0 .5em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead,.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.lead{border-left:4px solid var(--gold);border-radius:0 12px 12px 0;margin:26px 0}.lead p,.panel p{margin:.5em 0 0;color:var(--muted)}.lead p:first-child,.panel p:first-child{margin-top:0}.section{margin-top:34px;padding-top:16px;border-top:1px solid var(--line)}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.45em 0}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def main() -> None:
    rankings = json.loads(RANKINGS_JSON.read_text())
    themes = {item["slug"]: item for item in rankings["top_themes"]}
    subthemes = {}
    for item in rankings["top_subthemes"]:
        subthemes.setdefault(item["theme_slug"], []).append(item)
    bottlenecks = {}
    for item in rankings["top_bottlenecks"]:
        bottlenecks.setdefault(item["theme_slug"], []).append(item)
    exposed = {}
    for item in rankings["top_exposed_models"]:
        exposed.setdefault(item["theme_slug"], []).append(item)

    sections_html = []
    for section in MEMO_SECTIONS:
        theme_titles = [themes[slug]["title"] for slug in section["theme_slugs"] if slug in themes]
        signal_list = []
        bottleneck_list = []
        exposed_list = []
        for slug in section["theme_slugs"]:
            if slug in themes:
                signal_list.extend(themes[slug]["signals"][:1])
            if slug in bottlenecks:
                bottleneck_list.extend([row["title"] for row in bottlenecks[slug][:1]])
            if slug in exposed:
                exposed_list.extend([row["title"] for row in exposed[slug][:1]])
        accel_rows = []
        for slug in section["theme_slugs"]:
            accel_rows.extend(subthemes.get(slug, [])[:2])
        accel_rows = accel_rows[:4]
        sections_html.append(
            f"""<section class="section">
  <h2>{e(section['title'])}</h2>
  <div class="lead">{''.join(f'<p>{e(p)}</p>' for p in section['body'])}</div>
  <div class="chips">{''.join(f'<span class="chip">{e(title)}</span>' for title in theme_titles)}</div>
  <div class="split" style="margin-top:14px">
    <div class="panel">
      <div class="eyebrow">Key signals</div>
      <ul class="list">{''.join(f'<li>{e(item)}</li>' for item in signal_list[:4])}</ul>
    </div>
    <div class="panel">
      <div class="eyebrow">Most important bottlenecks</div>
      <ul class="list">{''.join(f'<li>{e(item)}</li>' for item in bottleneck_list[:4])}</ul>
    </div>
  </div>
  <div class="split" style="margin-top:14px">
    <div class="panel">
      <div class="eyebrow">Fastest-accelerating subthemes</div>
      <ul class="list">{''.join(f'<li><b>{e(row["title"])}</b>: {e(row["summary"])}</li>' for row in accel_rows)}</ul>
    </div>
    <div class="panel">
      <div class="eyebrow">Most exposed models</div>
      <ul class="list">{''.join(f'<li>{e(item)}</li>' for item in exposed_list[:4])}</ul>
    </div>
  </div>
</section>"""
        )

    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>American Implications Memo — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="american-synthesis-hub.html">Synthesis hub</a><a href="index.html">Industry briefs</a><a href="american-rankings.html">Rankings</a><a href="american-executive-summary.html">Executive summary</a><a href="american-synthesis-playbook.html">Playbook</a><a href="american-economy-2025-2026.html">Capstone</a><a href="american-outlook-2025-2026.html">American outlook</a></div>
<div class="eyebrow">Implications memo · US · 2025-2026</div>
<h1>American Implications Memo</h1>
<p class="sub">A polished long-form memo built from the ranked synthesis stack, focused on the societal, cultural, consumer, and industrial implications of the US economy.</p>
<div class="lead"><p>The short version is that America is not short on demand. It is short on easy ways to capture demand without control, proof, cultural fit, or the right position inside a tightening physical and institutional stack.</p></div>
{''.join(sections_html)}
</div></body></html>"""

    OUT.write_text(html_doc, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
