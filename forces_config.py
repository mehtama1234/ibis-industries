#!/usr/bin/env python3
"""Full taxonomy: 14 remaining forces, each with grouped subforces mapped to real evidence-industry slugs.
Each subforce = (subslug, title, "evidence slugs", angle)."""
import json, os
ROOT=os.path.dirname(os.path.abspath(__file__))

FORCES = [
{"slug":"the-graying-market","acc":"gold","lens":"Societal","title":"The Graying Market",
 "signature":"The boomers hit their care years — demand floods into everything age-related, but reimbursement cuts and a caregiver shortage cap the upside.",
 "groups":{
  "A · The body wears out":[
   ("joint-repair","Joint repair & surgery","orthopedic-products-manufacturing ambulatory-surgery-centers eye-surgery-clinics","Aging joints and eyes drive implant and outpatient-surgery volume; robotics is now standard of care but Medicare cuts squeeze the price."),
   ("the-senses-fade","When the senses fade","hearing-aid-manufacturing contact-lens-manufacturing glasses-and-contact-lens-manufacturing-in-the-us eyeglasses-and-contact-lens-stores-in-the-us","Hearing and vision decline create steady demand; OTC hearing aids and retail optical reshape who captures it."),
   ("chronic-care","The chronic-disease machine","dialysis-centers dialysis-equipment-manufacturing cardiologists","Kidney and heart disease scale with age into recurring, consolidated, reimbursement-dependent care."),
  ],
  "B · Care leaves the hospital":[
   ("senior-housing","Senior housing at scale","residential-senior-care-franchises","Boomer demand meets a bed shortage and a wage spiral; PE rolls up the fragment."),
   ("care-comes-home","Care comes home","home-care-providers-in-the-us","The money rewards keeping seniors out of facilities; home care booms but can't hire fast enough."),
   ("the-old-persons-specialists","The specialists of old age","dermatologists allergists chiropractors-in-the-us","Age-skewed outpatient specialties ride the demographic wave while fighting reimbursement pressure."),
  ],
  "C · The money side of aging":[
   ("longevity-insurance","Insuring a longer life","long-term-care-insurance life-insurance-and-annuities-in-the-us","Living longer turns into an annuity and long-term-care market — the balance-sheet side of aging."),
   ("the-drug-that-rewrote-aging","The drug that rewrote aging","weight-loss-services-in-the-us brand-name-pharmaceutical-manufacturing-in-the-us","GLP-1 drugs are the biggest force in aging health — remaking weight loss, cardio-metabolic care, and pharma."),
   ("grey-leisure","Grey leisure & the active old","hiking-and-outdoor-equipment-stores amusement-parks-in-the-us campgrounds-and-rv-parks-in-the-us","Wealthy, active retirees spend on experiences and the outdoors — a real growth pocket."),
  ],
  "D · The tensions":[
   ("who-pays","Who pays for all this","health-and-medical-insurance-in-the-us hmo-providers dental-insurance","Medicare Advantage and insurers hold the purse; benefit cuts and cost control cap every provider's pricing."),
   ("the-caregiver-shortage","The caregiver shortage","home-care-providers-in-the-us residential-senior-care-franchises","The binding constraint isn't demand — it's the aides and nurses to serve it, and wages spiral."),
  ],
  "E · The big picture":[
   ("the-graying-market","The graying market","orthopedic-products-manufacturing residential-senior-care-franchises long-term-care-insurance weight-loss-services-in-the-us","Capstone: aging is a guaranteed demand wave, but labor and reimbursement decide who actually profits."),
  ]}},

{"slug":"the-labor-squeeze","acc":"orange","lens":"Societal","title":"The Labor Squeeze",
 "signature":"Workers got scarce — wages spiral, the trades can't fill the gap, and whoever can automate or pay up wins while everyone else eats the margin hit.",
 "groups":{
  "A · The trades can't hire":[
   ("skilled-trades","The skilled-trades gap","electricians-in-the-us heating-and-air-conditioning-contractors-in-the-us roofing-contractors-in-the-us","An aging trades workforce and few new entrants push wages up faster than contractors can pass them on."),
   ("the-builders","The people who build things","masonry-in-the-us carpenters-in-the-us concrete-contractors-in-the-us","Construction demand meets a structural worker shortage; robots and prefab are the reluctant answer."),
   ("infrastructure-hands","Hands for the infrastructure boom","water-and-sewer-line-construction-in-the-us heavy-engineering-construction-in-the-us home-builders-in-the-us","Federal money and mandates create work, but the workers to do it are the bottleneck."),
  ],
  "B · Care work runs short":[
   ("the-care-crunch","The care-worker crunch","hospitals-in-the-us home-care-providers-in-the-us residential-senior-care-franchises","Nurses and aides are the scarce input in a demographically guaranteed-demand sector."),
   ("clinical-labor","Clinical labor everywhere","mental-health-and-substance-abuse-clinics-in-the-us gynecologists-and-obstetricians ambulatory-surgery-centers","Clinician shortages ripple through every corner of outpatient care."),
  ],
  "C · Moving things & serving people":[
   ("the-driver-shortage","The driver shortage","general-freight-trucking-truckload local-freight-trucking-in-the-us long-distance-refrigerated-trucking","Trucking's chronic driver churn collides with freight cycles; automation looms but isn't here yet."),
   ("aviation-labor","Aviation's people problem","domestic-airlines-in-the-us airport-operations-in-the-us airline-catering-services","Pilots, ground crew, and caterers are scarce and unionized; labor sets the cost floor."),
   ("hospitality-wages","The hospitality wage spiral","fast-food-restaurants-in-the-us chain-restaurants-in-the-us hotels-and-motels-in-the-us","Low-wage service work reprices upward; operators automate the counter or eat the margin."),
  ],
  "D · The responses":[
   ("automate-or-die","Automate or eat the margin","meat-beef-and-poultry-processing-in-the-us dairy-product-production-in-the-us vending-machine-operators-in-the-us","Where labor can be mechanized, it is; where it can't, margins compress."),
   ("the-wage-passthrough","Passing the wages on","coffee-and-snack-shops-in-the-us bars-and-nightclubs-in-the-us breweries-in-the-us","Service businesses try to pass wage inflation to customers — until price resistance bites."),
  ],
  "E · The big picture":[
   ("the-labor-squeeze","The labor squeeze","electricians-in-the-us home-care-providers-in-the-us general-freight-trucking-truckload fast-food-restaurants-in-the-us","Capstone: labor is the new scarce resource; automation, wages, and consolidation are the three ways out."),
  ]}},

{"slug":"the-fractional-worker","acc":"purple","lens":"Societal","title":"The Fractional Worker",
 "signature":"Permanent jobs unbundle into gigs, fractional roles, and expert networks — the firm rents talent by the hour, and the platform in the middle takes the cut.",
 "groups":{
  "A · Renting the expert":[
   ("expert-on-demand","The expert, on demand","expert-networks management-consulting-in-the-us","Companies rent senior judgment by the call or the project instead of hiring it full-time."),
   ("fractional-leaders","Fractional leadership","business-coaching-in-the-us executive-search-recruiters","Fractional CFOs, CMOs, and coaches replace full-time executives at smaller firms."),
   ("the-advice-business","Advice as a rented service","hr-consulting-in-the-us marketing-consultants environmental-consulting-in-the-us","Whole functions — HR, marketing, compliance — get rented from consultants instead of staffed."),
  ],
  "B · The platforms in the middle":[
   ("staffing-platforms","Who places the talent","executive-search-recruiters freight-forwarding-brokerages-and-agencies-in-the-us","Recruiters and brokers monetize the matching as work fragments."),
   ("the-credential-market","Selling the credential","business-certification-and-it-schools-in-the-us educational-services-in-the-us","Short-course and certification providers sell the fast credentials the gig market rewards."),
  ],
  "C · The tensions":[
   ("the-benefits-gap","The benefits gap","health-and-medical-insurance-in-the-us disability-insurance","Fractional work shifts benefits and stability onto the worker; insurers reprice the risk."),
   ("the-firm-thins","The firm gets thinner","law-firms-in-the-us accounting-services-in-the-us","Professional firms lean on contractors and offshoring, thinning the permanent core."),
  ],
  "E · The big picture":[
   ("the-fractional-worker","The fractional worker","expert-networks management-consulting-in-the-us business-coaching-in-the-us","Capstone: the unit of work shrinks from the job to the task; platforms and specialists win, stability loses."),
  ]}},

{"slug":"the-health-reckoning","acc":"red","lens":"Cultural","title":"The Health Reckoning",
 "signature":"GLP-1 drugs, the sober-curious wave, and the retreat from sugar are rewriting what people eat and drink — volume shrinks, and only the health-aligned or premium survive.",
 "groups":{
  "A · The drug that changed appetite":[
   ("the-glp1-shockwave","The GLP-1 shockwave","weight-loss-services-in-the-us brand-name-pharmaceutical-manufacturing-in-the-us","Weight-loss drugs cut appetite and are already reshaping food, drink, and weight-loss demand."),
   ("snacking-under-siege","Snacking under siege","candy-production-in-the-us ice-cream-production-in-the-us cookie-cracker-and-pasta-production-in-the-us","Indulgent, calorie-dense categories face structural demand pressure as appetites shrink and scrutiny rises."),
  ],
  "B · The retreat from alcohol":[
   ("sober-curious","The sober-curious wave","wine-bars breweries-in-the-us bars-and-nightclubs-in-the-us","Younger drinkers drink less; alcohol venues and makers face a structural, not cyclical, decline."),
   ("spirits-in-contraction","Spirits in contraction","whiskey-and-bourbon-distilleries distilleries-in-the-us","A boom-to-bust hangover: gluts, tariffs, and moderation hit premium spirits hard."),
  ],
  "C · The health-aligned winners":[
   ("functional-drinks","Functional & better-for-you drinks","energy-drink-production juice-production-in-the-us","Sugar-free, functional, and 'better-for-you' positioning is the only growth lane left in beverages."),
   ("the-diet-rewires","When diet meets convenience","meal-kit-delivery-services frozen-food-production-in-the-us","Health-conscious, convenient eating reshuffles who wins in packaged and prepared food."),
   ("what-you-drink-now","What you drink now","coffee-and-snack-shops-in-the-us dairy-product-production-in-the-us","Coffee, milk alternatives, and snacks reposition around health and premium to hold volume."),
  ],
  "D · The tensions":[
   ("fast-food-reckoning","Fast food's reckoning","fast-food-restaurants-in-the-us chain-restaurants-in-the-us","Value and indulgence collide with health scrutiny and GLP-1; chains reformulate or lose share."),
   ("regulation-and-warnings","Regulation & the warning label","energy-drink-production candy-production-in-the-us","Health warnings, sugar rules, and scrutiny become a cost and a repositioning trigger."),
  ],
  "E · The big picture":[
   ("the-health-reckoning","The health reckoning","weight-loss-services-in-the-us wine-bars energy-drink-production fast-food-restaurants-in-the-us","Capstone: wellness and weight-loss drugs shrink volume across food and drink; health-aligned and premium win, vice loses."),
  ]}},

{"slug":"the-hollow-middle","acc":"teal","lens":"Cultural","title":"The Hollow Middle",
 "signature":"The middle market collapses — shoppers split into premium and value, and anyone stuck selling undifferentiated mid-tier goods gets squeezed from both sides.",
 "groups":{
  "A · The stores splitting apart":[
   ("department-stores-fall","The department store falls","department-stores-in-the-us discount-department-stores","The mid-tier anchor of retail hollows out as shoppers go luxury or discount."),
   ("value-wins","The value floor","dollar-and-variety-stores-in-the-us convenience-stores-in-the-us ethnic-supermarkets","Trading down powers dollar, convenience, and value formats."),
   ("premium-holds","The premium ceiling","jewelry-stores-in-the-us beauty-cosmetics-and-fragrance-stores-in-the-us","Affluent shoppers keep spending on jewelry, beauty, and status goods."),
  ],
  "B · Apparel & footwear bifurcate":[
   ("apparel-split","Apparel splits","womens-clothing-stores-in-the-us mens-clothing-stores-in-the-us family-clothing-stores-in-the-us","Fast-fashion and luxury grow; mid-price apparel chains close."),
   ("footwear-and-niche","Footwear & the niche","athletic-shoe-stores shoe-stores-in-the-us lingerie-swimwear-and-bridal-stores-in-the-us","Specialty and athletic footwear thrive; generic mid-tier shoe retail shrinks."),
  ],
  "C · Eating & staying out":[
   ("dining-bifurcation","Dining bifurcates","chain-restaurants-in-the-us fast-food-restaurants-in-the-us","Casual-dining middle empties as diners split between cheap fast food and premium experiences."),
   ("hospitality-tiers","Hotels pick a lane","hotels-and-motels-in-the-us boutique-hotels extended-stay-hotels casino-hotels-in-the-us","Budget and luxury/experiential lodging grow; the mid-scale motel struggles."),
  ],
  "D · Experience & status":[
   ("experience-premium","Paying for the experience","amusement-parks-in-the-us movie-theaters-in-the-us concert-and-event-promotion-in-the-us","Consumers trade goods for experiences and premium live events."),
   ("the-dupe-economy","Value's revenge: the dupe","beauty-cosmetics-and-fragrance-stores-in-the-us health-stores-in-the-us","Cheap 'dupes' and private label eat the mainstream middle of consumer goods."),
  ],
  "E · The big picture":[
   ("the-hollow-middle","The hollow middle","department-stores-in-the-us dollar-and-variety-stores-in-the-us jewelry-stores-in-the-us chain-restaurants-in-the-us","Capstone: the middle market is hollowing out; luxury and value win, undifferentiated mid-tier loses."),
  ]}},

{"slug":"the-channel-shift","acc":"green","lens":"Cultural","title":"The Channel Shift",
 "signature":"The store stopped being where you buy — e-commerce, marketplaces, and direct-to-consumer hollow out physical retail, and only omnichannel or the experiential niche survives.",
 "groups":{
  "A · The categories that went online first":[
   ("electronics-online","Electronics go online","consumer-electronics-stores-in-the-us computer-stores-in-the-us camera-stores-in-the-us","Commodity electronics were the first to move online; specialty stores nearly vanished."),
   ("media-and-hobby","Media & hobby retail","book-stores-in-the-us art-supply-stores hardware-stores-in-the-us","Amazon and marketplaces gutted these categories; survivors go experiential and expert."),
   ("apparel-online","Apparel & the try-before-you-buy problem","womens-clothing-stores-in-the-us shoe-stores-in-the-us family-clothing-stores-in-the-us","Clothing and shoes shift online despite fit friction; stores become showrooms."),
  ],
  "B · The marketplace machine":[
   ("the-marketplace","The marketplace eats the middle","e-commerce-and-online-auctions-in-the-us","The platform takes a cut of everything and sets the terms of survival for sellers."),
   ("dtc-brands","Direct-to-consumer brands","beauty-cosmetics-and-fragrance-stores-in-the-us hiking-and-outdoor-equipment-stores","Brands sell straight to shoppers, cutting the retailer out entirely."),
  ],
  "C · Who's holding on":[
   ("omnichannel-or-die","Omnichannel or die","home-improvement-stores-in-the-us sporting-goods-stores-in-the-us auto-parts-stores-in-the-us","Big-box survivors fuse online and store — ship-from-store, buy-online-pickup — or lose."),
   ("the-experiential-niche","The experiential survivor","jewelry-stores-in-the-us health-stores-in-the-us convenience-stores-in-the-us","Expertise, immediacy, and experience are the moats physical retail has left."),
  ],
  "D · The tensions":[
   ("tariffs-and-de-minimis","Tariffs & the de-minimis end","womens-clothing-stores-in-the-us furniture-stores-in-the-us","Shein/Temu and the end of the de-minimis loophole reshape the price war online."),
   ("the-store-closures","The closure wave","department-stores-in-the-us discount-department-stores","Thousands of stores close a year; the real-estate and jobs fallout compounds."),
  ],
  "E · The big picture":[
   ("the-channel-shift","The channel shift","e-commerce-and-online-auctions-in-the-us womens-clothing-stores-in-the-us home-improvement-stores-in-the-us","Capstone: the point of sale moved online; platforms and omnichannel scale win, standalone mid-market stores lose."),
  ]}},

{"slug":"the-compute-super-cycle","acc":"green","lens":"Technological","title":"The Compute Super-Cycle",
 "signature":"AI's hunger for power is reshaping the grid and everything plugged into it — whoever has electricity, land, and cooling near the data centers wins a once-in-a-generation buildout.",
 "groups":{
  "A · Where the machines live":[
   ("the-data-center-rush","The data-center land rush","colocation-facilities data-processing-and-hosting-services-in-the-us","AI compute demand turns land, power, and cooling into the scarce inputs of the decade."),
   ("the-pipes","The pipes to the internet","internet-service-providers-in-the-us internet-hosting-services","Connectivity and hosting ride the same demand surge underneath the AI boom."),
   ("the-software-layer","The software that runs on top","business-analytics-and-enterprise-software-publishing-in-the-us database-storage-and-backup-software-publishing-in-the-us","Enterprise and data software monetize the compute build-out."),
  ],
  "B · The power scramble":[
   ("generation-scramble","The generation scramble","coal-and-natural-gas-power-in-the-us solar-power-in-the-us wind-power-in-the-us hydroelectric-power-in-the-us","Data centers need firm power now; gas, solar, wind, and hydro all get pulled in."),
   ("the-grid-bottleneck","The grid bottleneck","electric-power-transmission-in-the-us natural-gas-distribution-in-the-us gas-pipeline-transportation-in-the-us","Transmission and gas delivery — not generation — become the real constraint."),
  ],
  "C · The physical trades of the buildout":[
   ("the-electrical-trades","The electrical trades cash in","electricians-in-the-us heating-and-air-conditioning-contractors-in-the-us engine-and-turbine-manufacturing-in-the-us","Electricians, cooling contractors, and turbine makers are the picks-and-shovels of compute."),
   ("the-concrete-and-steel","Concrete, steel & the shell","commercial-building-construction-in-the-us cement-manufacturing-in-the-us","Data centers are also a construction-materials story — concrete, steel, and heavy build."),
  ],
  "D · The tensions":[
   ("power-scarcity","When power gets scarce","coal-and-natural-gas-power-in-the-us electric-power-transmission-in-the-us","Whoever can't get power — homes, factories, small ISPs — pays more or waits."),
   ("waste-heat-and-water","Heat, water & the environment","waste-to-energy-plant-operation hydroelectric-power-in-the-us","Cooling water and waste heat turn into constraints and opportunities."),
  ],
  "E · The big picture":[
   ("the-compute-super-cycle","The compute super-cycle","colocation-facilities coal-and-natural-gas-power-in-the-us electric-power-transmission-in-the-us electricians-in-the-us","Capstone: AI made electricity and land scarce again; the power-and-buildout chain is the trade of the decade."),
  ]}},

{"slug":"money-gets-unbundled","acc":"teal","lens":"Technological","title":"Money Gets Unbundled",
 "signature":"Banking leaves the banks — it's embedded in apps, cards, and platforms — and scale, data, and the rails win while regional players and middlemen get squeezed.",
 "groups":{
  "A · The core banks consolidate":[
   ("banking-scale","The scale game in banking","commercial-banking-in-the-us credit-unions-in-the-us industrial-banks-in-the-us","Deposits, tech, and compliance costs push banking toward a few giants."),
   ("the-card-rails","The rails that tax every swipe","credit-card-issuing-in-the-us credit-card-processing-and-money-transferring-in-the-us","Payment rails and card issuers take a cut of the whole economy's spending."),
   ("wall-street-machine","The Wall Street machine","investment-banking-and-securities-dealing-in-the-us custody-asset-and-securities-services-in-the-us","Capital markets and custody scale and financialize behind the scenes."),
  ],
  "B · Credit leaves the bank":[
   ("shadow-lending","Lending without a bank","loan-brokers-in-the-us invoice-factoring loan-administration-check-cashing-and-other-services-in-the-us","Non-bank and embedded lenders route credit around the traditional bank."),
   ("the-credit-graders","Who grades your credit","credit-bureaus-and-rating-agencies-in-the-us credit-repair-services credit-counselors-surveyors-and-appraisers-in-the-us","Scoring and rating is its own toll-taking layer, now AI-driven."),
  ],
  "C · Advice & the retail saver":[
   ("advice-commoditized","Advice gets commoditized","portfolio-management-in-the-us financial-planning-and-advice-in-the-us","Passive funds and robo-advice compress fees; scale and trust win."),
   ("the-money-movers","Moving and holding the money","commodity-dealing-and-brokerage-in-the-us custody-asset-and-securities-services-in-the-us","Brokerage, custody, and the float are quiet, scaled, rate-sensitive businesses."),
  ],
  "D · The tensions":[
   ("the-regional-squeeze","The regional-bank squeeze","commercial-banking-in-the-us credit-unions-in-the-us","Rate whiplash, a CRE loan wall, and tech costs pressure smaller banks toward mergers."),
   ("rate-sensitivity","Living and dying by the rate","invoice-factoring loan-brokers-in-the-us","Fed rate moves reprice the whole lending stack — the swing factor for margins."),
  ],
  "E · The big picture":[
   ("money-gets-unbundled","Money gets unbundled","commercial-banking-in-the-us credit-card-processing-and-money-transferring-in-the-us portfolio-management-in-the-us loan-brokers-in-the-us","Capstone: finance splinters out of banks into rails, apps, and platforms; scale and data win, middlemen lose."),
  ]}},

{"slug":"atoms-strike-back","acc":"orange","lens":"Industrial","title":"Atoms Strike Back",
 "signature":"Trade war and tariffs force reshoring, nearshoring, and inventory hoarding — physical supply chains get expensive and political, and whoever moves fastest to nearshore wins.",
 "groups":{
  "A · The auto reordering":[
   ("auto-tariff-shock","The auto tariff shock","auto-parts-manufacturing-in-the-us car-and-automobile-manufacturing-in-the-us automobile-engine-and-parts-manufacturing-in-the-us","2025 tariffs and the EV transition force the whole auto supply chain to reorder toward Mexico."),
   ("the-ev-transition","The EV transition & legacy parts","hybrid-and-electric-vehicle-manufacturing automobile-transmission-manufacturing-in-the-us automobile-steering-and-suspension-manufacturing-in-the-us","Electrification voids some parts and creates others; suppliers must pick a side."),
  ],
  "B · Heavy materials & metals":[
   ("metals-and-tariffs","Metals behind the tariff wall","iron-and-steel-manufacturing-in-the-us aluminum-manufacturing-in-the-us","Steel and aluminum tariffs ripple into every downstream builder and maker."),
   ("materials-of-everything","The materials of everything","chemical-product-manufacturing-in-the-us cement-manufacturing-in-the-us glass-product-manufacturing-in-the-us rubber-product-manufacturing-in-the-us","Basic materials get repriced by tariffs, energy, and reshoring."),
  ],
  "C · Reshoring the factory":[
   ("reshoring-advanced","Reshoring advanced manufacturing","3d-printer-manufacturing computer-manufacturing-in-the-us electrical-equipment-manufacturing-in-the-us","Defense, reshoring mandates, and supply-chain security pull advanced manufacturing home."),
   ("appliances-and-goods","Appliances & durable goods","major-household-appliance-manufacturing-in-the-us aircraft-engine-and-parts-manufacturing-in-the-us","Durable-goods makers weigh tariff costs against nearshoring and automation."),
  ],
  "D · Food & the retail edge":[
   ("food-supply-exposure","Food's tariff exposure","meat-beef-and-poultry-processing-in-the-us coffee-production-in-the-us soybean-processing","Food processing and ag ride commodity and trade-war volatility."),
   ("retail-import-shock","The retail import shock","womens-clothing-stores-in-the-us furniture-stores-in-the-us","Import-heavy retail eats tariff costs or passes them to shoppers."),
  ],
  "E · The big picture":[
   ("atoms-strike-back","Atoms strike back","auto-parts-manufacturing-in-the-us iron-and-steel-manufacturing-in-the-us 3d-printer-manufacturing soybean-processing","Capstone: the physical supply chain got political; nearshoring and domestic makers win, thin-margin importers lose."),
  ]}},

{"slug":"the-great-consolidation","acc":"purple","lens":"Industrial","title":"The Great Consolidation",
 "signature":"Capital rolls up fragmented Main Street — PE, franchises, REITs, and scale leaders absorb the independents, and financialization wins while owner-operators exit.",
 "groups":{
  "A · Rolling up healthcare":[
   ("pe-in-medicine","Private equity in medicine","dentists-in-the-us mental-health-and-substance-abuse-centers-in-the-us dialysis-centers","PE rolls up practices and clinics, chasing scale and billing power."),
   ("device-and-pharma-scale","Scale in devices & generics","medical-device-manufacturing-in-the-us generic-pharmaceutical-manufacturing-in-the-us orthopedic-products-manufacturing","Med-tech and generics consolidate to survive pricing pressure."),
  ],
  "B · Franchising Main Street":[
   ("franchise-rollups","The franchise roll-up","residential-senior-care-franchises chain-restaurants-in-the-us","Franchising and PE turn local services into scaled, financialized platforms."),
   ("services-consolidation","Consolidating boring services","funeral-adjacent" if False else "environmental-consulting-in-the-us engineering-services-in-the-us architects-in-the-us","Professional and boring-but-essential services get rolled into regional platforms."),
  ],
  "C · Scale in retail & food":[
   ("retail-scale","Scale wins in retail","home-improvement-stores-in-the-us auto-parts-stores-in-the-us sporting-goods-stores-in-the-us","A few big-box leaders capture the category; independents fold."),
   ("food-and-drink-scale","Scale in food & drink","breweries-in-the-us beer-wholesaling-in-the-us meat-beef-and-poultry-processing-in-the-us","Distribution and production consolidate; craft and independents get bought or squeezed."),
  ],
  "D · Capital owns the assets":[
   ("reits-own-it","REITs own the ground","commercial-real-estate-in-the-us apartment-rental-in-the-us land-leasing-in-the-us","Institutional capital owns the real assets and rents them back."),
   ("catalogs-as-assets","IP & catalogs as assets","music-publishing-in-the-us cable-networks-in-the-us","Rights and catalogs get financialized into yield-bearing assets."),
  ],
  "E · The big picture":[
   ("the-great-consolidation","The great consolidation","dentists-in-the-us residential-senior-care-franchises home-improvement-stores-in-the-us commercial-real-estate-in-the-us","Capstone: capital rolls up the fragmented economy; scale and financialization win, independent owners exit."),
  ]}},

{"slug":"the-real-estate-reckoning","acc":"gold","lens":"Industrial","title":"The Real-Estate Reckoning",
 "signature":"Hybrid work broke the office and higher rates broke the math — capital rotates from offices to logistics, data centers, and housing, and a debt wall forces the reckoning.",
 "groups":{
  "A · The office breaks":[
   ("the-office-crisis","The office crisis","commercial-real-estate-in-the-us architects-in-the-us","Hybrid work and vacancies gut office values; a maturity wall forces losses."),
   ("adaptive-reuse","Adaptive reuse & conversion","commercial-property-remodeling commercial-building-construction-in-the-us","Dead offices and malls get converted — a remodeling and construction opportunity."),
  ],
  "B · Where capital rotates":[
   ("housing-squeeze","The housing squeeze","home-builders-in-the-us apartment-rental-in-the-us","High rates freeze buying and pressure multifamily even as housing stays scarce."),
   ("logistics-and-data","Logistics & data centers","colocation-facilities heavy-engineering-construction-in-the-us","Capital flows to warehouses and data centers — the assets with demand."),
   ("the-land-play","Owning the land","land-leasing-in-the-us campgrounds-and-rv-parks-in-the-us","Land and ground-lease models become the quiet, durable real-estate bet."),
  ],
  "C · Hospitality & retail property":[
   ("hospitality-property","Hotels as real estate","hotels-and-motels-in-the-us casino-hotels-in-the-us boutique-hotels","Lodging bifurcates and gets financialized as an asset class."),
   ("retail-property","Retail's property fallout","department-stores-in-the-us discount-department-stores","Store closures dump retail real estate onto the market for reuse."),
  ],
  "D · The tensions":[
   ("the-debt-wall","The commercial-debt wall","commercial-real-estate-in-the-us commercial-banking-in-the-us","A wave of maturing CRE loans refinancing at higher rates is the sector's tail risk."),
   ("construction-costs","Building costs bite","commercial-building-construction-in-the-us home-builders-in-the-us","Tariffs, labor, and rates raise the cost to build anything new."),
  ],
  "E · The big picture":[
   ("the-real-estate-reckoning","The real-estate reckoning","commercial-real-estate-in-the-us apartment-rental-in-the-us colocation-facilities home-builders-in-the-us","Capstone: work and rates broke the old real-estate math; logistics, data, and housing win, offices lose."),
  ]}},

{"slug":"the-compliance-tax","acc":"blue","lens":"Industrial","title":"The Compliance Tax",
 "signature":"A patchwork of AI, privacy, climate, and cyber rules turns compliance into a rising cost — it favors scale, feeds the consultants, and prices out the small operator.",
 "groups":{
  "A · Finance under the rules":[
   ("banking-compliance","The bank compliance load","commercial-banking-in-the-us credit-card-issuing-in-the-us","Capital, KYC, and consumer rules make compliance a moat for big banks."),
   ("insurance-rules","Insurance & the regulators","health-and-medical-insurance-in-the-us cyber-liability-insurance workers-compensation-insurance","State-by-state rules and new risks make insurance a compliance-heavy, data-heavy game."),
  ],
  "B · Healthcare's paperwork":[
   ("healthcare-admin","Healthcare's paperwork machine","hospitals-in-the-us medical-device-manufacturing-in-the-us","Regulation and reimbursement rules make admin a huge, growing cost center."),
   ("data-and-privacy","Data, privacy & cyber","data-processing-and-hosting-services-in-the-us internet-service-providers-in-the-us internet-hosting-services","Privacy and cyber rules raise the cost of holding data — and create a security market."),
  ],
  "C · The compliance-industrial complex":[
   ("the-advisors","Who profits from the rules","law-firms-in-the-us audit-services accounting-services-in-the-us","Lawyers, auditors, and accountants sell the compliance the rules require."),
   ("environmental-rules","Environmental & climate rules","environmental-consulting-in-the-us waste-to-energy-plant-operation","Climate and environmental mandates create work and cost in equal measure."),
  ],
  "D · The tensions":[
   ("small-operator-squeeze","The small-operator squeeze","credit-repair-services business-certification-and-it-schools-in-the-us","Compliance cost is fixed, so it hits small firms hardest and pushes consolidation."),
   ("the-ai-rules","Governing the algorithms","business-analytics-and-enterprise-software-publishing-in-the-us credit-bureaus-and-rating-agencies-in-the-us","New AI-governance rules land first on data, credit, and software."),
  ],
  "E · The big picture":[
   ("the-compliance-tax","The compliance tax","commercial-banking-in-the-us hospitals-in-the-us law-firms-in-the-us data-processing-and-hosting-services-in-the-us","Capstone: rules multiply into a tax that favors scale and feeds advisors; small operators pay the most."),
  ]}},

{"slug":"the-margin-vise","acc":"red","lens":"Economic","title":"The Margin Vise",
 "signature":"Labor, materials, energy, and tariffs rise faster than pricing power — margins compress, and only the automated, the premium, or the locked-in escape the squeeze.",
 "groups":{
  "A · Food gets squeezed":[
   ("food-producers","The food-producer squeeze","bread-production-in-the-us dairy-product-production-in-the-us meat-beef-and-poultry-processing-in-the-us","Commodity, labor, and energy costs outrun what packaged-food makers can charge."),
   ("the-sweet-squeeze","The sweet-goods squeeze","candy-production-in-the-us ice-cream-production-in-the-us chocolate-production-in-the-us","Cocoa, sugar, and dairy inflation crush indulgent-category margins."),
  ],
  "B · Serving food at a loss-leader price":[
   ("restaurant-margins","The restaurant margin trap","fast-food-restaurants-in-the-us chain-restaurants-in-the-us coffee-and-snack-shops-in-the-us","Wage and food inflation collide with price-sensitive diners."),
   ("drinks-margins","The drinks squeeze","breweries-in-the-us beer-wholesaling-in-the-us juice-production-in-the-us","Input costs and flat demand compress beverage margins."),
  ],
  "C · Where the lock-in defends the margin":[
   ("the-lock-in-defense","The lock-in defense","cable-providers-in-the-us vending-machine-operators-in-the-us","Captive locations and bundles defend margin where switching is hard."),
   ("utility-like-margins","Utility-like resilience","waste-to-energy-plant-operation natural-gas-distribution-in-the-us","Regulated, contracted, or essential businesses hold margin better."),
  ],
  "D · The escape routes":[
   ("automate-the-cost","Automating the cost away","meat-beef-and-poultry-processing-in-the-us vending-machine-operators-in-the-us","Automation is the main lever left to protect margin from labor inflation."),
   ("premium-as-shield","Premium as the shield","coffee-and-snack-shops-in-the-us dairy-product-production-in-the-us","Trading up to premium is the other way to keep pricing power."),
  ],
  "E · The big picture":[
   ("the-margin-vise","The margin vise","bread-production-in-the-us fast-food-restaurants-in-the-us cable-providers-in-the-us","Capstone: costs rise faster than prices; automate, premiumize, or lock customers in — or watch margin vanish."),
  ]}},

{"slug":"the-pricing-power-collapse","acc":"red","lens":"Economic","title":"The Pricing-Power Collapse",
 "signature":"Medicare cuts and payer power strip pricing from providers and device makers — volume rises with aging, but the price per unit keeps falling, and only scale survives.",
 "groups":{
  "A · The providers get cut":[
   ("medicare-cuts","Death by reimbursement cut","dialysis-centers ambulatory-surgery-centers diagnostic-imaging-centers","Year after year, Medicare trims the rate while costs rise — a structural margin squeeze."),
   ("the-specialist-squeeze","The specialist squeeze","cardiologists dermatologists gynecologists-and-obstetricians","Specialists face flat reimbursement and rising costs, pushing them into groups."),
  ],
  "B · The makers get squeezed":[
   ("device-pricing","The device price grind","orthopedic-products-manufacturing dialysis-equipment-manufacturing medical-device-manufacturing-in-the-us","Hospital consolidation and payers grind device prices down 1-2% a year."),
   ("generic-deflation","Generic-drug deflation","generic-pharmaceutical-manufacturing-in-the-us","Relentless price erosion in generics rewards only the largest, lowest-cost makers."),
  ],
  "C · The payers hold the power":[
   ("payer-power","Who holds the purse","health-and-medical-insurance-in-the-us hmo-providers dental-insurance","Insurers and Medicare Advantage set prices and squeeze everyone downstream."),
   ("the-independent-exodus","The independent-practice exodus","dentists-in-the-us mental-health-and-substance-abuse-clinics-in-the-us","Solo and small practices sell to systems and PE to survive the pricing squeeze."),
  ],
  "D · The tensions":[
   ("volume-vs-price","Volume up, price down","hospitals-in-the-us home-care-providers-in-the-us","Aging drives volume, but falling per-unit prices and wage costs eat the gains."),
   ("value-based-shift","The value-based bet","hmo-providers ambulatory-surgery-centers","Shifting to value-based, lower-cost sites of care is the industry's escape hatch."),
  ],
  "E · The big picture":[
   ("the-pricing-power-collapse","The pricing-power collapse","dialysis-centers orthopedic-products-manufacturing generic-pharmaceutical-manufacturing-in-the-us health-and-medical-insurance-in-the-us","Capstone: reimbursement and payer power strip pricing from healthcare; volume grows but only scale survives."),
  ]}},
]

if __name__=='__main__':
    briefs={b['slug'] for b in json.load(open(f'{ROOT}/briefs_full.json'))}
    miss=set(); n_sub=0
    for f in FORCES:
        for g,subs in f['groups'].items():
            for tup in subs:
                slug,title,ev,angle=tup; n_sub+=1
                for e in ev.split():
                    if e not in briefs: miss.add((f['slug'],e))
    print(f"forces: {len(FORCES)} | subforces: {n_sub}")
    print("MISSING evidence slugs:", sorted(miss) or "none")
    json.dump([{k:v for k,v in f.items()} for f in FORCES], open(f'{ROOT}/_forces_all.json','w'), indent=1)
