#!/usr/bin/env python3
"""Build a concise end-state synthesis playbook for the US economy layer."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
COMPANY_MEMOS_JSON = ROOT / "company_memos.json"
OUT = ROOT / "american-synthesis-playbook.html"


PLAYBOOK = {
    "title": "American Synthesis Playbook",
    "subtitle": (
        "A direct end-state read on the 2025-2026 US economy: what is happening, "
        "why it matters, where it shows up, and what operators and investors should do."
    ),
    "thesis": (
        "The United States in 2025-2026 is not defined by one clean macro cycle. It is defined "
        "by a harsher selection system. Households are more selective, culture is reclassifying "
        "whole categories, institutions demand more coordination and proof, and the physical "
        "economy is back in charge of many digital outcomes."
    ),
    "national_calls": [
        {
            "title": "Demand still exists, but the right to earn margin is narrower",
            "body": "Many categories still have spend, need, or traffic. What changed is the burden required to turn that demand into durable economics. Labor, compliance, capital, and channel pressure now decide who keeps the value.",
            "themes": [
                "scale-financialization-and-the-owned-economy",
                "regulated-software-and-admin-state",
                "physical-reindustrialization-and-infrastructure",
            ],
        },
        {
            "title": "The middle weakens while value, scarcity, and control strengthen",
            "body": "The generic middle keeps eroding across consumer categories, regional intermediaries, and undifferentiated service stacks. The stronger positions are value machines, premium refuges, specified bottlenecks, and ownership of the rail beneath the experience.",
            "themes": [
                "barbelled-consumer-america",
                "scale-financialization-and-the-owned-economy",
                "space-housing-and-local-friction",
            ],
        },
        {
            "title": "America is becoming more assisted and more administered",
            "body": "Aging, fragmented work, thinner firms, reimbursement complexity, and trust infrastructure are all pushing more of the economy toward coordination-heavy systems. The growth is real, but the monetization often sits with the enabler rather than the visible frontline operator.",
            "themes": [
                "aging-care-and-the-assistance-economy",
                "work-without-the-old-firm",
                "regulated-software-and-admin-state",
            ],
        },
        {
            "title": "Cultural shifts are moving dollars before policy changes categories",
            "body": "Wellness, moderation, identity-bearing experiences, and permission-to-premium behavior are already reallocating demand. The consumer often rewrites the category before regulators, investors, or management teams update their language.",
            "themes": [
                "wellness-recodes-daily-life",
                "experience-status-and-community",
                "barbelled-consumer-america",
            ],
        },
        {
            "title": "AI is a physical economy story as much as a software story",
            "body": "Inference and automation demand flow upward into power, cooling, land, construction, equipment, permitting, and capital concentration. That means many of the best economics sit under the application layer rather than on the visible interface.",
            "themes": [
                "machine-intelligence-and-compute-buildout",
                "physical-reindustrialization-and-infrastructure",
                "scale-financialization-and-the-owned-economy",
            ],
        },
        {
            "title": "Operators and investors need a bottleneck map, not just a market map",
            "body": "The recurring winners are not random. They are the businesses that either own the bottleneck, absorb the complexity, shape the customer permission structure, or become culturally and operationally indispensable inside a fragmented system.",
            "themes": [
                "regulated-software-and-admin-state",
                "scale-financialization-and-the-owned-economy",
                "machine-intelligence-and-compute-buildout",
                "barbelled-consumer-america",
            ],
        },
    ],
    "lens_groups": [
        {
            "title": "Consumer",
            "summary": "Demand splits harder between prudence, permission-to-premium, convenience, and symbolic spend.",
            "themes": [
                "barbelled-consumer-america",
                "wellness-recodes-daily-life",
                "experience-status-and-community",
            ],
        },
        {
            "title": "Cultural and social",
            "summary": "Health, identity, participation, and modular work are changing what looks modern, respectable, and worth paying for.",
            "themes": [
                "wellness-recodes-daily-life",
                "experience-status-and-community",
                "work-without-the-old-firm",
            ],
        },
        {
            "title": "Societal and institutional",
            "summary": "Older households, managed systems, reimbursement, credentials, and trust infrastructure are thickening the coordination layer around daily life.",
            "themes": [
                "aging-care-and-the-assistance-economy",
                "work-without-the-old-firm",
                "regulated-software-and-admin-state",
                "space-housing-and-local-friction",
            ],
        },
        {
            "title": "Industrial and physical",
            "summary": "Power, land, trades, domestic capability, and system ownership now govern more outcomes that once looked digital or asset-light.",
            "themes": [
                "physical-reindustrialization-and-infrastructure",
                "machine-intelligence-and-compute-buildout",
                "scale-financialization-and-the-owned-economy",
            ],
        },
    ],
    "closing": [
        "The practical lesson is simple: the United States is still full of demand, but much less full of easy economics.",
        "The better operating and investing posture is to look for control, proof, bottlenecks, permission structures, and category legitimacy rather than broad exposure alone.",
        "That is the synthesis claim this repo now supports across the full 1,491-industry corpus.",
    ],
}


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.62}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.5rem,5vw,4.3rem);line-height:.98;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.06rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:16px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3{margin:.2em 0 .35em;font-size:1.1rem}.card p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.close{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px;margin-top:16px}.close p{color:var(--muted);margin:.55em 0 0}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def dedupe(values: list[str], limit: int | None = None) -> list[str]:
    out: list[str] = []
    seen: set[str] = set()
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
        if limit is not None and len(out) >= limit:
            break
    return out


def load_theme_lookup() -> dict[str, dict]:
    data = json.loads(THEMES_JSON.read_text())
    return {theme["slug"]: theme for theme in data["themes"]}


def load_company_lookup() -> dict[str, dict]:
    data = json.loads(COMPANY_MEMOS_JSON.read_text())
    return {company["slug"]: company for company in data}


def collect_group_evidence(
    theme_lookup: dict[str, dict], company_lookup: dict[str, dict], linked_themes: list[str]
) -> dict[str, list]:
    sectors: Counter[str] = Counter()
    companies: list[str] = []
    signals: list[str] = []
    tensions: list[str] = []
    operator_implications: list[str] = []
    capital_implications: list[str] = []
    second_order_effects: list[str] = []
    theme_titles: list[str] = []
    for slug in linked_themes:
        theme = theme_lookup[slug]
        theme_titles.append(theme["title"])
        signals.extend(theme.get("signals_to_watch", [])[:2])
        tensions.extend(theme.get("structural_tensions", [])[:2])
        operator_implications.extend(theme.get("strategic_implications", [])[:2])
        capital_implications.extend(theme.get("capital_implications", [])[:2])
        second_order_effects.extend(theme.get("second_order_effects", [])[:1])
        for subtheme in theme.get("subthemes", [])[:2]:
            for industry in subtheme.get("industries", []):
                sector = industry.get("sector")
                if sector:
                    sectors[sector] += 1
            for company in subtheme.get("companies", []):
                company_slug = company.get("slug")
                if company_slug and company_slug in company_lookup:
                    companies.append(company_lookup[company_slug]["title"])
    return {
        "theme_titles": dedupe(theme_titles, 4),
        "signals": dedupe(signals, 4),
        "tensions": dedupe(tensions, 3),
        "operator_implications": dedupe(operator_implications, 4),
        "capital_implications": dedupe(capital_implications, 4),
        "second_order_effects": dedupe(second_order_effects, 2),
        "top_sectors": sectors.most_common(4),
        "companies": dedupe(companies, 4),
    }


def build_national_cards(theme_lookup: dict[str, dict], company_lookup: dict[str, dict]) -> str:
    cards = []
    for item in PLAYBOOK["national_calls"]:
        evidence = collect_group_evidence(theme_lookup, company_lookup, item["themes"])
        cards.append(
            f"""<article class="card">
  <div class="meta">National call</div>
  <h3>{e(item['title'])}</h3>
  <p>{e(item['body'])}</p>
  <p><b>Where it shows up:</b> {e('; '.join(f'{sector} ({count})' for sector, count in evidence['top_sectors']))}</p>
  <p><b>Signals:</b> {e(' | '.join(evidence['signals']))}</p>
  <p><b>Tensions:</b> {e(' | '.join(evidence['tensions']))}</p>
  <p><b>Representative companies:</b> {e('; '.join(evidence['companies']))}</p>
  <div class="chips">{''.join(f'<span class="chip">{e(theme)}</span>' for theme in evidence['theme_titles'])}</div>
</article>"""
        )
    return "".join(cards)


def build_lens_cards(theme_lookup: dict[str, dict], company_lookup: dict[str, dict]) -> str:
    cards = []
    for item in PLAYBOOK["lens_groups"]:
        evidence = collect_group_evidence(theme_lookup, company_lookup, item["themes"])
        cards.append(
            f"""<article class="card">
  <div class="meta">{e(item['title'])} lens</div>
  <h3>{e(item['summary'])}</h3>
  <p><b>Where it shows up:</b> {e('; '.join(f'{sector} ({count})' for sector, count in evidence['top_sectors']))}</p>
  <p><b>Signals:</b> {e(' | '.join(evidence['signals']))}</p>
  <div class="meta" style="margin-top:14px">What to do</div>
  <ul class="list">{''.join(f'<li>{e(text)}</li>' for text in evidence['operator_implications'][:3])}</ul>
  <div class="meta" style="margin-top:14px">What to underwrite</div>
  <ul class="list">{''.join(f'<li>{e(text)}</li>' for text in evidence['capital_implications'][:3])}</ul>
  <div class="meta" style="margin-top:14px">Second-order effects</div>
  <ul class="list">{''.join(f'<li>{e(text)}</li>' for text in evidence['second_order_effects'])}</ul>
</article>"""
        )
    return "".join(cards)


def main() -> None:
    theme_lookup = load_theme_lookup()
    company_lookup = load_company_lookup()

    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(PLAYBOOK['title'])} — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="american-synthesis-hub.html">Synthesis hub</a><a href="index.html">Industry briefs</a><a href="american-rankings.html">Rankings</a><a href="american-executive-summary.html">Executive summary</a><a href="economic-intelligence.html">Economic intelligence</a><a href="american-outlook-2025-2026.html">American outlook</a><a href="american-economy-2025-2026.html">Capstone</a><a href="american-theme-memos.html">Theme memos</a></div>
<div class="eyebrow">Executive synthesis · US · 2025-2026</div>
<h1>{e(PLAYBOOK['title'])}</h1>
<p class="sub">{e(PLAYBOOK['subtitle'])}</p>
<div class="kpis">
  <div class="kpi"><div class="n">1491</div><div class="l">Industry briefs</div></div>
  <div class="kpi"><div class="n">10</div><div class="l">Themes</div></div>
  <div class="kpi"><div class="n">6</div><div class="l">National calls</div></div>
  <div class="kpi"><div class="n">4</div><div class="l">Lens playbooks</div></div>
</div>
<div class="lead"><p>{e(PLAYBOOK['thesis'])}</p></div>

<section class="section">
  <h2>National Read</h2>
  <div class="grid">{build_national_cards(theme_lookup, company_lookup)}</div>
</section>

<section class="section">
  <h2>Lens Playbooks</h2>
  <div class="grid">{build_lens_cards(theme_lookup, company_lookup)}</div>
</section>

<section class="section">
  <h2>Closing Read</h2>
  <div class="close">{''.join(f'<p>{e(item)}</p>' for item in PLAYBOOK['closing'])}</div>
</section>

</div></body></html>"""

    OUT.write_text(html_doc, encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
