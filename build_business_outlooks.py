#!/usr/bin/env python3
"""Build business-type outlooks through societal, cultural, consumer, and industrial lenses."""

from __future__ import annotations

import html
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BUSINESS_LENSES_JSON = ROOT / "business_lenses.json"
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
JSON_OUT = ROOT / "business_outlooks.json"
OUT = ROOT / "business-outlooks.html"
PAGES_OUT = ROOT / "business-outlooks"


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.6}.wrap{max-width:1220px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.45rem,5vw,4.2rem);line-height:1;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.45rem;margin:0 0 .45em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:26px 0}.lead p{margin:0;font-size:1.05rem}.kpis{display:flex;flex-wrap:wrap;gap:10px;margin-top:18px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:132px}.kpi .n{font-family:var(--mono);font-size:1.32rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.panel,.lens{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.card h3,.panel h3,.lens h3{margin:.2em 0 .35em;font-size:1.12rem}.card p,.panel p,.lens p{color:var(--muted);margin:.35em 0 0}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.outlook{margin-top:18px;padding-top:18px;border-top:1px solid var(--line)}.outlook:first-of-type{margin-top:0;padding-top:0;border-top:none}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


LENS_BUCKETS = {
    "societal": "Societal",
    "cultural": "Cultural",
    "consumer": "Consumer",
    "industrial": "Industrial",
}


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


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


def load_business_lenses() -> list[dict]:
    with BUSINESS_LENSES_JSON.open(encoding="utf-8") as handle:
        return json.load(handle)


def load_theme_records() -> list[dict]:
    with THEMES_JSON.open(encoding="utf-8") as handle:
        return json.load(handle)["themes"]


def build_force_theme_map(theme_records: list[dict]) -> dict[str, list[dict]]:
    mapping: dict[str, list[dict]] = defaultdict(list)
    for theme in theme_records:
        for force in theme.get("forces", []):
            mapping[force["slug"]].append(theme)
    return mapping


def dedupe_themes(themes: list[dict]) -> list[dict]:
    out = []
    seen = set()
    for theme in themes:
        if theme["slug"] in seen:
            continue
        seen.add(theme["slug"])
        out.append(theme)
    return out


def collect_relevant_themes(record: dict, force_theme_map: dict[str, list[dict]]) -> list[dict]:
    themes = []
    for force in record.get("linked_forces", []):
        themes.extend(force_theme_map.get(force["slug"], []))
    themes = dedupe_themes(themes)
    scored = []
    record_forces = {force["slug"] for force in record.get("linked_forces", [])}
    record_theme_terms = {item.lower() for item in record.get("themes", [])}
    record_sectors = {item.lower() for item in record.get("sectors", [])}
    for theme in themes:
        overlap = len(record_forces & {force["slug"] for force in theme.get("forces", [])})
        subtheme_hits = sum(
            1
            for subtheme in theme.get("subthemes", [])
            if any(term and term in subtheme["title"].lower() for term in record_theme_terms)
        )
        sector_hits = sum(
            1
            for subtheme in theme.get("subthemes", [])
            for industry in subtheme.get("industries", [])
            if industry.get("sector", "").lower() in record_sectors
        )
        scored.append((overlap, subtheme_hits, sector_hits, theme))
    scored.sort(key=lambda item: (item[0], item[1], item[2], item[3]["signal_count"]), reverse=True)
    return [item[3] for item in scored[:5]]


def build_lens_summary(record: dict, bucket: str, themes: list[dict]) -> str:
    theme_names = ", ".join(theme["title"] for theme in themes[:3])
    title = record["title"]
    if bucket == "societal":
        return f"{title} is being shaped socially by {theme_names}, where labor coordination, family burden, staffing reality, and managed systems change how the model actually scales."
    if bucket == "cultural":
        return f"{title} also sits inside a cultural reclassification through {theme_names}, where legitimacy, participation, wellness, and identity affect willingness to engage and pay."
    if bucket == "consumer":
        return f"{title} faces sharper consumer selection through {theme_names}, where buyers are more explicit about value, convenience, health, and permission to spend."
    return f"{title} is being repriced industrially through {theme_names}, where bottlenecks, compliance, infrastructure, procurement, and system ownership increasingly govern the margin pool."


def build_lens_cards(record: dict, themes: list[dict]) -> list[dict]:
    bucket_map: dict[str, dict] = {}
    for key, label in LENS_BUCKETS.items():
        bucket_map[key] = {
            "key": key,
            "label": label,
            "themes": [],
            "theme_titles": [],
            "tensions": [],
            "signals": [],
            "second_order": [],
            "subthemes": [],
        }

    for theme in themes:
        for bucket in classify_theme_lens(theme.get("lens", "")):
            bucket_map[bucket]["themes"].append(theme)
            bucket_map[bucket]["theme_titles"].append(theme["title"])
            for item in theme.get("structural_tensions", [])[:2]:
                if item not in bucket_map[bucket]["tensions"]:
                    bucket_map[bucket]["tensions"].append(item)
            for item in theme.get("signals_to_watch", [])[:2]:
                if item not in bucket_map[bucket]["signals"]:
                    bucket_map[bucket]["signals"].append(item)
            for item in theme.get("second_order_effects", [])[:2]:
                if item not in bucket_map[bucket]["second_order"]:
                    bucket_map[bucket]["second_order"].append(item)
            for subtheme in theme.get("subthemes", [])[:2]:
                if not any(existing["slug"] == subtheme["slug"] for existing in bucket_map[bucket]["subthemes"]):
                    bucket_map[bucket]["subthemes"].append(
                        {
                            "slug": subtheme["slug"],
                            "title": subtheme["title"],
                            "theme_slug": theme["slug"],
                            "theme_title": theme["title"],
                        }
                    )

    cards = []
    for key in ("societal", "cultural", "consumer", "industrial"):
        bucket = bucket_map[key]
        if not bucket["themes"]:
            continue
        bucket["summary"] = build_lens_summary(record, key, bucket["themes"])
        cards.append(bucket)
    return cards


def build_business_outlook_records() -> list[dict]:
    business_lenses = load_business_lenses()
    theme_records = load_theme_records()
    force_theme_map = build_force_theme_map(theme_records)
    out = []

    for record in business_lenses:
        themes = collect_relevant_themes(record, force_theme_map)
        lens_cards = build_lens_cards(record, themes)
        out.append(
            {
                **record,
                "dominant_theme_objects": themes,
                "lens_cards": lens_cards,
                "lens_count": len(lens_cards),
                "outlook_thesis": (
                    f"{record['title']} should be read less as a static category and more as a reusable operating model whose economics now depend on how societal, cultural, consumer, and industrial pressures stack together."
                ),
                "operator_angle": (
                    f"The operating question is not just how to grow {record['title'].lower()}, but which constraint actually governs it: labor, reimbursement, utilization, procurement, compliance, demand capture, or infrastructure access."
                ),
                "investor_angle": (
                    f"The investor question is which version of {record['title'].lower()} owns the bottleneck, routinizes the complexity, and keeps the new behavior legible enough to hold pricing and throughput."
                ),
            }
        )
    return out


def render_subtheme_chip(prefix: str, subtheme: dict) -> str:
    return f'<a class="chip" href="{e(prefix)}themes/{e(subtheme["theme_slug"])}.html#{e(subtheme["slug"])}">{e(subtheme["title"])}</a>'


def render_lens(lens: dict, prefix: str = "", seen: set | None = None) -> str:
    seen = seen if seen is not None else set()

    def dd(items: list, limit: int) -> str:
        out = []
        for item in items:
            if item in seen:
                continue
            seen.add(item)
            out.append(item)
            if len(out) >= limit:
                break
        return "".join(f"<li>{e(x)}</li>" for x in out)

    theme_chips = "".join(f'<span class="chip">{e(title)}</span>' for title in lens["theme_titles"][:4])
    tensions = dd(lens["tensions"], 3)
    signals = dd(lens["signals"], 3)
    second_order = dd(lens["second_order"], 3)
    subthemes = "".join(render_subtheme_chip(prefix, item) for item in lens["subthemes"][:5]) or '<span class="chip">no surfaced subthemes</span>'
    return f"""<article class="lens">
  <div class="meta">{e(lens['label'])} lens</div>
  <h3>{e(lens['label'])} Read</h3>
  <p>{e(lens['summary'])}</p>
  <div class="chips">{theme_chips}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">Tensions</div>
      <ul class="list">{tensions}</ul>
    </div>
    <div class="panel">
      <div class="meta">Signals</div>
      <ul class="list">{signals}</ul>
    </div>
  </div>
  <div class="panel" style="margin-top:14px">
    <div class="meta">Second-order effects</div>
    <ul class="list">{second_order}</ul>
  </div>
  <div class="panel" style="margin-top:14px">
    <div class="meta">Linked subthemes</div>
    <div class="chips">{subthemes}</div>
  </div>
</article>"""


def render_record(record: dict, prefix: str = "") -> str:
    _lens_seen: set = set()
    lenses = "".join(render_lens(lens, prefix=prefix, seen=_lens_seen) for lens in record["lens_cards"])
    forces = "".join(f'<span class="chip">{e(force["title"])}</span>' for force in record.get("linked_forces", [])[:4])
    constraints = "".join(f'<span class="chip">{e(item)}</span>' for item in record.get("binding_constraints", [])[:4])
    sectors = "".join(f'<span class="chip">{e(item)}</span>' for item in record.get("sectors", [])[:4])
    return f"""<section class="outlook">
  <div class="meta">{e(record['economic_role'])} outlook</div>
  <h3>{e(record['title'])}</h3>
  <p>{e(record['outlook_thesis'])}</p>
  <div class="chips"><span class="chip">{e(record['demand_type'])}</span><span class="chip">{e(record['best_owner_type'])}</span></div>
  <div class="meta" style="margin-top:14px">Where it shows up</div>
  <div class="chips">{sectors}</div>
  <div class="meta" style="margin-top:14px">Signals</div>
  <div class="chips">{forces}{constraints}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">What to do</div>
      <p>{e(record['operator_angle'])}</p>
    </div>
    <div class="panel">
      <div class="meta">What to underwrite</div>
      <p>{e(record['investor_angle'])}</p>
    </div>
  </div>
  <div class="panel" style="margin-top:14px">
    <div class="meta">Second-order effects</div>
    <ul class="list">{''.join(f'<li>{e(item)}</li>' for lens in record['lens_cards'] for item in lens['second_order'][:1])}</ul>
  </div>
  <div class="grid" style="margin-top:14px">{lenses}</div>
</section>"""


def build_hub(records: list[dict]) -> str:
    cards = "\n".join(
        f"""<article class="card">
  <div class="meta">{e(record['economic_role'])}</div>
  <h3><a href="business-outlooks/{e(record['slug'])}.html">{e(record['title'])}</a></h3>
  <p>{e(record['outlook_thesis'])}</p>
  <div class="meta" style="margin-top:14px">Where it shows up</div>
  <div class="chips">{''.join(f'<span class="chip">{e(item)}</span>' for item in record['sectors'][:4])}</div>
  <div class="meta" style="margin-top:14px">Signals</div>
  <div class="chips">{''.join(f'<span class="chip">{e(lens["label"])}</span>' for lens in record['lens_cards'])}</div>
  <div class="meta" style="margin-top:14px">What to do</div>
  <p>{e(record['operator_angle'])}</p>
  <div class="meta" style="margin-top:14px">What to underwrite</div>
  <p>{e(record['investor_angle'])}</p>
  <div class="meta" style="margin-top:14px">Second-order effects</div>
  <ul class="list">{''.join(f'<li>{e(item)}</li>' for lens in record['lens_cards'][:2] for item in lens['second_order'][:1])}</ul>
</article>"""
        for record in records
    )
    sections = "".join(render_record(record) for record in records)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Business Outlooks — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="business-lenses.html">Business lenses</a><a href="american-outlook-2025-2026.html">American outlook</a></div>
<div class="eyebrow">Business outlooks · US · 2025-2026</div>
<h1>Business Outlooks</h1>
<p class="sub">This layer re-reads recurring business archetypes through the same four top-level lenses used in the American outlook: societal, cultural, consumer, and industrial change.</p>
<div class="kpis">
  <div class="kpi"><div class="n">{len(records)}</div><div class="l">Business archetypes</div></div>
  <div class="kpi"><div class="n">{sum(record['lens_count'] for record in records)}</div><div class="l">Lens reads</div></div>
  <div class="kpi"><div class="n">{sum(len(record['dominant_theme_objects']) for record in records)}</div><div class="l">Mapped themes</div></div>
</div>
<div class="lead"><p>The point here is to show what kind of broader American change is actually doing the work inside recurring business models. A local services platform, a regulated workflow rail, or a specified manufacturer each faces a different stack of social, cultural, consumer, and industrial pressures.</p></div>

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
<title>{e(record['title'])} Outlook — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../business-outlooks.html">Business outlooks</a><a href="../business-lenses.html">Business lenses</a></div>
<div class="eyebrow">{e(record['title'])} outlook · US · 2025-2026</div>
<h1>{e(record['title'])}</h1>
<p class="sub">{e(record['outlook_thesis'])}</p>
<div class="kpis">
  <div class="kpi"><div class="n">{record['lens_count']}</div><div class="l">Lens reads</div></div>
  <div class="kpi"><div class="n">{len(record['dominant_theme_objects'])}</div><div class="l">Mapped themes</div></div>
  <div class="kpi"><div class="n">{len(record.get('binding_constraints', []))}</div><div class="l">Core constraints</div></div>
</div>
<div class="lead"><p>{e(record['operator_angle'])}</p></div>
<section class="section">
  {render_record(record, prefix="../")}
</section>
</div></body></html>"""


def main() -> None:
    records = build_business_outlook_records()
    records.sort(key=lambda item: item["title"])
    PAGES_OUT.mkdir(exist_ok=True)
    with JSON_OUT.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)
    with OUT.open("w", encoding="utf-8") as handle:
        handle.write(build_hub(records))
    for record in records:
        with (PAGES_OUT / f"{record['slug']}.html").open("w", encoding="utf-8") as handle:
            handle.write(build_detail(record))
    print(f"wrote {JSON_OUT}")
    print(f"wrote {OUT}")
    print(f"wrote business outlooks to {PAGES_OUT}")
    print(f"records={len(records)}")


if __name__ == "__main__":
    main()
