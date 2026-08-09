#!/usr/bin/env python3
"""Build a canonical economic-intelligence taxonomy from force and operator configs."""

from __future__ import annotations

import json
import os
from collections import Counter

from forces_config import FORCES
from operator_playbooks_config import PLAYBOOKS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "economic_intelligence_taxonomy.json")


DOMAIN_CONFIG = {
    "industrial": {
        "title": "Industrial",
        "description": "How the physical economy is being rebuilt through tariffs, capex, infrastructure, real-estate rotation, compliance burden, and margin pressure.",
        "questions": [
            "Where is capex flowing and what physical bottlenecks shape it?",
            "Which industries are being repriced by tariffs, power, labor, or real-estate math?",
            "Where does scale or asset ownership matter more than craftsmanship or fragmentation?",
        ],
        "force_slugs": [
            "atoms-strike-back",
            "the-great-consolidation",
            "the-real-estate-reckoning",
            "the-compliance-tax",
            "the-margin-vise",
            "the-pricing-power-collapse",
        ],
        "operator_slugs": [
            "specialty-manufacturer",
            "distribution-middleman",
            "regulated-admin-stack",
        ],
    },
    "consumer": {
        "title": "Consumer",
        "description": "How households are reallocating spend across value, premium, health, convenience, channels, and experiences.",
        "questions": [
            "Where are consumers trading down, and where do they still pay up?",
            "Which categories are being reshaped by health, convenience, or status signaling?",
            "Which parts of consumer demand are cyclical versus structurally re-ranked?",
        ],
        "force_slugs": [
            "the-health-reckoning",
            "the-hollow-middle",
            "the-channel-shift",
            "the-margin-vise",
        ],
        "operator_slugs": [
            "experiential-venue",
            "food-production-niche",
            "local-services-rollup",
        ],
    },
    "cultural_social": {
        "title": "Cultural & Social",
        "description": "How identity, work, attention, status, and norms are changing behavior across labor, media, food, retail, and services.",
        "questions": [
            "How are work identity, expertise, and junior labor changing?",
            "How is status moving between goods, experiences, and digital mediation?",
            "Which social changes are becoming economic demand shifts rather than niche behaviors?",
        ],
        "force_slugs": [
            "the-fractional-worker",
            "the-health-reckoning",
            "the-hollow-middle",
            "the-channel-shift",
        ],
        "operator_slugs": [
            "experiential-venue",
            "local-services-rollup",
            "health-services-operator",
        ],
    },
    "societal_institutional": {
        "title": "Societal & Institutional",
        "description": "How demographics, regulation, public funding, care burden, institutional risk, and labor supply are reorganizing the economy.",
        "questions": [
            "Where do demographics create inevitable demand but constrained returns?",
            "Where does regulation create drag, defensibility, or both?",
            "Which sectors are really driven by reimbursement, staffing, or policy rather than pure market demand?",
        ],
        "force_slugs": [
            "the-graying-market",
            "the-labor-squeeze",
            "the-fractional-worker",
            "the-compliance-tax",
            "the-pricing-power-collapse",
        ],
        "operator_slugs": [
            "care-and-family-infrastructure",
            "health-services-operator",
            "regulated-admin-stack",
        ],
    },
    "technological": {
        "title": "Technological",
        "description": "How AI, software, payments infrastructure, power demand, and data-center buildout are reshaping cost structures and winners.",
        "questions": [
            "Where does AI substitute labor versus increase demand for infrastructure?",
            "Which businesses own the rails, the software layer, or the compliance workflows around digitization?",
            "Where is compute demand spilling into power, construction, telecom, and cooling chains?",
        ],
        "force_slugs": [
            "the-compute-super-cycle",
            "money-gets-unbundled",
        ],
        "operator_slugs": [
            "regulated-admin-stack",
            "distribution-middleman",
            "specialty-manufacturer",
        ],
    },
    "operator_business_models": {
        "title": "Operator & Business-Model Lenses",
        "description": "How the force map translates into practical business archetypes and recurring operator questions.",
        "questions": [
            "What actually drives margin durability in this business type?",
            "Is the binding constraint labor, regulation, capital, demand, distribution, or procurement scale?",
            "What kind of operator is advantaged by the current force environment?",
        ],
        "force_slugs": [
            "the-margin-vise",
            "the-great-consolidation",
            "the-labor-squeeze",
            "the-pricing-power-collapse",
            "the-channel-shift",
        ],
        "operator_slugs": [p["slug"] for p in PLAYBOOKS],
    },
}


CROSSCUTS = [
    {
        "slug": "labor-scarcity",
        "title": "Labor Scarcity",
        "description": "Skilled trades, care work, logistics, and service labor remain binding constraints across otherwise unrelated industries.",
        "force_slugs": ["the-labor-squeeze", "the-graying-market", "the-fractional-worker"],
    },
    {
        "slug": "consumer-bifurcation",
        "title": "Consumer Bifurcation",
        "description": "The middle market is hollowing out while value and premium positions both keep winning for different reasons.",
        "force_slugs": ["the-hollow-middle", "the-channel-shift", "the-margin-vise"],
    },
    {
        "slug": "ai-and-automation",
        "title": "AI and Automation",
        "description": "AI is a labor story, an infrastructure story, and a software/compliance story at the same time.",
        "force_slugs": ["the-compute-super-cycle", "money-gets-unbundled", "the-fractional-worker"],
    },
    {
        "slug": "demographic-aging",
        "title": "Demographic Aging",
        "description": "Aging creates reliable demand growth, but staffing, reimbursement, and care-delivery friction cap who captures the upside.",
        "force_slugs": ["the-graying-market", "the-pricing-power-collapse", "the-labor-squeeze"],
    },
    {
        "slug": "capital-and-scale",
        "title": "Capital and Scale",
        "description": "Higher rates and heavier compliance reward scale players and financial owners while squeezing independents and mid-sized operators.",
        "force_slugs": ["the-great-consolidation", "the-real-estate-reckoning", "money-gets-unbundled", "the-compliance-tax"],
    },
]


def build_force_records():
    records = []
    for force in FORCES:
        group_records = []
        evidence_counter = Counter()
        subforce_count = 0
        for group_label, items in force["groups"].items():
            subforces = []
            for subslug, title, evidence_str, angle in items:
                evidence = [s for s in str(evidence_str).split() if s]
                evidence_counter.update(evidence)
                subforces.append(
                    {
                        "slug": subslug,
                        "title": title,
                        "angle": angle,
                        "evidence_slugs": evidence,
                    }
                )
                subforce_count += 1
            group_records.append(
                {
                    "label": group_label,
                    "subforces": subforces,
                }
            )
        records.append(
            {
                "slug": force["slug"],
                "title": force["title"],
                "repo_lens": force["lens"],
                "signature": force["signature"],
                "group_count": len(group_records),
                "subforce_count": subforce_count,
                "evidence_slug_count": len(evidence_counter),
                "groups": group_records,
            }
        )
    return records


def build_operator_records():
    return [
        {
            "slug": pb["slug"],
            "title": pb["title"],
            "lens": pb["lens"],
            "thesis": pb["thesis"],
            "industry_count": len(pb["slugs"]),
            "industry_slugs": pb["slugs"],
            "operator_questions": pb["operator_questions"],
        }
        for pb in PLAYBOOKS
    ]


def main() -> None:
    force_records = build_force_records()
    operator_records = build_operator_records()
    force_lookup = {f["slug"]: f for f in force_records}
    operator_lookup = {o["slug"]: o for o in operator_records}

    domains = []
    for slug, cfg in DOMAIN_CONFIG.items():
        domains.append(
            {
                "slug": slug,
                "title": cfg["title"],
                "description": cfg["description"],
                "questions": cfg["questions"],
                "forces": [force_lookup[s] for s in cfg["force_slugs"]],
                "operators": [operator_lookup[s] for s in cfg["operator_slugs"]],
            }
        )

    out = {
        "metadata": {
            "generated_at": "2026-08-09",
            "industry_brief_count": 1491,
            "force_count": len(force_records),
            "operator_playbook_count": len(operator_records),
            "purpose": "Canonical taxonomy for the economic-intelligence interpretation layer built on top of the completed industry corpus.",
        },
        "working_thesis": (
            "The US economy in 2025-2026 is being reorganized by overlapping pressures: labor scarcity, demographic aging, "
            "AI and compute buildout, consumer bifurcation, channel migration, politicized supply chains, compliance load, "
            "higher cost of capital, and consolidation."
        ),
        "domains": domains,
        "crosscuts": CROSSCUTS,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"wrote {OUT}")
    print(
        f"domains={len(domains)} forces={len(force_records)} "
        f"operators={len(operator_records)} crosscuts={len(CROSSCUTS)}"
    )


if __name__ == "__main__":
    main()
