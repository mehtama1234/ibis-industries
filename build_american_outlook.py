#!/usr/bin/env python3
"""Build a master American outlook page organized by major theme families."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
OUT = ROOT / "american-outlook-2025-2026.html"


OUTLOOK = {
    "title": "American Outlook 2025-2026",
    "subtitle": (
        "A higher-level synthesis of the societal, cultural, consumer, and industrial changes "
        "running through the 1,491-industry corpus and the American themes system."
    ),
    "thesis": (
        "The strongest read on America in 2025-2026 is that household behavior, cultural norms, "
        "institutional pressure, and industrial bottlenecks are changing together. The economy is "
        "not moving along one axis. It is reorganizing daily life, work, spending, place, and "
        "physical buildout at the same time."
    ),
    "sections": [
        {
            "slug": "societal-outlook",
            "label": "Societal",
            "title": "A More Assisted, Less Frictionless Society",
            "summary": (
                "The deepest social shift is that more of American life is being routed through "
                "care systems, managed workflows, constrained housing, and thinner work arrangements."
            ),
            "body": [
                "The social baseline is getting heavier. Older households need more care, more coordination, more insurance, and more age-adapted services. Workers face less stable firm attachment and thinner ladders. Families face more logistics around health, housing, and location because more basic decisions now sit inside constrained systems rather than open markets.",
                "This means the country is not simply aging or simply digitizing. It is becoming more managed. More demand sits inside payer rules, staffing shortages, credential systems, zoning friction, and administrative throughput. That raises the importance of operators that can reduce complexity for households rather than just sell into it.",
                "At the societal level, the big question is not just who needs what. It is which institutions and business models can absorb the coordination burden without collapsing under labor intensity or compliance load.",
            ],
            "linked_themes": [
                "aging-care-and-the-assistance-economy",
                "work-without-the-old-firm",
                "space-housing-and-local-friction",
            ],
        },
        {
            "slug": "cultural-outlook",
            "label": "Cultural",
            "title": "Culture Is Reclassifying What Counts as a Good Life",
            "summary": (
                "Wellness, moderation, participation, affiliation, and modular work identity are "
                "changing the categories Americans consider desirable, respectable, or worth paying for."
            ),
            "body": [
                "Cultural change is now economically legible. Health has become a mainstream identity filter. Drinking less, tracking more, and buying products that feel disciplined or functional are not niche behaviors anymore. At the same time, more status is moving toward experience, community, and participation rather than broad ownership of mid-tier goods.",
                "This matters because categories are being reclassified from inside culture before they are rewritten by regulation. Food, beverage, leisure, retail, and self-presentation all change when consumers start asking not only what a product costs, but what it says about them.",
                "The strongest cultural winners are the businesses that help consumers feel competent, modern, healthy, affiliated, or socially legible. The weakest are the ones still assuming older cultural scripts will quietly return.",
            ],
            "linked_themes": [
                "wellness-recodes-daily-life",
                "experience-status-and-community",
                "work-without-the-old-firm",
            ],
        },
        {
            "slug": "consumer-outlook",
            "label": "Consumer",
            "title": "The Consumer Is More Selective, More Split, and Less Forgiving",
            "summary": (
                "American households still spend, but they do it through sharper filters around "
                "value, convenience, health, identity, and permission-to-premium."
            ),
            "body": [
                "The consumer story is no longer a single confidence cycle. Households save hard in interchangeable categories and still spend where they see identity, trust, utility, or experiential payoff. That creates a harsher barbell: obvious value formats keep gaining, true premium refuges survive, and generic middle-market offers keep losing coherence.",
                "This selective behavior is strengthened by technology and culture together. Comparison shopping makes weak price positions more visible. Wellness norms make indulgence categories justify themselves differently. Experience-led spending competes directly with broad physical-goods categories. Convenience becomes its own form of value because time and friction matter more than simple ticket price.",
                "The end result is a consumer economy where the winning offer has to be legible. The buyer needs to know quickly whether a product is prudent, premium, useful, healthy, or meaningful enough to deserve the money.",
            ],
            "linked_themes": [
                "barbelled-consumer-america",
                "wellness-recodes-daily-life",
                "experience-status-and-community",
            ],
        },
        {
            "slug": "industrial-outlook",
            "label": "Industrial",
            "title": "The Physical and Institutional Stack Is Back in Charge",
            "summary": (
                "The industrial story is that power, land, labor, compliance, system ownership, "
                "and strategic scale are reasserting themselves as first-order economic selectors."
            ),
            "body": [
                "For a long stretch, many businesses could act as if physical and institutional constraints were secondary. That is no longer true. AI requires power and land. Reindustrialization requires trades, procurement, and domestic capability. More sectors require compliance, testing, and documentation just to stay in the game. Ownership structure matters more because complexity is harder for fragmented operators to absorb.",
                "This gives the economy a more material shape. Infrastructure, cooling, transmission, logistics corridors, regulated workflow layers, and scale owners all sit closer to value capture than many headline-facing operators do. The visible brand or application is not always the entity with the strongest economics.",
                "The industrial outlook is therefore not just about factories or infrastructure spending. It is about a broader return of bottlenecks, rails, and control layers. The more complex the environment gets, the more advantage shifts to the player that owns the system, the choke point, or the trusted workflow.",
            ],
            "linked_themes": [
                "physical-reindustrialization-and-infrastructure",
                "machine-intelligence-and-compute-buildout",
                "regulated-software-and-admin-state",
                "scale-financialization-and-the-owned-economy",
            ],
        },
    ],
    "closing": [
        "Taken together, these four lenses say the same thing from different angles: America is not just changing demand. It is changing the operating conditions around demand.",
        "The consumer is more selective. Culture is changing category legitimacy. Society is asking more systems to absorb more burden. Industry is being repriced by physical and institutional constraints.",
        "That combination is why the recurring winners in this corpus are not random. They are the businesses with clearer positioning, stronger rails, better system fluency, and more control over whichever bottleneck has become non-negotiable.",
    ],
}


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.62}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.5rem,5vw,4.3rem);line-height:.98;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.06rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:16px;border-top:1px solid var(--line)}.essay{margin-top:18px}.essay h3{font-size:1.36rem;margin:.1em 0 .45em}.essay p{color:var(--muted);margin:.6em 0 0}.summary{font-size:1rem;color:var(--ink)}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3{margin:.2em 0 .35em;font-size:1.1rem}.card p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.close{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px;margin-top:16px}.close p{color:var(--muted);margin:.55em 0 0}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_theme_lookup() -> dict[str, dict]:
    with THEMES_JSON.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return {theme["slug"]: theme for theme in data["themes"]}


def theme_brief_chip(theme_lookup: dict[str, dict], slug: str) -> str:
    theme = theme_lookup[slug]
    return f'<a class="chip" href="theme-briefs/{e(slug)}.html">{e(theme["title"])}</a>'


def collect_section_evidence(theme_lookup: dict[str, dict], linked_themes: list[str]) -> dict[str, list]:
    tensions: list[str] = []
    signals: list[str] = []
    subthemes: list[dict] = []
    seen_subthemes: set[tuple[str, str]] = set()

    for slug in linked_themes:
        theme = theme_lookup[slug]
        for item in theme.get("structural_tensions", [])[:2]:
            if item not in tensions:
                tensions.append(item)
        for item in theme.get("signals_to_watch", [])[:3]:
            if item not in signals:
                signals.append(item)
        for subtheme in theme.get("subthemes", [])[:2]:
            key = (theme["slug"], subtheme["slug"])
            if key in seen_subthemes:
                continue
            seen_subthemes.add(key)
            subthemes.append(
                {
                    "theme_slug": theme["slug"],
                    "theme_title": theme["title"],
                    "slug": subtheme["slug"],
                    "title": subtheme["title"],
                    "deep_read": subtheme.get("deep_read", subtheme.get("summary", "")),
                    "strategic_consequences": subtheme.get("strategic_consequences", []),
                }
            )
    return {
        "tensions": tensions[:4],
        "signals": signals[:5],
        "subthemes": subthemes[:4],
    }


def main() -> None:
    theme_lookup = load_theme_lookup()
    total_signals = sum(theme["signal_count"] for theme in theme_lookup.values())
    total_subthemes = sum(theme["subtheme_count"] for theme in theme_lookup.values())
    cards = []
    sections = []

    for section in OUTLOOK["sections"]:
        chips = "".join(theme_brief_chip(theme_lookup, slug) for slug in section["linked_themes"])
        body = "".join(f"<p>{e(paragraph)}</p>" for paragraph in section["body"])
        evidence = collect_section_evidence(theme_lookup, section["linked_themes"])
        tensions = "".join(f"<li>{e(item)}</li>" for item in evidence["tensions"])
        signals = "".join(f"<li>{e(item)}</li>" for item in evidence["signals"])
        subtheme_cards = "".join(
            f"""<article class="card">
  <div class="meta">{e(item['theme_title'])} subtheme</div>
  <h3><a href="themes/{e(item['theme_slug'])}.html#{e(item['slug'])}">{e(item['title'])}</a></h3>
  <p>{e(item['deep_read'])}</p>
  <p><b>Strategic consequence:</b> {e(item['strategic_consequences'][0]) if item['strategic_consequences'] else ''}</p>
</article>"""
            for item in evidence["subthemes"]
        )
        cards.append(
            f"""<article class="card">
  <div class="meta">{e(section['label'])} outlook</div>
  <h3><a href="#{e(section['slug'])}">{e(section['title'])}</a></h3>
  <p>{e(section['summary'])}</p>
  <div class="chips">{chips}</div>
</article>"""
        )
        sections.append(
            f"""<section class="essay" id="{e(section['slug'])}">
  <div class="meta">{e(section['label'])} outlook</div>
  <h3>{e(section['title'])}</h3>
  <p class="summary">{e(section['summary'])}</p>
  {body}
  <div class="split">
    <div class="card">
      <div class="meta">Core tensions</div>
      <h3>What makes this hard</h3>
      <ul class="list">{tensions}</ul>
    </div>
    <div class="card">
      <div class="meta">Signals</div>
      <h3>What to watch next</h3>
      <ul class="list">{signals}</ul>
    </div>
  </div>
  <div class="grid" style="margin-top:14px">{subtheme_cards}</div>
  <div class="chips">{chips}</div>
</section>"""
        )

    closing = "".join(f"<p>{e(item)}</p>" for item in OUTLOOK["closing"])
    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(OUTLOOK['title'])} — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="american-themes.html">American themes</a><a href="american-economy-2025-2026.html">Capstone</a></div>
<div class="eyebrow">Master synthesis · US · 2025-2026</div>
<h1>{e(OUTLOOK['title'])}</h1>
<p class="sub">{e(OUTLOOK['subtitle'])}</p>
<div class="kpis">
  <div class="kpi"><div class="n">4</div><div class="l">Master lenses</div></div>
  <div class="kpi"><div class="n">10</div><div class="l">Themes</div></div>
  <div class="kpi"><div class="n">{total_subthemes}</div><div class="l">Subthemes</div></div>
  <div class="kpi"><div class="n">{total_signals}</div><div class="l">Signals</div></div>
</div>
<div class="lead"><p>{e(OUTLOOK['thesis'])}</p></div>

<section class="section">
  <h2>Map</h2>
  <div class="grid">{''.join(cards)}</div>
</section>

<section class="section">
  <h2>The Read</h2>
  {''.join(sections)}
</section>

<section class="section">
  <h2>Closing Read</h2>
  <div class="close">{closing}</div>
</section>

</div></body></html>"""

    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(html_doc)

    print(f"wrote {OUT}")
    print(f"sections={len(OUTLOOK['sections'])}")


if __name__ == "__main__":
    main()
