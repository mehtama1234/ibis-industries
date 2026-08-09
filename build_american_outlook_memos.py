#!/usr/bin/env python3
"""Build applied memos from the master American outlook layer."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
OUT = ROOT / "american-outlook-memos.html"


MEMOS = [
    {
        "slug": "societal-systems-memo",
        "label": "Societal",
        "title": "Societal Systems Memo",
        "thesis": "The biggest societal pressure is not raw need. It is the system burden created by aging, housing friction, and thinner institutional support.",
        "operator_angle": "Reduce coordination load for households or institutions. That is where the durable pain sits.",
        "investor_angle": "Prefer rails around care, housing immobility, benefits fragmentation, and managed workflows over labor-heavy exposure without system leverage.",
        "linked_themes": [
            "aging-care-and-the-assistance-economy",
            "work-without-the-old-firm",
            "space-housing-and-local-friction",
        ],
        "best_hunting_grounds": [
            "family-coordination and reimbursement infrastructure",
            "portable admin, payroll, and benefits support for fragmented work",
            "housing-lock-in beneficiaries tied to local maintenance, rental support, and neighborhood services",
            "businesses turning institutional friction into repeatable workflow",
        ],
        "watch_for": [
            "rising coordination burden hidden inside categories that still look demand-rich",
            "sectors where labor shortage and administrative drag cap monetization",
            "new dependence on households to manage more of the system themselves",
        ],
    },
    {
        "slug": "cultural-reclassification-memo",
        "label": "Cultural",
        "title": "Cultural Reclassification Memo",
        "thesis": "Culture is changing what Americans consider healthy, respectable, social, and identity-bearing, and that is reorganizing category economics.",
        "operator_angle": "Design for the new permission structure around health, affiliation, participation, and self-presentation.",
        "investor_angle": "Prefer businesses that benefit when category legitimacy shifts toward wellness, community, moderation, and experience.",
        "linked_themes": [
            "wellness-recodes-daily-life",
            "experience-status-and-community",
            "work-without-the-old-firm",
        ],
        "best_hunting_grounds": [
            "wellness-coded consumption and recurring self-improvement routines",
            "experience formats with repeatable cultural or community gravity",
            "affiliation and fandom ecosystems with durable monetization loops",
            "service models that help customers feel competent, modern, or socially legible",
        ],
        "watch_for": [
            "old cultural scripts still embedded in product design or store logic",
            "vice and indulgence categories that have lost social permission faster than they have lost revenue",
            "categories where status migrated from ownership to participation",
        ],
    },
    {
        "slug": "consumer-selection-memo",
        "label": "Consumer",
        "title": "Consumer Selection Memo",
        "thesis": "The consumer is still spending, but the bar for what deserves the spend is much harsher and much more explicit.",
        "operator_angle": "Be legible fast: prudent, premium, convenient, healthy, or meaningful. The muddled middle gets punished.",
        "investor_angle": "Own value systems, premium refuges, convenience rails, and identity-rich categories rather than generic mid-tier exposure.",
        "linked_themes": [
            "barbelled-consumer-america",
            "wellness-recodes-daily-life",
            "experience-status-and-community",
        ],
        "best_hunting_grounds": [
            "scale value formats with strong own-brand economics",
            "premium niches with visible quality justification",
            "convenience businesses that remove real friction rather than just add fees",
            "retail and service formats that combine identity, habit, and experience",
        ],
        "watch_for": [
            "trade-down without shame in categories once protected by brand status",
            "categories where convenience survives even as broad pricing power weakens",
            "mid-market formats still assuming broad undifferentiated demand will come back",
        ],
    },
    {
        "slug": "industrial-control-memo",
        "label": "Industrial",
        "title": "Industrial Control Memo",
        "thesis": "The industrial winner is increasingly the business that controls the stack, the bottleneck, or the mandatory workflow rather than just the visible product.",
        "operator_angle": "Follow the real choke points: power, land, labor, compliance, procurement, and system ownership.",
        "investor_angle": "Prefer infrastructure, regulated workflow, specified capability, and scale-control positions over generalized growth stories.",
        "linked_themes": [
            "physical-reindustrialization-and-infrastructure",
            "machine-intelligence-and-compute-buildout",
            "regulated-software-and-admin-state",
            "scale-financialization-and-the-owned-economy",
        ],
        "best_hunting_grounds": [
            "power- and utility-linked infrastructure",
            "compliance and trust rails embedded in required workflows",
            "specified manufacturing and buildout bottlenecks",
            "asset or governance layers that capture the spread created by complexity",
        ],
        "watch_for": [
            "AI or reshoring narratives detached from real physical constraints",
            "operators serving growth without owning any scarce layer of the stack",
            "middlemen that can be compressed by scale owners or workflow software",
        ],
    },
]


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.45rem,5vw,4.2rem);line-height:1;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3,.panel h3{margin:.2em 0 .35em;font-size:1.12rem}.card p,.panel p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.memo{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.memo:first-of-type{margin-top:0;padding-top:0;border-top:none}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_theme_lookup() -> dict[str, dict]:
    with THEMES_JSON.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return {theme["slug"]: theme for theme in data["themes"]}


def collect_evidence(theme_lookup: dict[str, dict], linked_themes: list[str]) -> dict[str, list]:
    tensions: list[str] = []
    signals: list[str] = []
    subthemes: list[str] = []
    for slug in linked_themes:
        theme = theme_lookup[slug]
        for item in theme.get("structural_tensions", [])[:2]:
            if item not in tensions:
                tensions.append(item)
        for item in theme.get("signals_to_watch", [])[:2]:
            if item not in signals:
                signals.append(item)
        for item in theme.get("subthemes", [])[:2]:
            if item["title"] not in subthemes:
                subthemes.append(item["title"])
    return {"tensions": tensions[:4], "signals": signals[:4], "subthemes": subthemes[:5]}


def theme_chip(theme_lookup: dict[str, dict], slug: str) -> str:
    return f'<a class="chip" href="theme-briefs/{e(slug)}.html">{e(theme_lookup[slug]["title"])}</a>'


def render_memo(theme_lookup: dict[str, dict], memo: dict) -> str:
    evidence = collect_evidence(theme_lookup, memo["linked_themes"])
    hunting = "".join(f"<li>{e(item)}</li>" for item in memo["best_hunting_grounds"])
    watch = "".join(f"<li>{e(item)}</li>" for item in memo["watch_for"])
    tensions = "".join(f"<li>{e(item)}</li>" for item in evidence["tensions"])
    signals = "".join(f"<li>{e(item)}</li>" for item in evidence["signals"])
    subthemes = "".join(f'<span class="chip">{e(item)}</span>' for item in evidence["subthemes"])
    chips = "".join(theme_chip(theme_lookup, slug) for slug in memo["linked_themes"])
    return f"""<section class="memo">
  <div class="meta">{e(memo['label'])} memo</div>
  <h3>{e(memo['title'])}</h3>
  <p><b>Thesis:</b> {e(memo['thesis'])}</p>
  <p><b>Operator angle:</b> {e(memo['operator_angle'])}</p>
  <p><b>Investor angle:</b> {e(memo['investor_angle'])}</p>
  <div class="chips">{chips}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">Best hunting grounds</div>
      <ul class="list">{hunting}</ul>
    </div>
    <div class="panel">
      <div class="meta">Watch for</div>
      <ul class="list">{watch}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Core tensions</div>
      <ul class="list">{tensions}</ul>
    </div>
    <div class="panel">
      <div class="meta">Signals</div>
      <ul class="list">{signals}</ul>
      <div class="chips">{subthemes}</div>
    </div>
  </div>
</section>"""


def main() -> None:
    theme_lookup = load_theme_lookup()
    cards = []
    sections = []
    for memo in MEMOS:
        chips = "".join(theme_chip(theme_lookup, slug) for slug in memo["linked_themes"])
        cards.append(
            f"""<article class="card">
  <div class="meta">{e(memo['label'])} memo</div>
  <h3><a href="#{e(memo['slug'])}">{e(memo['title'])}</a></h3>
  <p>{e(memo['thesis'])}</p>
  <div class="chips">{chips}</div>
</article>"""
        )
        sections.append(render_memo(theme_lookup, memo).replace('<section class="memo">', f'<section class="memo" id="{e(memo["slug"])}">', 1))

    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>American Outlook Memos — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="american-outlook-2025-2026.html">American outlook</a><a href="american-economy-2025-2026.html">Capstone</a></div>
<div class="eyebrow">Applied macro memos · US · 2025-2026</div>
<h1>American Outlook Memos</h1>
<p class="sub">This is the board-style memo layer above the outlook essays: four applied macro reads for societal, cultural, consumer, and industrial change.</p>
<div class="kpis">
  <div class="kpi"><div class="n">4</div><div class="l">Macro memos</div></div>
  <div class="kpi"><div class="n">10</div><div class="l">Linked themes</div></div>
  <div class="kpi"><div class="n">16</div><div class="l">Watch items</div></div>
</div>
<div class="lead"><p>The point of this layer is decision compression. It turns the big essays into a smaller number of operating and underwriting reads that can be scanned quickly without losing the structure underneath them.</p></div>

<section class="section">
  <h2>Memo Index</h2>
  <div class="grid">{''.join(cards)}</div>
</section>

<section class="section">
  <h2>The Memos</h2>
  {''.join(sections)}
</section>

</div></body></html>"""

    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(html_doc)

    print(f"wrote {OUT}")
    print(f"memos={len(MEMOS)}")


if __name__ == "__main__":
    main()
