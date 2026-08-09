#!/usr/bin/env python3
import json, html, re, os
from collections import Counter

from build_american_outlook import OUTLOOK
ROOT=os.path.dirname(os.path.abspath(__file__))
briefs=json.load(open(f'{ROOT}/briefs_full.json'))
trends=json.load(open(f'{ROOT}/trends_full_raw.json'))
american_themes=json.load(open(f'{ROOT}/american_themes_taxonomy.json'))
economic_intelligence=json.load(open(f'{ROOT}/economic_intelligence_taxonomy.json'))
company_memos=json.load(open(f'{ROOT}/company_memos.json'))

SECTOR_ORDER=["Technology & Digital","Manufacturing","Healthcare","Finance & Insurance","Retail",
 "Food & Drink","Media & Entertainment","Energy & Environment","Agriculture","Construction",
 "Consumer Services","Business Services","Transport & Logistics","Real Estate"]
SECTOR_COLOR={
 "Agriculture":"#5cc08a","Manufacturing":"#e0985a","Construction":"#c9a06a","Retail":"#e07aa8",
 "Food & Drink":"#e0685e","Healthcare":"#3ec9b6","Finance & Insurance":"#d8ad4c",
 "Technology & Digital":"#6c9fd9","Energy & Environment":"#9ccc52","Business Services":"#a98cd9",
 "Consumer Services":"#c98cd9","Media & Entertainment":"#d97ad0","Transport & Logistics":"#5cc0c0",
 "Real Estate":"#c0a080"}

STOP={'in','the','us','and','of','a','an','services','service','stores','store','inc','co',
 'manufacturing','operation','operations','plant','industry','brief','market','size','the',
 '2025','2026','2024','sector','providers','provider'}
def toks(t):
    t=html.unescape(t).lower().replace('&',' and ')
    ws=re.sub(r'[^a-z0-9]+',' ',t).split()
    return [w for w in ws if w not in STOP and len(w)>1]
def tmatch(a,b):
    return a==b or (len(a)>=4 and b.startswith(a)) or (len(b)>=4 and a.startswith(b))
def overlap(tn, bt):
    used=set(); n=0
    for w in bt:
        for j,x in enumerate(tn):
            if j in used: continue
            if tmatch(w,x): used.add(j); n+=1; break
    return n
_briefkeys=[(b['slug'], toks(b['title'])) for b in briefs]
def match_slug(name):
    tn=toks(name)
    if not tn: return None
    best=None; bestscore=0; besttie=99
    for slug,bt in _briefkeys:
        if not bt: continue
        ov=overlap(tn,bt)
        if ov==0: continue
        # require covering all brief key tokens, OR >=2 tokens overlap
        covers = (ov==len(bt)) or (ov>=2)
        if not covers: continue
        # score: prefer full coverage of brief, then fewer brief tokens left over
        score=ov/len(bt)
        tie=len(bt)-ov
        if score>bestscore or (score==bestscore and tie<besttie):
            best=slug; bestscore=score; besttie=tie
    return best if bestscore>=0.5 else None
clean_trends=[]
for tr in trends['trends']:
    slugs=list(tr.get('slugs', []))
    if not slugs:
        for n in tr.get('industries',[]):
            s=match_slug(n)
            if s and s not in slugs: slugs.append(s)
    if len(slugs)>=2: clean_trends.append({**tr,"slugs":slugs})
clean_trends.sort(key=lambda x:-len(x['slugs']))

sectors_present=[s for s in SECTOR_ORDER if any(b['sector']==s for b in briefs)]
theme_lookup={theme['slug']: theme for theme in american_themes['themes']}
headline=(
    "Across the full 1,491-industry corpus in 2025-2026, labor scarcity, demographic aging, "
    "consumer bifurcation, AI buildout, compliance load, channel migration, and consolidation "
    "keep repricing who captures demand, who gets squeezed, and which operators can actually turn "
    "growth into durable economics."
)

def unique_ordered(values):
    seen=set(); out=[]
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value); out.append(value)
    return out

def trim_sentence(text, limit=180):
    text=' '.join(str(text or '').split())
    if len(text) <= limit:
        return text
    clipped=text[:limit].rsplit(' ', 1)[0].rstrip(' ,;:')
    return clipped + '...'

def collect_lens_evidence(linked_themes):
    sector_counts=Counter()
    companies=[]
    subthemes=[]
    operator_moves=[]
    investor_moves=[]
    signals=[]
    tensions=[]
    second_order=[]
    for slug in linked_themes:
        theme=theme_lookup[slug]
        operator_moves.extend(theme.get('strategic_implications', []))
        investor_moves.extend(theme.get('capital_implications', []))
        signals.extend(theme.get('signals_to_watch', []))
        tensions.extend(theme.get('structural_tensions', []))
        second_order.extend(theme.get('second_order_effects', []))
        for subtheme in theme.get('subthemes', []):
            subthemes.append(subtheme['title'])
            for industry in subtheme.get('industries', []):
                if industry.get('sector'):
                    sector_counts[industry['sector']] += 1
            for company in subtheme.get('companies', []):
                companies.append(company.get('title'))
    return {
        'sectors': [sector for sector, _ in sector_counts.most_common(4)],
        'companies': unique_ordered(companies)[:4],
        'subthemes': unique_ordered(subthemes)[:4],
        'operator_moves': unique_ordered(operator_moves)[:2],
        'investor_moves': unique_ordered(investor_moves)[:2],
        'signals': unique_ordered(signals)[:2],
        'tensions': unique_ordered(tensions)[:2],
        'second_order': unique_ordered(second_order)[:2],
    }

overview_cards=[
    {
        "label":"Synthesis hub",
        "title":"American Synthesis Hub",
        "href":"american-synthesis-hub.html",
        "body":"The dedicated front door for the ranked stack, summary surfaces, playbook, memo, and downstream evidence pages.",
        "where_it_shows_up":[
            "Executive summary and rankings entry",
            "Macro narrative, playbook, and derivative briefings",
            "Theme, sector, and company drill-down paths",
        ],
        "signals":[
            "The synthesis stack is now coherent enough to deserve its own landing surface.",
            "The ranked and narrative layers can now be navigated from one place.",
        ],
        "what_to_do":[
            "Start here when you want the whole synthesis stack organized in one view.",
            "Use it as the main front door for briefing and presentation workflows.",
        ],
        "what_to_underwrite":[
            "The highest-ranked bottlenecks, rails, and decision surfaces in the stack.",
            "The themes and models that remain strongest after prioritization rather than broad enumeration.",
        ],
        "tensions":[
            "A broad stack is only useful if the entry point makes the hierarchy legible.",
            "The landing page has to orient without collapsing the structure underneath.",
        ],
        "second_order":[
            "The ranked stack becomes much easier to reuse in presentations and derivative outputs.",
            "The synthesis work is easier to onboard for new readers once the hub exists.",
        ],
        "use_cases":[
            "Use it before rankings, summary, or memo reading.",
            "Best top-level entry point for the full synthesis stack.",
        ],
    },
    {
        "label":"Master synthesis",
        "title":"American Outlook 2025-2026",
        "href":"american-outlook-2025-2026.html",
        "body":"The cleanest top-level read on societal, cultural, consumer, and industrial change across the full corpus.",
        "where_it_shows_up":[
            "Household budgets and consumption mix",
            "Labor formation, hiring, and retention",
            "Power, housing, and physical buildout bottlenecks",
        ],
        "signals":[
            "Consumer demand keeps splitting between value-safe and premium-defensible positions.",
            "Capital and labor keep concentrating around constrained, high-importance systems.",
        ],
        "what_to_do":[
            "Use it to frame decisions before narrowing into themes, sectors, or companies.",
            "Treat it as the quickest way to orient around the current US macro stack.",
        ],
        "what_to_underwrite":[
            "Businesses aligned with recurring bottlenecks, not generic growth narratives.",
            "Operators that can turn constraint management into pricing power or workflow control.",
        ],
        "tensions":[
            "Demand can still grow while margins, labor, and capital intensity get worse.",
            "The economic winners are not always in the obvious headline categories.",
        ],
        "second_order":[
            "Operational complexity becomes a selection mechanism, not just a cost line.",
            "Sector outcomes increasingly depend on adjacent systems like power, logistics, or regulation.",
        ],
        "use_cases":[
            "Start here for the four-lens read on America.",
            "Use it before drilling into themes, sectors, or company evidence.",
        ],
    },
    {
        "label":"Capstone narrative",
        "title":"The US Economy in 2025-2026",
        "href":"american-economy-2025-2026.html",
        "body":"The full end-to-end argument tying labor, demand, institutions, geography, AI, and physical buildout together.",
        "where_it_shows_up":[
            "Households, institutions, and regional growth corridors",
            "AI infrastructure, logistics, and construction demand",
            "Consumer, healthcare, and financial operating models",
        ],
        "signals":[
            "AI demand increasingly behaves like a power and infrastructure story, not only a software story.",
            "Aging, labor scarcity, and admin burden keep showing up together across unrelated sectors.",
        ],
        "what_to_do":[
            "Use it when you need the whole-system explanation rather than a single theme slice.",
            "Read it before writing a broad investment or operating thesis on the US economy.",
        ],
        "what_to_underwrite":[
            "Assets and operators sitting on the advantaged side of labor, land, power, and workflow constraints.",
            "Business models that benefit when institutional complexity keeps rising.",
        ],
        "tensions":[
            "Digital productivity gains coexist with rising physical bottlenecks.",
            "Nominal growth can obscure worsening competitive separation underneath.",
        ],
        "second_order":[
            "Capital flows toward picks-and-shovels layers rather than only consumer-facing winners.",
            "Regional and sector divergence becomes more durable because bottlenecks are local and physical.",
        ],
        "use_cases":[
            "Use this when you want the full narrative, not just the map.",
            "Best for understanding how the major pressures fit together systemically.",
        ],
    },
    {
        "label":"Economic intelligence",
        "title":"Economic Intelligence",
        "href":"economic-intelligence.html",
        "body":"The surfaced force map linking recurring pressures, domains, operator questions, and flagship synthesis artifacts.",
        "where_it_shows_up":[
            "Cross-industry recurring forces",
            "Sector comparisons and operator workflows",
            "Theme, outlook, and memo navigation",
        ],
        "signals":[
            "The same force clusters keep repeating across sectors, not just inside isolated industries.",
            "Operator questions converge around constraint management rather than generic market share.",
        ],
        "what_to_do":[
            "Use it to move from industry detail into force logic and recurring pressure patterns.",
            "Read it when comparing why very different sectors are behaving similarly.",
        ],
        "what_to_underwrite":[
            "Platforms, tools, and owners that monetize mandatory complexity.",
            "Businesses positioned where repeated force overlap creates durable leverage.",
        ],
        "tensions":[
            "Macro narratives can look clean while the force stack underneath stays messy and uneven.",
            "A category can have strong demand and still be structurally exposed to the wrong force mix.",
        ],
        "second_order":[
            "Force overlap becomes a practical diligence shortcut across sectors and companies.",
            "Operating playbooks start converging even where end markets remain different.",
        ],
        "use_cases":[
            "Use this when you need the force system behind the industry corpus.",
            "Best for moving from repeated industry patterns into operating logic.",
        ],
    },
    {
        "label":"Theme memos",
        "title":"American Theme Memos",
        "href":"american-theme-memos.html",
        "body":"The decision layer translating the major themes into what to do, what to avoid, and what to underwrite.",
        "where_it_shows_up":[
            "Theme-level operating posture",
            "Investor diligence framing",
            "Representative industries and named companies",
        ],
        "signals":[
            "Theme evidence is strong enough to support operator and investor translation, not just taxonomy.",
            "The same macro pressures now map cleanly into hunt zones, avoid zones, and underwriting questions.",
        ],
        "what_to_do":[
            "Use it when you need the shortest path from macro read to operator action.",
            "Use it to screen where to hunt, what to avoid, and what diligence to run next.",
        ],
        "what_to_underwrite":[
            "Category leaders that convert structural themes into practical economics.",
            "Businesses whose advantages deepen as the theme becomes more normal rather than more novel.",
        ],
        "tensions":[
            "A theme can be right directionally while still punishing weak operators inside it.",
            "The best narrative categories are not always the best underwriting categories.",
        ],
        "second_order":[
            "Theme intensity changes hiring, procurement, service, and capital allocation before it changes headlines.",
            "Company-level separation becomes easier to explain once the macro theme is operationalized.",
        ],
        "use_cases":[
            "Use this when you need strategic and capital implications fast.",
            "Best bridge from macro interpretation to diligence and action.",
        ],
    },
    {
        "label":"Ranked synthesis",
        "title":"American Rankings",
        "href":"american-rankings.html",
        "body":"The priority map for the synthesis stack: ranked themes, subthemes, bottlenecks, and exposed business models.",
        "where_it_shows_up":[
            "Theme prioritization and subtheme acceleration",
            "Bottleneck underwriting and exposed-model screening",
            "Executive summary and memo construction",
        ],
        "signals":[
            "The strongest themes can now be ranked by breadth, recurrence, sector spread, and company evidence.",
            "The synthesis stack has enough structure to score bottlenecks and exposed models directly.",
        ],
        "what_to_do":[
            "Use it to decide what matters most before writing a memo or building a diligence list.",
            "Use it as the shortest path from broad synthesis to prioritized judgment.",
        ],
        "what_to_underwrite":[
            "The highest-ranked bottlenecks and rails rather than broad category stories.",
            "The business models least dependent on the generic middle staying healthy.",
        ],
        "tensions":[
            "Not every vivid theme deserves equal practical weight.",
            "A popular narrative can still rank below a quieter but more durable bottleneck.",
        ],
        "second_order":[
            "Ranked themes sharpen the operator and investor agenda by forcing prioritization.",
            "The stack becomes easier to present once the top calls and top exposures are explicit.",
        ],
        "use_cases":[
            "Start here when you want the ordered version of the synthesis stack.",
            "Use it before the executive summary or implications memo.",
        ],
    },
    {
        "label":"Executive summary",
        "title":"American Executive Summary",
        "href":"american-executive-summary.html",
        "body":"The one-page summary surface for the ranked US economy stack.",
        "where_it_shows_up":[
            "Top themes and fastest-accelerating subthemes",
            "Most investable bottlenecks and exposed models",
            "Operator and investor takeaways",
        ],
        "signals":[
            "The macro synthesis can now be reduced to a short decision-grade summary without losing the spine of the argument.",
            "Priority themes, bottlenecks, and risks are visible in one page.",
        ],
        "what_to_do":[
            "Use it as the briefing page before deeper reading.",
            "Use it when the audience needs high signal with minimal navigation overhead.",
        ],
        "what_to_underwrite":[
            "The assets, workflows, and choke points that sit at the top of the ranked stack.",
            "The categories that survive once demand is filtered through control, proof, and cultural permission.",
        ],
        "tensions":[
            "The summary has to stay concise without flattening the structure underneath.",
            "The biggest theme is not always the cleanest immediate investment setup.",
        ],
        "second_order":[
            "A cleaner entry surface makes the whole synthesis stack more reusable.",
            "The ranking layer becomes easier to communicate to non-specialist readers.",
        ],
        "use_cases":[
            "Use it for the shortest possible orientation to the stack.",
            "Read it before the long-form implications memo.",
        ],
    },
    {
        "label":"Implications memo",
        "title":"American Implications Memo",
        "href":"american-implications-memo.html",
        "body":"A polished long-form memo focused on the societal, cultural, consumer, and industrial implications of the ranked stack.",
        "where_it_shows_up":[
            "Societal and institutional reorganization",
            "Cultural permission shifts and consumer ranking behavior",
            "Industrial bottlenecks and physical constraint systems",
        ],
        "signals":[
            "The ranked themes can now support a coherent long-form narrative rather than only a taxonomy or playbook.",
            "Societal, cultural, consumer, and industrial sections can be written off the same scored spine.",
        ],
        "what_to_do":[
            "Use it when you need the polished essay version of the stack.",
            "Use it as the narrative wrapper around rankings, playbook, and capstone.",
        ],
        "what_to_underwrite":[
            "The intersection of control, proof, and bottlenecks across the four lenses.",
            "Business models that get stronger as the US economy becomes more selective and more managed.",
        ],
        "tensions":[
            "A clean memo still has to preserve the complexity of the underlying structure.",
            "The same social change can create demand in one layer and pressure in another.",
        ],
        "second_order":[
            "The synthesis layer now supports both decision surfaces and polished narrative surfaces.",
            "The stack becomes easier to reuse in presentations, briefs, and derivative memos.",
        ],
        "use_cases":[
            "Use it after the executive summary when you want the full written interpretation.",
            "Best for communicating the implications of the ranked stack to a broader audience.",
        ],
    },
]

lens_cards=[]
for section in OUTLOOK["sections"]:
    evidence=collect_lens_evidence(section["linked_themes"])
    lens_cards.append({
        "label":section["label"],
        "title":section["title"],
        "summary":section["summary"],
        "href":f"american-outlook-2025-2026.html#{section['slug']}",
        "themes":[theme_lookup[slug]["title"] for slug in section["linked_themes"]],
        "subthemes":evidence["subthemes"],
        "sectors":evidence["sectors"],
        "companies":evidence["companies"],
        "operator_moves":evidence["operator_moves"],
        "investor_moves":evidence["investor_moves"],
        "signals":evidence["signals"],
        "tensions":evidence["tensions"],
        "second_order":evidence["second_order"],
    })

landing_summary={
    "where_it_shows_up":[
        "Consumer demand, healthcare delivery, financial intermediation, and regional growth corridors.",
        "Power-heavy AI infrastructure, logistics networks, housing markets, and industrial buildout.",
    ],
    "signals":[
        "Value versus premium demand splitting keeps showing up across sectors instead of fading.",
        "Labor, regulation, and power constraints increasingly govern margins more than simple volume growth.",
    ],
    "what_to_do":[
        "Start with the macro stack before judging any sector or company in isolation.",
        "Use recurring constraints as a filter for strategy, diligence, pricing, staffing, and capital allocation.",
    ],
    "what_to_underwrite":[
        "Assets and operators on the advantaged side of labor, power, land, compliance, and workflow bottlenecks.",
        "Business models that convert complexity into repeat revenue, pricing power, or strategic control.",
    ],
    "tensions":[
        "Nominal growth can coexist with weaker economics when the wrong constraint becomes binding.",
        "The most obvious headline winners are not always the businesses capturing the durable margin pool.",
    ],
    "second_order":[
        "Operational complexity becomes a selection mechanism that separates scalable operators from the generic middle.",
        "Adjacent systems like logistics, power, permitting, and reimbursement increasingly determine sector outcomes.",
    ],
}

company_by_overlap={}
for trend in clean_trends:
    if trend.get('top_sectors') and trend.get('representative_companies'):
        company_by_overlap[trend['name']] = {
            'sectors': trend.get('top_sectors', []),
            'themes': trend.get('recurring_brief_themes', []),
            'companies': trend.get('representative_companies', []),
            'operator_lines': trend.get('operator_implications', []),
            'investor_lines': trend.get('investor_implications', []),
            'tensions': trend.get('structural_tensions', []),
            'signals': trend.get('signals_to_watch', []),
            'second_order': trend.get('second_order_effects', []),
        }
        continue
    trend_slugs=set(trend['slugs'])
    sector_counts=Counter()
    theme_counts=Counter()
    company_matches=[]
    constraint_counts=Counter()
    owner_counts=Counter()
    loser_counts=Counter()
    diligence=[]
    for slug in trend['slugs']:
        brief=next(b for b in briefs if b['slug']==slug)
        sector_counts[brief['sector']] += 1
        for theme in brief.get('themes', []):
            theme_counts[theme] += 1
    for company in company_memos:
        overlap=[item for item in company.get('linked_industries', []) if item.get('slug') in trend_slugs]
        if not overlap:
            continue
        company_matches.append((len(overlap), company))
        for constraint in company.get('constraints', []):
            constraint_counts[constraint] += 1
        if company.get('best_owner_type'):
            owner_counts[company['best_owner_type']] += 1
        for loser in company.get('likely_losers', []):
            loser_counts[loser] += 1
        for question in company.get('diligence_questions', []):
            if question not in diligence:
                diligence.append(question)
    company_matches.sort(key=lambda item: (-item[0], -item[1].get('mention_count', 0), item[1]['title']))
    top_companies=[company for _, company in company_matches[:4]]
    top_constraints=[name for name, _ in constraint_counts.most_common(3)]
    top_owners=[name for name, _ in owner_counts.most_common(2)]
    top_losers=[name for name, _ in loser_counts.most_common(2)]
    operator_lines=[]
    if top_constraints and top_owners:
        operator_lines.append(
            f"Operate for {top_constraints[0]} and {top_constraints[1] if len(top_constraints) > 1 else top_constraints[0]}; the current winners skew toward {top_owners[0]} structures."
        )
    elif top_constraints:
        operator_lines.append(
            f"Operate for {top_constraints[0]}; this trend keeps punishing businesses that treat it as a secondary issue."
        )
    if top_losers:
        operator_lines.append(
            f"Avoid setups that look like {top_losers[0]}{f' or {top_losers[1]}' if len(top_losers) > 1 else ''} where margin room and strategic flexibility are already thin."
        )
    if not operator_lines:
        operator_lines.append("Use this trend as a filter for where operating complexity is rising faster than generic demand growth.")
    investor_lines=unique_ordered(diligence)[:2]
    if not investor_lines and top_constraints:
        investor_lines.append(f"How durable is the company's advantage if {top_constraints[0]} becomes the binding constraint?")
    company_by_overlap[trend['name']]={
        'sectors':[sector for sector, _ in sector_counts.most_common(4)],
        'themes':[theme for theme, _ in theme_counts.most_common(4)],
        'companies':[{
            'title':company['title'],
            'slug':company['slug'],
            'sector':company.get('top_sector', 'Unknown'),
            'memo':trim_sentence(company.get('operator_memo') or company.get('investor_memo') or ''),
        } for company in top_companies],
        'operator_lines':operator_lines[:2],
        'investor_lines':investor_lines[:2],
        'tensions': [],
        'signals': [],
        'second_order': [],
    }

DATA=json.dumps({
 "industries":briefs,
 "trends":clean_trends,
 "headline":headline,
 "sectors":sectors_present,
 "sectorColor":SECTOR_COLOR,
 "workingThesis":economic_intelligence.get('working_thesis',''),
 "crosscuts":[c['title'] for c in economic_intelligence.get('crosscuts', [])[:6]],
 "landingSummary":landing_summary,
 "overviewCards":overview_cards,
 "lensCards":lens_cards,
 "trendEvidence":company_by_overlap,
}, ensure_ascii=False)

PAGE = """<title>US Industry Briefs — 2025-2026</title>
<style>
:root{
  --ink:#0e1218; --panel:#151b23; --panel2:#1b2531; --line:#27313f; --line2:#1e2733;
  --paper:#e9e5da; --muted:#9aa4b2; --faint:#66707e;
  --brass:#c9a24b; --up:#5cc08a; --down:#e08672;
  --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --mono:ui-monospace,"SF Mono",Menlo,Consolas,monospace;
}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--ink);color:var(--paper);font-family:var(--sans);line-height:1.6;font-size:16px;-webkit-font-smoothing:antialiased}
.wrap{max-width:1160px;margin:0 auto;padding:0 clamp(16px,4vw,40px) 80px}
.num{font-family:var(--mono);font-variant-numeric:tabular-nums}
a{color:var(--brass);text-decoration:none}
header.top{padding:40px 0 20px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:var(--mono);font-size:.72rem;letter-spacing:.24em;text-transform:uppercase;color:var(--brass)}
h1{font-size:clamp(2rem,5vw,3rem);font-weight:800;letter-spacing:-.025em;line-height:1.02;margin:.28em 0 .18em;text-wrap:balance}
.lede{color:var(--muted);max-width:660px;font-size:1.06rem}
.strip{display:flex;flex-wrap:wrap;gap:8px;margin-top:22px}
.kpi{background:var(--panel);border:1px solid var(--line2);border-radius:10px;padding:10px 16px;min-width:104px}
.kpi .n{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:1.42rem;font-weight:700}
.kpi .l{font-size:.68rem;text-transform:uppercase;letter-spacing:.07em;color:var(--faint);margin-top:1px}
.tabs{display:flex;gap:4px;margin:22px 0 0;border-bottom:1px solid var(--line)}
.tab{font-family:var(--mono);font-size:.8rem;letter-spacing:.03em;color:var(--muted);background:none;border:none;border-bottom:2px solid transparent;padding:11px 16px;cursor:pointer}
.tab:hover{color:var(--paper)} .tab.on{color:var(--brass);border-bottom-color:var(--brass)}
.linktab{font-family:var(--mono);font-size:.8rem;letter-spacing:.03em;color:var(--muted);padding:11px 16px;border-bottom:2px solid transparent}
.linktab:hover{color:var(--paper)}
.controls{display:flex;flex-wrap:wrap;gap:10px;align-items:center;margin:20px 0 6px;position:sticky;top:0;background:var(--ink);padding:12px 0;z-index:6}
#q{flex:1;min-width:200px;background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:10px 14px;color:var(--paper);font-size:.95rem;font-family:var(--sans)}
#q::placeholder{color:var(--faint)} #q:focus{outline:2px solid var(--brass);border-color:var(--brass)}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{font-family:var(--mono);font-size:.7rem;color:var(--muted);background:var(--panel);border:1px solid var(--line);border-radius:20px;padding:5px 11px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.chip:hover{color:var(--paper);border-color:var(--faint)}
.chip.on{background:var(--brass);border-color:var(--brass);color:#0e1218;font-weight:600}
.cdot{width:8px;height:8px;border-radius:50%}
.sechead{display:flex;align-items:center;gap:10px;margin:30px 0 12px;padding-top:12px;border-top:1px solid var(--line2)}
.sechead h2{font-size:1.14rem;font-weight:700} .sechead .c{font-family:var(--mono);font-size:.72rem;color:var(--faint)}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(258px,1fr));gap:11px}
.card{background:var(--panel);border:1px solid var(--line2);border-radius:12px;padding:15px 16px;border-left:3px solid var(--sc,var(--brass));cursor:pointer;transition:transform .12s,background .12s;text-align:left}
.card:hover{transform:translateY(-2px);background:var(--panel2)}
.card .co{font-size:1.03rem;font-weight:650;line-height:1.2}
.card .one{font-size:.85rem;color:var(--muted);margin:.35em 0 .7em;line-height:1.4}
.card .mini{display:flex;gap:12px;font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:.72rem;color:var(--faint);flex-wrap:wrap}
.card .mini b{color:var(--paper);font-weight:600}
.up{color:var(--up)} .down{color:var(--down)}
.nores{color:var(--faint);font-family:var(--mono);padding:36px 0}
.headline{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--brass);border-radius:0 12px 12px 0;padding:18px 22px;margin:22px 0}
.headline .l{font-family:var(--mono);font-size:.66rem;letter-spacing:.12em;text-transform:uppercase;color:var(--brass);margin-bottom:6px}
.headline p{font-size:1.16rem;font-weight:500}
.section{margin-top:26px;padding-top:14px;border-top:1px solid var(--line2)}
.split{display:grid;grid-template-columns:minmax(0,1.1fr) minmax(280px,.9fr);gap:14px}
.stack>*+*{margin-top:12px}
.story{background:var(--panel);border:1px solid var(--line2);border-radius:13px;padding:18px 20px}
.story h3{font-size:1.15rem;margin:0 0 .35em}
.story p{color:var(--muted)}
.overview-grid,.lens-grid,.summary-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.overview-card,.lens-card,.summary-card{background:var(--panel);border:1px solid var(--line2);border-radius:13px;padding:18px}
.eyeline{font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;color:var(--brass)}
.overview-card h3,.lens-card h3,.summary-card h3{font-size:1.08rem;margin:.22em 0 .35em}
.overview-card p,.lens-card p,.summary-card p{color:var(--muted)}
.list{padding-left:18px;color:var(--muted);margin:.5em 0 0}
.list li{margin:.32em 0}
.railcard{background:var(--panel);border:1px solid var(--line2);border-radius:13px;padding:18px}
.railcard h3{font-size:1rem;margin:0 0 .4em}
.railcard p{color:var(--muted)}
.microchips{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}
.microchip{font-family:var(--mono);font-size:.68rem;color:var(--muted);background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:4px 9px}
.trend{background:var(--panel);border:1px solid var(--line2);border-radius:13px;padding:19px 22px;margin:13px 0;border-left:3px solid var(--brass)}
.trend .kind{font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;color:var(--brass)}
.trend .cnt{float:right;font-family:var(--mono);font-size:.72rem;color:var(--faint)}
.trend h3{font-size:1.24rem;font-weight:700;margin:.12em 0 .45em;text-wrap:balance}
.trend p{color:var(--muted);font-size:.98rem}
.wl{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:13px 0}
.wl div{font-size:.9rem;color:var(--muted)} .wl b{font-family:var(--mono);font-size:.64rem;text-transform:uppercase;letter-spacing:.06em;display:block;margin-bottom:2px}
.wl .win b{color:var(--up)} .wl .lose b{color:var(--down)}
@media(max-width:560px){.wl{grid-template-columns:1fr}}
.trendgrid{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin:13px 0}
.trendbox{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:12px 14px}
.trendbox h4{font-family:var(--mono);font-size:.66rem;text-transform:uppercase;letter-spacing:.08em;color:var(--brass);margin:0 0 7px}
.trendbox ul{padding-left:18px;color:var(--muted);margin:0}
.trendbox li{margin:.32em 0}
.trendmini{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:8px;margin:12px 0}
.trendcompany{background:var(--panel2);border:1px solid var(--line);border-radius:10px;padding:12px}
.trendcompany .meta{font-size:.63rem}
.trendcompany h4{font-size:.92rem;margin:.22em 0 .32em}
.trendcompany p{font-size:.84rem;color:var(--muted);margin:0}
.trenddeep{display:grid;grid-template-columns:1fr 1fr 1fr;gap:10px;margin:12px 0}
@media(max-width:900px){.trenddeep{grid-template-columns:1fr}}
.hits{display:flex;flex-wrap:wrap;gap:6px}
.hit{font-size:.76rem;color:var(--muted);background:var(--panel2);border:1px solid var(--line);border-radius:7px;padding:4px 9px;cursor:pointer;display:inline-flex;align-items:center;gap:6px}
.hit:hover{color:var(--paper);border-color:var(--faint)}
.scrim{position:fixed;inset:0;background:rgba(6,9,13,.66);opacity:0;pointer-events:none;transition:opacity .2s;z-index:20}
.scrim.on{opacity:1;pointer-events:auto}
.panel{position:fixed;top:0;right:0;height:100%;width:min(580px,95vw);background:var(--ink);border-left:1px solid var(--line);transform:translateX(100%);transition:transform .24s cubic-bezier(.4,0,.2,1);z-index:21;overflow-y:auto}
.panel.on{transform:translateX(0)}
.panel .inner{padding:26px clamp(18px,4vw,30px) 60px}
.pclose{position:sticky;top:0;float:right;background:var(--panel);border:1px solid var(--line);color:var(--muted);border-radius:8px;width:34px;height:34px;font-size:1.1rem;cursor:pointer;line-height:1}
.pclose:hover{color:var(--paper)}
.sectag{display:inline-flex;align-items:center;gap:7px;font-family:var(--mono);font-size:.68rem;text-transform:uppercase;letter-spacing:.07em;border:1px solid;border-radius:20px;padding:4px 11px;margin-bottom:12px}
.dyr{font-family:var(--mono);font-size:.66rem;color:var(--faint);margin-left:8px}
.panel h2{font-size:1.6rem;font-weight:800;letter-spacing:-.015em;line-height:1.1;text-wrap:balance}
.panel .liner{color:var(--muted);font-style:italic;margin-top:.35em;font-size:1.04rem}
.kstats{display:grid;grid-template-columns:1fr 1fr;gap:1px;background:var(--line2);border:1px solid var(--line2);border-radius:11px;overflow:hidden;margin:20px 0}
.ks{background:var(--panel);padding:12px 14px}
.ks .l{font-size:.64rem;text-transform:uppercase;letter-spacing:.06em;color:var(--faint)}
.ks .v{font-family:var(--mono);font-variant-numeric:tabular-nums;font-size:1.02rem;font-weight:600;margin-top:3px}
.ks .was{font-family:var(--mono);font-size:.66rem;color:var(--faint);margin-top:3px}
.ks.big{grid-column:1/3} .ks.big .v{font-size:1.3rem;color:var(--brass)}
.blk{margin:18px 0 0} .blk h4{font-family:var(--mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.09em;color:var(--faint);margin-bottom:6px}
.blk p{font-size:1rem}
.now{background:var(--panel2);border:1px solid var(--line);border-radius:11px;padding:15px 17px;margin:18px 0 0}
.now h4{font-family:var(--mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.09em;color:var(--brass);margin-bottom:7px}
.now p{font-size:1rem}
.psplit{display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:18px}
@media(max-width:560px){.psplit{grid-template-columns:1fr}.kstats{grid-template-columns:1fr}.ks.big{grid-column:auto}}
.pane{background:var(--panel);border:1px solid var(--line2);border-radius:11px;padding:14px 16px;border-top:3px solid}
.pane.u{border-top-color:var(--up)} .pane.d{border-top-color:var(--down)}
.pane h4{font-family:var(--mono);font-size:.72rem;text-transform:uppercase;letter-spacing:.07em;margin-bottom:6px}
.pane.u h4{color:var(--up)} .pane.d h4{color:var(--down)}
.pane p{font-size:.92rem;color:var(--muted)}
.devs{list-style:none;margin-top:4px} .devs li{font-size:.92rem;color:var(--muted);padding:6px 0 6px 16px;border-left:2px solid var(--line);margin-bottom:2px;position:relative}
.devs li::before{content:"";position:absolute;left:-5px;top:12px;width:8px;height:8px;border-radius:50%;background:var(--brass)}
.players{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.pl{font-size:.85rem;background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:5px 10px}
.tchips{display:flex;flex-wrap:wrap;gap:6px;margin-top:6px}
.tc{font-family:var(--mono);font-size:.72rem;color:var(--muted);background:var(--panel2);border:1px solid var(--line);border-radius:20px;padding:4px 10px}
.take{background:var(--panel2);border:1px solid var(--line);border-left:4px solid var(--brass);border-radius:0 11px 11px 0;padding:15px 18px;margin-top:22px}
.take .l{font-family:var(--mono);font-size:.64rem;text-transform:uppercase;letter-spacing:.1em;color:var(--brass);margin-bottom:5px}
.take p{font-size:1.06rem;font-weight:500}
details.src{margin-top:18px} details.src summary{font-family:var(--mono);font-size:.72rem;color:var(--faint);cursor:pointer}
details.src ul{list-style:none;margin-top:8px} details.src li{font-size:.8rem;color:var(--muted);padding:2px 0}
footer{margin-top:40px;padding-top:20px;border-top:1px solid var(--line2);color:var(--faint);font-family:var(--mono);font-size:.72rem;line-height:1.8}
.hidden{display:none!important}
@media(max-width:880px){.split{grid-template-columns:1fr}}
@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style>

<div class="wrap">
 <header class="top">
 <div class="eyebrow">Plain-English business intelligence &middot; US &middot; 2025&ndash;2026</div>
  <h1>US Industry Briefs</h1>
  <p class="lede">The completed <b>1,491-industry US corpus</b>, refreshed to 2025&ndash;2026 and organized into a usable interpretation system: searchable industry briefs, cross-industry trends, force maps, American themes, sector/company evidence, and action-oriented synthesis.</p>
  <div class="strip" id="strip"></div>
 </header>
 <div class="tabs">
  <button class="tab on" data-view="ov">Overview</button>
  <button class="tab" data-view="ind">Industries</button>
  <button class="tab" data-view="tr">Cross-cutting trends</button>
  <a class="linktab" href="operators.html">Operator playbooks</a>
  <a class="linktab" href="forces/index.html">Forces</a>
  <a class="linktab" href="economic-intelligence.html">Economic intelligence</a>
 </div>
 <section id="view-ov">
  <div class="headline"><div class="l">Working thesis across all 1,491</div><p id="working-thesis"></p></div>
  <div class="section">
   <h2>Start Here</h2>
   <div class="overview-grid" id="overview-cards"></div>
  </div>
  <div class="section">
   <h2>The Four Macro Lenses</h2>
   <div class="lens-grid" id="lens-cards"></div>
  </div>
  <div class="section">
   <h2>Decision Surface</h2>
   <div class="summary-grid">
    <article class="summary-card">
     <div class="eyeline">Where it shows up</div>
     <ul class="list" id="landing-where"></ul>
    </article>
    <article class="summary-card">
     <div class="eyeline">Signals</div>
     <ul class="list" id="landing-signals"></ul>
    </article>
    <article class="summary-card">
     <div class="eyeline">What to do</div>
     <ul class="list" id="landing-do"></ul>
    </article>
    <article class="summary-card">
     <div class="eyeline">What to underwrite</div>
     <ul class="list" id="landing-underwrite"></ul>
    </article>
    <article class="summary-card">
     <div class="eyeline">Tensions</div>
     <ul class="list" id="landing-tensions"></ul>
    </article>
    <article class="summary-card">
     <div class="eyeline">Second-order effects</div>
     <ul class="list" id="landing-second-order"></ul>
    </article>
   </div>
  </div>
  <div class="section">
   <div class="split">
    <div class="stack">
     <article class="story">
      <div class="eyeline">Why this matters</div>
      <h3>The corpus now has an interpretation layer</h3>
      <p>The point is no longer just to browse industries one by one. The point is to read the American economy as a system, see which pressures repeat, and move from pattern recognition to decisions.</p>
     </article>
     <article class="story">
      <div class="eyeline">What keeps repeating</div>
      <h3>The same constraints are showing up everywhere</h3>
      <p>Labor scarcity, demographic aging, consumer bifurcation, AI buildout, compliance load, channel migration, and consolidation keep reappearing across sectors because they are not isolated stories. They are the operating conditions of the 2025&ndash;2026 economy.</p>
     </article>
    </div>
    <aside class="railcard">
     <div class="eyeline">Crosscuts</div>
     <h3>Repeat pressures</h3>
     <p>These are the recurring forces cutting across the corpus and linking industry detail back to the macro read.</p>
     <div class="microchips" id="crosscuts"></div>
    </aside>
   </div>
  </div>
 </section>
 <section id="view-ind" class="hidden">
  <div class="controls">
   <input id="q" type="text" placeholder="Search industries, sectors, or forces&hellip;" autocomplete="off">
   <div class="chips" id="filters"></div>
  </div>
  <div id="results"></div>
 <p class="nores hidden" id="nores">No industries match.</p>
 </section>
 <section id="view-tr" class="hidden">
  <div class="headline"><div class="l">The through-line across all 1,491, right now</div><p id="headline"></p></div>
  <div id="trends"></div>
 </section>
<footer>Source: 2022 IBISWorld reports as baseline, refreshed with live 2025&ndash;2026 web research. This landing surface now sits on top of the completed 1,491-industry corpus and its synthesis layers. Figures carry their year; verify before relying on them.</footer>
</div>
<div class="scrim" id="scrim"></div>
<aside class="panel" id="panel" aria-label="Industry detail"><div class="inner" id="pinner"></div></aside>

<script>
const D=__DATA__;
const bySlug=Object.fromEntries(D.industries.map(b=>[b.slug,b]));
const SC=D.sectorColor;
const esc=s=>String(s==null?'':s).replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
const gcls=g=>String(g||'').replace(/^[~]/,'').trim().startsWith('-')?'down':'up';
document.getElementById('strip').innerHTML=[
 [D.industries.length,'Industries'],[D.sectors.length,'Sectors'],
 [D.trends.length,'Current trends'],[D.lensCards.length,'Macro lenses']
].map(([n,l])=>`<div class="kpi"><div class="n">${n}</div><div class="l">${l}</div></div>`).join('');
document.getElementById('working-thesis').textContent=D.workingThesis;
document.getElementById('crosscuts').innerHTML=D.crosscuts.map(item=>`<span class="microchip">${esc(item)}</span>`).join('');
document.getElementById('landing-where').innerHTML=D.landingSummary.where_it_shows_up.map(item=>`<li>${esc(item)}</li>`).join('');
document.getElementById('landing-signals').innerHTML=D.landingSummary.signals.map(item=>`<li>${esc(item)}</li>`).join('');
document.getElementById('landing-do').innerHTML=D.landingSummary.what_to_do.map(item=>`<li>${esc(item)}</li>`).join('');
document.getElementById('landing-underwrite').innerHTML=D.landingSummary.what_to_underwrite.map(item=>`<li>${esc(item)}</li>`).join('');
document.getElementById('landing-tensions').innerHTML=D.landingSummary.tensions.map(item=>`<li>${esc(item)}</li>`).join('');
document.getElementById('landing-second-order').innerHTML=D.landingSummary.second_order.map(item=>`<li>${esc(item)}</li>`).join('');
document.getElementById('overview-cards').innerHTML=D.overviewCards.map(card=>`
 <article class="overview-card">
  <div class="eyeline">${esc(card.label)}</div>
  <h3><a href="${esc(card.href)}">${esc(card.title)}</a></h3>
  <p>${esc(card.body)}</p>
  <div class="eyeline" style="margin-top:14px">Where it shows up</div>
  <ul class="list">${card.where_it_shows_up.map(line=>`<li>${esc(line)}</li>`).join('')}</ul>
  <div class="eyeline" style="margin-top:14px">Signals</div>
  <ul class="list">${card.signals.map(line=>`<li>${esc(line)}</li>`).join('')}</ul>
  <div class="eyeline" style="margin-top:14px">What to do</div>
  <ul class="list">${card.what_to_do.map(line=>`<li>${esc(line)}</li>`).join('')}</ul>
  <div class="eyeline" style="margin-top:14px">What to underwrite</div>
  <ul class="list">${card.what_to_underwrite.map(line=>`<li>${esc(line)}</li>`).join('')}</ul>
  <div class="eyeline" style="margin-top:14px">Tensions</div>
  <ul class="list">${card.tensions.map(line=>`<li>${esc(line)}</li>`).join('')}</ul>
  <div class="eyeline" style="margin-top:14px">Second-order effects</div>
  <ul class="list">${card.second_order.map(line=>`<li>${esc(line)}</li>`).join('')}</ul>
  <ul class="list">${card.use_cases.map(line=>`<li>${esc(line)}</li>`).join('')}</ul>
 </article>`).join('');
document.getElementById('lens-cards').innerHTML=D.lensCards.map(card=>`
 <article class="lens-card">
  <div class="eyeline">${esc(card.label)} lens</div>
  <h3><a href="${esc(card.href)}">${esc(card.title)}</a></h3>
  <p>${esc(card.summary)}</p>
  <div class="eyeline" style="margin-top:14px">Themes</div>
  <div class="microchips">${card.themes.map(item=>`<span class="microchip">${esc(item)}</span>`).join('')}</div>
  <div class="eyeline" style="margin-top:14px">Subthemes</div>
  <div class="microchips">${card.subthemes.map(item=>`<span class="microchip">${esc(item)}</span>`).join('')}</div>
  <div class="eyeline" style="margin-top:14px">Where it shows up</div>
  <div class="microchips">${card.sectors.concat(card.companies).map(item=>`<span class="microchip">${esc(item)}</span>`).join('')}</div>
  <div class="eyeline" style="margin-top:14px">What to do</div>
  <ul class="list">${card.operator_moves.map(item=>`<li>${esc(item)}</li>`).join('')}</ul>
  <div class="eyeline" style="margin-top:14px">What to underwrite</div>
  <ul class="list">${card.investor_moves.map(item=>`<li>${esc(item)}</li>`).join('')}</ul>
  <div class="eyeline" style="margin-top:14px">Signals</div>
  <ul class="list">${card.signals.map(item=>`<li>${esc(item)}</li>`).join('')}</ul>
  <div class="eyeline" style="margin-top:14px">Tensions</div>
  <ul class="list">${card.tensions.map(item=>`<li>${esc(item)}</li>`).join('')}</ul>
  <div class="eyeline" style="margin-top:14px">Second-order effects</div>
  <ul class="list">${card.second_order.map(item=>`<li>${esc(item)}</li>`).join('')}</ul>
 </article>`).join('');
const filters=document.getElementById('filters');
filters.innerHTML=`<span class="chip on" data-f="all">All</span>`+D.sectors.map(s=>
 `<span class="chip" data-f="${esc(s)}"><span class="cdot" style="background:${SC[s]}"></span>${esc(s)}</span>`).join('');
function cardHTML(b){
 const g=b.key_stats.growth||'n/a';
 return `<button class="card" style="--sc:${SC[b.sector]}" data-slug="${b.slug}">
  <div class="co">${esc(b.title)}</div><div class="one">${esc(b.one_liner)}</div>
  <div class="mini"><span><b>${esc(b.key_stats.market_size||'n/a')}</b></span>
  <span class="${gcls(g)}">${esc(g)}</span></div></button>`;
}
function renderResults(q,sector){
 q=(q||'').trim().toLowerCase(); const out=[];
 for(const s of D.sectors){
  const items=D.industries.filter(b=>b.sector===s && (sector==='all'||b.sector===sector) &&
    (!q||b.title.toLowerCase().includes(q)||s.toLowerCase().includes(q)||(b.themes||[]).join(' ').toLowerCase().includes(q)));
  if(!items.length) continue;
  out.push(`<div class="sechead"><span class="cdot" style="background:${SC[s]};width:10px;height:10px"></span><h2>${esc(s)}</h2><span class="c">${items.length}</span></div><div class="grid">${items.map(cardHTML).join('')}</div>`);
 }
 document.getElementById('results').innerHTML=out.join('');
 document.getElementById('nores').classList.toggle('hidden',out.length>0);
}
let curSector='all';
document.getElementById('q').addEventListener('input',e=>renderResults(e.target.value,curSector));
filters.addEventListener('click',e=>{const c=e.target.closest('.chip');if(!c)return;
 filters.querySelectorAll('.chip').forEach(x=>x.classList.remove('on'));c.classList.add('on');
 curSector=c.dataset.f;renderResults(document.getElementById('q').value,curSector);});
const scrim=document.getElementById('scrim'),panel=document.getElementById('panel');
function openDetail(slug){
 const b=bySlug[slug]; if(!b)return; const col=SC[b.sector], k=b.key_stats, base=b.baseline_2022||{};
 const players=(b.major_players&&b.major_players.length?b.major_players:['n/a']).map(p=>`<span class="pl">${esc(p)}</span>`).join('');
 const themes=(b.themes||[]).map(t=>`<span class="tc">${esc(t)}</span>`).join('');
 const devs=(b.recent_developments||[]).map(d=>`<li>${esc(d)}</li>`).join('');
 const srcs=(b.sources||[]).map(s=>`<li>${esc(s)}</li>`).join('');
 const was=base.market_size?`<div class="was">2022 baseline: ${esc(base.market_size)}</div>`:'';
 document.getElementById('pinner').innerHTML=`
  <button class="pclose" id="pclose" aria-label="Close">&times;</button>
  <span class="sectag" style="color:${col};border-color:${col}"><span class="cdot" style="background:${col}"></span>${esc(b.sector)}</span><span class="dyr">data: ${esc(b.data_year||'2025-2026')}</span>
  <h2>${esc(b.title)}</h2><div class="liner">${esc(b.one_liner)}</div>
  <div class="kstats">
   <div class="ks big"><div class="l">Market size (latest)</div><div class="v">${esc(k.market_size||'n/a')}</div>${was}</div>
   <div class="ks"><div class="l">Growth</div><div class="v ${gcls(k.growth||'')}">${esc(k.growth||'n/a')}</div></div>
   <div class="ks"><div class="l">Profit margin</div><div class="v">${esc(k.profit_margin||'n/a')}</div></div>
   <div class="ks"><div class="l">Businesses</div><div class="v">${esc(k.businesses||'n/a')}</div></div>
   <div class="ks"><div class="l">Employees</div><div class="v">${esc(k.employees||'n/a')}</div></div>
  </div>
  <div class="blk"><h4>What it is</h4><p>${esc(b.overview)}</p></div>
  <div class="now"><h4>&#9679; What's happening now (2025&ndash;2026)</h4><p>${esc(b.current_dynamics||b.overview)}</p></div>
  <div class="psplit">
   <div class="pane u"><h4>&uarr; Growing</h4><p>${esc(b.whats_growing)}</p></div>
   <div class="pane d"><h4>&darr; Shrinking</h4><p>${esc(b.whats_shrinking)}</p></div>
  </div>
  ${devs?`<div class="blk"><h4>Recent developments</h4><ul class="devs">${devs}</ul></div>`:''}
  ${b.outlook?`<div class="blk"><h4>Outlook to 2026&ndash;2027</h4><p>${esc(b.outlook)}</p></div>`:''}
  <div class="blk"><h4>How it makes money</h4><p>${esc(b.how_it_makes_money)}</p></div>
  <div class="blk"><h4>Cost structure</h4><p>${esc(b.cost_structure)}</p></div>
  <div class="blk"><h4>Major players</h4><div class="players">${players}</div></div>
  <div class="blk"><h4>Forces shaping it</h4><div class="tchips">${themes}</div></div>
  <div class="take"><div class="l">The one takeaway</div><p>${esc(b.one_sentence)}</p></div>
  ${srcs?`<details class="src"><summary>Sources (${(b.sources||[]).length})</summary><ul>${srcs}</ul></details>`:''}`;
 panel.classList.add('on');scrim.classList.add('on');
 document.getElementById('pclose').onclick=closeDetail; panel.scrollTop=0;
}
function closeDetail(){panel.classList.remove('on');scrim.classList.remove('on');}
scrim.addEventListener('click',closeDetail);
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeDetail();});
document.getElementById('results').addEventListener('click',e=>{const c=e.target.closest('.card');if(c)openDetail(c.dataset.slug);});
document.getElementById('headline').textContent=D.headline;
document.getElementById('trends').innerHTML=D.trends.map(tr=>{
 const ev=D.trendEvidence[tr.name]||{sectors:[],themes:[],companies:[],operator_lines:[],investor_lines:[]};
 const hits=tr.slugs.map(s=>`<span class="hit" data-slug="${s}"><span class="cdot" style="background:${SC[bySlug[s].sector]}"></span>${esc(bySlug[s].title)}</span>`).join('');
 const exposure=ev.sectors.concat(ev.themes).map(item=>`<span class="microchip">${esc(item)}</span>`).join('');
 const companies=ev.companies.map(company=>`<article class="trendcompany">
   <div class="meta">${esc(company.sector)}</div>
   <h4><a href="company-memos/${esc(company.slug)}.html">${esc(company.title)}</a></h4>
   <p>${esc(company.memo)}</p>
  </article>`).join('');
 return `<div class="trend"><span class="cnt">${tr.slugs.length} industries</span><span class="kind">${esc(tr.kind)}</span>
  <h3>${esc(tr.name)}</h3><p>${esc(tr.what_it_is)}</p>
  <div class="wl"><div class="win"><b>Who wins</b>${esc(tr.who_wins)}</div><div class="lose"><b>Who's squeezed</b>${esc(tr.who_loses)}</div></div>
  <div class="eyeline" style="margin-top:10px">Where it shows up</div>
  <div class="microchips">${exposure}</div>
  <div class="trendmini">${companies}</div>
  <div class="trenddeep">
   <div class="trendbox"><h4>Tensions</h4><ul>${(ev.tensions||[]).map(item=>`<li>${esc(item)}</li>`).join('')}</ul></div>
   <div class="trendbox"><h4>Signals</h4><ul>${(ev.signals||[]).map(item=>`<li>${esc(item)}</li>`).join('')}</ul></div>
   <div class="trendbox"><h4>Second-order effects</h4><ul>${(ev.second_order||[]).map(item=>`<li>${esc(item)}</li>`).join('')}</ul></div>
  </div>
  <div class="trendgrid">
   <div class="trendbox"><h4>What to do</h4><ul>${ev.operator_lines.map(item=>`<li>${esc(item)}</li>`).join('')}</ul></div>
   <div class="trendbox"><h4>What to underwrite</h4><ul>${ev.investor_lines.map(item=>`<li>${esc(item)}</li>`).join('')}</ul></div>
  </div>
  <div class="hits">${hits}</div></div>`;
}).join('');
document.getElementById('trends').addEventListener('click',e=>{const h=e.target.closest('.hit');if(h)openDetail(h.dataset.slug);});
document.querySelector('.tabs').addEventListener('click',e=>{const t=e.target.closest('.tab');if(!t)return;
 document.querySelectorAll('.tab').forEach(x=>x.classList.remove('on'));t.classList.add('on');
 const v=t.dataset.view;
 document.getElementById('view-ov').classList.toggle('hidden',v!=='ov');
 document.getElementById('view-ind').classList.toggle('hidden',v!=='ind');
 document.getElementById('view-tr').classList.toggle('hidden',v!=='tr');});
renderResults('','all');
</script>
"""
out=PAGE.replace("__DATA__", DATA)
open(f'{ROOT}/index.html','w').write(out)
print("wrote index.html", len(out), "bytes;", len(clean_trends), "trends;", len(briefs), "industries")
