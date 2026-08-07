#!/usr/bin/env python3
"""Combine ALL force collections into one self-contained navigable HTML (top hub -> collection hubs -> pages/patterns)."""
import json, os, glob, html, re
ROOT=os.path.dirname(os.path.abspath(__file__))
def e(s): return html.escape(str(s or ''),quote=True)
def paras(t): return "".join(f"<p>{e(p.strip())}</p>" for p in re.split(r'\n\n+',str(t)) if p.strip()) or f"<p>{e(t)}</p>"
CSS=open(f'{ROOT}/_house_styles.css').read()
LENS_ORDER=["Societal","Cultural","Technological","Industrial","Economic"]
LENS_DESC={"Societal":"Who we are and how we work","Cultural":"How taste and spending shift","Technological":"What the machines are changing","Industrial":"How the economy's machine reorganizes","Economic":"The money pressures underneath"}

forces=[]
for p in sorted(glob.glob(f'{ROOT}/_forcebuild_*.json')):
    b=json.load(open(p)); f=b['force']; slug=f['slug']
    wf=f'{ROOT}/_writeups_{slug}.json'
    if not os.path.exists(wf): continue
    wr={w['slug']:w for w in json.load(open(wf))}
    forces.append({"force":f,"specs":b['specs'],"wr":wr})

def pid(force,sub): return f"{force}--{sub}"
sections=[]

# top hub
bylens={}
for fc in forces: bylens.setdefault(fc['force']['lens'],[]).append(fc)
lensblocks=""
for lens in LENS_ORDER:
    fs=bylens.get(lens,[])
    if not fs: continue
    cards="".join(f'<a class="fcard rt acc-{fc["force"]["acc"]}" href="#hub--{fc["force"]["slug"]}"><div class="ft">{e(fc["force"]["title"])}</div><div class="fs">{e(fc["force"]["signature"])}</div><div class="fn">{len(fc["specs"])} write-ups →</div></a>' for fc in fs)
    lensblocks+=f'<section class="lens"><div class="lens-h"><h2>{e(lens)}</h2><span>{e(LENS_DESC[lens])}</span></div><div class="fgrid">{cards}</div></section>'
totalpages=sum(len(fc['specs']) for fc in forces)
home=(f'<header class="hero"><div class="eyebrow">Forces from the data · US · 2025–2026</div><h1>Forces from the Data</h1>'
  f'<div class="sub">We read 221 US industries side by side and asked: what forces keep showing up? These are the {len(forces)} that do — each its own collection, with the real numbers as proof.</div></header>'
  f'<div class="big"><div class="lbl">The method</div><p>The data-grounded companion to the Strategy Under a Force series. Every claim traces back to a specific industry we researched — {totalpages} write-ups across {len(forces)} forces and five lenses.</p></div>{lensblocks}')
sections.append(f'<section class="pg" id="home">{home}</section>')

for fc in forces:
    f=fc['force']; specs=fc['specs']; wr=fc['wr']; ACC=f['acc']; fslug=f['slug']
    order=[s['slug'] for s in specs]; navt={s['slug']:s['title'] for s in specs}
    GROUPS={}
    for s in specs: GROUPS.setdefault(s['group'],[]).append(s)
    cap=wr.get(specs[-1]['slug'],{})
    # collection hub
    seccards=""
    for grp,subs in GROUPS.items():
        cc="".join(f'<a class="card rt" href="#{pid(fslug,s["slug"])}"><div class="co">{e(s["title"])}</div><div class="one">{e(wr.get(s["slug"],{}).get("dek",""))}</div></a>' for s in subs)
        seccards+=f'<section class="sec"><div class="sec-h"><span class="tag">{e(grp.split(" · ")[0])}</span><h2>{e(grp.split(" · ",1)[1] if " · " in grp else grp)}</h2></div><div class="cards">{cc}</div></section>'
    hub=(f'<div class="top"><a href="#home" class="rt">← all forces</a><a href="#patterns--{fslug}" class="rt">the patterns →</a></div>'
      f'<header class="hero"><div class="eyebrow">A force from the data · {e(f["lens"])} · 2025–2026</div><h1>{e(f["title"])}</h1><div class="sub">{e(f["signature"])}</div></header>'
      f'<div class="big"><div class="lbl">The one idea</div><p>{e(cap.get("one_sentence",f["signature"]))}</p></div>{seccards}')
    sections.append(f'<section class="pg" id="hub--{fslug}" hidden>{hub}</section>')
    # subforce pages
    for i,s in enumerate(specs):
        w=wr.get(s['slug'])
        if not w: continue
        facts="".join(f'<div class="fact"><div class="num{" warn" if ft.get("warn") else ""}">{e(ft.get("num",""))}</div><div class="txt">{e(ft.get("txt",""))}</div></div>' for ft in (w.get('facts') or []))
        ev="".join(f"<li>{e(x)}</li>" for x in (w.get('evidence') or []))
        prev=order[i-1] if i>0 else None; nxt=order[i+1] if i<len(order)-1 else None
        nav=f'<a href="#hub--{fslug}" class="rt">← all {len(order)}</a><a href="#patterns--{fslug}" class="rt">patterns</a>'
        if prev: nav+=f'<a href="#{pid(fslug,prev)}" class="rt">← {e(navt[prev])}</a>'
        if nxt: nav+=f'<a href="#{pid(fslug,nxt)}" class="rt">{e(navt[nxt])} →</a>'
        body=(f'<div class="top">{nav}</div>'
          f'<header class="hero"><div class="eyebrow">{e(s["group"])}</div><h1>{e(w.get("title"))}</h1><div class="sub">{e(w.get("dek"))}</div></header>'
          f'<p class="lede">{e(w.get("lede"))}</p><div class="cols"><main class="prose">'
          f'<h2>What changed</h2>{paras(w.get("what_changed"))}'
          f'<h2>The evidence</h2><ul class="pts">{ev}</ul>'
          f'<div class="split"><div class="s good"><h3>Who rides it</h3><p>{e(w.get("win"))}</p></div><div class="s bad"><h3>Who\'s squeezed</h3><p>{e(w.get("lose"))}</p></div></div>'
          f'<h2>The main worry</h2><div class="big warn"><div class="lbl">The single biggest risk</div><p>{e(w.get("worry"))}</p></div>'
          f'<h2>In one sentence</h2><div class="big"><div class="lbl">{e(navt[s["slug"]])} in a nutshell</div><p>{e(w.get("one_sentence"))}</p></div>'
          f'</main><aside class="rail"><div class="rail-h">By the numbers</div>{facts}</aside></div>')
        sections.append(f'<section class="pg" id="{pid(fslug,s["slug"])}" hidden>{body}</section>')
    # patterns
    rows="".join(f'<div class="pat"><div class="n">{e(s["group"].split(" · ")[0])}</div><h3><a href="#{pid(fslug,s["slug"])}" class="rt">{e(s["title"])}</a></h3><p>{e(wr.get(s["slug"],{}).get("one_sentence",""))}</p></div>' for s in specs if s['slug']!=specs[-1]['slug'])
    pat=(f'<div class="top"><a href="#hub--{fslug}" class="rt">← all {len(order)}</a><a href="#home" class="rt">★ all forces</a></div>'
      f'<header class="hero"><div class="eyebrow">The synthesis · {e(f["title"])}</div><h1>The patterns</h1><div class="sub">{e(f["signature"])}</div></header>'
      f'<div class="big"><div class="lbl">The through-line</div><p>{e(cap.get("one_sentence",f["signature"]))}</p></div><h2>Where it shows up</h2>{rows}'
      f'<div class="split"><div class="s good"><h3>Who wins across the board</h3><p>{e(cap.get("win",""))}</p></div><div class="s bad"><h3>Who\'s squeezed across the board</h3><p>{e(cap.get("lose",""))}</p></div></div>'
      f'<h2>The biggest tension</h2><div class="big warn"><div class="lbl">The one to watch</div><p>{e(cap.get("worry",""))}</p></div>')
    sections.append(f'<section class="pg" id="patterns--{fslug}" hidden>{pat}</section>')

doc=f'''<title>Forces from the Data — {len(forces)} forces across 221 US industries</title>
<style>{CSS}
.pg{{padding-top:6px}}
.lens{{margin:2.2em 0 0}}.lens-h{{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;padding-top:1.2em;border-top:1px solid var(--line2);margin-bottom:.7em}}
.lens-h h2{{font-size:1.45rem;border:none;padding:0;margin:0}}.lens-h span{{font-family:var(--mono);font-size:.72rem;color:var(--ink3)}}
.fgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));gap:13px}}
.fcard{{background:var(--g1);border:1px solid var(--line2);border-radius:13px;padding:17px 19px;border-left:3px solid var(--accent);text-decoration:none;display:block}}
.fcard:hover{{transform:translateY(-2px)}}.fcard .ft{{font-size:1.2rem;font-weight:700;color:var(--ink)}}.fcard .fs{{font-size:.94rem;color:var(--ink2);margin:.35em 0 .6em;font-style:italic}}.fcard .fn{{font-family:var(--mono);font-size:.68rem;color:var(--accent)}}
.sec{{margin:2em 0 0}}.sec-h{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding-top:1.1em;border-top:1px solid var(--line2);margin-bottom:2px}}
.sec-h .tag{{font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;padding:2px 9px;border-radius:20px;border:1px solid var(--accent);color:var(--accent)}}.sec-h h2{{font-size:1.3rem;border:none;padding:0;margin:0}}
.cards{{display:grid;grid-template-columns:repeat(auto-fill,minmax(260px,1fr));gap:12px;margin:1em 0}}
.card{{background:var(--g1);border:1px solid var(--line2);border-radius:11px;padding:14px 16px;border-left:3px solid var(--accent);text-decoration:none;display:block}}.card:hover{{transform:translateY(-2px)}}.card .co{{font-size:1.03rem;color:var(--ink);font-weight:700}}.card .one{{font-size:.88rem;color:var(--ink2);margin-top:.25em;font-style:italic}}
.pat{{background:var(--g1);border:1px solid var(--line2);border-radius:12px;padding:14px 18px;margin:11px 0;border-left:3px solid var(--accent)}}.pat .n{{font-family:var(--mono);font-size:.64rem;letter-spacing:.1em;color:var(--ink3);text-transform:uppercase}}.pat h3{{font-size:1.08rem;margin:.15em 0 .4em}}.pat h3 a{{color:var(--ink);text-decoration:none}}.pat p{{font-size:.94rem;margin:0}}
</style>
<body class="acc-blue">
<div class="wrap">{"".join(sections)}</div>
<script>
function show(id){{id=(id||'').replace('#','')||'home';var el=document.getElementById(id);if(!el){{id='home';}}document.querySelectorAll('.pg').forEach(p=>p.hidden=p.id!==id);
 // set body accent from target section's nearest acc- class on cards? default keep. scroll top.
 window.scrollTo(0,0);}}
document.addEventListener('click',e=>{{var a=e.target.closest('a.rt');if(a){{e.preventDefault();var id=a.getAttribute('href');history.replaceState(0,0,id);show(id);}}}});
show(location.hash);
</script>'''
open(f'{ROOT}/forces-mega-bundle.html','w').write(doc)
print(f"wrote forces-mega-bundle.html: {len(forces)} forces, {len(sections)} sections, {len(doc)} bytes")
