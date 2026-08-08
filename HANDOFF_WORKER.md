# End-to-End Objective: complete all US IBISWorld industry briefs in one Codex-owned thread

Long-term goal (no helper threads): turn the remaining ~970 US IBISWorld industries into **current 2025–2026 web-researched
briefs**, grow `briefs_full.json` from 521 → the full ~1,491, then refresh force and collection assets that consume
those briefs, and commit + push the result.

Work in tranches of ~300 (or 200) at a time. Everything below is already scripted in this repo.

---

## 0. Ground truth / locations

- **Repo (cwd for everything):** `/home/manishmehta/ui-projects/ibis-industries` (private GitHub `mehtama1234/ibis-industries`).
- **Source zip:** `/home/manishmehta/ui-projects/business-stuff/IBISReports-20260807T194014Z-1-001.zip`
  — 1,491 industry PDFs, **2022 vintage**, ~53 pages each, clean extractable text (pypdf). Skip the junk file `502 Bad Gateway.pdf`.
- **Master output you grow:** `briefs_full.json` (currently 521 records). Each record schema is at the bottom.
- **All 1,491 names:** `scratchpad/ibis/all_names.json` (if this path is missing, regenerate: `python3 -c "import zipfile,json; z=zipfile.ZipFile('<zip>'); json.dump(sorted(n for n in z.namelist() if n.endswith('.pdf') and '502 Bad' not in n), open('all_names.json','w'))"`).
- **Already-done slugs:** the 521 slugs already in `briefs_full.json` — always dedupe against these.

## HARD RULES (non-negotiable)
1. **Model-agnostic execution.** Run agents with the configured/default model for this environment; do not hardcode a model in the workflow.
2. **No external helper threads.** This run is fully end-to-end and self-contained in this Codex thread; no Claude, no off-thread agents, no extra assistant handoff.
   Every workflow prompt must still forbid the Agent tool / deep-research / sub-agents ("if you do, you fail"). The workflow template already does.
3. **Never read a workflow/agent transcript `.output` into your context** — they're 600KB–1.5MB. Always harvest with the scripts (they parse on disk, print only a summary).
4. **Git identity:** `user.name="Manish Mehta"`, `user.email="manishmehta@local"`.
5. **PAT** for `mehtama1234` is in `~/.git-credentials` — extract host/user/token via python regex, **NEVER print it**. `git push origin main` uses the store helper automatically.

---

## PHASE 1 — pick the next tranche (~300 new)
1. Compute the remaining (not-yet-done) names → `_remaining_names.json`:
```
python3 - <<'PY'
import json,re,html
allnames=json.load(open('scratchpad/ibis/all_names.json'))   # fix path
done={b['slug'] for b in json.load(open('briefs_full.json'))}
def slug(d): return re.sub(r'[^a-z0-9]+','-',d.replace("'",'').replace('&','and').lower()).strip('-')
rem=[]
for n in allnames:
    disp=html.unescape(n).replace('IBISReports/','').replace('.pdf','').replace('_',"'")
    if slug(disp) not in done: rem.append(disp)
json.dump(rem,open('_remaining_names.json','w')); print('remaining:',len(rem))
PY
```
2. Select the next tranche from `_remaining_names.json` into `run` form.
   Use a deterministic script (no picker model) that preserves sector diversity and returns ~300 exact names.
   You can reuse a prior selector command, but keep the logic explicit and auditable in this handoff run.
3. Resolve the selected names and cap at 300 → `_run300.json` (list of `{title, slug, zippath, file}`).
   Reuse the exact resolve block format below:
unescape `&amp;`→`&` but **keep the `_`** (IBIS uses `_` for apostrophes in filenames); display title = `_`→`'`;
`file` = `<repo>/txt_full/<slug>.txt`. Dedupe vs `done`. (See the exact block in git history / prior `prep_200.py`.)

## PHASE 2 — extract baseline text (background)
`extract_full.py` / `extract_300.py` already do this: pypdf, **first 22 pages only** (meat is front-loaded),
cap 38k chars, strip the `M/D/YY, H:MM` headers + searchfunder URLs → `txt_full/<slug>.txt`.
**Run it in the background** (pypdf is ~4s/PDF; 300 ≈ 15 min). Point it at `_run300.json`. Verify 0 missing/thin.

## PHASE 3 — deep web-research briefs (the heavy lifting)
This is where the numbers get pulled. Use **background Workflows in chunks of ~60** (5 chunks for 300).
- The template is **`wf_ibis_full.js`** — a parameterized workflow: one model-configured agent per industry, reads its
  `txt_full/<slug>.txt` baseline AND **WebSearch/WebFetch's the current 2025-2026 data**, returns the full brief
  via a **loosened JSON schema** (schema already has NO `enum`, NO `additionalProperties:false`, minimal
  `required` — this is critical: strict schemas cause `StructuredOutput retry cap (5) exceeded` failures).
- Generate the chunk scripts by baking the items into the template (string-slice the `const items` line):
```
python3 - <<'PY'
import json,math
items=json.load(open('_run300.json')); tmpl=open('wf_ibis_full.js').read()
n=5; sz=math.ceil(len(items)/n)
for i in range(n):
    lite=[{k:x[k] for k in ('title','slug','file')} for x in items[i*sz:(i+1)*sz]]
    s=tmpl.replace("const items = (args && args.items) || []", "const items = "+json.dumps(lite))
    s=s.replace("name: 'ibis-deep-current',", f"name: 'ibis-r3-chunk{i+1}',")
    open(f'wf_r3_chunk{i+1}.js','w').write(s); print(i+1,len(lite))
PY
```
- Fire chunks **one at a time** (`Workflow({scriptPath:'wf_r3_chunk1.js'})`). When each completes, **harvest to disk**:
```
python3 harvest_wf.py <task.output> briefs_r3_1.json 60 0   # (n, start args are cosmetic; the real check below)
python3 - <<'PY'
import json
got={b['slug'] for b in json.load(open('briefs_r3_1.json'))}
items=json.load(open('_run300.json'))[0:60]
print('missing:',[it['slug'] for it in items if it['slug'] not in got])
PY
```
  `harvest_wf.py` parses the workflow `.output` (a pretty-printed JSON dict; the briefs are under key `result`)
  and writes a clean array — it does NOT load the transcript into your model context.
- **Expect ~1–2 schema failures per 60-chunk.** After all chunks, collect the missing slugs, build a tiny
  retry workflow (same template, bake just the missing items), run it, harvest → `briefs_r3_R.json`.

## PHASE 4 — combine + rebuild the index
1. Add your new files to `combine.py`'s `sources` list (e.g. `briefs_r3_1.json … briefs_r3_5.json`, `briefs_r3_R.json`)
   and extend its `canon` title map to include your `_run300.json` (agents rename titles verbosely, e.g.
   "US X Industry 2025-2026"; combine.py overrides `title` with the clean name from the run file). Then:
```
python3 combine.py        # dedupes by slug, normalizes, clamps sector to the 14-set -> briefs_full.json
python3 build_full.py     # rebuilds the searchable index.html (single self-contained file)
```
2. **Commit + push** (this is the handoff artifact):
```
git -c user.name="Manish Mehta" -c user.email="manishmehta@local" add -f briefs_full.json index.html _run300.json combine.py
git -c user.name="Manish Mehta" -c user.email="manishmehta@local" commit -q -m "Tranche 3: briefs NNN -> MMM ...<footer>"
git push origin main
```

## PHASE 5 — combine forces and collections
1. Rebuild force packs and collection assets from the updated full briefs set:
   - `python3 build_force_packs.py` (or the forced variant for any specific theme pass already used in this repo)
   - `for f in _forcebuild_*.json; do s=${f#_forcebuild_}; s=${s%.json}; python3 build_collection.py "$s"; done`
   - `python3 build_mega_bundle.py`
2. Re-run `python3 build_full.py` if `index.html` changed or if force/collection content changed.
3. Commit + push once briefs, forces, and collections are all updated and consistent.

## PHASE 6 — verify + report
- **Model purity:** scan run logs for forbidden `Agent` delegation. Must be single-model runs, 0 sub-agents.
- Report back to the user: **new total count**, sectors gained, and confirm that `briefs_full.json` plus rebuilt force
  files are pushed.

---

## The brief schema (what each agent returns — already encoded in `wf_ibis_full.js`)
`title, sector` (one of: Agriculture | Manufacturing | Construction | Retail | Food & Drink | Healthcare |
Finance & Insurance | Technology & Digital | Energy & Environment | Business Services | Consumer Services |
Media & Entertainment | Transport & Logistics | Real Estate), `one_liner, overview` (current 2025-26),
`key_stats{market_size(+yr), growth, businesses, employees, profit_margin, concentration}`,
`baseline_2022{market_size, growth}`, `how_it_makes_money, cost_structure, major_players[],
current_dynamics` (deep), `whats_growing, whats_shrinking, recent_developments[]` (dated 2023-26),
`outlook, themes[]` (4-6 reusable force-tags), `data_year, sources[], one_sentence`.

## Gotchas checklist
- [ ] pypdf slow → background + first 22 pages only.
- [ ] Loosen the schema (no enum / no additionalProperties) or you get StructuredOutput retry-cap fails.
- [ ] Never read workflow `.output` transcripts into context — harvest with the scripts.
- [ ] Workflow `.output` = JSON dict; briefs are under `result` (harvest_wf.py handles it).
- [ ] Agents rename `title` verbosely → combine.py must override from the `_run*.json` canon map.
- [ ] Fire chunks one at a time and harvest between (keeps context clean; on 1M context you can also do 2).
- [ ] Retry the handful of per-chunk schema failures at the end.
- [ ] If this run is for final publish, refresh forces/collections after briefs merge (`build_force_packs.py`, `build_collection.py`, `build_mega_bundle.py`).
