#!/usr/bin/env python3
"""Combine pilot (25) + full-run chunk briefs into one normalized briefs_full.json."""
import json, os, html, glob
ROOT=os.path.dirname(os.path.abspath(__file__))

SECTORS={'Agriculture','Manufacturing','Construction','Retail','Food & Drink','Healthcare',
 'Finance & Insurance','Technology & Digital','Energy & Environment','Business Services',
 'Consumer Services','Media & Entertainment','Transport & Logistics','Real Estate'}

def norm(x):
    if isinstance(x,str): return html.unescape(x).strip()
    if isinstance(x,list): return [norm(i) for i in x]
    if isinstance(x,dict): return {k:norm(v) for k,v in x.items()}
    return x
def listify(v):
    if v is None: return []
    if isinstance(v,list): return [str(i) for i in v]
    return [str(v)]
def strify(v):
    if isinstance(v,list): return "; ".join(str(i) for i in v)
    return v or ""
def _guess(b):
    t=(str(b.get('title',''))+' '+str(b.get('one_liner',''))).lower()
    for kw,sec in [('bank','Finance & Insurance'),('insur','Finance & Insurance'),('loan','Finance & Insurance'),
        ('hospital','Healthcare'),('clinic','Healthcare'),('medical','Healthcare'),('health','Healthcare'),('dental','Healthcare'),
        ('store','Retail'),('restaurant','Food & Drink'),('production','Food & Drink'),('manufactur','Manufacturing'),
        ('construction','Construction'),('trucking','Transport & Logistics'),('airline','Transport & Logistics'),
        ('hotel','Real Estate'),('real estate','Real Estate'),('software','Technology & Digital'),('internet','Technology & Digital'),
        ('power','Energy & Environment'),('consult','Business Services'),('publishing','Media & Entertainment')]:
        if kw in t: return sec
    return 'Business Services'

canon={}
for rl in ('_run200.json','_run300.json'):
    p=f'{ROOT}/{rl}'
    if os.path.exists(p):
        for it in json.load(open(p)): canon[it['slug']]=it['title']
sources=['briefs_deep.json','briefs_full_1.json','briefs_full_2.json','briefs_full_3.json','briefs_full_R.json',
         'briefs_r2_1.json','briefs_r2_2.json','briefs_r2_3.json','briefs_r2_4.json','briefs_r2_5.json','briefs_r2_R.json',
         'briefs_r3_1.json','briefs_r3_2.json','briefs_r3_3.json','briefs_r3_4.json','briefs_r3_5.json','briefs_r3_R.json',
         'briefs_r3_batch__run300_next3_full.json',
         'briefs_r3_batch__run300_0_150.json','briefs_r3_batch__run300_150_150.json',
         'briefs_r3_batch__run300_next_0_150.json','briefs_r3_batch__run300_next_150_150.json',
         'briefs_r3_batch__run300_next2_0_150.json','briefs_r3_batch__run300_next2_150_150.json']
sources += sorted(os.path.basename(p) for p in glob.glob(f'{ROOT}/briefs_r3_batch__*.json'))
sources = list(dict.fromkeys(sources))
seen={}; order=[]
for f in sources:
    p=f'{ROOT}/{f}'
    if not os.path.exists(p): print("skip (missing):",f); continue
    for b in json.load(open(p)):
        if not isinstance(b, dict):
            continue
        b=norm(b); s=b.get('slug')
        if not s or s in seen: continue
        if s in canon: b['title']=canon[s]   # clean canonical display title
        # normalize fields
        b['whats_growing']=strify(b.get('whats_growing'))
        b['whats_shrinking']=strify(b.get('whats_shrinking'))
        for k in ('major_players','themes','recent_developments','sources'):
            b[k]=listify(b.get(k))
        ks=b.get('key_stats') or {}
        for k in ('market_size','growth','businesses','employees','profit_margin','concentration'):
            ks.setdefault(k,'n/a')
        b['key_stats']=ks
        b.setdefault('baseline_2022',{})
        b.setdefault('data_year','2025-2026')
        b.setdefault('overview',''); b.setdefault('current_dynamics',b.get('overview',''))
        b.setdefault('outlook',''); b.setdefault('how_it_makes_money',''); b.setdefault('cost_structure','')
        b.setdefault('one_liner',''); b.setdefault('one_sentence','')
        # clamp sector to known set (some deep briefs used odd sector strings)
        if b.get('sector') not in SECTORS:
            sec=str(b.get('sector','')).split('/')[0].split(' - ')[0].strip()
            b['sector']= sec if sec in SECTORS else _guess(b)
        seen[s]=b; order.append(s)

out=[seen[s] for s in order]
json.dump(out, open(f'{ROOT}/briefs_full.json','w'), ensure_ascii=False, indent=1)
from collections import Counter
c=Counter(b['sector'] for b in out)
print("combined:",len(out),"industries")
for s,n in c.most_common(): print(f"  {n:3d} {s}")
bad=[b['slug'] for b in out if b['sector'] not in SECTORS]
if bad: print("NON-STANDARD sectors:",bad)
