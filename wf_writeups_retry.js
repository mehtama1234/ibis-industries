export const meta = {
  name: 'forces-writeups-retry',
  description: 'Write all subforce pages across the 14 data-grounded force collections (evidence-grounded)',
  phases: [{ title: 'Write' }],
}
const SPECS = [{"slug": "hospitality-wages", "title": "The hospitality wage spiral", "group": "C \u00b7 Moving things & serving people", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-labor-squeeze__hospitality-wages.txt", "cap": false, "force": "the-labor-squeeze", "ftitle": "The Labor Squeeze", "sig": "Workers got scarce \u2014 wages spiral, the trades can't fill the gap, and whoever can automate or pay up wins while everyone else eats the margin hit."}, {"slug": "dining-bifurcation", "title": "Dining bifurcates", "group": "C \u00b7 Eating & staying out", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-hollow-middle__dining-bifurcation.txt", "cap": false, "force": "the-hollow-middle", "ftitle": "The Hollow Middle", "sig": "The middle market collapses \u2014 shoppers split into premium and value, and anyone stuck selling undifferentiated mid-tier goods gets squeezed from both sides."}, {"slug": "the-compute-super-cycle", "title": "The compute super-cycle", "group": "E \u00b7 The big picture", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-compute-super-cycle__the-compute-super-cycle.txt", "cap": true, "force": "the-compute-super-cycle", "ftitle": "The Compute Super-Cycle", "sig": "AI's hunger for power is reshaping the grid and everything plugged into it \u2014 whoever has electricity, land, and cooling near the data centers wins a once-in-a-generation buildout."}, {"slug": "wall-street-machine", "title": "The Wall Street machine", "group": "A \u00b7 The core banks consolidate", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/money-gets-unbundled__wall-street-machine.txt", "cap": false, "force": "money-gets-unbundled", "ftitle": "Money Gets Unbundled", "sig": "Banking leaves the banks \u2014 it's embedded in apps, cards, and platforms \u2014 and scale, data, and the rails win while regional players and middlemen get squeezed."}, {"slug": "the-ev-transition", "title": "The EV transition & legacy parts", "group": "A \u00b7 The auto reordering", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/atoms-strike-back__the-ev-transition.txt", "cap": false, "force": "atoms-strike-back", "ftitle": "Atoms Strike Back", "sig": "Trade war and tariffs force reshoring, nearshoring, and inventory hoarding \u2014 physical supply chains get expensive and political, and whoever moves fastest to nearshore wins."}];
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
  return `You are writing ONE page of a plain-English collection titled "${s.ftitle}". The collection's thesis: ${s.sig}\n\n`+
  `This page is "${s.title}" (${s.group}).${cap}\n\n`+
  `Read your evidence pack (real 2025-2026 US industry data we researched) at this local file and BASE THE PAGE ENTIRELY ON IT:\n${s.pack}\n\n`+
  `VOICE: plain, everyday English. Short sentences. No jargon, no clichés, no hype. Explain like a smart friend. Be RICH and detailed — write 3-4 full paragraphs in what_changed and give 5-8 dated data facts. Use the REAL numbers from the pack, each WITH its year. Frame it as: what did this force make scarce, cheap, risky, or newly valuable here? Then who wins and who gets squeezed. Be concrete and specific to the named industries — never generic. Do NOT use the Agent tool, web search, or sub-agents. Return ONLY the JSON.`;
}
phase('Write')
const out = await parallel(SPECS.map(s => () =>
  agent(prompt(s), { label: `${s.force}:${s.slug}`, phase:'Write', schema: SCHEMA })
    .then(r => r ? { ...r, slug:s.slug, force:s.force, group:s.group, nav_title:s.title, cap:s.cap } : null)))
return out.filter(Boolean)
