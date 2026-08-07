import json,html,re,sys,os
from collections import defaultdict
def deent(s):
    s=html.unescape(str(s or '')); s=re.sub(r'</?[ibem]>','',s); return s.strip().strip('*_').strip()
def clean(x):
    if isinstance(x,str): return deent(x)
    if isinstance(x,list): return [clean(i) for i in x]
    if isinstance(x,dict): return {k:clean(v) for k,v in x.items()}
    return x
def find(o):
    if isinstance(o,list):
        if o and isinstance(o[0],dict) and 'title' in o[0] and 'one_sentence' in o[0] and 'lede' in o[0]: return o
        for v in o:
            r=find(v)
            if r:return r
    elif isinstance(o,dict):
        for v in o.values():
            r=find(v)
            if r:return r
    return None
top=json.loads(open(sys.argv[1]).read())
arr=[clean(w) for w in (find(top) or [])]
byforce=defaultdict(list)
for w in arr: byforce[w.get('force','?')].append(w)
for f,ws in byforce.items():
    json.dump(ws, open(f'_writeups_{f}.json','w'), ensure_ascii=False, indent=1)
print("total writeups:",len(arr))
for f in sorted(byforce): print(f"  {len(byforce[f]):2d}  {f}")
