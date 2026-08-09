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


def e(value):
    return html.escape(str(value or ""), quote=True)


PLAYBOOKS = json.load(open(os.path.join(ROOT, "operator_playbooks.json"), encoding="utf-8"))
FORCE_TRANSLATIONS = json.load(open(os.path.join(ROOT, "force_operator_translations.json"), encoding="utf-8"))

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
            }
        )
    return records


def build_html(records):
    cards = []
    for r in records:
        force_chips = "".join(f'<span class="chip">{e(f["title"])}</span>' for f in r["linked_forces"][:5])
        sector_chips = "".join(f'<span class="chip">{e(s)}</span>' for s in r["sectors"])
        theme_chips = "".join(f'<span class="chip">{e(t)}</span>' for t in r["themes"])
        constraint_chips = "".join(f'<span class="chip">{e(c)}</span>' for c in r["binding_constraints"])
        moves = "".join(f"<li>{e(m)}</li>" for m in r["advantaged_moves"])
        cards.append(
            f"""<article class="card">
  <div class="meta">{e(r['economic_role'])}</div>
  <h3>{e(r['title'])}</h3>
  <p>{e(r['business_truth'])}</p>
  <p><b>Demand type:</b> {e(r['demand_type'])}</p>
  <p><b>Best owner type:</b> {e(r['best_owner_type'])}</p>
  <p>{e(r['why_this_owner_type'])}</p>
  <div class="chips">{sector_chips}</div>
  <div class="chips">{theme_chips}</div>
  <div class="chips">{force_chips}</div>
  <div class="chips">{constraint_chips}</div>
  <ul class="list">{moves}</ul>
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
<section class="section"><div class="grid">{''.join(cards)}</div></section>
<footer>Built from operator playbooks, force-to-operator translations, and the company/business lens template. Use these as starting points for company and sector writeups.</footer>
</div></body></html>"""


def main():
    records = build_records()
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(build_html(records))
    print(f"wrote {JSON_OUT}")
    print(f"wrote {HTML_OUT}")
    print(f"records={len(records)}")


if __name__ == "__main__":
    main()
