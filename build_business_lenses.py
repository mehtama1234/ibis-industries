#!/usr/bin/env python3
"""Build business-lens archetypes from operator playbooks and force translations."""

from __future__ import annotations

import html
import json
import os
from collections import Counter

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_OUT = os.path.join(ROOT, "business_lenses.json")
HTML_OUT = os.path.join(ROOT, "business-lenses.html")
PAGES_OUT = os.path.join(ROOT, "business-lenses")


def e(value):
    return html.escape(str(value or ""), quote=True)


PLAYBOOKS = json.load(open(os.path.join(ROOT, "operator_playbooks.json"), encoding="utf-8"))
FORCE_TRANSLATIONS = json.load(open(os.path.join(ROOT, "force_operator_translations.json"), encoding="utf-8"))
BRIEFS = json.load(open(os.path.join(ROOT, "briefs_full.json"), encoding="utf-8"))
BRIEFS_BY_SLUG = {b["slug"]: b for b in BRIEFS}

FORCES_BY_PLAYBOOK: dict[str, list[dict]] = {}
for force in FORCE_TRANSLATIONS:
    for pb in force["linked_playbooks"]:
        FORCES_BY_PLAYBOOK.setdefault(pb["slug"], []).append(force)


BUSINESS_LENS_CONFIG = {
    "local-services-rollup": {
        "lens_slug": "local-services-platform",
        "lens_title": "Local Services Platform",
        "core_offer": "Multi-site neighborhood services with centralized scheduling, marketing, pricing, and labor systems.",
        "economic_role": "service operator",
        "primary_customer": "Households and small local commercial buyers",
        "value_chain_position": "Last-mile local service delivery with centralized demand capture and operations",
        "demand_type": "non-discretionary + convenience-driven",
        "best_owner_type": "scaled regional platform",
        "why_owner_type": "This business wins when dispatch, marketing, retention, and labor systems scale across fragmented local demand.",
    },
    "specialty-manufacturer": {
        "lens_slug": "specified-product-manufacturer",
        "lens_title": "Specified Product Manufacturer",
        "core_offer": "Narrow industrial products that sit inside technical, regulated, or specified procurement flows.",
        "economic_role": "manufacturer",
        "primary_customer": "Contractors, labs, OEMs, distributors, and institutional buyers",
        "value_chain_position": "Upstream product supplier inside specified and replacement-driven demand chains",
        "demand_type": "mission-critical / non-discretionary",
        "best_owner_type": "specialist/niche expert",
        "why_owner_type": "The business works when product know-how, specification status, and operational discipline matter more than broad brand marketing.",
    },
    "health-services-operator": {
        "lens_slug": "reimbursement-managed-care-operator",
        "lens_title": "Reimbursement-Managed Care Operator",
        "core_offer": "Clinical or quasi-clinical services where reimbursement, staffing, compliance, and referral flow determine the economics.",
        "economic_role": "service operator",
        "primary_customer": "Patients, payers, referral sources, and care coordinators",
        "value_chain_position": "Direct care delivery inside payer and referral systems",
        "demand_type": "reimbursement-driven",
        "best_owner_type": "scaled regional platform",
        "why_owner_type": "Margin depends on throughput, payer mix, staffing, and documentation discipline, which favor scaled operators.",
    },
    "experiential-venue": {
        "lens_slug": "utilization-managed-experience-venue",
        "lens_title": "Utilization-Managed Experience Venue",
        "core_offer": "A venue where the experience itself is the product and economics depend on utilization, group bookings, and local scarcity.",
        "economic_role": "service operator",
        "primary_customer": "Consumers, families, corporate groups, and event buyers",
        "value_chain_position": "Consumer-facing destination format combining space, programming, and optional food/drink",
        "demand_type": "premium/status-driven + experience-driven",
        "best_owner_type": "franchise operator",
        "why_owner_type": "The business wins when a repeatable concept, utilization discipline, and local operating playbook can be scaled without losing venue quality.",
    },
    "food-production-niche": {
        "lens_slug": "niche-food-brand-producer",
        "lens_title": "Niche Food Brand Producer",
        "core_offer": "A focused food or beverage producer balancing taste, health, premium positioning, and channel power.",
        "economic_role": "manufacturer",
        "primary_customer": "Retailers, wholesalers, foodservice buyers, and consumers via branded channels",
        "value_chain_position": "Branded or niche producer upstream of retail and distribution intermediaries",
        "demand_type": "consumer preference-driven",
        "best_owner_type": "specialist/niche expert",
        "why_owner_type": "This works when brand, formulation, and mix discipline matter enough to offset retailer leverage and volatile inputs.",
    },
    "regulated-admin-stack": {
        "lens_slug": "regulated-workflow-infrastructure",
        "lens_title": "Regulated Workflow Infrastructure",
        "core_offer": "Software or service layers that convert mandatory administrative complexity into recurring revenue.",
        "economic_role": "claims/admin/compliance layer",
        "primary_customer": "Insurers, employers, healthcare operators, regulated enterprises, and public-sector buyers",
        "value_chain_position": "Workflow, identity, testing, and claims infrastructure inside mandatory systems",
        "demand_type": "policy-driven + mission-critical / non-discretionary",
        "best_owner_type": "software-led consolidator",
        "why_owner_type": "Recurring workflow, compliance, and auditability economics favor software-centric businesses with productized fulfillment.",
    },
    "distribution-middleman": {
        "lens_slug": "inventory-and-credit-distributor",
        "lens_title": "Inventory and Credit Distributor",
        "core_offer": "A distributor that survives because it provides inventory availability, technical know-how, credit, and local fulfillment speed.",
        "economic_role": "distributor",
        "primary_customer": "Contractors, institutions, retailers, and small operators who need availability and working-capital relief",
        "value_chain_position": "Middle layer between producers and fragmented end buyers",
        "demand_type": "mission-critical / non-discretionary",
        "best_owner_type": "scaled regional platform",
        "why_owner_type": "Scale matters because working capital, procurement, and service reliability make the middleman hard to remove.",
    },
    "care-and-family-infrastructure": {
        "lens_slug": "care-and-family-demand-platform",
        "lens_title": "Care and Family Demand Platform",
        "core_offer": "Services tied to aging, caregiving, child development, family support, and health-complexity spillover.",
        "economic_role": "service operator",
        "primary_customer": "Families, seniors, caregivers, payers, and public/private support systems",
        "value_chain_position": "Direct support layer sitting between households and institutional care systems",
        "demand_type": "demographic",
        "best_owner_type": "scaled regional platform",
        "why_owner_type": "Demographic demand is durable, but staffing, regulation, and service coordination favor scaled operators with strong labor systems.",
    },
}


CSS = """
:root{--bg:#101318;--panel:#171d24;--panel2:#1d2630;--line:#2a3440;--ink:#f0eadc;--muted:#a9b2bd;--faint:#74808d;--gold:#d4ad55;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,40px) 72px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:34px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.2rem,5vw,4rem);line-height:1;margin:.18em 0 .25em}.sub{max-width:850px;color:var(--muted);font-size:1.07rem}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.card h3{margin:.2em 0 .35em;font-size:1.12rem}.card p{margin:.35em 0 0;color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.list{margin:.75em 0 0;padding-left:18px;color:var(--muted)}.list li{margin:.4em 0}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);color:var(--faint);font-family:var(--mono);font-size:.72rem}
"""


PAGE_CSS = """
:root{--bg:#101318;--panel:#171d24;--panel2:#1d2630;--line:#2a3440;--ink:#f0eadc;--muted:#a9b2bd;--faint:#74808d;--gold:#d4ad55;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,40px) 72px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:34px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.2rem,5vw,4rem);line-height:1;margin:.18em 0 .22em}.sub{max-width:860px;color:var(--muted);font-size:1.07rem}.split{display:grid;grid-template-columns:minmax(0,1.15fr) minmax(280px,.85fr);gap:18px;margin-top:26px}.panel,.brief{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.panel h2,.brief h2{margin:0 0 .45em;font-size:1.18rem}.panel p,.brief p{color:var(--muted);margin:.4em 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.4em 0}.stack>*+*{margin-top:12px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}.brief h3{margin:.15em 0;font-size:1.04rem}.brief .stats{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.brief .stats span{font-family:var(--mono);font-size:.72rem;background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}@media(max-width:900px){.split{grid-template-columns:1fr}}footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);color:var(--faint);font-family:var(--mono);font-size:.72rem}
"""


def top_themes(playbook: dict) -> list[str]:
    return [theme for theme, _n in playbook.get("common_themes", [])[:5]]


def top_sectors(playbook: dict) -> list[str]:
    return [sector for sector, _n in playbook.get("sector_mix", [])[:3]]


def build_records():
    records = []
    for playbook in PLAYBOOKS:
        cfg = BUSINESS_LENS_CONFIG[playbook["slug"]]
        linked_forces = FORCES_BY_PLAYBOOK.get(playbook["slug"], [])
        constraint_counter = Counter()
        exposed_types = Counter()
        for force in linked_forces:
            constraint_counter.update(force["binding_constraints"])
            exposed_types.update(force["exposed_operator_types"])

        records.append(
            {
                "slug": cfg["lens_slug"],
                "title": cfg["lens_title"],
                "playbook_slug": playbook["slug"],
                "playbook_title": playbook["title"],
                "core_offer": cfg["core_offer"],
                "economic_role": cfg["economic_role"],
                "primary_customer": cfg["primary_customer"],
                "value_chain_position": cfg["value_chain_position"],
                "business_truth": (
                    f"This is a {cfg['economic_role']} business that wins when {playbook['thesis'].lower()}"
                ),
                "primary_industry_slug": playbook["industries"][0]["slug"],
                "adjacent_industry_slugs": [x["slug"] for x in playbook["industries"][1:5]],
                "evidence_industry_slugs": [x["slug"] for x in playbook["industries"][:6]],
                "sectors": top_sectors(playbook),
                "themes": top_themes(playbook),
                "primary_force_slugs": [f["slug"] for f in linked_forces[:3]],
                "secondary_force_slugs": [f["slug"] for f in linked_forces[3:6]],
                "demand_type": cfg["demand_type"],
                "binding_constraints": [x for x, _n in constraint_counter.most_common(3)],
                "best_owner_type": cfg["best_owner_type"],
                "why_this_owner_type": cfg["why_owner_type"],
                "advantaged_moves": [
                    "Use the linked force map as an operating dashboard, not just a research lens.",
                    "Design the business around the real constraint rather than the nominal category label.",
                    "Exploit scale only where it materially improves labor, compliance, channel, or procurement outcomes.",
                ],
                "likely_losers": [x for x, _n in exposed_types.most_common(2)],
                "linked_forces": [
                    {
                        "slug": f["slug"],
                        "title": f["title"],
                        "demand_logic": f["demand_logic"],
                        "margin_logic": f["margin_logic"],
                    }
                    for f in linked_forces
                ],
                "tension_items": [
                    f"This lens gets squeezed when {item} becomes the dominant constraint without enough scale, workflow, or pricing leverage."
                    for item in [x for x, _n in constraint_counter.most_common(3)]
                ],
                "second_order_items": [
                    f"{BRIEFS_BY_SLUG[x['slug']]['title']} shows how this model spills into adjacent markets once the same operator logic starts repeating."
                    for x in playbook["industries"][1:4]
                    if x["slug"] in BRIEFS_BY_SLUG
                ],
            }
        )
    return records


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


def build_detail_page(record: dict) -> str:
    primary = BRIEFS_BY_SLUG[record["primary_industry_slug"]]
    adjacent = [BRIEFS_BY_SLUG[s] for s in record["adjacent_industry_slugs"] if s in BRIEFS_BY_SLUG]
    evidence = [BRIEFS_BY_SLUG[s] for s in record["evidence_industry_slugs"] if s in BRIEFS_BY_SLUG]
    linked_force_cards = []
    for force in record["linked_forces"]:
        linked_force_cards.append(
            f"""<div class="panel">
  <div class="meta">Force</div>
  <h2>{e(force['title'])}</h2>
  <p><b>Demand logic:</b> {e(force['demand_logic'])}</p>
  <p><b>Margin logic:</b> {e(force['margin_logic'])}</p>
</div>"""
        )
    adjacent_cards = "\n".join(brief_card(b) for b in adjacent)
    evidence_cards = "\n".join(brief_card(b) for b in evidence)
    moves = "".join(f"<li>{e(m)}</li>" for m in record["advantaged_moves"])
    tensions = "".join(f"<li>{e(item)}</li>" for item in record["tension_items"])
    second_order = "".join(f"<li>{e(item)}</li>" for item in record["second_order_items"])
    likely_losers = "".join(f'<span class="chip">{e(x)}</span>' for x in record["likely_losers"])
    sectors = "".join(f'<span class="chip">{e(s)}</span>' for s in record["sectors"])
    themes = "".join(f'<span class="chip">{e(t)}</span>' for t in record["themes"])
    constraints = "".join(f'<span class="chip">{e(c)}</span>' for c in record["binding_constraints"])
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(record['title'])} — Business Lens</title><style>{PAGE_CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../force-operator-translations.html">Force-to-operator</a><a href="../business-lenses.html">Business lenses</a></div>
<div class="eyebrow">Business lens · US · 2025–2026</div>
<h1>{e(record['title'])}</h1>
<p class="sub">{e(record['business_truth'])}</p>
<div class="split">
  <main class="stack">
    <div class="panel">
      <div class="meta">Business truth</div>
      <h2>What this business really is</h2>
      <p>{e(record['core_offer'])}</p>
      <p><b>Primary customer:</b> {e(record['primary_customer'])}</p>
      <p><b>Value-chain position:</b> {e(record['value_chain_position'])}</p>
      <div class="chips">{sectors}</div>
      <div class="chips">{themes}</div>
    </div>
    <div class="panel">
      <div class="meta">Representative industry</div>
      <h2>{e(primary['title'])}</h2>
      <p>{e(primary.get('one_sentence') or primary.get('one_liner'))}</p>
      <div class="chips">{''.join(f'<span class="chip">{e(t)}</span>' for t in primary.get('themes', [])[:5])}</div>
    </div>
    <div class="section">
      <h2>Linked Forces</h2>
      <div class="stack">{''.join(linked_force_cards)}</div>
    </div>
    <div class="section">
      <h2>Evidence Industries</h2>
      <div class="grid">{evidence_cards}</div>
    </div>
    <div class="section">
      <h2>Adjacent Industry Reads</h2>
      <div class="grid">{adjacent_cards}</div>
    </div>
  </main>
  <aside class="stack">
    <div class="panel">
      <div class="meta">Demand and ownership</div>
      <h2>Operating stance</h2>
      <p><b>Demand type:</b> {e(record['demand_type'])}</p>
      <p><b>Best owner type:</b> {e(record['best_owner_type'])}</p>
      <p>{e(record['why_this_owner_type'])}</p>
      <div class="chips">{constraints}</div>
    </div>
    <div class="panel">
      <div class="meta">What to do</div>
      <h2>Advantaged moves</h2>
      <ul class="list">{moves}</ul>
    </div>
    <div class="panel">
      <div class="meta">Tensions</div>
      <h2>What breaks the read</h2>
      <ul class="list">{tensions}</ul>
    </div>
    <div class="panel">
      <div class="meta">Second-order effects</div>
      <h2>Where it spills next</h2>
      <ul class="list">{second_order}</ul>
    </div>
    <div class="panel">
      <div class="meta">Who gets squeezed</div>
      <h2>Likely losers</h2>
      <div class="chips">{likely_losers}</div>
    </div>
  </aside>
</div>
<footer>Built from the operator playbooks, force translations, and representative industries in the 1,491-industry corpus.</footer>
</div></body></html>"""


def build_html(records):
    cards = []
    for r in records:
        force_chips = "".join(f'<span class="chip">{e(f["title"])}</span>' for f in r["linked_forces"][:5])
        sector_chips = "".join(f'<span class="chip">{e(s)}</span>' for s in r["sectors"])
        theme_chips = "".join(f'<span class="chip">{e(t)}</span>' for t in r["themes"])
        constraint_chips = "".join(f'<span class="chip">{e(c)}</span>' for c in r["binding_constraints"])
        moves = "".join(f"<li>{e(m)}</li>" for m in r["advantaged_moves"])
        tensions = "".join(f"<li>{e(item)}</li>" for item in r["tension_items"][:2])
        second_order = "".join(f"<li>{e(item)}</li>" for item in r["second_order_items"][:2])
        cards.append(
            f"""<article class="card">
  <div class="meta">{e(r['economic_role'])}</div>
  <h3><a href="business-lenses/{e(r['slug'])}.html">{e(r['title'])}</a></h3>
  <p>{e(r['business_truth'])}</p>
  <p><b>Demand type:</b> {e(r['demand_type'])}</p>
  <p><b>Best owner type:</b> {e(r['best_owner_type'])}</p>
  <div class="meta" style="margin-top:14px">Where it shows up</div>
  <div class="chips">{sector_chips}{theme_chips}</div>
  <div class="meta" style="margin-top:14px">Signals</div>
  <div class="chips">{force_chips}</div>
  <div class="chips">{constraint_chips}</div>
  <div class="meta" style="margin-top:14px">What to do</div>
  <p>{e(r['why_this_owner_type'])}</p>
  <div class="meta" style="margin-top:14px">What to underwrite</div>
  <ul class="list">{moves}</ul>
  <div class="meta" style="margin-top:14px">Tensions</div>
  <ul class="list">{tensions}</ul>
  <div class="meta" style="margin-top:14px">Second-order effects</div>
  <ul class="list">{second_order}</ul>
</article>"""
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Business Lenses — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="force-operator-translations.html">Force-to-operator</a><a href="operators.html">Operator playbooks</a></div>
<div class="eyebrow">Business lenses · US · 2025–2026</div>
<h1>Business Lenses</h1>
<p class="sub">These are reusable business archetypes built from the operator playbooks, the force taxonomy, and the company/business lens template. They show how to turn industry and force context into a repeatable business read.</p>
<div class="section"><div class="card"><p>Use this page to move from category language to archetype logic: where the model shows up, which forces signal opportunity or pressure, what operator stance tends to work, and what investors should actually underwrite inside the model.</p></div></div>
<section class="section"><div class="grid">{''.join(cards)}</div></section>
<footer>Built from operator playbooks, force-to-operator translations, and the company/business lens template. Use these as starting points for company and sector writeups.</footer>
</div></body></html>"""


def main():
    records = build_records()
    os.makedirs(PAGES_OUT, exist_ok=True)
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(build_html(records))
    for record in records:
        with open(os.path.join(PAGES_OUT, f"{record['slug']}.html"), "w", encoding="utf-8") as f:
            f.write(build_detail_page(record))
    print(f"wrote {JSON_OUT}")
    print(f"wrote {HTML_OUT}")
    print(f"records={len(records)}")


if __name__ == "__main__":
    main()
