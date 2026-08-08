import json, os
from forces_config_t2 import FORCES
ROOT=os.path.dirname(os.path.abspath(__file__))
briefs={b['slug']:b for b in json.load(open(f'{ROOT}/briefs_full.json'))}
os.makedirs(f'{ROOT}/_packs',exist_ok=True)
def pack_text(force, t, angle, ev, cap):
    L=[f"FORCE: {force['title']} — {force['signature']}",f"THIS SUBFORCE: {t}",f"ANGLE: {angle}",""]
    if cap: L.append("(CAPSTONE — synthesize across the whole force.)")
    L.append("EVIDENCE (real 2025-2026 US industry data; use these numbers, each dated):")
    for e in ev:
        b=briefs[e]; ks=b['key_stats']
        L.append(f"\n### {b['title']} ({b['sector']})")
        L.append(f"- Market size: {ks.get('market_size','n/a')} | growth: {ks.get('growth','n/a')} | margin: {ks.get('profit_margin','n/a')} | businesses: {ks.get('businesses','n/a')} | employees: {ks.get('employees','n/a')}")
        L.append(f"- 2022 baseline: {(b.get('baseline_2022') or {}).get('market_size','n/a')}")
        L.append(f"- Takeaway: {b.get('one_sentence','')}")
        L.append(f"- Current dynamics: {b.get('current_dynamics','')[:1100]}")
        rd=b.get('recent_developments',[])[:4]
        if rd: L.append("- Recent: "+" | ".join(rd))
    return "\n".join(L)
all_specs=[]
for force in FORCES:
    specs=[]; newgroups={}
    for grp,subs in force['groups'].items():
        kept=[]
        for (slug,title,ev,angle) in subs:
            avail=[e for e in ev.split() if e in briefs]
            cap = slug==force['slug']
            if not avail and not cap: continue
            if cap and not avail:  # capstone: give it a few from the force
                avail=[e for e in briefs if False][:0] or [s['ev'][0] for s in [] ]
            if not avail: continue
            pf=f"{ROOT}/_packs/{force['slug']}__{slug}.txt"
            open(pf,'w').write(pack_text(force,title,angle,avail,cap))
            spec={"slug":slug,"title":title,"group":grp,"pack":pf,"is_capstone":cap,"angle":angle}
            specs.append(spec); kept.append(spec)
            all_specs.append({**spec,"force":force['slug']})
    json.dump({"force":force,"specs":specs}, open(f'{ROOT}/_forcebuild_{force["slug"]}.json','w'), indent=1)
    print(f"  {force['slug']:24s} {len(specs)} subforces")
# flattened workflow
lite=[{"slug":s['slug'],"title":s['title'],"group":s['group'],"pack":s['pack'],"cap":s['is_capstone'],
       "force":s['force'],"ftitle":next(f['title'] for f in FORCES if f['slug']==s['force']),
       "sig":next(f['signature'] for f in FORCES if f['slug']==s['force'])} for s in all_specs]
tmpl=open(f'{ROOT}/wf_all_writeups.js').read()
a=tmpl.index('const SPECS = '); b=tmpl.index('];',a)+2
new=tmpl[:a]+'const SPECS = '+json.dumps(lite)+';'+tmpl[b:]
new=new.replace("name: 'forces-writeups-all'","name: 'forces-writeups-t2'")
open(f'{ROOT}/wf_t2_writeups.js','w').write(new)
print("total new subforces:",len(all_specs))
