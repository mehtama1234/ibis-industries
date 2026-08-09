#!/usr/bin/env python3
"""Build ranked theme and bottleneck surfaces for the US synthesis layer."""

from __future__ import annotations

import html
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
COMPANY_MEMOS_JSON = ROOT / "company_memos.json"
OUT_JSON = ROOT / "american_rankings.json"
OUT_HTML = ROOT / "american-rankings.html"


BOTTLENECK_LIBRARY = {
    "barbelled-consumer-america": [
        ("Owned demand and low-friction distribution", "Households are punishing weak middle positioning and rewarding operators that already control traffic, basket economics, and convenience."),
        ("Private label and value architecture", "Margin defense increasingly depends on making the prudent option feel obvious rather than promotional."),
    ],
    "wellness-recodes-daily-life": [
        ("Health-aligned product mix", "Food, beverage, beauty, and adjacent categories need products that survive under wellness scrutiny."),
        ("Behavioral permission structures", "Consumers still buy indulgence, but categories now need sober-curious, functional, or self-improvement logic around the spend."),
    ],
    "experience-status-and-community": [
        ("Scarce venues and programmable experiences", "Pricing power now depends more on curation, social signaling, and repeatable memory creation than on generic capacity."),
        ("Affiliation loops", "Operators that create community and participation can hold demand better than broad goods categories."),
    ],
    "aging-care-and-the-assistance-economy": [
        ("Care coordination and reimbursement fluency", "Demand is real, but the margin pool sits with whoever can navigate staffing, coding, and care orchestration."),
        ("Home-first aging infrastructure", "The migration of care into homes and outpatient systems creates a recurring logistics and monitoring bottleneck."),
    ],
    "work-without-the-old-firm": [
        ("Portable admin and worker support layers", "The thinner firm creates demand for outsourced workflow, payroll, credential, and employability support."),
        ("Training linked to real wage outcomes", "Workers need shorter pathways to employability, and providers need credible links to job placement or earnings gain."),
    ],
    "physical-reindustrialization-and-infrastructure": [
        ("Power-ready industrial capacity", "Power, transmission, cooling, and utility access are re-emerging as industrial selectors."),
        ("Specified domestic capability", "Categories with procurement sensitivity or security logic are rewarding producers with domestic or nearshore reliability."),
    ],
    "scale-financialization-and-the-owned-economy": [
        ("Asset control over visible operation", "The owner of the land, rail, catalog, or centralized platform is often capturing more value than the frontline operator."),
        ("Roll-up system quality", "Acquisition discipline, shared services, and financing advantages are concentrating fragmented categories."),
    ],
    "regulated-software-and-admin-state": [
        ("Mandatory workflow software", "Compliance, identity, reimbursement, and trust infrastructure keep becoming harder to avoid and easier to monetize."),
        ("Verification and fraud control", "Institutions need more proof, which creates durable demand for scoring, monitoring, and auditability."),
    ],
    "space-housing-and-local-friction": [
        ("Utility-linked land and logistics corridors", "The right geography is no longer neutral; the scarce site next to the unavoidable flow gets the rent."),
        ("Adaptive reuse and housing lock-in solutions", "Mobility friction and obsolete commercial space are reshaping local economics."),
    ],
    "machine-intelligence-and-compute-buildout": [
        ("Power, cooling, and data-center land", "AI demand reprices the physical stack beneath compute before it broadens the software upside."),
        ("Workflow embedding rather than frontier ownership", "Many winners will come from integrating AI into regulated or routine workflows rather than building the frontier model."),
    ],
}


EXPOSED_MODEL_LIBRARY = {
    "barbelled-consumer-america": [
        "Generic mid-market retail and brand stacks without clear value or premium permission",
        "Promotion-dependent formats that rent traffic but do not own demand",
    ],
    "wellness-recodes-daily-life": [
        "Vice-heavy consumer categories assuming old indulgence habits return unchanged",
        "Health-branded products with weak functional credibility",
    ],
    "experience-status-and-community": [
        "Undifferentiated leisure capacity without social meaning or venue scarcity",
        "Transactional retail formats that cannot turn visits into discovery or affiliation",
    ],
    "aging-care-and-the-assistance-economy": [
        "Labor-heavy care operators without coordination or reimbursement advantage",
        "Demand-rich senior categories that treat demographic growth as sufficient economics",
    ],
    "work-without-the-old-firm": [
        "Entry-level pathways reliant on patient internal training by employers",
        "Service businesses selling bespoke labor instead of modular capability",
    ],
    "physical-reindustrialization-and-infrastructure": [
        "Manufacturers exposed to politicized inputs without pricing or specification power",
        "Buildout stories that lack access to power, labor, or disciplined procurement",
    ],
    "scale-financialization-and-the-owned-economy": [
        "Regional intermediaries trapped between scaled owners and embedded software",
        "Local operators that sit inside someone else's system economics",
    ],
    "regulated-software-and-admin-state": [
        "Manual compliance and admin service shops with weak productization",
        "Trust-sensitive workflows without verification or fraud defenses",
    ],
    "space-housing-and-local-friction": [
        "Commodity office exposure tied to old weekday-density assumptions",
        "Location-sensitive models that depend on easy household mobility",
    ],
    "machine-intelligence-and-compute-buildout": [
        "Knowledge-work models assuming AI changes cost structure but not competitive intensity",
        "Application stories that ignore the physical constraints under compute growth",
    ],
}


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--green:#78ca90;--red:#e07d6d;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1240px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.5rem,5vw,4.2rem);line-height:.98;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:940px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3{margin:.2em 0 .35em;font-size:1.1rem}.card p{margin:.35em 0 0;color:var(--muted)}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.table{display:grid;gap:10px;margin-top:14px}.row{display:grid;grid-template-columns:72px 1.1fr .9fr;gap:12px;align-items:start;background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:14px}.score{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:10px 8px;text-align:center}.score .n{font-family:var(--mono);font-size:1.2rem;font-weight:700}.score .l{font-size:.62rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}@media(max-width:880px){.row{grid-template-columns:1fr}}
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


def simplify_signal(text: str) -> str:
    text = (text or "").strip()
    prefixes = [
        "A practical timing marker is whether ",
    ]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):]
    return text[:1].upper() + text[1:] if text else text


def simplify_tension(text: str) -> str:
    text = (text or "").strip()
    replacements = [
        ("The central tension inside ", ""),
        ("A second tension sits between household or institutional demand and the operating constraints surfaced by ", "Another tension is "),
        (", but the route to capturing that demand runs through the practical frictions surfaced by ", ". The friction point is "),
    ]
    for old, new in replacements:
        text = text.replace(old, new)
    return text


def load_theme_lookup() -> dict[str, dict]:
    data = json.loads(THEMES_JSON.read_text())
    return {theme["slug"]: theme for theme in data["themes"]}


def load_company_lookup() -> dict[str, dict]:
    data = json.loads(COMPANY_MEMOS_JSON.read_text())
    return {company["slug"]: company for company in data}


def score_theme(theme: dict) -> dict:
    sectors = {industry.get("sector") for sub in theme["subthemes"] for industry in sub.get("industries", []) if industry.get("sector")}
    companies = {company.get("slug") for sub in theme["subthemes"] for company in sub.get("companies", []) if company.get("slug")}
    force_count = len(theme.get("forces", []))
    crosscut_count = len(theme.get("crosscuts", []))
    score = (
        len(sectors) * 4
        + len(companies) * 2
        + len(theme.get("signals_to_watch", [])) * 3
        + len(theme.get("structural_tensions", [])) * 2
        + len(theme.get("second_order_effects", [])) * 2
        + len(theme.get("subthemes", [])) * 3
        + force_count * 2
        + crosscut_count
    )
    return {
        "slug": theme["slug"],
        "title": theme["title"],
        "lens": theme["lens"],
        "score": score,
        "sector_breadth": len(sectors),
        "company_breadth": len(companies),
        "force_count": force_count,
        "crosscut_count": crosscut_count,
        "thesis": theme["thesis"],
        "signals": dedupe([simplify_signal(item) for item in theme.get("signals_to_watch", [])], 3),
        "tensions": dedupe([simplify_tension(item) for item in theme.get("structural_tensions", [])], 2),
    }


def score_subtheme(theme: dict, subtheme: dict) -> dict:
    sectors = {industry.get("sector") for industry in subtheme.get("industries", []) if industry.get("sector")}
    companies = {company.get("slug") for company in subtheme.get("companies", []) if company.get("slug")}
    score = (
        len(sectors) * 4
        + len(companies) * 3
        + len(subtheme.get("signals_to_watch", [])) * 2
        + len(subtheme.get("pressure_points", []))
        + len(subtheme.get("timing_markers", []))
    )
    return {
        "theme_slug": theme["slug"],
        "theme_title": theme["title"],
        "slug": subtheme["slug"],
        "title": subtheme["title"],
        "score": score,
        "summary": subtheme.get("summary", ""),
        "deep_read": subtheme.get("deep_read", ""),
        "sector_breadth": len(sectors),
        "company_breadth": len(companies),
        "signals": dedupe([simplify_signal(item) for item in subtheme.get("signals_to_watch", [])], 2),
        "consequences": subtheme.get("strategic_consequences", [])[:2],
    }


def build_rankings(theme_lookup: dict[str, dict], company_lookup: dict[str, dict]) -> dict:
    theme_rows = sorted((score_theme(theme) for theme in theme_lookup.values()), key=lambda row: (-row["score"], row["title"]))
    subtheme_rows = []
    for theme in theme_lookup.values():
        for subtheme in theme["subthemes"]:
            subtheme_rows.append(score_subtheme(theme, subtheme))
    subtheme_rows.sort(key=lambda row: (-row["score"], row["title"]))

    bottlenecks = []
    for row in theme_rows:
        for rank_title, rationale in BOTTLENECK_LIBRARY.get(row["slug"], []):
            bottlenecks.append({
                "theme_slug": row["slug"],
                "theme_title": row["title"],
                "title": rank_title,
                "score": row["score"],
                "rationale": rationale,
            })
    bottlenecks.sort(key=lambda row: (-row["score"], row["title"]))

    exposed_models = []
    for row in theme_rows:
        for title in EXPOSED_MODEL_LIBRARY.get(row["slug"], []):
            exposed_models.append({
                "theme_slug": row["slug"],
                "theme_title": row["title"],
                "title": title,
                "score": row["score"],
            })
    exposed_models.sort(key=lambda row: (-row["score"], row["title"]))

    representative_companies = []
    for row in theme_rows[:6]:
        theme = theme_lookup[row["slug"]]
        names = []
        for subtheme in theme["subthemes"][:3]:
            for company in subtheme.get("companies", []):
                slug = company.get("slug")
                if slug and slug in company_lookup:
                    names.append(company_lookup[slug]["title"])
        representative_companies.append({
            "theme_slug": row["slug"],
            "theme_title": row["title"],
            "companies": dedupe(names, 6),
        })

    return {
        "metadata": {
            "generated_at": "2026-08-09",
            "theme_count": len(theme_rows),
            "subtheme_count": len(subtheme_rows),
            "bottleneck_count": len(bottlenecks),
            "exposed_model_count": len(exposed_models),
        },
        "top_themes": theme_rows,
        "top_subthemes": subtheme_rows,
        "top_bottlenecks": bottlenecks,
        "top_exposed_models": exposed_models,
        "representative_companies": representative_companies,
    }


def render_ranked_rows(rows: list[dict], body_fn) -> str:
    return "".join(
        f"""<article class="row">
  <div class="score"><div class="n">{row['score']}</div><div class="l">score</div></div>
  <div>{body_fn(row)[0]}</div>
  <div>{body_fn(row)[1]}</div>
</article>"""
        for row in rows
    )


def breadth_label(count: int) -> str:
    if count >= 15:
        return "very broad"
    if count >= 8:
        return "broad"
    if count >= 4:
        return "moderately broad"
    return "narrower"


def main() -> None:
    theme_lookup = load_theme_lookup()
    company_lookup = load_company_lookup()
    rankings = build_rankings(theme_lookup, company_lookup)
    OUT_JSON.write_text(json.dumps(rankings, indent=2) + "\n", encoding="utf-8")

    top_themes = rankings["top_themes"][:10]
    top_subthemes = rankings["top_subthemes"][:15]
    top_bottlenecks = rankings["top_bottlenecks"][:12]
    top_exposed = rankings["top_exposed_models"][:12]

    def theme_body(row):
        left = (
            f'<div class="meta">{e(row["lens"])}</div>'
            f'<h3>{e(row["title"])}</h3>'
            f'<p>{e(row["thesis"])}</p>'
            f'<div class="chips">' + "".join(f'<span class="chip">{e(item)}</span>' for item in row["signals"]) + '</div>'
        )
        right = (
            f'<p><b>Why it ranks high:</b> This theme shows up across a {breadth_label(row["sector_breadth"])} set of sectors '
            f'({row["sector_breadth"]}) and companies ({row["company_breadth"]}), with {row["force_count"]} major forces and '
            f'{row["crosscut_count"]} cross-cutting links inside the taxonomy.</p>'
            f'<p><b>Main tensions:</b> {e(" | ".join(row["tensions"]))}</p>'
        )
        return left, right

    def subtheme_body(row):
        left = (
            f'<div class="meta">{e(row["theme_title"])}</div>'
            f'<h3>{e(row["title"])}</h3>'
            f'<p>{e(row["summary"])}</p>'
        )
        right = (
            f'<p><b>Why it ranks high:</b> It already appears across {row["sector_breadth"]} sectors and {row["company_breadth"]} companies in the source set.</p>'
            f'<p><b>What to watch:</b> {e(" | ".join(row["signals"]))}</p>'
            f'<p><b>What it means:</b> {e(" | ".join(row["consequences"]))}</p>'
        )
        return left, right

    def bottleneck_body(row):
        left = (
            f'<div class="meta">{e(row["theme_title"])}</div>'
            f'<h3>{e(row["title"])}</h3>'
            f'<p>{e(row["rationale"])}</p>'
        )
        right = f'<p><b>Theme anchor:</b> {e(row["theme_title"])}</p>'
        return left, right

    def exposed_body(row):
        left = (
            f'<div class="meta">{e(row["theme_title"])}</div>'
            f'<h3>{e(row["title"])}</h3>'
            f'<p>{e("This model is structurally exposed if the theme keeps intensifying.")}</p>'
        )
        right = f'<p><b>Why it is exposed:</b> This business model gets harder to defend if {e(row["theme_title"])} keeps strengthening.</p>'
        return left, right

    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>American Rankings — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="american-outlook-2025-2026.html">American outlook</a><a href="american-economy-2025-2026.html">Capstone</a><a href="american-synthesis-playbook.html">Playbook</a><a href="american-theme-memos.html">Theme memos</a></div>
<div class="eyebrow">Ranked synthesis · US · 2025-2026</div>
<h1>American Rankings</h1>
<p class="sub">A priority map for the current US economy: which themes, subthemes, bottlenecks, and exposed business models matter most right now.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(rankings['top_themes'])}</div><div class="l">Themes ranked</div></div>
  <div class="kpi"><div class="n">{len(rankings['top_subthemes'])}</div><div class="l">Subthemes ranked</div></div>
  <div class="kpi"><div class="n">{len(rankings['top_bottlenecks'])}</div><div class="l">Bottlenecks</div></div>
  <div class="kpi"><div class="n">{len(rankings['top_exposed_models'])}</div><div class="l">Exposed models</div></div>
</div>
<div class="lead"><p>Read this as a ranking tool, not a claim of mathematical precision. The scores help sort for breadth, recurrence, sector spread, company evidence, and practical decision value inside the 2025-2026 synthesis stack.</p></div>

<section class="section"><h2>Top Themes</h2><div class="table">{render_ranked_rows(top_themes, theme_body)}</div></section>
<section class="section"><h2>Top Subthemes</h2><div class="table">{render_ranked_rows(top_subthemes, subtheme_body)}</div></section>
<section class="section"><h2>Top Bottlenecks</h2><div class="table">{render_ranked_rows(top_bottlenecks, bottleneck_body)}</div></section>
<section class="section"><h2>Most Exposed Business Models</h2><div class="table">{render_ranked_rows(top_exposed, exposed_body)}</div></section>
</div></body></html>"""

    OUT_HTML.write_text(html_doc, encoding="utf-8")
    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_HTML}")


if __name__ == "__main__":
    main()
