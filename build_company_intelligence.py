#!/usr/bin/env python3
"""Build a company-intelligence layer from named operators in the industry corpus."""

from __future__ import annotations

import ast
import html
import json
import os
import re
from collections import Counter, defaultdict
from typing import Any

ROOT = os.path.dirname(os.path.abspath(__file__))
BRIEFS = json.load(open(os.path.join(ROOT, "briefs_full.json"), encoding="utf-8"))
BRIEFS_BY_SLUG = {brief["slug"]: brief for brief in BRIEFS}
LENSES = json.load(open(os.path.join(ROOT, "business_lenses.json"), encoding="utf-8"))
FORCE_TRANSLATIONS = json.load(open(os.path.join(ROOT, "force_operator_translations.json"), encoding="utf-8"))
TAXONOMY = json.load(open(os.path.join(ROOT, "economic_intelligence_taxonomy.json"), encoding="utf-8"))
AMERICAN_THEMES = json.load(open(os.path.join(ROOT, "american_themes_taxonomy.json"), encoding="utf-8"))["themes"]

UNIVERSE_JSON = os.path.join(ROOT, "company_universe.json")
UNIVERSE_HTML = os.path.join(ROOT, "company-universe.html")
CLUSTERS_JSON = os.path.join(ROOT, "company_clusters.json")
CLUSTERS_HTML = os.path.join(ROOT, "company-clusters.html")
SCOREBOARD_JSON = os.path.join(ROOT, "company_scoreboard.json")
SCOREBOARD_HTML = os.path.join(ROOT, "company-scoreboard.html")
COMPARISONS_JSON = os.path.join(ROOT, "company_comparisons.json")
COMPARISONS_HTML = os.path.join(ROOT, "company-comparisons.html")
PAGES_DIR = os.path.join(ROOT, "company-pages")
_MODELLINE_PATH = os.path.join(ROOT, "business_model_prose.json")
MODELLINE = json.load(open(_MODELLINE_PATH, encoding="utf-8")) if os.path.exists(_MODELLINE_PATH) else {}

FORCES_BY_SLUG = {force["slug"]: force for force in FORCE_TRANSLATIONS}
LENSES_BY_SLUG = {lens["slug"]: lens for lens in LENSES}
THEMES_BY_SLUG = {theme["slug"]: theme for theme in AMERICAN_THEMES}

POSITIVE_THEME_SLUGS = {
    "machine-intelligence-and-compute-buildout",
    "physical-reindustrialization-and-infrastructure",
    "regulated-software-and-admin-state",
    "scale-financialization-and-the-owned-economy",
    "aging-care-and-the-assistance-economy",
}

NEGATIVE_THEME_SLUGS = {
    "barbelled-consumer-america",
    "work-without-the-old-firm",
    "space-housing-and-local-friction",
}

CORP_SUFFIXES = {
    "inc",
    "inc.",
    "corp",
    "corp.",
    "corporation",
    "co",
    "co.",
    "company",
    "companies",
    "holdings",
    "holding",
    "group",
    "plc",
    "llc",
    "ltd",
    "ltd.",
    "lp",
    "l.p.",
    "sa",
    "ag",
    "nv",
}

SKIP_PREFIXES = (
    "no ",
    "independent ",
    "thousands of ",
    "fragmented ",
    "commercial banks ",
    "owner-operators",
    "various ",
)

SKIP_EXACT = {
    "competitive set",
    "regional and independent operators",
    "independent operators",
    "other regional operators",
    "private operators",
    "major regional operators",
}

NORMALIZATION_OVERRIDES = {
    "amazon com": "amazon",
    "jp morgan chase": "jpmorgan chase",
    "jpmorgan": "jpmorgan chase",
    "walmart inc": "walmart",
    "walmart marketplace": "walmart",
    "home depot": "the home depot",
    "lowes": "lowe's",
    "3m company": "3m",
    "3m co": "3m",
    "google": "alphabet",
    "meta platforms": "meta",
    "coca cola": "the coca-cola company",
    "coca cola company": "the coca-cola company",
    "ibm consulting": "ibm",
    "samsung electronics": "samsung",
    "abbott laboratories": "abbott",
    "caterpillar inc": "caterpillar",
}

POSITIVE_FORCE_SLUGS = {
    "the-great-consolidation",
    "the-compute-super-cycle",
    "the-graying-market",
    "the-breach-economy",
    "the-compliance-tax",
    "the-channel-shift",
    "the-electrification",
    "atoms-strike-back",
    "money-gets-unbundled",
    "the-experience-economy",
}

NEGATIVE_FORCE_SLUGS = {
    "the-pricing-power-collapse",
    "the-margin-vise",
    "the-labor-squeeze",
    "the-hollow-middle",
    "the-health-reckoning",
    "the-real-estate-reckoning",
    "commodity-whiplash",
    "the-immigration-squeeze",
}

FAVORABLE_OWNER_TYPES = {
    "scaled regional platform",
    "software-led consolidator",
    "specialist/niche expert",
}

PSEUDO_CLUSTER_CONFIG = {
    "omnichannel-scale-retailer": {
        "title": "Omnichannel Scale Retailer",
        "business_truth": "This is a scaled merchant-platform business that wins when traffic, fulfillment, supplier terms, and customer data are centralized across physical and digital channels.",
        "best_owner_type": "scaled platform operator",
        "why_owner_type": "The economics favor operators that can spread logistics, merchandising, pricing, and media infrastructure across huge transaction volume.",
        "constraints": ["channel access", "pricing power", "fulfillment intensity"],
        "likely_losers": ["single-channel merchant", "mid-market retailer"],
    },
    "industrial-project-operator": {
        "title": "Industrial Project Operator",
        "business_truth": "This is a project operator business that wins when labor coordination, procurement, compliance, and execution at scale matter more than commodity bid pricing alone.",
        "best_owner_type": "scaled project platform",
        "why_owner_type": "The winners are the operators that can manage labor bottlenecks, bonding capacity, procurement risk, and schedule complexity across large programs.",
        "constraints": ["labor", "capital / rates", "execution risk"],
        "likely_losers": ["small contractor", "under-capitalized bidder"],
    },
    "software-and-network-platform": {
        "title": "Software and Network Platform",
        "business_truth": "This is a software/network platform business that wins when workflows, compute, distribution, or installed-base leverage compound across a large customer system.",
        "best_owner_type": "software-led consolidator",
        "why_owner_type": "Scale matters because product, data, channel, and infrastructure reuse create operating leverage and lock-in.",
        "constraints": ["compute / infrastructure", "compliance / regulation", "platform relevance"],
        "likely_losers": ["point-solution vendor", "subscale network"],
    },
    "branded-food-scale-operator": {
        "title": "Branded Food Scale Operator",
        "business_truth": "This is a branded food and staples operator that wins when procurement, distribution, portfolio mix, and reformulation discipline offset retailer power and changing health preferences.",
        "best_owner_type": "scaled brand portfolio",
        "why_owner_type": "The model works when scale buys procurement resilience and shelf access while portfolio management keeps the company on the right side of consumer change.",
        "constraints": ["procurement / inputs", "consumer preference-driven demand", "channel access"],
        "likely_losers": ["single-product brand", "commodity processor"],
    },
    "industrial-scale-manufacturer": {
        "title": "Industrial Scale Manufacturer",
        "business_truth": "This is a scaled industrial manufacturer that wins when specification, installed base, procurement leverage, and production discipline create defensibility across cyclical end markets.",
        "best_owner_type": "scaled industrial platform",
        "why_owner_type": "The economics favor manufacturers that can spread engineering, sourcing, and capacity planning across many end uses while staying inside mission-critical specs.",
        "constraints": ["procurement / inputs", "capex cycle", "utilization"],
        "likely_losers": ["import-reliant assembler", "subscale producer"],
    },
    "expert-services-platform": {
        "title": "Expert Services Platform",
        "business_truth": "This is an expert-services platform that wins when scarce talent, compliance-heavy delivery, and enterprise trust push buyers toward scaled firms rather than loose independent providers.",
        "best_owner_type": "scaled expert network",
        "why_owner_type": "Talent, client trust, and workflow standardization favor operators that can productize expertise without losing credibility.",
        "constraints": ["talent concentration", "utilization", "client concentration"],
        "likely_losers": ["solo practitioner", "commodity outsourcer"],
    },
    "healthcare-product-and-distribution-platform": {
        "title": "Healthcare Product and Distribution Platform",
        "business_truth": "This is a healthcare supply platform that wins when regulatory know-how, distribution reach, procurement leverage, and clinical product breadth sit between care delivery and manufacturers.",
        "best_owner_type": "scaled healthcare intermediary",
        "why_owner_type": "The winners are the operators that can combine compliance, inventory, contracting, and channel control across fragmented providers and institutional buyers.",
        "constraints": ["compliance / regulation", "pricing power", "channel access"],
        "likely_losers": ["single-line supplier", "independent distributor"],
    },
    "insurance-risk-platform": {
        "title": "Insurance Risk Platform",
        "business_truth": "This is a risk-bearing insurance platform that wins when underwriting data, claims discipline, pricing power, and regulatory navigation scale together.",
        "best_owner_type": "scaled risk manager",
        "why_owner_type": "The economics favor carriers with enough data, capital, and technology to reprice risk and absorb volatility faster than smaller rivals.",
        "constraints": ["regulatory approval", "claims cost inflation", "pricing power"],
        "likely_losers": ["subscale carrier", "rate-constrained niche writer"],
    },
    "transport-and-logistics-network": {
        "title": "Transport and Logistics Network",
        "business_truth": "This is a network logistics business that wins when route density, labor coordination, fleet utilization, and customer integration create operating leverage across a physical network.",
        "best_owner_type": "scaled network operator",
        "why_owner_type": "The winners are the operators that can turn density, labor systems, and service reliability into structural cost and service advantages.",
        "constraints": ["labor", "utilization", "fuel and operating cost"],
        "likely_losers": ["subscale carrier", "spot-market operator"],
    },
    "hospitality-and-experience-platform": {
        "title": "Hospitality and Experience Platform",
        "business_truth": "This is an experience platform that wins when brand, occupancy, distribution, and asset-light operating systems convert travel and leisure demand into repeatable unit economics.",
        "best_owner_type": "asset-light scale operator",
        "why_owner_type": "Scale matters because booking channels, loyalty systems, and brand standards create leverage that independents struggle to match.",
        "constraints": ["occupancy / utilization", "labor", "consumer bifurcation"],
        "likely_losers": ["single-asset owner", "mid-market undifferentiated venue"],
    },
    "scaled-consumer-brand-platform": {
        "title": "Scaled Consumer Brand Platform",
        "business_truth": "This is a scaled consumer products platform that wins when formulation, procurement, shelf access, and portfolio management offset retailer power and changing consumer taste.",
        "best_owner_type": "scaled brand portfolio",
        "why_owner_type": "The model works when scale buys sourcing resilience, distribution clout, and enough portfolio breadth to keep up with consumer shifts.",
        "constraints": ["procurement / inputs", "consumer preference-driven demand", "retailer leverage"],
        "likely_losers": ["single-SKU brand", "commodity producer"],
    },
    "industrial-technology-platform": {
        "title": "Industrial Technology Platform",
        "business_truth": "This is an industrial technology platform that wins when engineering breadth, installed base, aftermarket pull-through, and specification status compound across many end markets.",
        "best_owner_type": "scaled industrial platform",
        "why_owner_type": "The winners are the manufacturers that can spread engineering, service, and sourcing across many categories while holding specification power.",
        "constraints": ["capex cycle", "utilization", "procurement / inputs"],
        "likely_losers": ["subscale OEM", "undifferentiated assembler"],
    },
    "digital-platform-and-software-network": {
        "title": "Digital Platform and Software Network",
        "business_truth": "This is a digital platform or software network that wins when distribution, data, workflow depth, and ecosystem position compound faster than point-solution competition.",
        "best_owner_type": "scaled software/network operator",
        "why_owner_type": "The economics favor platforms that can spread product, data, and distribution across a large installed base and keep users inside the system.",
        "constraints": ["platform relevance", "compute / infrastructure", "customer acquisition cost"],
        "likely_losers": ["subscale app", "feature vendor"],
    },
    "media-rights-and-audience-platform": {
        "title": "Media Rights and Audience Platform",
        "business_truth": "This is a media and audience platform that wins when rights, franchises, distribution, and monetizable attention compound across multiple formats.",
        "best_owner_type": "scaled IP and distribution owner",
        "why_owner_type": "The winners control audience, rights, and distribution instead of renting attention one campaign or one title at a time.",
        "constraints": ["audience retention", "content cost", "distribution leverage"],
        "likely_losers": ["single-format publisher", "subscale content owner"],
    },
    "energy-and-environmental-infrastructure": {
        "title": "Energy and Environmental Infrastructure",
        "business_truth": "This is an infrastructure operator that wins when regulated assets, field-service density, and mission-critical environmental or energy systems create durable demand.",
        "best_owner_type": "scaled infrastructure operator",
        "why_owner_type": "The economics favor operators that can spread compliance, maintenance, and capital intensity across large regulated or mission-critical networks.",
        "constraints": ["regulation", "capital intensity", "field execution"],
        "likely_losers": ["subscale field operator", "commodity service contractor"],
    },
    "industrial-distribution-platform": {
        "title": "Industrial Distribution Platform",
        "business_truth": "This is an industrial distribution platform that wins when inventory, branch density, credit, and technical fulfillment make the middle layer hard to remove.",
        "best_owner_type": "scaled distributor",
        "why_owner_type": "Scale matters because inventory depth, procurement, and local availability are the real moat in fragmented supply chains.",
        "constraints": ["inventory intensity", "pricing power", "service reliability"],
        "likely_losers": ["single-branch wholesaler", "thin-margin reseller"],
    },
    "real-estate-and-facilities-platform": {
        "title": "Real Estate and Facilities Platform",
        "business_truth": "This is a property and facilities platform that wins when asset access, tenant/workflow relationships, and recurring service layers turn real-estate complexity into durable fee streams.",
        "best_owner_type": "scaled property-services operator",
        "why_owner_type": "The winners sit in the workflow around property, occupancy, and facilities rather than relying on one-time transactions.",
        "constraints": ["utilization", "rate sensitivity", "labor"],
        "likely_losers": ["transaction-only intermediary", "single-market operator"],
    },
    "education-and-tutoring-platform": {
        "title": "Education and Tutoring Platform",
        "business_truth": "This is a learning-support platform that wins when trusted curriculum, local or digital distribution, and measurable outcomes turn fragmented tutoring demand into repeatable enrollment.",
        "best_owner_type": "scaled education network",
        "why_owner_type": "The winners combine curriculum, brand trust, and student-acquisition efficiency across many local or digital nodes.",
        "constraints": ["customer acquisition cost", "outcomes credibility", "utilization"],
        "likely_losers": ["independent tutor", "single-site center"],
    },
    "event-and-gifting-commerce-platform": {
        "title": "Event and Gifting Commerce Platform",
        "business_truth": "This is a life-event and gifting commerce platform that wins when discovery, personalization, vendor aggregation, and fulfillment convert episodic demand into a recurring customer-acquisition engine.",
        "best_owner_type": "scaled demand aggregator",
        "why_owner_type": "The economics favor platforms that own discovery and transaction flow in fragmented, emotionally driven purchase categories.",
        "constraints": ["customer acquisition cost", "seasonality", "fulfillment quality"],
        "likely_losers": ["single-store merchant", "transactional local provider"],
    },
    "gaming-and-betting-platform": {
        "title": "Gaming and Betting Platform",
        "business_truth": "This is a digital wagering platform that wins when state access, product engagement, and data-driven customer economics compound across mobile betting and related gaming formats.",
        "best_owner_type": "scaled licensed platform",
        "why_owner_type": "The winners can spread compliance, product development, and customer acquisition across a broad wagering base and multiple regulated states.",
        "constraints": ["regulatory access", "customer acquisition cost", "hold / take rate"],
        "likely_losers": ["subscale operator", "single-state sportsbook"],
    },
    "specialty-retail-platform": {
        "title": "Specialty Retail Platform",
        "business_truth": "This is a specialty retail platform that wins when merchandising, niche demand capture, and channel control matter more than pure scale alone.",
        "best_owner_type": "scaled specialty merchant",
        "why_owner_type": "The winners combine differentiated assortment with enough digital and fulfillment capability to avoid being commoditized by larger generalists.",
        "constraints": ["channel access", "inventory turns", "customer acquisition cost"],
        "likely_losers": ["single-location merchant", "undifferentiated reseller"],
    },
    "workflow-and-advisory-services-platform": {
        "title": "Workflow and Advisory Services Platform",
        "business_truth": "This is a workflow and advisory services platform that wins when expertise, process discipline, and recurring client workflow embed the operator inside a business or institutional system.",
        "best_owner_type": "scaled services platform",
        "why_owner_type": "The model works when trust, workflow repetition, and specialist process matter enough to create sticky client relationships.",
        "constraints": ["talent concentration", "client concentration", "workflow standardization"],
        "likely_losers": ["solo advisory shop", "pure transaction broker"],
    },
    "local-services-and-leisure-platform": {
        "title": "Local Services and Leisure Platform",
        "business_truth": "This is a local services and leisure platform that wins when recurring local demand, route density, bookings, and brand trust convert fragmented activity into repeatable utilization.",
        "best_owner_type": "scaled local operator",
        "why_owner_type": "The winners centralize booking, routing, customer retention, and local brand trust across fragmented service or leisure demand.",
        "constraints": ["labor", "utilization", "local demand density"],
        "likely_losers": ["owner-operator", "single-site leisure venue"],
    },
}

KEYWORD_FORCE_HINTS = {
    "the-channel-shift": [
        "e-commerce",
        "marketplace",
        "omnichannel",
        "delivery",
        "direct to consumer",
        "online",
        "search",
        "app store",
        "digital advertising",
    ],
    "the-compute-super-cycle": [
        "ai",
        "cloud",
        "hosting",
        "data center",
        "compute",
        "semiconductor",
        "software",
        "analytics",
        "storage",
        "network",
    ],
    "the-compliance-tax": [
        "regulatory",
        "compliance",
        "privacy",
        "claims",
        "audit",
        "documentation",
        "security",
        "underwriting",
        "testing",
        "medical waste",
    ],
    "the-great-consolidation": [
        "consolidation",
        "roll-up",
        "scale",
        "m&a",
        "franchise",
        "portfolio",
        "institutional",
    ],
    "the-graying-market": [
        "aging",
        "senior",
        "medicare",
        "elderly",
        "retirement",
        "chronic",
        "vision",
        "caregiver",
    ],
    "the-pricing-power-collapse": [
        "reimbursement",
        "pricing pressure",
        "rate pressure",
        "price competition",
        "rate cuts",
        "payer",
        "margin compression",
    ],
    "the-margin-vise": [
        "input costs",
        "cost inflation",
        "tariff",
        "commodity",
        "freight",
        "wage pressure",
        "thin margins",
    ],
    "the-labor-squeeze": [
        "labor shortage",
        "staffing",
        "wage",
        "driver",
        "hiring",
        "skilled trades",
        "workforce",
    ],
    "the-hollow-middle": [
        "premiumization",
        "trade-down",
        "value",
        "mid-market",
        "consumer bifurcation",
        "discounting",
        "luxury",
    ],
    "the-health-reckoning": [
        "glp-1",
        "health consciousness",
        "low calorie",
        "functional",
        "sugar",
        "wellness",
        "sober curious",
    ],
    "the-real-estate-reckoning": [
        "occupancy",
        "hotel",
        "leasing",
        "property",
        "real estate",
        "rent",
        "office",
        "construction",
    ],
    "money-gets-unbundled": [
        "payments",
        "banking",
        "brokerage",
        "wealth",
        "asset management",
        "credit card",
        "fintech",
        "insurance",
    ],
    "atoms-strike-back": [
        "reshoring",
        "nearshoring",
        "manufacturing",
        "industrial",
        "supply chain",
        "equipment",
        "factory",
        "tariffs",
    ],
    "the-fractional-worker": [
        "outsourcing",
        "consulting",
        "bpo",
        "recruiting",
        "staffing",
        "expert network",
        "professional employer",
    ],
}

CLUSTER_SCORE_BIAS = {
    "omnichannel-scale-retailer": 1,
    "regulated-workflow-infrastructure": 1,
    "insurance-risk-platform": 1,
    "industrial-distribution-platform": 1,
    "digital-platform-and-software-network": 1,
    "software-and-network-platform": 1,
    "healthcare-product-and-distribution-platform": 0,
    "expert-services-platform": 0,
    "transport-and-logistics-network": 0,
    "industrial-project-operator": 0,
    "industrial-technology-platform": 0,
    "scaled-consumer-brand-platform": 0,
    "energy-and-environmental-infrastructure": 0,
    "real-estate-and-facilities-platform": 0,
    "hospitality-and-experience-platform": -1,
    "branded-food-scale-operator": -1,
    "niche-food-brand-producer": -1,
    "education-and-tutoring-platform": 0,
    "event-and-gifting-commerce-platform": 0,
    "gaming-and-betting-platform": 0,
    "specialty-retail-platform": 0,
    "workflow-and-advisory-services-platform": 0,
    "local-services-and-leisure-platform": 0,
}

CLUSTER_FORCE_BONUS = {
    "omnichannel-scale-retailer": {
        "positive": {"the-channel-shift", "the-great-consolidation", "the-compute-super-cycle"},
        "negative": {"the-hollow-middle", "the-pricing-power-collapse"},
    },
    "transport-and-logistics-network": {
        "positive": {"the-channel-shift", "the-great-consolidation", "the-compute-super-cycle"},
        "negative": {"the-labor-squeeze", "the-margin-vise"},
    },
    "hospitality-and-experience-platform": {
        "positive": {"the-experience-economy", "the-graying-market"},
        "negative": {"the-hollow-middle", "the-labor-squeeze", "the-real-estate-reckoning"},
    },
    "healthcare-product-and-distribution-platform": {
        "positive": {"the-graying-market", "the-compliance-tax", "the-great-consolidation"},
        "negative": {"the-pricing-power-collapse", "the-labor-squeeze"},
    },
    "insurance-risk-platform": {
        "positive": {"money-gets-unbundled", "the-compliance-tax", "the-great-consolidation"},
        "negative": {"the-pricing-power-collapse"},
    },
    "industrial-distribution-platform": {
        "positive": {"the-great-consolidation", "the-compute-super-cycle", "money-gets-unbundled"},
        "negative": {"the-margin-vise", "the-labor-squeeze"},
    },
    "industrial-technology-platform": {
        "positive": {"atoms-strike-back", "the-compute-super-cycle", "the-great-consolidation"},
        "negative": {"the-margin-vise", "the-pricing-power-collapse"},
    },
    "scaled-consumer-brand-platform": {
        "positive": {"the-graying-market", "the-channel-shift"},
        "negative": {"the-health-reckoning", "the-margin-vise", "the-hollow-middle"},
    },
    "branded-food-scale-operator": {
        "positive": {"the-channel-shift", "the-great-consolidation"},
        "negative": {"the-health-reckoning", "the-margin-vise", "the-labor-squeeze"},
    },
    "media-rights-and-audience-platform": {
        "positive": {"the-channel-shift", "the-great-consolidation", "the-experience-economy"},
        "negative": {"the-hollow-middle"},
    },
    "education-and-tutoring-platform": {
        "positive": {"the-channel-shift", "the-compute-super-cycle", "the-great-consolidation"},
        "negative": {"the-hollow-middle"},
    },
    "event-and-gifting-commerce-platform": {
        "positive": {"the-channel-shift", "the-compute-super-cycle"},
        "negative": {"the-hollow-middle", "the-margin-vise"},
    },
    "gaming-and-betting-platform": {
        "positive": {"the-channel-shift", "the-compute-super-cycle", "the-compliance-tax"},
        "negative": {"the-hollow-middle"},
    },
    "specialty-retail-platform": {
        "positive": {"the-channel-shift", "the-compute-super-cycle"},
        "negative": {"the-hollow-middle", "the-margin-vise"},
    },
    "workflow-and-advisory-services-platform": {
        "positive": {"the-compliance-tax", "the-fractional-worker", "the-great-consolidation"},
        "negative": {"the-pricing-power-collapse"},
    },
    "local-services-and-leisure-platform": {
        "positive": {"the-great-consolidation", "the-channel-shift"},
        "negative": {"the-labor-squeeze", "the-hollow-middle"},
    },
    "digital-platform-and-software-network": {
        "positive": {"the-channel-shift", "the-compute-super-cycle", "the-great-consolidation"},
        "negative": {"the-pricing-power-collapse"},
    },
    "software-and-network-platform": {
        "positive": {"the-channel-shift", "the-compute-super-cycle", "the-compliance-tax"},
        "negative": {"the-pricing-power-collapse"},
    },
}

CSS = """
:root{--bg:#101318;--panel:#171d24;--panel2:#1d2630;--line:#2a3440;--ink:#f0eadc;--muted:#a9b2bd;--faint:#74808d;--gold:#d4ad55;--green:#71c58b;--red:#df806e;--amber:#d9a441;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1220px;margin:0 auto;padding:30px clamp(16px,4vw,40px) 72px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:34px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.2rem,5vw,4rem);line-height:1;margin:.18em 0 .22em}.sub{max-width:900px;color:var(--muted);font-size:1.07rem}.strip{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0 0}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:130px}.kpi .n{font-family:var(--mono);font-size:1.3rem;font-weight:700}.kpi .l{font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:var(--faint);margin-top:1px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:14px}.card,.panel,.brief,.force{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3,.panel h2,.brief h3,.force h3{margin:.2em 0 .35em}.card p,.panel p,.brief p,.force p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.stats{display:flex;flex-wrap:wrap;gap:8px;margin-top:10px}.stats span{font-family:var(--mono);font-size:.72rem;background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(280px,.9fr);gap:18px;margin-top:26px}.stack>*+*{margin-top:12px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.4em 0}.status{display:inline-flex;align-items:center;gap:8px;font-family:var(--mono);font-size:.72rem;padding:5px 9px;border-radius:999px;border:1px solid var(--line);margin-top:10px}.status.advantaged{color:var(--green)}.status.mixed{color:var(--amber)}.status.exposed{color:var(--red)}table{width:100%;border-collapse:collapse;margin-top:10px}th,td{text-align:left;padding:10px 0;border-bottom:1px solid var(--line);vertical-align:top}th{font-family:var(--mono);font-size:.7rem;color:var(--faint);text-transform:uppercase;letter-spacing:.08em}.small{font-size:.92rem;color:var(--muted)}@media(max-width:920px){.split{grid-template-columns:1fr}}footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);color:var(--faint);font-family:var(--mono);font-size:.72rem}
"""


def e(value: Any) -> str:
    return html.escape(str(value or ""), quote=True)


def slugify(value: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return value or "company"


def parse_player_name(item: Any) -> str | None:
    if isinstance(item, dict):
        name = item.get("name")
        return str(name).strip() if name else None
    if not isinstance(item, str):
        return None
    raw = item.strip().strip("\"'").lstrip("-* ").strip()
    lower = raw.lower()
    if not raw or any(lower.startswith(prefix) for prefix in SKIP_PREFIXES):
        return None
    if raw.startswith("{") and "'name'" in raw:
        try:
            parsed = ast.literal_eval(raw)
            if isinstance(parsed, dict) and parsed.get("name"):
                return str(parsed["name"]).strip()
        except Exception:
            pass
    parts = re.split(r"\s+[—–-]\s+|\s+\(|:\s+|,\s+(?=[A-Z$])", raw, maxsplit=1)
    name = parts[0].strip()
    name = re.sub(r"\s+", " ", name).strip(" .;:")
    if name.lower() in SKIP_EXACT:
        return None
    if len(name) < 2 or len(name) > 80:
        return None
    return name


def normalize_key(name: str) -> str:
    key = name.lower().replace("&", " and ")
    key = re.sub(r"[^a-z0-9\s']", " ", key)
    tokens = [token for token in key.split() if token]
    while tokens and tokens[-1] in CORP_SUFFIXES:
        tokens.pop()
    key = " ".join(tokens).strip()
    key = NORMALIZATION_OVERRIDES.get(key, key)
    return key


def collect_force_evidence() -> dict[str, set[str]]:
    evidence: dict[str, set[str]] = defaultdict(set)
    for domain in TAXONOMY["domains"]:
        for force in domain["forces"]:
            for group in force["groups"]:
                for subforce in group["subforces"]:
                    evidence[force["slug"]].update(subforce.get("evidence_slugs", []))
    return evidence


FORCE_EVIDENCE = collect_force_evidence()


def brief_card(brief: dict[str, Any]) -> str:
    themes = "".join(f'<span class="chip">{e(theme)}</span>' for theme in brief.get("themes", [])[:4])
    return f"""<article class="brief">
  <div class="meta">{e(brief.get('sector'))}</div>
  <h3>{e(brief.get('title'))}</h3>
  <p>{e(brief.get('one_sentence') or brief.get('one_liner'))}</p>
  <div class="stats"><span>{e(brief.get('key_stats', {}).get('market_size') or 'n/a')}</span><span>{e(brief.get('key_stats', {}).get('growth') or 'n/a')}</span></div>
  <div class="chips">{themes}</div>
</article>"""


def company_status(score: int) -> str:
    if score >= 5:
        return "advantaged"
    if score <= -3:
        return "exposed"
    return "mixed"


def contains_any(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def status_label(status: str) -> str:
    return {
        "advantaged": "Advantaged",
        "mixed": "Mixed",
        "exposed": "Exposed",
    }[status]


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


def build_force_theme_map() -> dict[str, list[dict[str, Any]]]:
    mapping: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for theme in AMERICAN_THEMES:
        for force in theme.get("forces", []):
            mapping[force["slug"]].append(theme)
    return mapping


def dedupe_themes(themes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    seen = set()
    for theme in themes:
        if theme["slug"] in seen:
            continue
        seen.add(theme["slug"])
        out.append(theme)
    return out


FORCE_THEME_MAP = build_force_theme_map()


def collect_company_themes(
    industries: list[str],
    theme_counts: Counter[str],
    sector_mix: list[tuple[str, int]],
    force_scores: Counter[str],
) -> list[dict[str, Any]]:
    candidate_themes = []
    for force_slug, _score in force_scores.most_common(5):
        candidate_themes.extend(FORCE_THEME_MAP.get(force_slug, []))
    themes = dedupe_themes(candidate_themes)
    record_theme_terms = {item.lower() for item in theme_counts}
    sector_count_map = {sector.lower(): count for sector, count in sector_mix}
    scored = []
    for theme in themes:
        overlap = sum(force_scores.get(force["slug"], 0) for force in theme.get("forces", []))
        subtheme_hits = 0
        sector_hits = 0
        for subtheme in theme.get("subthemes", []):
            title = subtheme.get("title", "").lower()
            microthemes = [item.lower() for item in subtheme.get("microthemes", [])]
            for term in record_theme_terms:
                if term and (term in title or any(term in item for item in microthemes)):
                    subtheme_hits += 1
            for industry in subtheme.get("industries", []):
                sector = industry.get("sector", "").lower()
                if sector:
                    sector_hits += sector_count_map.get(sector, 0)
        scored.append((overlap, subtheme_hits, sector_hits, theme.get("signal_count", 0), theme))
    scored.sort(key=lambda item: (item[0], item[1], item[2], item[3]), reverse=True)
    return [item[4] for item in scored[:5]]


def build_theme_scorecard(themes: list[dict[str, Any]]) -> dict[str, int]:
    scorecard = {}
    for index, theme in enumerate(themes):
        base = max(1, 3 - index)
        if theme["slug"] in POSITIVE_THEME_SLUGS:
            scorecard[theme["slug"]] = base
        elif theme["slug"] in NEGATIVE_THEME_SLUGS:
            scorecard[theme["slug"]] = -base
        else:
            scorecard[theme["slug"]] = 0
    return scorecard


def build_company_records() -> list[dict[str, Any]]:
    raw_companies: dict[str, dict[str, Any]] = {}
    for brief in BRIEFS:
        for item in brief.get("major_players") or []:
            parsed = parse_player_name(item)
            if not parsed:
                continue
            key = normalize_key(parsed)
            if not key:
                continue
            record = raw_companies.setdefault(
                key,
                {
                    "key": key,
                    "display_names": Counter(),
                    "industry_counts": Counter(),
                    "sector_counts": Counter(),
                    "theme_counts": Counter(),
                    "mentions": [],
                },
            )
            record["display_names"][parsed] += 1
            record["industry_counts"][brief["slug"]] += 1
            record["sector_counts"][brief["sector"]] += 1
            record["theme_counts"].update(brief.get("themes", []))
            record["mentions"].append({"industry_slug": brief["slug"], "raw": item})

    records: list[dict[str, Any]] = []
    for key, company in raw_companies.items():
        industries = list(company["industry_counts"].keys())
        sector_mix = company["sector_counts"].most_common()
        lens_scores = Counter()
        force_scores = Counter()
        theme_blob = " | ".join(company["theme_counts"].keys()).lower()
        industry_blob = " | ".join(BRIEFS_BY_SLUG[slug]["title"] for slug in industries if slug in BRIEFS_BY_SLUG).lower()
        for lens in LENSES:
            evidence = set(lens.get("evidence_industry_slugs", []))
            adjacent = set(lens.get("adjacent_industry_slugs", []))
            primary = {lens.get("primary_industry_slug")}
            overlap_evidence = len(evidence.intersection(industries))
            overlap_adjacent = len(adjacent.intersection(industries))
            overlap_primary = len(primary.intersection(industries))
            score = overlap_primary * 4 + overlap_evidence * 3 + overlap_adjacent * 2
            if score:
                lens_scores[lens["slug"]] += score
        for force_slug, evidence_slugs in FORCE_EVIDENCE.items():
            overlap = len(evidence_slugs.intersection(industries))
            if overlap:
                force_scores[force_slug] += overlap
        for force_slug, needles in KEYWORD_FORCE_HINTS.items():
            keyword_hits = sum(1 for needle in needles if needle in theme_blob or needle in industry_blob)
            if keyword_hits:
                force_scores[force_slug] += 1

        dominant_lens_slug = None
        if lens_scores:
            top_lenses = lens_scores.most_common(2)
            top_slug, top_score = top_lenses[0]
            second_score = top_lenses[1][1] if len(top_lenses) > 1 else 0
            if top_score >= 4 and top_score >= second_score + 2:
                dominant_lens_slug = top_slug
        dominant_lens = LENSES_BY_SLUG.get(dominant_lens_slug) if dominant_lens_slug else None
        top_sector = sector_mix[0][0] if sector_mix else None
        dominant_force_slugs = [force_slug for force_slug, _score in force_scores.most_common(3)]
        pseudo_cluster_slug = None
        if not dominant_lens and top_sector == "Retail" and "the-channel-shift" in dominant_force_slugs:
            pseudo_cluster_slug = "omnichannel-scale-retailer"
        elif not dominant_lens and top_sector == "Construction" and any(
            slug in dominant_force_slugs
            for slug in ("the-real-estate-reckoning", "the-labor-squeeze", "the-compute-super-cycle", "atoms-strike-back")
        ):
            pseudo_cluster_slug = "industrial-project-operator"
        elif not dominant_lens and top_sector == "Technology & Digital" and any(
            slug in dominant_force_slugs
            for slug in ("the-compute-super-cycle", "the-compliance-tax", "the-fractional-worker", "the-channel-shift")
        ):
            pseudo_cluster_slug = "software-and-network-platform"
        elif not dominant_lens and top_sector in {"Food & Drink", "Agriculture"} and any(
            slug in dominant_force_slugs
            for slug in ("the-health-reckoning", "the-margin-vise", "atoms-strike-back")
        ):
            pseudo_cluster_slug = "branded-food-scale-operator"
        elif not dominant_lens and top_sector == "Manufacturing" and any(
            slug in dominant_force_slugs for slug in ("atoms-strike-back", "the-compute-super-cycle", "the-great-consolidation")
        ):
            pseudo_cluster_slug = "industrial-scale-manufacturer"
        elif not dominant_lens and top_sector == "Business Services" and any(
            slug in dominant_force_slugs for slug in ("the-fractional-worker", "the-compliance-tax", "the-great-consolidation")
        ):
            pseudo_cluster_slug = "expert-services-platform"
        elif not dominant_lens and top_sector == "Healthcare" and (
            any(slug in dominant_force_slugs for slug in ("the-compliance-tax", "the-pricing-power-collapse", "the-graying-market"))
            or contains_any(industry_blob, ["medical", "pharmacy", "diagnostic", "surgical", "hospital", "care", "device"])
        ):
            pseudo_cluster_slug = "healthcare-product-and-distribution-platform"
        elif not dominant_lens and top_sector == "Finance & Insurance" and (
            any(slug in dominant_force_slugs for slug in ("money-gets-unbundled", "the-compliance-tax"))
            or contains_any(industry_blob, ["insurance", "bank", "broker", "asset", "investment", "credit", "trust"])
        ):
            pseudo_cluster_slug = "insurance-risk-platform"
        elif not dominant_lens and top_sector == "Transport & Logistics" and (
            any(slug in dominant_force_slugs for slug in ("the-labor-squeeze", "the-fractional-worker", "the-compute-super-cycle"))
            or contains_any(industry_blob, ["trucking", "freight", "delivery", "logistics", "rail", "airlines", "transport"])
        ):
            pseudo_cluster_slug = "transport-and-logistics-network"
        elif not dominant_lens and top_sector == "Consumer Services" and (
            any(slug in dominant_force_slugs for slug in ("the-hollow-middle", "the-real-estate-reckoning", "the-labor-squeeze"))
            or contains_any(industry_blob, ["hotel", "casino", "travel", "spa", "funeral", "vacation", "rental", "tourism"])
        ):
            pseudo_cluster_slug = "hospitality-and-experience-platform"
        elif not dominant_lens and contains_any(
            industry_blob, ["tutoring", "after-school", "test preparation", "learning center", "online tutoring"]
        ):
            pseudo_cluster_slug = "education-and-tutoring-platform"
        elif not dominant_lens and contains_any(
            industry_blob, ["greeting card", "flower", "gift shop", "photo printing", "wedding", "party", "event planner"]
        ):
            pseudo_cluster_slug = "event-and-gifting-commerce-platform"
        elif not dominant_lens and contains_any(
            industry_blob, ["gambling", "fantasy sports", "sportsbook", "betting"]
        ):
            pseudo_cluster_slug = "gaming-and-betting-platform"
        elif not dominant_lens and top_sector in {"Food & Drink", "Agriculture"}:
            pseudo_cluster_slug = "scaled-consumer-brand-platform"
        elif not dominant_lens and top_sector == "Manufacturing" and (
            contains_any(theme_blob, ["tariff", "automation", "aftermarket", "installed base", "reshoring", "premium", "supply chain", "regulatory"])
            or contains_any(industry_blob, ["manufacturing", "equipment", "machinery", "industrial", "medical", "appliance", "paper", "chemical"])
        ):
            pseudo_cluster_slug = "industrial-technology-platform"
        elif not dominant_lens and contains_any(
            industry_blob, ["hotel", "extended stay", "boutique hotel"]
        ):
            pseudo_cluster_slug = "hospitality-and-experience-platform"
        elif not dominant_lens and contains_any(
            industry_blob, ["beer", "breweries", "spirits", "liquor"]
        ):
            pseudo_cluster_slug = "branded-food-scale-operator"
        elif not dominant_lens and top_sector == "Retail" and contains_any(
            industry_blob, ["drug store", "pharmacies", "optical", "pet", "furniture", "sporting goods", "hardware", "grocery"]
        ):
            pseudo_cluster_slug = "omnichannel-scale-retailer"
        elif not dominant_lens and top_sector == "Technology & Digital" and (
            contains_any(industry_blob, ["software", "search", "payment", "game", "digital advertising", "hosting", "analytics", "platform", "network"])
            or contains_any(theme_blob, ["ai", "cloud", "platform", "digital", "automation", "data"])
        ):
            pseudo_cluster_slug = "digital-platform-and-software-network"
        elif not dominant_lens and top_sector == "Media & Entertainment" and (
            contains_any(industry_blob, ["movie", "television", "cable", "book", "publishing", "concert", "advertising", "casino", "stream", "media"])
            or any(slug in dominant_force_slugs for slug in ("the-hollow-middle", "the-great-consolidation", "the-graying-market"))
        ):
            pseudo_cluster_slug = "media-rights-and-audience-platform"
        elif not dominant_lens and top_sector == "Energy & Environment" and (
            contains_any(industry_blob, ["waste", "power", "pipeline", "oil", "gas", "solar", "wind", "water", "mining", "environmental"])
            or any(slug in dominant_force_slugs for slug in ("the-compute-super-cycle", "the-compliance-tax", "the-great-consolidation"))
        ):
            pseudo_cluster_slug = "energy-and-environmental-infrastructure"
        elif not dominant_lens and top_sector == "Business Services" and (
            contains_any(industry_blob, ["wholesaling", "distributors", "industrial supplies", "logistics", "equipment", "safety", "plumbing", "hardware"])
            or contains_any(theme_blob, ["inventory", "distribution", "branch", "fulfillment"])
        ):
            pseudo_cluster_slug = "industrial-distribution-platform"
        elif not dominant_lens and top_sector in {"Real Estate", "Business Services"} and (
            contains_any(industry_blob, ["real estate", "leasing", "appraisal", "facilities", "building", "property", "storage"])
            or any(slug in dominant_force_slugs for slug in ("the-real-estate-reckoning", "the-great-consolidation"))
        ):
            pseudo_cluster_slug = "real-estate-and-facilities-platform"
        elif not dominant_lens and top_sector == "Construction" and contains_any(
            industry_blob, ["rental", "contracting", "construction", "engineering", "building", "scaffolding", "highway", "demolition"]
        ):
            pseudo_cluster_slug = "industrial-project-operator"
        elif not dominant_lens and top_sector == "Consumer Services":
            pseudo_cluster_slug = "local-services-and-leisure-platform"
        elif not dominant_lens and top_sector == "Retail":
            pseudo_cluster_slug = "specialty-retail-platform"
        elif not dominant_lens and top_sector == "Business Services":
            pseudo_cluster_slug = "workflow-and-advisory-services-platform"
        elif not dominant_lens and top_sector == "Media & Entertainment":
            pseudo_cluster_slug = "media-rights-and-audience-platform"
        elif not dominant_lens and top_sector == "Healthcare":
            pseudo_cluster_slug = "healthcare-product-and-distribution-platform"
        elif not dominant_lens and top_sector == "Manufacturing":
            pseudo_cluster_slug = "industrial-technology-platform"
        elif not dominant_lens and top_sector == "Transport & Logistics":
            pseudo_cluster_slug = "transport-and-logistics-network"
        elif not dominant_lens and top_sector == "Construction":
            pseudo_cluster_slug = "industrial-project-operator"
        elif not dominant_lens and top_sector == "Technology & Digital":
            pseudo_cluster_slug = "digital-platform-and-software-network"
        elif not dominant_lens and top_sector == "Real Estate":
            pseudo_cluster_slug = "real-estate-and-facilities-platform"
        elif not dominant_lens and top_sector == "Finance & Insurance":
            pseudo_cluster_slug = "insurance-risk-platform"
        elif not dominant_lens and top_sector == "Energy & Environment":
            pseudo_cluster_slug = "energy-and-environmental-infrastructure"
        if dominant_lens:
            for force_slug in dominant_lens.get("primary_force_slugs", []):
                force_scores[force_slug] += 2

        dominant_theme_objects = collect_company_themes(industries, company["theme_counts"], sector_mix, force_scores)
        theme_scorecard = build_theme_scorecard(dominant_theme_objects)
        positive_theme_score = sum(value for value in theme_scorecard.values() if value > 0)
        negative_theme_score = sum(-value for value in theme_scorecard.values() if value < 0)
        theme_tailwind_score = max(-2, min(2, positive_theme_score - negative_theme_score))

        positive_score = sum(force_scores[slug] for slug in POSITIVE_FORCE_SLUGS if slug in force_scores)
        negative_score = sum(force_scores[slug] for slug in NEGATIVE_FORCE_SLUGS if slug in force_scores)
        structural_bonus = 1 if dominant_lens and dominant_lens["best_owner_type"] in FAVORABLE_OWNER_TYPES else 0
        scale_bonus = 1 if len(industries) >= 4 else 0
        cluster_for_bias = dominant_lens_slug or pseudo_cluster_slug
        cluster_bias = CLUSTER_SCORE_BIAS.get(cluster_for_bias, 0)
        cluster_force_bonus = 0
        cluster_force_config = CLUSTER_FORCE_BONUS.get(cluster_for_bias)
        if cluster_force_config:
            for force_slug, value in force_scores.items():
                if force_slug in cluster_force_config["positive"]:
                    cluster_force_bonus += min(2, value)
                if force_slug in cluster_force_config["negative"]:
                    cluster_force_bonus -= min(2, value)
        rating_score = (
            positive_score
            - negative_score
            + structural_bonus
            + scale_bonus
            + cluster_bias
            + cluster_force_bonus
            + theme_tailwind_score
        )
        status = company_status(rating_score)

        dominant_force_records = []
        for force_slug, _score in force_scores.most_common(3):
            force = FORCES_BY_SLUG.get(force_slug)
            if not force:
                continue
            dominant_force_records.append(
                {
                    "slug": force_slug,
                    "title": force["title"],
                    "demand_logic": force["demand_logic"],
                    "margin_logic": force["margin_logic"],
                }
            )

        display_name = company["display_names"].most_common(1)[0][0]
        title = display_name
        if dominant_lens:
            lens_title = dominant_lens["title"]
            best_owner = dominant_lens["best_owner_type"]
            business_truth = dominant_lens["business_truth"]
            why_owner = dominant_lens["why_this_owner_type"]
            constraints = dominant_lens["binding_constraints"]
            likely_losers = dominant_lens["likely_losers"]
            cluster_slug = dominant_lens_slug
            business_truth = MODELLINE.get(cluster_slug, business_truth)
        elif pseudo_cluster_slug:
            pseudo = PSEUDO_CLUSTER_CONFIG[pseudo_cluster_slug]
            lens_title = pseudo["title"]
            best_owner = pseudo["best_owner_type"]
            business_truth = pseudo["business_truth"]
            why_owner = pseudo["why_owner_type"]
            constraints = pseudo["constraints"]
            likely_losers = pseudo["likely_losers"]
            cluster_slug = pseudo_cluster_slug
            business_truth = MODELLINE.get(cluster_slug, business_truth)
        else:
            lens_title = "Unassigned"
            best_owner = "mixed / case-specific"
            business_truth = "This operator appears across the corpus but does not yet map cleanly into a single business archetype."
            why_owner = "The company spans too many models to reduce to one ownership pattern."
            constraints = []
            likely_losers = []
            cluster_slug = None

        industry_rows = []
        for industry_slug, count in company["industry_counts"].most_common(6):
            brief = BRIEFS_BY_SLUG[industry_slug]
            industry_rows.append(
                {
                    "slug": industry_slug,
                    "title": brief["title"],
                    "sector": brief["sector"],
                    "mentions": count,
                    "one_sentence": brief.get("one_sentence") or brief.get("one_liner"),
                }
            )

        records.append(
            {
                "slug": slugify(key),
                "company_key": key,
                "title": title,
                "mention_count": sum(company["industry_counts"].values()),
                "industry_count": len(company["industry_counts"]),
                "sector_count": len(company["sector_counts"]),
                "sector_mix": [{"sector": sector, "count": count} for sector, count in sector_mix[:4]],
                "top_themes": [theme for theme, _count in company["theme_counts"].most_common(6)],
                "dominant_theme_objects": [
                    {
                        "slug": theme["slug"],
                        "title": theme["title"],
                        "lens": theme["lens"],
                        "score": theme_scorecard.get(theme["slug"], 0),
                        "subthemes": [
                            {
                                "slug": subtheme["slug"],
                                "title": subtheme["title"],
                            }
                            for subtheme in theme.get("subthemes", [])[:3]
                        ],
                    }
                    for theme in dominant_theme_objects
                ],
                "business_model_cluster_slug": cluster_slug,
                "business_model_cluster_title": lens_title,
                "business_truth": business_truth,
                "best_owner_type": best_owner,
                "why_owner_type": why_owner,
                "constraints": constraints,
                "likely_losers": likely_losers,
                "dominant_forces": dominant_force_records,
                "force_scorecard": dict(force_scores.most_common()),
                "theme_scorecard": theme_scorecard,
                "theme_tailwind_score": theme_tailwind_score,
                "rating_score": rating_score,
                "status": status,
                "industry_rows": industry_rows,
                "page": len(company["industry_counts"]) >= 3 and sum(company["industry_counts"].values()) >= 4,
            }
        )

    records.sort(key=lambda row: (-row["mention_count"], -row["industry_count"], row["title"]))
    return records


def build_cluster_records(companies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for company in companies:
        grouped[company["business_model_cluster_slug"] or "unassigned"].append(company)

    records = []
    for slug, members in grouped.items():
        lens = LENSES_BY_SLUG.get(slug)
        if lens:
            title = lens["title"]
            thesis = lens["business_truth"]
            owner = lens["best_owner_type"]
        elif slug in PSEUDO_CLUSTER_CONFIG:
            pseudo = PSEUDO_CLUSTER_CONFIG[slug]
            title = pseudo["title"]
            thesis = pseudo["business_truth"]
            owner = pseudo["best_owner_type"]
        else:
            title = "Unassigned"
            thesis = "These companies span too many models to slot neatly into one existing business lens."
            owner = "mixed / case-specific"
        status_counts = Counter(member["status"] for member in members)
        top_companies = [
            {
                "slug": member["slug"],
                "title": member["title"],
                "mention_count": member["mention_count"],
                "status": member["status"],
            }
            for member in sorted(members, key=lambda row: (-row["mention_count"], row["title"]))[:8]
        ]
        force_counts = Counter()
        constraint_counts = Counter()
        for member in members:
            for force in member["dominant_forces"]:
                force_counts[force["title"]] += 1
            for constraint in member.get("constraints", []):
                constraint_counts[constraint] += 1
        records.append(
            {
                "slug": slug,
                "title": title,
                "thesis": thesis,
                "best_owner_type": owner,
                "company_count": len(members),
                "advantaged_count": status_counts["advantaged"],
                "mixed_count": status_counts["mixed"],
                "exposed_count": status_counts["exposed"],
                "top_forces": [title for title, _count in force_counts.most_common(4)],
                "top_constraints": [title for title, _count in constraint_counts.most_common(4)],
                "top_companies": top_companies,
            }
        )
    records.sort(key=lambda row: (-row["company_count"], row["title"]))
    return records


def build_universe_page(companies: list[dict[str, Any]]) -> str:
    top_companies = [company for company in companies if company["page"]][:60]
    cards = "\n".join(
        f"""<article class="card">
  <div class="meta">{e(company['business_model_cluster_title'])}</div>
  <h3><a href="company-pages/{e(company['slug'])}.html">{e(company['title'])}</a></h3>
  <p>{e(company['business_truth'])}</p>
  <div class="status {e(company['status'])}">{e(status_label(company['status']))}</div>
  <div class="stats"><span>{company['mention_count']} corpus mentions</span><span>{company['industry_count']} industries</span><span>{e(company['best_owner_type'])}</span></div>
  <div class="meta" style="margin-top:14px">Where it shows up</div>
  <div class="chips">{''.join(f'<span class="chip">{e(item["sector"])}</span>' for item in company['sector_mix'][:4])}</div>
  <div class="meta" style="margin-top:14px">Signals</div>
  <div class="chips">{''.join(f'<span class="chip">{e(force["title"])}</span>' for force in company['dominant_forces'][:3])}</div>
  <div class="meta" style="margin-top:14px">What to do</div>
  <p>{e(company['why_owner_type'])}</p>
  <div class="meta" style="margin-top:14px">What to underwrite</div>
  <p class="small">{e('The key question is whether ' + company['title'] + ' can stay on the right side of ' + ', '.join(company['constraints'][:3]) + ' while preserving its ' + company['business_model_cluster_title'].lower() + ' position.')}</p>
  <div class="meta" style="margin-top:14px">Tensions</div>
  <p class="small">{e(company['title'] + ' has to preserve its current edge while ' + ', '.join(company['constraints'][:2]) + ' keep tightening around the cluster.')}</p>
  <div class="meta" style="margin-top:14px">Second-order effects</div>
  <p class="small">{e('If this read holds, adjacent sectors like ' + ', '.join(item['sector'] for item in company['sector_mix'][:2]) + ' will likely reprice around the same workflow and owner-type logic.')}</p>
</article>"""
        for company in top_companies
    )

    table_rows = "\n".join(
        f"""<tr>
  <td><a href="company-pages/{e(company['slug'])}.html">{e(company['title'])}</a></td>
  <td>{e(company['business_model_cluster_title'])}</td>
  <td>{company['mention_count']}</td>
  <td>{company['industry_count']}</td>
  <td>{e(status_label(company['status']))}</td>
</tr>"""
        for company in top_companies[:25]
    )

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company Universe — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="business-profiles.html">Business profiles</a><a href="company-clusters.html">Company clusters</a></div>
<div class="eyebrow">Company universe · US · 2025–2026</div>
<h1>Company Universe</h1>
<p class="sub">This layer aggregates named operators from the 1,491-industry corpus, maps them back into the business-lens and force system, and turns scattered company mentions into a usable operator/investor surface.</p>
<div class="strip">
  <div class="kpi"><div class="n">{len(companies)}</div><div class="l">Companies extracted</div></div>
  <div class="kpi"><div class="n">{sum(1 for company in companies if company['page'])}</div><div class="l">Detailed pages</div></div>
  <div class="kpi"><div class="n">{len({company['business_model_cluster_slug'] for company in companies if company['business_model_cluster_slug']})}</div><div class="l">Mapped clusters</div></div>
  <div class="kpi"><div class="n">{sum(company['mention_count'] for company in companies)}</div><div class="l">Player mentions</div></div>
</div>
<div class="panel" style="margin-top:24px">
  <div class="meta">How to use it</div>
  <p>This page is the named-operator entry point into the synthesis system. Use it to see which companies recur most, where they show up, which force mix governs them, and what kind of operator or investor question the corpus is really asking about them.</p>
</div>

<section class="section">
  <h2>Most Recurrent Operators</h2>
  <div class="grid">{cards}</div>
</section>

<section class="section">
  <h2>Quick Table</h2>
  <div class="panel">
    <table>
      <thead><tr><th>Company</th><th>Cluster</th><th>Mentions</th><th>Industries</th><th>Read</th></tr></thead>
      <tbody>{table_rows}</tbody>
    </table>
  </div>
</section>

<footer>Built from `major_players` across the completed industry corpus, then mapped into the existing company/business interpretation framework.</footer>
</div></body></html>"""


def build_clusters_page(clusters: list[dict[str, Any]]) -> str:
    cards = "\n".join(
        f"""<article class="card">
  <div class="meta">{e(cluster['best_owner_type'])}</div>
  <h3>{e(cluster['title'])}</h3>
  <p>{e(MODELLINE.get(cluster['slug'], cluster['thesis']))}</p>
  <div class="stats"><span>{cluster['company_count']} companies</span><span>{cluster['advantaged_count']} advantaged</span><span>{cluster['exposed_count']} exposed</span></div>
  <div class="meta" style="margin-top:14px">Signals</div>
  <div class="chips">{''.join(f'<span class="chip">{e(force)}</span>' for force in cluster['top_forces'])}</div>
  <div class="meta" style="margin-top:14px">Where it shows up</div>
  <div class="chips">{''.join(f'<span class="chip">{e(item["title"])}</span>' for item in cluster['top_companies'][:4])}</div>
  <div class="meta" style="margin-top:14px">What to do</div>
  <p>{e('This cluster usually rewards ' + cluster['best_owner_type'] + ' behavior rather than generic participation in the category.')}</p>
  <div class="meta" style="margin-top:14px">What to underwrite</div>
  <p class="small">{e('The real question is whether the apparent leaders in ' + cluster['title'] + ' still own the right bottleneck, workflow, or bargaining position once force pressure intensifies.')}</p>
  <div class="meta" style="margin-top:14px">Tensions</div>
  <p class="small">{e('This cluster gets stressed when ' + ', '.join(cluster.get('top_constraints', [])[:2]) + ' stop looking manageable and start defining the economics.')}</p>
  <div class="meta" style="margin-top:14px">Second-order effects</div>
  <p class="small">{e('If the cluster thesis is right, the spillover shows up in adjacent company behavior, not just in the headline leaders.')}</p>
</article>"""
        for cluster in clusters
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company Clusters — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="company-universe.html">Company universe</a><a href="business-lenses.html">Business lenses</a></div>
<div class="eyebrow">Company clusters · US · 2025–2026</div>
<h1>Company Clusters</h1>
<p class="sub">These are the dominant business-model groupings implied by the company universe. They are not stock screens. They are operating clusters: what sort of business this is, what force set governs it, and which owner type tends to win.</p>
<div class="panel" style="margin-top:24px">
  <div class="meta">How to use it</div>
  <p>Use this page to move from named companies to recurring business-model logic. The point is to see which clusters are structurally advantaged, which force signals repeat inside them, and what investors or operators should actually underwrite before backing a name in the cluster.</p>
</div>
<section class="section"><div class="grid">{cards}</div></section>
<footer>Clustered from the extracted company universe and the existing business-lens taxonomy.</footer>
</div></body></html>"""


def build_scoreboard_records(companies: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [company for company in companies if company["mention_count"] >= 3]
    advantaged = sorted(
        [company for company in eligible if company["status"] == "advantaged"],
        key=lambda row: (-row["rating_score"], -row["mention_count"], row["title"]),
    )[:40]
    exposed = sorted(
        [company for company in eligible if company["status"] == "exposed"],
        key=lambda row: (row["rating_score"], -row["mention_count"], row["title"]),
    )[:40]
    mixed = sorted(
        [company for company in eligible if company["status"] == "mixed"],
        key=lambda row: (-row["mention_count"], row["title"]),
    )[:40]
    return {
        "advantaged": advantaged,
        "exposed": exposed,
        "mixed": mixed,
    }


def build_comparison_records(companies: list[dict[str, Any]]) -> list[dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for company in companies:
        if company["mention_count"] < 3:
            continue
        grouped[company["business_model_cluster_title"]].append(company)

    records = []
    for cluster_title, members in grouped.items():
        if len(members) < 3:
            continue
        sorted_members = sorted(members, key=lambda row: (-row["mention_count"], row["title"]))
        advantaged = [row for row in members if row["status"] == "advantaged"][:5]
        exposed = [row for row in members if row["status"] == "exposed"][:5]
        mixed = [row for row in members if row["status"] == "mixed"][:5]
        records.append(
            {
                "cluster_title": cluster_title,
                "company_count": len(members),
                "leaders": sorted_members[:8],
                "advantaged": sorted(advantaged, key=lambda row: (-row["rating_score"], -row["mention_count"], row["title"])),
                "exposed": sorted(exposed, key=lambda row: (row["rating_score"], -row["mention_count"], row["title"])),
                "mixed": sorted(mixed, key=lambda row: (-row["mention_count"], row["title"])),
            }
        )
    records.sort(key=lambda row: (-row["company_count"], row["cluster_title"]))
    return records


def scoreboard_table(companies: list[dict[str, Any]]) -> str:
    rows = "\n".join(
        f"""<tr>
  <td><a href="company-pages/{e(company['slug'])}.html">{e(company['title'])}</a></td>
  <td>{e(company['business_model_cluster_title'])}</td>
  <td>{company['mention_count']}</td>
  <td>{company['rating_score']}</td>
  <td>{', '.join(e(force['title']) for force in company['dominant_forces'][:2])}</td>
</tr>"""
        for company in companies
    )
    return f"""<table>
  <thead><tr><th>Company</th><th>Cluster</th><th>Mentions</th><th>Score</th><th>Main forces</th></tr></thead>
  <tbody>{rows}</tbody>
</table>"""


def build_scoreboard_page(scoreboard: dict[str, Any]) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company Scoreboard — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="company-universe.html">Company universe</a><a href="company-clusters.html">Company clusters</a></div>
<div class="eyebrow">Company scoreboard · US · 2025–2026</div>
<h1>Company Scoreboard</h1>
<p class="sub">This is the explicit judgment layer. It ranks recurring operators by the force exposure and business-model logic implied by the corpus, separating current structural winners, pressured names, and the large middle that still reads as mixed.</p>

<section class="section">
  <h2>Most Advantaged</h2>
  <div class="panel">{scoreboard_table(scoreboard['advantaged'][:20])}</div>
</section>

<section class="section">
  <h2>Most Exposed</h2>
  <div class="panel">{scoreboard_table(scoreboard['exposed'][:20])}</div>
</section>

<section class="section">
  <h2>The Big Middle</h2>
  <div class="panel">{scoreboard_table(scoreboard['mixed'][:20])}</div>
</section>

<footer>Ranked from the extracted company universe using the current force and business-model scoring logic.</footer>
</div></body></html>"""


def comparison_list(items: list[dict[str, Any]]) -> str:
    if not items:
        return "<p class=\"small\">No names surfaced yet.</p>"
    rows = "".join(
        f"<li><a href=\"company-pages/{e(item['slug'])}.html\">{e(item['title'])}</a> <span class=\"small\">({e(item['status'])}, {item['mention_count']} mentions)</span></li>"
        for item in items
    )
    return f"<ul class=\"list\">{rows}</ul>"


def build_comparisons_page(comparisons: list[dict[str, Any]]) -> str:
    sections = "\n".join(
        f"""<article class="card">
  <div class="meta">{section['company_count']} companies</div>
  <h3>{e(section['cluster_title'])}</h3>
  <p class="small">Most recurrent names in this cluster, plus the current advantaged/exposed/middle split from the scoring model.</p>
  <div class="section">
    <h3>Largest names</h3>
    {comparison_list(section['leaders'])}
  </div>
  <div class="section">
    <h3>Advantaged</h3>
    {comparison_list(section['advantaged'])}
  </div>
  <div class="section">
    <h3>Exposed</h3>
    {comparison_list(section['exposed'])}
  </div>
  <div class="section">
    <h3>Mixed</h3>
    {comparison_list(section['mixed'])}
  </div>
</article>"""
        for section in comparisons
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Company Comparisons — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="company-universe.html">Company universe</a><a href="company-clusters.html">Company clusters</a><a href="company-scoreboard.html">Company scoreboard</a></div>
<div class="eyebrow">Company comparisons · US · 2025–2026</div>
<h1>Company Comparisons</h1>
<p class="sub">This is the cluster-by-cluster comparison layer. It shows the biggest recurring names inside each business model, then separates the current apparent winners, the pressured names, and the contested middle.</p>
<section class="section"><div class="grid">{sections}</div></section>
<footer>Built from the clustered company universe and current scoring model.</footer>
</div></body></html>"""


def build_company_page(company: dict[str, Any]) -> str:
    industry_cards = "\n".join(
        brief_card(BRIEFS_BY_SLUG[row["slug"]]) for row in company["industry_rows"][:6] if row["slug"] in BRIEFS_BY_SLUG
    )
    force_cards = "\n".join(
        f"""<div class="force">
  <div class="meta">Force</div>
  <h3>{e(force['title'])}</h3>
  <p><b>Demand logic:</b> {e(force['demand_logic'])}</p>
  <p><b>Margin logic:</b> {e(force['margin_logic'])}</p>
</div>"""
        for force in company["dominant_forces"]
    )
    themes = "".join(f'<span class="chip">{e(theme)}</span>' for theme in company["top_themes"])
    constraints = "".join(f'<span class="chip">{e(item)}</span>' for item in company["constraints"])
    sector_mix = "".join(
        f"<li>{e(item['sector'])}: {item['count']} linked industries</li>"
        for item in company["sector_mix"]
    )
    investor_read = (
        f"{company['title']} screens as {status_label(company['status']).lower()} because it appears repeatedly inside "
        f"{company['business_model_cluster_title'].lower()} situations and the corpus keeps tying those situations to "
        f"{', '.join(force['title'] for force in company['dominant_forces'][:2]) or 'cross-force exposure'}."
    )
    operator_read = (
        f"The operating question is whether {company['title']} can keep converting scale and position into "
        f"{company['best_owner_type']} economics rather than drifting into the constraints that squeeze this cluster."
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(company['title'])} — Company Intelligence</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../company-universe.html">Company universe</a><a href="../company-clusters.html">Company clusters</a><a href="../company-memos.html">Company memos</a></div>
<div class="eyebrow">Company intelligence · US · 2025–2026</div>
<h1>{e(company['title'])}</h1>
<p class="sub">{e(company['business_truth'])}</p>
<div class="status {e(company['status'])}">{e(status_label(company['status']))}</div>
<div class="split">
  <main class="stack">
    <div class="panel">
      <div class="meta">Business model</div>
      <h2>{e(company['business_model_cluster_title'])}</h2>
      <p>{e(company['why_owner_type'])}</p>
      <div class="stats"><span>{company['mention_count']} corpus mentions</span><span>{company['industry_count']} industries</span><span>{e(company['best_owner_type'])}</span></div>
      <div class="chips">{themes}</div>
    </div>
    <div class="panel">
      <div class="meta">Investor read</div>
      <h2>Why it wins or gets squeezed</h2>
      <p>{e(investor_read)}</p>
      <p>{e(operator_read)}</p>
      <div class="chips">{constraints}</div>
    </div>
    <div class="section">
      <h2>Linked industries</h2>
      <div class="grid">{industry_cards}</div>
    </div>
    <div class="section">
      <h2>Governing forces</h2>
      <div class="stack">{force_cards}</div>
    </div>
  </main>
  <aside class="stack">
    <div class="panel">
      <div class="meta">Sector mix</div>
      <h2>Where it keeps showing up</h2>
      <ul class="list">{sector_mix}</ul>
    </div>
    <div class="panel">
      <div class="meta">Main risk</div>
      <h2>What would break the read</h2>
      <p class="small">The current read is only as strong as the company’s ability to stay on the right side of {e(', '.join(company['constraints']) or 'its governing constraints')} while preserving relevance inside {e(company['business_model_cluster_title'].lower())} markets.</p>
    </div>
  </aside>
</div>
<footer>Built from recurring company mentions in the corpus and mapped into the force/lens system.</footer>
</div></body></html>"""


def main() -> None:
    companies = build_company_records()
    clusters = build_cluster_records(companies)
    scoreboard = build_scoreboard_records(companies)
    comparisons = build_comparison_records(companies)
    os.makedirs(PAGES_DIR, exist_ok=True)
    for name in os.listdir(PAGES_DIR):
        if name.endswith(".html"):
            os.remove(os.path.join(PAGES_DIR, name))

    with open(UNIVERSE_JSON, "w", encoding="utf-8") as handle:
        json.dump(companies, handle, ensure_ascii=False, indent=2)
    with open(CLUSTERS_JSON, "w", encoding="utf-8") as handle:
        json.dump(clusters, handle, ensure_ascii=False, indent=2)
    with open(SCOREBOARD_JSON, "w", encoding="utf-8") as handle:
        json.dump(scoreboard, handle, ensure_ascii=False, indent=2)
    with open(COMPARISONS_JSON, "w", encoding="utf-8") as handle:
        json.dump(comparisons, handle, ensure_ascii=False, indent=2)
    with open(UNIVERSE_HTML, "w", encoding="utf-8") as handle:
        handle.write(build_universe_page(companies))
    with open(CLUSTERS_HTML, "w", encoding="utf-8") as handle:
        handle.write(build_clusters_page(clusters))
    with open(SCOREBOARD_HTML, "w", encoding="utf-8") as handle:
        handle.write(build_scoreboard_page(scoreboard))
    with open(COMPARISONS_HTML, "w", encoding="utf-8") as handle:
        handle.write(build_comparisons_page(comparisons))

    page_count = 0
    for company in companies:
        if company["mention_count"] < 3:
            continue
        page_count += 1
        with open(os.path.join(PAGES_DIR, f"{company['slug']}.html"), "w", encoding="utf-8") as handle:
            handle.write(build_company_page(company))

    print(f"wrote {UNIVERSE_JSON}")
    print(f"wrote {CLUSTERS_JSON}")
    print(f"wrote {SCOREBOARD_JSON}")
    print(f"wrote {COMPARISONS_JSON}")
    print(f"wrote {UNIVERSE_HTML}")
    print(f"wrote {CLUSTERS_HTML}")
    print(f"wrote {SCOREBOARD_HTML}")
    print(f"wrote {COMPARISONS_HTML}")
    print(f"companies={len(companies)}")
    print(f"pages={page_count}")
    print(f"clusters={len(clusters)}")


if __name__ == "__main__":
    main()
