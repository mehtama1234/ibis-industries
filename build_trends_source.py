#!/usr/bin/env python3
"""Regenerate the cross-cutting trend source from the current full-corpus synthesis layers."""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BRIEFS_JSON = ROOT / "briefs_full.json"
RAW_TRENDS_JSON = ROOT / "trends_full_raw.json"
THEMES_JSON = ROOT / "american_themes_taxonomy.json"
COMPANY_JSON = ROOT / "company_memos.json"
OUT = ROOT / "trends_full_raw.json"

STOP = {
    "in",
    "the",
    "us",
    "and",
    "of",
    "a",
    "an",
    "services",
    "service",
    "stores",
    "store",
    "inc",
    "co",
    "manufacturing",
    "operation",
    "operations",
    "plant",
    "industry",
    "brief",
    "market",
    "size",
    "providers",
    "provider",
    "2025",
    "2026",
    "2024",
    "sector",
}

TREND_THEME_MAP = {
    "AI adoption and labor displacement": [
        "machine-intelligence-and-compute-buildout",
        "work-without-the-old-firm",
        "regulated-software-and-admin-state",
    ],
    "Tariff-driven cost shock and supply chain upheaval": [
        "physical-reindustrialization-and-infrastructure",
        "scale-financialization-and-the-owned-economy",
    ],
    "Consolidation and scale-driven shakeout": [
        "scale-financialization-and-the-owned-economy",
        "barbelled-consumer-america",
        "regulated-software-and-admin-state",
    ],
    "Reimbursement pressure and pricing power collapse": [
        "aging-care-and-the-assistance-economy",
        "regulated-software-and-admin-state",
    ],
    "Labor shortage and wage spiral": [
        "work-without-the-old-firm",
        "aging-care-and-the-assistance-economy",
        "physical-reindustrialization-and-infrastructure",
    ],
    "Energy demand surge from AI and data centers": [
        "machine-intelligence-and-compute-buildout",
        "physical-reindustrialization-and-infrastructure",
    ],
    "Real estate bifurcation and office crisis": [
        "space-housing-and-local-friction",
        "physical-reindustrialization-and-infrastructure",
    ],
    "Channel shift: e-commerce and direct-to-consumer displacement of physical retail": [
        "barbelled-consumer-america",
        "experience-status-and-community",
        "scale-financialization-and-the-owned-economy",
    ],
    "Demographic dividend: aging population driving demand in healthcare and senior living": [
        "aging-care-and-the-assistance-economy",
    ],
    "Margin compression from inflation and input costs": [
        "barbelled-consumer-america",
        "physical-reindustrialization-and-infrastructure",
        "scale-financialization-and-the-owned-economy",
    ],
    "Consolidation and scale in media, publishing, and entertainment": [
        "experience-status-and-community",
        "scale-financialization-and-the-owned-economy",
    ],
    "Health consciousness and dietary shift away from sugar and alcohol": [
        "wellness-recodes-daily-life",
    ],
    "Regulatory fragmentation and compliance cost explosion": [
        "regulated-software-and-admin-state",
    ],
    "Fintech and embedded finance disrupting traditional banking and payments": [
        "scale-financialization-and-the-owned-economy",
        "regulated-software-and-admin-state",
    ],
    "Premiumization and bifurcation: affluent vs. value consumers diverging": [
        "barbelled-consumer-america",
        "experience-status-and-community",
    ],
    "Supply chain shortages and geopolitical volatility": [
        "physical-reindustrialization-and-infrastructure",
        "machine-intelligence-and-compute-buildout",
    ],
    "Gig economy and fractional work blurring permanent employment": [
        "work-without-the-old-firm",
    ],
    "Alternative ownership: PE, REIT, and institutional capital reshaping industries": [
        "scale-financialization-and-the-owned-economy",
        "space-housing-and-local-friction",
        "aging-care-and-the-assistance-economy",
    ],
}


def toks(text: str) -> list[str]:
    text = html.unescape(text).lower().replace("&", " and ")
    words = re.sub(r"[^a-z0-9]+", " ", text).split()
    return [word for word in words if word not in STOP and len(word) > 1]


def tmatch(a: str, b: str) -> bool:
    return a == b or (len(a) >= 4 and b.startswith(a)) or (len(b) >= 4 and a.startswith(b))


def overlap(name_tokens: list[str], brief_tokens: list[str]) -> int:
    used = set()
    count = 0
    for word in brief_tokens:
        for idx, token in enumerate(name_tokens):
            if idx in used:
                continue
            if tmatch(word, token):
                used.add(idx)
                count += 1
                break
    return count


def match_slug(name: str, briefkeys: list[tuple[str, list[str]]]) -> str | None:
    name_tokens = toks(name)
    if not name_tokens:
        return None
    best = None
    bestscore = 0.0
    besttie = 99
    for slug, brief_tokens in briefkeys:
        if not brief_tokens:
            continue
        ov = overlap(name_tokens, brief_tokens)
        if ov == 0:
            continue
        covers = ov == len(brief_tokens) or ov >= 2
        if not covers:
            continue
        score = ov / len(brief_tokens)
        tie = len(brief_tokens) - ov
        if score > bestscore or (score == bestscore and tie < besttie):
            best = slug
            bestscore = score
            besttie = tie
    return best if bestscore >= 0.5 else None


def unique_ordered(values):
    seen = set()
    out = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(value)
    return out


def trim(text: str, limit: int = 220) -> str:
    text = " ".join(str(text or "").split())
    if len(text) <= limit:
        return text
    return text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:") + "..."


def main() -> None:
    briefs = json.loads(BRIEFS_JSON.read_text())
    raw_trends = json.loads(RAW_TRENDS_JSON.read_text())
    themes = {theme["slug"]: theme for theme in json.loads(THEMES_JSON.read_text())["themes"]}
    companies = json.loads(COMPANY_JSON.read_text())
    briefkeys = [(brief["slug"], toks(brief["title"])) for brief in briefs]
    brief_by_slug = {brief["slug"]: brief for brief in briefs}

    enriched = []
    for trend in raw_trends["trends"]:
        linked_theme_slugs = TREND_THEME_MAP.get(trend["name"], [])
        linked_themes = [themes[slug] for slug in linked_theme_slugs]
        slugs = []
        for name in trend.get("industries", []):
            slug = match_slug(name, briefkeys)
            if slug and slug not in slugs:
                slugs.append(slug)
        sector_counts = Counter()
        brief_theme_counts = Counter()
        subtheme_titles = []
        subtheme_effects = []
        company_matches = []
        constraints = Counter()
        owner_types = Counter()
        loser_types = Counter()
        diligence_questions = []
        for slug in slugs:
            brief = brief_by_slug[slug]
            sector_counts[brief["sector"]] += 1
            for item in brief.get("themes", []):
                brief_theme_counts[item] += 1
        slugs_set = set(slugs)
        for company in companies:
            overlap_hits = [
                item for item in company.get("linked_industries", []) if item.get("slug") in slugs_set
            ]
            if not overlap_hits:
                continue
            company_matches.append((len(overlap_hits), company))
            for item in company.get("constraints", []):
                constraints[item] += 1
            if company.get("best_owner_type"):
                owner_types[company["best_owner_type"]] += 1
            for item in company.get("likely_losers", []):
                loser_types[item] += 1
            for item in company.get("diligence_questions", []):
                if item not in diligence_questions:
                    diligence_questions.append(item)
        company_matches.sort(
            key=lambda item: (-item[0], -item[1].get("mention_count", 0), item[1]["title"])
        )
        for theme in linked_themes:
            for subtheme in theme.get("subthemes", [])[:3]:
                subtheme_titles.append(subtheme["title"])
                effect = subtheme.get("follow_on_effects", [])
                if effect:
                    subtheme_effects.append(effect[0])
        top_companies = []
        for _, company in company_matches[:4]:
            top_companies.append(
                {
                    "slug": company["slug"],
                    "title": company["title"],
                    "sector": company.get("top_sector", "Unknown"),
                    "memo": trim(company.get("operator_memo") or company.get("investor_memo") or ""),
                }
            )
        top_constraints = [item for item, _ in constraints.most_common(3)]
        top_owner_types = [item for item, _ in owner_types.most_common(2)]
        top_losers = [item for item, _ in loser_types.most_common(2)]
        operator_implications = []
        if top_constraints and top_owner_types:
            operator_implications.append(
                f"The current winners usually solve for {top_constraints[0]} and {top_constraints[1] if len(top_constraints) > 1 else top_constraints[0]}, and they more often look like {top_owner_types[0]} structures than fragmented independents."
            )
        if top_losers:
            operator_implications.append(
                f"This trend keeps squeezing {top_losers[0]}{f' and {top_losers[1]}' if len(top_losers) > 1 else ''} because they have the least room to absorb the new constraint stack."
            )
        if not operator_implications:
            operator_implications.append(
                "Use this trend as a filter for where operating complexity is rising faster than generic demand."
            )
        investor_implications = unique_ordered(diligence_questions)[:2]
        if not investor_implications and top_constraints:
            investor_implications.append(
                f"What would break if {top_constraints[0]} became the binding constraint instead of a secondary issue?"
            )
        tensions = unique_ordered(
            item for theme in linked_themes for item in theme.get("structural_tensions", [])[:2]
        )[:3]
        signals = unique_ordered(
            item for theme in linked_themes for item in theme.get("signals_to_watch", [])[:2]
        )[:3]
        second_order_effects = unique_ordered(subtheme_effects)[:3]
        enriched.append(
            {
                **trend,
                "slugs": slugs,
                "linked_theme_slugs": linked_theme_slugs,
                "linked_theme_titles": [theme["title"] for theme in linked_themes],
                "top_sectors": [sector for sector, _ in sector_counts.most_common(4)],
                "recurring_brief_themes": [item for item, _ in brief_theme_counts.most_common(5)],
                "subthemes": unique_ordered(subtheme_titles)[:5],
                "structural_tensions": tensions,
                "signals_to_watch": signals,
                "second_order_effects": second_order_effects,
                "representative_companies": top_companies,
                "operator_implications": operator_implications[:2],
                "investor_implications": investor_implications[:2],
            }
        )

    payload = {
        "headline": (
            "Across the full 1,491-industry corpus in 2025-2026, labor scarcity, demographic aging, "
            "consumer bifurcation, AI buildout, compliance load, channel migration, and consolidation "
            "keep repricing who captures demand, who gets squeezed, and which operators can actually "
            "turn growth into durable economics."
        ),
        "trends": enriched,
    }
    OUT.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {OUT}")
    print(f"trends={len(enriched)}")


if __name__ == "__main__":
    main()
