#!/usr/bin/env python3
"""Rebuild company scoreboard and comparison pages with richer theme-aware decision surfaces."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCOREBOARD_JSON = ROOT / "company_scoreboard.json"
COMPARISONS_JSON = ROOT / "company_comparisons.json"
UNIVERSE_JSON = ROOT / "company_universe.json"
CLUSTER_OUTLOOKS_JSON = ROOT / "company_cluster_outlooks.json"
SCOREBOARD_HTML = ROOT / "company-scoreboard.html"
COMPARISONS_HTML = ROOT / "company-comparisons.html"


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--green:#78ca90;--red:#e07d6d;--blue:#7cb0ea;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1220px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.45rem,5vw,4.2rem);line-height:1;margin:.18em 0 .22em;max-width:13ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:940px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel,.bucket,.mini{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3,.panel h3,.bucket h3,.mini h4{margin:.2em 0 .35em;font-size:1.12rem}.card p,.panel p,.bucket p,.mini p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted);margin:.35em 0 0}.list li{margin:.42em 0}.small{font-size:.9rem;color:var(--muted)}.bucket{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.bucket:first-of-type{margin-top:0;padding-top:0;border-top:none}.stack>*+*{margin-top:14px}.badge{font-family:var(--mono);font-size:.66rem;border-radius:999px;padding:3px 8px;display:inline-block;margin-top:7px;border:1px solid var(--line)}.adv{color:var(--green)}.mix{color:var(--muted)}.exp{color:var(--red)}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def company_badge(status: str) -> str:
    cls = "mix"
    if status == "advantaged":
        cls = "adv"
    elif status == "exposed":
        cls = "exp"
    return f'<span class="badge {cls}">{e(status)}</span>'


def company_link(company: dict) -> str:
    href = f"company-pages/{company['slug']}.html"
    if (ROOT / "company-pages" / f"{company['slug']}.html").exists():
        return f'<a href="{e(href)}">{e(company["title"])}</a>'
    return e(company["title"])


def render_force_chips(company: dict) -> str:
    return "".join(f'<span class="chip">{e(force["title"])}</span>' for force in company.get("dominant_forces", [])[:4])


def render_theme_chips(company: dict) -> str:
    return "".join(f'<span class="chip">{e(item)}</span>' for item in company.get("top_themes", [])[:5])


def render_constraint_chips(company: dict) -> str:
    return "".join(f'<span class="chip">{e(item)}</span>' for item in company.get("constraints", [])[:4])


def render_sector_chips(company: dict) -> str:
    return "".join(f'<span class="chip">{e(item["sector"])}</span>' for item in company.get("sector_mix", [])[:4])


def render_sector_lines(company: dict) -> str:
    items = [
        f"{item['sector']}: {item['count']} linked industries"
        for item in company.get("sector_mix", [])[:4]
    ] or ["No sector concentration surfaced yet."]
    return "".join(f"<li>{e(item)}</li>" for item in items)


def render_signal_lines(company: dict) -> str:
    items = [force["title"] for force in company.get("dominant_forces", [])[:3]]
    items += [f"Primary constraints: {', '.join(company.get('constraints', [])[:3])}."]
    return "".join(f"<li>{e(item)}</li>" for item in items if item)


def render_underwrite_lines(company: dict) -> str:
    items = [
        f"Can {company['title']} keep converting {company.get('business_model_cluster_title', '').lower()} position into {company.get('best_owner_type', 'advantaged owner')} economics?",
        f"Do {', '.join(company.get('constraints', [])[:3])} remain manageable rather than thesis-breaking constraints?",
    ]
    if company.get("likely_losers"):
        items.append(f"If the read breaks, it likely starts looking more like {company['likely_losers'][0]}.")
    return "".join(f"<li>{e(item)}</li>" for item in items if item)


def render_company_card(company: dict, cluster_outlook: dict | None) -> str:
    lens_chips = ""
    cluster_themes = ""
    if cluster_outlook:
        lens_chips = "".join(f'<span class="chip">{e(lens["label"])}</span>' for lens in cluster_outlook.get("lens_cards", [])[:4])
        cluster_themes = "".join(f'<span class="chip">{e(theme["title"])}</span>' for theme in cluster_outlook.get("dominant_theme_objects", [])[:4])
    return f"""<article class="card">
  <div class="meta">{e(company['business_model_cluster_title'])}</div>
  <h3>{company_link(company)}</h3>
  <p>{e(company.get('business_truth', ''))}</p>
  {company_badge(company['status'])}
  <div class="chips"><span class="chip">score {company['rating_score']}</span><span class="chip">{company['mention_count']} mentions</span><span class="chip">{company['industry_count']} industries</span></div>
  <div class="chips">{render_force_chips(company)}</div>
  <div class="chips">{render_theme_chips(company)}</div>
  <div class="chips">{render_constraint_chips(company)}</div>
  <div class="meta" style="margin-top:14px">Where it shows up</div>
  <div class="chips">{render_sector_chips(company)}</div>
  <ul class="list">{render_sector_lines(company)}</ul>
  <div class="meta" style="margin-top:14px">Signals</div>
  <ul class="list">{render_signal_lines(company)}</ul>
  <div class="chips">{lens_chips}</div>
  <div class="chips">{cluster_themes}</div>
  <div class="meta" style="margin-top:14px">What to do</div>
  <p>{e(company.get('why_owner_type', ''))}</p>
  <div class="meta" style="margin-top:14px">What to underwrite</div>
  <ul class="list">{render_underwrite_lines(company)}</ul>
</article>"""


def enrich_comparison_records(comparisons: list[dict], universe: dict[str, dict], cluster_outlooks: dict[str, dict]) -> list[dict]:
    title_to_slug = {record["title"]: slug for slug, record in cluster_outlooks.items()}
    enriched = []
    for record in comparisons:
        cluster_slug = title_to_slug.get(record["cluster_title"])
        outlook = cluster_outlooks.get(cluster_slug, {})
        top_forces = outlook.get("top_forces", [])
        dominant_sectors = outlook.get("dominant_sectors", [])
        dominant_constraints = outlook.get("dominant_constraints", [])
        recurring_theme_terms = outlook.get("recurring_theme_terms", [])
        lenses = [lens["label"] for lens in outlook.get("lens_cards", [])]
        themed = {
            **record,
            "cluster_slug": cluster_slug,
            "cluster_thesis": outlook.get("thesis", ""),
            "operator_angle": outlook.get("operator_angle", ""),
            "investor_angle": outlook.get("investor_angle", ""),
            "top_forces": top_forces,
            "dominant_sectors": dominant_sectors,
            "dominant_constraints": dominant_constraints,
            "recurring_theme_terms": recurring_theme_terms,
            "lenses": lenses,
            "dominant_themes": [theme["title"] for theme in outlook.get("dominant_theme_objects", [])[:5]],
        }
        for key in ("leaders", "advantaged", "exposed", "mixed"):
            themed[key] = [universe[item["slug"]] for item in record[key] if item["slug"] in universe]
        enriched.append(themed)
    return enriched


def build_scoreboard_page(scoreboard: dict, cluster_outlooks: dict[str, dict]) -> str:
    sections = []
    config = [
        ("advantaged", "Most Advantaged", "These names currently sit in the strongest structural positions implied by the corpus, force mix, and business-model logic."),
        ("exposed", "Most Exposed", "These names show the weakest structural setup in the current model: wrong-side force exposure, thinner bargaining power, or more fragile economics."),
        ("mixed", "The Big Middle", "These names still matter, but the current read is contested rather than cleanly advantaged or cleanly broken."),
    ]
    for key, title, body in config:
        cards = []
        for company in scoreboard[key][:20]:
            outlook = cluster_outlooks.get(company.get("business_model_cluster_slug"))
            cards.append(render_company_card(company, outlook))
        sections.append(
            f"""<section class="section">
  <h2>{e(title)}</h2>
  <p class="sub">{e(body)}</p>
  <div class="lead"><p>{e('Use this section to separate structural fit from simple brand familiarity. The names here matter because they sit in, or outside, the right bottlenecks, channels, and owner types for the current regime.')}</p></div>
  <div class="grid">{''.join(cards)}</div>
</section>"""
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company Scoreboard — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="company-universe.html">Company universe</a><a href="company-cluster-outlooks.html">Cluster outlooks</a><a href="company-comparisons.html">Company comparisons</a></div>
<div class="eyebrow">Company scoreboard · US · 2025-2026</div>
<h1>Company Scoreboard</h1>
<p class="sub">This is the explicit judgment layer. It turns the recurring named-company surface into a decision read: who looks structurally advantaged, who looks exposed, and who still sits in the large contested middle once force exposure, cluster logic, and theme pressure are read together.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(scoreboard['advantaged'])}</div><div class="l">Advantaged names</div></div>
  <div class="kpi"><div class="n">{len(scoreboard['exposed'])}</div><div class="l">Exposed names</div></div>
  <div class="kpi"><div class="n">{len(scoreboard['mixed'])}</div><div class="l">Mixed names</div></div>
  <div class="kpi"><div class="n">{sum(item['mention_count'] for group in scoreboard.values() for item in group[:20])}</div><div class="l">Mentions surfaced</div></div>
</div>
<div class="lead"><p>Read this page as a decision surface, not a leaderboard. A high score only matters if the company sits inside the right business model, the right bottleneck, and the right part of the broader societal, cultural, consumer, and industrial story.</p></div>
{''.join(sections)}
</div></body></html>"""


def build_bucket(section_title: str, items: list[dict], cluster_outlook: dict | None) -> str:
    if not items:
        return f"""<div class="panel"><div class="meta">{e(section_title)}</div><p class="small">No names surfaced yet.</p></div>"""
    cards = "".join(render_company_card(item, cluster_outlook) for item in items)
    return f"""<div class="panel">
  <div class="meta">{e(section_title)}</div>
  <div class="grid">{cards}</div>
</div>"""


def build_comparisons_page(comparisons: list[dict], cluster_outlooks: dict[str, dict]) -> str:
    sections = []
    for section in comparisons:
        cluster_outlook = cluster_outlooks.get(section["cluster_slug"]) if section.get("cluster_slug") else None
        lens_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in section["lenses"][:4])
        force_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in section["top_forces"][:5])
        sector_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in section["dominant_sectors"][:5])
        constraint_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in section["dominant_constraints"][:5])
        theme_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in section["dominant_themes"][:5])
        term_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in section["recurring_theme_terms"][:6])
        sections.append(
            f"""<article class="bucket">
  <div class="meta">{section['company_count']} companies</div>
  <h3>{e(section['cluster_title'])}</h3>
  <p>{e(section.get('cluster_thesis') or 'This comparison groups the recurrent names inside one operating cluster and separates the apparent leaders, pressures, and contested middle.')}</p>
  <div class="meta" style="margin-top:14px">Signals</div>
  <div class="chips">{lens_chips}{force_chips}{constraint_chips}</div>
  <div class="meta" style="margin-top:14px">Where it shows up</div>
  <div class="chips">{sector_chips}</div>
  <div class="meta" style="margin-top:14px">Recurring themes</div>
  <div class="chips">{constraint_chips}</div>
  <div class="chips">{theme_chips}</div>
  <div class="chips">{term_chips}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">What to do</div>
      <p>{e(section.get('operator_angle', ''))}</p>
    </div>
    <div class="panel">
      <div class="meta">What to underwrite</div>
      <p>{e(section.get('investor_angle', ''))}</p>
    </div>
  </div>
  <div class="stack" style="margin-top:14px">
    {build_bucket("Largest names", section["leaders"], cluster_outlook)}
    {build_bucket("Advantaged", section["advantaged"], cluster_outlook)}
    {build_bucket("Exposed", section["exposed"], cluster_outlook)}
    {build_bucket("Mixed", section["mixed"], cluster_outlook)}
  </div>
</article>"""
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company Comparisons — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="company-universe.html">Company universe</a><a href="company-cluster-outlooks.html">Cluster outlooks</a><a href="company-scoreboard.html">Company scoreboard</a></div>
<div class="eyebrow">Company comparisons · US · 2025-2026</div>
<h1>Company Comparisons</h1>
<p class="sub">This is the cluster-by-cluster company decision layer. It keeps the biggest recurrent names together, but now reads them through cluster economics, theme exposure, lens pressure, and the current advantaged / exposed / contested split.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(comparisons)}</div><div class="l">Compared clusters</div></div>
  <div class="kpi"><div class="n">{sum(section['company_count'] for section in comparisons)}</div><div class="l">Companies covered</div></div>
  <div class="kpi"><div class="n">{sum(len(section['lenses']) for section in comparisons)}</div><div class="l">Lens reads</div></div>
</div>
<div class="lead"><p>The point is not just to list companies inside a business model. It is to show which names are sitting in the right structural lane for the next 2025-2026 regime, and which names are still fighting the wrong demand, channel, labor, compliance, or infrastructure setup.</p></div>
<section class="section"><div class="stack">{''.join(sections)}</div></section>
</div></body></html>"""


def main() -> None:
    scoreboard = load_json(SCOREBOARD_JSON)
    comparisons = load_json(COMPARISONS_JSON)
    universe_rows = load_json(UNIVERSE_JSON)
    cluster_outlooks_rows = load_json(CLUSTER_OUTLOOKS_JSON)["records"]
    universe = {row["slug"]: row for row in universe_rows}
    cluster_outlooks = {row["slug"]: row for row in cluster_outlooks_rows}
    enriched_comparisons = enrich_comparison_records(comparisons, universe, cluster_outlooks)

    with SCOREBOARD_HTML.open("w", encoding="utf-8") as handle:
        handle.write(build_scoreboard_page(scoreboard, cluster_outlooks))
    with COMPARISONS_HTML.open("w", encoding="utf-8") as handle:
        handle.write(build_comparisons_page(enriched_comparisons, cluster_outlooks))

    print(f"wrote {SCOREBOARD_HTML}")
    print(f"wrote {COMPARISONS_HTML}")
    print(f"comparisons={len(enriched_comparisons)}")


if __name__ == "__main__":
    main()
