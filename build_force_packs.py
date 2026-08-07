#!/usr/bin/env python3
"""For all 14 forces: build evidence packs + per-force build spec, and emit one flattened write-up workflow."""
import json, os
from forces_config import FORCES
ROOT=os.path.dirname(os.path.abspath(__file__))
briefs={b['slug']:b for b in json.load(open(f'{ROOT}/briefs_full.json'))}
os.makedirs(f'{ROOT}/_packs',exist_ok=True)

def pack_text(force, sub_title, angle, ev, cap):
    L=[f"FORCE: {force['title']} — {force['signature']}",
       f"THIS SUBFORCE: {sub_title}", f"ANGLE: {angle}",""]
    if cap: L.append("(This is the CAPSTONE page — synthesize across the whole force.)")
    L.append("EVIDENCE (real 2025-2026 US industry data we researched; use these numbers, each dated):")
    for e in ev.split():
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
    specs=[]
    for grp,subs in force['groups'].items():
        for (slug,title,ev,angle) in subs:
            cap = slug==force['slug']
            pf=f"{ROOT}/_packs/{force['slug']}__{slug}.txt"
            open(pf,'w').write(pack_text(force,title,angle,ev,cap))
            spec={"slug":slug,"title":title,"group":grp,"pack":pf,"is_capstone":cap,"angle":angle}
            specs.append(spec)
            all_specs.append({**spec,"force":force['slug']})
    json.dump({"force":force,"specs":specs}, open(f'{ROOT}/_forcebuild_{force["slug"]}.json','w'), indent=1)

# flattened workflow over all subforces
lite=[{"slug":s['slug'],"title":s['title'],"group":s['group'],"pack":s['pack'],"cap":s['is_capstone'],
       "force":s['force'],"ftitle":next(f['title'] for f in FORCES if f['slug']==s['force']),
       "sig":next(f['signature'] for f in FORCES if f['slug']==s['force'])} for s in all_specs]
tmpl='''export const meta = {
  name: 'forces-writeups-all',
  description: 'Write all subforce pages across the 14 data-grounded force collections (Haiku, evidence-grounded)',
  phases: [{ title: 'Write' }],
}
const SPECS = %SPECS%;
const SCHEMA = {
  type:'object',
  required:['title','dek','lede','what_changed','facts','evidence','win','lose','worry','one_sentence'],
  properties:{
    title:{type:'string'}, dek:{type:'string',description:'one-sentence subtitle'},
    lede:{type:'string',description:'opening paragraph, plain English, 2-3 sentences'},
    what_changed:{type:'string',description:'3 to 4 SUBSTANTIAL paragraphs, plain English, dense with the real dated numbers from the pack: what this force made scarce, cheap, risky, or newly valuable in this corner.'},
    facts:{type:'array',description:'5 to 8 data callouts',items:{type:'object',required:['num','txt'],properties:{num:{type:'string'},warn:{type:'boolean'},txt:{type:'string',description:'the dated fact, grounded in the pack'}}}},
    evidence:{type:'array',items:{type:'string'},description:'3-5 bullets, each naming a specific industry and a real 2025-2026 number from the pack'},
    win:{type:'string',description:'who rides it, 2-3 sentences'},
    lose:{type:'string',description:'who is squeezed, 2-3 sentences'},
    worry:{type:'string',description:'the single biggest risk, 2-3 sentences'},
    one_sentence:{type:'string'}
  }
}
function prompt(s){
  const cap = s.cap ? ' This is the CAPSTONE page — make what_changed a 3-4 paragraph synthesis across the whole force, make win/lose the overall winners vs losers, and worry the single biggest tension.' : '';
  return `You are writing ONE page of a plain-English collection titled "${s.ftitle}". The collection's thesis: ${s.sig}\\n\\n`+
  `This page is "${s.title}" (${s.group}).${cap}\\n\\n`+
  `Read your evidence pack (real 2025-2026 US industry data we researched) at this local file and BASE THE PAGE ENTIRELY ON IT:\\n${s.pack}\\n\\n`+
  `VOICE: plain, everyday English. Short sentences. No jargon, no clichés, no hype. Explain like a smart friend. Be RICH and detailed — write 3-4 full paragraphs in what_changed and give 5-8 dated data facts. Use the REAL numbers from the pack, each WITH its year. Frame it as: what did this force make scarce, cheap, risky, or newly valuable here? Then who wins and who gets squeezed. Be concrete and specific to the named industries — never generic. Do NOT use the Agent tool, web search, or sub-agents. Return ONLY the JSON.`;
}
phase('Write')
const out = await parallel(SPECS.map(s => () =>
  agent(prompt(s), { label: `${s.force}:${s.slug}`, phase:'Write', schema: SCHEMA, model:'haiku' })
    .then(r => r ? { ...r, slug:s.slug, force:s.force, group:s.group, nav_title:s.title, cap:s.cap } : null)))
return out.filter(Boolean)
'''
open(f'{ROOT}/wf_all_writeups.js','w').write(tmpl.replace('%SPECS%',json.dumps(lite)))
print(f"built {len(all_specs)} packs across {len(FORCES)} forces; wf_all_writeups.js ready ({len(lite)} agents)")
