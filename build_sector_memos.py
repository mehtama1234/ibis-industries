#!/usr/bin/env python3
"""Build major-sector memos from the themes, briefs, and company layers."""

from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRIEFS_JSON = ROOT / "briefs_full.json"
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
COMPANIES_JSON = ROOT / "company_universe.json"
OUT = ROOT / "sector-memos.html"
PAGES_OUT = ROOT / "sector-memos"
SECTOR_PROSE_JSON = ROOT / "sector_prose.json"  # authored sector prose, keyed by sector slug


SECTOR_CONFIG = {
    "Agriculture": {
        "operator_angle": "Treat volatility, biology, and trade exposure as core economics rather than background noise.",
        "investor_angle": "Prefer sectors with distribution leverage, controlled-environment advantages, or strong ties to processing and infrastructure rather than pure commodity exposure.",
    },
    "Business Services": {
        "operator_angle": "The best businesses convert complexity into recurring workflows instead of selling hours alone.",
        "investor_angle": "Prefer firms with embedded compliance, specialized expertise, or software-led delivery over generic people-heavy service models.",
    },
    "Construction": {
        "operator_angle": "Follow bottlenecks: labor, permitting, power, and specialized scope matter more than generic backlog bragging.",
        "investor_angle": "Own scarce trades, infrastructure-linked contractors, and disciplined operators positioned beside unavoidable build cycles.",
    },
    "Consumer Services": {
        "operator_angle": "Consumer services win when they combine local presence with habit, convenience, or identity rather than generic discretionary spend.",
        "investor_angle": "Prefer repeatable formats with pricing discipline, retention loops, or premium niches over undifferentiated service capacity.",
    },
    "Energy & Environment": {
        "operator_angle": "Energy businesses increasingly sit inside the AI, electrification, and compliance stack, not outside the economy’s main story.",
        "investor_angle": "Prefer transmission, power-linked infrastructure, and environmental compliance enablers over undifferentiated exposure to commodity swings.",
    },
    "Finance & Insurance": {
        "operator_angle": "The key question is whether the business owns rails, trust, workflow, or simply a shrinking spread.",
        "investor_angle": "Prefer scaled institutions, data-rich intermediaries, and mandatory workflow layers over regional middlemen without strong moats.",
    },
    "Food & Drink": {
        "operator_angle": "This sector now has to answer to health behavior, ingredient volatility, and channel power at the same time.",
        "investor_angle": "Prefer health-aligned, functional, premium, or distribution-advantaged positions over generic volume-dependent indulgence stories.",
    },
    "Healthcare": {
        "operator_angle": "Demand is rarely the problem. Labor, reimbursement, and administrative execution are the real constraints.",
        "investor_angle": "Prefer enabling infrastructure, chronic-care systems, and reimbursement-fluent operators over labor-heavy exposure without pricing control.",
    },
    "Manufacturing": {
        "operator_angle": "Specification, access to inputs, and the right side of industrial bottlenecks matter more than generalized factory optimism.",
        "investor_angle": "Prefer specified manufacturers, domestic capability in strategic categories, and businesses attached to buildout bottlenecks.",
    },
    "Media & Entertainment": {
        "operator_angle": "Attention is abundant, but monetizable scarcity is not.",
        "investor_angle": "Prefer rights owners, participation-led formats, and strong affiliation ecosystems over generic ad-dependent or easily substitutable media capacity.",
    },
    "Real Estate": {
        "operator_angle": "Read assets through present-day flows of work, housing, logistics, and power rather than old category labels.",
        "investor_angle": "Prefer logistics, utility-linked land, adaptive reuse capability, and assets aligned with current demand geometry over weak commodity office exposure.",
    },
    "Retail": {
        "operator_angle": "Pick value, pick premium, or build real convenience. The middle gets punished.",
        "investor_angle": "Prefer scale retailers, private-label systems, and formats that combine channel control with habit or experience.",
    },
    "Technology & Digital": {
        "operator_angle": "AI and software advantage depend on workflow ownership, infrastructure access, and trust, not just feature velocity.",
        "investor_angle": "Prefer embedded workflow software, compute-adjacent infrastructure, and control layers with recurring necessity.",
    },
    "Transport & Logistics": {
        "operator_angle": "Orchestration, density, and labor discipline matter more than simple volume narratives.",
        "investor_angle": "Prefer networks with throughput leverage, freight intelligence, and asset positioning near strategic flows over generic exposed capacity.",
    },
}


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--green:#78ca90;--red:#e07d6d;--amber:#d9a441;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1220px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.4rem,5vw,4.2rem);line-height:1;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel,.brief{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3,.panel h3,.brief h3{margin:.2em 0 .35em;font-size:1.12rem}.card p,.panel p,.brief p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.memo{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.memo:first-of-type{margin-top:0;padding-top:0;border-top:none}.memo h3{font-size:1.28rem;margin:.2em 0 .35em}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.smallgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-top:14px}.mini{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:12px}.mini h4{margin:0 0 .35em;font-size:.96rem}.mini p{margin:0;color:var(--muted);font-size:.9rem}.subcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-top:14px}.subcard{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:14px}.subcard h4{margin:.2em 0 .35em;font-size:1rem}.subcard p{margin:.35em 0 0;color:var(--muted);font-size:.95rem}.status{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:.68rem;border:1px solid var(--line);border-radius:999px;padding:4px 8px}.status.adv{color:var(--green)}.status.mix{color:var(--amber)}.status.exp{color:var(--red)}@media(max-width:920px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def slugify(value: str) -> str:
    return (
        value.lower()
        .replace("&", "and")
        .replace(" ", "-")
        .replace("/", "-")
    )


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def top_industries_for_sector(briefs: list[dict], sector: str) -> list[dict]:
    rows = [b for b in briefs if b.get("sector") == sector]
    return sorted(rows, key=lambda row: (row.get("title", "")))[:6]


def build_sector_records() -> list[dict]:
    briefs = load_json(BRIEFS_JSON)
    themes = load_json(THEMES_JSON)["themes"]
    companies = load_json(COMPANIES_JSON)
    sector_prose = load_json(SECTOR_PROSE_JSON) if SECTOR_PROSE_JSON.exists() else {}

    sector_data: dict[str, dict] = {}
    for sector, cfg in SECTOR_CONFIG.items():
        sector_data[sector] = {
            "slug": slugify(sector),
            "sector": sector,
            "operator_angle": cfg["operator_angle"],
            "investor_angle": cfg["investor_angle"],
            "industry_count": 0,
            "theme_counts": Counter(),
            "force_counts": Counter(),
            "theme_objects": {},
            "subtheme_records": [],
            "subtheme_keys": set(),
            "example_industries": [],
            "advantaged": [],
            "mixed": [],
            "exposed": [],
        }

    for brief in briefs:
        sector = brief.get("sector")
        if sector in sector_data:
            sector_data[sector]["industry_count"] += 1

    for theme in themes:
        for subtheme in theme["subthemes"]:
            for industry in subtheme["industries"]:
                sector = industry.get("sector")
                if sector in sector_data:
                    sector_data[sector]["theme_counts"][theme["title"]] += 1
                    sector_data[sector]["theme_objects"][theme["slug"]] = {
                        "slug": theme["slug"],
                        "title": theme["title"],
                        "lens": theme["lens"],
                        "structural_tensions": theme.get("structural_tensions", []),
                        "signals_to_watch": theme.get("signals_to_watch", []),
                        "strategic_implications": theme.get("strategic_implications", []),
                        "capital_implications": theme.get("capital_implications", []),
                    }
                    subtheme_key = (theme["slug"], subtheme["slug"])
                    if subtheme_key not in sector_data[sector]["subtheme_keys"]:
                        sector_data[sector]["subtheme_keys"].add(subtheme_key)
                        sector_data[sector]["subtheme_records"].append(
                            {
                                "theme_slug": theme["slug"],
                                "theme_title": theme["title"],
                                "slug": subtheme["slug"],
                                "title": subtheme["title"],
                                "deep_read": subtheme.get("deep_read", subtheme.get("summary", "")),
                                "pressure_points": subtheme.get("pressure_points", []),
                                "signals_to_watch": subtheme.get("signals_to_watch", []),
                                "strategic_consequences": subtheme.get("strategic_consequences", []),
                                "forces": subtheme["forces"],
                            }
                        )
                    for force in subtheme["forces"]:
                        sector_data[sector]["force_counts"][force["title"]] += 1

    companies_by_sector = defaultdict(list)
    for company in companies:
        sector_mix = company.get("sector_mix") or []
        top_sector = sector_mix[0]["sector"] if sector_mix else None
        if top_sector in sector_data:
            companies_by_sector[top_sector].append(company)

    for sector, record in sector_data.items():
        record["example_industries"] = top_industries_for_sector(briefs, sector)
        sector_companies = sorted(
            companies_by_sector.get(sector, []),
            key=lambda row: (-row.get("mention_count", 0), -row.get("rating_score", 0), row.get("title", "")),
        )
        record["advantaged"] = [c for c in sector_companies if c.get("status") == "advantaged"][:6]
        record["mixed"] = [c for c in sector_companies if c.get("status") == "mixed"][:6]
        record["exposed"] = [c for c in sector_companies if c.get("status") == "exposed"][:6]
        record["dominant_themes"] = [name for name, _ in record["theme_counts"].most_common(4)]
        record["dominant_forces"] = [name for name, _ in record["force_counts"].most_common(4)]
        ordered_theme_slugs = [
            slug for slug, theme_obj in record["theme_objects"].items()
            if theme_obj["title"] in record["dominant_themes"]
        ]
        record["dominant_theme_objects"] = sorted(
            [record["theme_objects"][slug] for slug in ordered_theme_slugs],
            key=lambda row: record["dominant_themes"].index(row["title"]) if row["title"] in record["dominant_themes"] else 99,
        )[:3]
        record["theme_tensions"] = []
        record["theme_signals"] = []
        for theme_obj in record["dominant_theme_objects"]:
            for item in theme_obj["structural_tensions"][:2]:
                if item not in record["theme_tensions"]:
                    record["theme_tensions"].append(item)
            for item in theme_obj["signals_to_watch"][:2]:
                if item not in record["theme_signals"]:
                    record["theme_signals"].append(item)
        record["subtheme_map"] = record["subtheme_records"][:6]
        record["sector_thesis"] = build_sector_thesis(sector, record)
        record["diligence_questions"] = build_diligence_questions(sector, record)
        record["advantaged_setups"] = build_advantaged_setups(sector, record)
        record["exposed_setups"] = build_exposed_setups(sector, record)
        record["sector_takeaway"] = ""
        prose = sector_prose.get(record["slug"])
        if prose:
            if prose.get("outlook"):
                record["sector_thesis"] = prose["outlook"]
            if prose.get("takeaway"):
                record["sector_takeaway"] = prose["takeaway"]
            if prose.get("advantaged"):
                record["advantaged_setups"] = prose["advantaged"]
            if prose.get("exposed"):
                record["exposed_setups"] = prose["exposed"]
            if prose.get("diligence"):
                record["diligence_questions"] = prose["diligence"]

    return list(sector_data.values())


def build_sector_thesis(sector: str, record: dict) -> str:
    themes = ", ".join(record["dominant_themes"][:3]) or "cross-cutting pressures"
    if sector == "Retail":
        return f"Retail in 2025-2026 is governed by {themes}: value, convenience, and channel control are separating winners from the undifferentiated middle."
    if sector == "Healthcare":
        return f"Healthcare is being reorganized by {themes}: demand remains durable, but labor, reimbursement, and administrative fluency determine who captures economics."
    if sector == "Finance & Insurance":
        return f"Finance & Insurance is increasingly shaped by {themes}: rails, trust infrastructure, and scaled workflow systems look stronger than thin-spread intermediaries."
    if sector == "Technology & Digital":
        return f"Technology & Digital is being split by {themes}: workflow ownership, AI infrastructure, and embedded necessity matter more than generic software exposure."
    if sector == "Manufacturing":
        return f"Manufacturing is increasingly defined by {themes}: specified capability, input access, and position inside industrial bottlenecks matter more than broad cyclical optimism."
    if sector == "Real Estate":
        return f"Real Estate is being repriced by {themes}: commodity office is weaker while logistics, utility-linked land, and adaptive reuse gain importance."
    return f"{sector} in 2025-2026 is being reorganized by {themes}, with the economics increasingly determined by who can absorb complexity and sit on the right side of sector bottlenecks."


def build_diligence_questions(sector: str, record: dict) -> list[str]:
    base = [
        f"Which of the dominant themes in {sector} are structural rather than cyclical?",
        "Where does margin actually get lost: labor, procurement, compliance, capital, or channel access?",
        "Does the operator own a bottleneck, or is it merely exposed to one?",
    ]
    if sector in {"Healthcare", "Finance & Insurance"}:
        base.append("How much of the economics are governed by reimbursement, regulation, fraud control, or trust infrastructure?")
    elif sector in {"Retail", "Consumer Services", "Food & Drink"}:
        base.append("Is the business aligned with value, premium, convenience, health, or experience, and is that positioning actually legible to customers?")
    elif sector in {"Construction", "Manufacturing", "Energy & Environment", "Transport & Logistics", "Real Estate"}:
        base.append("Which physical constraint matters most here: labor, land, power, materials, utilization, or permitting?")
    else:
        base.append("What lets this operator keep relevance as automation, software, and consolidation spread through the sector?")
    return base[:4]


def build_advantaged_setups(sector: str, record: dict) -> list[str]:
    theme_text = record["dominant_themes"][:2]
    setups = [
        f"Businesses positioned on the right side of {theme_text[0] if theme_text else 'the main sector pressure'}.",
        "Operators with real system leverage: scale, workflow, procurement, or distribution control.",
        "Formats with visible differentiation rather than generic middle positioning.",
    ]
    if sector in {"Technology & Digital", "Finance & Insurance", "Business Services"}:
        setups.append("Embedded workflow and trust infrastructure with recurring necessity.")
    elif sector in {"Construction", "Manufacturing", "Energy & Environment", "Transport & Logistics"}:
        setups.append("Bottleneck providers attached to buildout, throughput, or infrastructure scarcity.")
    elif sector in {"Healthcare", "Consumer Services", "Food & Drink"}:
        setups.append("Demand systems with strong retention, coordination, or habit loops.")
    return setups[:4]


def build_exposed_setups(sector: str, record: dict) -> list[str]:
    setups = [
        "Undifferentiated middle-market operators without pricing power.",
        "Businesses carrying rising complexity without enough scale or workflow leverage.",
        "Models exposed to secular behavior change but still priced as if old demand patterns hold.",
    ]
    if sector in {"Retail", "Food & Drink", "Consumer Services", "Media & Entertainment"}:
        setups.append("Formats that depend on generic traffic without strong identity, habit, or community.")
    elif sector in {"Finance & Insurance", "Business Services", "Technology & Digital"}:
        setups.append("Middlemen and service layers that can be compressed by software or platform control.")
    else:
        setups.append("Asset- or labor-heavy operators exposed to input volatility without pass-through rights.")
    return setups[:4]


def company_chip(company: dict, prefix: str = "") -> str:
    href = f"{prefix}company-pages/{company['slug']}.html"
    path = ROOT / "company-pages" / f"{company['slug']}.html"
    if path.exists():
        return f'<a class="chip" href="{e(href)}">{e(company["title"])}</a>'
    return f'<span class="chip">{e(company["title"])}</span>'


def status_class(status: str) -> str:
    return "adv" if status == "advantaged" else "exp" if status == "exposed" else "mix"


def brief_card(brief: dict) -> str:
    return f"""<article class="brief">
  <div class="meta">{e(brief.get('sector'))}</div>
  <h3>{e(brief.get('title'))}</h3>
  <p>{e(brief.get('one_sentence') or brief.get('one_liner'))}</p>
</article>"""


def render_subtheme_application(subtheme: dict, prefix: str = "", seen: set | None = None) -> str:
    seen = seen if seen is not None else set()

    def dd(items: list, limit: int) -> str:
        out = []
        for item in items:
            if item in seen:
                continue
            seen.add(item)
            out.append(item)
            if len(out) >= limit:
                break
        return "".join(f"<li>{e(x)}</li>" for x in out)

    force_chips = "".join(
        f'<a class="chip" href="{e(prefix)}forces/{e(force["slug"])}/index.html">{e(force["title"])}</a>'
        for force in subtheme["forces"][:3]
    )
    pressure = dd(subtheme["pressure_points"], 2)
    signals = dd(subtheme["signals_to_watch"], 2)
    consequences = dd(subtheme["strategic_consequences"], 2)
    return f"""<article class="subcard">
  <div class="meta">{e(subtheme['theme_title'])}</div>
  <h4><a href="{e(prefix)}themes/{e(subtheme['theme_slug'])}.html#{e(subtheme['slug'])}">{e(subtheme['title'])}</a></h4>
  <p>{e(subtheme['deep_read'])}</p>
  <div class="chips">{force_chips}</div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Pressure points</div>
    <ul class="list">{pressure}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Signals and consequences</div>
    <ul class="list">{signals}{consequences}</ul>
  </div>
</article>"""


def render_sector(record: dict, prefix: str = "") -> str:
    themes = "".join(f'<span class="chip">{e(item)}</span>' for item in record["dominant_themes"])
    forces = "".join(f'<span class="chip">{e(item)}</span>' for item in record["dominant_forces"])
    questions = "".join(f"<li>{e(item)}</li>" for item in record["diligence_questions"])
    advantaged = "".join(f"<li>{e(item)}</li>" for item in record["advantaged_setups"])
    exposed = "".join(f"<li>{e(item)}</li>" for item in record["exposed_setups"])
    tensions = "".join(f"<li>{e(item)}</li>" for item in record["theme_tensions"][:4])
    signals = "".join(f"<li>{e(item)}</li>" for item in record["theme_signals"][:4])
    where_it_shows_up = "".join(
        f"<li>{e(item['title'])} <span class=\"meta\">{e(item.get('sector', ''))}</span></li>"
        for item in record["example_industries"][:4]
    )
    second_order_effects = "".join(
        f"<li>{e(item['title'])}: {e((item.get('strategic_consequences') or [''])[0])}</li>"
        for item in record["subtheme_map"][:4]
    )
    industry_cards = "".join(brief_card(item) for item in record["example_industries"][:4])
    _seen: set = set(record["theme_tensions"][:4]) | set(record["theme_signals"][:4])
    subtheme_cards = "".join(render_subtheme_application(item, prefix=prefix, seen=_seen) for item in record["subtheme_map"])

    def company_block(rows: list[dict], label: str, cls: str) -> str:
        chips = "".join(company_chip(row, prefix=prefix) for row in rows) or '<span class="chip">none surfaced</span>'
        return f"""<div class="mini">
  <h4>{e(label)}</h4>
  <div class="chips">{chips}</div>
</div>"""

    return f"""<section class="memo">
  <div class="meta">{e(record['sector'])} memo</div>
  <h3>{e(record['sector'])}</h3>
  <p><b>Operator angle:</b> {e(record['operator_angle'])}</p>
  <p><b>Investor angle:</b> {e(record['investor_angle'])}</p>
  <p>{e(record['sector_thesis'])}</p>
  <div class="chips">{themes}{forces}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">What to do</div>
      <ul class="list">{advantaged}</ul>
    </div>
    <div class="panel">
      <div class="meta">What to underwrite</div>
      <ul class="list">{questions}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Where it shows up</div>
      <ul class="list">{where_it_shows_up}</ul>
    </div>
    <div class="panel">
      <div class="meta">Representative industries</div>
      <div class="grid">{industry_cards}</div>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Tensions</div>
      <ul class="list">{tensions}</ul>
    </div>
    <div class="panel">
      <div class="meta">Signals</div>
      <ul class="list">{signals}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Second-order effects</div>
      <ul class="list">{second_order_effects}</ul>
    </div>
    <div class="panel">
      <div class="meta">Exposed setups</div>
      <ul class="list">{exposed}</ul>
    </div>
  </div>
  <div class="smallgrid">
    {company_block(record['advantaged'], 'Advantaged names', 'adv')}
    {company_block(record['mixed'], 'Contested middle', 'mix')}
    {company_block(record['exposed'], 'Exposed names', 'exp')}
  </div>
  <div class="panel" style="margin-top:14px">
    <div class="meta">Sector subtheme map</div>
    <div class="subcards">{subtheme_cards}</div>
  </div>
</section>"""


def build_hub(records: list[dict]) -> str:
    cards = "\n".join(
        f"""<article class="card">
  <div class="meta">{e(record['sector'])}</div>
  <h3><a href="sector-memos/{e(record['slug'])}.html">{e(record['sector'])}</a></h3>
  <p>{e(record['sector_thesis'])}</p>
  <div class="chips">{''.join(f'<span class="chip">{e(item)}</span>' for item in record['dominant_themes'][:3])}</div>
</article>"""
        for record in records
    )
    memos = "".join(render_sector(record) for record in records)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sector Memos — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="american-theme-memos.html">Theme memos</a><a href="sector-cases.html">Sector cases</a></div>
<div class="eyebrow">Sector memos · US · 2025-2026</div>
<h1>Sector Memos</h1>
<p class="sub">This is the sector application layer. It maps the major sectors to dominant themes, force pressures, representative industries, and surfaced advantaged versus exposed setups so the interpretation stack can be used by sector quickly.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(records)}</div><div class="l">Major sectors</div></div>
  <div class="kpi"><div class="n">{sum(record['industry_count'] for record in records)}</div><div class="l">Mapped industries</div></div>
  <div class="kpi"><div class="n">{sum(len(record['diligence_questions']) for record in records)}</div><div class="l">Diligence questions</div></div>
  <div class="kpi"><div class="n">{sum(len(record['theme_signals']) for record in records)}</div><div class="l">Signals surfaced</div></div>
</div>
<div class="lead"><p>Use this layer when the question is not just what a theme means, but what it means for an entire sector. The memos are designed to compress screening, diligence, and sector positioning into one read.</p></div>

<section class="section">
  <h2>Sector Index</h2>
  <div class="grid">{cards}</div>
</section>

<section class="section">
  <h2>Applied Read</h2>
  {memos}
</section>

</div></body></html>"""


def build_detail(record: dict) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(record['sector'])} Memo — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../sector-memos.html">Sector memos</a><a href="../american-theme-memos.html">Theme memos</a></div>
<div class="eyebrow">{e(record['sector'])} memo · US · 2025-2026</div>
<h1>{e(record['sector'])}</h1>
<p class="sub">{e(record['sector_thesis'])}</p>
<div class="kpis">
  <div class="kpi"><div class="n">{record['industry_count']}</div><div class="l">Industries</div></div>
  <div class="kpi"><div class="n">{len(record['diligence_questions'])}</div><div class="l">Diligence questions</div></div>
  <div class="kpi"><div class="n">{len(record['dominant_themes'])}</div><div class="l">Dominant themes</div></div>
  <div class="kpi"><div class="n">{len(record['subtheme_map'])}</div><div class="l">Mapped subthemes</div></div>
</div>
<div class="lead"><p>{e(record['operator_angle'])}</p></div>
<section class="section">
  {render_sector(record, prefix="../")}
</section>
</div></body></html>"""


def main() -> None:
    records = build_sector_records()
    records.sort(key=lambda item: item["sector"])
    PAGES_OUT.mkdir(exist_ok=True)

    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(build_hub(records))

    for record in records:
        with (PAGES_OUT / f"{record['slug']}.html").open("w", encoding="utf-8") as handle:
            handle.write(build_detail(record))

    print(f"wrote {OUT}")
    print(f"wrote sector memos to {PAGES_OUT}")
    print(f"sectors={len(records)}")


if __name__ == "__main__":
    main()
