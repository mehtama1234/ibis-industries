# Synthesis Completion Audit

Generated from the current worktree.

## Corpus

- Industry briefs: `1491`
- Top-level themes: `10`
- Subthemes: `50`
- Microthemes: `200`
- Theme signal bullets: `60`
- Theme tension bullets: `40`
- Theme second-order bullets: `40`
- Company memos: `251`
- Extracted company universe: `7218`
- Company pages surfaced: `251`

## Theme Lenses

- `Consumer`
- `Cultural / Consumer`
- `Cultural / Social`
- `Industrial`
- `Industrial / Institutional`
- `Institutional / Technological`
- `Social / Labor`
- `Societal / Industrial`
- `Societal / Institutional`
- `Technological / Industrial`

## Artifact Coverage

| Artifact | Size | Where | Signals | Do | Underwrite | Tensions | Second-order | Total |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| `index.html` | 13934641 | 4 | 9 | 4 | 4 | 4 | 4 | 29 |
| `economic-intelligence.html` | 35987 | 5 | 5 | 5 | 5 | 5 | 5 | 30 |
| `american-outlook-2025-2026.html` | 71076 | 10 | 11 | 4 | 4 | 8 | 4 | 41 |
| `american-economy-2025-2026.html` | 139271 | 16 | 17 | 8 | 8 | 12 | 8 | 69 |
| `american-synthesis-playbook.html` | 27790 | 10 | 10 | 4 | 4 | 6 | 4 | 38 |
| `american-themes.html` | 47342 | 10 | 21 | 10 | 10 | 10 | 10 | 71 |
| `american-theme-briefs.html` | 447136 | 20 | 71 | 20 | 20 | 10 | 10 | 151 |
| `american-theme-memos.html` | 470613 | 20 | 21 | 10 | 10 | 20 | 20 | 101 |
| `subthemes.html` | 220844 | 69 | 83 | 69 | 83 | 14 | 14 | 332 |
| `business-lenses.html` | 24428 | 8 | 8 | 8 | 8 | 8 | 8 | 48 |
| `business-outlooks.html` | 127624 | 16 | 38 | 16 | 16 | 22 | 38 | 146 |
| `business-profiles.html` | 9824 | 4 | 4 | 4 | 4 | 4 | 4 | 24 |
| `sector-memos.html` | 293290 | 14 | 86 | 14 | 14 | 14 | 14 | 156 |
| `sector-outlooks.html` | 202825 | 28 | 48 | 62 | 62 | 48 | 48 | 296 |
| `sector-cases.html` | 9408 | 4 | 4 | 4 | 4 | 4 | 4 | 24 |
| `force-operator-translations.html` | 37035 | 14 | 14 | 14 | 14 | 14 | 14 | 84 |
| `company-cluster-outlooks.html` | 495145 | 31 | 111 | 31 | 31 | 111 | 31 | 346 |
| `company-universe.html` | 120625 | 60 | 60 | 60 | 60 | 60 | 60 | 360 |
| `company-clusters.html` | 60629 | 31 | 31 | 31 | 31 | 31 | 31 | 186 |
| `company-scoreboard.html` | 219345 | 60 | 60 | 60 | 60 | 60 | 60 | 360 |
| `company-comparisons.html` | 1138819 | 318 | 318 | 318 | 318 | 318 | 318 | 1908 |
| `company-memos.html` | 614940 | 40 | 40 | 40 | 40 | 40 | 40 | 240 |
| `operators.html` | 12720 | 8 | 8 | 8 | 8 | 8 | 8 | 48 |

## Requirement Audit

| Requirement | Status | Evidence |
| --- | --- | --- |
| Completed 1,491-industry corpus exists as the base layer | Proved | `briefs_full.json` contains `1491` researched industry briefs. |
| A detailed 2025-2026 US economy interpretation exists across societal, cultural, consumer, and industrial lenses | Proved | The macro/theme stack exists in `american-outlook-2025-2026.html`, `american-economy-2025-2026.html`, `american-synthesis-playbook.html`, `economic-intelligence.html`, and `american-themes.html`; the capstone explicitly includes four umbrella sections for consumer, cultural/social, societal/institutional, and industrial/physical readings (`5`/5 markers present), and the outlook page adds explicit national-consequence and decision-agenda sections (`4`/4 markers present). |
| Each major theme is deepened into explicit subthemes, tensions, signals, and second-order effects | Proved | `american_themes_taxonomy.json` contains `10` themes, `50` subthemes, `200` microthemes, `60` theme-level signal bullets, `40` theme-level tension bullets, and `40` theme-level second-order bullets; the brief/memo surfaces render those structures in `american-theme-briefs.html` and `american-theme-memos.html`. |
| Themes are connected to sectors and representative companies | Proved | Sector/company linkage appears across `sector-memos.html`, `sector-outlooks.html`, `company-memos.html`, `company-universe.html`, `company-clusters.html`, and `company-comparisons.html`; the company layer contains `251` memos and `251` surfaced pages, while the macro artifacts surface representative companies directly. |
| Output artifacts explain what is happening, why it matters, where it shows up, and what operators/investors should do | Proved | The major artifacts all carry the six recurring fields: `Where it shows up`, `Signals`, `What to do`, `What to underwrite`, `Tensions`, and `Second-order effects`; the new `american-synthesis-playbook.html` consolidates those fields into an explicit end-state executive artifact. |
| The requested synthesis layer exists as a coherent end-state stack rather than as scattered partial pages | Proved | The current worktree contains a stacked macro surface (`american-outlook-2025-2026.html`), capstone narrative (`american-economy-2025-2026.html`), executive playbook (`american-synthesis-playbook.html`), theme briefs (`american-theme-briefs.html`), theme memos (`american-theme-memos.html`), and linked sector/company evidence pages. |

## Current Read

- The synthesis stack now consistently covers the six decision fields across the major macro, theme, sector, business, company, and operator artifacts.
- The macro layer is no longer just a distributed set of pages: the capstone now carries a four-lens and system-consequences read, while the outlook page carries national-consequence and decision-agenda sections.
- The current worktree now proves the requested synthesis stack exists at macro, theme, sector, and company levels with direct operator/investor translation.
- The audit evidence is aligned to the actual objective: produce the synthesis layer, deepen the themes, connect them to sectors and companies, and expose clear decision-grade artifacts.

