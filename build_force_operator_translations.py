#!/usr/bin/env python3
"""Build operator implications for each major force."""

from __future__ import annotations

import html
import json
import os

from forces_config import FORCES
from operator_playbooks_config import PLAYBOOKS

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_OUT = os.path.join(ROOT, "force_operator_translations.json")
HTML_OUT = os.path.join(ROOT, "force-operator-translations.html")


def e(value):
    return html.escape(str(value or ""), quote=True)


FORCE_OPERATOR_VIEWS = {
    "atoms-strike-back": {
        "demand_logic": "Demand follows physical security, domestic production mandates, reshoring, and tariff-induced supply-chain rewiring rather than pure end-market growth.",
        "margin_logic": "Margins improve for domestic suppliers with specification, proximity, or procurement leverage; they compress for import-reliant sellers and downstream price takers.",
        "binding_constraints": ["procurement / inputs", "capital / rates", "channel access"],
        "advantaged_operator_types": ["specialist/niche expert", "scaled regional platform", "asset-heavy institutional owner"],
        "exposed_operator_types": ["local owner-operator", "marketplace/intermediary"],
        "linked_playbooks": ["specialty-manufacturer", "distribution-middleman"],
        "what_to_do": [
            "Reduce single-country sourcing exposure.",
            "Move toward specified, harder-to-substitute products.",
            "Use procurement scale or nearshoring relationships as a moat.",
        ],
    },
    "the-great-consolidation": {
        "demand_logic": "Demand is stable enough, but the winning structure is scale: buyers and operators that can centralize finance, labor, compliance, and distribution absorb the fragmented tail.",
        "margin_logic": "Platform economics improve through shared overhead and purchasing power; independent operators lose margin as complexity rises.",
        "binding_constraints": ["capital / rates", "labor", "compliance / regulation"],
        "advantaged_operator_types": ["PE roll-up", "scaled regional platform", "franchise operator"],
        "exposed_operator_types": ["local owner-operator", "specialist/niche expert"],
        "linked_playbooks": ["local-services-rollup", "health-services-operator", "distribution-middleman"],
        "what_to_do": [
            "Centralize back office and procurement before chasing more locations.",
            "Buy fragmentation where local trust matters but systems can still scale.",
            "Treat compliance and staffing as core platform capabilities, not overhead.",
        ],
    },
    "the-real-estate-reckoning": {
        "demand_logic": "Demand is rotating away from weak office formats toward logistics, data-linked assets, adaptive reuse, land, and selective housing formats.",
        "margin_logic": "Owners on the right side of utilization and asset repositioning can capture upside; static owners and rate-sensitive landlords get squeezed.",
        "binding_constraints": ["capital / rates", "utilization", "power / infrastructure"],
        "advantaged_operator_types": ["asset-heavy institutional owner", "scaled regional platform"],
        "exposed_operator_types": ["local owner-operator", "franchise operator"],
        "linked_playbooks": ["care-and-family-infrastructure", "experiential-venue"],
        "what_to_do": [
            "Prioritize assets with durable demand or conversion optionality.",
            "Underwrite refinancing risk as seriously as occupancy risk.",
            "Treat land, power access, and entitlement position as strategic assets.",
        ],
    },
    "the-compliance-tax": {
        "demand_logic": "Demand is created by mandatory workflows: reporting, documentation, testing, claims, privacy, security, and regulated admin tasks that customers cannot fully defer.",
        "margin_logic": "Margins improve when compliance work is software-enabled, recurring, and embedded; they erode when delivery stays manual and bespoke.",
        "binding_constraints": ["compliance / regulation", "labor", "customer acquisition cost"],
        "advantaged_operator_types": ["software-led consolidator", "scaled regional platform", "specialist/niche expert"],
        "exposed_operator_types": ["local owner-operator", "marketplace/intermediary"],
        "linked_playbooks": ["regulated-admin-stack", "health-services-operator"],
        "what_to_do": [
            "Sell risk reduction and workflow certainty, not generic admin support.",
            "Automate low-value fulfillment while protecting auditability and trust.",
            "Bundle compliance into recurring infrastructure rather than project work.",
        ],
    },
    "the-margin-vise": {
        "demand_logic": "Demand may still exist, but customers resist price increases and often downgrade mix, forcing operators to defend profitability through efficiency, mix, or positioning.",
        "margin_logic": "Premium positioning, automation, and lock-in preserve margin; commodity formats and labor-heavy businesses without pricing power get squeezed.",
        "binding_constraints": ["labor", "procurement / inputs", "pricing power"],
        "advantaged_operator_types": ["specialist/niche expert", "scaled regional platform", "software-led consolidator"],
        "exposed_operator_types": ["local owner-operator", "franchise operator"],
        "linked_playbooks": ["food-production-niche", "local-services-rollup", "distribution-middleman"],
        "what_to_do": [
            "Find the customer segment that still pays for speed, trust, or premium positioning.",
            "Automate wherever labor is repetitive and customer-facing differentiation is low.",
            "Cut low-margin complexity before chasing volume.",
        ],
    },
    "the-pricing-power-collapse": {
        "demand_logic": "Volume often rises because aging, utilization, or need rises, but reimbursement or payer control prevents operators from fully monetizing that demand.",
        "margin_logic": "Only scaled providers, specialists with referral power, or operators with superior workflow discipline defend returns.",
        "binding_constraints": ["reimbursement", "compliance / regulation", "labor"],
        "advantaged_operator_types": ["scaled regional platform", "PE roll-up", "software-led consolidator"],
        "exposed_operator_types": ["local owner-operator", "specialist/niche expert"],
        "linked_playbooks": ["health-services-operator", "care-and-family-infrastructure", "regulated-admin-stack"],
        "what_to_do": [
            "Treat payer mix as a core operating lever.",
            "Improve throughput and documentation before expanding footprint.",
            "Add adjacent reimbursable services only where operational complexity can be handled.",
        ],
    },
    "the-health-reckoning": {
        "demand_logic": "Demand shifts from pure indulgence toward health-aligned, lower-calorie, sober-curious, convenient, and functional consumption patterns.",
        "margin_logic": "Premium or health-aligned products can hold margin; legacy vice or sugary volume stories face shrinkage and discounting pressure.",
        "binding_constraints": ["consumer preference-driven demand", "procurement / inputs", "channel access"],
        "advantaged_operator_types": ["specialist/niche expert", "brand-led scaled platform", "franchise operator"],
        "exposed_operator_types": ["local owner-operator", "marketplace/intermediary"],
        "linked_playbooks": ["food-production-niche", "experiential-venue"],
        "what_to_do": [
            "Reposition around function, moderation, or premium ritual instead of mass indulgence.",
            "Watch GLP-1 and sober-curious effects at the category level, not as anecdotes.",
            "Protect gross margin through mix, not only through price increases.",
        ],
    },
    "the-hollow-middle": {
        "demand_logic": "Consumers split between value and premium, leaving undifferentiated mid-market formats without a clear reason to win.",
        "margin_logic": "Margins hold at the ends of the barbell; the middle competes on discounting, promotional intensity, and fading relevance.",
        "binding_constraints": ["consumer preference-driven demand", "channel access", "pricing power"],
        "advantaged_operator_types": ["brand-led scaled platform", "specialist/niche expert", "asset-heavy institutional owner"],
        "exposed_operator_types": ["local owner-operator", "franchise operator"],
        "linked_playbooks": ["experiential-venue", "food-production-niche", "local-services-rollup"],
        "what_to_do": [
            "Pick a lane: value, premium, or strong niche identity.",
            "Remove generic middle-market assortment or service design.",
            "Use experience or community as a moat where product itself is commoditizing.",
        ],
    },
    "the-channel-shift": {
        "demand_logic": "Demand is increasingly discovered, compared, and fulfilled through platforms, marketplaces, omnichannel systems, or experience-led physical venues.",
        "margin_logic": "Platform owners and omnichannel scale players capture economics; single-channel physical sellers lose traffic and gross margin.",
        "binding_constraints": ["channel access", "customer acquisition cost", "utilization"],
        "advantaged_operator_types": ["software-led consolidator", "scaled regional platform", "specialist/niche expert"],
        "exposed_operator_types": ["local owner-operator", "marketplace/intermediary"],
        "linked_playbooks": ["experiential-venue", "distribution-middleman", "local-services-rollup"],
        "what_to_do": [
            "Treat channel control as strategy, not marketing.",
            "Build omnichannel or experiential defensibility where physical presence remains important.",
            "Assume platform tax and customer acquisition costs will rise over time.",
        ],
    },
    "the-fractional-worker": {
        "demand_logic": "Firms are buying narrower slices of expertise and execution, creating demand for fractional leadership, expert networks, recruiters, and project-based support.",
        "margin_logic": "Margins improve for trusted matching layers, specialist networks, and high-signal experts; generic labor providers face commoditization.",
        "binding_constraints": ["labor", "customer acquisition cost", "trust"],
        "advantaged_operator_types": ["specialist/niche expert", "marketplace/intermediary", "software-led consolidator"],
        "exposed_operator_types": ["local owner-operator", "franchise operator"],
        "linked_playbooks": ["regulated-admin-stack", "local-services-rollup"],
        "what_to_do": [
            "Package expertise into repeatable offerings rather than vague advisory hours.",
            "Differentiate on signal, trust, or workflow integration, not just access to talent.",
            "Assume buyers want variable cost structures and faster ramp time.",
        ],
    },
    "the-graying-market": {
        "demand_logic": "Demographic aging creates steady demand in care delivery, chronic disease, senior living, home support, and longevity finance.",
        "margin_logic": "Demand is durable, but labor scarcity and reimbursement rules decide whether that demand becomes attractive economics.",
        "binding_constraints": ["labor", "reimbursement", "compliance / regulation"],
        "advantaged_operator_types": ["scaled regional platform", "PE roll-up", "asset-heavy institutional owner"],
        "exposed_operator_types": ["local owner-operator", "specialist/niche expert"],
        "linked_playbooks": ["care-and-family-infrastructure", "health-services-operator"],
        "what_to_do": [
            "Treat staffing system quality as strategically important as occupancy or referrals.",
            "Focus on care models that shift acuity or site of care in economically rewarded directions.",
            "Use scale where compliance and labor coordination are burdensome.",
        ],
    },
    "the-labor-squeeze": {
        "demand_logic": "Demand remains present across trades, care, logistics, and service sectors, but the missing input is labor rather than customers.",
        "margin_logic": "Wage inflation compresses margins unless operators automate, reprice, or structurally improve utilization.",
        "binding_constraints": ["labor", "utilization", "pricing power"],
        "advantaged_operator_types": ["scaled regional platform", "asset-heavy institutional owner", "software-led consolidator"],
        "exposed_operator_types": ["local owner-operator", "franchise operator"],
        "linked_playbooks": ["local-services-rollup", "care-and-family-infrastructure", "specialty-manufacturer"],
        "what_to_do": [
            "Recruitment and retention need to be treated as operating systems, not HR functions.",
            "Automate low-skill, repetitive work where customer trust does not suffer.",
            "Reprice faster and simplify service mix where labor cannot be scaled.",
        ],
    },
    "the-compute-super-cycle": {
        "demand_logic": "AI creates direct demand for compute, storage, hosting, power, cooling, and supporting industrial trades and materials.",
        "margin_logic": "Ownership of scarce infrastructure and enabling trades improves economics; businesses downstream of power scarcity face rising costs and delays.",
        "binding_constraints": ["power / infrastructure", "capital / rates", "labor"],
        "advantaged_operator_types": ["asset-heavy institutional owner", "scaled regional platform", "specialist/niche expert"],
        "exposed_operator_types": ["local owner-operator", "marketplace/intermediary"],
        "linked_playbooks": ["specialty-manufacturer", "distribution-middleman", "regulated-admin-stack"],
        "what_to_do": [
            "Map exposure to data-center and transmission buildout explicitly.",
            "Prioritize positions with power access, electrical capability, or mission-critical software linkage.",
            "Assume second-order winners exist in construction, cooling, and equipment supply, not just software.",
        ],
    },
    "money-gets-unbundled": {
        "demand_logic": "Financial services demand is moving from branch-centric institutions toward rails, embedded workflows, platforms, and data-rich intermediaries.",
        "margin_logic": "Scale, data, and recurring transaction flow preserve economics; undifferentiated middlemen and smaller institutions lose spread and relevance.",
        "binding_constraints": ["compliance / regulation", "capital / rates", "channel access"],
        "advantaged_operator_types": ["software-led consolidator", "scaled regional platform", "asset-heavy institutional owner"],
        "exposed_operator_types": ["local owner-operator", "marketplace/intermediary"],
        "linked_playbooks": ["regulated-admin-stack", "distribution-middleman"],
        "what_to_do": [
            "Own the workflow or the rail, not just the customer relationship veneer.",
            "Treat rate sensitivity and regulatory overhead as core economics, not macro noise.",
            "Differentiate on embeddedness, switching friction, or proprietary data.",
        ],
    },
}


CSS = """
:root{--bg:#0f1319;--panel:#171d24;--panel2:#1d2630;--line:#2a3440;--ink:#f0eadc;--muted:#a9b2bd;--faint:#74808d;--gold:#d4ad55;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,40px) 72px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:34px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.2rem,5vw,4rem);line-height:1;margin:.18em 0 .25em}h2{font-size:1.45rem;margin:0 0 .5em}.sub{max-width:850px;color:var(--muted);font-size:1.07rem}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.card h3{margin:.2em 0 .35em;font-size:1.12rem}.card p{margin:.35em 0 0;color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.list{margin:.75em 0 0;padding-left:18px;color:var(--muted)}.list li{margin:.4em 0}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);color:var(--faint);font-family:var(--mono);font-size:.72rem}
"""


def build_records():
    playbook_lookup = {p["slug"]: p for p in PLAYBOOKS}
    records = []
    for force in FORCES:
        view = FORCE_OPERATOR_VIEWS[force["slug"]]
        records.append(
            {
                "slug": force["slug"],
                "title": force["title"],
                "repo_lens": force["lens"],
                "signature": force["signature"],
                "demand_logic": view["demand_logic"],
                "margin_logic": view["margin_logic"],
                "binding_constraints": view["binding_constraints"],
                "advantaged_operator_types": view["advantaged_operator_types"],
                "exposed_operator_types": view["exposed_operator_types"],
                "linked_playbooks": [
                    {
                        "slug": s,
                        "title": playbook_lookup[s]["title"],
                        "lens": playbook_lookup[s]["lens"],
                    }
                    for s in view["linked_playbooks"]
                ],
                "what_to_do": view["what_to_do"],
            }
        )
    return records


def build_html(records):
    cards = []
    for r in records:
        linked = "".join(f'<span class="chip">{e(p["title"])}</span>' for p in r["linked_playbooks"])
        constraints = "".join(f'<span class="chip">{e(c)}</span>' for c in r["binding_constraints"])
        winners = "".join(f'<span class="chip">{e(x)}</span>' for x in r["advantaged_operator_types"])
        losers = "".join(f'<span class="chip">{e(x)}</span>' for x in r["exposed_operator_types"])
        moves = "".join(f"<li>{e(x)}</li>" for x in r["what_to_do"])
        cards.append(
            f"""<article class="card">
  <div class="meta">{e(r['repo_lens'])}</div>
  <h3>{e(r['title'])}</h3>
  <p>{e(r['signature'])}</p>
  <p><b>Demand logic:</b> {e(r['demand_logic'])}</p>
  <p><b>Margin logic:</b> {e(r['margin_logic'])}</p>
  <div class="chips">{constraints}</div>
  <p><b>Advantaged operator types</b></p>
  <div class="chips">{winners}</div>
  <p><b>Exposed operator types</b></p>
  <div class="chips">{losers}</div>
  <p><b>Linked playbooks</b></p>
  <div class="chips">{linked}</div>
  <p><b>What to do</b></p>
  <ul class="list">{moves}</ul>
</article>"""
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Force-to-Operator Translations — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="forces/index.html">Forces</a><a href="operators.html">Operator playbooks</a></div>
<div class="eyebrow">Operator implications · US · 2025–2026</div>
<h1>Force-to-Operator Translations</h1>
<p class="sub">This is the bridge from macro force to business reality. Each major force is translated into demand logic, margin logic, binding constraints, advantaged operator types, exposed operator types, and practical moves.</p>
<section class="section"><div class="grid">{''.join(cards)}</div></section>
<footer>Built from the current force taxonomy and operator playbook layer. Use this page as the decision bridge between macro interpretation and business-level writing.</footer>
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
