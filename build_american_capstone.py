#!/usr/bin/env python3
"""Build a capstone synthesis page for the American themes system."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
OUT = ROOT / "american-economy-2025-2026.html"


CAPSTONE = {
    "title": "The US Economy in 2025-2026",
    "subtitle": (
        "A capstone synthesis built from the 1,491-industry corpus, the force system, "
        "the detailed American themes taxonomy, and the theme-brief interpretation layer."
    ),
    "thesis": (
        "The US economy in 2025-2026 still has demand, but it has fewer easy ways to turn "
        "demand into durable profit. Labor is scarce, capital is more selective, AI is both "
        "software and infrastructure, households are split between value and premium, health "
        "behavior is changing consumption, aging is shifting spend into assistance systems, "
        "and scale keeps winning because complexity keeps rising."
    ),
    "sections": [
        {
            "slug": "margin-rights-get-narrower",
            "title": "1. The Right To Earn Margin Is Narrowing",
            "summary": (
                "The most important macro conclusion is not that demand disappeared. It is that "
                "the conditions required to capture attractive economics from that demand became "
                "harder to satisfy."
            ),
            "body": [
                "Across the corpus, many markets still have volume, need, or foot traffic. What changed is that more businesses now have to clear a higher bar to turn that activity into durable profit. They need labor they can actually find, costs they can pass through, software or workflows they can absorb, and enough purchasing, distribution, or brand leverage to keep rising complexity from overwhelming them.",
                "This is why so many seemingly unrelated sectors converge on the same operating reality. The winning structure is increasingly the one that can metabolize friction: procurement friction, staffing friction, reimbursement friction, compliance friction, capital-cost friction, and platform-access friction. Demand is not enough. Structure matters more.",
                "In practice, that means the broad middle of the economy looks more fragile. Generic retailers, undifferentiated service businesses, weak intermediaries, and labor-heavy operators without pricing power all face a much narrower path than businesses with scale, scarcity, specification, or deep embeddedness in required workflows.",
            ],
            "linked_themes": [
                "scale-financialization-and-the-owned-economy",
                "regulated-software-and-admin-state",
                "physical-reindustrialization-and-infrastructure",
            ],
        },
        {
            "slug": "the-household-splits",
            "title": "2. The Household Splits Into Multiple Economic Personalities",
            "summary": (
                "Consumers are not acting like one bloc anymore. They are editing aggressively, "
                "saving hard in some categories and still spending decisively in others."
            ),
            "body": [
                "The consumer economy now makes more sense when read as a set of filters than as a single confidence level. Value matters more in routine and interchangeable categories. Premium still works where trust, aesthetics, self-reward, or visible quality remain legible. Convenience still commands spend when it saves time or cognitive load. Health changes what even counts as acceptable consumption. Experiences keep winning where they carry identity and memory.",
                "This means the old middle keeps losing coherence. Shoppers increasingly refuse to subsidize undifferentiated mid-tier products and formats. They will trade down without embarrassment where substitution feels easy, and they will still pay up where the category feels symbolic, social, or useful enough to deserve the money.",
                "The deeper social change is that prudence and aspiration now coexist inside the same person. That makes consumer behavior less stable but more interpretable: households are not giving up on consumption. They are ranking it more selectively.",
            ],
            "linked_themes": [
                "barbelled-consumer-america",
                "wellness-recodes-daily-life",
                "experience-status-and-community",
            ],
        },
        {
            "slug": "culture-is-not-soft",
            "title": "3. Cultural Change Is Now Visible as Economic Structure",
            "summary": (
                "Culture is not background context in this corpus. It is demand logic, labor logic, "
                "and category logic."
            ),
            "body": [
                "Health is becoming a broad social classifier, not only a medical issue. Participation and experience are becoming stronger carriers of status than many broad goods categories. Work identity is becoming thinner and more modular. Each of these shifts changes where money goes and how operators need to think about loyalty, aspiration, and habit.",
                "That matters because more categories now require reading through social meaning, not just price elasticity. Sober-curious norms affect nightlife economics. GLP-1 use affects fast food and packaged snacks. Fandom changes hobby and leisure demand. Platform-mediated comparison shopping alters what consumers consider fair or worth paying for. Retail survives better where it behaves like theater, service, or curation.",
                "The result is an economy where seemingly soft social changes keep turning into hard sector outcomes. Businesses that ignore cultural reclassification end up describing their markets with old language while demand has already moved on.",
            ],
            "linked_themes": [
                "wellness-recodes-daily-life",
                "experience-status-and-community",
                "work-without-the-old-firm",
            ],
        },
        {
            "slug": "assistance-state-expands",
            "title": "4. An Older, More Managed America Expands the Assistance Economy",
            "summary": (
                "Aging and institutional complexity are steering more of the economy than many "
                "headline narratives admit."
            ),
            "body": [
                "The country is moving deeper into sectors where demand is obvious but monetization is conditional. Aging pushes need into care, devices, housing, insurance, chronic-disease management, and family support. But these sectors are not governed by raw consumer willingness to pay alone. They are governed by staffing limits, payer constraints, reimbursement coding, compliance, and operational coordination.",
                "That makes assistance a central organizing theme. More care leaves hospitals and moves into homes, outpatient settings, logistics systems, and admin stacks. More value flows toward businesses that reduce family friction, manage documentation, navigate reimbursement, or supply bottleneck inputs rather than toward every frontline operator equally.",
                "This is one reason the economy increasingly rewards businesses that know how to operate inside systems. In many institutional markets, the real skill is not just serving demand. It is surviving the rules that shape how that demand can be paid for and delivered.",
            ],
            "linked_themes": [
                "aging-care-and-the-assistance-economy",
                "regulated-software-and-admin-state",
                "space-housing-and-local-friction",
            ],
        },
        {
            "slug": "the-firm-thins-the-stack-thickens",
            "title": "5. The Firm Thins While the Supporting Stack Thickens",
            "summary": (
                "Companies are internalizing less, renting more, and leaning harder on external "
                "software, service, and workflow layers."
            ),
            "body": [
                "Labor scarcity, better coordination tools, and AI-assisted workflows are pushing firms toward thinner permanent cores. Senior expertise is rented fractionally, repeatable white-collar tasks are compressed, and junior ladders look weaker in many categories. Benefits and stability increasingly sit with the worker instead of the employer.",
                "At the same time, the external stack gets thicker. Payroll, HR, claims, identity, fraud control, managed compliance, workflow software, credentialing, and outsourced expertise all gain importance as firms stop trying to own every capability themselves. This makes the economy look more flexible from the top, but more fragmented from below.",
                "The strategic implication is that more value may sit around the firm than inside the traditional firm. Workflow platforms, admin layers, compliance infrastructure, and selective expert networks can become more attractive than many businesses that once seemed to own the whole relationship directly.",
            ],
            "linked_themes": [
                "work-without-the-old-firm",
                "regulated-software-and-admin-state",
                "machine-intelligence-and-compute-buildout",
            ],
        },
        {
            "slug": "ai-is-physical",
            "title": "6. AI Is a Software Story Sitting on a Physical Constraint System",
            "summary": (
                "AI does not only reward application builders. It also reprices power, land, "
                "transmission, cooling, and the trades that support the stack."
            ),
            "body": [
                "The easy mistake is to isolate AI as a software vertical. The corpus says otherwise. AI is a workflow-compression story, a labor-substitution story, a control-layer story, and a heavy physical buildout story at the same time. It creates winners in software and admin, but it also creates winners in utilities, construction, cooling, electrical work, equipment, and infrastructure-linked real estate.",
                "This matters because digital growth now depends on very non-digital bottlenecks. Power-ready land, transmission, generation, cooling, and permitting are becoming strategic choke points. The players that control those constraints may capture more value than some of the companies that look more glamorous from a distance.",
                "It also means AI deepens concentration. The capital and infrastructure needed to operate at the frontier favor a relatively small set of owners. Many smaller businesses will still benefit, but mostly by embedding AI into boring workflows rather than by competing to own the whole upstream stack.",
            ],
            "linked_themes": [
                "machine-intelligence-and-compute-buildout",
                "physical-reindustrialization-and-infrastructure",
                "regulated-software-and-admin-state",
            ],
        },
        {
            "slug": "place-matters-again",
            "title": "7. Geography Matters More Again, Just in Different Ways",
            "summary": (
                "Housing lock-in, office impairment, logistics demand, and utility-linked land "
                "are producing a new geography of advantage and friction."
            ),
            "body": [
                "The digital economy did not abolish place. It changed which places matter. Commodity office space is weaker. Adaptive reuse is more important. Housing scarcity keeps households in place longer. Neighborhood and suburban convenience patterns strengthen as old downtown assumptions weaken. Logistics corridors, utility-rich sites, and power-linked land gain strategic rent.",
                "This makes local friction more economically important. When households cannot move easily, labor mobility suffers. When office traffic thins, surrounding service ecosystems have to rebase demand. When data-center and industrial buildouts cluster around scarce infrastructure, land and utility access stop being neutral background variables.",
                "In short, place is back as a live economic differentiator. Not every location wins the same way, but geography once again affects labor, asset values, service density, and industrial optionality.",
            ],
            "linked_themes": [
                "space-housing-and-local-friction",
                "physical-reindustrialization-and-infrastructure",
                "machine-intelligence-and-compute-buildout",
            ],
        },
        {
            "slug": "complexity-picks-the-winners",
            "title": "8. Complexity Keeps Selecting for Scale, Systems, and Scarcity",
            "summary": (
                "The single recurring selector across the corpus is complexity. As it rises, "
                "the advantaged positions are the ones with scale, system control, or true scarcity."
            ),
            "body": [
                "Procurement is harder. Compliance is heavier. Staffing is tougher. Capital is dearer. Technology is more mandatory. Reimbursement is more managed. Channel access is more mediated. These are all forms of rising complexity, and they repeatedly reward operators who can spread fixed burden across larger systems or who occupy truly scarce niches.",
                "That is why scale keeps appearing as an economic answer in retail, finance, healthcare, logistics, industrial production, and services. It does not mean every large company wins. It means that when complexity rises, size and systems become more valuable inputs. Small operators can still succeed, but usually only where they have local scarcity, expert trust, premium defensibility, or specified niche demand.",
                "The big picture, then, is not only that America is changing. It is that the economic selection mechanism is changing. The economy is becoming harsher on the generic middle and more rewarding to the player that either owns the system, runs inside the right bottleneck, or becomes culturally or operationally indispensable.",
            ],
            "linked_themes": [
                "scale-financialization-and-the-owned-economy",
                "barbelled-consumer-america",
                "physical-reindustrialization-and-infrastructure",
                "regulated-software-and-admin-state",
            ],
        },
    ],
    "closing": [
        "Taken together, these themes describe a country that is not simply booming or weakening. It is being reorganized. Daily life, institutions, technology, labor, and industrial capacity are all shifting at once, and the boundaries between them are getting thinner.",
        "The most reliable way to read this economy is to ask a more demanding question than whether demand exists. Ask what governs the right to capture it. In 2025-2026, that answer increasingly comes back to labor, system complexity, cultural alignment, power access, institutional fluency, and scale.",
        "That is the core claim of this repo: the important economic story is not any single sector. It is the repeating structure that links them.",
    ],
}


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.63}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.5rem,5vw,4.4rem);line-height:.98;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.4rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.06rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:16px;border-top:1px solid var(--line)}.essay{margin-top:18px}.essay h3{font-size:1.36rem;margin:.1em 0 .45em}.essay p{color:var(--muted);margin:.6em 0 0}.summary{font-size:1rem;color:var(--ink)}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3{margin:.2em 0 .35em;font-size:1.1rem}.card p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.close{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px;margin-top:16px}.close p{color:var(--muted);margin:.55em 0 0}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_theme_lookup() -> dict[str, dict]:
    with THEMES_JSON.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return {theme["slug"]: theme for theme in data["themes"]}


def build_chip(theme_lookup: dict[str, dict], slug: str) -> str:
    theme = theme_lookup[slug]
    return f'<a class="chip" href="theme-briefs/{e(slug)}.html">{e(theme["title"])}</a>'


def main() -> None:
    theme_lookup = load_theme_lookup()
    sections = []
    cards = []
    for section in CAPSTONE["sections"]:
        chips = "".join(build_chip(theme_lookup, slug) for slug in section["linked_themes"])
        body = "".join(f"<p>{e(paragraph)}</p>" for paragraph in section["body"])
        sections.append(
            f"""<section class="essay" id="{e(section['slug'])}">
  <div class="meta">Capstone synthesis</div>
  <h3>{e(section['title'])}</h3>
  <p class="summary">{e(section['summary'])}</p>
  {body}
  <div class="chips">{chips}</div>
</section>"""
        )
        cards.append(
            f"""<article class="card">
  <div class="meta">Capstone section</div>
  <h3><a href="#{e(section['slug'])}">{e(section['title'])}</a></h3>
  <p>{e(section['summary'])}</p>
  <div class="chips">{chips}</div>
</article>"""
        )

    closing = "".join(f"<p>{e(paragraph)}</p>" for paragraph in CAPSTONE["closing"])

    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(CAPSTONE['title'])} — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="american-themes.html">American themes</a><a href="american-theme-briefs.html">Theme briefs</a></div>
<div class="eyebrow">Capstone narrative · US · 2025-2026</div>
<h1>{e(CAPSTONE['title'])}</h1>
<p class="sub">{e(CAPSTONE['subtitle'])}</p>
<div class="kpis">
  <div class="kpi"><div class="n">1491</div><div class="l">Industry briefs</div></div>
  <div class="kpi"><div class="n">14</div><div class="l">Forces</div></div>
  <div class="kpi"><div class="n">10</div><div class="l">Themes</div></div>
  <div class="kpi"><div class="n">8</div><div class="l">Capstone sections</div></div>
</div>
<div class="lead"><p>{e(CAPSTONE['thesis'])}</p></div>

<section class="section">
  <h2>Map</h2>
  <div class="grid">{''.join(cards)}</div>
</section>

<section class="section">
  <h2>The Argument</h2>
  {''.join(sections)}
</section>

<section class="section">
  <h2>Closing Read</h2>
  <div class="close">{closing}</div>
</section>

</div></body></html>"""

    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(html_doc)

    print(f"wrote {OUT}")
    print(f"sections={len(CAPSTONE['sections'])}")


if __name__ == "__main__":
    main()
