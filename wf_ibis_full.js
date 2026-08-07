export const meta = {
  name: 'ibis-deep-current',
  description: 'Deep 2025-2026 web-researched plain-English briefs for a batch of US IBIS industries (Haiku)',
  phases: [{ title: 'Research', detail: 'one Haiku agent per industry: read 2022 baseline + web-research current' }],
}

// args = { items: [ { title, slug, file } ... ] }
const items = (args && args.items) || []

const SCHEMA = {
  type: 'object',
  required: ['title','sector','one_liner','overview','key_stats','current_dynamics','one_sentence'],
  properties: {
    title: { type: 'string' },
    sector: { type: 'string', description: 'ONE of: Agriculture | Manufacturing | Construction | Retail | Food & Drink | Healthcare | Finance & Insurance | Technology & Digital | Energy & Environment | Business Services | Consumer Services | Media & Entertainment | Transport & Logistics | Real Estate' },
    one_liner: { type: 'string' },
    overview: { type: 'string', description: '3-4 plain sentences on the CURRENT 2025-2026 state' },
    key_stats: {
      type: 'object',
      required: ['market_size','growth'],
      properties: {
        market_size: { type: 'string', description: 'latest $ WITH year' },
        growth: { type: 'string' }, businesses: { type: 'string' }, employees: { type: 'string' },
        profit_margin: { type: 'string' }, concentration: { type: 'string' },
      },
    },
    baseline_2022: {
      type: 'object', required: ['market_size','growth'],
      properties: { market_size: { type: 'string' }, growth: { type: 'string' } },
    },
    how_it_makes_money: { type: 'string' },
    cost_structure: { type: 'string' },
    major_players: { type: 'array', items: { type: 'string' } },
    current_dynamics: { type: 'string', description: '4-6 plain sentences of real depth on what is happening now' },
    whats_growing: { type: 'string' },
    whats_shrinking: { type: 'string' },
    recent_developments: { type: 'array', items: { type: 'string' }, description: '3-6 dated 2023-2026 events' },
    outlook: { type: 'string' },
    themes: { type: 'array', items: { type: 'string' }, description: '4-6 short reusable force tags' },
    data_year: { type: 'string' },
    sources: { type: 'array', items: { type: 'string' } },
    one_sentence: { type: 'string' },
  },
}

function prompt(it) {
  return (
`Produce a CURRENT (2025-2026) plain-English brief on the US "${it.title}" industry, with real depth on its present dynamics.

TWO INPUTS:
1) A 2022 IBISWorld report (baseline only) at this local file — read it for structure and the 2022 figures: ${it.file}
2) THE WEB — you MUST use your WebSearch and WebFetch tools to research the CURRENT state (2024, 2025, 2026): latest market size and growth, recent company moves / M&A / bankruptcies, the main forces disrupting or reshaping the industry right now (technology, regulation, consumer shifts, macro/tariffs), current competitive dynamics, and the 2025-2026 outlook. Attach a YEAR to every number. If a search returns nothing useful, use your own most recent knowledge and label the year — but genuinely try the web first.

Write in plain, everyday English: short sentences, no jargon, no clichés. Every number must carry its year. Do NOT present 2022 figures as current. Put the 2022 report's revenue and 5-yr growth in baseline_2022. Do NOT spawn sub-agents or use the deep-research skill.`
  )
}

phase('Research')
const briefs = await parallel(items.map(it => () =>
  agent(prompt(it), { label: `ibis:${it.slug}`, phase: 'Research', schema: SCHEMA, model: 'haiku' })
    .then(b => (b ? { ...b, slug: it.slug } : null))
))
return briefs.filter(Boolean)
