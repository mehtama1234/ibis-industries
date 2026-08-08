#!/usr/bin/env python3
"""Build one 'force' collection (hub + subforce pages + patterns) in the Strategy-Under-a-Force house style."""
import json, os, sys, html, re

ROOT=os.path.dirname(os.path.abspath(__file__))
force_slug=sys.argv[1]                       # e.g. the-ai-rewiring
build=json.load(open(f'{ROOT}/_forcebuild_{force_slug}.json'))
writeups={w['slug']:w for w in json.load(open(f'{ROOT}/_writeups_{force_slug}.json'))}
force=build['force']; specs=build['specs']
OUT=f'{ROOT}/forces/{force_slug}'; os.makedirs(OUT,exist_ok=True)
ACC=force.get('acc','blue')
def e(s): return html.escape(str(s or ''), quote=True)
def paras(txt):
    return "".join(f"<p>{e(p.strip())}</p>\n" for p in re.split(r'\n\n+|\n(?=[A-Z])', str(txt)) if p.strip()) or f"<p>{e(txt)}</p>"

# ---- copy house styles.css (self-contained) ----
STYLES=open(f'{ROOT}/_house_styles.css').read()
open(f'{OUT}/styles.css','w').write(STYLES)

# order = specs order (already A..E)
order=[s['slug'] for s in specs]
navtitle={s['slug']:s['title'] for s in specs}
groupof={s['slug']:s['group'] for s in specs}

def page(i, s):
    w=writeups.get(s['slug'])
    if not w: return
    slug=s['slug']; grp=s['group']
    prev=order[i-1] if i>0 else None
    nxt=order[i+1] if i<len(order)-1 else None
    topnav=f'<a href="index.html">← all {len(order)}</a><a href="patterns.html">the patterns</a>'
    if prev: topnav+=f'<a href="{prev}.html">← {e(navtitle[prev])}</a>'
    if nxt: topnav+=f'<a href="{nxt}.html">{e(navtitle[nxt])} →</a>'
    topnav+='<a href="../../index.html">★ industry briefs</a><a href="../../../strategy-under-a-force/index.html">the 50 forces</a>'
    facts="".join(
      f'<div class="fact"><div class="num{" warn" if f.get("warn") else ""}">{e(f.get("num",""))}</div>'
      f'<div class="txt">{e(f.get("txt",""))}</div></div>\n' for f in (w.get('facts') or []))
    ev="".join(f'<li>{e(x)}</li>\n' for x in (w.get('evidence') or []))
    nextfoot=f'Next: <a href="{nxt}.html">{e(navtitle[nxt])} →</a>' if nxt else 'The end of the collection.'
    htmlp=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(w.get("title"))} — {e(force["title"])}</title>
<link rel="stylesheet" href="styles.css"></head>
<body class="acc-{ACC}">
<div class="wrap">
  <div class="top">{topnav}</div>
  <header class="hero">
    <div class="eyebrow">{e(grp)}</div>
    <h1>{e(w.get("title"))}</h1>
    <div class="sub">{e(w.get("dek"))}</div>
  </header>
  <p class="lede">{e(w.get("lede"))}</p>
  <div class="cols">
    <main class="prose">
      <h2>What changed</h2>
      {paras(w.get("what_changed"))}
      <h2>The evidence</h2>
      <ul class="pts">{ev}</ul>
      <div class="split">
        <div class="s good"><h3>Who rides it</h3><p>{e(w.get("win"))}</p></div>
        <div class="s bad"><h3>Who's squeezed</h3><p>{e(w.get("lose"))}</p></div>
      </div>
      <h2>The main worry</h2>
      <div class="big warn"><div class="lbl">The single biggest risk</div><p>{e(w.get("worry"))}</p></div>
      <h2>In one sentence</h2>
      <div class="big"><div class="lbl">{e(navtitle[slug])} in a nutshell</div><p>{e(w.get("one_sentence"))}</p></div>
    </main>
    <aside class="rail"><div class="rail-h">By the numbers</div>{facts}</aside>
  </div>
  <footer>{e(grp)}. {nextfoot}<br><br><a href="index.html">← back to all {len(order)}</a> · Grounded in our 2025–2026 US industry research. Research uses the configured model.</footer>
</div></body></html>'''
    open(f'{OUT}/{slug}.html','w').write(htmlp)

for i,s in enumerate(specs): page(i,s)

# ---- hub ----
GROUPS={}
for s in specs: GROUPS.setdefault(s['group'],[]).append(s)
acccol={'blue':'--blue','red':'--red','teal':'--teal','purple':'--purple','gold':'--gold','green':'--green','orange':'--orange'}[ACC]
seccards=""
gi=0
for grp,subs in GROUPS.items():
    gi+=1
    cards=""
    for s in subs:
        w=writeups.get(s['slug'],{})
        cards+=(f'<a class="card" href="{s["slug"]}.html"><div class="co">{e(s["title"])}</div>'
                f'<div class="one">{e(w.get("dek",""))}</div></a>\n')
    seccards+=(f'<section class="sec"><div class="sec-h"><span class="tag">{e(grp.split(" · ")[0])}</span>'
               f'<h2>{e(grp.split(" · ",1)[1] if " · " in grp else grp)}</h2></div><div class="cards">{cards}</div></section>\n')
cap=writeups.get('the-ai-rewiring',{}) if 'the-ai-rewiring' in writeups else writeups.get(specs[-1]['slug'],{})
hub=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(force["title"])} — a force from the industry data</title>
<link rel="stylesheet" href="styles.css">
<style>
.wrap{{max-width:900px}}
.seed{{background:var(--g1);border:1px solid var(--line2);border-radius:10px;padding:13px 17px;margin:1.3em 0;font-size:.95rem;color:var(--ink2)}}
.seed .k{{font-family:var(--mono);font-size:.62rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent);display:block;margin-bottom:5px}}
.sec{{margin:2.4em 0 0}}
.sec-h{{display:flex;align-items:baseline;gap:12px;flex-wrap:wrap;padding-top:1.3em;border-top:1px solid var(--line2);margin-bottom:2px}}
.sec-h .tag{{font-family:var(--mono);font-size:.66rem;letter-spacing:.1em;text-transform:uppercase;padding:2px 9px;border-radius:20px;border:1px solid var(--accent);color:var(--accent)}}
.sec-h h2{{font-size:1.4rem;border:none;padding:0;margin:0}}
.cards{{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:1em 0}}
@media(max-width:620px){{.cards{{grid-template-columns:1fr}}}}
.card{{background:var(--g1);border:1px solid var(--line2);border-radius:11px;padding:15px 16px;border-left:3px solid var(--accent);text-decoration:none;display:block;transition:transform .13s}}
.card:hover{{transform:translateY(-2px)}}
.card .co{{font-size:1.06rem;color:var(--ink);font-weight:700}}
.card .one{{font-size:.9rem;color:var(--ink2);margin-top:.25em;font-style:italic;line-height:1.4}}
</style></head>
<body class="acc-{ACC}">
<div class="wrap">
  <div class="top"><a href="../../index.html">★ the industry briefs</a><a href="../../../strategy-under-a-force/index.html">the 50 forces</a><a href="patterns.html">the patterns →</a></div>
  <header class="hero">
    <div class="eyebrow">A force from the data · {e(force["lens"])} · 2025–2026</div>
    <h1>{e(force["title"])}</h1>
    <div class="sub">{e(force["signature"])}</div>
  </header>
  <div class="seed"><span class="k">How we found this</span>
  This isn't a hunch — it's what fell out of reading {open(f'{ROOT}/briefs_full.json').read().count(chr(34)+"slug"+chr(34))} US industries side by side. The same force kept reappearing. Each page below is one corner of the economy where it shows up, with the real 2025–2026 numbers as proof.</div>
  <div class="big"><div class="lbl">The one idea</div><p>{e(cap.get("one_sentence", force["signature"]))}</p></div>
  <p style="text-align:center;margin:1.6em 0"><a href="patterns.html" style="display:inline-block;font-family:var(--mono);font-size:.8rem;color:var(--accent);border:1px solid var(--accent);border-radius:24px;padding:10px 22px;text-decoration:none">★ The patterns — what repeats across all {len(order)} &nbsp;→</a></p>
  {seccards}
  <footer>A data-grounded companion to the <a href="../../../strategy-under-a-force/index.html">Strategy Under a Force</a> series. Built from our 2025–2026 US industry research. Research uses the configured model.</footer>
</div></body></html>'''
open(f'{OUT}/index.html','w').write(hub)

# ---- patterns.html ----
rows=""
for i,s in enumerate(specs,1):
    w=writeups.get(s['slug'],{})
    if s['slug']==(cap and cap.get('slug')): continue
    rows+=(f'<div class="pat"><div class="n">{e(s["group"].split(" · ")[0])}</div>'
           f'<h3><a href="{s["slug"]}.html">{e(s["title"])}</a></h3><p>{e(w.get("one_sentence",""))}</p></div>\n')
pat=f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>The patterns — {e(force["title"])}</title>
<link rel="stylesheet" href="styles.css">
<style>
.pat{{background:var(--g1);border:1px solid var(--line2);border-radius:12px;padding:15px 18px;margin:12px 0;border-left:3px solid var(--accent)}}
.pat .n{{font-family:var(--mono);font-size:.64rem;letter-spacing:.1em;color:var(--ink3);text-transform:uppercase}}
.pat h3{{font-size:1.12rem;margin:.15em 0 .4em}}.pat h3 a{{color:var(--ink);text-decoration:none}}.pat h3 a:hover{{color:var(--accent)}}
.pat p{{font-size:.96rem;margin:0}}
</style></head>
<body class="acc-{ACC}">
<div class="wrap">
  <div class="top"><a href="index.html">← all {len(order)}</a><a href="../../index.html">★ industry briefs</a><a href="../../../strategy-under-a-force/index.html">the 50 forces</a></div>
  <header class="hero"><div class="eyebrow">The synthesis · what repeats across all {len(order)}</div>
  <h1>The patterns</h1>
  <div class="sub">{e(force["signature"])}</div></header>
  <p class="lede">{e(cap.get("what_changed","").split(chr(10))[0] if cap.get("what_changed") else force["signature"])}</p>
  <div class="big"><div class="lbl">The through-line</div><p>{e(cap.get("one_sentence", force["signature"]))}</p></div>
  <h2>Where it shows up</h2>
  {rows}
  <div class="split">
    <div class="s good"><h3>Who wins across the board</h3><p>{e(cap.get("win",""))}</p></div>
    <div class="s bad"><h3>Who's squeezed across the board</h3><p>{e(cap.get("lose",""))}</p></div>
  </div>
  <h2>The biggest tension</h2>
  <div class="big warn"><div class="lbl">The one to watch</div><p>{e(cap.get("worry",""))}</p></div>
  <footer>Drawn from all {len(order)} pages. <a href="index.html">← back</a> · A data-grounded companion to the <a href="../../../strategy-under-a-force/index.html">Strategy Under a Force</a> series. Research uses the configured model.</footer>
</div></body></html>'''
open(f'{OUT}/patterns.html','w').write(pat)
print(f"built collection '{force_slug}': {len([s for s in specs if writeups.get(s['slug'])])} pages + index + patterns -> {OUT}")
