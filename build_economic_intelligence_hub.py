#!/usr/bin/env python3
"""Build a surfaced economic-intelligence hub from the generated taxonomy."""

from __future__ import annotations

import html
import json
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "economic-intelligence.html")


def e(value):
    return html.escape(str(value or ""), quote=True)


INTRO = (
    "This is the interpretation layer on top of the 1,491-industry corpus: the recurring forces, "
    "the broader domains they roll up into, and the operator questions that matter once you stop "
    "reading industries one at a time and start reading the economy as a system."
)

TRANSLATION_LINK = (
    "The next layer down is practical: force-to-operator translations that turn each major force into "
    "margin logic, demand logic, binding constraints, advantaged owner types, and concrete moves."
)

BUSINESS_LENSES_LINK = (
    "The business-lens layer applies the force map to concrete archetypes: local service platforms, specified manufacturers, "
    "reimbursement-managed care operators, regulated workflow infrastructure, distributors, and other recurring business types."
)

SECTOR_CASES_LINK = (
    "Applied sector cases show how the framework gets used on real industries: a representative market, the linked business lens, "
    "the governing forces, and the owner/operator logic that follows."
)

SUBTHEMES_LINK = (
    "The subtheme layer breaks each major force into its recurring underlying patterns, with angles and evidence footprints, so the map is readable below the headline level."
)

AMERICAN_THEMES_LINK = (
    "The American themes layer turns the force map into a broader read on societal, cultural, consumer, industrial, and institutional change, with detailed subthemes and second-order patterns."
)

AMERICAN_THEME_BRIEFS_LINK = (
    "The theme briefs layer adds the long-form interpretation: what each major theme actually means, what tensions define it, and what signals matter next."
)

AMERICAN_CAPSTONE_LINK = (
    "The capstone narrative is the single end-to-end read on the US economy in 2025-2026: how demand, labor, culture, institutions, geography, AI, and scale fit together."
)

AMERICAN_OUTLOOK_LINK = (
    "The master outlook reorganizes the same system into four top-level lenses: societal, cultural, consumer, and industrial change, with linked tensions, signals, and subtheme evidence."
)

AMERICAN_OUTLOOK_MEMOS_LINK = (
    "The outlook memo pack is the applied macro layer above the essays: four board-style memos for societal, cultural, consumer, and industrial change."
)

AMERICAN_THEME_MEMOS_LINK = (
    "The memo layer translates the themes system into operator and investor decisions: where to hunt, what to avoid, what to do, and what to diligence."
)

SECTOR_MEMOS_LINK = (
    "The sector memo layer maps the major sectors to dominant themes, force pressures, representative industries, and advantaged versus exposed setups."
)

SECTOR_OUTLOOKS_LINK = (
    "The sector outlook layer re-reads each major sector through the same four top-level lenses used in the American outlook: societal, cultural, consumer, and industrial change."
)

COMPANY_MEMOS_LINK = (
    "The company memo layer translates important names into explicit structural reads tied back to sector logic, dominant themes, force exposure, and break-risk questions."
)

BUSINESS_PROFILES_LINK = (
    "Business profiles are company-style reads of representative business types: not just what sector they sit in, but what actually drives demand, margins, ownership logic, and risk."
)

COMPANY_UNIVERSE_LINK = (
    "The company universe aggregates named operators from the full corpus and maps them back into the business-model and force system, so repeated company mentions become a usable intelligence surface."
)

COMPANY_CLUSTERS_LINK = (
    "Company clusters group recurring operators by business model and force exposure, turning scattered mentions into comparative reads on who is structurally advantaged, mixed, or exposed."
)

COMPANY_SCOREBOARD_LINK = (
    "The company scoreboard is the explicit judgment layer: which recurring operators look structurally advantaged, which look exposed, and which sit in the large contested middle."
)

COMPANY_COMPARISONS_LINK = (
    "The comparison layer shows the biggest names inside each business-model cluster and separates the apparent winners, losers, and contested middle within each cluster."
)


NARRATIVE_BLOCKS = [
    {
        "title": "The Short Read",
        "body": (
            "The economy in 2025-2026 still has demand, but it has fewer easy places to turn demand "
            "into durable profit. Labor is scarce, capital is more selective, AI is both software "
            "and infrastructure, consumers are split between value and premium, and regulation plus "
            "reimbursement are steering more industries than they first appear to."
        ),
    },
    {
        "title": "What Keeps Repeating",
        "body": (
            "Across the corpus, the same pressures keep showing up: labor scarcity, demographic aging, "
            "consumer bifurcation, platform channel shift, health behavior change, AI-driven workflow "
            "compression, power and data-center buildout, political supply chains, and consolidation "
            "as the answer to rising complexity."
        ),
    },
    {
        "title": "What Operators Need To Know",
        "body": (
            "Most businesses are no longer constrained by demand alone. They are constrained by labor, "
            "power, compliance, reimbursement, capital, or channel access. The right question is not "
            "just whether a market is growing. It is whether the operator has the structure to capture "
            "that growth without getting squeezed."
        ),
    },
]


CSS = """
:root{--bg:#0e1218;--panel:#151b23;--panel2:#1b2531;--line:#27313f;--line2:#1f2935;--ink:#efe8da;--muted:#a5afbc;--faint:#6f7a89;--gold:#d3ab55;--green:#71c58b;--blue:#77a7dc;--red:#df806e;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,40px) 72px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:34px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.3rem,5vw,4.1rem);line-height:1;margin:.18em 0 .22em;max-width:11ch}h2{font-size:1.5rem;margin:0 0 .45em}.sub{max-width:850px;color:var(--muted);font-size:1.07rem}.strip{display:flex;gap:10px;flex-wrap:wrap;margin:22px 0 0}.kpi{background:var(--panel);border:1px solid var(--line2);border-radius:10px;padding:10px 14px;min-width:120px}.kpi .n{font-family:var(--mono);font-size:1.34rem;font-weight:700}.kpi .l{font-size:.68rem;text-transform:uppercase;letter-spacing:.08em;color:var(--faint);margin-top:1px}.lead{background:var(--panel);border:1px solid var(--line2);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;color:var(--ink);font-size:1.06rem}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line2)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(285px,1fr));gap:14px}.card,.story,.force{background:var(--panel);border:1px solid var(--line2);border-radius:10px;padding:18px}.card h3,.story h3,.force h3{margin:0 0 .35em;font-size:1.12rem}.card p,.story p,.force p{margin:.35em 0 0;color:var(--muted)}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.qs,.chips{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 9px}.force .count{font-family:var(--mono);font-size:.72rem;color:var(--faint);margin-top:.7em}.split{display:grid;grid-template-columns:minmax(0,1.05fr) minmax(280px,.95fr);gap:18px}.stack>*+*{margin-top:12px}@media(max-width:880px){.split{grid-template-columns:1fr}}footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line2);color:var(--faint);font-family:var(--mono);font-size:.72rem}
"""


def build_domain_card(domain):
    force_chips = "".join(f'<span class="chip">{e(f["title"])}</span>' for f in domain["forces"])
    return f"""<article class="card">
  <div class="meta">{e(domain['title'])}</div>
  <h3>{e(domain['title'])}</h3>
  <p>{e(domain['description'])}</p>
  <div class="chips">{force_chips}</div>
</article>"""


def build_force_card(force):
    return f"""<article class="force">
  <div class="meta">{e(force['repo_lens'])}</div>
  <h3>{e(force['title'])}</h3>
  <p>{e(force['signature'])}</p>
  <div class="count">{force['subforce_count']} subforces · {force['evidence_slug_count']} evidence industries</div>
</article>"""


def build_operator_card(operator):
    questions = "".join(f"<span class=\"chip\">{e(q)}</span>" for q in operator["operator_questions"][:2])
    return f"""<article class="card">
  <div class="meta">{e(operator['lens'])}</div>
  <h3>{e(operator['title'])}</h3>
  <p>{e(operator['thesis'])}</p>
  <div class="chips">{questions}</div>
</article>"""


def main():
    taxonomy = json.load(open(os.path.join(ROOT, "economic_intelligence_taxonomy.json"), encoding="utf-8"))
    domains = taxonomy["domains"]
    forces = [force for domain in domains for force in domain["forces"]]
    unique_forces = {f["slug"]: f for f in forces}
    operators = {op["slug"]: op for domain in domains for op in domain["operators"]}

    domain_cards = "\n".join(build_domain_card(d) for d in domains)
    force_cards = "\n".join(build_force_card(f) for f in unique_forces.values())
    operator_cards = "\n".join(build_operator_card(o) for o in operators.values())
    story_cards = "\n".join(
        f"""<article class="story"><h3>{e(block['title'])}</h3><p>{e(block['body'])}</p></article>"""
        for block in NARRATIVE_BLOCKS
    )
    crosscuts = "".join(f'<span class="chip">{e(c["title"])}</span>' for c in taxonomy["crosscuts"])

    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Economic Intelligence — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="forces/index.html">Forces</a><a href="operators.html">Operator playbooks</a><a href="american-themes.html">American themes</a></div>
<div class="eyebrow">Economic intelligence · US · 2025–2026</div>
<h1>Economic Intelligence</h1>
<p class="sub">{e(INTRO)}</p>
<div class="strip">
  <div class="kpi"><div class="n">{taxonomy['metadata']['industry_brief_count']}</div><div class="l">Industries</div></div>
  <div class="kpi"><div class="n">{taxonomy['metadata']['force_count']}</div><div class="l">Forces</div></div>
  <div class="kpi"><div class="n">{len(domains)}</div><div class="l">Domains</div></div>
  <div class="kpi"><div class="n">{taxonomy['metadata']['operator_playbook_count']}</div><div class="l">Operator lenses</div></div>
</div>
<div class="lead"><p>{e(taxonomy['working_thesis'])}</p></div>

<section class="section">
  <h2>The Read</h2>
  <div class="split">
    <div class="stack">{story_cards}</div>
    <div class="card">
      <div class="meta">Crosscuts</div>
      <h3>What Repeats Across Domains</h3>
      <p>These are the recurring pressures that show up across industrial, consumer, social, and institutional markets at the same time.</p>
      <div class="chips">{crosscuts}</div>
    </div>
  </div>
</section>

<section class="section">
  <h2>Domains</h2>
  <div class="grid">{domain_cards}</div>
</section>

<section class="section">
  <h2>Forces</h2>
  <div class="grid">{force_cards}</div>
</section>

<section class="section">
  <h2>Themes</h2>
  <div class="card">
    <div class="meta">Interpretation layer</div>
    <h3><a href="american-themes.html">American Themes</a></h3>
    <p>{e(AMERICAN_THEMES_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Narrative layer</div>
    <h3><a href="american-theme-briefs.html">American Theme Briefs</a></h3>
    <p>{e(AMERICAN_THEME_BRIEFS_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Master synthesis</div>
    <h3><a href="american-outlook-2025-2026.html">American Outlook 2025-2026</a></h3>
    <p>{e(AMERICAN_OUTLOOK_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Applied macro layer</div>
    <h3><a href="american-outlook-memos.html">American Outlook Memos</a></h3>
    <p>{e(AMERICAN_OUTLOOK_MEMOS_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Capstone narrative</div>
    <h3><a href="american-economy-2025-2026.html">The US Economy in 2025-2026</a></h3>
    <p>{e(AMERICAN_CAPSTONE_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Applied layer</div>
    <h3><a href="american-theme-memos.html">American Theme Memos</a></h3>
    <p>{e(AMERICAN_THEME_MEMOS_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Sector layer</div>
    <h3><a href="sector-memos.html">Sector Memos</a></h3>
    <p>{e(SECTOR_MEMOS_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Sector outlook layer</div>
    <h3><a href="sector-outlooks.html">Sector Outlooks</a></h3>
    <p>{e(SECTOR_OUTLOOKS_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Company layer</div>
    <h3><a href="company-memos.html">Company Memos</a></h3>
    <p>{e(COMPANY_MEMOS_LINK)}</p>
  </div>
</section>

<section class="section">
  <h2>Subthemes</h2>
  <div class="card">
    <div class="meta">Inside the forces</div>
    <h3><a href="subthemes.html">Subtheme Index</a></h3>
    <p>{e(SUBTHEMES_LINK)}</p>
  </div>
</section>

<section class="section">
  <h2>Operator Lenses</h2>
  <div class="grid">{operator_cards}</div>
</section>

<section class="section">
  <h2>Decision Layer</h2>
  <div class="grid">
  <div class="card">
    <div class="meta">Force to operator</div>
    <h3><a href="force-operator-translations.html">Force-to-Operator Translations</a></h3>
    <p>{e(TRANSLATION_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Business archetypes</div>
    <h3><a href="business-lenses.html">Business Lenses</a></h3>
    <p>{e(BUSINESS_LENSES_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Applied cases</div>
    <h3><a href="sector-cases.html">Sector Cases</a></h3>
    <p>{e(SECTOR_CASES_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Business profiles</div>
    <h3><a href="business-profiles.html">Business Profiles</a></h3>
    <p>{e(BUSINESS_PROFILES_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Company universe</div>
    <h3><a href="company-universe.html">Company Universe</a></h3>
    <p>{e(COMPANY_UNIVERSE_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Company clusters</div>
    <h3><a href="company-clusters.html">Company Clusters</a></h3>
    <p>{e(COMPANY_CLUSTERS_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Company scoreboard</div>
    <h3><a href="company-scoreboard.html">Company Scoreboard</a></h3>
    <p>{e(COMPANY_SCOREBOARD_LINK)}</p>
  </div>
  <div class="card">
    <div class="meta">Company comparisons</div>
    <h3><a href="company-comparisons.html">Company Comparisons</a></h3>
    <p>{e(COMPANY_COMPARISONS_LINK)}</p>
  </div>
  </div>
</section>

<footer>Built from the completed 1,491-industry corpus and the generated force/operator taxonomy. This page is the surfaced interpretation layer linking briefs, forces, and operator playbooks.</footer>
</div></body></html>"""
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(html_doc)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
