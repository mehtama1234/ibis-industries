#!/usr/bin/env python3
"""Build a surfaced subtheme index from the force taxonomy."""

from __future__ import annotations

import html
import json
import os
from collections import Counter

from forces_config import FORCES

ROOT = os.path.dirname(os.path.abspath(__file__))
JSON_OUT = os.path.join(ROOT, "subtheme_index.json")
HTML_OUT = os.path.join(ROOT, "subthemes.html")


def e(value):
    return html.escape(str(value or ""), quote=True)


def unique_ordered(values):
    seen = set()
    ordered = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        ordered.append(value)
    return ordered


def trim(items, limit):
    return unique_ordered(items)[:limit]


CSS = """
:root{--bg:#101318;--panel:#171d24;--panel2:#1d2630;--line:#2a3440;--ink:#f0eadc;--muted:#a9b2bd;--faint:#74808d;--gold:#d4ad55;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1180px;margin:0 auto;padding:30px clamp(16px,4vw,40px) 72px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:34px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.2rem,5vw,4rem);line-height:1;margin:.18em 0 .22em}.sub{max-width:860px;color:var(--muted);font-size:1.07rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:24px 0}.lead p{margin:0;color:var(--ink)}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.card h3{margin:.2em 0 .35em;font-size:1.12rem}.card p{color:var(--muted);margin:.35em 0 0}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.4em 0}.count{font-family:var(--mono);font-size:.72rem;color:var(--faint);margin-top:.75em}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.mini{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:12px}.mini h4{margin:0 0 .35em;font-size:.96rem}.mini p{margin:0;color:var(--muted);font-size:.92rem}@media(max-width:920px){.split{grid-template-columns:1fr}}footer{margin-top:44px;padding-top:18px;border-top:1px solid var(--line);color:var(--faint);font-family:var(--mono);font-size:.72rem}
"""


def load_briefs():
    with open(os.path.join(ROOT, "briefs_full.json"), encoding="utf-8") as handle:
        return json.load(handle)


def load_themes():
    with open(os.path.join(ROOT, "american_themes_taxonomy.json"), encoding="utf-8") as handle:
        return json.load(handle)["themes"]


def build_records():
    briefs = load_briefs()
    themes = load_themes()
    brief_lookup = {brief["slug"]: brief for brief in briefs}
    records = []
    for force in FORCES:
        related_themes = [theme for theme in themes if any(item["slug"] == force["slug"] for item in theme["forces"])]
        theme_titles = [theme["title"] for theme in related_themes]
        force_signals = trim((
            signal
            for theme in related_themes
            for signal in theme.get("signals_to_watch", [])
        ), 4)
        force_underwrite = trim((
            line
            for theme in related_themes
            for line in theme.get("capital_implications", [])
        ), 4)
        force_tensions = trim((
            line
            for theme in related_themes
            for line in theme.get("structural_tensions", [])
        ), 3)
        force_second_order = trim((
            line
            for theme in related_themes
            for line in theme.get("second_order_effects", [])
        ), 3)
        group_records = []
        subtheme_count = 0
        for group_label, items in force["groups"].items():
            subthemes = []
            group_evidence_slugs = []
            group_related_theme_subthemes = []
            for subslug, title, evidence_str, angle in items:
                evidence_slugs = [s for s in str(evidence_str).split() if s]
                group_evidence_slugs.extend(evidence_slugs)
                matching_theme_subthemes = []
                for theme in related_themes:
                    for subtheme in theme.get("subthemes", []):
                        industry_slugs = {industry["slug"] for industry in subtheme.get("industries", [])}
                        if industry_slugs.intersection(evidence_slugs):
                            matching_theme_subthemes.append(subtheme)
                            group_related_theme_subthemes.append(subtheme)
                subthemes.append(
                    {
                        "slug": subslug,
                        "title": title,
                        "angle": angle,
                        "evidence_slug_count": len(set(evidence_slugs)),
                        "evidence_slugs": evidence_slugs,
                        "related_theme_subthemes": trim(
                            [subtheme["title"] for subtheme in matching_theme_subthemes],
                            3,
                        ),
                    }
                )
                subtheme_count += 1
            sector_counts = Counter()
            example_industries = []
            for slug in unique_ordered(group_evidence_slugs):
                brief = brief_lookup.get(slug)
                if not brief:
                    continue
                sector_counts[brief["sector"]] += 1
                example_industries.append(brief["title"])
            group_signals = trim((
                signal
                for subtheme in group_related_theme_subthemes
                for signal in subtheme.get("signals_to_watch", [])
            ), 3) or force_signals[:3]
            group_operator = trim((
                line
                for subtheme in group_related_theme_subthemes
                for line in subtheme.get("operator_implications", [])
            ), 3) or trim((
                line
                for theme in related_themes
                for line in theme.get("strategic_implications", [])
            ), 3)
            group_underwrite = trim((
                line
                for subtheme in group_related_theme_subthemes
                for line in subtheme.get("strategic_consequences", [])
            ), 3) or force_underwrite[:3]
            group_companies = trim((
                company["title"]
                for subtheme in group_related_theme_subthemes
                for company in subtheme.get("companies", [])
            ), 4)
            group_records.append(
                {
                    "label": group_label,
                    "subthemes": subthemes,
                    "where_it_shows_up": [sector for sector, _ in sector_counts.most_common(4)],
                    "example_industries": trim(example_industries, 4),
                    "example_companies": group_companies,
                    "signals": group_signals,
                    "what_to_do": group_operator,
                    "what_to_underwrite": group_underwrite,
                }
            )
        records.append(
            {
                "force_slug": force["slug"],
                "force_title": force["title"],
                "lens": force["lens"],
                "signature": force["signature"],
                "subtheme_count": subtheme_count,
                "related_themes": theme_titles,
                "signals": force_signals,
                "structural_tensions": force_tensions,
                "second_order_effects": force_second_order,
                "what_to_underwrite": force_underwrite,
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
                f"<li><b>{e(st['title'])}</b>: {e(st['angle'])} <span class=\"chip\">{st['evidence_slug_count']} evidence industries</span>"
                + (
                    f" <span class=\"chip\">Linked themes: {e(', '.join(st['related_theme_subthemes']))}</span>"
                    if st["related_theme_subthemes"]
                    else ""
                )
                + "</li>"
                for st in group["subthemes"]
            )
            where_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in group["where_it_shows_up"])
            industry_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in group["example_industries"])
            company_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in group["example_companies"])
            signal_items = "".join(f"<li>{e(item)}</li>" for item in group["signals"])
            do_items = "".join(f"<li>{e(item)}</li>" for item in group["what_to_do"])
            underwrite_items = "".join(f"<li>{e(item)}</li>" for item in group["what_to_underwrite"])
            group_blocks.append(
                f"""<div class="card">
  <div class="meta">{e(record['force_title'])}</div>
  <h3>{e(group['label'])}</h3>
  <ul class="list">{items}</ul>
  <div class="meta" style="margin-top:14px">Where it shows up</div>
  <div class="chips">{where_chips}{industry_chips}</div>
  <div class="meta" style="margin-top:14px">Signals</div>
  <ul class="list">{signal_items}</ul>
  <div class="meta" style="margin-top:14px">Representative companies</div>
  <div class="chips">{company_chips}</div>
  <div class="meta" style="margin-top:14px">What to do</div>
  <ul class="list">{do_items}</ul>
  <div class="meta" style="margin-top:14px">What to underwrite</div>
  <ul class="list">{underwrite_items}</ul>
</div>"""
            )
        force_theme_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in record["related_themes"])
        force_signal_items = "".join(f"<li>{e(item)}</li>" for item in record["signals"])
        force_tension_items = "".join(f"<li>{e(item)}</li>" for item in record["structural_tensions"])
        force_second_order = "".join(f"<li>{e(item)}</li>" for item in record["second_order_effects"])
        force_underwrite_items = "".join(f"<li>{e(item)}</li>" for item in record["what_to_underwrite"])
        cards.append(
            f"""<section class="section">
  <div class="card">
    <div class="meta">{e(record['lens'])}</div>
    <h3>{e(record['force_title'])}</h3>
    <p>{e(record['signature'])}</p>
    <div class="count">{record['subtheme_count']} surfaced subthemes</div>
    <div class="chips">{force_theme_chips}</div>
    <div class="split">
      <div class="mini">
        <div class="meta">Signals</div>
        <ul class="list">{force_signal_items}</ul>
      </div>
      <div class="mini">
        <div class="meta">What to underwrite</div>
        <ul class="list">{force_underwrite_items}</ul>
      </div>
    </div>
    <div class="split">
      <div class="mini">
        <div class="meta">Tensions</div>
        <ul class="list">{force_tension_items}</ul>
      </div>
      <div class="mini">
        <div class="meta">Second-order effects</div>
        <ul class="list">{force_second_order}</ul>
      </div>
    </div>
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
<div class="lead"><p>Use this page to move from force headlines into the actual recurring patterns, then into sectors, representative companies, operating signals, and underwriting questions. It is the bridge between abstract force language and concrete market behavior.</p></div>
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
