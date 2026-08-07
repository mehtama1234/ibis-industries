#!/usr/bin/env python3
"""Harvest each agent's final JSON brief from its task transcript, WITHOUT loading into model context."""
import json, html, re, os, sys

ROOT=os.path.dirname(os.path.abspath(__file__))
TASKS="/tmp/claude-1000/-home-manishmehta-projects/de20a7fc-8dc8-42cf-b660-6cc71272fcc7/tasks"
ids=json.load(open(f'{ROOT}/_agent_ids.json'))

def walk_strings(obj):
    if isinstance(obj,str): yield obj
    elif isinstance(obj,dict):
        for v in obj.values(): yield from walk_strings(v)
    elif isinstance(obj,list):
        for v in obj: yield from walk_strings(v)

def is_skeleton(d):
    """Reject the prompt's schema skeleton (placeholder values)."""
    sec=str(d.get('sector','')); ms=str(d.get('key_stats',{}).get('market_size','')) if isinstance(d.get('key_stats'),dict) else ''
    ol=str(d.get('one_liner','')); dy=str(d.get('data_year',''))
    return (sec.startswith('pick ONE') or 'latest $' in ms or ol.startswith('one plain sentence')
            or dy.startswith('the year of') or 'the single biggest takeaway' in str(d.get('one_sentence','')).lower()[:40])

def candidates_from_text(text):
    cands=[]
    for m in re.finditer(r'```json\s*(\{.*?\})\s*```', text, re.S): cands.append(m.group(1))
    for m in re.finditer(r'```\s*(\{.*?\})\s*```', text, re.S): cands.append(m.group(1))
    if '"one_sentence"' in text and '"title"' in text:
        i=text.find('{'); j=text.rfind('}')
        if i!=-1 and j!=-1 and j>i: cands.append(text[i:j+1])
    out=[]
    for c in cands:
        try:
            d=json.loads(c)
            if isinstance(d,dict) and 'title' in d and 'one_sentence' in d and not is_skeleton(d):
                out.append(d)
        except Exception: continue
    return out

def collect_text(path):
    """Gather all candidate text blobs from a transcript file (JSONL or plain)."""
    blobs=[]
    raw=open(path,encoding='utf-8',errors='replace').read()
    parsed_any=False
    for line in raw.splitlines():
        line=line.strip()
        if not line: continue
        try:
            obj=json.loads(line); parsed_any=True
        except Exception:
            continue
        for s in walk_strings(obj):
            if '```' in s or ('"one_sentence"' in s) or ('one_sentence' in s and 'title' in s):
                blobs.append(s)
    if not parsed_any:
        blobs.append(raw)  # not JSONL; treat whole file as text
    return blobs

def norm(x):
    if isinstance(x,str): return html.unescape(x).strip()
    if isinstance(x,list): return [norm(i) for i in x]
    if isinstance(x,dict): return {k:norm(v) for k,v in x.items()}
    return x

def listify(v):
    """Normalize fields that may come back as str or list -> list of strings."""
    if v is None: return []
    if isinstance(v,list): return [str(i) for i in v]
    return [str(v)]

out=[]; missing=[]
for slug,aid in ids.items():
    path=f'{TASKS}/{aid}.output'
    if not os.path.exists(path): missing.append((slug,'no file')); continue
    allc=[]
    for blob in collect_text(path):
        allc.extend(candidates_from_text(blob))
    d=allc[-1] if allc else None   # last real (non-skeleton) brief = the agent's answer
    if not d: missing.append((slug,'no json')); continue
    d=norm(d); d['slug']=slug
    # normalize whats_growing/shrinking to strings; recent_developments/sources/major_players/themes to lists
    for f in ('whats_growing','whats_shrinking'):
        if isinstance(d.get(f),list): d[f]="; ".join(d[f])
    for f in ('major_players','themes','recent_developments','sources'):
        d[f]=listify(d.get(f))
    out.append(d)

# preserve pilot order
order=list(ids.keys())
out.sort(key=lambda b: order.index(b['slug']))
json.dump(out, open(f'{ROOT}/briefs_deep.json','w'), ensure_ascii=False, indent=1)
print(f"extracted {len(out)}/{len(ids)}")
if missing: print("MISSING:", missing)
# quick integrity: which have current (non-2022) data_year
for b in out:
    dy=b.get('data_year','?')
    print(f"  {b['slug'][:34]:34s} {b['sector'][:20]:20s} {str(b['key_stats'].get('market_size',''))[:26]:26s} dy={dy}")
