#!/usr/bin/env python3
"""Build operator/sector-area playbooks from researched industry briefs."""

from __future__ import annotations

import html
import json
import os
from collections import Counter

from operator_playbooks_config import PLAYBOOKS

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, "operators")


def e(value):
    return html.escape(str(value or ""), quote=True)


def stat(b, key):
    return (b.get("key_stats") or {}).get(key) or "n/a"


def brief_card(b):
    themes = " ".join(f"<span>{e(t)}</span>" for t in (b.get("themes") or [])[:4])
    return f"""<article class="brief">
  <div class="meta">{e(b.get('sector'))}</div>
  <h3>{e(b.get('title'))}</h3>
  <p>{e(b.get('one_sentence') or b.get('one_liner'))}</p>
  <div class="stats">
    <b>{e(stat(b, 'market_size'))}</b>
    <span>{e(stat(b, 'growth'))}</span>
    <span>{e(stat(b, 'profit_margin'))}</span>
  </div>
  <div class="themes">{themes}</div>
</article>"""


def playbook_record(pb, briefs_by_slug):
    briefs = [briefs_by_slug[s] for s in pb["slugs"] if s in briefs_by_slug]
    sectors = Counter(b.get("sector", "Unknown") for b in briefs)
    themes = Counter(t for b in briefs for t in (b.get("themes") or []))
    developments = []
    for b in briefs:
        for d in (b.get("recent_developments") or [])[:2]:
            developments.append({"industry": b["title"], "development": d})
    return {
        **pb,
        "industries": [
            {
                "slug": b["slug"],
                "title": b["title"],
                "sector": b.get("sector"),
                "one_sentence": b.get("one_sentence") or b.get("one_liner"),
                "market_size": stat(b, "market_size"),
                "growth": stat(b, "growth"),
                "profit_margin": stat(b, "profit_margin"),
                "themes": (b.get("themes") or [])[:6],
            }
            for b in briefs
        ],
        "sector_mix": sectors.most_common(),
        "common_themes": themes.most_common(10),
        "recent_developments": developments[:12],
    }


CSS = """
:root{--bg:#101318;--panel:#171d24;--panel2:#1d2630;--line:#2a3440;--ink:#f0eadc;--muted:#a9b2bd;--faint:#74808d;--gold:#d4ad55;--green:#71c58b;--red:#df806e;--blue:#77a7dc;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1180px;margin:0 auto;padding:28px clamp(16px,4vw,40px) 70px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;font-family:var(--mono);font-size:.78rem;margin-bottom:36px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.2rem,5vw,4rem);line-height:1;margin:.2em 0 .25em}h2{font-size:1.55rem;margin:1.6em 0 .55em}.sub{max-width:760px;color:var(--muted);font-size:1.08rem}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(290px,1fr));gap:14px;margin-top:28px}.card,.brief,.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card:hover{background:var(--panel2)}.card h2{margin:0 0 .35em;font-size:1.22rem}.lens,.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.card p,.brief p{color:var(--muted);margin:.55em 0}.count{font-family:var(--mono);font-size:.72rem;color:var(--faint)}.split{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(280px,.8fr);gap:18px;margin-top:28px}@media(max-width:820px){.split{grid-template-columns:1fr}}.brief{margin-bottom:12px}.brief h3{margin:.2em 0;font-size:1.08rem}.stats{display:flex;flex-wrap:wrap;gap:8px;margin:.75em 0;font-family:var(--mono);font-size:.76rem}.stats>*{background:var(--panel2);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.themes{display:flex;flex-wrap:wrap;gap:6px}.themes span,.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:3px 8px}.qs{padding-left:18px;color:var(--muted)}.qs li{margin:.45em 0}.dev{border-left:2px solid var(--gold);padding-left:12px;margin:.8em 0;color:var(--muted)}footer{margin-top:48px;color:var(--faint);font-family:var(--mono);font-size:.72rem;border-top:1px solid var(--line);padding-top:18px}
"""


def build_page(record, briefs_by_slug):
    briefs = [briefs_by_slug[s] for s in record["slugs"] if s in briefs_by_slug]
    sector_mix = "".join(f'<span class="chip">{e(sec)}: {n}</span>' for sec, n in record["sector_mix"])
    common = "".join(f'<span class="chip">{e(t)}: {n}</span>' for t, n in record["common_themes"][:8])
    questions = "".join(f"<li>{e(q)}</li>" for q in record["operator_questions"])
    devs = "".join(
        f'<div class="dev"><b>{e(d["industry"])}</b><br>{e(d["development"])}</div>'
        for d in record["recent_developments"][:8]
    )
    cards = "\n".join(brief_card(b) for b in briefs)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(record['title'])} — Operator Playbooks</title><link rel="stylesheet" href="../operators.css"></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../operators.html">Operator playbooks</a><a href="../forces/index.html">Forces</a></div>
<div class="eyebrow">{e(record['lens'])}</div><h1>{e(record['title'])}</h1>
<p class="sub">{e(record['thesis'])}</p>
<div class="split"><main>
<h2>Evidence Industries</h2>{cards}
</main><aside>
<div class="panel"><h2>How To Read It</h2><ul class="qs">{questions}</ul></div>
<div class="panel"><h2>Sector Mix</h2><div class="themes">{sector_mix}</div></div>
<div class="panel"><h2>Repeated Themes</h2><div class="themes">{common}</div></div>
<div class="panel"><h2>Recent Signals</h2>{devs}</div>
</aside></div>
<footer>Built from the current researched industry corpus. Each playbook is a sector-area/operator view over specific industry briefs.</footer>
</div></body></html>"""


def build_hub(records, industry_count):
    cards = "\n".join(
        f"""<a class="card" href="operators/{e(r['slug'])}.html">
  <div class="lens">{e(r['lens'])}</div><h2>{e(r['title'])}</h2>
  <p>{e(r['thesis'])}</p><div class="count">{len(r['industries'])} evidence industries</div>
</a>"""
        for r in records
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Operator Playbooks — US Industry Briefs</title><link rel="stylesheet" href="operators.css"></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="forces/index.html">Forces</a></div>
<div class="eyebrow">Business archetypes from the data</div><h1>Operator Playbooks</h1>
<p class="sub">The industry briefs show what is happening inside each market. These playbooks group those markets into business types: local services, specialty manufacturing, regulated admin, healthcare delivery, experience venues, food niches, and distributors. Built from {industry_count} researched industries.</p>
<div class="grid">{cards}</div>
<footer>Use these as operator lenses: what makes the business work, what pressures margins, and which forces matter.</footer>
</div></body></html>"""


def main():
    briefs = json.load(open(os.path.join(ROOT, "briefs_full.json")))
    briefs_by_slug = {b["slug"]: b for b in briefs}
    os.makedirs(OUT, exist_ok=True)
    records = [playbook_record(pb, briefs_by_slug) for pb in PLAYBOOKS]
    json.dump(records, open(os.path.join(ROOT, "operator_playbooks.json"), "w"), ensure_ascii=False, indent=2)
    open(os.path.join(ROOT, "operators.css"), "w").write(CSS)
    for r in records:
        open(os.path.join(OUT, f"{r['slug']}.html"), "w").write(build_page(r, briefs_by_slug))
    open(os.path.join(ROOT, "operators.html"), "w").write(build_hub(records, len(briefs)))
    print(f"built {len(records)} operator playbooks from {len(briefs)} industries")


if __name__ == "__main__":
    main()
