#!/usr/bin/env python3
"""Build structured export files for the American synthesis stack."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
RANKINGS_JSON = ROOT / "american_rankings.json"
COMPANY_MEMOS_JSON = ROOT / "company_memos.json"

OUT_THEME_RANKINGS = ROOT / "american_theme_rankings.json"
OUT_SUBTHEME_RANKINGS = ROOT / "american_subtheme_rankings.json"
OUT_BOTTLENECKS = ROOT / "american_bottlenecks.json"
OUT_EXPOSED = ROOT / "american_exposed_models.json"
OUT_THEME_SECTORS = ROOT / "american_theme_sector_links.json"
OUT_THEME_COMPANIES = ROOT / "american_theme_company_links.json"


def load_json(path: Path):
    return json.loads(path.read_text())


def main() -> None:
    rankings = load_json(RANKINGS_JSON)
    themes = load_json(THEMES_JSON)["themes"]
    company_memos = {row["slug"]: row for row in load_json(COMPANY_MEMOS_JSON)}

    theme_rows = rankings["top_themes"]
    subtheme_rows = rankings["top_subthemes"]
    bottlenecks = rankings["top_bottlenecks"]
    exposed_models = rankings["top_exposed_models"]

    theme_sector_links = []
    theme_company_links = []
    for theme in themes:
        sector_map = {}
        company_map = {}
        for subtheme in theme["subthemes"]:
            for industry in subtheme.get("industries", []):
                sector = industry.get("sector")
                if not sector:
                    continue
                bucket = sector_map.setdefault(sector, {"sector": sector, "industries": [], "subthemes": set()})
                bucket["industries"].append({
                    "slug": industry.get("slug"),
                    "title": industry.get("title"),
                    "one_sentence": industry.get("one_sentence"),
                })
                bucket["subthemes"].add(subtheme["title"])
            for company in subtheme.get("companies", []):
                slug = company.get("slug")
                if not slug:
                    continue
                memo = company_memos.get(slug, {})
                bucket = company_map.setdefault(slug, {
                    "slug": slug,
                    "title": company.get("title"),
                    "sector": memo.get("top_sector", company.get("sector")),
                    "status": company.get("status"),
                    "cluster": company.get("cluster"),
                    "subthemes": set(),
                })
                bucket["subthemes"].add(subtheme["title"])

        theme_sector_links.append({
            "theme_slug": theme["slug"],
            "theme_title": theme["title"],
            "lens": theme["lens"],
            "sectors": [
                {
                    "sector": item["sector"],
                    "industry_count": len(item["industries"]),
                    "subthemes": sorted(item["subthemes"]),
                    "industries": item["industries"],
                }
                for item in sorted(sector_map.values(), key=lambda row: (-len(row["industries"]), row["sector"]))
            ],
        })
        theme_company_links.append({
            "theme_slug": theme["slug"],
            "theme_title": theme["title"],
            "lens": theme["lens"],
            "companies": [
                {
                    "slug": item["slug"],
                    "title": item["title"],
                    "sector": item["sector"],
                    "status": item["status"],
                    "cluster": item["cluster"],
                    "subthemes": sorted(item["subthemes"]),
                }
                for item in sorted(company_map.values(), key=lambda row: (row["sector"] or "", row["title"]))
            ],
        })

    exports = {
        OUT_THEME_RANKINGS: theme_rows,
        OUT_SUBTHEME_RANKINGS: subtheme_rows,
        OUT_BOTTLENECKS: bottlenecks,
        OUT_EXPOSED: exposed_models,
        OUT_THEME_SECTORS: theme_sector_links,
        OUT_THEME_COMPANIES: theme_company_links,
    }
    for path, payload in exports.items():
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {path}")


if __name__ == "__main__":
    main()
