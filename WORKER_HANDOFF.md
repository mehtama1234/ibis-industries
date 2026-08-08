# IBIS Industries Worker Handoff

## Status at handoff

- Done: `python3` tranche resolver and baseline extract are now prepared for the next **300-industry chunk**.
- Not done: Workflow web-research chunk execution and combination into `briefs_full.json`.
- Repo context is noisy: many unrelated force/index edits already exist in git status (see below), but the tranche artifacts are in place.

## What I changed in this turn

1. Regenerated ` _run300.json` with valid records and no malformed slugs:
   - 300 items selected from `scratchpad/ibis/all_names.json` excluding done slugs from `briefs_full.json`.
   - Format now uses
     - `title` without trailing `.pdf`
     - `slug` without `-pdf`
     - `zippath` as `IBISReports/<original name>.pdf`
     - `file` as `/home/manishmehta/ui-projects/ibis-industries/txt_full/<slug>.txt`
   - `remaining` written to `_remaining_names.json` (~948 entries).

2. Re-ran extraction script after fixing tranche resolution:
   - `python3 extract_300.py`
   - Result: `ALL DONE 300 / 300`.

3. Rebuilt chunk workflow scripts from template:
   - `wf_r3_chunk1.js` … `wf_r3_chunk5.js` regenerated from `wf_ibis_full.js` (60 items each).

## Current artifact check

- `_run300.json` → `300` items
- `txt_full/` contains full 300 baseline txt files (from current `_run300.json`)
- `briefs_r3_1.json` exists but is stale from an older partial run (12 records) and not part of this tranche.
- `wf_r3_chunk1.output`, `wf_r3_chunk2.output`, `wf_r3_chunk1_live.output`, etc. are legacy outputs and do not reflect current tranche completion.

## Last blocking step (important)

- Workflow runner remains unavailable in this environment.
- `run_next_chunk_sequence.sh` requires `WORKFLOW_CMD` and a runnable JS workflow runner:
  - `bash -lc "${WORKFLOW_CMD} \"Workflow({scriptPath:'${script}')\"" > ...`
- `codex exec` attempts from here have failed earlier with environment/app-server errors (no workable runner path surfaced in-shell).
- Therefore, chunk jobs cannot be executed in this shell yet.

## Next thread should run

### 1) Execute five chunk jobs (background-capable)

From repo root:

```bash
WORKFLOW_CMD="<your-working-workflow-runner-command>" \
  bash -lc './run_next_chunk_sequence.sh _run300.json wf_r3_chunk 60'
```

or manually one-by-one:

```bash
for i in 1 2 3 4 5; do
  bash -lc "${WORKFLOW_CMD} \"Workflow({scriptPath:'wf_r3_chunk${i}.js'})\"" > wf_r3_chunk${i}.output 2>&1 || true
  python3 harvest_wf.py wf_r3_chunk${i}.output briefs_r3_${i}.json 60 $(((i-1)*60)) _run300.json
  python3 - <<'PY'
import json
arr=json.load(open('_run300.json'))
out=json.load(open(f'briefs_r3_${i}.json'))
start=$(((i-1)*60)); end=min(start+60,len(arr))
want={x['slug'] for x in arr[start:end]}
got={x.get('slug') for x in out}
print('chunk',${i},'missing',sorted(want-got))
PY

done
```

### 2) Retry missing entries if needed

- If any slugs are missing, build a tiny retry script from `wf_ibis_full.js` and run once, harvesting to `briefs_r3_R.json`.

### 3) Merge into master

- Add `briefs_r3_1.json` … `briefs_r3_5.json` + `briefs_r3_R.json` to `combine.py` source list if needed and include current tranche canon map for title overrides.
- Run:
  - `python3 combine.py`
  - `python3 build_full.py`
- Then commit + push.

## Command cheat-sheet

- Rebuild tranche from current code:
  - `python3 - <<'PY' ...` (same selection block used in this turn)
- Rebuild chunk scripts:
  - `python3 - <<'PY'` (template split to 5 × 60, already run)
- Baseline extraction:
  - `python3 extract_300.py`

## Important reminders

- Do NOT read `.output` files into model context; use `harvest_wf.py` only.
- Keep all output briefs schema relaxed (current schema in `wf_ibis_full.js` already does this).
- Keep Codex-only execution thread continuity in the worker prompt if applicable.
