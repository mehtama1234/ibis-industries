#!/usr/bin/env python3
"""Build long-form synthesis briefs for the American themes layer."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
OUT = ROOT / "american-theme-briefs.html"
BRIEFS_DIR = ROOT / "theme-briefs"


BRIEFS = {
    "barbelled-consumer-america": {
        "hook": "The most important consumer fact in the corpus is not that Americans stopped spending. It is that they stopped spending as one bloc.",
        "long_read": [
            "The center of mass in consumer markets keeps getting weaker. Households still spend, but they increasingly do it through two different logics. One is defensive: visible value, lower risk, reliable replenishment, fewer wasted trips, and less buyer's remorse. The other is selective and aspirational: categories where quality, aesthetics, trust, or self-reward still justify the premium. What keeps breaking is the generic middle, where the product is neither distinctly cheap nor distinctly worth paying up for.",
            "That makes consumer competition more brutal than a simple slowdown story would imply. Operators are not just fighting for fewer dollars. They are being forced to declare what they are. A chain, brand, or format that cannot tell the shopper whether it is the prudent choice or the special choice gets dragged into permanent promotional defense. This is why the middle tier looks fragile in department stores, apparel, furniture, and broadline general merchandise while value formats, memberships, and certain premium niches still hold up.",
            "The deeper social point is that frugality and aspiration are now coexisting inside the same household. Consumers are not consistently trading down or consistently premiumizing. They are editing. They save aggressively on categories that feel interchangeable so they can still spend on categories that feel identity-bearing, convenient, or emotionally distinct.",
        ],
        "structural_shifts": [
            "Value is increasingly judged through total-trip economics, not only sticker price.",
            "Premium only survives where the buyer can explain the difference to themselves or to others.",
            "Private label and dupe behavior are reducing the shame once attached to imitation or trade-down.",
            "Platform discovery and comparison tools make weak middle positioning easier to expose.",
        ],
        "tensions": [
            "Retailers want margin but shoppers want proof of prudence.",
            "Brands want loyalty but consumers are getting more comfortable with substitution.",
            "Physical stores still matter, but only when they help with trust, service, or experience.",
        ],
        "watchpoints": [
            "Whether mid-tier brands can rebuild identity without living on discounting.",
            "How far private label expands into categories once protected by branding.",
            "Which consumer categories preserve real premium power after health and convenience filters intensify.",
        ],
    },
    "wellness-recodes-daily-life": {
        "hook": "Health has stopped acting like a silo. It is now a cultural sorting mechanism for daily consumption.",
        "long_read": [
            "The strongest signal in food, drink, beauty, and adjacent services is that wellness is no longer a niche preference held by a thin upper-income cohort. It is becoming a mass behavior filter. Consumers are using health to decide what feels responsible, modern, attractive, disciplined, or socially legible. That shifts demand even where no regulator forces it and even where income alone would not have predicted it.",
            "GLP-1s sharpen this shift because they alter both appetite and the social narrative around appetite. Sober-curious behavior does something similar for nightlife and beverage mix. Functional drinks and protein-forward or nutrient-forward products do it for packaged consumption. Together they create a world in which indulgence still exists, but now needs explanation, reformulation, portion control, or premium framing to remain durable.",
            "The bigger implication is that health behavior is now crossing into identity behavior. People increasingly buy products that help them feel aligned with a version of themselves that is more optimized, more controlled, more future-oriented, or at least less obviously self-destructive. That makes wellness not just a product trend, but a reclassification of what ordinary daily life should look like.",
        ],
        "structural_shifts": [
            "Pharma is affecting mainstream food and beverage demand.",
            "Alcohol moderation is moving from stigma to visible social normality.",
            "Functional claims increasingly matter more than pure indulgence cues.",
            "Beauty, fitness, and medicalized self-improvement are blending together.",
        ],
        "tensions": [
            "Consumers still want pleasure, but they increasingly want permission structures around it.",
            "Legacy vice categories retain scale, but their cultural footing looks weaker.",
            "Operators want to charge premium prices for wellness, but buyers punish vague claims.",
        ],
        "watchpoints": [
            "The pace at which GLP-1 effects show up in mainstream restaurant and packaged-food volumes.",
            "How far nonalcoholic and functional beverage categories cannibalize traditional alcohol spend.",
            "Whether wellness remains premium-coded or becomes a default expectation across mass channels.",
        ],
    },
    "experience-status-and-community": {
        "hook": "The consumer economy is increasingly paying out to participation, not just possession.",
        "long_read": [
            "Status is not disappearing. It is moving. More of it is now expressed through experiences, affiliation, aesthetics, curation, and participation in scenes or communities rather than through broad mid-tier product ownership. This helps explain why the same economy can show softness in generic goods while still supporting live events, destination leisure, fandom-driven spend, and stores that behave more like stages than shelves.",
            "Digital life is part of the reason. When so much attention is mediated, in-person presence and memory become more valuable as social currency. That makes venues, hospitality formats, outdoor recreation, hobby ecosystems, and other participation-based categories more economically important than a simple discretionary label suggests. They are not just leisure purchases. They are where identity gets performed and stored.",
            "This does not mean every experience business wins. It means the categories with scarcity, programming, community, or symbolic weight have stronger pricing logic than generic capacity. A venue, retail format, or leisure operator now needs to answer a cultural question: why does this visit matter beyond the transaction itself?",
        ],
        "structural_shifts": [
            "Memory and shareability have become part of the product.",
            "Retail survives best where it behaves like discovery, service, or theater.",
            "Fandom and affiliation create deeper spending loops than generic categories.",
            "Older consumers are sustaining experience demand rather than aging out of it immediately.",
        ],
        "tensions": [
            "Experience categories need novelty without sacrificing repeatability.",
            "Physical venues can gain power, but only if they avoid becoming interchangeable.",
            "Goods still matter, but they increasingly compete against live time and attention.",
        ],
        "watchpoints": [
            "Which physical formats build true recurring communities rather than one-off traffic.",
            "How much outdoor and leisure demand continues to benefit from active aging.",
            "Whether more retailers can turn stores into cultural or service assets instead of inventory boxes.",
        ],
    },
    "aging-care-and-the-assistance-economy": {
        "hook": "Aging is one of the clearest demand stories in the corpus, but it is not an easy profit story.",
        "long_read": [
            "The United States is moving deeper into an assistance economy. Older households need more care, more monitoring, more chronic-disease management, more insurance, more planning, and more physical or administrative support. That much is obvious. What is less obvious, but more important, is that this demand arrives in sectors where reimbursement, staffing, and operational coordination are often the real constraints.",
            "That makes aging different from a naive growth narrative. Businesses tied to older Americans can be demand-rich and return-poor at the same time. Home care can grow while struggling to hire. Senior housing can face strong need while fighting wage pressure and uneven unit economics. Chronic-care categories can scale while remaining tightly rationed by payer math. The signal is not simply that aging creates spend. It is that aging increases the weight of sectors where coordination and institutional control decide who gets paid.",
            "The broader social consequence is that families, payers, and operators all feel the burden at once. More care leaves the hospital and moves into homes and outpatient settings, but that only redistributes the complexity. The result is a larger assistance economy where the most attractive positions often sit in enabling infrastructure, reimbursement competence, and bottleneck inputs rather than in labor-heavy frontline care alone.",
        ],
        "structural_shifts": [
            "Home-first aging is redistributing care work across families, aides, devices, and logistics.",
            "Care categories are becoming more industrialized and operationally standardized.",
            "Payer control is shaping demand capture as much as underlying demographic need.",
            "Longevity is expanding the overlap between healthcare, insurance, and financial planning.",
        ],
        "tensions": [
            "Demand is rising, but staffing remains the binding constraint.",
            "Public and private payers ration economics even when patient need is obvious.",
            "Families want aging in place, but distributed care creates coordination strain.",
        ],
        "watchpoints": [
            "Where home-based models can truly scale without collapsing under labor intensity.",
            "How payer pressure changes the economics of senior-focused service categories.",
            "Which enabling layers around chronic care and family coordination capture durable value.",
        ],
    },
    "work-without-the-old-firm": {
        "hook": "The old promise that a stable firm would internalize training, benefits, and career progression is weakening.",
        "long_read": [
            "The corpus points to a labor market where firms increasingly buy capability in fragments. Senior expertise is rented on a project basis. Functions that once sat inside the company move to agencies, consultants, platforms, or software. Junior work gets compressed by automation, offshoring, or cautious hiring. Benefits and predictability drift away from the employer and toward the worker's own balance sheet.",
            "This is not just a gig-economy story. It is a broader thinning of the firm. Employers want optionality because labor is expensive, uncertain, and often augmented by better software. Workers respond by buying credentials, chasing flexible arrangements, or stitching income and identity together across multiple roles. The result is a labor market that can look more efficient from the top and more unstable from the bottom.",
            "The deeper economic issue is that institutional training capacity gets weaker when every employer wants talent but fewer want to build it patiently. That is why the user-facing story about AI and productivity should be read together with the social story about thinner ladders, weaker apprenticeships, and rising dependence on modular expertise. The efficiency gain is real. So is the distributional cost.",
        ],
        "structural_shifts": [
            "Fractional leadership and rented expertise are becoming normal operating choices.",
            "Credential markets are expanding as workers self-fund employability.",
            "Entry-level white-collar pathways are narrowing in many workflow-heavy sectors.",
            "Automation is increasingly justified as labor arbitrage and reliability insurance.",
        ],
        "tensions": [
            "Firms want flexibility while workers still need stability.",
            "Automation improves throughput but can weaken long-run talent formation.",
            "Credentialing expands, but it does not always replace deep employer training.",
        ],
        "watchpoints": [
            "Which sectors rebuild meaningful apprenticeships or junior pathways.",
            "Whether portable-benefit and administrative-support businesses grow fast enough to meet fragmented work patterns.",
            "How much AI adoption reduces headcount versus simply raises output expectations.",
        ],
    },
    "physical-reindustrialization-and-infrastructure": {
        "hook": "The physical economy is no longer background plumbing. It is back at the center of strategic advantage.",
        "long_read": [
            "Across the corpus, tariffs, power demand, reshoring pressure, infrastructure spending, and logistics complexity keep pointing to the same conclusion: the United States is repricing the physical side of the economy. Materials, land, transmission access, freight capacity, and specific skilled trades all matter more than they did when global supply chains were treated as neutral and abundant.",
            "This does not mean a clean return to old manufacturing romanticism. It means the businesses on the right side of physical bottlenecks have more leverage. Electrical contractors, cooling specialists, transmission-linked assets, specified manufacturers, logistics land, and certain domestic producers are all benefiting because scarcity moved closer to the real economy. Supply chains are more political, more capital-intensive, and less forgiving of naive sourcing assumptions.",
            "The strategic lesson is that the industrial winners in this period are not just the companies with demand. They are the ones with access: access to power, to labor, to compliant production, to domestic or nearshore resilience, and to the procurement or capital discipline needed to operate through volatility. The buildout story is real, but it is distributed across many boring bottlenecks rather than concentrated only in headline factories.",
        ],
        "structural_shifts": [
            "Tariffed and politicized inputs are reshaping downstream economics.",
            "Power access is becoming a first-order industrial location variable.",
            "Electrical, cooling, and heavy construction trades sit inside multiple secular buildouts at once.",
            "Specified domestic manufacturing is regaining strategic value in complex categories.",
        ],
        "tensions": [
            "Political desire for domestic capacity collides with labor and capital constraints.",
            "Physical buildout demand is strong, but many enabling categories remain bottlenecked.",
            "Reshoring narratives can outrun the economics unless specification or security really matters.",
        ],
        "watchpoints": [
            "How much power scarcity constrains both AI and broader industrial expansion.",
            "Which trade and equipment bottlenecks keep capturing the most value.",
            "Whether procurement discipline becomes a clearer separator between winners and losers.",
        ],
    },
    "scale-financialization-and-the-owned-economy": {
        "hook": "A growing share of the economy is being won by the owner of the system rather than the visible operator inside it.",
        "long_read": [
            "The corpus repeatedly shows that scale, ownership structure, and financial control matter more than many sector narratives admit. Fragmented categories across healthcare, services, retail, property, and finance are increasingly being reorganized by roll-ups, institutional ownership, platform control, and governance layers that sit above the frontline operator. The visible business may still look local or sector-specific, but the economics often flow upward to the scaled owner or orchestrator.",
            "This is partly a rate and compliance story. As software, regulatory, labor, and procurement burdens rise, scale does more than produce vanity. It spreads overhead, improves buying power, lowers financing cost, and turns complexity into something manageable. That makes independents and mid-sized intermediaries more fragile, especially where customers no longer reward localness by itself.",
            "The deeper implication is that markets increasingly need to be read through ownership topology. Who owns the land? Who owns the rail? Who controls the franchise terms? Who aggregates the data? Who sits between the fragmented edge and the centralized stack? In many sectors, that owner captures more durable value than the operator who looks more visible from the outside.",
        ],
        "structural_shifts": [
            "Essential services keep moving from fragmented ownership into managed platforms.",
            "Asset owners and rail owners often gain relative leverage over frontline operators.",
            "Regional intermediaries face pressure from both scaled incumbents and embedded digital alternatives.",
            "Institutional procurement and finance widen the gap between large and small operators.",
        ],
        "tensions": [
            "Scale solves complexity, but it can flatten local differentiation.",
            "Independent operators still exist, but they increasingly need sharp specialization.",
            "The owner and the operator can have diverging incentives even in the same asset.",
        ],
        "watchpoints": [
            "Which fragmented categories are still genuinely hospitable to independents.",
            "Where platform governance becomes more extractive than enabling.",
            "How often asset-control businesses outperform the operating businesses built on top of them.",
        ],
    },
    "regulated-software-and-admin-state": {
        "hook": "One of the most durable growth engines in the corpus is the need to manage complexity that customers cannot simply opt out of.",
        "long_read": [
            "A surprising amount of economic value now comes from mandatory workflows. Compliance, identity, fraud control, reimbursement, testing, reporting, privacy, cybersecurity, audit trails, and certification all create demand that is only partly tied to macro growth. Customers often pay not because they want to, but because they must. That makes regulated workflow businesses structurally different from ordinary discretionary software or services.",
            "This layer matters because the administrative burden of the economy keeps thickening. Healthcare billing and coding grow more complex. Financial identity and fraud systems become more critical as scams industrialize. Cyber controls, documentation, and audit readiness move downmarket. Environmental, safety, and technical standards keep expanding the zones where formal compliance becomes a gate to participation.",
            "The important strategic divide is between businesses that can turn this complexity into repeatable infrastructure and those that still deliver it through expensive bespoke labor. The first category can become a toll-taking layer with recurring economics. The second may still benefit from demand, but it remains vulnerable to margin pressure. In other words, the admin state creates a lot of work, but the highest-value positions are the ones that productize that work.",
        ],
        "structural_shifts": [
            "Compliance demand is acting more like a permanent revenue layer than a cyclical add-on.",
            "Identity, verification, and fraud control are becoming deeper infrastructure markets.",
            "Healthcare and other regulated sectors are monetizing administrative throughput, not just core service delivery.",
            "Testing and certification bodies are quietly gaining gatekeeper power.",
        ],
        "tensions": [
            "Customers resent compliance spending even as they cannot avoid it.",
            "Manual service demand can be strong while still producing mediocre margins.",
            "AI can compress administrative work, but regulated customers still need auditability and trust.",
        ],
        "watchpoints": [
            "Which compliance-heavy categories become true software rails rather than labor-heavy service shops.",
            "How fraud and cyber risk keep expanding the trust infrastructure market.",
            "Where mandatory workflow vendors gain pricing power because they become hard to displace.",
        ],
    },
    "space-housing-and-local-friction": {
        "hook": "Geography is not dead. It is being repriced in more uneven and more consequential ways.",
        "long_read": [
            "Housing lock-in, office impairment, logistics-land demand, and utility-linked scarcity all point to a new geography of economic friction. Where Americans live and where firms can physically place activity increasingly shape labor mobility, local service patterns, and asset values. The physical map matters more when high rates freeze households in place and when new strategic demand clusters around land with the right infrastructure.",
            "The office market is the clearest break with the old order. Weak commodity office space is no longer a default winner just because work exists. At the same time, adaptive reuse, housing scarcity, and data-center or logistics-linked corridors are creating new winners in places that align with current flows rather than past assumptions. That means real estate no longer sorts cleanly by sector label alone. It sorts by whether the place still solves a live coordination problem.",
            "At the social level, this produces local friction. Households cannot move easily. Downtown routines weaken. Neighborhood and suburban convenience patterns get stronger. Labor markets become less fluid. The economy keeps digitizing, but digital coordination does not eliminate the importance of where housing, utilities, and daily life actually sit.",
        ],
        "structural_shifts": [
            "Commodity office space is structurally weaker than it looked in the old urban-work model.",
            "Adaptive reuse is turning into a genuine development discipline.",
            "Housing lock-in changes spending and labor mobility even without a collapse in basic need.",
            "Infrastructure-linked land is gaining strategic rent as logistics and compute concentrate.",
        ],
        "tensions": [
            "Cities still need dense activity, but weekday work patterns are less reliable demand anchors.",
            "Housing scarcity supports demand but reduces flexibility and mobility.",
            "Some physical places are becoming more valuable precisely because others lost their old purpose.",
        ],
        "watchpoints": [
            "Which markets successfully convert weak offices into live assets.",
            "How housing immobility changes demand for repair, rental, and neighborhood services.",
            "Where utility and land scarcity create outsize local winners.",
        ],
    },
    "machine-intelligence-and-compute-buildout": {
        "hook": "AI is not only a software cycle. It is a new way of redistributing scarcity across labor, capital, and infrastructure.",
        "long_read": [
            "The common simplification is that AI is mainly about better software. The corpus suggests something bigger and messier. AI is simultaneously compressing knowledge-work workflows, concentrating capital, increasing demand for data centers and power, and changing what types of labor remain differentiated. That makes it both a digital story and a heavy industrial story.",
            "On one side, AI tools are changing service delivery, administrative throughput, search, analysis, and drafting work. This affects consulting, software, support, finance, and many regulated workflows. On the other side, the physical requirements of training and inference are creating new scarcity around land, transmission, cooling, generation, and the trades needed to build and maintain the stack. A market that sounds abstract from the top suddenly becomes concrete at the bottom.",
            "The deeper structural point is concentration. Frontier AI economics reward the players that already control capital, compute, infrastructure, and distribution. That does not mean smaller companies have no place. It means many of them will win by embedding AI into boring workflows rather than by owning the frontier. The broad social and industrial effect is a world where digital productivity gains arrive together with heavier dependence on scarce physical systems.",
        ],
        "structural_shifts": [
            "Power-ready land and data-center capacity have become strategic assets.",
            "Knowledge-work throughput is increasingly governed by workflow compression tools.",
            "AI economics favor upstream owners of capital, infrastructure, and distribution.",
            "Boring sectors may capture more durable value from embedded AI than flashy consumer surfaces do.",
        ],
        "tensions": [
            "Productivity gains in white-collar work can coexist with rising infrastructure costs.",
            "AI looks lightweight in the interface and heavy underneath.",
            "Smaller firms can adopt AI quickly while remaining dependent on large upstream platforms.",
        ],
        "watchpoints": [
            "Where power and utility constraints become the practical limit on AI expansion.",
            "How much workflow compression translates into real labor displacement.",
            "Which embedded AI use cases in regulated and operational sectors become enduring franchises.",
        ],
    },
}


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 80px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.4rem,5vw,4.2rem);line-height:1;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.card h3,.panel h3{margin:.2em 0 .35em;font-size:1.12rem}.card p,.panel p{color:var(--muted);margin:.35em 0 0}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.split{display:grid;grid-template-columns:1.05fr .95fr;gap:14px}.theme{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.theme:first-of-type{margin-top:0;padding-top:0;border-top:none}.theme h3{font-size:1.3rem;margin:.2em 0 .35em}.theme p{color:var(--muted)}.subthemes{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;margin-top:14px}.subcard{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:14px}.subcard h4{margin:.2em 0 .35em;font-size:1rem}.subcard p{margin:.35em 0 0;color:var(--muted);font-size:.95rem}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_theme_records() -> list[dict]:
    with THEMES_JSON.open(encoding="utf-8") as handle:
        data = json.load(handle)
    return data["themes"]


def build_theme_brief(theme: dict) -> dict:
    brief = BRIEFS[theme["slug"]]
    return {
        **theme,
        **brief,
    }


def build_theme_card(theme: dict) -> str:
    chips = "".join(f'<span class="chip">{e(item["title"])}</span>' for item in theme["crosscuts"])
    return f"""<article class="card">
  <div class="meta">{e(theme['lens'])}</div>
  <h3><a href="theme-briefs/{e(theme['slug'])}.html">{e(theme['title'])}</a></h3>
  <p>{e(theme['hook'])}</p>
  <div class="chips">{chips}</div>
</article>"""


def render_subtheme_digest(theme: dict, subtheme: dict, prefix: str = "") -> str:
    driver_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["structural_drivers"][:3])
    signal_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["signals_to_watch"][:3])
    rewrite_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["market_rewrites"][:2])
    follow_on_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["follow_on_effects"][:2])
    behavioral_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["behavioral_expression"][:3])
    economic_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["economic_mechanics"][:3])
    timing_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["timing_markers"][:2])
    hazard_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["execution_hazards"][:2])
    href = f'{e(prefix)}themes/{e(theme["slug"])}.html#{e(subtheme["slug"])}'
    return f"""<article class="subcard">
  <div class="meta">Subtheme</div>
  <h4><a href="{href}">{e(subtheme['title'])}</a></h4>
  <p>{e(subtheme['deep_read'])}</p>
  <div class="chips">{''.join(f'<span class="chip">{e(item)}</span>' for item in subtheme['microthemes'][:3])}</div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Drivers</div>
    <ul class="list">{driver_items}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Signals</div>
    <ul class="list">{signal_items}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Market rewrite</div>
    <ul class="list">{rewrite_items}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Follow-on effects</div>
    <ul class="list">{follow_on_items}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Behavioral expression</div>
    <ul class="list">{behavioral_items}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Economic mechanics</div>
    <ul class="list">{economic_items}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Timing markers</div>
    <ul class="list">{timing_items}</ul>
  </div>
  <div class="panel" style="margin-top:12px;padding:12px">
    <div class="meta">Execution hazards</div>
    <ul class="list">{hazard_items}</ul>
  </div>
</article>"""


def render_theme_section(theme: dict, prefix: str = "") -> str:
    long_read = "".join(f"<p>{e(paragraph)}</p>" for paragraph in theme["long_read"])
    deep_read = f"<p>{e(theme['deep_read'])}</p>"
    structural = "".join(f"<li>{e(item)}</li>" for item in theme["structural_shifts"])
    mechanisms = "".join(f"<li>{e(item)}</li>" for item in theme["core_mechanisms"])
    tensions = "".join(f"<li>{e(item)}</li>" for item in (theme["tensions"] + theme["structural_tensions"]))
    implications = "".join(f"<li>{e(item)}</li>" for item in theme["strategic_implications"])
    stakeholder_map = "".join(f"<li>{e(item)}</li>" for item in theme["stakeholder_map"])
    second_order_effects = "".join(f"<li>{e(item)}</li>" for item in theme["second_order_effects"])
    societal_read = "".join(f"<li>{e(item)}</li>" for item in theme["societal_read"])
    consumer_read = "".join(f"<li>{e(item)}</li>" for item in theme["consumer_read"])
    industrial_read = "".join(f"<li>{e(item)}</li>" for item in theme["industrial_read"])
    capital_implications = "".join(f"<li>{e(item)}</li>" for item in theme["capital_implications"])
    watchpoints = "".join(f"<li>{e(item)}</li>" for item in theme["watchpoints"])
    theme_signals = "".join(f"<li>{e(item)}</li>" for item in theme["signals_to_watch"])
    subtheme_links = "".join(
        f'<a class="chip" href="{e(prefix)}themes/{e(theme["slug"])}.html#{e(sub["slug"])}">{e(sub["title"])}</a>'
        for sub in theme["subthemes"]
    )
    force_links = "".join(
        f'<a class="chip" href="{e(prefix)}forces/{e(force["slug"])}/index.html">{e(force["title"])}</a>'
        for force in theme["forces"]
    )
    subtheme_digests = "".join(render_subtheme_digest(theme, subtheme, prefix=prefix) for subtheme in theme["subthemes"])
    return f"""<section class="theme">
  <div class="meta">{e(theme['lens'])}</div>
  <h3>{e(theme['title'])}</h3>
  <p><b>{e(theme['hook'])}</b></p>
  {long_read}
  <div class="panel" style="margin-top:14px">
    <div class="meta">Deep theme read</div>
    {deep_read}
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Structural shifts</div>
      <ul class="list">{structural}</ul>
    </div>
    <div class="panel">
      <div class="meta">Core mechanisms</div>
      <ul class="list">{mechanisms}</ul>
    </div>
  </div>
  <div class="split" style="margin-top:14px">
    <div class="panel">
      <div class="meta">Tensions</div>
      <ul class="list">{tensions}</ul>
    </div>
    <div class="panel">
      <div class="meta">Strategic implications</div>
      <ul class="list">{implications}</ul>
    </div>
  </div>
  <div class="split" style="margin-top:14px">
    <div class="panel">
      <div class="meta">Theme-level signals</div>
      <ul class="list">{theme_signals}</ul>
    </div>
    <div class="panel">
      <div class="meta">Watchpoints</div>
      <ul class="list">{watchpoints}</ul>
      <div class="chips">{force_links}</div>
      <div class="chips">{subtheme_links}</div>
    </div>
  </div>
  <div class="split" style="margin-top:14px">
    <div class="panel">
      <div class="meta">Stakeholder map</div>
      <ul class="list">{stakeholder_map}</ul>
    </div>
    <div class="panel">
      <div class="meta">Second-order effects</div>
      <ul class="list">{second_order_effects}</ul>
    </div>
  </div>
  <div class="split" style="margin-top:14px">
    <div class="panel">
      <div class="meta">Societal read</div>
      <ul class="list">{societal_read}</ul>
    </div>
    <div class="panel">
      <div class="meta">Consumer read</div>
      <ul class="list">{consumer_read}</ul>
    </div>
  </div>
  <div class="split" style="margin-top:14px">
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
    <div class="meta">Subtheme diagnosis</div>
    <div class="subthemes">{subtheme_digests}</div>
  </div>
</section>"""


def build_hub(theme_briefs: list[dict]) -> str:
    cards = "\n".join(build_theme_card(theme) for theme in theme_briefs)
    sections = "\n".join(render_theme_section(theme) for theme in theme_briefs)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>American Theme Briefs — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="american-themes.html">American themes</a><a href="subthemes.html">Force subthemes</a></div>
<div class="eyebrow">Theme briefs · US · 2025-2026</div>
<h1>American Theme Briefs</h1>
<p class="sub">This is the narrative layer above the taxonomy. It explains what the themes mean, what changed in American life and business structure, what tensions define each theme, and what signals matter next.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(theme_briefs)}</div><div class="l">Theme briefs</div></div>
  <div class="kpi"><div class="n">{sum(len(theme['subthemes']) for theme in theme_briefs)}</div><div class="l">Linked subthemes</div></div>
  <div class="kpi"><div class="n">{sum(len(theme['long_read']) for theme in theme_briefs)}</div><div class="l">Long-read blocks</div></div>
  <div class="kpi"><div class="n">{sum(theme['signal_count'] for theme in theme_briefs)}</div><div class="l">Signals carried through</div></div>
</div>
<div class="lead"><p>Read this layer as the argument, not just the index. The economy in 2025-2026 is being reorganized through overlapping consumer, cultural, institutional, and industrial shifts. These briefs translate that structure into a legible story about how Americans live, spend, age, work, locate themselves, and operate businesses now.</p></div>

<section class="section">
  <h2>Briefs</h2>
  <div class="grid">{cards}</div>
</section>

<section class="section">
  <h2>The Long Read</h2>
  {sections}
</section>

</div></body></html>"""


def build_detail_page(theme: dict) -> str:
    section = render_theme_section(theme, prefix="../")
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(theme['title'])} Brief — American Themes</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../american-themes.html">American themes</a><a href="../american-theme-briefs.html">Theme briefs</a></div>
<div class="eyebrow">{e(theme['lens'])} brief · US · 2025-2026</div>
<h1>{e(theme['title'])}</h1>
<p class="sub">{e(theme['why_now'])}</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(theme['subthemes'])}</div><div class="l">Subthemes</div></div>
  <div class="kpi"><div class="n">{len(theme['long_read'])}</div><div class="l">Narrative blocks</div></div>
  <div class="kpi"><div class="n">{theme['signal_count']}</div><div class="l">Signals</div></div>
  <div class="kpi"><div class="n">{theme['evidence_industry_count']}</div><div class="l">Evidence industries</div></div>
</div>
<div class="lead"><p>{e(theme['thesis'])}</p></div>
<section class="section">
  {section}
</section>
</div></body></html>"""


def main() -> None:
    theme_records = load_theme_records()
    theme_briefs = [build_theme_brief(theme) for theme in theme_records if theme["slug"] in BRIEFS]
    BRIEFS_DIR.mkdir(exist_ok=True)

    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(build_hub(theme_briefs))

    for theme in theme_briefs:
        with (BRIEFS_DIR / f"{theme['slug']}.html").open("w", encoding="utf-8") as handle:
            handle.write(build_detail_page(theme))

    print(f"wrote {OUT}")
    print(f"wrote theme briefs to {BRIEFS_DIR}")
    print(f"briefs={len(theme_briefs)}")


if __name__ == "__main__":
    main()
