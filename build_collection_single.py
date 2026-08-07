#!/usr/bin/env python3
"""Bundle one force collection into a single self-contained navigable HTML (for Artifact review)."""
import json, os, sys, html, re
ROOT=os.path.dirname(os.path.abspath(__file__))
force_slug=sys.argv[1]     # e.g. the-ai-rewiring
build=json.load(open(f'{ROOT}/_forcebuild_{force_slug}.json'))
writeups={w['slug']:w for w in json.load(open(f'{ROOT}/_writeups_{force_slug}.json'))}
force=build['force']; specs=build['specs']; ACC=force.get('acc','blue')
def e(s): return html.escape(str(s or ''),quote=True)
def paras(t): return "".join(f"<p>{e(p.strip())}</p>" for p in re.split(r'\n\n+',str(t)) if p.strip()) or f"<p>{e(t)}</p>"
CSS=open(f'{ROOT}/_house_styles.css').read()
order=[s['slug'] for s in specs]; navt={s['slug']:s['title'] for s in specs}
GROUPS={}
for s in specs: GROUPS.setdefault(s['group'],[]).append(s)

def page_inner(i,s):
    w=writeups.get(s['slug']);
    if not w: return ""
    facts="".join(f'<div class="fact"><div class="num{" warn" if f.get("warn") else ""}">{e(f.get("num",""))}</div><div class="txt">{e(f.get("txt",""))}</div></div>' for f in (w.get('facts') or []))
    ev="".join(f"<li>{e(x)}</li>" for x in (w.get('evidence') or []))
    nxt=order[i+1] if i<len(order)-1 else None
    prev=order[i-1] if i>0 else None
    nav=f'<a href="#hub" class="rt">← all {len(order)}</a><a href="#patterns" class="rt">the patterns</a>'
    if prev: nav+=f'<a href="#{prev}" class="rt">← {e(navt[prev])}</a>'
    if nxt: nav+=f'<a href="#{nxt}" class="rt">{e(navt[nxt])} →</a>'
    return (f'<div class="top">{nav}</div>'
      f'<header class="hero"><div class="eyebrow">{e(s["group"])}</div><h1>{e(w.get("title"))}</h1><div class="sub">{e(w.get("dek"))}</div></header>'
      f'<p class="lede">{e(w.get("lede"))}</p>'
      f'<div class="cols"><main class="prose">'
      f'<h2>What changed</h2>{paras(w.get("what_changed"))}'
      f'<h2>The evidence</h2><ul class="pts">{ev}</ul>'
      f'<div class="split"><div class="s good"><h3>Who rides it</h3><p>{e(w.get("win"))}</p></div><div class="s bad"><h3>Who\'s squeezed</h3><p>{e(w.get("lose"))}</p></div></div>'
      f'<h2>The main worry</h2><div class="big warn"><div class="lbl">The single biggest risk</div><p>{e(w.get("worry"))}</p></div>'
      f'<h2>In one sentence</h2><div class="big"><div class="lbl">{e(navt[s["slug"]])} in a nutshell</div><p>{e(w.get("one_sentence"))}</p></div>'
      f'</main><aside class="rail"><div class="rail-h">By the numbers</div>{facts}</aside></div>')

cap=writeups.get(specs[-1]['slug'],{})
# hub inner
seccards=""
for grp,subs in GROUPS.items():
    cards="".join(f'<a class="card rt" href="#{s["slug"]}"><div class="co">{e(s["title"])}</div><div class="one">{e(writeups.get(s["slug"],{}).get("dek",""))}</div></a>' for s in subs)
    seccards+=f'<section class="sec"><div class="sec-h"><span class="tag">{e(grp.split(" · ")[0])}</span><h2>{e(grp.split(" · ",1)[1])}</h2></div><div class="cards">{cards}</div></section>'
hub_inner=(f'<header class="hero"><div class="eyebrow">A force from the data · {e(force["lens"])} · 2025–2026</div><h1>{e(force["title"])}</h1><div class="sub">{e(force["signature"])}</div></header>'
  f'<div class="seed"><span class="k">How we found this</span>This is what fell out of reading 221 US industries side by side — the same force kept reappearing. Each page below is one corner of the economy where it shows up, with the real 2025–2026 numbers as proof.</div>'
  f'<div class="big"><div class="lbl">The one idea</div><p>{e(cap.get("one_sentence",force["signature"]))}</p></div>'
  f'<p style="text-align:center;margin:1.4em 0"><a href="#patterns" class="rt" style="display:inline-block;font-family:var(--mono);font-size:.8rem;color:var(--accent);border:1px solid var(--accent);border-radius:24px;padding:10px 22px;text-decoration:none">★ The patterns — what repeats across all {len(order)} →</a></p>{seccards}')
# patterns inner
rows="".join(f'<div class="pat"><div class="n">{e(s["group"].split(" · ")[0])}</div><h3><a href="#{s["slug"]}" class="rt">{e(s["title"])}</a></h3><p>{e(writeups.get(s["slug"],{}).get("one_sentence",""))}</p></div>' for s in specs if s['slug']!=specs[-1]['slug'])
pat_inner=(f'<div class="top"><a href="#hub" class="rt">← all {len(order)}</a></div><header class="hero"><div class="eyebrow">The synthesis · what repeats across all {len(order)}</div><h1>The patterns</h1><div class="sub">{e(force["signature"])}</div></header>'
  f'<div class="big"><div class="lbl">The through-line</div><p>{e(cap.get("one_sentence",force["signature"]))}</p></div><h2>Where it shows up</h2>{rows}'
  f'<div class="split"><div class="s good"><h3>Who wins across the board</h3><p>{e(cap.get("win",""))}</p></div><div class="s bad"><h3>Who\'s squeezed</h3><p>{e(cap.get("lose",""))}</p></div></div>'
  f'<h2>The biggest tension</h2><div class="big warn"><div class="lbl">The one to watch</div><p>{e(cap.get("worry",""))}</p></div>')

sections=f'<section class="pg" id="hub">{hub_inner}</section>'
for i,s in enumerate(specs):
    sections+=f'<section class="pg" id="{s["slug"]}" hidden>{page_inner(i,s)}</section>'
sections+=f'<section class="pg" id="patterns" hidden>{pat_inner}</section>'

doc=f'''<title>{e(force["title"])} — a force from the industry data</title>
<style>{CSS}
.pg{{padding-top:8px}}
.sec{{margin:2.2em 0 0}}
.sec-h{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding-top:1.2em;border-top:1px solid var(--line2);margin-bottom:2px}}
.sec-h .tag{{font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;padding:2px 9px;border-radius:20px;border:1px solid var(--accent);color:var(--accent)}}
.sec-h h2{{font-size:1.35rem;border:none;padding:0;margin:0}}
.cards{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:1em 0}}
@media(max-width:620px){{.cards{{grid-template-columns:1fr}}}}
.card{{background:var(--g1);border:1px solid var(--line2);border-radius:11px;padding:15px 16px;border-left:3px solid var(--accent);text-decoration:none;display:block}}
.card:hover{{transform:translateY(-2px)}}.card .co{{font-size:1.05rem;color:var(--ink);font-weight:700}}.card .one{{font-size:.9rem;color:var(--ink2);margin-top:.25em;font-style:italic}}
.seed{{background:var(--g1);border:1px solid var(--line2);border-radius:10px;padding:13px 17px;margin:1.2em 0;font-size:.95rem;color:var(--ink2)}}
.seed .k{{font-family:var(--mono);font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);display:block;margin-bottom:5px}}
.pat{{background:var(--g1);border:1px solid var(--line2);border-radius:12px;padding:14px 18px;margin:11px 0;border-left:3px solid var(--accent)}}
.pat .n{{font-family:var(--mono);font-size:.64rem;letter-spacing:.1em;color:var(--ink3);text-transform:uppercase}}.pat h3{{font-size:1.1rem;margin:.15em 0 .4em}}.pat h3 a{{color:var(--ink);text-decoration:none}}.pat p{{font-size:.95rem;margin:0}}
</style>
<body class="acc-{ACC}">
<div class="wrap">{sections}</div>
<script>
function show(id){{id=id.replace('#','')||'hub';document.querySelectorAll('.pg').forEach(p=>p.hidden=p.id!==id);window.scrollTo(0,0);}}
document.addEventListener('click',e=>{{const a=e.target.closest('a.rt');if(a){{e.preventDefault();const id=a.getAttribute('href');history.replaceState(0,0,id);show(id);}}}});
show(location.hash);
</script>'''
open(f'{ROOT}/forces/{force["slug"]}-bundle.html','w').write(doc)
print("wrote bundle:",f'forces/{force["slug"]}-bundle.html', len(doc),"bytes")
