#!/usr/bin/env python3
"""Build derivative briefing surfaces from the ranked synthesis stack."""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RANKINGS_JSON = ROOT / "american_rankings.json"

OUT_INVESTOR = ROOT / "american-investor-letter.html"
OUT_OPERATOR = ROOT / "american-operator-briefing.html"
OUT_BOARD = ROOT / "american-board-summary.html"


CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.64}.wrap{max-width:1100px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 84px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:30px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.4rem,5vw,4rem);line-height:.98;margin:.18em 0 .22em;max-width:13ch}h2{font-size:1.5rem;margin:0 0 .5em}.sub{max-width:920px;color:var(--muted);font-size:1.06rem}.lead,.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.lead{border-left:4px solid var(--gold);border-radius:0 12px 12px 0;margin:26px 0}.lead p,.panel p{margin:.5em 0 0;color:var(--muted)}.lead p:first-child,.panel p:first-child{margin-top:0}.section{margin-top:32px;padding-top:14px;border-top:1px solid var(--line)}.list{padding-left:18px;color:var(--muted)}.list li{margin:.42em 0}.split{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def write_page(path: Path, title: str, subtitle: str, intro: str, sections: list[tuple[str, str, list[str], list[str]]]) -> None:
    section_html = []
    for head, body, left, right in sections:
        left_items = "".join(f"<li>{e(item)}</li>" for item in left)
        right_items = "".join(f"<li>{e(item)}</li>" for item in right)
        section_html.append(
            f"""<section class="section">
  <h2>{e(head)}</h2>
  <div class="panel"><p>{e(body)}</p></div>
  <div class="split" style="margin-top:14px">
    <div class="panel">
      <div class="eyebrow">Priority themes</div>
      <ul class="list">{left_items}</ul>
    </div>
    <div class="panel">
      <div class="eyebrow">What to do</div>
      <ul class="list">{right_items}</ul>
    </div>
  </div>
</section>"""
        )
    html_doc = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)} — US Industry Briefs</title><style>{CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="american-synthesis-hub.html">Synthesis hub</a><a href="american-rankings.html">Rankings</a><a href="american-executive-summary.html">Executive summary</a><a href="american-implications-memo.html">Implications memo</a><a href="american-synthesis-playbook.html">Playbook</a></div>
<div class="eyebrow">Derivative briefing · US · 2025-2026</div>
<h1>{e(title)}</h1>
<p class="sub">{e(subtitle)}</p>
<div class="lead"><p>{e(intro)}</p></div>
{"".join(section_html)}
</div></body></html>"""
    path.write_text(html_doc, encoding="utf-8")
    print(f"wrote {path}")


def main() -> None:
    rankings = json.loads(RANKINGS_JSON.read_text())
    top_themes = [row["title"] for row in rankings["top_themes"][:6]]
    top_bottlenecks = [row["title"] for row in rankings["top_bottlenecks"][:6]]
    top_exposed = [row["title"] for row in rankings["top_exposed_models"][:6]]

    write_page(
        OUT_INVESTOR,
        "American Investor Letter",
        "An investor-oriented version of the ranked synthesis stack.",
        "The central investment question in the 2025-2026 United States is not where demand exists. It is where the margin pool and strategic control sit once labor, proof, cultural change, and physical constraints all interact.",
        [
            ("What matters most", "The highest-ranked themes are the ones where breadth, recurrence, and real bottlenecks are aligned.", top_themes[:4], [
                "Prioritize asset control, mandatory workflows, and physical chokepoints over broad cyclical exposure.",
                "Screen out stories where thematic demand exists but the monetization sits with someone else.",
                "Treat cultural legitimacy and operator control as part of underwriting, not as side commentary.",
            ]),
            ("What to underwrite", "The best setups are the scarce layers and repeatable proof systems beneath visible demand.", top_bottlenecks[:4], [
                "Own rails, workflow software, reimbursement fluency, and power-linked infrastructure.",
                "Prefer models that get stronger as the middle weakens and the admin burden rises.",
                "Use exposed-model lists as a hard risk filter rather than a soft caution.",
            ]),
        ],
    )

    write_page(
        OUT_OPERATOR,
        "American Operator Briefing",
        "An operator-oriented version of the ranked synthesis stack.",
        "Management teams in 2025-2026 need sharper choices. The market is less forgiving of generic middle positioning, weak system control, and labor-heavy operating models that mistake demand for durable economics.",
        [
            ("Operating reality", "The ranked themes say the same thing in different domains: control and clarity matter more.", top_themes[1:5], [
                "Choose the bottleneck or permission structure you actually own.",
                "Simplify SKUs, channels, staffing, and workflows around the real constraint, not the legacy org chart.",
                "Price for saved time, trusted execution, or unavoidable compliance rather than broad category membership.",
            ]),
            ("Where teams get exposed", "The weakest models are the ones depending on easy demand, cheap labor, or undifferentiated middle layers.", top_exposed[:4], [
                "Cut exposure to promotion-dependent, subscale, and manual admin-heavy models.",
                "Move faster on productization, verification, and owned demand.",
                "Treat cultural permission and consumer ranking behavior as operating inputs, not brand fluff.",
            ]),
        ],
    )

    write_page(
        OUT_BOARD,
        "American Board Summary",
        "A board-style summary of the ranked synthesis stack.",
        "The board-level issue is not whether the company has exposure to growth themes. It is whether the company sits on the advantaged side of the current American constraint stack.",
        [
            ("Board questions", "The ranked layer helps isolate which questions actually matter at the oversight level.", top_themes[:4], [
                "What bottleneck or proof layer do we control that competitors do not?",
                "Which of our business lines sit in exposed models rather than advantaged ones?",
                "Where do labor, compliance, power, or cultural shifts cap returns unless the model changes?",
            ]),
            ("Oversight priorities", "The highest-value oversight work is around resource allocation and model exposure.", top_bottlenecks[2:6], [
                "Allocate capital toward scarce rails and repeatable workflows.",
                "Reduce dependence on commodity middle layers and low-trust labor intensity.",
                "Use the ranked stack to align strategy, M&A, hiring, and pricing decisions.",
            ]),
        ],
    )


if __name__ == "__main__":
    main()
