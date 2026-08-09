#!/usr/bin/env python3
"""Build applied sector/company-style cases from business lenses."""

from __future__ import annotations

import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_OUT = os.path.join(ROOT, "sector_cases.json")
HTML_OUT = os.path.join(ROOT, "sector-cases.html")
PAGES_OUT = os.path.join(ROOT, "sector-cases")


def e(value):
    return html.escape(str(value or ""), quote=True)


BRIEFS = json.load(open(os.path.join(ROOT, "briefs_full.json"), encoding="utf-8"))
BRIEFS_BY_SLUG = {b["slug"]: b for b in BRIEFS}
LENSES = json.load(open(os.path.join(ROOT, "business_lenses.json"), encoding="utf-8"))
LENSES_BY_SLUG = {x["slug"]: x for x in LENSES}


CASE_CONFIG = [
    {
        "slug": "hair-and-nail-salons-case",
        "title": "Hair & Nail Salons as a Local Services Platform",
        "lens_slug": "local-services-platform",
        "industry_slug": "hair-and-nail-salons-in-the-us",
        "case_for": "A fragmented local-services category where labor, booking, pricing, and retention systems determine whether scale helps or just adds overhead.",
    },
    {
        "slug": "laboratory-casework-case",
        "title": "Laboratory Casework as a Specified Product Manufacturer",
        "lens_slug": "specified-product-manufacturer",
        "industry_slug": "laboratory-casework-manufacturing",
        "case_for": "A narrow industrial niche where specification status, lab-construction cycles, and import-sensitive inputs matter more than broad consumer demand.",
    },
    {
        "slug": "elderly-disabled-services-case",
        "title": "Elderly & Disabled Services as a Care Demand Platform",
        "lens_slug": "care-and-family-demand-platform",
        "industry_slug": "elderly-and-disabled-services-in-the-us",
        "case_for": "A demographically advantaged care category where staffing, reimbursement, and service coordination cap who can actually convert demand into returns.",
    },
    {
        "slug": "claims-software-case",
        "title": "Insurance Claims Processing Software as Regulated Workflow Infrastructure",
        "lens_slug": "regulated-workflow-infrastructure",
        "industry_slug": "insurance-claims-processing-software",
        "case_for": "A recurring software/admin layer where mandatory workflow, AI-assisted claims automation, and fraud/compliance pressure create durable infrastructure demand.",
    },
]


CSS = """
:root{--bg:#101318;--panel:#171d24;--panel2:#1d2630;--line:#2a3440;--ink:#f0eadc;--muted:#a9b2bd;--faint:#74808d;--gold:#d4ad55;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,40px) 72px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:34px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.2rem,5vw,4rem);line-height:1;margin:.18em 0 .22em}.sub{max-width:860px;color:var(--muted);font-size:1.07rem}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel,.brief{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.card h3,.panel h2,.brief h3{margin:.2em 0 .35em}.card p,.panel p,.brief p{color:var(--muted);margin:.35em 0 0}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.stats{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.stats span{font-family:var(--mono);font-size:.72rem;background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.split{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(280px,.85fr);gap:18px;margin-top:26px}.stack>*+*{margin-top:12px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.4em 0}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}@media(max-width:900px){.split{grid-template-columns:1fr}}footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);color:var(--faint);font-family:var(--mono);font-size:.72rem}
"""


def brief_card(brief: dict) -> str:
    themes = "".join(f'<span class="chip">{e(t)}</span>' for t in brief.get("themes", [])[:4])
    stats = "".join(
        f"<span>{e(brief.get('key_stats', {}).get(key) or 'n/a')}</span>"
        for key in ("market_size", "growth", "profit_margin")
    )
    return f"""<article class="brief">
  <div class="meta">{e(brief.get('sector'))}</div>
  <h3>{e(brief.get('title'))}</h3>
  <p>{e(brief.get('one_sentence') or brief.get('one_liner'))}</p>
  <div class="stats">{stats}</div>
  <div class="chips">{themes}</div>
</article>"""


def build_records():
    records = []
    for cfg in CASE_CONFIG:
        lens = LENSES_BY_SLUG[cfg["lens_slug"]]
        industry = BRIEFS_BY_SLUG[cfg["industry_slug"]]
        adjacent = [BRIEFS_BY_SLUG[s] for s in lens["adjacent_industry_slugs"] if s in BRIEFS_BY_SLUG]
        records.append(
            {
                "slug": cfg["slug"],
                "title": cfg["title"],
                "lens_slug": cfg["lens_slug"],
                "lens_title": lens["title"],
                "industry_slug": cfg["industry_slug"],
                "industry_title": industry["title"],
                "case_for": cfg["case_for"],
                "business_truth": lens["business_truth"],
                "one_sentence": industry.get("one_sentence") or industry.get("one_liner"),
                "sector": industry["sector"],
                "market_size": industry["key_stats"]["market_size"],
                "growth": industry["key_stats"]["growth"],
                "themes": industry.get("themes", [])[:6],
                "primary_forces": lens["primary_force_slugs"],
                "constraints": lens["binding_constraints"],
                "best_owner_type": lens["best_owner_type"],
                "why_owner_type": lens["why_this_owner_type"],
                "evidence_slugs": lens["evidence_industry_slugs"],
                "adjacent_slugs": lens["adjacent_industry_slugs"],
            }
        )
    return records


def build_page(record: dict) -> str:
    industry = BRIEFS_BY_SLUG[record["industry_slug"]]
    evidence = [BRIEFS_BY_SLUG[s] for s in record["evidence_slugs"] if s in BRIEFS_BY_SLUG][:6]
    adjacent = [BRIEFS_BY_SLUG[s] for s in record["adjacent_slugs"] if s in BRIEFS_BY_SLUG][:4]
    themes = "".join(f'<span class="chip">{e(t)}</span>' for t in record["themes"])
    constraints = "".join(f'<span class="chip">{e(c)}</span>' for c in record["constraints"])
    where_it_shows_up = "".join(
        f"<li>{e(item['title'])} <span class=\"meta\">{e(item.get('sector',''))}</span></li>"
        for item in evidence[:4]
    )
    signals = "".join(f"<li>{e(item)}</li>" for item in record["constraints"][:3])
    what_to_do = "".join(
        f"<li>{e('Design the operating model around ' + item + ' rather than treating it as a side constraint.')}</li>"
        for item in record["constraints"][:3]
    )
    what_to_underwrite = "".join(
        f"<li>{e('Underwrite whether ' + item + ' is manageable or thesis-breaking in this category.')}</li>"
        for item in record["constraints"][:3]
    )
    tensions = "".join(
        f"<li>{e('This case gets harder when ' + item + ' stops looking manageable and starts defining the economics.')}</li>"
        for item in record["constraints"][:3]
    )
    second_order = "".join(
        f"<li>{e(item['title'])}: {e(item.get('one_sentence') or item.get('one_liner'))}</li>"
        for item in adjacent[:3]
    )
    evidence_cards = "\n".join(brief_card(b) for b in evidence)
    adjacent_cards = "\n".join(brief_card(b) for b in adjacent)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(record['title'])} — Sector Case</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../business-lenses.html">Business lenses</a><a href="../force-operator-translations.html">Force-to-operator</a></div>
<div class="eyebrow">Applied sector case · US · 2025–2026</div>
<h1>{e(record['title'])}</h1>
<p class="sub">{e(record['case_for'])}</p>
<div class="split">
  <main class="stack">
    <div class="panel">
      <div class="meta">Representative industry</div>
      <h2>{e(record['industry_title'])}</h2>
      <p>{e(record['one_sentence'])}</p>
      <div class="stats"><span>{e(record['market_size'])}</span><span>{e(record['growth'])}</span></div>
      <div class="chips">{themes}</div>
    </div>
    <div class="panel">
      <div class="meta">Why this case matters</div>
      <h2>Business interpretation</h2>
      <p>{e(record['business_truth'])}</p>
      <p>{e(record['why_owner_type'])}</p>
      <div class="chips">{constraints}</div>
    </div>
    <div class="split">
      <div class="panel">
        <div class="meta">Where it shows up</div>
        <ul class="list">{where_it_shows_up}</ul>
      </div>
      <div class="panel">
        <div class="meta">Signals</div>
        <ul class="list">{signals}</ul>
      </div>
    </div>
    <div class="split">
      <div class="panel">
        <div class="meta">What to do</div>
        <ul class="list">{what_to_do}</ul>
      </div>
      <div class="panel">
        <div class="meta">What to underwrite</div>
        <ul class="list">{what_to_underwrite}</ul>
      </div>
    </div>
    <div class="split">
      <div class="panel">
        <div class="meta">Tensions</div>
        <ul class="list">{tensions}</ul>
      </div>
      <div class="panel">
        <div class="meta">Second-order effects</div>
        <ul class="list">{second_order}</ul>
      </div>
    </div>
    <div class="section">
      <h2>Evidence industries</h2>
      <div class="grid">{evidence_cards}</div>
    </div>
    <div class="section">
      <h2>Adjacent reads</h2>
      <div class="grid">{adjacent_cards}</div>
    </div>
  </main>
  <aside class="stack">
    <div class="panel">
      <div class="meta">Case summary</div>
      <h2>What governs the economics</h2>
      <p><b>Sector:</b> {e(record['sector'])}</p>
      <p><b>Best owner type:</b> {e(record['best_owner_type'])}</p>
      <p><b>Primary forces:</b> {e(', '.join(record['primary_forces']))}</p>
    </div>
  </aside>
</div>
<footer>Built from the detailed business lens layer and representative industries in the 1,491-industry corpus.</footer>
</div></body></html>"""


def build_hub(records: list[dict]) -> str:
    cards = "\n".join(
        f"""<article class="card">
  <div class="meta">{e(r['sector'])}</div>
  <h3><a href="sector-cases/{e(r['slug'])}.html">{e(r['title'])}</a></h3>
  <p>{e(r['case_for'])}</p>
  <div class="stats"><span>{e(r['industry_title'])}</span><span>{e(r['best_owner_type'])}</span></div>
  <div class="meta" style="margin-top:14px">Where it shows up</div>
  <div class="chips">{''.join(f'<span class="chip">{e(BRIEFS_BY_SLUG[s]["title"])}</span>' for s in r["evidence_slugs"][:2] if s in BRIEFS_BY_SLUG)}</div>
  <div class="meta" style="margin-top:14px">Signals</div>
  <div class="chips">{''.join(f'<span class="chip">{e(item)}</span>' for item in r["constraints"][:2])}</div>
  <div class="meta" style="margin-top:14px">What to do</div>
  <p>{e(r['why_owner_type'])}</p>
  <div class="meta" style="margin-top:14px">What to underwrite</div>
  <p>{e('Whether ' + ', '.join(r['constraints'][:2]) + ' is manageable or thesis-breaking.')}</p>
  <div class="meta" style="margin-top:14px">Tensions</div>
  <p>{e('This case gets harder when ' + ', '.join(r['constraints'][:2]) + ' stop looking operational and start determining the economics.')}</p>
  <div class="meta" style="margin-top:14px">Second-order effects</div>
  <p>{e('Adjacent industries start repricing around the same owner-type and constraint logic once this case becomes the template.')}</p>
</article>"""
        for r in records
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sector Cases — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="business-lenses.html">Business lenses</a><a href="force-operator-translations.html">Force-to-operator</a><a href="sector-memos.html">Sector memos</a></div>
<div class="eyebrow">Applied cases · US · 2025–2026</div>
<h1>Sector Cases</h1>
<p class="sub">These are concrete sector/business-style applications of the lens framework. Each case starts with a representative industry, then reads it through the business-lens and force map instead of treating it as an isolated sector summary.</p>
<section class="section"><div class="grid">{cards}</div></section>
<footer>Built from business lenses and representative industry evidence.</footer>
</div></body></html>"""


def main():
    records = build_records()
    os.makedirs(PAGES_OUT, exist_ok=True)
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(build_hub(records))
    for record in records:
        with open(os.path.join(PAGES_OUT, f"{record['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(build_page(record))
    print(f"wrote {JSON_OUT}")
    print(f"wrote {HTML_OUT}")
    print(f"records={len(records)}")


if __name__ == "__main__":
    main()
