#!/usr/bin/env python3
"""Build a detailed American themes layer on top of the force and company corpus."""

from __future__ import annotations

import html
import json
import os
import re
from pathlib import Path

from forces_config import FORCES

ROOT = Path(__file__).resolve().parent
JSON_OUT = ROOT / "american_themes_taxonomy.json"
HTML_OUT = ROOT / "american-themes.html"
THEMES_DIR = ROOT / "themes"


THEMES = [
    {
        "slug": "barbelled-consumer-america",
        "title": "Barbelled Consumer America",
        "lens": "Consumer",
        "thesis": "The old middle of American consumption keeps losing coherence. Households polarize between ruthless value-seeking and selective premium spend, while undifferentiated mid-market operators get squeezed from both sides.",
        "why_now": "Inflation fatigue, platform comparison shopping, private-label quality gains, and tighter household budgeting have turned consumer demand into a barbell rather than a mass middle.",
        "forces": ["the-hollow-middle", "the-channel-shift", "the-margin-vise"],
        "crosscuts": ["consumer-bifurcation", "capital-and-scale"],
        "questions": [
            "Is this category a value machine, a premium refuge, or dead-center middle?",
            "What actually gives the customer permission to keep paying up?",
            "Does the operator own demand, or merely rent traffic from a platform?",
        ],
        "subthemes": [
            {
                "slug": "value-machines",
                "title": "Value Machines Win the Weekly Basket",
                "summary": "Traffic concentrates around operators that make basic household shopping feel reliably cheaper, faster, and less cognitively expensive.",
                "microthemes": [
                    "bulk purchasing as household insurance",
                    "membership and loyalty as value signaling",
                    "private label as margin plus trust",
                    "trip consolidation into fewer higher-yield baskets",
                ],
                "forces": ["the-hollow-middle", "the-channel-shift"],
                "industries": [
                    "discount-department-stores",
                    "warehouse-clubs-and-supercenters-in-the-us",
                    "grocery-stores-in-the-us",
                    "auto-parts-stores-in-the-us",
                ],
                "companies": ["walmart", "costco", "kroger", "amazon"],
                "operator_implications": [
                    "Winning formats remove search friction and visibly defend value.",
                    "Scale buying power matters more than merchant taste alone.",
                    "The basket has to feel prudent before it feels exciting.",
                ],
            },
            {
                "slug": "premium-refuges",
                "title": "Premium Refuges Still Hold Price",
                "summary": "Some categories still support premium spend, but only where status, trust, aesthetics, or specialized quality remain legible to the buyer.",
                "microthemes": [
                    "premium as self-permission rather than simple indulgence",
                    "quality signaling through brand, fit, and finish",
                    "small luxuries surviving inside stretched budgets",
                    "premium niches outperforming broad mid-tier assortments",
                ],
                "forces": ["the-hollow-middle", "the-margin-vise"],
                "industries": [
                    "beauty-salons-in-the-us",
                    "jewelry-stores-in-the-us",
                    "cosmetics-and-beauty-products-manufacturing-in-the-us",
                    "wineries-in-the-us",
                ],
                "companies": ["ulta-beauty", "williams-sonoma", "lululemon", "tiffany-and"],
                "operator_implications": [
                    "Premium only works when the customer can articulate why the product is better.",
                    "Operators need visible differentiation, not generic upscale positioning.",
                    "Mix quality matters more than raw volume growth.",
                ],
            },
            {
                "slug": "mid-market-erosion",
                "title": "Mid-Market Erosion Becomes Structural",
                "summary": "Mid-tier stores and brands lose both emotional distinctiveness and economic room as shoppers compare prices instantly and reserve discretionary spend for categories that feel more necessary or more special.",
                "microthemes": [
                    "department-store logic losing the category anchor role",
                    "mid-tier apparel and home formats getting trapped in promotion",
                    "brand sameness reducing willingness to pay",
                    "channel fragmentation making mall-era positioning weaker",
                ],
                "forces": ["the-hollow-middle", "the-channel-shift", "the-margin-vise"],
                "industries": [
                    "department-stores-in-the-us",
                    "womens-clothing-stores-in-the-us",
                    "furniture-stores-in-the-us",
                    "consumer-electronics-stores-in-the-us",
                ],
                "companies": ["target", "nordstrom", "gamestop", "under-armour"],
                "operator_implications": [
                    "Mid-tier operators need a hard pivot toward value, service, or curation.",
                    "Promotion without distinctiveness becomes a slow margin bleed.",
                    "Generic assortment is increasingly nonviable.",
                ],
            },
            {
                "slug": "convenience-as-spend-logic",
                "title": "Convenience Becomes Its Own Pricing Layer",
                "summary": "Households will still pay for time savings, reduced hassle, and predictable fulfillment even when they resist broad-based price increases elsewhere.",
                "microthemes": [
                    "fast delivery as default expectation",
                    "subscription and replenishment models reducing decision fatigue",
                    "pickup and omnichannel logistics as habit infrastructure",
                    "convenience premiums surviving inside otherwise price-sensitive behavior",
                ],
                "forces": ["the-channel-shift", "the-margin-vise"],
                "industries": [
                    "e-commerce-and-online-auctions-in-the-us",
                    "meal-kit-delivery-services",
                    "pharmacies-and-drug-stores-in-the-us",
                    "coffee-and-snack-shops-in-the-us",
                ],
                "companies": ["amazon", "doordash", "cvs-health", "panera-bread"],
                "operator_implications": [
                    "Convenience must be operationally real, not just a marketing claim.",
                    "Fulfillment reliability becomes part of product quality.",
                    "Operators should price against time and friction, not just against substitutes.",
                ],
            },
            {
                "slug": "private-label-and-dupes",
                "title": "Private Label and Dupes Legitimize Trade-Down",
                "summary": "Consumers increasingly treat lower-priced alternatives as socially acceptable rather than embarrassing, which weakens the moat of many branded middle-market incumbents.",
                "microthemes": [
                    "private label moving from compromise to smart shopping",
                    "dupe culture spreading from beauty into broad retail behavior",
                    "social media normalizing imitation over heritage loyalty",
                    "retailers using store brands as both value signal and margin tool",
                ],
                "forces": ["the-hollow-middle", "the-channel-shift"],
                "industries": [
                    "health-stores-in-the-us",
                    "cosmetics-and-beauty-products-manufacturing-in-the-us",
                    "grocery-stores-in-the-us",
                    "department-stores-in-the-us",
                ],
                "companies": ["walmart", "target", "ulta-beauty", "procter-and-gamble"],
                "operator_implications": [
                    "Brand owners need genuine product or distribution advantage to outrun imitation.",
                    "Retailers can use own-brand lines to hold both traffic and gross margin.",
                    "The consumer no longer needs to hide the trade-down decision.",
                ],
            },
        ],
    },
    {
        "slug": "wellness-recodes-daily-life",
        "title": "Wellness Recodes Daily Life",
        "lens": "Cultural / Consumer",
        "thesis": "Health behavior is no longer a niche vertical. It is becoming a general operating system for food, drink, beauty, self-presentation, and everyday social decisions.",
        "why_now": "GLP-1 adoption, sober-curious norms, functional consumption, and constant biometric self-monitoring are turning wellness from a preference into a mass behavioral filter.",
        "forces": ["the-health-reckoning", "the-hollow-middle", "the-channel-shift"],
        "crosscuts": ["consumer-bifurcation", "demographic-aging"],
        "questions": [
            "Does this category align with health, fight it, or need to be reformulated around it?",
            "Is wellness a real demand engine here or just branding language?",
            "Where does identity change faster than formal regulation?",
        ],
        "subthemes": [
            {
                "slug": "glp1-appetite-reset",
                "title": "GLP-1 Resets Appetite and Portion Economics",
                "summary": "Reduced appetite and changing food routines ripple across snacks, fast food, weight management, and consumer packaged goods.",
                "microthemes": [
                    "smaller portion logic reaching mainstream households",
                    "traditional weight-loss services being rewritten by pharma",
                    "calorie-dense impulse categories losing easy volume",
                    "food brands rethinking satiety, protein, and nutrient density",
                ],
                "forces": ["the-health-reckoning", "the-margin-vise"],
                "industries": [
                    "weight-loss-services-in-the-us",
                    "fast-food-restaurants-in-the-us",
                    "candy-production-in-the-us",
                    "cookie-cracker-and-pasta-production-in-the-us",
                ],
                "companies": ["jenny-craig", "mcdonald-s", "the-coca-cola", "kraft-heinz"],
                "operator_implications": [
                    "Volume assumptions based on old appetite patterns are less reliable.",
                    "Protein, satiety, and better-for-you positioning become more strategic.",
                    "Pharma is now a consumer-sector force, not just a healthcare one.",
                ],
            },
            {
                "slug": "sober-socializing",
                "title": "Sober Socializing Changes Nightlife and Beverage Mix",
                "summary": "Younger consumers are moderating alcohol more openly, which shifts venue economics and creates room for nonalcoholic, functional, and premium alternatives.",
                "microthemes": [
                    "drinking less without abandoning social ritual",
                    "venue formats adapting around lower alcohol intensity",
                    "nonalcoholic options becoming mandatory, not token",
                    "premium spirits losing some insulation against moderation",
                ],
                "forces": ["the-health-reckoning", "the-experience-economy"],
                "industries": [
                    "bars-and-nightclubs-in-the-us",
                    "breweries-in-the-us",
                    "distilleries-in-the-us",
                    "wine-bars",
                ],
                "companies": ["anheuser-busch-inbev", "panera-bread", "the-coca-cola", "draftkings"],
                "operator_implications": [
                    "Beverage programs need abstention-compatible margin drivers.",
                    "Venues cannot assume alcohol is the default profit center forever.",
                    "Nonalcoholic menus should be built as products, not apologies.",
                ],
            },
            {
                "slug": "functional-consumption",
                "title": "Functional Consumption Beats Empty Indulgence",
                "summary": "Shoppers increasingly want food and drink to do something specific: energize, hydrate, recover, sharpen focus, or support long-term health.",
                "microthemes": [
                    "energy and hydration as daily performance categories",
                    "supplement-like branding migrating into mainstream beverages",
                    "protein and gut-health language broadening beyond athletes",
                    "wellness framing becoming a permission structure for premium pricing",
                ],
                "forces": ["the-health-reckoning", "the-hollow-middle"],
                "industries": [
                    "energy-drink-production",
                    "juice-production-in-the-us",
                    "health-stores-in-the-us",
                    "coffee-and-snack-shops-in-the-us",
                ],
                "companies": ["the-coca-cola", "haleon", "abbott", "cvs-health"],
                "operator_implications": [
                    "Function can justify premium pricing if the use case is legible.",
                    "Packaging and merchandising need to tell a utility story quickly.",
                    "Operators should design around rituals, not abstract wellness claims.",
                ],
            },
            {
                "slug": "beauty-fitness-health-merge",
                "title": "Beauty, Fitness, and Health Start to Merge",
                "summary": "The line between medical improvement, cosmetic improvement, and self-optimization keeps fading in both consumer spending and service delivery.",
                "microthemes": [
                    "appearance and health narratives converging",
                    "beauty spend reframed as maintenance rather than indulgence",
                    "med-spa and wellness adjacencies expanding the service stack",
                    "self-tracking habits feeding repeated purchases",
                ],
                "forces": ["the-health-reckoning", "the-graying-market"],
                "industries": [
                    "beauty-salons-in-the-us",
                    "dermatologists",
                    "weight-loss-services-in-the-us",
                    "gyms-and-fitness-centers-in-the-us",
                ],
                "companies": ["ulta-beauty", "abbott", "lyra-health", "jenny-craig"],
                "operator_implications": [
                    "The customer increasingly buys an identity project, not a single service.",
                    "Recurring routines and memberships become more valuable than one-off visits.",
                    "Health-adjacent trust matters even in nominally cosmetic categories.",
                ],
            },
            {
                "slug": "reformulated-indulgence",
                "title": "Indulgence Survives by Being Reformulated",
                "summary": "Consumers still want treats and comfort, but the category increasingly has to defend itself through portion control, cleaner labels, or premium differentiation.",
                "microthemes": [
                    "smaller treats replacing unrestricted volume",
                    "clean-label framing softening category guilt",
                    "premium indulgence surviving where cheap sugar weakens",
                    "legacy brands forced into nutritional repositioning",
                ],
                "forces": ["the-health-reckoning", "the-margin-vise", "the-hollow-middle"],
                "industries": [
                    "ice-cream-production-in-the-us",
                    "candy-production-in-the-us",
                    "dairy-product-production-in-the-us",
                    "chain-restaurants-in-the-us",
                ],
                "companies": ["kraft-heinz", "the-j-m-smucker", "unilever", "mcdonald-s"],
                "operator_implications": [
                    "Indulgence categories need either better ingredients, better story, or better scarcity.",
                    "The old mass-volume snack model looks less secure.",
                    "Treats still sell, but the social justification around them has changed.",
                ],
            },
        ],
    },
    {
        "slug": "experience-status-and-community",
        "title": "Experience, Status, and Community",
        "lens": "Cultural / Social",
        "thesis": "More consumer status is being expressed through participation, memory, aesthetics, and curation rather than through ownership of broad mid-tier goods.",
        "why_now": "Digital saturation, uneven goods affordability, and social signaling through shared experiences have made participation-based spending more culturally central.",
        "forces": ["the-experience-economy", "the-channel-shift", "the-hollow-middle"],
        "crosscuts": ["consumer-bifurcation", "capital-and-scale"],
        "questions": [
            "Is this product really competing with other products, or with experiences?",
            "Where does participation create pricing power that goods cannot?",
            "What turns a venue from generic capacity into cultural scarcity?",
        ],
        "subthemes": [
            {
                "slug": "memory-over-merchandise",
                "title": "Memory Beats Merchandise",
                "summary": "Households still spend discretionary dollars, but a larger share goes toward events, travel, leisure, and social participation instead of incremental objects.",
                "microthemes": [
                    "travel and events as post-purchase social proof",
                    "goods losing to moments in aspirational categories",
                    "identity expressed through doing more than owning",
                    "scarce calendar time becoming part of the value proposition",
                ],
                "forces": ["the-experience-economy", "the-hollow-middle"],
                "industries": [
                    "amusement-parks-in-the-us",
                    "campgrounds-and-rv-parks-in-the-us",
                    "domestic-airlines-in-the-us",
                    "hotels-and-motels-in-the-us",
                ],
                "companies": ["delta-air-lines", "hyatt-hotels", "draftkings", "williams-sonoma"],
                "operator_implications": [
                    "Experience categories win when they generate stories worth retelling.",
                    "Scarcity, novelty, and social shareability matter to pricing power.",
                    "Goods businesses need stronger experiential hooks to compete for discretionary budgets.",
                ],
            },
            {
                "slug": "venue-scarcity",
                "title": "Venue Scarcity Creates Durable Pricing Power",
                "summary": "Well-located, well-programmed physical venues gain leverage because digital life cannot fully substitute for live gathering, entertainment, or symbolic public presence.",
                "microthemes": [
                    "destination venues outperforming generic local capacity",
                    "event programming becoming as important as real estate itself",
                    "ticket, food, beverage, and sponsorship economics interlocking",
                    "physical attendance retaining emotional premium over digital viewing",
                ],
                "forces": ["the-experience-economy", "the-real-estate-reckoning"],
                "industries": [
                    "theme-and-parks",
                    "casino-hotels-in-the-us",
                    "bars-and-nightclubs-in-the-us",
                    "sporting-goods-stores-in-the-us",
                ],
                "companies": ["hyatt-hotels", "draftkings", "mcdonald-s", "dick-s-sporting-goods"],
                "operator_implications": [
                    "Programming and curation can matter more than square footage alone.",
                    "Venue operators need reasons for repeat visitation, not only one-time traffic.",
                    "Real estate becomes stronger when culture keeps refreshing the demand loop.",
                ],
            },
            {
                "slug": "active-aging-outdoors",
                "title": "Active Aging and Outdoor Identity Expand Leisure Demand",
                "summary": "Affluent and healthier older consumers are spending on travel, outdoors, recreation, and experience-heavy leisure rather than retreating from discretionary participation.",
                "microthemes": [
                    "retirees staying active longer",
                    "outdoor gear and travel tied to identity, not only utility",
                    "RV, camping, and destination leisure broadening across age groups",
                    "experience spend sustaining categories linked to longevity and mobility",
                ],
                "forces": ["the-experience-economy", "the-graying-market"],
                "industries": [
                    "campgrounds-and-rv-parks-in-the-us",
                    "hiking-and-outdoor-equipment-stores",
                    "amusement-parks-in-the-us",
                    "sporting-goods-stores-in-the-us",
                ],
                "companies": ["sportsman-s-warehouse", "dick-s-sporting-goods", "hyatt-hotels", "yamaha-motor"],
                "operator_implications": [
                    "Aging does not only redirect spend into care; it also sustains leisure.",
                    "Durable outdoor and recreational brands can benefit from demographic tailwinds.",
                    "The winning offer combines vitality signaling with convenience and safety.",
                ],
            },
            {
                "slug": "retail-as-stage",
                "title": "Retail Has to Become a Stage, Not Just a Shelf",
                "summary": "Physical commerce increasingly survives where the store acts as a discovery environment, service node, or brand theater rather than just a place to transact.",
                "microthemes": [
                    "showroom logic replacing inventory-heavy generalism",
                    "events, classes, and demos creating store relevance",
                    "pickup and service blending with experience functions",
                    "brand theater becoming a defense against platform commoditization",
                ],
                "forces": ["the-channel-shift", "the-experience-economy", "the-hollow-middle"],
                "industries": [
                    "consumer-electronics-stores-in-the-us",
                    "home-improvement-stores-in-the-us",
                    "beauty-salons-in-the-us",
                    "sporting-goods-stores-in-the-us",
                ],
                "companies": ["the-home-depot", "ulta-beauty", "dick-s-sporting-goods", "best-buy"],
                "operator_implications": [
                    "Physical retail should justify a trip, not merely host inventory.",
                    "Service and community are now part of the merchandising strategy.",
                    "Stores that feel interchangeable are easier to displace online.",
                ],
            },
            {
                "slug": "fandom-and-affiliation",
                "title": "Fandom and Affiliation Become Spend Infrastructure",
                "summary": "Consumers increasingly spend into identities built around teams, creators, hobbies, and communities, which creates pockets of unusual resilience and monetization depth.",
                "microthemes": [
                    "shared affiliation deepening willingness to spend",
                    "communities monetized across merchandise, events, and media",
                    "hobby categories acting as durable identity ecosystems",
                    "cultural attachment reducing pure price sensitivity",
                ],
                "forces": ["the-experience-economy", "the-channel-shift"],
                "industries": [
                    "sporting-goods-stores-in-the-us",
                    "video-games-in-the-us",
                    "music-publishing-in-the-us",
                    "craft-supplies-stores-in-the-us",
                ],
                "companies": ["draftkings", "gamestop", "mattel", "hallmark-cards"],
                "operator_implications": [
                    "Affiliation businesses need ongoing ritual and refresh, not just a one-time sale.",
                    "Identity-rich categories can withstand generic commoditization longer.",
                    "Community design is increasingly an economic function.",
                ],
            },
        ],
    },
    {
        "slug": "aging-care-and-the-assistance-economy",
        "title": "Aging, Care, and the Assistance Economy",
        "lens": "Societal / Institutional",
        "thesis": "An older America is creating durable demand across care, insurance, home services, devices, and finance, but labor shortages and payer control determine who actually captures that demand.",
        "why_now": "The largest aging cohort is moving deeper into chronic care years just as caregiving labor, reimbursement generosity, and housing capacity remain constrained.",
        "forces": ["the-graying-market", "the-labor-squeeze", "the-pricing-power-collapse", "the-compliance-tax"],
        "crosscuts": ["demographic-aging", "labor-scarcity"],
        "questions": [
            "Where is demand guaranteed but return capture uncertain?",
            "Which parts of aging are consumer-funded versus payer-gated?",
            "Does this business own care delivery, a bottleneck input, or only a thin reimbursement spread?",
        ],
        "subthemes": [
            {
                "slug": "home-first-aging",
                "title": "Home-First Aging Reorders the Care Stack",
                "summary": "Families and payers increasingly prefer keeping older adults at home, which shifts demand into home care, monitoring, delivery, and support services.",
                "microthemes": [
                    "institutional care delayed until later acuity",
                    "home settings absorbing more clinical and nonclinical tasks",
                    "family logistics becoming part of the care economy",
                    "distributed care models increasing coordination complexity",
                ],
                "forces": ["the-graying-market", "the-labor-squeeze"],
                "industries": [
                    "home-care-providers-in-the-us",
                    "health-and-medical-insurance-in-the-us",
                    "medical-device-manufacturing-in-the-us",
                    "couriers-and-local-delivery-services-in-the-us",
                ],
                "companies": ["humana", "cvs-health", "abbott", "amazon"],
                "operator_implications": [
                    "Home-first care creates recurring demand but heavy coordination burden.",
                    "Businesses that reduce family friction can capture real value.",
                    "Labor-light enablement layers may be more attractive than labor-heavy direct care.",
                ],
            },
            {
                "slug": "senior-housing-bottleneck",
                "title": "Senior Housing Demand Meets Staffing and Capacity Friction",
                "summary": "Senior living remains demand-rich, but beds, staffing, regulation, and wage pressure cap how smoothly the sector can absorb aging demand.",
                "microthemes": [
                    "care intensity increasing inside facilities",
                    "occupancy recovery colliding with staffing scarcity",
                    "institutional operators gaining share over independents",
                    "real estate and operating economics separating more sharply",
                ],
                "forces": ["the-graying-market", "the-labor-squeeze", "the-great-consolidation"],
                "industries": [
                    "residential-senior-care-franchises",
                    "apartment-rental-in-the-us",
                    "commercial-real-estate-in-the-us",
                    "nursing-care-facilities-in-the-us",
                ],
                "companies": ["brookdale-senior-living", "cbre", "humana", "prologis"],
                "operator_implications": [
                    "Care labor and occupancy quality matter more than simple unit count.",
                    "Asset owners and operators may have diverging incentives.",
                    "Consolidation can help, but it does not remove staffing reality.",
                ],
            },
            {
                "slug": "chronic-care-industrialization",
                "title": "Chronic Care Becomes an Industrial Service Chain",
                "summary": "Dialysis, cardio-metabolic care, orthopedic support, diagnostics, and outpatient specialties are scaling into highly managed recurring care systems.",
                "microthemes": [
                    "chronic disease producing recurring procedure and device demand",
                    "outpatient settings capturing more volume",
                    "care pathways standardized into repeatable operating models",
                    "specialized devices and monitoring becoming embedded in long-term care",
                ],
                "forces": ["the-graying-market", "the-pricing-power-collapse"],
                "industries": [
                    "dialysis-centers",
                    "orthopedic-products-manufacturing",
                    "ambulatory-surgery-centers",
                    "cardiologists",
                ],
                "companies": ["zimmer-biomet", "abbott", "labcorp", "cleveland-clinic"],
                "operator_implications": [
                    "These are process businesses as much as clinical ones.",
                    "Scale in procurement, scheduling, and documentation becomes central.",
                    "The margin opportunity often sits beside, not inside, direct care labor.",
                ],
            },
            {
                "slug": "payer-gated-aging",
                "title": "Payers Gatekeep the Aging Economy",
                "summary": "Medicare Advantage, insurers, and reimbursement schedules increasingly decide which aging-demand businesses can convert need into acceptable economics.",
                "microthemes": [
                    "public-private reimbursement rules steering provider behavior",
                    "utilization management becoming a margin determinant",
                    "benefit design reshaping patient flow",
                    "pricing power capped by payer concentration",
                ],
                "forces": ["the-pricing-power-collapse", "the-compliance-tax", "the-graying-market"],
                "industries": [
                    "health-and-medical-insurance-in-the-us",
                    "hmo-providers",
                    "dental-insurance",
                    "home-care-providers-in-the-us",
                ],
                "companies": ["humana", "cvs-health", "unitedhealth-group", "chubb"],
                "operator_implications": [
                    "Demand alone is a weak indicator in payer-shaped sectors.",
                    "Administrative competence can matter as much as bedside competence.",
                    "Winning operators understand coding, reimbursement, and utilization controls deeply.",
                ],
            },
            {
                "slug": "longevity-finance",
                "title": "Longevity Turns Into a Financial Product Problem",
                "summary": "Living longer creates demand not only for care, but for insurance, annuities, wealth planning, estate logistics, and services that price extended life expectancy.",
                "microthemes": [
                    "retirement duration extending balance-sheet risk",
                    "care financing pushing households toward structured products",
                    "inheritance and planning services expanding with age complexity",
                    "insurers repricing risk around longevity and chronic disease",
                ],
                "forces": ["the-graying-market", "money-gets-unbundled"],
                "industries": [
                    "life-insurance-and-annuities-in-the-us",
                    "long-term-care-insurance",
                    "portfolio-management-in-the-us",
                    "financial-planning-and-advice-in-the-us",
                ],
                "companies": ["prudential-financial", "marsh-and-mclennan", "aon", "state-farm"],
                "operator_implications": [
                    "Aging households need both care and financial orchestration.",
                    "Long-duration trust businesses can benefit if they manage underwriting discipline.",
                    "Advice, insurance, and care planning increasingly intersect.",
                ],
            },
        ],
    },
    {
        "slug": "work-without-the-old-firm",
        "title": "Work Without the Old Firm",
        "lens": "Social / Labor",
        "thesis": "The traditional firm is thinning. Expertise is rented more often, junior pathways are weaker, benefits are externalized, and automation is increasingly used to defend margins against labor scarcity.",
        "why_now": "Higher labor costs, digital coordination tools, AI assistance, and employer caution are making staffing more variable and task-based than the old full-time ladder model.",
        "forces": ["the-fractional-worker", "the-labor-squeeze", "the-compute-super-cycle"],
        "crosscuts": ["labor-scarcity", "ai-and-automation"],
        "questions": [
            "What work must stay internal and what can be rented or automated?",
            "Where is the junior career ladder getting hollowed out?",
            "Who captures value when expertise becomes modular?",
        ],
        "subthemes": [
            {
                "slug": "fractional-executive-layer",
                "title": "The Fractional Executive Layer Expands",
                "summary": "Smaller and mid-sized companies increasingly rent senior judgment instead of hiring full-time leaders across finance, marketing, HR, and strategy.",
                "microthemes": [
                    "leadership bought by project or part-time retainer",
                    "specialist expertise replacing generalist middle management",
                    "SMBs gaining access to senior talent without full payroll commitment",
                    "advisory services becoming more operational and embedded",
                ],
                "forces": ["the-fractional-worker", "the-margin-vise"],
                "industries": [
                    "business-coaching-in-the-us",
                    "management-consulting-in-the-us",
                    "marketing-consultants",
                    "hr-consulting-in-the-us",
                ],
                "companies": ["accenture", "wpp", "adp", "trinet"],
                "operator_implications": [
                    "Advisory businesses should package expertise into recurring, productized offers.",
                    "Clients increasingly buy outcomes, not hours alone.",
                    "Operational trust beats generic thought leadership.",
                ],
            },
            {
                "slug": "skills-and-credentials-market",
                "title": "Skills and Credentials Replace Slow Career Ladders",
                "summary": "Workers respond to thinner promotion pathways by buying targeted credentials, practical certificates, and short-cycle training linked to immediate labor-market value.",
                "microthemes": [
                    "micro-credentials as employability insurance",
                    "shorter training loops replacing long formal pathways",
                    "worker self-funding of adaptability",
                    "employers using credentials as screening shortcuts",
                ],
                "forces": ["the-fractional-worker", "the-labor-squeeze"],
                "industries": [
                    "business-certification-and-it-schools-in-the-us",
                    "educational-services-in-the-us",
                    "electricians-in-the-us",
                    "heating-and-air-conditioning-contractors-in-the-us",
                ],
                "companies": ["kumon", "adp", "trinet", "microsoft"],
                "operator_implications": [
                    "Training providers need clearer links to wage gain and employability.",
                    "Trades and technical certifications should be sold as economic mobility infrastructure.",
                    "Credential markets benefit when hiring remains fragmented and anxious.",
                ],
            },
            {
                "slug": "junior-rung-compression",
                "title": "The Junior Rung Gets Compressed",
                "summary": "Automation, offshoring, and selective hiring make it harder for new entrants to access training-rich early-career roles, especially in knowledge work.",
                "microthemes": [
                    "entry-level cognitive work replaced by software and workflows",
                    "fewer apprenticeship-style roles in white-collar sectors",
                    "career progression becoming less linear and less firm-sponsored",
                    "credential inflation masking weaker true training investment",
                ],
                "forces": ["the-fractional-worker", "the-compute-super-cycle"],
                "industries": [
                    "accounting-services-in-the-us",
                    "law-firms-in-the-us",
                    "business-analytics-and-enterprise-software-publishing-in-the-us",
                    "customer-service-representative-services-in-the-us",
                ],
                "companies": ["ey", "infosys", "wipro", "accenture"],
                "operator_implications": [
                    "Firms may save cost now while weakening their long-term talent pipeline.",
                    "Vendors selling workflow automation should expect labor substitution scrutiny.",
                    "Training design becomes a strategic question rather than an HR afterthought.",
                ],
            },
            {
                "slug": "benefits-externalized",
                "title": "Benefits and Stability Shift Onto Workers",
                "summary": "As work fragments, healthcare, disability coverage, retirement savings, and schedule predictability become more individualized and more precarious.",
                "microthemes": [
                    "portable benefits still lagging real labor-market fragmentation",
                    "independent workers buying more risk coverage themselves",
                    "irregular schedules increasing household planning stress",
                    "insurers and payroll platforms monetizing the gap",
                ],
                "forces": ["the-fractional-worker", "money-gets-unbundled"],
                "industries": [
                    "health-and-medical-insurance-in-the-us",
                    "disability-insurance",
                    "payroll-and-bookkeeping-services-in-the-us",
                    "professional-employer-organizations-in-the-us",
                ],
                "companies": ["paychex", "adp", "trinet", "aon"],
                "operator_implications": [
                    "There is demand for administrative simplification around unstable work.",
                    "Platform businesses can capture value by packaging protection with flexibility.",
                    "The benefits gap is both a social problem and a recurring revenue opportunity.",
                ],
            },
            {
                "slug": "automation-as-labor-arbitrage",
                "title": "Automation Becomes Labor Arbitrage",
                "summary": "Many automation decisions are no longer primarily about innovation theater. They are responses to unavailable labor, wage pressure, and the need for throughput consistency.",
                "microthemes": [
                    "robots and software filling labor gaps before they chase full transformation",
                    "automation prioritized where turnover is chronic",
                    "workflow compression valued for reliability as much as headcount reduction",
                    "operators preferring selective mechanization over total redesign",
                ],
                "forces": ["the-labor-squeeze", "the-compute-super-cycle"],
                "industries": [
                    "meat-beef-and-poultry-processing-in-the-us",
                    "vending-machine-operators-in-the-us",
                    "general-freight-trucking-truckload",
                    "business-analytics-and-enterprise-software-publishing-in-the-us",
                ],
                "companies": ["amazon", "sysco", "microsoft", "cargill"],
                "operator_implications": [
                    "Automation budgets should be framed against labor reliability, not only labor cost.",
                    "Partial automation can create better payback than ambitious full-stack reinvention.",
                    "The operator question is where labor is truly the binding constraint.",
                ],
            },
        ],
    },
    {
        "slug": "physical-reindustrialization-and-infrastructure",
        "title": "Physical Reindustrialization and Infrastructure",
        "lens": "Industrial",
        "thesis": "The physical economy has become strategic again. Tariffs, reshoring, power demand, logistics, and infrastructure needs are repricing materials, locations, and the trades that make modern buildout possible.",
        "why_now": "Trade politics, AI infrastructure demand, federal spending, and supply-chain insecurity have made land, steel, power access, and construction capacity central economic bottlenecks again.",
        "forces": ["atoms-strike-back", "the-compute-super-cycle", "the-labor-squeeze", "commodity-whiplash"],
        "crosscuts": ["labor-scarcity", "capital-and-scale", "ai-and-automation"],
        "questions": [
            "Where are political supply chains changing cost structure permanently?",
            "Which bottleneck input actually governs growth: labor, power, land, or materials?",
            "Who sits on the advantaged side of physical scarcity?",
        ],
        "subthemes": [
            {
                "slug": "tariffed-inputs",
                "title": "Tariffed Inputs Flow Through the Whole Stack",
                "summary": "Trade barriers on metals, auto components, and imported goods ripple outward into manufacturing, retail, and construction pricing.",
                "microthemes": [
                    "materials inflation transmitted through downstream sectors",
                    "import dependency becoming a strategic vulnerability",
                    "procurement capability growing in importance",
                    "manufacturers and merchants repricing around policy volatility",
                ],
                "forces": ["atoms-strike-back", "commodity-whiplash"],
                "industries": [
                    "iron-and-steel-manufacturing-in-the-us",
                    "aluminum-manufacturing-in-the-us",
                    "auto-parts-manufacturing-in-the-us",
                    "furniture-stores-in-the-us",
                ],
                "companies": ["cleveland-cliffs", "stellantis", "whirlpool", "walmart"],
                "operator_implications": [
                    "Procurement and sourcing discipline become strategic, not back-office.",
                    "Thin-margin import models look structurally less attractive.",
                    "Domestic or nearshore optionality gains value even before full relocation.",
                ],
            },
            {
                "slug": "power-centric-geography",
                "title": "Power-Centric Geography Reorders Industrial Value",
                "summary": "Sites with access to power, transmission, cooling, and permissive land economics gain strategic value relative to places that merely looked attractive in the old logistics-only model.",
                "microthemes": [
                    "data-center demand changing land value maps",
                    "generation and transmission access determining site viability",
                    "industrial geography shifting toward energy-rich corridors",
                    "small users crowded by hyperscale infrastructure demand",
                ],
                "forces": ["the-compute-super-cycle", "the-real-estate-reckoning"],
                "industries": [
                    "colocation-facilities",
                    "electric-power-transmission-in-the-us",
                    "natural-gas-distribution-in-the-us",
                    "land-leasing-in-the-us",
                ],
                "companies": ["coreweave", "nextera-energy", "kinder-morgan", "prologis"],
                "operator_implications": [
                    "Power access should be treated as a first-order go-to-market variable.",
                    "Asset owners near transmission and gas infrastructure gain optionality.",
                    "Land is no longer generic when compute or electrification demand is nearby.",
                ],
            },
            {
                "slug": "electrical-and-cooling-trades",
                "title": "Electrical and Cooling Trades Become Picks and Shovels",
                "summary": "Electricians, HVAC contractors, turbine suppliers, and electrical-equipment manufacturers sit in the middle of multiple secular buildouts at once.",
                "microthemes": [
                    "AI infrastructure, building retrofits, and electrification sharing the same labor pool",
                    "cooling becoming central to industrial and digital buildout",
                    "trade labor scarcity improving pricing leverage",
                    "maintenance and retrofit work compounding alongside new construction",
                ],
                "forces": ["the-compute-super-cycle", "the-labor-squeeze"],
                "industries": [
                    "electricians-in-the-us",
                    "heating-and-air-conditioning-contractors-in-the-us",
                    "engine-and-turbine-manufacturing-in-the-us",
                    "electrical-equipment-manufacturing-in-the-us",
                ],
                "companies": ["eaton", "emerson-electric", "mastec", "honeywell"],
                "operator_implications": [
                    "Trade bottlenecks can be more investable than the headline megaprojects they support.",
                    "Backlog quality and labor retention are crucial operating metrics.",
                    "Equipment suppliers with installed bases gain follow-on demand from service and replacement.",
                ],
            },
            {
                "slug": "reshored-specification-manufacturing",
                "title": "Reshored Specification Manufacturing Gains Relevance",
                "summary": "Domestic and nearshore manufacturing regains appeal in categories where lead time, compliance, defense, or system integration matter more than lowest nominal cost.",
                "microthemes": [
                    "security and resilience overriding pure landed-cost logic",
                    "advanced manufacturing linked to national capability goals",
                    "shorter supply chains valued in specified or regulated categories",
                    "automation making domestic production more defensible",
                ],
                "forces": ["atoms-strike-back", "the-compute-super-cycle"],
                "industries": [
                    "computer-manufacturing-in-the-us",
                    "3d-printer-manufacturing",
                    "aircraft-engine-and-parts-manufacturing-in-the-us",
                    "medical-device-manufacturing-in-the-us",
                ],
                "companies": ["honeywell-international", "precision-castparts", "thermo-fisher-scientific", "3m"],
                "operator_implications": [
                    "Specified domestic capability can support better customer stickiness.",
                    "Manufacturers should lean into reliability and integration, not commodity volume alone.",
                    "Reshoring works best where complexity and trust matter.",
                ],
            },
            {
                "slug": "freight-warehouse-repricing",
                "title": "Freight and Warehousing Are Being Repriced by Complexity",
                "summary": "Even where freight demand is uneven, logistics complexity, delivery expectations, and strategic inventory decisions keep transportation and warehousing economically central.",
                "microthemes": [
                    "inventory localization increasing node complexity",
                    "faster fulfillment increasing logistics intensity",
                    "trucking labor and fuel volatility still shaping margins",
                    "warehouse assets gaining strategic value relative to older retail real estate",
                ],
                "forces": ["atoms-strike-back", "the-channel-shift", "the-labor-squeeze"],
                "industries": [
                    "general-freight-trucking-truckload",
                    "local-freight-trucking-in-the-us",
                    "couriers-and-local-delivery-services-in-the-us",
                    "commercial-real-estate-in-the-us",
                ],
                "companies": ["xpo-logistics", "amazon", "sysco", "prologis"],
                "operator_implications": [
                    "The value sits in orchestration and network quality, not simply miles moved.",
                    "Logistics real estate and physical throughput infrastructure remain strategic.",
                    "Asset-light models still need deep operational discipline to survive volatility.",
                ],
            },
        ],
    },
    {
        "slug": "scale-financialization-and-the-owned-economy",
        "title": "Scale, Financialization, and the Owned Economy",
        "lens": "Industrial / Institutional",
        "thesis": "More of the economy is being shaped by scale owners, roll-up logic, institutional asset holders, and platform economics that centralize purchasing power, compliance, and capital access.",
        "why_now": "Higher rates, heavier regulation, labor complexity, and digital coordination all make fragmented ownership harder to sustain and make scaled control more valuable.",
        "forces": ["the-great-consolidation", "the-real-estate-reckoning", "money-gets-unbundled", "the-compliance-tax"],
        "crosscuts": ["capital-and-scale", "consumer-bifurcation"],
        "questions": [
            "Is this market still hospitable to independents, or has the structure already shifted?",
            "Where does ownership scale matter more than local craftsmanship?",
            "Who captures the spread created by complexity?",
        ],
        "subthemes": [
            {
                "slug": "rollups-in-essential-services",
                "title": "Roll-Ups Colonize Essential Services",
                "summary": "Healthcare, home services, consulting, and everyday operational categories keep moving from local ownership into regional and national platforms.",
                "microthemes": [
                    "fragmented local sectors becoming acquisition targets",
                    "back-office centralization improving unit economics",
                    "brand standardization replacing individual reputation",
                    "exit markets rewarding scale more than independent durability",
                ],
                "forces": ["the-great-consolidation", "the-compliance-tax"],
                "industries": [
                    "dentists-in-the-us",
                    "environmental-consulting-in-the-us",
                    "engineering-services-in-the-us",
                    "residential-senior-care-franchises",
                ],
                "companies": ["marsh-and-mclennan", "stantec", "clean-harbors", "massage-envy"],
                "operator_implications": [
                    "Fragmented categories should be evaluated for acquisition-system quality, not just local share.",
                    "Centralized admin and procurement are core sources of value capture.",
                    "Independents need a stronger moat than being merely local and competent.",
                ],
            },
            {
                "slug": "asset-owners-over-operators",
                "title": "Asset Owners Keep Gaining Relative Power",
                "summary": "The owner of land, rights, infrastructure, or financial rails often captures more durable economics than the visible operator working on top of those assets.",
                "microthemes": [
                    "ground ownership and lease control separating from operations",
                    "rights catalogs and infrastructure assets treated as yield-bearing instruments",
                    "operators renting critical assets from institutional owners",
                    "cash-flow stability prized over entrepreneurial messiness",
                ],
                "forces": ["the-great-consolidation", "the-real-estate-reckoning"],
                "industries": [
                    "land-leasing-in-the-us",
                    "commercial-real-estate-in-the-us",
                    "music-publishing-in-the-us",
                    "colocation-facilities",
                ],
                "companies": ["prologis", "cbre", "alphabet", "at-and-t"],
                "operator_implications": [
                    "Owning the constraint often beats operating on top of it.",
                    "Investors should distinguish asset control from operating revenue noise.",
                    "The hidden landlord or rail owner may be the true power center in the value chain.",
                ],
            },
            {
                "slug": "regional-intermediary-squeeze",
                "title": "Regional Intermediaries Get Squeezed",
                "summary": "Smaller banks, brokers, and mid-sized intermediaries face pressure from both scaled incumbents above and embedded or digital alternatives below.",
                "microthemes": [
                    "tech and compliance spend overwhelming smaller balance sheets",
                    "rate volatility exposing weak spread businesses",
                    "embedded digital experiences stealing customer relationships",
                    "merger pressure rising as independence gets more expensive",
                ],
                "forces": ["money-gets-unbundled", "the-great-consolidation"],
                "industries": [
                    "commercial-banking-in-the-us",
                    "credit-unions-in-the-us",
                    "loan-brokers-in-the-us",
                    "portfolio-management-in-the-us",
                ],
                "companies": ["experian", "intuit", "s-and-p-global", "prudential-financial"],
                "operator_implications": [
                    "Regional players need a niche or service quality that software cannot easily erase.",
                    "Balance-sheet businesses should be judged on tech burden as well as credit quality.",
                    "The middleman without unique data or trust keeps losing ground.",
                ],
            },
            {
                "slug": "franchise-and-platform-governance",
                "title": "Franchise and Platform Governance Matter More Than Local Hustle",
                "summary": "Local operators increasingly sit inside systems governed by franchisors, marketplaces, and scaled workflow owners that define the real economics.",
                "microthemes": [
                    "local ownership constrained by platform rules",
                    "brand systems taking more of the value stack",
                    "unit-level execution still matters but inside centralized terms",
                    "operators trading autonomy for demand and tooling",
                ],
                "forces": ["the-great-consolidation", "the-channel-shift"],
                "industries": [
                    "chain-restaurants-in-the-us",
                    "residential-senior-care-franchises",
                    "e-commerce-and-online-auctions-in-the-us",
                    "hotels-and-motels-in-the-us",
                ],
                "companies": ["mcdonald-s", "subway", "amazon", "hyatt-hotels"],
                "operator_implications": [
                    "Unit economics must be read alongside platform take rates and system control.",
                    "The nominal operator may not be the real strategic decision-maker.",
                    "Franchise and marketplace governance quality is a first-order diligence issue.",
                ],
            },
            {
                "slug": "institutional-buying-power",
                "title": "Institutional Buying Power Widens the Gap",
                "summary": "Centralized purchasing, financing, and shared services let scaled operators absorb shocks that punish smaller competitors.",
                "microthemes": [
                    "procurement scale insulating against input volatility",
                    "shared overhead lowering per-unit compliance and software cost",
                    "access to cheaper capital improving resilience",
                    "vendor negotiations shifting toward giant repeat buyers",
                ],
                "forces": ["the-great-consolidation", "the-margin-vise", "the-compliance-tax"],
                "industries": [
                    "home-improvement-stores-in-the-us",
                    "meat-beef-and-poultry-processing-in-the-us",
                    "medical-device-manufacturing-in-the-us",
                    "grocery-stores-in-the-us",
                ],
                "companies": ["walmart", "costco", "medline-industries", "sysco"],
                "operator_implications": [
                    "Scale should be treated as an operating asset, not a descriptive label.",
                    "Independent players need sharper specialization where buyers cannot fully commoditize them.",
                    "Cost shocks increasingly separate the scaled from the merely adequate.",
                ],
            },
        ],
    },
    {
        "slug": "regulated-software-and-admin-state",
        "title": "Regulated Software and the Admin State",
        "lens": "Institutional / Technological",
        "thesis": "A larger share of economic value now comes from managing mandatory complexity: compliance, identity, reimbursement, audit trails, fraud control, privacy, testing, and other workflows customers cannot simply skip.",
        "why_now": "Regulatory burden, cyber risk, healthcare documentation, and financial scrutiny keep rising, which creates durable demand for businesses that turn complexity into software, services, or embedded infrastructure.",
        "forces": ["the-compliance-tax", "money-gets-unbundled", "the-compute-super-cycle", "the-pricing-power-collapse"],
        "crosscuts": ["ai-and-automation", "capital-and-scale"],
        "questions": [
            "Is this demand discretionary, or is it effectively mandatory?",
            "Can the workflow be productized and embedded, or does it stay bespoke and labor-heavy?",
            "Who benefits when rules, risk, and documentation all get denser?",
        ],
        "subthemes": [
            {
                "slug": "compliance-as-demand",
                "title": "Compliance Itself Becomes a Demand Engine",
                "summary": "Reporting, safety, environmental, quality, and documentation requirements create revenue pools that are only loosely tied to discretionary end-market growth.",
                "microthemes": [
                    "mandatory workflows sustaining demand through weak cycles",
                    "regulated sectors outsourcing rule complexity",
                    "documentation and auditability becoming product features",
                    "software plus service bundles beating pure labor fulfillment",
                ],
                "forces": ["the-compliance-tax", "the-margin-vise"],
                "industries": [
                    "environmental-consulting-in-the-us",
                    "testing-laboratories-in-the-us",
                    "engineering-services-in-the-us",
                    "hr-consulting-in-the-us",
                ],
                "companies": ["ecolab", "clean-harbors", "stantec", "adp"],
                "operator_implications": [
                    "Compliance demand can be sticky even when customers dislike paying for it.",
                    "Recurring embedded workflows deserve higher strategic value than episodic projects.",
                    "The key question is how much manual labor remains in delivery.",
                ],
            },
            {
                "slug": "identity-fraud-infrastructure",
                "title": "Identity, Fraud, and Trust Infrastructure Thickens",
                "summary": "Synthetic identity fraud, deepfakes, cyber risk, and financial scams are increasing the value of verification, scoring, monitoring, and risk infrastructure.",
                "microthemes": [
                    "identity systems becoming more continuous and layered",
                    "fraud defense shifting from after-the-fact recovery to prevention",
                    "consumer trust mediated by invisible scoring and verification rails",
                    "risk data turning into a toll-taking business model",
                ],
                "forces": ["money-gets-unbundled", "the-compute-super-cycle", "the-compliance-tax"],
                "industries": [
                    "credit-bureaus-and-rating-agencies-in-the-us",
                    "identity-theft-insurance",
                    "cybersecurity-consulting-in-the-us",
                    "credit-card-processing-and-money-transferring-in-the-us",
                ],
                "companies": ["experian", "lexisnexis-risk-solutions", "s-and-p-global", "chubb"],
                "operator_implications": [
                    "Trust infrastructure benefits when fraud methods improve faster than institutions adapt.",
                    "Data depth and embedded distribution are stronger moats than raw feature counts.",
                    "Many businesses will pay for prevention long before they pay for elegance.",
                ],
            },
            {
                "slug": "reimbursement-admin-layers",
                "title": "Reimbursement and Admin Layers Capture Value Around Care",
                "summary": "Healthcare generates large recurring administrative workloads around coding, claims, prior authorization, eligibility, and payment reconciliation.",
                "microthemes": [
                    "care delivery complexity spawning specialized admin infrastructure",
                    "billing and coding sophistication separating winners from losers",
                    "administrative throughput becoming part of clinical competitiveness",
                    "software-enabled outsourcing growing around payer-provider friction",
                ],
                "forces": ["the-compliance-tax", "the-pricing-power-collapse", "the-graying-market"],
                "industries": [
                    "health-and-medical-insurance-in-the-us",
                    "medical-billing-services-in-the-us",
                    "ambulatory-surgery-centers",
                    "mental-health-and-substance-abuse-clinics-in-the-us",
                ],
                "companies": ["cvs-health", "humana", "labcorp", "thermo-fisher-scientific"],
                "operator_implications": [
                    "In healthcare, admin performance can decide whether demand is monetizable.",
                    "Back-office friction is a real source of customer pain and therefore real value capture.",
                    "Operators should distinguish between labor-heavy services and scalable workflow rails.",
                ],
            },
            {
                "slug": "cyber-audit-overhead",
                "title": "Cyber and Audit Overhead Keep Expanding",
                "summary": "Cybersecurity, controls, and audit readiness are now ordinary operating requirements across finance, infrastructure, healthcare, and the mid-market.",
                "microthemes": [
                    "security spend shifting from optional to table stakes",
                    "insurance, compliance, and technology controls converging",
                    "audit trails becoming part of vendor qualification",
                    "regulatory scrutiny widening beyond the largest enterprises",
                ],
                "forces": ["the-compliance-tax", "the-compute-super-cycle"],
                "industries": [
                    "cybersecurity-consulting-in-the-us",
                    "commercial-banking-in-the-us",
                    "credit-unions-in-the-us",
                    "internet-hosting-services",
                ],
                "companies": ["alphabet", "microsoft", "aon", "experian"],
                "operator_implications": [
                    "Security should be treated as operating infrastructure, not an IT accessory.",
                    "Vendors that simplify evidence collection and control mapping can capture recurring budgets.",
                    "Auditability itself is part of enterprise product value now.",
                ],
            },
            {
                "slug": "mandatory-testing-and-certification",
                "title": "Testing, Certification, and Standards Quietly Gain Power",
                "summary": "As products, environments, and labor become more regulated or specialized, testing and certification bodies take a larger hidden cut of the economy.",
                "microthemes": [
                    "more sectors requiring formal validation before sale or deployment",
                    "quality assurance moving from back-end check to market-entry gate",
                    "certification acting as customer-trust transfer mechanism",
                    "specialized labs and standards vendors benefiting from institutional complexity",
                ],
                "forces": ["the-compliance-tax", "atoms-strike-back"],
                "industries": [
                    "testing-laboratories-in-the-us",
                    "medical-device-manufacturing-in-the-us",
                    "electrical-equipment-manufacturing-in-the-us",
                    "business-certification-and-it-schools-in-the-us",
                ],
                "companies": ["thermo-fisher-scientific", "labcorp", "3m", "msa-safety"],
                "operator_implications": [
                    "Gatekeeper positions around standards can be structurally attractive.",
                    "The customer often pays because they have to, not because they want to.",
                    "Certification businesses get stronger as product complexity rises.",
                ],
            },
        ],
    },
    {
        "slug": "space-housing-and-local-friction",
        "title": "Space, Housing, and Local Friction",
        "lens": "Societal / Industrial",
        "thesis": "Where Americans live, commute, and locate activity is being reorganized by housing lock-in, office impairment, land scarcity near infrastructure, and the uneven value of local place.",
        "why_now": "Higher rates, hybrid work, data-center and logistics demand, and persistent housing shortages are all altering the economic value of geography.",
        "forces": ["the-real-estate-reckoning", "the-compute-super-cycle", "atoms-strike-back"],
        "crosscuts": ["capital-and-scale", "labor-scarcity"],
        "questions": [
            "Which physical places are getting more valuable and which are losing strategic purpose?",
            "How does housing friction spill into labor and local services?",
            "Where is geography now a competitive moat?",
        ],
        "subthemes": [
            {
                "slug": "office-obsolescence",
                "title": "Office Obsolescence Is a Structural Shift",
                "summary": "The office is no longer the default high-value urban container for work, which leaves many assets struggling for a new economic purpose.",
                "microthemes": [
                    "hybrid work reducing demand for commodity office space",
                    "capital markets forcing repricing through debt maturities",
                    "service ecosystems around offices losing traffic density",
                    "top-tier trophy assets diverging from the weak middle",
                ],
                "forces": ["the-real-estate-reckoning", "the-fractional-worker"],
                "industries": [
                    "commercial-real-estate-in-the-us",
                    "architects-in-the-us",
                    "commercial-property-remodeling",
                    "janitorial-services-in-the-us",
                ],
                "companies": ["cbre", "stantec", "dpr-construction", "the-whiting-turner-contracting"],
                "operator_implications": [
                    "Office exposure should be segmented by asset quality and adaptability, not averaged.",
                    "Secondary service businesses around office density need fresh demand sources.",
                    "Debt structure matters almost as much as rent roll.",
                ],
            },
            {
                "slug": "adaptive-reuse",
                "title": "Adaptive Reuse Becomes a New Development Discipline",
                "summary": "Weak offices, malls, and older commercial assets create opportunity for conversion, repositioning, and selective redevelopment tied to housing or mixed-use demand.",
                "microthemes": [
                    "conversion economics replacing pure new-build economics",
                    "older assets assessed for code, utility, and zoning flexibility",
                    "reuse creating winners in remodeling and specialty construction",
                    "local regulatory capacity shaping what actually pencils",
                ],
                "forces": ["the-real-estate-reckoning", "the-compliance-tax"],
                "industries": [
                    "commercial-building-construction-in-the-us",
                    "commercial-property-remodeling",
                    "architects-in-the-us",
                    "engineering-services-in-the-us",
                ],
                "companies": ["dpr-construction", "granite-construction", "stantec", "pcl-construction"],
                "operator_implications": [
                    "Reuse work requires technical coordination and permitting fluency.",
                    "Local regulation and utility constraints can make or break project viability.",
                    "Specialty contractors may benefit more than general market narratives imply.",
                ],
            },
            {
                "slug": "housing-lock-in",
                "title": "Housing Lock-In Distorts Mobility and Spend",
                "summary": "High mortgage rates and limited affordable supply reduce household mobility, which affects renovation, rental demand, local services, and labor flexibility.",
                "microthemes": [
                    "owners staying put longer because replacement housing is too expensive",
                    "repair and remodel benefiting from frozen transaction volume",
                    "renting staying elevated even when households would prefer to buy",
                    "labor mobility reduced by housing mismatch",
                ],
                "forces": ["the-real-estate-reckoning", "the-margin-vise"],
                "industries": [
                    "home-builders-in-the-us",
                    "apartment-rental-in-the-us",
                    "home-improvement-stores-in-the-us",
                    "roofing-contractors-in-the-us",
                ],
                "companies": ["the-home-depot", "lowe-s", "cbre", "floor-and-decor"],
                "operator_implications": [
                    "Transaction-light housing environments can still support strong maintenance and retrofit demand.",
                    "Geographic labor matching gets harder when households cannot move cheaply.",
                    "Rental and repair ecosystems benefit from housing immobility.",
                ],
            },
            {
                "slug": "logistics-land-and-utility-corridors",
                "title": "Logistics Land and Utility Corridors Gain Strategic Rent",
                "summary": "Warehouses, data-center sites, and utility-linked land capture more value because they sit next to the flows that the modern economy cannot avoid.",
                "microthemes": [
                    "warehousing retaining strategic relevance despite e-commerce normalization",
                    "utility adjacency increasing development value",
                    "industrial land scarcity creating quiet winners",
                    "old retail land losing while logistics and data land gains",
                ],
                "forces": ["the-real-estate-reckoning", "the-compute-super-cycle", "the-channel-shift"],
                "industries": [
                    "land-leasing-in-the-us",
                    "commercial-real-estate-in-the-us",
                    "colocation-facilities",
                    "couriers-and-local-delivery-services-in-the-us",
                ],
                "companies": ["prologis", "coreweave", "amazon", "kinder-morgan"],
                "operator_implications": [
                    "Not all land is equal; adjacency to power or throughput matters enormously.",
                    "Real estate diligence should be flow-based, not only cap-rate-based.",
                    "Local place can still be a hard moat in a digital economy.",
                ],
            },
            {
                "slug": "local-service-density",
                "title": "Local Service Density Follows New Patterns of Presence",
                "summary": "Neighborhoods and corridors with stable residential activity gain relative importance as weekday downtown density weakens and local routine spend redistributes.",
                "microthemes": [
                    "suburban and neighborhood nodes capturing more everyday activity",
                    "service businesses re-optimizing around where people actually spend time",
                    "downtown foot traffic becoming less reliable as a default demand source",
                    "place-based convenience still mattering despite digital substitution",
                ],
                "forces": ["the-real-estate-reckoning", "the-channel-shift"],
                "industries": [
                    "coffee-and-snack-shops-in-the-us",
                    "fast-food-restaurants-in-the-us",
                    "pharmacies-and-drug-stores-in-the-us",
                    "grocery-stores-in-the-us",
                ],
                "companies": ["starbucks", "cvs-health", "kroger", "panera-bread"],
                "operator_implications": [
                    "Micro-location strategy matters more when daily routines change.",
                    "Neighborhood convenience can be structurally stronger than central-business-district assumptions.",
                    "Service density should be mapped to lived presence, not historical traffic.",
                ],
            },
        ],
    },
    {
        "slug": "machine-intelligence-and-compute-buildout",
        "title": "Machine Intelligence and Compute Buildout",
        "lens": "Technological / Industrial",
        "thesis": "AI is not just a software feature cycle. It is simultaneously a workflow-compression story, a compute and power infrastructure story, and a market concentration story around who can afford the stack.",
        "why_now": "Massive model training and inference demand are colliding with power availability, data-center capacity, labor substitution pressure, and capital intensity across the broader economy.",
        "forces": ["the-compute-super-cycle", "money-gets-unbundled", "the-fractional-worker"],
        "crosscuts": ["ai-and-automation", "capital-and-scale", "labor-scarcity"],
        "questions": [
            "Where is AI substituting labor and where is it creating new physical bottlenecks?",
            "Who owns the scarce layer: models, chips, data centers, power, or workflow distribution?",
            "Which sectors get productivity and which mostly get higher input costs?",
        ],
        "subthemes": [
            {
                "slug": "data-center-land-rush",
                "title": "The Data-Center Land Rush Creates New Scarcity",
                "summary": "AI demand turns power-ready land, colocation capacity, cooling systems, and permitting speed into strategic bottlenecks.",
                "microthemes": [
                    "power-ready land becoming a premium asset class",
                    "hyperscale and AI tenants pulling forward physical demand",
                    "cooling and water infrastructure becoming site constraints",
                    "regional buildout concentrating around utility-friendly zones",
                ],
                "forces": ["the-compute-super-cycle", "the-real-estate-reckoning"],
                "industries": [
                    "colocation-facilities",
                    "electric-power-transmission-in-the-us",
                    "commercial-building-construction-in-the-us",
                    "land-leasing-in-the-us",
                ],
                "companies": ["coreweave", "alphabet", "microsoft", "prologis"],
                "operator_implications": [
                    "The AI trade includes real estate, utilities, and heavy construction, not just software.",
                    "Permitting speed and power contracts can be more decisive than raw model ambition.",
                    "Physical scarcity will shape who can scale inference economically.",
                ],
            },
            {
                "slug": "workflow-compression",
                "title": "Workflow Compression Rewrites Knowledge Work",
                "summary": "AI tools increasingly collapse drafting, analysis, support, and administrative work into fewer steps, which changes staffing economics across white-collar sectors.",
                "microthemes": [
                    "junior and repeatable tasks being automated first",
                    "throughput expectations rising because tooling improves",
                    "buyers expecting more output for the same service budget",
                    "human oversight shifting toward exception handling and judgment",
                ],
                "forces": ["the-compute-super-cycle", "the-fractional-worker"],
                "industries": [
                    "business-analytics-and-enterprise-software-publishing-in-the-us",
                    "customer-service-representative-services-in-the-us",
                    "accounting-services-in-the-us",
                    "management-consulting-in-the-us",
                ],
                "companies": ["microsoft", "accenture", "infosys", "wipro"],
                "operator_implications": [
                    "Service firms need a deliberate view on which labor layers remain differentiated.",
                    "Software vendors should position around throughput and auditability, not magic.",
                    "Productivity gains may compress fees before they expand margins.",
                ],
            },
            {
                "slug": "capital-concentration",
                "title": "AI Concentrates Capital and Strategic Power",
                "summary": "Training frontier models and operating at scale require enormous capital, compute access, and distribution, which favors a relatively small set of large platform or infrastructure players.",
                "microthemes": [
                    "frontier model economics rewarding extreme scale",
                    "platform distribution controlling customer access to AI usage",
                    "smaller players depending on infrastructure leased from giants",
                    "capital markets rewarding perceived infrastructure leverage",
                ],
                "forces": ["the-compute-super-cycle", "money-gets-unbundled"],
                "industries": [
                    "internet-hosting-services",
                    "business-analytics-and-enterprise-software-publishing-in-the-us",
                    "database-storage-and-backup-software-publishing-in-the-us",
                    "commercial-banking-in-the-us",
                ],
                "companies": ["microsoft", "alphabet", "amazon", "coreweave"],
                "operator_implications": [
                    "Infrastructure ownership can matter more than app-level novelty.",
                    "Dependent software businesses need to understand their exposure to upstream platform control.",
                    "The AI market is likely to be less democratic than the rhetoric implies.",
                ],
            },
            {
                "slug": "power-and-water-externalities",
                "title": "Power, Water, and Heat Become AI Externalities",
                "summary": "The compute boom pushes environmental and utility consequences into local politics, utility planning, and industrial cost structures far outside software.",
                "microthemes": [
                    "grid stress spilling into broader commercial and residential economics",
                    "cooling-water demand creating local permitting friction",
                    "waste heat and energy efficiency becoming operational variables",
                    "utility planning increasingly shaped by digital rather than household demand",
                ],
                "forces": ["the-compute-super-cycle", "commodity-whiplash"],
                "industries": [
                    "electric-power-transmission-in-the-us",
                    "hydroelectric-power-in-the-us",
                    "waste-to-energy-plant-operation",
                    "natural-gas-distribution-in-the-us",
                ],
                "companies": ["nextera-energy", "kinder-morgan", "baker-hughes", "eaton"],
                "operator_implications": [
                    "Digital growth has real physical and political costs.",
                    "Utilities and infrastructure suppliers become indirect AI beneficiaries and constraints.",
                    "Local externalities will increasingly shape where compute gets built.",
                ],
            },
            {
                "slug": "ai-inside-boring-industries",
                "title": "AI Seeps Into Boring Industries Through Workflows First",
                "summary": "The most durable AI adoption may come from embedding into routine workflows in finance, logistics, healthcare, and regulated admin rather than from flashy standalone consumer products.",
                "microthemes": [
                    "workflow integration beating general-purpose novelty",
                    "boring sectors adopting where ROI is legible",
                    "documentation and search tasks absorbing early gains",
                    "compliance-heavy sectors preferring controlled AI usage over open experimentation",
                ],
                "forces": ["the-compute-super-cycle", "the-compliance-tax", "money-gets-unbundled"],
                "industries": [
                    "credit-bureaus-and-rating-agencies-in-the-us",
                    "medical-billing-services-in-the-us",
                    "general-freight-trucking-truckload",
                    "payroll-and-bookkeeping-services-in-the-us",
                ],
                "companies": ["experian", "intuit", "paychex", "xpo-logistics"],
                "operator_implications": [
                    "The practical AI opportunity is often incremental but highly monetizable.",
                    "Embedded workflow adoption should be measured by time saved and error reduced.",
                    "The biggest winners may be unglamorous software and admin layers.",
                ],
            },
        ],
    },
]


def e(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def load_json(path: Path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_lookups():
    force_lookup = {}
    for force in FORCES:
        subtheme_count = sum(len(items) for items in force["groups"].values())
        evidence_slugs = []
        for items in force["groups"].values():
            for _, _, evidence_str, _ in items:
                evidence_slugs.extend([slug for slug in str(evidence_str).split() if slug])
        force_lookup[force["slug"]] = {
            "slug": force["slug"],
            "title": force["title"],
            "lens": force["lens"],
            "signature": force["signature"],
            "subtheme_count": subtheme_count,
            "evidence_slug_count": len(set(evidence_slugs)),
        }

    taxonomy = load_json(ROOT / "economic_intelligence_taxonomy.json")
    crosscut_lookup = {item["slug"]: item for item in taxonomy["crosscuts"]}
    company_lookup = {item["slug"]: item for item in load_json(ROOT / "company_universe.json")}
    brief_lookup = {item["slug"]: item for item in load_json(ROOT / "briefs_full.json")}
    return force_lookup, crosscut_lookup, company_lookup, brief_lookup


FORCE_FRAMES = {
    "the-hollow-middle": {
        "driver": "demand keeps separating into value-safe and premium-defensible positions",
        "pressure": "undifferentiated middle-market offers lose both pricing room and emotional clarity",
        "signal": "mix shifts toward either obvious value packs or visibly better premium tiers",
    },
    "the-channel-shift": {
        "driver": "discovery, comparison, and fulfillment are being reorganized by digital channels",
        "pressure": "operators that do not control demand or service convenience get commoditized faster",
        "signal": "traffic, basket construction, and repeat behavior move toward low-friction channels",
    },
    "the-margin-vise": {
        "driver": "input, labor, and service costs are staying elevated against selective customer willingness to pay",
        "pressure": "categories with weak differentiation get forced into promotion or mix deterioration",
        "signal": "operators lean harder on pricing architecture, pack-size changes, and cost takeout",
    },
    "the-health-reckoning": {
        "driver": "health behavior is moving from niche preference to mainstream social filter",
        "pressure": "legacy products and routines face reformulation pressure from wellness expectations",
        "signal": "protein, low-sugar, sober-curious, and health-tracking language becomes more central",
    },
    "the-experience-economy": {
        "driver": "status and discretionary spend are moving toward participation, memory, and live presence",
        "pressure": "generic goods and generic venues struggle to justify spend against curated experiences",
        "signal": "winners show stronger repeat visitation, programming leverage, and social shareability",
    },
    "the-graying-market": {
        "driver": "older households are becoming a larger and more economically decisive cohort",
        "pressure": "care intensity, mobility limits, and age-linked financial needs reshape category economics",
        "signal": "demand tilts toward chronic care, assistance, protection, and age-adapted convenience",
    },
    "the-labor-squeeze": {
        "driver": "scarce labor and wage pressure are forcing redesign in service and physical operations",
        "pressure": "throughput and quality become harder to defend when skilled labor is the bottleneck",
        "signal": "automation, scheduling discipline, retention tactics, and selective simplification accelerate",
    },
    "the-pricing-power-collapse": {
        "driver": "buyers with payer leverage or concentrated purchasing power are capping monetization",
        "pressure": "headline demand overstates actual return capture where reimbursement or procurement rules dominate",
        "signal": "margin performance diverges more from volume growth in payer-shaped sectors",
    },
    "the-compliance-tax": {
        "driver": "mandatory documentation, testing, privacy, and audit overhead keep thickening",
        "pressure": "more value accrues to those who can operationalize rule complexity at scale",
        "signal": "workflow software, certification, and managed compliance budgets keep deepening",
    },
    "the-fractional-worker": {
        "driver": "employment is becoming more modular, rented, and task-specific",
        "pressure": "traditional ladders, benefits, and firm-sponsored stability weaken at the edges first",
        "signal": "advisory retainers, project staffing, and portable admin layers gain relevance",
    },
    "the-compute-super-cycle": {
        "driver": "AI and compute demand are simultaneously compressing workflows and straining physical infrastructure",
        "pressure": "capital, power, and data-center access become competitive variables rather than background inputs",
        "signal": "automation budgets, inference demand, and power-ready site competition keep rising",
    },
    "atoms-strike-back": {
        "driver": "physical supply chains, manufacturing capacity, and infrastructure have regained strategic value",
        "pressure": "operators are re-exposed to land, freight, material, and plant constraints",
        "signal": "domestic capability, logistics resilience, and buildout bottlenecks matter more in valuation",
    },
    "commodity-whiplash": {
        "driver": "volatile material and energy inputs are transmitting instability into downstream pricing",
        "pressure": "thin-margin models are less able to absorb policy or commodity shocks cleanly",
        "signal": "sourcing optionality and contract discipline become visibly more strategic",
    },
    "the-real-estate-reckoning": {
        "driver": "the value of place is being repriced by rates, hybrid work, logistics, and compute demand",
        "pressure": "commodity space loses relevance while utility-linked or flow-linked sites gain rent",
        "signal": "adaptive reuse, housing lock-in, and power-adjacent land become recurring decision points",
    },
    "the-great-consolidation": {
        "driver": "ownership scale is increasingly rewarded in sectors burdened by complexity",
        "pressure": "independent operators face rising disadvantages in procurement, software, and compliance",
        "signal": "platform control, roll-ups, and centralized purchasing keep widening the gap",
    },
    "money-gets-unbundled": {
        "driver": "financial products, risk management, and payment rails are fragmenting into specialized layers",
        "pressure": "intermediaries without privileged data, trust, or embedded distribution lose ground",
        "signal": "verification, underwriting precision, and workflow adjacency become stronger moats",
    },
}


def lower_first(text: str) -> str:
    if not text:
        return ""
    return text[0].lower() + text[1:]


def clean_text(text: str) -> str:
    value = str(text or "")
    value = re.sub(r"<[^>]+>", " ", value)
    value = html.unescape(value)
    value = re.sub(r"\s+", " ", value).strip()
    value = value.replace("uS ", "US ").replace("aI ", "AI ")
    value = re.sub(r"(?<![A-Za-z])us\b", "US", value, flags=re.IGNORECASE)
    value = re.sub(r"(?<![A-Za-z])ai\b", "AI", value, flags=re.IGNORECASE)
    value = re.sub(r"(?<![A-Za-z])u\.s\.\b", "U.S.", value, flags=re.IGNORECASE)
    return value


def sentence_ready(text: str) -> str:
    value = clean_text(text).rstrip(".")
    if not value:
        return ""
    return value[0].upper() + value[1:]


def sentence_tail(text: str) -> str:
    value = clean_text(text).rstrip(".")
    if not value:
        return ""
    return lower_first(value)


def join_titles(items: list[dict], fallback: str, limit: int = 3) -> str:
    titles = [item.get("title", "") for item in items if item.get("title")]
    if not titles:
        return fallback
    titles = titles[:limit]
    if len(titles) == 1:
        return titles[0]
    if len(titles) == 2:
        return f"{titles[0]} and {titles[1]}"
    return f"{', '.join(titles[:-1])}, and {titles[-1]}"


def join_strings(items: list[str], fallback: str, limit: int = 3) -> str:
    values = [item for item in items if item]
    if not values:
        return fallback
    values = values[:limit]
    if len(values) == 1:
        return values[0]
    if len(values) == 2:
        return f"{values[0]} and {values[1]}"
    return f"{', '.join(values[:-1])}, and {values[-1]}"


def force_phrase(forces: list[dict], limit: int = 3) -> tuple[str, str]:
    labels = []
    for force in forces[:limit]:
        title = clean_text(force.get("title", "")).strip().lower()
        if title:
            labels.append(title)
    if not labels:
        return "multiple linked forces", "are"
    phrase = join_strings(labels, "multiple linked forces", limit=limit)
    verb = "is" if len(labels) == 1 else "are"
    return phrase, verb


def sector_phrase(industries: list[dict]) -> str:
    sectors = []
    for item in industries:
        sector = item.get("sector", "").strip()
        if sector and sector not in sectors:
            sectors.append(sector)
    if not sectors:
        return "multiple parts of the economy"
    if len(sectors) == 1:
        return sectors[0].lower()
    if len(sectors) == 2:
        return f"{sectors[0].lower()} and {sectors[1].lower()}"
    return f"{', '.join(sector.lower() for sector in sectors[:2])}, and adjacent sectors"


def build_subtheme_deep_read(theme: dict, subtheme: dict, industries: list[dict], companies: list[dict], forces: list[dict]) -> str:
    micro_a = subtheme["microthemes"][0] if subtheme["microthemes"] else "category behavior"
    micro_b = subtheme["microthemes"][1] if len(subtheme["microthemes"]) > 1 else micro_a
    force_mix, force_verb = force_phrase(forces, limit=2)
    sectors = sector_phrase(industries)
    company_mix = join_titles(companies, "scaled operators", limit=3)
    implication = lower_first(subtheme["operator_implications"][0].rstrip(".")) if subtheme["operator_implications"] else "execution discipline matters more"
    return (
        f"{micro_a.capitalize()} and {micro_b} are no longer isolated category quirks. "
        f"They are showing up across {sectors}, where {force_mix} {force_verb} changing the operating baseline. "
        f"That pushes the category toward a world where {implication}. "
        f"The pattern is already visible in example operators such as {company_mix}."
    )


def build_subtheme_drivers(subtheme: dict, forces: list[dict]) -> list[str]:
    drivers = []
    for item in subtheme["microthemes"][:2]:
        drivers.append(f"Demand and behavior are reorganizing around {item}.")
    for force in forces[:2]:
        frame = FORCE_FRAMES.get(force["slug"])
        if frame:
            drivers.append(sentence_ready(frame["driver"]) + ".")
    return drivers[:4]


def build_subtheme_pressure_points(subtheme: dict, industries: list[dict], forces: list[dict]) -> list[str]:
    points = []
    for item in industries[:2]:
        sector = item.get("sector", "the category").lower()
        one_sentence = sentence_tail(item.get("one_sentence", "baseline customer expectations"))
        points.append(f"{sector.capitalize()} operators have to absorb this shift in a market where {one_sentence}.")
    for force in forces[:2]:
        frame = FORCE_FRAMES.get(force["slug"])
        if frame:
            points.append(sentence_ready(frame["pressure"]) + ".")
    return points[:4]


def build_subtheme_signals(subtheme: dict, industries: list[dict], companies: list[dict], forces: list[dict]) -> list[str]:
    signals = []
    for force in forces[:2]:
        frame = FORCE_FRAMES.get(force["slug"])
        if frame:
            signals.append(sentence_ready(frame["signal"]) + ".")
    if companies:
        advantaged = sum(1 for item in companies if item.get("status") == "advantaged")
        exposed = sum(1 for item in companies if item.get("status") == "exposed")
        signals.append(
            f"Company mix is already separating, with {advantaged} advantaged examples and {exposed} exposed examples inside this subtheme set."
        )
    if industries:
        signals.append(
            f"Watch whether evidence industries such as {join_titles(industries, 'linked industries', limit=2)} start treating this as a planning assumption rather than a side case."
        )
    return signals[:4]


def build_subtheme_consequences(subtheme: dict) -> list[str]:
    items = []
    for implication in subtheme["operator_implications"][:3]:
        items.append(implication)
    if subtheme["microthemes"]:
        items.append(
            f"The second-order read is that {subtheme['microthemes'][0]} stops being anecdotal and starts altering category structure."
        )
    return items[:4]


def build_subtheme_market_rewrites(subtheme: dict, industries: list[dict], companies: list[dict]) -> list[str]:
    rewrites = []
    if industries:
        rewrites.append(
            f"Evidence industries such as {join_titles(industries, 'linked industries', limit=3)} increasingly have to budget, merchandise, or position around this pattern as a baseline assumption."
        )
    if companies:
        rewrites.append(
            f"Named companies such as {join_titles(companies, 'example operators', limit=3)} show that this is no longer a niche edge case but a live separator in competitive positioning."
        )
    for item in subtheme["microthemes"][:2]:
        rewrites.append(f"Category economics get rewritten as {item} moves from localized behavior into default customer or operator expectation.")
    return rewrites[:4]


def build_subtheme_stakeholders(subtheme: dict, industries: list[dict], companies: list[dict]) -> list[str]:
    stakeholders = []
    if industries:
        sectors = sector_phrase(industries)
        stakeholders.append(f"Frontline operators in {sectors} feel the change first because they have to translate it into pricing, staffing, assortment, or service design.")
    if companies:
        stakeholders.append(
            f"Scaled operators such as {join_titles(companies, 'named companies', limit=2)} can often operationalize the shift faster than smaller rivals because they have more room to test, absorb, and signal the new behavior."
        )
    for implication in subtheme["operator_implications"][:2]:
        stakeholders.append(f"Management teams are being pushed toward a clearer posture: {lower_first(implication.rstrip('.'))}.")
    return stakeholders[:4]


def build_subtheme_counterforces(subtheme: dict, forces: list[dict]) -> list[str]:
    counterforces = []
    for force in forces[:2]:
        frame = FORCE_FRAMES.get(force["slug"])
        if frame:
            counterforces.append(
                f"This subtheme still faces resistance because {lower_first(frame['pressure'].rstrip('.'))}."
            )
    if subtheme["microthemes"]:
        counterforces.append(
            f"The pattern is directionally strong, but adoption can remain uneven when {subtheme['microthemes'][-1]} is still category-specific rather than universal."
        )
    return counterforces[:4]


def build_subtheme_follow_on_effects(subtheme: dict, industries: list[dict]) -> list[str]:
    effects = []
    for item in industries[:2]:
        title = item.get("title", "linked industries")
        one_sentence = sentence_tail(item.get("one_sentence", "category structure changes"))
        effects.append(f"In {title}, this tends to show up as a second-order consequence where {one_sentence}.")
    for implication in subtheme["operator_implications"][:2]:
        effects.append(f"Over time this creates a broader market consequence: {lower_first(implication.rstrip('.'))}.")
    return effects[:4]


def build_theme_tensions(theme: dict) -> list[str]:
    first = theme["subthemes"][0]["title"] if theme["subthemes"] else theme["title"]
    second = theme["subthemes"][1]["title"] if len(theme["subthemes"]) > 1 else theme["title"]
    thesis = clean_text(theme["thesis"]).rstrip(".")
    return [
        f"The central tension inside {theme['title']} is that {lower_first(thesis)}, but the route to capturing that demand runs through the practical frictions surfaced by {first}.",
        f"A second tension sits between household or institutional demand and the operating constraints surfaced by {second}.",
        "The durable winners are usually the operators that can make the new behavior legible, routinized, and economically repeatable.",
    ]


def build_theme_signals(theme: dict) -> list[str]:
    signals = []
    seen = set()
    for subtheme in theme["subthemes"]:
        for signal in subtheme.get("signals_to_watch", [])[:1]:
            if signal not in seen:
                seen.add(signal)
                signals.append(signal)
            if len(signals) == 4:
                return signals
    return signals


def build_theme_deep_read(theme: dict, subthemes: list[dict], forces: list[dict], industries: list[dict], companies: list[dict]) -> str:
    first = subthemes[0]["title"] if subthemes else theme["title"]
    second = subthemes[1]["title"] if len(subthemes) > 1 else first
    force_mix, force_verb = force_phrase(forces, limit=3)
    sectors = sector_phrase(industries)
    company_mix = join_titles(companies, "scaled operators", limit=3)
    return (
        f"{theme['title']} is not one isolated trend. It is a system-level pattern showing up across {sectors}, where {force_mix} {force_verb} reinforcing one another. "
        f"The practical expression runs through subthemes such as {first} and {second}, which show how the same macro pressure gets translated into behavior, operating choices, and market structure. "
        f"The pattern is already legible in named companies such as {company_mix}, but the bigger point is that this theme now behaves like a planning assumption rather than a niche thesis."
    )


def build_theme_core_mechanisms(theme: dict, subthemes: list[dict], forces: list[dict]) -> list[str]:
    mechanisms = []
    for force in forces[:3]:
        frame = FORCE_FRAMES.get(force["slug"])
        if frame:
            mechanisms.append(sentence_ready(frame["driver"]) + ".")
    for subtheme in subthemes[:2]:
        mechanisms.append(f"{subtheme['title']} translates the macro shift into a repeatable operating pattern rather than a one-off anecdote.")
    return mechanisms[:5]


def build_theme_implications(theme: dict, subthemes: list[dict]) -> list[str]:
    implications = []
    for subtheme in subthemes[:3]:
        if subtheme["strategic_consequences"]:
            implications.append(
                f"{subtheme['title']} implies that {lower_first(subtheme['strategic_consequences'][0].rstrip('.'))}."
            )
    implications.append(
        "The common winner profile is the operator that can make the new behavior easier to understand, easier to repeat, and easier to monetize than peers can."
    )
    return implications[:4]


def build_theme_stakeholder_map(theme: dict, industries: list[dict], companies: list[dict]) -> list[str]:
    stakeholder_map = []
    stakeholder_map.append(
        f"Households, workers, and local operators feel {theme['title']} as a daily-life change before public narratives fully catch up."
    )
    if industries:
        stakeholder_map.append(
            f"Evidence industries spanning {sector_phrase(industries)} show that the adjustment burden is distributed across frontline service, distribution, and institutional categories."
        )
    if companies:
        stakeholder_map.append(
            f"Large operators such as {join_titles(companies, 'named companies', limit=3)} often capture the upside faster because they have more control over pricing, process, and customer communication."
        )
    stakeholder_map.append(
        "Investors and executives should read this theme as a structure question first: who absorbs the friction, who routinizes the new behavior, and who owns the bottleneck."
    )
    return stakeholder_map[:4]


def build_theme_second_order_effects(theme: dict, subthemes: list[dict]) -> list[str]:
    effects = []
    for subtheme in subthemes[:3]:
        if subtheme["market_rewrites"]:
            effects.append(
                f"{subtheme['title']} pushes second-order effects beyond the immediate category, especially where {lower_first(subtheme['market_rewrites'][0].rstrip('.'))}."
            )
    effects.append(
        "As these subthemes compound, the market starts rewarding operators built for the new regime and punishing those still organized around the old one."
    )
    return effects[:4]


def build_theme_records():
    force_lookup, crosscut_lookup, company_lookup, brief_lookup = build_lookups()
    theme_records = []

    for theme in THEMES:
        subtheme_records = []
        theme_industries = set()
        theme_companies = set()
        microtheme_total = 0
        theme_industry_records = []
        theme_company_records = []

        for subtheme in theme["subthemes"]:
            microtheme_total += len(subtheme["microthemes"])
            industries = [brief_lookup[slug] for slug in subtheme["industries"] if slug in brief_lookup]
            companies = [company_lookup[slug] for slug in subtheme["companies"] if slug in company_lookup]
            linked_forces = [force_lookup[slug] for slug in subtheme["forces"] if slug in force_lookup]
            deep_read = build_subtheme_deep_read(theme, subtheme, industries, companies, linked_forces)
            structural_drivers = build_subtheme_drivers(subtheme, linked_forces)
            pressure_points = build_subtheme_pressure_points(subtheme, industries, linked_forces)
            signals_to_watch = build_subtheme_signals(subtheme, industries, companies, linked_forces)
            strategic_consequences = build_subtheme_consequences(subtheme)
            market_rewrites = build_subtheme_market_rewrites(subtheme, industries, companies)
            stakeholder_map = build_subtheme_stakeholders(subtheme, industries, companies)
            counterforces = build_subtheme_counterforces(subtheme, linked_forces)
            follow_on_effects = build_subtheme_follow_on_effects(subtheme, industries)
            theme_industries.update(item["slug"] for item in industries)
            theme_companies.update(item["slug"] for item in companies)
            theme_industry_records.extend(industries)
            theme_company_records.extend(companies)
            subtheme_records.append(
                {
                    "slug": subtheme["slug"],
                    "title": subtheme["title"],
                    "summary": subtheme["summary"],
                    "deep_read": deep_read,
                    "microthemes": subtheme["microthemes"],
                    "structural_drivers": structural_drivers,
                    "pressure_points": pressure_points,
                    "signals_to_watch": signals_to_watch,
                    "strategic_consequences": strategic_consequences,
                    "market_rewrites": market_rewrites,
                    "stakeholder_map": stakeholder_map,
                    "counterforces": counterforces,
                    "follow_on_effects": follow_on_effects,
                    "operator_implications": subtheme["operator_implications"],
                    "forces": linked_forces,
                    "industries": [
                        {
                            "slug": item["slug"],
                            "title": item["title"],
                            "sector": item.get("sector", ""),
                            "one_sentence": sentence_ready(item.get("one_sentence", "")),
                        }
                        for item in industries
                    ],
                    "companies": [
                        {
                            "slug": item["slug"],
                            "title": item["title"],
                            "status": item.get("status", "mixed"),
                            "cluster": item.get("business_model_cluster_title", ""),
                            "top_themes": item.get("top_themes", [])[:4],
                        }
                        for item in companies
                    ],
                }
            )

        company_status_counts = {"advantaged": 0, "mixed": 0, "exposed": 0}
        for slug in theme_companies:
            status = company_lookup.get(slug, {}).get("status", "mixed")
            company_status_counts[status] = company_status_counts.get(status, 0) + 1

        theme_records.append(
            {
                "slug": theme["slug"],
                "title": theme["title"],
                "lens": theme["lens"],
                "thesis": sentence_ready(theme["thesis"]),
                "why_now": sentence_ready(theme["why_now"]),
                "questions": theme["questions"],
                "forces": [force_lookup[slug] for slug in theme["forces"] if slug in force_lookup],
                "crosscuts": [crosscut_lookup[slug] for slug in theme["crosscuts"] if slug in crosscut_lookup],
                "subthemes": subtheme_records,
                "deep_read": build_theme_deep_read(theme, subtheme_records, [force_lookup[slug] for slug in theme["forces"] if slug in force_lookup], theme_industry_records, theme_company_records),
                "core_mechanisms": build_theme_core_mechanisms(theme, subtheme_records, [force_lookup[slug] for slug in theme["forces"] if slug in force_lookup]),
                "strategic_implications": build_theme_implications(theme, subtheme_records),
                "stakeholder_map": build_theme_stakeholder_map(theme, theme_industry_records, theme_company_records),
                "second_order_effects": build_theme_second_order_effects(theme, subtheme_records),
                "structural_tensions": build_theme_tensions({"title": theme["title"], "thesis": sentence_ready(theme["thesis"]), "subthemes": subtheme_records}),
                "signals_to_watch": build_theme_signals({"subthemes": subtheme_records}),
                "subtheme_count": len(subtheme_records),
                "microtheme_count": microtheme_total,
                "signal_count": sum(len(subtheme["signals_to_watch"]) for subtheme in subtheme_records),
                "evidence_industry_count": len(theme_industries),
                "example_company_count": len(theme_companies),
                "company_status_counts": company_status_counts,
            }
        )

    return theme_records


MAIN_CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--green:#78ca90;--red:#e07d6d;--blue:#7cb0ea;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.55}.wrap{max-width:1200px;margin:0 auto;padding:30px clamp(16px,4vw,42px) 80px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:32px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.5rem,5vw,4.3rem);line-height:.98;margin:.18em 0 .22em;max-width:12ch}h2{font-size:1.55rem;margin:0 0 .45em}.sub{max-width:900px;color:var(--muted);font-size:1.06rem}.strip{display:flex;flex-wrap:wrap;gap:10px;margin-top:22px}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:128px}.kpi .n{font-family:var(--mono);font-size:1.35rem;font-weight:700}.kpi .l{font-size:.68rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:28px 0}.lead p{margin:0;font-size:1.06rem}.section{margin-top:32px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:14px}.card,.story{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.card h3,.story h3{margin:.2em 0 .35em;font-size:1.15rem}.card p,.story p{margin:.35em 0 0;color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.stats{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:14px}.stat{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:10px 12px}.stat .n{font-family:var(--mono);font-size:1.05rem;font-weight:700}.stat .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:3px}.qlist{padding-left:18px;color:var(--muted);margin:.5em 0 0}.qlist li{margin:.45em 0}.storygrid{display:grid;grid-template-columns:1.1fr .9fr;gap:16px}.summary{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.summary h3{margin:0 0 .5em;font-size:1.08rem}.summary p{margin:0;color:var(--muted)}@media(max-width:880px){.storygrid{grid-template-columns:1fr}}
"""


THEME_CSS = """
:root{--bg:#0f141b;--panel:#171f29;--panel2:#1e2935;--line:#2a3644;--ink:#f1eadc;--muted:#a9b2be;--faint:#73808e;--gold:#d5ac57;--green:#78ca90;--red:#e07d6d;--mono:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;--sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font-family:var(--sans);line-height:1.58}.wrap{max-width:1160px;margin:0 auto;padding:28px clamp(16px,4vw,42px) 80px}a{color:var(--gold);text-decoration:none}.top{display:flex;gap:18px;flex-wrap:wrap;font-family:var(--mono);font-size:.78rem;margin-bottom:26px}.eyebrow{font-family:var(--mono);font-size:.72rem;color:var(--gold);letter-spacing:.16em;text-transform:uppercase}h1{font-size:clamp(2.3rem,5vw,4rem);line-height:1;margin:.18em 0 .18em;max-width:12ch}h2{font-size:1.35rem;margin:0 0 .5em}.sub{max-width:900px;color:var(--muted);font-size:1.05rem}.lead{background:var(--panel);border:1px solid var(--line);border-left:4px solid var(--gold);border-radius:0 12px 12px 0;padding:18px 22px;margin:24px 0}.lead p{margin:0;font-size:1.04rem}.strip{display:flex;flex-wrap:wrap;gap:10px;margin:18px 0 0}.kpi{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px;min-width:128px}.kpi .n{font-family:var(--mono);font-size:1.3rem;font-weight:700}.kpi .l{font-size:.66rem;letter-spacing:.08em;text-transform:uppercase;color:var(--faint);margin-top:2px}.section{margin-top:30px;padding-top:14px;border-top:1px solid var(--line)}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:14px}.panel,.subtheme{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:18px}.meta{font-family:var(--mono);font-size:.68rem;color:var(--gold);letter-spacing:.08em;text-transform:uppercase}.panel h3,.subtheme h3{margin:.2em 0 .35em;font-size:1.1rem}.panel p,.subtheme p{margin:.35em 0 0;color:var(--muted)}.chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:12px}.chip{font-family:var(--mono);font-size:.68rem;color:var(--muted);border:1px solid var(--line);border-radius:999px;padding:4px 8px}.q{padding-left:18px;color:var(--muted)}.q li{margin:.42em 0}.subtheme{margin-top:14px}.split{display:grid;grid-template-columns:1.1fr .9fr;gap:14px;margin-top:14px}.list{padding-left:18px;color:var(--muted);margin:.35em 0 0}.list li{margin:.38em 0}.entity{background:var(--panel2);border:1px solid var(--line);border-radius:8px;padding:10px 12px}.entity h4{margin:0 0 .3em;font-size:.96rem}.entity p{margin:0;color:var(--muted);font-size:.9rem}.badge{font-family:var(--mono);font-size:.66rem;border-radius:999px;padding:3px 8px;display:inline-block;margin-top:7px;border:1px solid var(--line)}.adv{color:var(--green)}.mix{color:var(--muted)}.exp{color:var(--red)}@media(max-width:900px){.split{grid-template-columns:1fr}}
"""


def force_chip(force: dict, prefix: str = "") -> str:
    href = f"{prefix}forces/{force['slug']}/index.html" if prefix else f"forces/{force['slug']}/index.html"
    return f'<a class="chip" href="{e(href)}">{e(force["title"])}</a>'


def theme_card(theme: dict) -> str:
    force_links = "".join(force_chip(force) for force in theme["forces"])
    return f"""<article class="card">
  <div class="meta">{e(theme['lens'])}</div>
  <h3><a href="themes/{e(theme['slug'])}.html">{e(theme['title'])}</a></h3>
  <p>{e(theme['thesis'])}</p>
  <div class="stats">
    <div class="stat"><div class="n">{theme['subtheme_count']}</div><div class="l">Subthemes</div></div>
    <div class="stat"><div class="n">{theme['microtheme_count']}</div><div class="l">Second-order themes</div></div>
    <div class="stat"><div class="n">{theme['signal_count']}</div><div class="l">Signals</div></div>
    <div class="stat"><div class="n">{theme['evidence_industry_count']}</div><div class="l">Evidence industries</div></div>
    <div class="stat"><div class="n">{theme['example_company_count']}</div><div class="l">Example companies</div></div>
  </div>
  <div class="chips">{force_links}</div>
</article>"""


def build_main_page(theme_records: list[dict]) -> str:
    cards = "\n".join(theme_card(theme) for theme in theme_records)
    questions = "\n".join(
        f"<li>{e(question)}</li>"
        for theme in theme_records
        for question in theme["questions"][:1]
    )
    crosscuts = sorted({cut["title"] for theme in theme_records for cut in theme["crosscuts"]})
    crosscut_chips = "".join(f'<span class="chip">{e(item)}</span>' for item in crosscuts)
    microtheme_count = sum(theme["microtheme_count"] for theme in theme_records)
    subtheme_count = sum(theme["subtheme_count"] for theme in theme_records)
    signal_count = sum(theme["signal_count"] for theme in theme_records)

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>American Themes — US Industry Briefs</title><style>{MAIN_CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="index.html">Industry briefs</a><a href="economic-intelligence.html">Economic intelligence</a><a href="subthemes.html">Force subthemes</a><a href="company-universe.html">Company universe</a><a href="american-theme-memos.html">Theme memos</a></div>
<div class="eyebrow">American themes · US · 2025-2026</div>
<h1>American Themes</h1>
<p class="sub">This is the detailed themes layer the repo was missing: broad societal, cultural, consumer, industrial, and institutional themes, each broken into deep subthemes and second-order patterns, with links back to forces, industries, and named companies.</p>
<div class="strip">
  <div class="kpi"><div class="n">{len(theme_records)}</div><div class="l">Top-level themes</div></div>
  <div class="kpi"><div class="n">{subtheme_count}</div><div class="l">Subthemes</div></div>
  <div class="kpi"><div class="n">{microtheme_count}</div><div class="l">Second-order themes</div></div>
  <div class="kpi"><div class="n">{signal_count}</div><div class="l">Signals</div></div>
  <div class="kpi"><div class="n">1491</div><div class="l">Industry base</div></div>
</div>
<div class="lead"><p>The big picture is not just that the economy is changing. It is that daily life, business structure, and institutional behavior are changing together: households are splitting into value and premium, health is becoming a social norm engine, care is aging into a labor bottleneck, AI is turning into both a power trade and a workflow trade, and scale owners keep taking more of the spread created by complexity. This version adds a denser read inside each theme, with explicit drivers, pressure points, signals, and strategic consequences at the subtheme level.</p></div>

<section class="section">
  <h2>How To Read It</h2>
  <div class="storygrid">
    <div class="story">
      <h3>What This Layer Adds</h3>
      <p>The force map says what keeps repeating across industries. This themes layer says what those repetitions mean for American life: how people spend, how institutions ration, how firms hire, how place changes, and where power is concentrating.</p>
    </div>
    <div class="summary">
      <h3>Recurring Questions</h3>
      <ul class="qlist">{questions}</ul>
      <div class="chips">{crosscut_chips}</div>
    </div>
  </div>
</section>

<section class="section">
  <h2>Themes</h2>
  <div class="grid">{cards}</div>
</section>

<section class="section">
  <div class="card">
    <div class="meta">Narrative layer</div>
    <h3><a href="american-theme-briefs.html">American Theme Briefs</a></h3>
    <p>This is the written synthesis layer above the taxonomy: a long-form read on what each theme means, what tensions define it, and what signals matter next.</p>
  </div>
</section>

</div></body></html>"""


def company_badge(status: str) -> str:
    cls = "mix"
    if status == "advantaged":
        cls = "adv"
    elif status == "exposed":
        cls = "exp"
    return f'<span class="badge {cls}">{e(status)}</span>'


def build_theme_page(theme: dict) -> str:
    questions = "".join(f"<li>{e(question)}</li>" for question in theme["questions"])
    core_mechanisms = "".join(f"<li>{e(item)}</li>" for item in theme["core_mechanisms"])
    strategic_implications = "".join(f"<li>{e(item)}</li>" for item in theme["strategic_implications"])
    stakeholder_map = "".join(f"<li>{e(item)}</li>" for item in theme["stakeholder_map"])
    second_order_effects = "".join(f"<li>{e(item)}</li>" for item in theme["second_order_effects"])
    tensions = "".join(f"<li>{e(item)}</li>" for item in theme["structural_tensions"])
    watch_signals = "".join(f"<li>{e(item)}</li>" for item in theme["signals_to_watch"])
    force_links = "".join(force_chip(force, prefix="../") for force in theme["forces"])
    crosscut_chips = "".join(f'<span class="chip">{e(item["title"])}</span>' for item in theme["crosscuts"])
    subtheme_blocks = []

    for subtheme in theme["subthemes"]:
        microthemes = "".join(f'<span class="chip">{e(item)}</span>' for item in subtheme["microthemes"])
        force_chips = "".join(force_chip(force, prefix="../") for force in subtheme["forces"])
        driver_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["structural_drivers"])
        pressure_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["pressure_points"])
        signal_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["signals_to_watch"])
        consequence_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["strategic_consequences"])
        rewrite_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["market_rewrites"])
        stakeholder_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["stakeholder_map"])
        counterforce_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["counterforces"])
        follow_on_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["follow_on_effects"])
        industry_items = "".join(
            f"<li><b>{e(item['title'])}</b> <span class=\"meta\">{e(item['sector'])}</span><br>{e(item['one_sentence'])}</li>"
            for item in subtheme["industries"]
        )
        company_items = []
        for item in subtheme["companies"]:
            href = f"../company-pages/{item['slug']}.html"
            linked_title = f'<a href="{e(href)}">{e(item["title"])}</a>' if (ROOT / "company-pages" / f"{item['slug']}.html").exists() else e(item["title"])
            company_items.append(
                f"""<div class="entity">
  <h4>{linked_title}</h4>
  <p>{e(item['cluster'])}</p>
  {company_badge(item['status'])}
</div>"""
            )
        operator_items = "".join(f"<li>{e(item)}</li>" for item in subtheme["operator_implications"])
        subtheme_blocks.append(
            f"""<section class="subtheme" id="{e(subtheme['slug'])}">
  <div class="meta">{e(theme['title'])}</div>
  <h3>{e(subtheme['title'])}</h3>
  <p>{e(subtheme['summary'])}</p>
  <div class="panel">
    <div class="meta">Deeper read</div>
    <p>{e(subtheme['deep_read'])}</p>
  </div>
  <div class="chips">{microthemes}</div>
  <div class="chips">{force_chips}</div>
  <div class="split">
    <div class="panel">
      <div class="meta">Structural drivers</div>
      <ul class="list">{driver_items}</ul>
    </div>
    <div class="panel">
      <div class="meta">Pressure points</div>
      <ul class="list">{pressure_items}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Signals to watch</div>
      <ul class="list">{signal_items}</ul>
    </div>
    <div class="panel">
      <div class="meta">Strategic consequences</div>
      <ul class="list">{consequence_items}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Market rewrites</div>
      <ul class="list">{rewrite_items}</ul>
    </div>
    <div class="panel">
      <div class="meta">Stakeholder map</div>
      <ul class="list">{stakeholder_items}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Counterforces</div>
      <ul class="list">{counterforce_items}</ul>
    </div>
    <div class="panel">
      <div class="meta">Follow-on effects</div>
      <ul class="list">{follow_on_items}</ul>
    </div>
  </div>
  <div class="split">
    <div class="panel">
      <div class="meta">Evidence industries</div>
      <ul class="list">{industry_items}</ul>
    </div>
    <div class="panel">
      <div class="meta">Example companies</div>
      <div class="grid">{''.join(company_items)}</div>
    </div>
  </div>
  <div class="panel">
    <div class="meta">Operator implications</div>
    <ul class="list">{operator_items}</ul>
  </div>
</section>"""
        )

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(theme['title'])} — American Themes</title><style>{THEME_CSS}</style></head>
<body><div class="wrap">
<div class="top"><a href="../index.html">Industry briefs</a><a href="../economic-intelligence.html">Economic intelligence</a><a href="../american-themes.html">American themes</a><a href="../subthemes.html">Force subthemes</a></div>
<div class="eyebrow">{e(theme['lens'])} theme · US · 2025-2026</div>
<h1>{e(theme['title'])}</h1>
<p class="sub">{e(theme['why_now'])}</p>
<div class="strip">
  <div class="kpi"><div class="n">{theme['subtheme_count']}</div><div class="l">Subthemes</div></div>
  <div class="kpi"><div class="n">{theme['microtheme_count']}</div><div class="l">Second-order themes</div></div>
  <div class="kpi"><div class="n">{theme['signal_count']}</div><div class="l">Signals</div></div>
  <div class="kpi"><div class="n">{theme['evidence_industry_count']}</div><div class="l">Evidence industries</div></div>
  <div class="kpi"><div class="n">{theme['example_company_count']}</div><div class="l">Example companies</div></div>
</div>
<div class="lead"><p>{e(theme['thesis'])}</p></div>

<section class="section">
  <div class="panel">
    <div class="meta">Deep read</div>
    <p>{e(theme['deep_read'])}</p>
  </div>
</section>

<section class="section">
  <div class="grid">
    <div class="panel">
      <div class="meta">Questions</div>
      <ul class="q">{questions}</ul>
    </div>
    <div class="panel">
      <div class="meta">Core mechanisms</div>
      <ul class="q">{core_mechanisms}</ul>
    </div>
    <div class="panel">
      <div class="meta">Structural tensions</div>
      <ul class="q">{tensions}</ul>
    </div>
    <div class="panel">
      <div class="meta">Linked forces</div>
      <div class="chips">{force_links}</div>
      <div class="meta" style="margin-top:14px">Crosscuts</div>
      <div class="chips">{crosscut_chips}</div>
    </div>
    <div class="panel">
      <div class="meta">Signals to watch</div>
      <ul class="q">{watch_signals}</ul>
    </div>
    <div class="panel">
      <div class="meta">Strategic implications</div>
      <ul class="q">{strategic_implications}</ul>
    </div>
    <div class="panel">
      <div class="meta">Stakeholder map</div>
      <ul class="q">{stakeholder_map}</ul>
    </div>
    <div class="panel">
      <div class="meta">Second-order effects</div>
      <ul class="q">{second_order_effects}</ul>
    </div>
    <div class="panel">
      <div class="meta">Company mix</div>
      <div class="chips">
        <span class="chip">advantaged {theme['company_status_counts']['advantaged']}</span>
        <span class="chip">mixed {theme['company_status_counts']['mixed']}</span>
        <span class="chip">exposed {theme['company_status_counts']['exposed']}</span>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <h2>Subthemes</h2>
  {''.join(subtheme_blocks)}
</section>

</div></body></html>"""


def main() -> None:
    theme_records = build_theme_records()
    out = {
        "metadata": {
            "generated_at": "2026-08-09",
            "theme_count": len(theme_records),
            "subtheme_count": sum(theme["subtheme_count"] for theme in theme_records),
            "microtheme_count": sum(theme["microtheme_count"] for theme in theme_records),
            "signal_count": sum(theme["signal_count"] for theme in theme_records),
            "purpose": "Detailed societal, cultural, consumer, industrial, and institutional themes built on top of the industry, force, and company corpus.",
        },
        "themes": theme_records,
    }

    THEMES_DIR.mkdir(exist_ok=True)
    with JSON_OUT.open("w", encoding="utf-8") as handle:
        json.dump(out, handle, ensure_ascii=False, indent=2)
    with HTML_OUT.open("w", encoding="utf-8") as handle:
        handle.write(build_main_page(theme_records))
    for theme in theme_records:
        with (THEMES_DIR / f"{theme['slug']}.html").open("w", encoding="utf-8") as handle:
            handle.write(build_theme_page(theme))

    print(f"wrote {JSON_OUT}")
    print(f"wrote {HTML_OUT}")
    print(f"wrote theme pages to {THEMES_DIR}")
    print(
        f"themes={out['metadata']['theme_count']} "
        f"subthemes={out['metadata']['subtheme_count']} "
        f"microthemes={out['metadata']['microtheme_count']} "
        f"signals={out['metadata']['signal_count']}"
    )


if __name__ == "__main__":
    main()
