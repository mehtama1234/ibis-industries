#!/usr/bin/env python3
"""Build applied company memos from the company intelligence layer."""

from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
COMPANIES_JSON = ROOT / "company_universe.json"
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
OUT_JSON = ROOT / "company_memos.json"
OUT_HTML = ROOT / "company-memos.html"
PAGES_OUT = ROOT / "company-memos"
PROSE_JSON = ROOT / "company_memos_prose.json"  # human-quality authored prose, keyed by slug


STATUS_LABELS = {
    "advantaged": "Advantaged",
    "mixed": "Contested Middle",
    "exposed": "Exposed",
}


SECTOR_ANGLES = {
    "Agriculture": "The real question is whether this company has protection from raw commodity exposure through processing, distribution, biology, or trade positioning.",
    "Business Services": "The test is whether the company sells repeatable workflow or specialized trust rather than just labor hours.",
    "Construction": "The key issue is whether the company sits beside an unavoidable bottleneck in labor, power, permitting, or specialized scope.",
    "Consumer Services": "The key issue is whether this business owns habit, convenience, or identity rather than generic discretionary demand.",
    "Energy & Environment": "The key issue is whether the company benefits from electrification, infrastructure scarcity, or compliance burden rather than just commodity prices.",
    "Finance & Insurance": "The key issue is whether the company owns rails, workflow, trust, or data instead of a shrinking undifferentiated spread.",
    "Food & Drink": "The key issue is whether the company is aligned with health, premium, convenience, or distribution power rather than legacy volume assumptions.",
    "Healthcare": "The key issue is whether the company can convert durable demand into economics despite reimbursement, staffing, and admin friction.",
    "Manufacturing": "The key issue is whether the company has specified capability and the right position inside physical bottlenecks.",
    "Media & Entertainment": "The key issue is whether the company owns scarcity, rights, or affiliation instead of generic attention supply.",
    "Real Estate": "The key issue is whether the asset base aligns with current flows of housing, logistics, and power rather than old utilization assumptions.",
    "Retail": "The key issue is whether the company owns value, premium, convenience, or channel control rather than being stranded in the middle.",
    "Technology & Digital": "The key issue is whether the company owns workflow, infrastructure, or trust layers that remain necessary as AI diffuses.",
    "Transport & Logistics": "The key issue is whether the company owns orchestration, density, or strategic throughput rather than exposed capacity alone.",
}


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--green:#78ca90;--red:#e07d6d;--amber:#d9a441;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1220px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.4rem,5vw,4.2rem);line-height:1;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel,.brief,.force{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3,.panel h3,.brief h3,.force h3{margin:.2em 0 .35em;font-size:1.12rem}.card p,.panel p,.brief p,.force p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.memo{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.memo:first-of-type{margin-top:0;padding-top:0;border-top:none}.memo h3{font-size:1.28rem;margin:.2em 0 .35em}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.smallgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-top:14px}.mini{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:12px}.mini h4{margin:0 0 .35em;font-size:.96rem}.mini p{margin:0;color:var(--muted);font-size:.9rem}.status{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:.68rem;border:1px solid var(--line);border-radius:999px;padding:4px 8px}.status.adv{color:var(--green)}.status.mix{color:var(--amber)}.status.exp{color:var(--red)}@media(max-width:920px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def status_class(status: str) -> str:
    return "adv" if status == "advantaged" else "exp" if status == "exposed" else "mix"


def top_sector(company: dict) -> str | None:
    sector_mix = company.get("sector_mix") or []
    return sector_mix[0]["sector"] if sector_mix else None


def build_theme_lookup(themes: list[dict]) -> tuple[dict[str, dict], dict[str, list[dict]]]:
    theme_lookup = {theme["slug"]: theme for theme in themes}
    force_to_themes: dict[str, list[dict]] = defaultdict(list)
    for theme in themes:
        for force in theme["forces"]:
            force_to_themes[force["slug"]].append(theme)
    return theme_lookup, force_to_themes


def classify_theme_lens(lens: str) -> list[str]:
    text = (lens or "").lower()
    buckets = []
    if "societal" in text or "social" in text or "institutional" in text or "labor" in text:
        buckets.append("societal")
    if "cultural" in text:
        buckets.append("cultural")
    if "consumer" in text:
        buckets.append("consumer")
    if "industrial" in text or "technological" in text:
        buckets.append("industrial")
    return buckets or ["industrial"]


def infer_related_themes(company: dict, force_to_themes: dict[str, list[dict]]) -> list[dict]:
    if company.get("dominant_theme_objects"):
        return [
            {
                "slug": item["slug"],
                "title": item["title"],
                "lens": item.get("lens", ""),
                "subthemes": item.get("subthemes", []),
                "score": item.get("score", 0),
            }
            for item in company["dominant_theme_objects"][:5]
        ]
    counts = Counter()
    theme_records: dict[str, dict] = {}
    for force in company.get("dominant_forces", []):
        for theme in force_to_themes.get(force["slug"], []):
            counts[theme["slug"]] += 1
            theme_records[theme["slug"]] = theme
    ordered = [theme_records[slug] for slug, _ in counts.most_common(4)]
    return ordered


def build_lens_cards(related_themes: list[dict]) -> list[dict]:
    bucket_map: dict[str, dict] = {
        "societal": {"key": "societal", "label": "Societal", "themes": [], "theme_titles": [], "subthemes": []},
        "cultural": {"key": "cultural", "label": "Cultural", "themes": [], "theme_titles": [], "subthemes": []},
        "consumer": {"key": "consumer", "label": "Consumer", "themes": [], "theme_titles": [], "subthemes": []},
        "industrial": {"key": "industrial", "label": "Industrial", "themes": [], "theme_titles": [], "subthemes": []},
    }
    for theme in related_themes:
        for bucket in classify_theme_lens(theme.get("lens", "")):
            bucket_map[bucket]["themes"].append(theme)
            bucket_map[bucket]["theme_titles"].append(theme["title"])
            for subtheme in theme.get("subthemes", [])[:3]:
                slug = subtheme.get("slug")
                if slug and not any(existing.get("slug") == slug for existing in bucket_map[bucket]["subthemes"]):
                    bucket_map[bucket]["subthemes"].append(subtheme)
    return [bucket_map[key] for key in ("societal", "cultural", "consumer", "industrial") if bucket_map[key]["themes"]]


def build_lens_summary(record: dict, bucket: str, theme_titles: list[str]) -> str:
    names = ", ".join(theme_titles[:3])
    title = record["title"]
    cluster = record["business_model_cluster_title"].lower()
    if bucket == "societal":
        return f"{title} should be read socially through {names}, where labor formation, institutional burden, demographic strain, and coordination complexity determine how {cluster} economics actually scale."
    if bucket == "cultural":
        return f"{title} also sits inside a cultural reclassification through {names}, where trust, legitimacy, identity, participation, and wellness norms reshape how the company is chosen and valued."
    if bucket == "consumer":
        return f"{title} faces sharper demand selection through {names}, where buyers are more explicit about value, convenience, health, service confidence, and permission to spend."
    return f"{title} is being repriced industrially through {names}, where bottlenecks, compliance, infrastructure, procurement, and system ownership increasingly govern the margin pool around {cluster} economics."


def build_record(company: dict, force_to_themes: dict[str, list[dict]]) -> dict:
    sector = top_sector(company) or "Unknown"
    related_themes = infer_related_themes(company, force_to_themes)
    lens_cards = build_lens_cards(related_themes)
    dominant_force_titles = [force["title"] for force in company.get("dominant_forces", [])[:3]]
    force_text = ", ".join(dominant_force_titles) or "cross-force exposure"
    primary_constraint = company.get("constraints", ["complexity"])[0]
    top_lens_labels = [lens["label"] for lens in lens_cards[:2]]
    top_theme_titles = [theme["title"] for theme in related_themes[:3]]
    top_subthemes = []
    for theme in related_themes:
        for subtheme in theme.get("subthemes", [])[:2]:
            title = subtheme.get("title")
            if title and title not in top_subthemes:
                top_subthemes.append(title)
    signal_items = [
        f"Dominant forces: {', '.join(force['title'] for force in company['dominant_forces'])}."
        if company.get("dominant_forces")
        else "Dominant forces are diffuse rather than concentrated in one obvious regime.",
        f"Primary constraints: {', '.join(company['constraints'][:3])}."
        if company.get("constraints")
        else "Primary constraints are spread across execution rather than one single bottleneck.",
        f"Linked theme pressure: {', '.join(top_theme_titles)}."
        if top_theme_titles
        else "Linked theme pressure remains mixed rather than concentrated in one explicit theme set.",
    ]
    action_items = [
        f"Operate around {primary_constraint} as the binding constraint, not a secondary cleanup item.",
        f"Use {company['business_model_cluster_title'].lower()} position to protect demand, workflow, or distribution before chasing adjacent expansion.",
        (
            f"Translate {', '.join(top_lens_labels).lower()} signals into pricing, service, and capital-allocation decisions now."
            if top_lens_labels
            else "Translate the current force mix into pricing, service, and capital-allocation decisions now."
        ),
    ]
    tension_items = [
        f"{company['title']} has to preserve {company['best_owner_type']} economics while still absorbing pressure from {primary_constraint}.",
        (
            f"The main structural tension is whether {company['title']} stays on the advantaged side of {', '.join(top_theme_titles[:2])} without drifting back toward a generic middle position."
            if top_theme_titles
            else f"The main structural tension is whether {company['title']} keeps a differentiated position or gets pulled back toward a generic middle."
        ),
        (
            f"If the read deteriorates, the business starts looking more like {', '.join(company['likely_losers'][:2])}."
            if company.get("likely_losers")
            else f"If the read deteriorates, the business starts losing the practical advantages that currently defend returns."
        ),
    ]
    second_order_items = [
        (
            f"If {', '.join(top_subthemes[:2])} keep intensifying, procurement, labor, pricing, and channel choices around {company['title']} will tighten further."
            if top_subthemes
            else f"If the linked themes keep intensifying, procurement, labor, pricing, and channel choices around {company['title']} will tighten further."
        ),
        (
            f"Because {company['title']} shows up across {sector} and {company['sector_mix'][1]['sector'] if len(company.get('sector_mix', [])) > 1 else sector}, shifts here can spill across multiple adjacent operating surfaces."
            if company.get("sector_mix")
            else f"Because {company['title']} touches multiple operating surfaces, shifts here can spill into adjacent categories faster than the headline sector suggests."
        ),
        f"Changes in {force_text.lower()} will likely alter capital intensity and competitive separation before they show up as simple revenue changes.",
    ]
    record = {
        "slug": company["slug"],
        "title": company["title"],
        "status": company["status"],
        "status_label": STATUS_LABELS.get(company["status"], company["status"].title()),
        "business_model_cluster_title": company["business_model_cluster_title"],
        "business_truth": company["business_truth"],
        "top_sector": sector,
        "sector_angle": SECTOR_ANGLES.get(sector, "The key issue is whether the company sits on the right side of the sector's governing constraints."),
        "mention_count": company["mention_count"],
        "industry_count": company["industry_count"],
        "best_owner_type": company["best_owner_type"],
        "constraints": company["constraints"],
        "top_themes": company.get("top_themes", [])[:6],
        "dominant_forces": company.get("dominant_forces", [])[:3],
        "related_themes": related_themes,
        "theme_tailwind_score": company.get("theme_tailwind_score", 0),
        "theme_scorecard": company.get("theme_scorecard", {}),
        "lens_cards": [
            {
                **lens,
                "summary": build_lens_summary(
                    {
                        "title": company["title"],
                        "business_model_cluster_title": company["business_model_cluster_title"],
                    },
                    lens["key"],
                    lens["theme_titles"],
                ),
            }
            for lens in lens_cards
        ],
        "linked_industries": company.get("industry_rows", [])[:6],
        "sector_mix": company.get("sector_mix", [])[:4],
        "likely_losers": company.get("likely_losers", []),
        "operator_memo": (
            f"{company['title']} needs to keep converting {company['business_model_cluster_title'].lower()} position "
            f"into {company['best_owner_type']} economics while staying on the right side of {primary_constraint}."
        ),
        "investor_memo": (
            f"The current read depends on whether {company['title']} can keep its advantage inside {force_text.lower()} "
            f"rather than being dragged back toward the generic middle of its cluster."
        ),
        "signal_items": signal_items,
        "action_items": action_items,
        "tension_items": tension_items,
        "second_order_items": second_order_items,
        "diligence_questions": [
            f"What would make {company['title']} lose its current edge in {company['business_model_cluster_title'].lower()} markets?",
            f"Is {primary_constraint} a manageable operating issue here or the thing that caps returns?",
            f"Does the company still own demand, workflow, trust, or distribution where it matters most?",
            f"Are the dominant forces around {company['title']} structural enough to justify the current read?",
        ],
    }
    return record


def render_company_card(record: dict) -> str:
    chips = "".join(f'<span class="chip">{e(theme["title"])}</span>' for theme in record["related_themes"][:3])
    lens_chips = "".join(f'<span class="chip">{e(lens["label"])}</span>' for lens in record["lens_cards"][:4])
    prose = record.get("prose")
    snippet = prose["headline"] if prose else record["investor_memo"]
    return f"""<article class="card">
  <div class="meta">{e(record['top_sector'])}</div>
  <h3><a href="company-memos/{e(record['slug'])}.html">{e(record['title'])}</a></h3>
  <p>{e(snippet)}</p>
  <div class="chips">{chips}</div>
  <div class="chips">{lens_chips}</div>
</article>"""


def theme_chip(theme: dict, prefix: str = "") -> str:
    return f'<a class="chip" href="{e(prefix)}theme-briefs/{e(theme["slug"])}.html">{e(theme["title"])}</a>'


def force_chip(force: dict, prefix: str = "") -> str:
    return f'<a class="chip" href="{e(prefix)}forces/{e(force["slug"])}/index.html">{e(force["title"])}</a>'


def company_page_chip(record: dict, prefix: str = "") -> str:
    return f'<a class="chip" href="{e(prefix)}company-pages/{e(record["slug"])}.html">Company page</a>'


def sector_chip(record: dict, prefix: str = "") -> str:
    sector_slug = (
        record["top_sector"].lower()
        .replace("&", "and")
        .replace(" ", "-")
        .replace("/", "-")
    )
    return f'<a class="chip" href="{e(prefix)}sector-memos/{e(sector_slug)}.html">{e(record["top_sector"])} sector memo</a>'


def linked_industry_cards(record: dict) -> str:
    cards = []
    for industry in record["linked_industries"]:
        cards.append(
            f"""<article class="brief">
  <div class="meta">{e(industry.get('sector'))}</div>
  <h3>{e(industry.get('title'))}</h3>
  <p>{e(industry.get('one_sentence'))}</p>
</article>"""
        )
    return "".join(cards)


def render_lens_section(lens: dict, prefix: str = "") -> str:
    theme_chips = "".join(theme_chip(theme, prefix) for theme in lens["themes"][:4]) or '<span class="chip">no linked themes</span>'
    subtheme_chips = "".join(
        f'<a class="chip" href="{e(prefix)}themes/{e(theme["slug"])}.html#{e(subtheme["slug"])}">{e(subtheme["title"])}</a>'
        for theme in lens["themes"]
        for subtheme in theme.get("subthemes", [])[:2]
    )
    if not subtheme_chips:
        subtheme_chips = '<span class="chip">no surfaced subthemes</span>'
    return f"""<article class="panel">
  <div class="meta">{e(lens['label'])} lens</div>
  <h3>{e(lens['label'])} Read</h3>
  <p>{e(lens['summary'])}</p>
  <div class="chips">{theme_chips}</div>
  <div class="chips">{subtheme_chips}</div>
</article>"""


def render_memo(record: dict, prefix: str = "") -> str:
    prose = record.get("prose")
    if prose:
        p_theme_chips = "".join(theme_chip(theme, prefix) for theme in record["related_themes"])
        p_force_chips = "".join(force_chip(force, prefix) for force in record["dominant_forces"])
        p_constraints = "".join(f'<span class="chip">{e(item)}</span>' for item in record["constraints"])
        p_sector_mix = "".join(f"<li>{e(item['sector'])}: {item['count']} linked industries</li>" for item in record["sector_mix"])
        return f"""<section class="memo">
  <div class="meta">{e(record['top_sector'])} company memo</div>
  <h3>{e(record['title'])}</h3>
  <div class="status {status_class(record['status'])}">{e(record['status_label'])}</div>
  <div class="panel">
    <div class="meta">What's happening</div>
    <p>{e(prose['whats_happening'])}</p>
  </div>
  <div class="split">
    <div class="panel"><div class="meta">The investor question</div><p>{e(prose['investor_take'])}</p></div>
    <div class="panel"><div class="meta">The operator playbook</div><p>{e(prose['operator_take'])}</p></div>
  </div>
  <div class="panel">
    <div class="meta">The core tension</div>
    <p>{e(prose['the_tension'])}</p>
  </div>
  <div class="lead"><p><b>Bottom line:</b> {e(prose['bottom_line'])}</p></div>
  <div class="chips">{company_page_chip(record, prefix)}{sector_chip(record, prefix)}{p_theme_chips}{p_force_chips}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">Business position</div>
      <p>{e(record['business_truth'])}</p>
      <div class="chips">{p_constraints}</div>
    </div>
    <div class="panel">
      <div class="meta">Where it shows up</div>
      <ul class="list">{p_sector_mix}</ul>
      <p><b>{record['mention_count']}</b> corpus mentions across <b>{record['industry_count']}</b> linked industries.</p>
    </div>
  </div>
  <div class="panel">
    <div class="meta">Linked industries</div>
    <div class="grid">{linked_industry_cards(record)}</div>
  </div>
</section>"""
    theme_chips = "".join(theme_chip(theme, prefix) for theme in record["related_themes"]) or '<span class="chip">no direct theme inference</span>'
    force_chips = "".join(force_chip(force, prefix) for force in record["dominant_forces"])
    top_theme_tags = "".join(f'<span class="chip">{e(item)}</span>' for item in record["top_themes"])
    constraints = "".join(f'<span class="chip">{e(item)}</span>' for item in record["constraints"])
    lens_chips = "".join(f'<span class="chip">{e(lens["label"])}</span>' for lens in record["lens_cards"])
    sector_mix = "".join(f"<li>{e(item['sector'])}: {item['count']} linked industries</li>" for item in record["sector_mix"])
    likely_losers = "".join(f"<li>{e(item)}</li>" for item in record["likely_losers"]) or "<li>No explicit loser set surfaced</li>"
    diligence = "".join(f"<li>{e(item)}</li>" for item in record["diligence_questions"])
    signal_items = "".join(f"<li>{e(item)}</li>" for item in record["signal_items"])
    action_items = "".join(f"<li>{e(item)}</li>" for item in record["action_items"])
    tension_items = "".join(f"<li>{e(item)}</li>" for item in record["tension_items"])
    second_order_items = "".join(f"<li>{e(item)}</li>" for item in record["second_order_items"])
    theme_scorecard = "".join(
        f'<span class="chip">{e(slug.replace("-", " "))}: {score}</span>'
        for slug, score in sorted(record["theme_scorecard"].items(), key=lambda item: (-abs(item[1]), item[0]))[:5]
    ) or '<span class="chip">no explicit theme scorecard</span>'
    lens_sections = "".join(render_lens_section(lens, prefix=prefix) for lens in record["lens_cards"])
    return f"""<section class="memo">
  <div class="meta">{e(record['top_sector'])} company memo</div>
  <h3>{e(record['title'])}</h3>
  <div class="status {status_class(record['status'])}">{e(record['status_label'])}</div>
  <p><b>Investor memo:</b> {e(record['investor_memo'])}</p>
  <p><b>Operator memo:</b> {e(record['operator_memo'])}</p>
  <p>{e(record['sector_angle'])}</p>
  <div class="chips">{company_page_chip(record, prefix)}{sector_chip(record, prefix)}{theme_chips}{force_chips}</div>
  <div class="chips">{lens_chips}<span class="chip">theme tailwind {record['theme_tailwind_score']}</span></div>
  <div class="split">
    <div class="panel">
      <div class="meta">Business position</div>
      <p>{e(record['business_truth'])}</p>
      <div class="chips">{constraints}{top_theme_tags}</div>
    </div>
    <div class="panel">
      <div class="meta">Where it shows up</div>
      <ul class="list">{sector_mix}</ul>
      <p><b>{record['mention_count']}</b> corpus mentions across <b>{record['industry_count']}</b> linked industries.</p>
    </div>
  </div>
  <div class="panel">
    <div class="meta">Theme scorecard</div>
    <div class="chips">{theme_scorecard}</div>
  </div>
  <div class="panel">
    <div class="meta">Signals</div>
    <ul class="list">{signal_items}</ul>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">What to do</div>
      <ul class="list">{action_items}</ul>
    </div>
    <div class="panel">
      <div class="meta">Tensions</div>
      <ul class="list">{tension_items}</ul>
    </div>
  </div>
  <div class="grid">
    {lens_sections}
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">What to underwrite</div>
      <ul class="list">{diligence}</ul>
    </div>
    <div class="panel">
      <div class="meta">If the read breaks</div>
      <ul class="list">{likely_losers}</ul>
    </div>
  </div>
  <div class="panel">
    <div class="meta">Second-order effects</div>
    <ul class="list">{second_order_items}</ul>
  </div>
  <div class="panel">
    <div class="meta">Linked industries</div>
    <div class="grid">{linked_industry_cards(record)}</div>
  </div>
</section>"""


def build_hub(records: list[dict]) -> str:
    cards = "\n".join(render_company_card(record) for record in records[:120])
    sections = "".join(render_memo(record) for record in records[:40])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company Memos — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="company-scoreboard.html">Company scoreboard</a><a href="sector-memos.html">Sector memos</a></div>
<div class="eyebrow">Company memos · US · 2025-2026</div>
<h1>Company Memos</h1>
<p class="sub">This is the company application layer. It takes the surfaced company universe and translates each important company into a memo tied back to sector logic, dominant themes, force exposure, and the current structural read.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(records)}</div><div class="l">Company memos</div></div>
  <div class="kpi"><div class="n">{sum(1 for record in records if record['status'] == 'advantaged')}</div><div class="l">Advantaged</div></div>
  <div class="kpi"><div class="n">{sum(1 for record in records if record['status'] == 'exposed')}</div><div class="l">Exposed</div></div>
  <div class="kpi"><div class="n">{sum(len(record['lens_cards']) for record in records)}</div><div class="l">Lens reads</div></div>
</div>
<div class="lead"><p>Use this layer when the question is not what a company is, but what its current structural position means. The memo format makes the read explicit: why the name screens well or poorly, what governs the economics, and what would break the thesis.</p></div>

<section class="section">
  <h2>Memo Index</h2>
  <div class="grid">{cards}</div>
</section>

<section class="section">
  <h2>Applied Read</h2>
  {sections}
</section>

</div></body></html>"""


def build_detail(record: dict) -> str:
    prose = record.get("prose")
    sub = prose["headline"] if prose else record["business_truth"]
    lead_html = "" if prose else f'<div class="lead"><p>{e(record["investor_memo"])}</p></div>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(record['title'])} Memo — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../company-memos.html">Company memos</a><a href="../company-scoreboard.html">Company scoreboard</a></div>
<div class="eyebrow">Company memo · US · 2025-2026</div>
<h1>{e(record['title'])}</h1>
<p class="sub">{e(sub)}</p>
<div class="kpis">
  <div class="kpi"><div class="n">{record['mention_count']}</div><div class="l">Mentions</div></div>
  <div class="kpi"><div class="n">{record['industry_count']}</div><div class="l">Industries</div></div>
  <div class="kpi"><div class="n">{len(record['related_themes'])}</div><div class="l">Related themes</div></div>
  <div class="kpi"><div class="n">{len(record['lens_cards'])}</div><div class="l">Lens reads</div></div>
</div>
{lead_html}
<section class="section">
  {render_memo(record, prefix="../")}
</section>
</div></body></html>"""


def main() -> None:
    companies = load_json(COMPANIES_JSON)
    themes = load_json(THEMES_JSON)["themes"]
    _, force_to_themes = build_theme_lookup(themes)
    records = [build_record(company, force_to_themes) for company in companies if company.get("page")]
    records.sort(key=lambda row: (-row["mention_count"], row["title"]))

    prose_map = load_json(PROSE_JSON) if PROSE_JSON.exists() else {}
    matched = 0
    for record in records:
        record["prose"] = prose_map.get(record["slug"])
        if record["prose"]:
            matched += 1
            # Also overwrite the legacy templated snippet fields so downstream
            # readers (capstones, hubs) inherit the authored prose, not templates.
            prose = record["prose"]
            if prose.get("headline"):
                record["investor_memo"] = prose["headline"]
            if prose.get("operator_take"):
                record["operator_memo"] = prose["operator_take"]
    print(f"authored prose matched for {matched}/{len(records)} memos")

    PAGES_OUT.mkdir(exist_ok=True)

    with OUT_JSON.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)
    with OUT_HTML.open("w", encoding="utf-8") as handle:
        handle.write(build_hub(records))
    for record in records:
        with (PAGES_OUT / f"{record['slug']}.html").open("w", encoding="utf-8") as handle:
            handle.write(build_detail(record))

    print(f"wrote {OUT_JSON}")
    print(f"wrote {OUT_HTML}")
    print(f"wrote company memos to {PAGES_OUT}")
    print(f"memos={len(records)}")


if __name__ == "__main__":
    main()
