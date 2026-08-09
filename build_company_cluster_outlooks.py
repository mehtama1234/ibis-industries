#!/usr/bin/env python3
"""Build company-cluster outlooks through societal, cultural, consumer, and industrial lenses."""

from __future__ import annotations

import html
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CLUSTERS_JSON = ROOT / "company_clusters.json"
COMPANIES_JSON = ROOT / "company_universe.json"
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
JSON_OUT = ROOT / "company_cluster_outlooks.json"
OUT = ROOT / "company-cluster-outlooks.html"
PAGES_OUT = ROOT / "company-cluster-outlooks"


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--green:#78ca90;--red:#e07d6d;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1220px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.45rem,5vw,4.2rem);line-height:1;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel,.lens,.entity{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3,.panel h3,.lens h3,.entity h4{margin:.2em 0 .35em;font-size:1.12rem}.card p,.panel p,.lens p,.entity p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.outlook{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.outlook:first-of-type{margin-top:0;padding-top:0;border-top:none}.badge{font-family:var(--mono);font-size:.66rem;border-radius:999px;padding:3px 8px;display:inline-block;margin-top:7px;border:1px solid var(--line)}.adv{color:var(--green)}.mix{color:var(--muted)}.exp{color:var(--red)}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


LENS_BUCKETS = {
    "societal": "Societal",
    "cultural": "Cultural",
    "consumer": "Consumer",
    "industrial": "Industrial",
}


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def classify_theme_lens(lens: str) -> list[str]:
    text = (lens or "").lower()
    buckets = []
    if "societal" in text or "social" in text or "institutional" in text:
        buckets.append("societal")
    if "cultural" in text:
        buckets.append("cultural")
    if "consumer" in text:
        buckets.append("consumer")
    if "industrial" in text or "technological" in text:
        buckets.append("industrial")
    return buckets or ["industrial"]


def load_clusters() -> list[dict]:
    with CLUSTERS_JSON.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_companies() -> list[dict]:
    with COMPANIES_JSON.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_themes() -> list[dict]:
    with THEMES_JSON.open(encoding="utf-8") as handle:
        return json.load(handle)["themes"]


def build_force_theme_map(theme_records: list[dict]) -> dict[str, list[dict]]:
    mapping: dict[str, list[dict]] = defaultdict(list)
    for theme in theme_records:
        for force in theme.get("forces", []):
            mapping[force["slug"]].append(theme)
    return mapping


def dedupe_themes(themes: list[dict]) -> list[dict]:
    out = []
    seen = set()
    for theme in themes:
        if theme["slug"] in seen:
            continue
        seen.add(theme["slug"])
        out.append(theme)
    return out


def build_cluster_company_map(companies: list[dict]) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for company in companies:
        grouped[company.get("business_model_cluster_slug") or "unassigned"].append(company)
    return grouped


def collect_relevant_themes(members: list[dict], force_theme_map: dict[str, list[dict]]) -> list[dict]:
    candidate_themes = []
    force_counts: Counter[str] = Counter()
    theme_term_counts: Counter[str] = Counter()
    sector_counts: Counter[str] = Counter()
    for member in members:
        for force in member.get("dominant_forces", []):
            force_counts[force["slug"]] += 1
            candidate_themes.extend(force_theme_map.get(force["slug"], []))
        for theme_term in member.get("top_themes", []):
            term = theme_term.strip().lower()
            if term:
                theme_term_counts[term] += 1
        for row in member.get("sector_mix", []):
            sector = row.get("sector", "").strip().lower()
            if sector:
                sector_counts[sector] += int(row.get("count", 1) or 1)

    themes = dedupe_themes(candidate_themes)
    scored = []
    for theme in themes:
        overlap = sum(force_counts.get(force["slug"], 0) for force in theme.get("forces", []))
        subtheme_hits = 0
        sector_hits = 0
        for subtheme in theme.get("subthemes", []):
            title = subtheme.get("title", "").lower()
            microthemes = [item.lower() for item in subtheme.get("microthemes", [])]
            for term, count in theme_term_counts.items():
                if term and (term in title or any(term in micro for micro in microthemes)):
                    subtheme_hits += count
            for industry in subtheme.get("industries", []):
                sector = industry.get("sector", "").lower()
                if sector:
                    sector_hits += sector_counts.get(sector, 0)
        scored.append((overlap, subtheme_hits, sector_hits, theme.get("signal_count", 0), theme))
    scored.sort(key=lambda item: (item[0], item[1], item[2], item[3]), reverse=True)
    return [item[4] for item in scored[:6]]


def build_lens_summary(record: dict, bucket: str, themes: list[dict]) -> str:
    theme_names = ", ".join(theme["title"] for theme in themes[:3])
    title = record["title"]
    if bucket == "societal":
        return f"{title} is being shaped socially by {theme_names}, where labor formation, institutional burden, demographic strain, and coordination complexity change which operators can actually scale."
    if bucket == "cultural":
        return f"{title} also sits inside a cultural reclassification through {theme_names}, where trust, identity, participation, legitimacy, and wellness norms affect how demand shows up and how the cluster gets valued."
    if bucket == "consumer":
        return f"{title} faces sharper demand selection through {theme_names}, where buyers are more explicit about value, convenience, health, service confidence, and permission to spend."
    return f"{title} is being repriced industrially through {theme_names}, where bottlenecks, compliance, infrastructure, procurement, system ownership, and scale economics increasingly govern the margin pool."


def build_lens_cards(record: dict, themes: list[dict]) -> list[dict]:
    bucket_map: dict[str, dict] = {}
    for key, label in LENS_BUCKETS.items():
        bucket_map[key] = {
            "key": key,
            "label": label,
            "themes": [],
            "theme_titles": [],
            "tensions": [],
            "signals": [],
            "subthemes": [],
        }

    for theme in themes:
        for bucket in classify_theme_lens(theme.get("lens", "")):
            bucket_map[bucket]["themes"].append(theme)
            bucket_map[bucket]["theme_titles"].append(theme["title"])
            for item in theme.get("structural_tensions", [])[:3]:
                if item not in bucket_map[bucket]["tensions"]:
                    bucket_map[bucket]["tensions"].append(item)
            for item in theme.get("signals_to_watch", [])[:3]:
                if item not in bucket_map[bucket]["signals"]:
                    bucket_map[bucket]["signals"].append(item)
            for subtheme in theme.get("subthemes", [])[:3]:
                if not any(existing["slug"] == subtheme["slug"] for existing in bucket_map[bucket]["subthemes"]):
                    bucket_map[bucket]["subthemes"].append(
                        {
                            "slug": subtheme["slug"],
                            "title": subtheme["title"],
                            "theme_slug": theme["slug"],
                            "theme_title": theme["title"],
                        }
                    )

    cards = []
    for key in ("societal", "cultural", "consumer", "industrial"):
        bucket = bucket_map[key]
        if not bucket["themes"]:
            continue
        bucket["summary"] = build_lens_summary(record, key, bucket["themes"])
        cards.append(bucket)
    return cards


def company_badge(status: str) -> str:
    cls = "mix"
    if status == "advantaged":
        cls = "adv"
    elif status == "exposed":
        cls = "exp"
    return f'<span class="badge {cls}">{e(status)}</span>'


def build_outlook_records() -> list[dict]:
    cluster_rows = {row["slug"]: row for row in load_clusters()}
    companies = load_companies()
    themes = load_themes()
    force_theme_map = build_force_theme_map(themes)
    grouped = build_cluster_company_map(companies)
    records = []

    for slug, members in grouped.items():
        cluster = cluster_rows.get(slug, {})
        force_counts: Counter[str] = Counter()
        force_lookup: dict[str, str] = {}
        sector_counts: Counter[str] = Counter()
        constraint_counts: Counter[str] = Counter()
        top_theme_counts: Counter[str] = Counter()
        industry_rows = []
        industry_seen = set()
        for member in members:
            for force in member.get("dominant_forces", []):
                force_counts[force["title"]] += 1
                force_lookup[force["slug"]] = force["title"]
            for row in member.get("sector_mix", []):
                sector = row.get("sector", "").strip()
                if sector:
                    sector_counts[sector] += int(row.get("count", 1) or 1)
            for item in member.get("constraints", []):
                if item:
                    constraint_counts[item] += 1
            for item in member.get("top_themes", [])[:4]:
                if item:
                    top_theme_counts[item] += 1
            for row in member.get("industry_rows", [])[:3]:
                if row.get("slug") and row["slug"] not in industry_seen:
                    industry_seen.add(row["slug"])
                    industry_rows.append(row)

        relevant_themes = collect_relevant_themes(members, force_theme_map)
        status_counts = Counter(member.get("status", "mixed") for member in members)
        top_companies = [
            {
                "slug": member["slug"],
                "title": member["title"],
                "status": member["status"],
                "mention_count": member["mention_count"],
                "industry_count": member["industry_count"],
            }
            for member in sorted(members, key=lambda row: (-row["mention_count"], -row["industry_count"], row["title"]))[:12]
        ]
        dominant_sectors = [sector for sector, _count in sector_counts.most_common(5)]
        dominant_constraints = [item for item, _count in constraint_counts.most_common(6)]
        recurring_themes = [item for item, _count in top_theme_counts.most_common(6)]
        lens_cards = build_lens_cards(
            {
                "slug": slug,
                "title": cluster.get("title", slug.replace("-", " ").title()),
            },
            relevant_themes,
        )
        record = {
            "slug": slug,
            "title": cluster.get("title", slug.replace("-", " ").title()),
            "thesis": cluster.get("thesis", "This cluster groups operators with a shared economic model and force exposure."),
            "best_owner_type": cluster.get("best_owner_type", "mixed / case-specific"),
            "company_count": len(members),
            "advantaged_count": status_counts["advantaged"],
            "mixed_count": status_counts["mixed"],
            "exposed_count": status_counts["exposed"],
            "top_forces": [title for title, _count in force_counts.most_common(5)],
            "dominant_sectors": dominant_sectors,
            "dominant_constraints": dominant_constraints,
            "recurring_theme_terms": recurring_themes,
            "top_companies": top_companies,
            "evidence_industries": industry_rows[:8],
            "dominant_theme_objects": relevant_themes,
            "lens_cards": lens_cards,
            "lens_count": len(lens_cards),
            "outlook_thesis": (
                f"{cluster.get('title', slug.replace('-', ' ').title())} should be read less as a grab-bag of famous companies and more as a repeatable operating system whose economics now depend on how societal, cultural, consumer, and industrial pressures stack together."
            ),
            "operator_angle": (
                f"The operating question inside {cluster.get('title', slug.replace('-', ' ').title()).lower()} is which constraint actually governs the spread pool: demand capture, staffing, compliance, procurement, capital intensity, utilization, reimbursement, or infrastructure access."
            ),
            "investor_angle": (
                f"The investor question is which version of {cluster.get('title', slug.replace('-', ' ').title()).lower()} owns the bottleneck, routinizes the complexity, and keeps the new behavior legible enough to hold pricing, throughput, or renewal power."
            ),
        }
        records.append(record)

    records.sort(key=lambda item: (-item["company_count"], item["title"]))
    return records


def render_subtheme_chip(prefix: str, subtheme: dict) -> str:
    return f'<a class="chip" href="{e(prefix)}themes/{e(subtheme["theme_slug"])}.html#{e(subtheme["slug"])}">{e(subtheme["title"])}</a>'


def render_company_chip(company: dict, prefix: str = "") -> str:
    href = f"{prefix}company-pages/{company['slug']}.html"
    if (ROOT / "company-pages" / f"{company['slug']}.html").exists():
        return f'<a class="chip" href="{e(href)}">{e(company["title"])}</a>'
    return f'<span class="chip">{e(company["title"])}</span>'


def render_lens(lens: dict, prefix: str = "") -> str:
    theme_chips = "".join(f'<span class="chip">{e(title)}</span>' for title in lens["theme_titles"][:4])
    tensions = "".join(f"<li>{e(item)}</li>" for item in lens["tensions"][:3])
    signals = "".join(f"<li>{e(item)}</li>" for item in lens["signals"][:3])
    subthemes = "".join(render_subtheme_chip(prefix, item) for item in lens["subthemes"][:6]) or '<span class="chip">no surfaced subthemes</span>'
    return f"""<article class="lens">
  <div class="meta">{e(lens['label'])} lens</div>
  <h3>{e(lens['label'])} Read</h3>
  <p>{e(lens['summary'])}</p>
  <div class="chips">{theme_chips}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">Core tensions</div>
      <ul class="list">{tensions}</ul>
    </div>
    <div class="panel">
      <div class="meta">Signals</div>
      <ul class="list">{signals}</ul>
    </div>
  </div>
  <div class="panel" style="margin-top:14px">
    <div class="meta">Linked subthemes</div>
    <div class="chips">{subthemes}</div>
  </div>
</article>"""


def render_record(record: dict, prefix: str = "") -> str:
    lenses = "".join(render_lens(lens, prefix=prefix) for lens in record["lens_cards"])
    sector_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in record["dominant_sectors"][:5])
    constraint_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in record["dominant_constraints"][:6])
    theme_term_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in record["recurring_theme_terms"][:6])
    force_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in record["top_forces"][:5])
    company_cards = []
    for company in record["top_companies"][:8]:
        linked = render_company_chip(company, prefix=prefix)
        company_cards.append(
            f"""<div class="entity">
  <div class="meta">{company['mention_count']} mentions · {company['industry_count']} industries</div>
  <h4>{linked}</h4>
  {company_badge(company['status'])}
</div>"""
        )
    industries = "".join(
        f"<li><b>{e(item['title'])}</b> <span class=\"meta\">{e(item.get('sector', ''))}</span><br>{e(item.get('one_sentence', ''))}</li>"
        for item in record["evidence_industries"][:6]
    )
    return f"""<section class="outlook">
  <div class="meta">Company cluster outlook</div>
  <h3>{e(record['title'])}</h3>
  <p>{e(record['outlook_thesis'])}</p>
  <div class="chips"><span class="chip">{e(record['best_owner_type'])}</span><span class="chip">{record['company_count']} companies</span></div>
  <div class="chips">{force_chips}</div>
  <div class="chips">{sector_chips}</div>
  <div class="chips">{constraint_chips}</div>
  <div class="chips">{theme_term_chips}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">Operator angle</div>
      <p>{e(record['operator_angle'])}</p>
    </div>
    <div class="panel">
      <div class="meta">Investor angle</div>
      <p>{e(record['investor_angle'])}</p>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Cluster thesis</div>
      <p>{e(record['thesis'])}</p>
    </div>
    <div class="panel">
      <div class="meta">Status mix</div>
      <div class="chips">
        <span class="chip">advantaged {record['advantaged_count']}</span>
        <span class="chip">mixed {record['mixed_count']}</span>
        <span class="chip">exposed {record['exposed_count']}</span>
      </div>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Representative companies</div>
      <div class="grid">{''.join(company_cards)}</div>
    </div>
    <div class="panel">
      <div class="meta">Evidence industries</div>
      <ul class="list">{industries}</ul>
    </div>
  </div>
  <div class="grid" style="margin-top:14px">{lenses}</div>
</section>"""


def build_hub(records: list[dict]) -> str:
    cards = "\n".join(
        f"""<article class="card">
  <div class="meta">{e(record['best_owner_type'])}</div>
  <h3><a href="company-cluster-outlooks/{e(record['slug'])}.html">{e(record['title'])}</a></h3>
  <p>{e(record['outlook_thesis'])}</p>
  <div class="chips">{''.join(f'<span class="chip">{e(lens["label"])}</span>' for lens in record['lens_cards'])}</div>
</article>"""
        for record in records
    )
    sections = "".join(render_record(record) for record in records)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company Cluster Outlooks — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="company-clusters.html">Company clusters</a><a href="business-outlooks.html">Business outlooks</a></div>
<div class="eyebrow">Company cluster outlooks · US · 2025-2026</div>
<h1>Company Cluster Outlooks</h1>
<p class="sub">This layer re-reads the recurring company clusters through the same four top-level lenses used in the American outlook: societal, cultural, consumer, and industrial change.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(records)}</div><div class="l">Cluster outlooks</div></div>
  <div class="kpi"><div class="n">{sum(record['lens_count'] for record in records)}</div><div class="l">Lens reads</div></div>
  <div class="kpi"><div class="n">{sum(record['company_count'] for record in records)}</div><div class="l">Mapped companies</div></div>
  <div class="kpi"><div class="n">{sum(len(record['dominant_theme_objects']) for record in records)}</div><div class="l">Mapped themes</div></div>
</div>
<div class="lead"><p>The point here is to stop treating big company names as one-off trivia. This layer shows which broader societal, cultural, consumer, and industrial pressures are actually doing the work inside each recurring company archetype.</p></div>

<section class="section">
  <h2>Index</h2>
  <div class="grid">{cards}</div>
</section>

<section class="section">
  <h2>The Outlooks</h2>
  {sections}
</section>

</div></body></html>"""


def build_detail(record: dict) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(record['title'])} Outlook — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../company-cluster-outlooks.html">Cluster outlooks</a><a href="../company-clusters.html">Company clusters</a></div>
<div class="eyebrow">{e(record['title'])} outlook · US · 2025-2026</div>
<h1>{e(record['title'])}</h1>
<p class="sub">{e(record['outlook_thesis'])}</p>
<div class="kpis">
  <div class="kpi"><div class="n">{record['company_count']}</div><div class="l">Companies</div></div>
  <div class="kpi"><div class="n">{record['lens_count']}</div><div class="l">Lens reads</div></div>
  <div class="kpi"><div class="n">{len(record['dominant_theme_objects'])}</div><div class="l">Mapped themes</div></div>
  <div class="kpi"><div class="n">{len(record['evidence_industries'])}</div><div class="l">Evidence industries</div></div>
</div>
<div class="lead"><p>{e(record['operator_angle'])}</p></div>
<section class="section">
  {render_record(record, prefix="../")}
</section>
</div></body></html>"""


def main() -> None:
    records = build_outlook_records()
    out = {
        "metadata": {
            "generated_at": "2026-08-09",
            "cluster_count": len(records),
            "company_count": sum(record["company_count"] for record in records),
            "lens_count": sum(record["lens_count"] for record in records),
            "purpose": "Company-cluster outlooks mapped back to American themes, subthemes, and four-lens reads.",
        },
        "records": records,
    }
    PAGES_OUT.mkdir(exist_ok=True)
    with JSON_OUT.open("w", encoding="utf-8") as handle:
        json.dump(out, handle, ensure_ascii=False, indent=2)
    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(build_hub(records))
    for record in records:
        with (PAGES_OUT / f"{record['slug']}.html").open("w", encoding="utf-8") as handle:
            handle.write(build_detail(record))
    print(f"wrote {JSON_OUT}")
    print(f"wrote {OUT}")
    print(f"wrote cluster outlooks to {PAGES_OUT}")
    print(f"clusters={len(records)} companies={sum(record['company_count'] for record in records)}")


if __name__ == "__main__":
    main()
