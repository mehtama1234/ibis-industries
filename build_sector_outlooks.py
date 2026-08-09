#!/usr/bin/env python3
"""Build sector outlooks through societal, cultural, consumer, and industrial lenses."""

from __future__ import annotations

import html
from collections import Counter
from pathlib import Path

from build_sector_memos import build_sector_records

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "sector-outlooks.html"
PAGES_OUT = ROOT / "sector-outlooks"


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1220px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.45rem,5vw,4.2rem);line-height:1;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel,.lens,.brief{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3,.panel h3,.lens h3,.brief h3{margin:.2em 0 .35em;font-size:1.12rem}.card p,.panel p,.lens p,.brief p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.outlook{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.outlook:first-of-type{margin-top:0;padding-top:0;border-top:none}.smallgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:12px;margin-top:14px}.mini{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:12px}.mini h4{margin:0 0 .35em;font-size:.96rem}.mini p{margin:0;color:var(--muted);font-size:.9rem}.badge{display:inline-block;margin-top:8px;font-family:var(--mono);font-size:.66rem;border:1px solid var(--line);border-radius:999px;padding:3px 8px;color:var(--muted)}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


LENS_BUCKETS = {
    "societal": "Societal",
    "cultural": "Cultural",
    "consumer": "Consumer",
    "industrial": "Industrial",
}


def classify_theme_lens(lens: str) -> list[str]:
    text = (lens or "").lower()
    buckets = []
    if "societal" in text or "social" in text or "institutional" in text:
        buckets.append("societal")
    if "cultural" in text:
        buckets.append("cultural")
    if "consumer" in text:
        buckets.append("consumer")
    if "industrial" in text or "technological" in text:
        buckets.append("industrial")
    return buckets or ["industrial"]


def build_lens_summary(sector: str, bucket: str, themes: list[dict]) -> str:
    theme_names = ", ".join(theme["title"] for theme in themes[:3])
    if bucket == "societal":
        return f"{sector} is being pushed by broader social and institutional strain through {theme_names}, where labor availability, coordination burden, and managed systems increasingly shape the market."
    if bucket == "cultural":
        return f"{sector} is also being reclassified culturally through {theme_names}, where identity, wellness, participation, and legitimacy affect demand more directly than older category assumptions did."
    if bucket == "consumer":
        return f"{sector} faces sharper consumer selection through {theme_names}, where buyers are more explicit about value, convenience, health, and permission to spend."
    return f"{sector} sits inside a harder industrial environment through {theme_names}, where bottlenecks, system ownership, compliance, and infrastructure constraints matter more than broad end-market optimism."


def build_sector_outlook_records() -> list[dict]:
    records = build_sector_records()
    for record in records:
        bucket_map: dict[str, dict] = {}
        for key, label in LENS_BUCKETS.items():
            bucket_map[key] = {
                "key": key,
                "label": label,
                "themes": [],
                "theme_titles": [],
                "tensions": [],
                "signals": [],
                "subthemes": [],
                "operator_implications": [],
                "capital_implications": [],
            }

        for theme in record["dominant_theme_objects"]:
            for bucket in classify_theme_lens(theme.get("lens", "")):
                bucket_map[bucket]["themes"].append(theme)
                bucket_map[bucket]["theme_titles"].append(theme["title"])
                for item in theme.get("structural_tensions", [])[:2]:
                    if item not in bucket_map[bucket]["tensions"]:
                        bucket_map[bucket]["tensions"].append(item)
                for item in theme.get("signals_to_watch", [])[:2]:
                    if item not in bucket_map[bucket]["signals"]:
                        bucket_map[bucket]["signals"].append(item)
                for item in theme.get("strategic_implications", [])[:3]:
                    if item not in bucket_map[bucket]["operator_implications"]:
                        bucket_map[bucket]["operator_implications"].append(item)
                for item in theme.get("capital_implications", [])[:3]:
                    if item not in bucket_map[bucket]["capital_implications"]:
                        bucket_map[bucket]["capital_implications"].append(item)

        seen = {key: set() for key in LENS_BUCKETS}
        for subtheme in record["subtheme_map"]:
            for bucket in classify_theme_lens(subtheme["theme_title"]):
                pass
        theme_bucket_lookup = {}
        for bucket, data in bucket_map.items():
            for title in data["theme_titles"]:
                theme_bucket_lookup.setdefault(title, []).append(bucket)
        for subtheme in record["subtheme_map"]:
            for bucket in theme_bucket_lookup.get(subtheme["theme_title"], []):
                if subtheme["title"] not in seen[bucket]:
                    seen[bucket].add(subtheme["title"])
                    bucket_map[bucket]["subthemes"].append(subtheme)

        lens_cards = []
        lens_count = 0
        for key in ("societal", "cultural", "consumer", "industrial"):
            bucket = bucket_map[key]
            if not bucket["themes"] and not bucket["subthemes"]:
                continue
            lens_count += 1
            bucket["summary"] = build_lens_summary(record["sector"], key, bucket["themes"] or record["dominant_theme_objects"])
            lens_cards.append(bucket)
        record["lens_cards"] = lens_cards
        record["lens_count"] = lens_count
    return records


def render_subtheme_chip(prefix: str, subtheme: dict) -> str:
    return f'<a class="chip" href="{e(prefix)}themes/{e(subtheme["theme_slug"])}.html#{e(subtheme["slug"])}">{e(subtheme["title"])}</a>'


def company_chip(company: dict, prefix: str = "") -> str:
    return f'<a class="chip" href="{e(prefix)}company-pages/{e(company["slug"])}.html">{e(company["title"])}</a>'


def brief_card(brief: dict) -> str:
    return f"""<article class="brief">
  <div class="meta">{e(brief.get('sector'))}</div>
  <h3>{e(brief.get('title'))}</h3>
  <p>{e(brief.get('one_sentence') or brief.get('one_liner'))}</p>
</article>"""


def render_lens(lens: dict, prefix: str = "") -> str:
    theme_chips = "".join(f'<span class="chip">{e(title)}</span>' for title in lens["theme_titles"][:4])
    tension_items = "".join(f"<li>{e(item)}</li>" for item in lens["tensions"][:3])
    signal_items = "".join(f"<li>{e(item)}</li>" for item in lens["signals"][:3])
    operator_items = "".join(f"<li>{e(item)}</li>" for item in lens["operator_implications"][:3])
    capital_items = "".join(f"<li>{e(item)}</li>" for item in lens["capital_implications"][:3])
    subtheme_chips = "".join(render_subtheme_chip(prefix, item) for item in lens["subthemes"][:5]) or '<span class="chip">no surfaced subthemes</span>'
    return f"""<article class="lens">
  <div class="meta">{e(lens['label'])} lens</div>
  <h3>{e(lens['label'])} Read</h3>
  <p>{e(lens['summary'])}</p>
  <div class="chips">{theme_chips}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">Core tensions</div>
      <ul class="list">{tension_items}</ul>
    </div>
    <div class="panel">
      <div class="meta">Signals</div>
      <ul class="list">{signal_items}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Operator implications</div>
      <ul class="list">{operator_items}</ul>
    </div>
    <div class="panel">
      <div class="meta">Investor implications</div>
      <ul class="list">{capital_items}</ul>
    </div>
  </div>
  <div class="panel" style="margin-top:14px">
    <div class="meta">Linked subthemes</div>
    <div class="chips">{subtheme_chips}</div>
  </div>
</article>"""


def render_sector(record: dict, prefix: str = "") -> str:
    lenses = "".join(render_lens(lens, prefix=prefix) for lens in record["lens_cards"])
    industry_cards = "".join(brief_card(item) for item in record["example_industries"][:4])
    company_chips = "".join(
        company_chip(item, prefix=prefix) for item in (record["advantaged"][:2] + record["mixed"][:2] + record["exposed"][:2])
    ) or '<span class="chip">none surfaced</span>'
    return f"""<section class="outlook">
  <div class="meta">{e(record['sector'])} outlook</div>
  <h3>{e(record['sector'])}</h3>
  <p>{e(record['sector_thesis'])}</p>
  <div class="chips"><span class="chip">{e(record['operator_angle'])}</span><span class="chip">{e(record['investor_angle'])}</span></div>
  <div class="split">
    <div class="panel">
      <div class="meta">Where it shows up</div>
      <h3>Representative industries</h3>
      <div class="grid">{industry_cards}</div>
    </div>
    <div class="panel">
      <div class="meta">Representative companies</div>
      <h3>Named evidence</h3>
      <div class="chips">{company_chips}</div>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">What to do</div>
      <ul class="list"><li>{e(record['operator_angle'])}</li></ul>
    </div>
    <div class="panel">
      <div class="meta">What to underwrite</div>
      <ul class="list"><li>{e(record['investor_angle'])}</li></ul>
    </div>
  </div>
  <div class="grid" style="margin-top:14px">{lenses}</div>
</section>"""


def build_hub(records: list[dict]) -> str:
    cards = "\n".join(
        f"""<article class="card">
  <div class="meta">{e(record['sector'])}</div>
  <h3><a href="sector-outlooks/{e(record['slug'])}.html">{e(record['sector'])}</a></h3>
  <p>{e(record['sector_thesis'])}</p>
  <div class="chips">{''.join(f'<span class="chip">{e(lens["label"])}</span>' for lens in record['lens_cards'])}</div>
</article>"""
        for record in records
    )
    sections = "".join(render_sector(record) for record in records)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sector Outlooks — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="sector-memos.html">Sector memos</a><a href="american-outlook-2025-2026.html">American outlook</a></div>
<div class="eyebrow">Sector outlooks · US · 2025-2026</div>
<h1>Sector Outlooks</h1>
<p class="sub">This layer re-reads the major sectors through the same four top-level lenses used in the American outlook: societal, cultural, consumer, and industrial change.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(records)}</div><div class="l">Major sectors</div></div>
  <div class="kpi"><div class="n">{sum(record['lens_count'] for record in records)}</div><div class="l">Lens reads</div></div>
  <div class="kpi"><div class="n">{sum(len(record['subtheme_map']) for record in records)}</div><div class="l">Mapped subthemes</div></div>
</div>
<div class="lead"><p>The point here is not to repeat the sector memo. It is to show which part of the broader American story is actually doing the work inside each sector, and how those lenses stack together.</p></div>

<section class="section">
  <h2>Index</h2>
  <div class="grid">{cards}</div>
</section>

<section class="section">
  <h2>The Outlooks</h2>
  {sections}
</section>

</div></body></html>"""


def build_detail(record: dict) -> str:
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(record['sector'])} Outlook — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../sector-outlooks.html">Sector outlooks</a><a href="../sector-memos.html">Sector memos</a></div>
<div class="eyebrow">{e(record['sector'])} outlook · US · 2025-2026</div>
<h1>{e(record['sector'])}</h1>
<p class="sub">{e(record['sector_thesis'])}</p>
<div class="kpis">
  <div class="kpi"><div class="n">{record['industry_count']}</div><div class="l">Industries</div></div>
  <div class="kpi"><div class="n">{record['lens_count']}</div><div class="l">Lens reads</div></div>
  <div class="kpi"><div class="n">{len(record['subtheme_map'])}</div><div class="l">Mapped subthemes</div></div>
</div>
<div class="lead"><p>{e(record['operator_angle'])}</p></div>
<section class="section">
  {render_sector(record, prefix="../")}
</section>
</div></body></html>"""


def main() -> None:
    records = build_sector_outlook_records()
    records.sort(key=lambda item: item["sector"])
    PAGES_OUT.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(build_hub(records))
    for record in records:
        with (PAGES_OUT / f"{record['slug']}.html").open("w", encoding="utf-8") as handle:
            handle.write(build_detail(record))
    print(f"wrote {OUT}")
    print(f"wrote sector outlooks to {PAGES_OUT}")
    print(f"sectors={len(records)}")


if __name__ == "__main__":
    main()
