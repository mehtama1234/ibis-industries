#!/usr/bin/env python3
"""Build a surfaced subtheme index from the force taxonomy."""

from __future__ import annotations

import html
import json
import os

from forces_config import FORCES

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_OUT = os.path.join(ROOT, "subtheme_index.json")
HTML_OUT = os.path.join(ROOT, "subthemes.html")


def e(value):
    return html.escape(str(value or ""), quote=True)


CSS = """
:root{--bg:#101318;--panel:#171d24;--panel2:#1d2630;--line:#2a3440;--ink:#f0eadc;--muted:#a9b2bd;--faint:#74808d;--gold:#d4ad55;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,40px) 72px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:34px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.2rem,5vw,4rem);line-height:1;margin:.18em 0 .22em}.sub{max-width:860px;color:var(--muted);font-size:1.07rem}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.card h3{margin:.2em 0 .35em;font-size:1.12rem}.card p{color:var(--muted);margin:.35em 0 0}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.4em 0}.count{font-family:var(--mono);font-size:.72rem;color:var(--faint);margin-top:.75em}footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);color:var(--faint);font-family:var(--mono);font-size:.72rem}
"""


def build_records():
    records = []
    for force in FORCES:
        group_records = []
        subtheme_count = 0
        for group_label, items in force["groups"].items():
            subthemes = []
            for subslug, title, evidence_str, angle in items:
                evidence_slugs = [s for s in str(evidence_str).split() if s]
                subthemes.append(
                    {
                        "slug": subslug,
                        "title": title,
                        "angle": angle,
                        "evidence_slug_count": len(set(evidence_slugs)),
                        "evidence_slugs": evidence_slugs,
                    }
                )
                subtheme_count += 1
            group_records.append(
                {
                    "label": group_label,
                    "subthemes": subthemes,
                }
            )
        records.append(
            {
                "force_slug": force["slug"],
                "force_title": force["title"],
                "lens": force["lens"],
                "signature": force["signature"],
                "subtheme_count": subtheme_count,
                "groups": group_records,
            }
        )
    return records


def build_html(records):
    cards = []
    for record in records:
        group_blocks = []
        for group in record["groups"]:
            items = "".join(
                f"<li><b>{e(st['title'])}</b>: {e(st['angle'])} <span class=\"chip\">{st['evidence_slug_count']} evidence industries</span></li>"
                for st in group["subthemes"]
            )
            group_blocks.append(
                f"""<div class="card">
  <div class="meta">{e(record['force_title'])}</div>
  <h3>{e(group['label'])}</h3>
  <ul class="list">{items}</ul>
</div>"""
            )
        cards.append(
            f"""<section class="section">
  <div class="card">
    <div class="meta">{e(record['lens'])}</div>
    <h3>{e(record['force_title'])}</h3>
    <p>{e(record['signature'])}</p>
    <div class="count">{record['subtheme_count']} surfaced subthemes</div>
  </div>
  <div class="grid">{''.join(group_blocks)}</div>
</section>"""
        )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Subthemes — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="forces/index.html">Forces</a><a href="force-operator-translations.html">Force-to-operator</a></div>
<div class="eyebrow">Subthemes · US · 2025–2026</div>
<h1>Subthemes</h1>
<p class="sub">This is the fine-grained layer inside the force map. Each major force breaks into subthemes with explicit angles and evidence-industry footprints, so the interpretation layer is not stuck at only macro headline level.</p>
{''.join(cards)}
<footer>Built from the force taxonomy. Use this page to move from top-level forces into the specific recurring patterns underneath them.</footer>
</div></body></html>"""


def main():
    records = build_records()
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)
    with open(HTML_OUT, "w", encoding="utf-8") as f:
        f.write(build_html(records))
    print(f"wrote {JSON_OUT}")
    print(f"wrote {HTML_OUT}")
    print(f"forces={len(records)}")


if __name__ == "__main__":
    main()
