#!/usr/bin/env python3
"""Build applied operator and investor memos from the American themes system."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
OUT = ROOT / "american-theme-memos.html"
MEMOS_DIR = ROOT / "theme-memos"


MEMOS = {
    "barbelled-consumer-america": {
        "operator_angle": "Pick a side. The middle is where promotional death happens.",
        "investor_angle": "Own the value system, the premium refuge, or the enabling infrastructure. Avoid undifferentiated middle-market inventory stories.",
        "best_hunting_grounds": [
            "membership and basket-consolidation formats",
            "retailers with real private-label strength",
            "premium niches with visible quality signaling",
            "convenience systems that remove friction rather than merely charge more",
        ],
        "avoid_zones": [
            "generic mid-tier goods without real loyalty or cost advantage",
            "businesses living on promotion to preserve traffic",
            "brands vulnerable to dupe culture without distribution control",
        ],
        "operator_moves": [
            "Decide whether the format is for prudence or for permission-to-splurge.",
            "Use private label and own-brand lines to defend both traffic and gross margin.",
            "Design pricing and merchandising around trip economics, not only unit price.",
        ],
        "investor_questions": [
            "What percent of gross margin comes from categories where substitution is easy?",
            "Does the business own demand or rent it from platforms and paid acquisition?",
            "Can management explain why shoppers still willingly pay up?",
        ],
    },
    "wellness-recodes-daily-life": {
        "operator_angle": "Assume health is a mainstream filter, not a niche overlay.",
        "investor_angle": "Back categories that benefit from reclassification toward health, function, moderation, or controlled indulgence.",
        "best_hunting_grounds": [
            "functional beverage and nutrition-adjacent categories",
            "consumer products aligned with portion control or protein/satiety narratives",
            "beauty, fitness, and wellness hybrids with recurring routines",
            "service businesses that help consumers feel optimized rather than guilty",
        ],
        "avoid_zones": [
            "volume-dependent vice categories with weak premium insulation",
            "legacy indulgence categories assuming old appetite norms still hold",
            "wellness branding that is vague, cosmetic, or easy to disbelieve",
        ],
        "operator_moves": [
            "Rebuild packaging and positioning around explicit utility or controlled pleasure.",
            "Treat nonalcoholic and moderation-friendly options as core products, not side menus.",
            "Use routines, subscriptions, or repeatable behavior loops to create recurrence.",
        ],
        "investor_questions": [
            "Is growth coming from true behavior change or just temporary novelty?",
            "How exposed is the model to shrinking volume in legacy high-sugar or alcohol-heavy mixes?",
            "Does the brand have scientific, social, or retail proof that the health claim is real?",
        ],
    },
    "experience-status-and-community": {
        "operator_angle": "Make the visit mean something beyond the transaction.",
        "investor_angle": "Scarcity, programming, and affiliation matter more than raw capacity in participation-driven markets.",
        "best_hunting_grounds": [
            "destinations with repeatable cultural or community gravity",
            "retail formats that combine service, theater, and discovery",
            "fandom ecosystems with multiple monetization loops",
            "active-aging leisure and outdoor demand platforms",
        ],
        "avoid_zones": [
            "generic venues without reasons for return visitation",
            "experience businesses dependent on one narrow demand occasion",
            "physical formats that function like shelves but pay venue-level costs",
        ],
        "operator_moves": [
            "Program the venue, do not just operate the venue.",
            "Use memberships, communities, or events to turn visits into habit loops.",
            "Design the physical format to generate shareable memory, not only throughput.",
        ],
        "investor_questions": [
            "What creates real scarcity here: location, programming, community, or brand?",
            "How much of repeat demand is structural versus event-driven?",
            "Can the operator price above generic alternatives without losing relevance?",
        ],
    },
    "aging-care-and-the-assistance-economy": {
        "operator_angle": "Assistance demand is real, but the monetization bottleneck sits in labor, reimbursement, and coordination.",
        "investor_angle": "Own enabling infrastructure and system fluency around aging, not just exposure to the aging demographic itself.",
        "best_hunting_grounds": [
            "home-first support layers that reduce family and admin friction",
            "chronic-care infrastructure with repeatable operational models",
            "care-adjacent software, logistics, and reimbursement layers",
            "financial and insurance products built around longevity complexity",
        ],
        "avoid_zones": [
            "labor-heavy direct care models with weak pricing power",
            "categories that depend on demographic demand but lack payer leverage",
            "operators mistaking obvious need for easy economics",
        ],
        "operator_moves": [
            "Build around family coordination and documentation, not only clinical service.",
            "Treat payer and coding fluency as part of the product, not back-office overhead.",
            "Use distributed care models only where the coordination stack is strong enough to hold.",
        ],
        "investor_questions": [
            "Where does reimbursement control the margin pool?",
            "How much of the service can be standardized without harming quality?",
            "Is the real bottleneck labor, beds, admin workflow, or underwriting capacity?",
        ],
    },
    "work-without-the-old-firm": {
        "operator_angle": "The opportunity sits in modular capability, training, and administrative support for fragmented work.",
        "investor_angle": "Back the stack around a thinner firm: expert networks, workflow infrastructure, credentialing, and portable support systems.",
        "best_hunting_grounds": [
            "fractional expertise and advisory platforms with repeatable trust",
            "training and credentials tied to real employability gains",
            "admin systems that simplify fragmented labor arrangements",
            "workflow tools replacing repeatable junior labor",
        ],
        "avoid_zones": [
            "services relying on abundant low-cost junior labor",
            "credential businesses detached from wage or placement outcomes",
            "firms assuming thin staffing will not damage long-run talent formation",
        ],
        "operator_moves": [
            "Productize expertise into recurring offers rather than bespoke hours.",
            "Design tools and services around employer caution and worker instability at the same time.",
            "Use automation to remove repetitive load, not to erase trust-critical human judgment blindly.",
        ],
        "investor_questions": [
            "Does the platform solve a real coordination burden or only intermediate supply?",
            "Are workers and employers both better off using it repeatedly?",
            "What happens to unit economics if AI compresses the routine layer faster than expected?",
        ],
    },
    "physical-reindustrialization-and-infrastructure": {
        "operator_angle": "The best economics sit on the bottleneck side of physical buildout.",
        "investor_angle": "Prefer constraint owners and picks-and-shovels providers over romantic generalized reshoring narratives.",
        "best_hunting_grounds": [
            "electrical, cooling, transmission, and utility-adjacent trades",
            "specified manufacturers with domestic or nearshore relevance",
            "logistics land and throughput infrastructure",
            "equipment and services linked to power-ready industrial buildout",
        ],
        "avoid_zones": [
            "thin-margin import models with no sourcing leverage",
            "reshoring stories lacking specification, security, or power access advantages",
            "operators exposed to material volatility without pass-through rights",
        ],
        "operator_moves": [
            "Treat power access and procurement discipline as strategic assets.",
            "Focus expansion where the business sits next to unavoidable constraints.",
            "Sell reliability, compliance, and access instead of just output volume.",
        ],
        "investor_questions": [
            "Does this company own a bottleneck or merely serve one indirectly?",
            "How much of the margin pool depends on tariff or energy volatility?",
            "What makes the demand durable after the initial build cycle passes?",
        ],
    },
    "scale-financialization-and-the-owned-economy": {
        "operator_angle": "Read markets through ownership topology, not only through customer demand.",
        "investor_angle": "The owner of the system, rail, asset, or governance layer often captures more durable value than the visible operator.",
        "best_hunting_grounds": [
            "roll-up categories with real back-office and procurement synergies",
            "asset-control businesses with quiet pricing leverage",
            "platform or franchise systems with strong governance and captive flows",
            "scaled intermediaries that turn complexity into repeatable spread",
        ],
        "avoid_zones": [
            "regional middlemen without unique data, trust, or cost advantage",
            "independents in categories already structurally shaped by scale owners",
            "platforms where extraction outruns operator economics",
        ],
        "operator_moves": [
            "Separate local execution from system ownership and optimize each deliberately.",
            "Use centralized buying, software, and financing to widen the gap versus the fragmented edge.",
            "Measure who really controls the customer, the terms, the land, and the data.",
        ],
        "investor_questions": [
            "Who actually owns the constraint in this value chain?",
            "Is scale producing real operating leverage or only narrative prestige?",
            "How much of the spread can a regional or local player still keep?",
        ],
    },
    "regulated-software-and-admin-state": {
        "operator_angle": "Mandatory complexity is one of the cleanest recurring demand pools in the system.",
        "investor_angle": "Own productized compliance, verification, fraud, admin, and standards infrastructure where the customer cannot really opt out.",
        "best_hunting_grounds": [
            "workflow software embedded in required processes",
            "identity, fraud, and trust infrastructure with deep data moats",
            "testing, certification, and audit layers that function as gates",
            "healthcare and regulated-admin rails where throughput quality matters",
        ],
        "avoid_zones": [
            "manual service shops exposed to wage inflation without software leverage",
            "compliance tools that are nice-to-have rather than required",
            "vendors unable to prove auditability and workflow fit in regulated settings",
        ],
        "operator_moves": [
            "Convert bespoke labor into recurring workflow wherever regulation permits.",
            "Sell auditability, traceability, and evidence collection as part of core value.",
            "Go after markets where the rule burden is durable and unlikely to be optionalized away.",
        ],
        "investor_questions": [
            "What makes this workflow mandatory rather than discretionary?",
            "How much of fulfillment is already software-led versus labor-led?",
            "How hard would it be for a customer to remove this layer from the process?",
        ],
    },
    "space-housing-and-local-friction": {
        "operator_angle": "Geography is now a live operating variable again.",
        "investor_angle": "Back the places and service systems aligned with current human and infrastructure flows, not with inherited assumptions.",
        "best_hunting_grounds": [
            "adaptive reuse and specialty redevelopment capabilities",
            "neighborhood and suburban convenience systems with stable lived-density demand",
            "housing-lock-in beneficiaries in repair, remodel, and rental support",
            "land and property linked to logistics, utilities, or compute infrastructure",
        ],
        "avoid_zones": [
            "commodity office exposure without a plausible reuse path",
            "service models dependent on old central-business-district traffic assumptions",
            "location strategies built on mobility that households no longer have",
        ],
        "operator_moves": [
            "Map demand to where people actually spend time now, not to pre-2020 flow assumptions.",
            "Treat zoning, utility access, and conversion feasibility as first-order operating questions.",
            "Use housing immobility as a clue to where service demand will persist locally.",
        ],
        "investor_questions": [
            "What local friction makes this asset or service more valuable rather than less?",
            "Can the site or footprint be repurposed if the current use weakens?",
            "How exposed is the model to household immobility and commuting pattern shifts?",
        ],
    },
    "machine-intelligence-and-compute-buildout": {
        "operator_angle": "AI should be read as a stack of constraints and workflow changes, not just a feature race.",
        "investor_angle": "Prefer positions with infrastructure leverage, workflow entrenchment, or scarce enabling capacity over generic AI labeling.",
        "best_hunting_grounds": [
            "power-linked and colocation-adjacent infrastructure",
            "boring workflow software that becomes more valuable with AI integration",
            "control, security, and audit layers around AI adoption",
            "physical buildout suppliers tied to compute expansion",
        ],
        "avoid_zones": [
            "AI surfaces with weak distribution or no real workflow ownership",
            "businesses facing compute-cost inflation without pricing power",
            "service firms pretending automation will not pressure their junior labor base",
        ],
        "operator_moves": [
            "Anchor AI strategy in a clear bottleneck: labor, throughput, evidence, or infrastructure access.",
            "Sell trustworthy workflow gains instead of generic AI novelty.",
            "Track where utility and physical constraints could become the real growth cap.",
        ],
        "investor_questions": [
            "Does this company own part of the scarce stack or depend entirely on others for it?",
            "What portion of value creation is physical infrastructure versus software margin?",
            "How durable is the workflow embed if upstream AI capabilities commoditize?",
        ],
    },
}


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--green:#78ca90;--red:#e07d6d;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1200px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.4rem,5vw,4.2rem);line-height:1;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3,.panel h3{margin:.2em 0 .35em;font-size:1.12rem}.card p,.panel p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.memo{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.memo:first-of-type{margin-top:0;padding-top:0;border-top:none}.memo h3{font-size:1.28rem;margin:.2em 0 .35em}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.smallgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-top:14px}.mini{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:12px}.mini h4{margin:0 0 .35em;font-size:.96rem}.mini p{margin:0;color:var(--muted);font-size:.9rem}.subcards{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-top:14px}.subcard{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:14px}.subcard h4{margin:.2em 0 .35em;font-size:1rem}.subcard p{margin:.35em 0 0;color:var(--muted);font-size:.95rem}@media(max-width:920px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_themes() -> list[dict]:
    with THEMES_JSON.open(encoding="utf-8") as handle:
        return json.load(handle)["themes"]


def build_theme_record(theme: dict) -> dict:
    memo = MEMOS[theme["slug"]]
    exposed_companies = []
    advantaged_companies = []
    for subtheme in theme["subthemes"]:
        for company in subtheme["companies"]:
            if company["status"] == "advantaged" and company not in advantaged_companies:
                advantaged_companies.append(company)
            if company["status"] == "exposed" and company not in exposed_companies:
                exposed_companies.append(company)
    return {
        **theme,
        **memo,
        "advantaged_examples": advantaged_companies[:6],
        "exposed_examples": exposed_companies[:6],
    }


def company_link(company: dict, prefix: str = "") -> str:
    href = f"{prefix}company-pages/{company['slug']}.html"
    path = ROOT / "company-pages" / f"{company['slug']}.html"
    title = e(company["title"])
    if path.exists():
        return f'<a class="chip" href="{e(href)}">{title}</a>'
    return f'<span class="chip">{title}</span>'


def theme_brief_chip(theme: dict, prefix: str = "") -> str:
    return f'<a class="chip" href="{e(prefix)}theme-briefs/{e(theme["slug"])}.html">{e(theme["title"])}</a>'


def theme_taxonomy_chip(theme: dict, prefix: str = "") -> str:
    return f'<a class="chip" href="{e(prefix)}themes/{e(theme["slug"])}.html">{e(theme["title"])} taxonomy</a>'


def render_subtheme_application(theme: dict, subtheme: dict, prefix: str = "") -> str:
    forces = "".join(
        f'<a class="chip" href="{e(prefix)}forces/{e(force["slug"])}/index.html">{e(force["title"])}</a>'
        for force in subtheme["forces"]
    )
    return f"""<article class="subcard">
  <div class="meta">Applied subtheme</div>
  <h4><a href="{e(prefix)}themes/{e(theme['slug'])}.html#{e(subtheme['slug'])}">{e(subtheme['title'])}</a></h4>
  <p>{e(subtheme['deep_read'])}</p>
  <div class="chips">{forces}</div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Pressure points</div>
    <ul class="list">{''.join(f"<li>{e(item)}</li>" for item in subtheme['pressure_points'][:3])}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Strategic consequences</div>
    <ul class="list">{''.join(f"<li>{e(item)}</li>" for item in subtheme['strategic_consequences'][:3])}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Market rewrites</div>
    <ul class="list">{''.join(f"<li>{e(item)}</li>" for item in subtheme['market_rewrites'][:2])}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Counterforces</div>
    <ul class="list">{''.join(f"<li>{e(item)}</li>" for item in subtheme['counterforces'][:2])}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Behavioral expression</div>
    <ul class="list">{''.join(f"<li>{e(item)}</li>" for item in subtheme['behavioral_expression'][:3])}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Economic mechanics</div>
    <ul class="list">{''.join(f"<li>{e(item)}</li>" for item in subtheme['economic_mechanics'][:3])}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Timing markers</div>
    <ul class="list">{''.join(f"<li>{e(item)}</li>" for item in subtheme['timing_markers'][:2])}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Execution hazards</div>
    <ul class="list">{''.join(f"<li>{e(item)}</li>" for item in subtheme['execution_hazards'][:2])}</ul>
  </div>
</article>"""


def render_memo(theme: dict, prefix: str = "") -> str:
    best = "".join(f"<li>{e(item)}</li>" for item in theme["best_hunting_grounds"])
    avoid = "".join(f"<li>{e(item)}</li>" for item in theme["avoid_zones"])
    moves = "".join(f"<li>{e(item)}</li>" for item in theme["operator_moves"])
    questions = "".join(f"<li>{e(item)}</li>" for item in theme["investor_questions"])
    tensions = "".join(f"<li>{e(item)}</li>" for item in theme["structural_tensions"])
    signals = "".join(f"<li>{e(item)}</li>" for item in theme["signals_to_watch"])
    implications = "".join(f"<li>{e(item)}</li>" for item in theme["strategic_implications"])
    stakeholder_map = "".join(f"<li>{e(item)}</li>" for item in theme["stakeholder_map"])
    second_order_effects = "".join(f"<li>{e(item)}</li>" for item in theme["second_order_effects"])
    societal_read = "".join(f"<li>{e(item)}</li>" for item in theme["societal_read"])
    consumer_read = "".join(f"<li>{e(item)}</li>" for item in theme["consumer_read"])
    industrial_read = "".join(f"<li>{e(item)}</li>" for item in theme["industrial_read"])
    capital_implications = "".join(f"<li>{e(item)}</li>" for item in theme["capital_implications"])
    force_chips = "".join(
        f'<a class="chip" href="{e(prefix)}forces/{e(force["slug"])}/index.html">{e(force["title"])}</a>'
        for force in theme["forces"]
    )
    advantaged = "".join(company_link(company, prefix=prefix) for company in theme["advantaged_examples"]) or '<span class="chip">none surfaced</span>'
    exposed = "".join(company_link(company, prefix=prefix) for company in theme["exposed_examples"]) or '<span class="chip">none surfaced</span>'
    subcards = "".join(render_subtheme_application(theme, subtheme, prefix=prefix) for subtheme in theme["subthemes"])
    return f"""<section class="memo">
  <div class="meta">{e(theme['lens'])} memo</div>
  <h3>{e(theme['title'])}</h3>
  <p><b>Operator angle:</b> {e(theme['operator_angle'])}</p>
  <p><b>Investor angle:</b> {e(theme['investor_angle'])}</p>
  <div class="panel" style="margin-top:14px">
    <div class="meta">Deep theme read</div>
    <p>{e(theme['deep_read'])}</p>
  </div>
  <div class="chips">{theme_brief_chip(theme, prefix)}{theme_taxonomy_chip(theme, prefix)}{force_chips}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">Best hunting grounds</div>
      <ul class="list">{best}</ul>
    </div>
    <div class="panel">
      <div class="meta">Avoid zones</div>
      <ul class="list">{avoid}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Operator moves</div>
      <ul class="list">{moves}</ul>
    </div>
    <div class="panel">
      <div class="meta">Investor diligence questions</div>
      <ul class="list">{questions}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Structural tensions</div>
      <ul class="list">{tensions}</ul>
    </div>
    <div class="panel">
      <div class="meta">Signals to watch</div>
      <ul class="list">{signals}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Strategic implications</div>
      <ul class="list">{implications}</ul>
    </div>
    <div class="panel">
      <div class="meta">Stakeholder map</div>
      <ul class="list">{stakeholder_map}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Societal read</div>
      <ul class="list">{societal_read}</ul>
    </div>
    <div class="panel">
      <div class="meta">Consumer read</div>
      <ul class="list">{consumer_read}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Industrial read</div>
      <ul class="list">{industrial_read}</ul>
    </div>
    <div class="panel">
      <div class="meta">Capital implications</div>
      <ul class="list">{capital_implications}</ul>
    </div>
  </div>
  <div class="panel" style="margin-top:14px">
    <div class="meta">Second-order effects</div>
    <ul class="list">{second_order_effects}</ul>
  </div>
  <div class="smallgrid">
    <div class="mini">
      <h4>Advantaged examples</h4>
      <div class="chips">{advantaged}</div>
    </div>
    <div class="mini">
      <h4>Exposed examples</h4>
      <div class="chips">{exposed}</div>
    </div>
  </div>
  <div class="panel" style="margin-top:14px">
    <div class="meta">Subtheme application map</div>
    <div class="subcards">{subcards}</div>
  </div>
</section>"""


def build_hub(records: list[dict]) -> str:
    cards = []
    for theme in records:
        cards.append(
            f"""<article class="card">
  <div class="meta">{e(theme['lens'])}</div>
  <h3><a href="theme-memos/{e(theme['slug'])}.html">{e(theme['title'])}</a></h3>
  <p>{e(theme['operator_angle'])}</p>
  <div class="chips">{theme_brief_chip(theme)}</div>
</article>"""
        )
    memos = "".join(render_memo(theme) for theme in records)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>American Theme Memos — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="american-themes.html">American themes</a><a href="american-theme-briefs.html">Theme briefs</a><a href="sector-memos.html">Sector memos</a></div>
<div class="eyebrow">Applied memos · US · 2025-2026</div>
<h1>American Theme Memos</h1>
<p class="sub">This is the applied layer. It turns the themes system into operator and investor memos: where to hunt, what to avoid, what to do, and what to ask before underwriting a category or business.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(records)}</div><div class="l">Theme memos</div></div>
  <div class="kpi"><div class="n">{sum(len(theme['operator_moves']) for theme in records)}</div><div class="l">Operator moves</div></div>
  <div class="kpi"><div class="n">{sum(len(theme['investor_questions']) for theme in records)}</div><div class="l">Diligence questions</div></div>
  <div class="kpi"><div class="n">{sum(theme['signal_count'] for theme in records)}</div><div class="l">Signals carried through</div></div>
</div>
<div class="lead"><p>Use this layer when the question shifts from what is happening to what to do with it. The memos assume the theme system is already true and translate it into actionable screening, diligence, and operating posture.</p></div>

<section class="section">
  <h2>Memo Index</h2>
  <div class="grid">{''.join(cards)}</div>
</section>

<section class="section">
  <h2>Applied Read</h2>
  {memos}
</section>

</div></body></html>"""


def build_detail(theme: dict) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(theme['title'])} Memo — American Themes</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../american-theme-memos.html">Theme memos</a><a href="../american-theme-briefs.html">Theme briefs</a></div>
<div class="eyebrow">{e(theme['lens'])} memo · US · 2025-2026</div>
<h1>{e(theme['title'])}</h1>
<p class="sub">{e(theme['thesis'])}</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(theme['operator_moves'])}</div><div class="l">Operator moves</div></div>
  <div class="kpi"><div class="n">{len(theme['investor_questions'])}</div><div class="l">Investor questions</div></div>
  <div class="kpi"><div class="n">{theme['signal_count']}</div><div class="l">Signals</div></div>
  <div class="kpi"><div class="n">{theme['evidence_industry_count']}</div><div class="l">Evidence industries</div></div>
</div>
<div class="lead"><p>{e(theme['operator_angle'])}</p></div>
<section class="section">
  {render_memo(theme, prefix="../")}
</section>
</div></body></html>"""


def main() -> None:
    records = [build_theme_record(theme) for theme in load_themes() if theme["slug"] in MEMOS]
    MEMOS_DIR.mkdir(exist_ok=True)

    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(build_hub(records))

    for theme in records:
        with (MEMOS_DIR / f"{theme['slug']}.html").open("w", encoding="utf-8") as handle:
            handle.write(build_detail(theme))

    print(f"wrote {OUT}")
    print(f"wrote memos to {MEMOS_DIR}")
    print(f"memos={len(records)}")


if __name__ == "__main__":
    main()
