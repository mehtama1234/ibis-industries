import json, sys, html

def clean(x):
    if isinstance(x,str): return html.unescape(x)
    if isinstance(x,list): return [clean(i) for i in x]
    if isinstance(x,dict): return {k:clean(v) for k,v in x.items()}
    return x

def find_briefs(obj):
    """Return the first list of brief-dicts found anywhere in obj."""
    if isinstance(obj,list):
        if obj and isinstance(obj[0],dict) and 'title' in obj[0] and 'one_sentence' in obj[0]:
            return obj
        for v in obj:
            r=find_briefs(v)
            if r: return r
    elif isinstance(obj,dict):
        for v in obj.values():
            r=find_briefs(v)
            if r: return r
    return None
if __name__=='__main__':
    if len(sys.argv) < 3:
        raise SystemExit("Usage: python3 harvest_wf.py <workflow_output> <out_json> [n] [start] [runfile]")

    path,out=sys.argv[1],sys.argv[2]
    top=json.loads(open(path,encoding='utf-8',errors='replace').read())
    print("top-level keys:", list(top.keys()) if isinstance(top,dict) else type(top).__name__)
    arr=find_briefs(top)
    arr=[clean(b) for b in arr]
    json.dump(arr,open(out,'w'),ensure_ascii=False,indent=1)
    print("harvested",len(arr),"->",out)
    print("slugs sample:",[b['slug'] for b in arr[:6]])

    if len(sys.argv) >= 5:
        n=int(sys.argv[3]); start=int(sys.argv[4])
        runfile = sys.argv[5] if len(sys.argv) > 5 else '_run200.json'
        try:
            items=json.load(open(runfile))[start:start+n]
        except FileNotFoundError:
            print("runfile missing:", runfile)
            raise
        got={b.get('slug') for b in arr}
        miss=[it['slug'] for it in items if it['slug'] not in got]
        print(f"MISSING ({len(miss)}):",miss)
    else:
        # Backward-compatibility: no completion check requested, just harvest the output list.
        pass
