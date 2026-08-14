#!/usr/bin/env python3
"""Top-level 'Forces from the Data' hub: all force collections grouped by lens."""
import json, os, glob, html
ROOT=os.path.dirname(os.path.abspath(__file__))
industry_count=len(json.load(open(f'{ROOT}/briefs_full.json')))
def e(s): return html.escape(str(s or ''),quote=True)
forces=[]
for p in sorted(glob.glob(f'{ROOT}/_forcebuild_*.json')):
    f=json.load(open(p))['force']
    n=sum(len(v) for v in f['groups'].values())
    forces.append({"slug":f['slug'],"title":f['title'],"sig":f['signature'],"lens":f['lens'],"acc":f.get('acc','blue'),"n":n})
LENS_ORDER=["Societal","Cultural","Technological","Industrial","Economic"]
LENS_DESC={"Societal":"Who we are and how we work","Cultural":"How taste and spending shift",
 "Technological":"What the machines are changing","Industrial":"How the economy's machine reorganizes",
 "Economic":"The money pressures underneath"}
bylens={}
for f in forces: bylens.setdefault(f['lens'],[]).append(f)
os.makedirs(f'{ROOT}/forces',exist_ok=True)
STYLES=open(f'{ROOT}/_house_styles.css').read()
open(f'{ROOT}/forces/styles.css','w').write(STYLES)
sections=""
total=len(forces); totalpages=sum(f['n'] for f in forces)
for lens in LENS_ORDER:
    fs=bylens.get(lens,[])
    if not fs: continue
    cards=""
    for f in fs:
        cards+=(f'<a class="fcard acc-{f["acc"]}" href="{f["slug"]}/index.html">'
                f'<div class="ft">{e(f["title"])}</div><div class="fs">{e(f["sig"])}</div>'
                f'<div class="fn">{f["n"]} write-ups →</div></a>\n')
    sections+=(f'<section class="lens"><div class="lens-h"><h2>{e(lens)}</h2><span>{e(LENS_DESC[lens])}</span></div>'
               f'<div class="fgrid">{cards}</div></section>\n')
hub=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Forces from the Data — what {totalpages} write-ups across {industry_count} industries reveal</title>
<link rel="stylesheet" href="styles.css">
<style>
.wrap{{max-width:1180px}}
.lens{{margin:2.6em 0 0}}
.lens-h{{display:flex;align-items:baseline;gap:14px;flex-wrap:wrap;padding-top:1.3em;border-top:1px solid var(--line2);margin-bottom:.8em}}
.lens-h h2{{font-size:1.5rem;border:none;padding:0;margin:0;color:var(--ink)}}
.lens-h span{{font-family:var(--mono);font-size:.74rem;color:var(--ink3)}}
.fgrid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}}
.fcard{{background:var(--g1);border:1px solid var(--line2);border-radius:13px;padding:18px 20px;border-left:3px solid var(--accent);text-decoration:none;display:block;transition:transform .13s,background .13s}}
.fcard:hover{{transform:translateY(-2px);background:var(--g2)}}
.fcard .ft{{font-size:1.24rem;font-weight:700;color:var(--ink);line-height:1.15}}
.fcard .fs{{font-size:.96rem;color:var(--ink2);margin:.4em 0 .7em;font-style:italic;line-height:1.5}}
.fcard .fn{{font-family:var(--mono);font-size:.7rem;color:var(--accent)}}
</style></head>
<body class="acc-blue">
<div class="wrap">
  <div class="top"><a href="../index.html">★ the {industry_count} industry briefs</a><a href="../economic-intelligence.html">economic intelligence</a><a href="../american-themes.html">American themes</a></div>
  <header class="hero">
    <div class="eyebrow">Forces from the data · US · 2025–2026</div>
    <h1>Forces from the Data</h1>
    <div class="sub">We read {industry_count} US industries side by side and asked one question: what forces keep showing up? These are the {total} that do — each built out into its own collection, with the real numbers as proof.</div>
  </header>
  <div class="big"><div class="lbl">The method</div><p>These forces are read straight from hard 2025–2026 industry data, not headlines. Every claim traces back to a specific industry we researched. {totalpages} write-ups across {total} forces and five lenses.</p></div>
  {sections}
  <footer>Built from our 2025–2026 US industry research (the <a href="../index.html">{industry_count} industry briefs</a>).</footer>
</div></body></html>'''
open(f'{ROOT}/forces/index.html','w').write(hub)
print(f"built forces hub: {total} forces / {totalpages} write-ups across {len(bylens)} lenses")
