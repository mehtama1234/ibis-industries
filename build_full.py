#!/usr/bin/env python3
import json, html, re, os
from collections import Counter

from build_american_outlook import OUTLOOK
ROOT=os.path.dirname(os.path.abspath(__file__))
briefs=json.load(open(f'{ROOT}/briefs_full.json'))
trends=json.load(open(f'{ROOT}/trends_full_raw.json'))
american_themes=json.load(open(f'{ROOT}/american_themes_taxonomy.json'))
economic_intelligence=json.load(open(f'{ROOT}/economic_intelligence_taxonomy.json'))

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
    slugs=[]
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

def collect_lens_evidence(linked_themes):
    sector_counts=Counter()
    companies=[]
    subthemes=[]
    operator_moves=[]
    investor_moves=[]
    for slug in linked_themes:
        theme=theme_lookup[slug]
        operator_moves.extend(theme.get('strategic_implications', []))
        investor_moves.extend(theme.get('capital_implications', []))
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
    }

overview_cards=[
    {
        "label":"Master synthesis",
        "title":"American Outlook 2025-2026",
        "href":"american-outlook-2025-2026.html",
        "body":"The cleanest top-level read on societal, cultural, consumer, and industrial change across the full corpus.",
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
        "use_cases":[
            "Use this when you need strategic and capital implications fast.",
            "Best bridge from macro interpretation to diligence and action.",
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
    })

DATA=json.dumps({
 "industries":briefs,
 "trends":clean_trends,
 "headline":headline,
 "sectors":sectors_present,
 "sectorColor":SECTOR_COLOR,
 "workingThesis":economic_intelligence.get('working_thesis',''),
 "crosscuts":[c['title'] for c in economic_intelligence.get('crosscuts', [])[:6]],
 "overviewCards":overview_cards,
 "lensCards":lens_cards,
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
.overview-grid,.lens-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px}
.overview-card,.lens-card{background:var(--panel);border:1px solid var(--line2);border-radius:13px;padding:18px}
.eyeline{font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;color:var(--brass)}
.overview-card h3,.lens-card h3{font-size:1.08rem;margin:.22em 0 .35em}
.overview-card p,.lens-card p{color:var(--muted)}
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
document.getElementById('overview-cards').innerHTML=D.overviewCards.map(card=>`
 <article class="overview-card">
  <div class="eyeline">${esc(card.label)}</div>
  <h3><a href="${esc(card.href)}">${esc(card.title)}</a></h3>
  <p>${esc(card.body)}</p>
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
 const hits=tr.slugs.map(s=>`<span class="hit" data-slug="${s}"><span class="cdot" style="background:${SC[bySlug[s].sector]}"></span>${esc(bySlug[s].title)}</span>`).join('');
 return `<div class="trend"><span class="cnt">${tr.slugs.length} industries</span><span class="kind">${esc(tr.kind)}</span>
  <h3>${esc(tr.name)}</h3><p>${esc(tr.what_it_is)}</p>
  <div class="wl"><div class="win"><b>Who wins</b>${esc(tr.who_wins)}</div><div class="lose"><b>Who's squeezed</b>${esc(tr.who_loses)}</div></div>
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
