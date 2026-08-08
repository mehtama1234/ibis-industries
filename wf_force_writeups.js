export const meta = {
  name: 'ai-rewiring-writeups',
  description: 'Write the 13 plain-English subforce pages for The AI Rewiring collection (evidence-grounded)',
  phases: [{ title: 'Write' }],
}
const SPECS = [{"slug": "design-and-the-web", "title": "Design & the web", "group": "A \u00b7 Creative & knowledge work gets automated", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__design-and-the-web.txt", "cap": false}, {"slug": "video-and-content", "title": "Video & content", "group": "A \u00b7 Creative & knowledge work gets automated", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__video-and-content.txt", "cap": false}, {"slug": "words-and-publishing", "title": "Words & publishing", "group": "A \u00b7 Creative & knowledge work gets automated", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__words-and-publishing.txt", "cap": false}, {"slug": "accounting-and-audit", "title": "Accounting & audit", "group": "B \u00b7 The back office thins out", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__accounting-and-audit.txt", "cap": false}, {"slug": "insurance-claims", "title": "Insurance claims & broking", "group": "B \u00b7 The back office thins out", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__insurance-claims.txt", "cap": false}, {"slug": "law-and-consulting", "title": "Law & consulting", "group": "B \u00b7 The back office thins out", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__law-and-consulting.txt", "cap": false}, {"slug": "medical-diagnostics", "title": "Medical diagnostics", "group": "C \u00b7 Even diagnosis & advice", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__medical-diagnostics.txt", "cap": false}, {"slug": "money-and-advice", "title": "Money & advice", "group": "C \u00b7 Even diagnosis & advice", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__money-and-advice.txt", "cap": false}, {"slug": "education-and-credentials", "title": "Education & credentials", "group": "C \u00b7 Even diagnosis & advice", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__education-and-credentials.txt", "cap": false}, {"slug": "the-deploy-dividend", "title": "The deploy dividend", "group": "D \u00b7 The new scarcities", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__the-deploy-dividend.txt", "cap": false}, {"slug": "the-human-premium", "title": "The human premium", "group": "D \u00b7 The new scarcities", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__the-human-premium.txt", "cap": false}, {"slug": "the-junior-collapse", "title": "The junior-role collapse", "group": "D \u00b7 The new scarcities", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__the-junior-collapse.txt", "cap": false}, {"slug": "the-ai-rewiring", "title": "The AI rewiring", "group": "E \u00b7 The big picture", "pack": "/home/manishmehta/ui-projects/ibis-industries/_packs/the-ai-rewiring__the-ai-rewiring.txt", "cap": true}];
const FORCE_TITLE = "The AI Rewiring";
const SIGNATURE = "AI automates the routine cognitive work \u2014 and the value moves to whoever deploys it, owns the data, or sells the judgment a machine can't.";
const SCHEMA = {
  type:'object',
  required:['title','dek','lede','what_changed','facts','evidence','win','lose','worry','one_sentence'],
  properties:{
    title:{type:'string',description:'punchy plain-English page title'},
    dek:{type:'string',description:'one-sentence italic subtitle'},
    lede:{type:'string',description:'opening paragraph, plain English, 2-3 sentences'},
    what_changed:{type:'string',description:'1-2 paragraphs: what AI made scarce, cheap, risky, or newly valuable in this corner. Plain English, short sentences.'},
    facts:{type:'array',items:{type:'object',required:['num','txt'],properties:{num:{type:'string',description:'short stat e.g. "$61B" or "-3.1%/yr"'},warn:{type:'boolean'},txt:{type:'string',description:'the dated fact, grounded in the pack'}}}},
    evidence:{type:'array',items:{type:'string'},description:'2-4 bullets, each naming a specific industry and a real 2025-2026 number from the pack'},
    win:{type:'string',description:'who rides it, 1-2 sentences'},
    lose:{type:'string',description:'who is squeezed, 1-2 sentences'},
    worry:{type:'string',description:'the single biggest risk, 1-2 sentences'},
    one_sentence:{type:'string',description:'the one-sentence takeaway'}
  }
}
function prompt(s){
  const capNote = s.cap ? ' This is the CAPSTONE page that synthesizes the whole collection — make what_changed a 2-3 paragraph synthesis across all the corners of the economy, make win/lose the overall winners vs losers, and make worry the single biggest tension.' : '';
  return `You are writing ONE page of a plain-English collection titled "${FORCE_TITLE}". The collection's thesis: ${SIGNATURE}\n\n`+
  `This page is "${s.title}" (${s.group}).${capNote}\n\n`+
  `Read your evidence pack (real 2025-2026 US industry data we researched) at this local file and BASE THE PAGE ON IT:\n${s.pack}\n\n`+
  `VOICE: plain, everyday English. Short sentences. No jargon, no clichés, no hype. Explain like a smart friend. Use REAL numbers from the pack, each WITH its year. Frame it as: what did this force make scarce, cheap, risky, or newly valuable? Then who wins and who gets squeezed. Be concrete and specific to the named industries — never generic.\n\n`+
  `Do NOT use the Agent tool or spawn sub-agents. Return ONLY the JSON.`;
}
phase('Write')
const out = await parallel(SPECS.map(s => () =>
  agent(prompt(s), { label: `write:${s.slug}`, phase:'Write', schema: SCHEMA })
    .then(r => r ? { ...r, slug:s.slug, group:s.group, nav_title:s.title, cap:s.cap } : null)))
return out.filter(Boolean)
