#!/usr/bin/env python3
"""Fallback generator: produce industry briefs by calling `codex --search exec` directly."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any, Dict, List
from concurrent.futures import ThreadPoolExecutor, as_completed


REQUIRED_KEYS = [
    "title",
    "sector",
    "one_liner",
    "overview",
    "key_stats",
    "baseline_2022",
    "how_it_makes_money",
    "cost_structure",
    "major_players",
    "current_dynamics",
    "whats_growing",
    "whats_shrinking",
    "recent_developments",
    "outlook",
    "themes",
    "data_year",
    "sources",
    "one_sentence",
    "slug",
]


def _prompt(item: Dict[str, Any]) -> str:
    return f"""You are drafting a US IBIS industry brief for the dataset described below.
Use web search for current 2025–2026 data.

Read the baseline file:
{item["file"]}

Return ONE raw JSON object only (no markdown, no explanation). It MUST include exactly these keys:
title, sector, one_liner, one_sentence, overview, key_stats, baseline_2022, how_it_makes_money, cost_structure, major_players, current_dynamics, whats_growing, whats_shrinking, recent_developments, outlook, themes, data_year, sources, slug

Rules:
- sector must be one of: Agriculture | Manufacturing | Construction | Retail | Food & Drink | Healthcare | Finance & Insurance | Technology & Digital | Energy & Environment | Business Services | Consumer Services | Media & Entertainment | Transport & Logistics | Real Estate
- key_stats must include market_size and growth at minimum.
- baseline_2022 must include market_size and growth.
- major_players and themes arrays.
- recent_developments MUST be an array of 3-6 short dated strings.
- Use year-stamped numbers only.

Industry:
title: {item["title"]}
slug: {item["slug"]}
"""


def _extract_json_text(raw: str) -> str | None:
    raw = raw.strip()
    start = raw.find("{")
    while start != -1:
        depth = 0
        for i in range(start, len(raw)):
            ch = raw[i]
            if ch == "{":
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return raw[start : i + 1]
        start = raw.find("{", start + 1)
    return None


def _normalize_record(r: Dict[str, Any]) -> Dict[str, Any]:
    out = {k: r.get(k) for k in REQUIRED_KEYS if k in r}
    out["title"] = out.get("title", "")
    out["slug"] = out.get("slug", "")
    out["sector"] = out.get("sector", "Business Services")
    out["one_liner"] = out.get("one_liner", "")
    out["one_sentence"] = out.get("one_sentence", "")
    out["overview"] = out.get("overview", "")
    out["current_dynamics"] = out.get("current_dynamics", "")
    out["whats_growing"] = out.get("whats_growing", "")
    out["whats_shrinking"] = out.get("whats_shrinking", "")
    out["outlook"] = out.get("outlook", "")
    out["data_year"] = out.get("data_year", "2025-2026")

    def _as_list(x):
        if isinstance(x, list):
            return [str(i) for i in x]
        if x is None:
            return []
        return [str(x)]

    out["major_players"] = _as_list(out.get("major_players"))
    out["themes"] = _as_list(out.get("themes"))
    rd = out.get("recent_developments", [])
    if isinstance(rd, dict):
        rd = [v for _, v in rd.items() if v]
    out["recent_developments"] = _as_list(rd)[:6]

    ks = out.get("key_stats") if isinstance(out.get("key_stats"), dict) else {}
    if not isinstance(ks, dict):
        ks = {}
    for k in ("market_size", "growth", "businesses", "employees", "profit_margin", "concentration"):
        ks.setdefault(k, "n/a")
    out["key_stats"] = ks

    b2 = out.get("baseline_2022") if isinstance(out.get("baseline_2022"), dict) else {}
    if not isinstance(b2, dict):
        b2 = {}
    b2.setdefault("market_size", "n/a")
    b2.setdefault("growth", "n/a")
    out["baseline_2022"] = b2

    out["how_it_makes_money"] = out.get("how_it_makes_money", "")
    out["cost_structure"] = out.get("cost_structure", "")
    out["sources"] = _as_list(out.get("sources"))[:40]
    return out


def _run_one(
    item: Dict[str, Any], idx: int, retries: int = 1, model: str = "gpt-5.5"
) -> Dict[str, Any] | None:
    return _run_one_with_model(item, idx, retries, _prompt(item), model=model)


def _run_one_with_model(
    item: Dict[str, Any],
    idx: int,
    retries: int,
    prompt: str,
    model: str = "gpt-5.5",
) -> Dict[str, Any] | None:
    cmd = ["codex", "--search", "exec", "-m", model, prompt] if model else ["codex", "--search", "exec", prompt]
    for attempt in range(retries + 1):
        proc = subprocess.run(
            cmd,
            cwd=Path(__file__).resolve().parent,
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            if attempt < retries:
                time.sleep(1.0)
                continue
            return None
        text = proc.stdout.strip()
        js = _extract_json_text(text)
        if not js:
            if attempt < retries:
                time.sleep(1.0)
                continue
            return None
        try:
            data = json.loads(js)
        except Exception:
            if attempt < retries:
                time.sleep(1.0)
                continue
            return None
        if not isinstance(data, dict):
            return None

        record = _normalize_record(data)
        if not record.get("slug"):
            record["slug"] = item["slug"]
        if not record.get("title"):
            record["title"] = item["title"]
        return {**record, "_codex_index": idx}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("run_file", help="Tranche file such as _run300_next3.json")
    ap.add_argument("--start", type=int, default=0)
    ap.add_argument("--count", type=int, default=5)
    ap.add_argument("--output", default=None)
    ap.add_argument("--workers", type=int, default=1, help="Parallel worker count")
    ap.add_argument("--retries", type=int, default=1, help="Retries per item")
    ap.add_argument("--model", default="gpt-5.5", help="Codex model")
    args = ap.parse_args()

    items = json.loads(Path(args.run_file).read_text(encoding="utf-8"))
    slice_ = items[args.start : args.start + args.count]
    out_path = Path(
        args.output
        or f"briefs_r3_batch_{Path(args.run_file).stem}_{args.start}_{args.count}.json"
    )
    results: List[Dict[str, Any]] = []

    if args.workers <= 1:
        for i, item in enumerate(slice_, start=1):
            print(f"[{i}/{len(slice_)}] {item['slug']}", flush=True)
            rec = _run_one(item, i, retries=args.retries, model=args.model)
            if rec is not None:
                results.append(rec)
            else:
                print(f"  -> failed, skipping")
            time.sleep(0.75)
    else:
        with ThreadPoolExecutor(max_workers=args.workers) as ex:
            futures = {}
            for i, item in enumerate(slice_, start=1):
                print(f"[{i}/{len(slice_)}] {item['slug']}", flush=True)
                futures[ex.submit(_run_one, item, i, args.retries, args.model)] = i
            for fut in as_completed(futures):
                rec = fut.result()
                if rec is not None:
                    results.append(rec)
                else:
                    print(f"  -> failed, skipping", flush=True)

    results.sort(key=lambda r: r.pop("_codex_index", 10**9))

    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {len(results)} / {len(slice_)} to {out_path}")


if __name__ == "__main__":
    main()
