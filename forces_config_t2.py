#!/usr/bin/env python3
"""Tranche-2 NEW forces the 521-industry dataset revealed (beyond the original 15). Same tuple format."""
FORCES = [
{"slug":"the-electrification","acc":"blue","lens":"Technological","title":"The Electrification",
 "signature":"The car goes electric and software-defined — and the whole century-old machine of engines, transmissions, gas, and exhaust starts dying while batteries, chips, and copper take over.",
 "groups":{
  "A · The engine's slow death":[
   ("engine-and-drivetrain","The engine & drivetrain","automobile-engine-and-parts-manufacturing-in-the-us automobile-transmission-manufacturing-in-the-us engine-rebuilding-and-remanufacturing","EVs have no engine or transmission; a huge legacy supply chain is on borrowed time."),
   ("exhaust-and-fuel","Exhaust, fuel & the gas station","catalytic-converter-manufacturing gas-stations-in-the-us gas-stations-with-convenience-stores-in-the-us","Catalytic converters, gas stations, and fuel retail lose their reason to exist as cars stop burning fuel."),
   ("the-aftermarket","The repair aftermarket","car-body-shops-in-the-us auto-parts-stores-in-the-us auto-parts-remanufacturing","EVs need far less maintenance; the oil-change and parts aftermarket shrinks."),
  ],
  "B · What replaces it":[
   ("the-battery","The battery is the new engine","battery-manufacturing-in-the-us lithium-battery-manufacturing battery-recycling","The battery becomes the most valuable part of the car — and a whole make-and-recycle industry with it."),
   ("car-electronics","The car becomes a computer","automobile-electronics-manufacturing-in-the-us circuit-board-and-electronic-component-manufacturing-in-the-us","Software and chips, not mechanical parts, now define the car."),
   ("the-copper-hunger","Electrification's hunger for copper","copper-nickel-lead-and-zinc-mining-in-the-us copper-rolling-drawing-and-extruding-in-the-us aluminum-manufacturing-in-the-us","EVs and the grid need two to three times the copper — a mining and metals tailwind."),
  ],
  "C · The ripple effects":[
   ("financing-and-leasing","Financing the switch","auto-leasing-loans-and-sales-financing-in-the-us fleet-car-leasing car-and-automobile-manufacturing-in-the-us","EV price and residual-value uncertainty reshapes auto lending and leasing."),
   ("insuring-the-ev","Insuring the EV","commercial-auto-insurance automobile-insurance auto-extended-warranty-providers","Higher repair costs and battery risk reprice auto insurance and warranties."),
  ],
  "E · The big picture":[
   ("the-electrification","The electrification","battery-manufacturing-in-the-us automobile-engine-and-parts-manufacturing-in-the-us gas-stations-in-the-us copper-nickel-lead-and-zinc-mining-in-the-us","Capstone: value migrates from the engine to the battery and the chip; copper and software win, fuel and mechanicals lose."),
  ]}},

{"slug":"the-breach-economy","acc":"red","lens":"Technological","title":"Cybersecurity & the Breach Economy",
 "signature":"Every business is now a data target — and the cost of getting breached spawns a whole economy of insurance, forensics, detection, and identity protection.",
 "groups":{
  "A · Insuring the risk":[
   ("cyber-insurance","Insuring the breach","cyber-liability-insurance identity-theft-insurance","Cyber risk became a fast-growing, hard-to-price insurance line."),
   ("identity-protection","Protecting the person","identity-theft-protection-services background-check-services","Consumer identity and vetting services scale with breach frequency and fraud."),
  ],
  "B · Detecting & cleaning up":[
   ("fraud-detection","Catching the fraud","fraud-detection-software-developers digital-forensic-services data-recovery-services","AI-enabled attacks meet AI-enabled fraud detection and after-the-fact forensics."),
   ("security-software","The security software layer","security-software-publishing-in-the-us biometrics-scan-software","Detection, identity, and access software is a structural growth market."),
  ],
  "C · Guarding the doors":[
   ("physical-security","Guarding the physical door","security-alarm-services-in-the-us security-services-in-the-us electronic-access-control-system-manufacturing","Physical and digital security converge into one spend."),
   ("who-advises","Who sells the compliance","it-consulting-in-the-us it-security-consulting","Consultants and IT services monetize the rising security and compliance burden."),
  ],
  "E · The big picture":[
   ("the-breach-economy","The breach economy","cyber-liability-insurance fraud-detection-software-developers digital-forensic-services security-software-publishing-in-the-us","Capstone: the cost of insecurity created a whole industry; insurers, security software, and forensics win."),
  ]}},

{"slug":"the-experience-economy","acc":"purple","lens":"Cultural","title":"The Experience Economy",
 "signature":"People spend less on owning things and more on doing things — the money moves from the shelf to the ticket, the table, and the night out.",
 "groups":{
  "A · Going out again":[
   ("nightlife","The night out","bars-and-nightclubs-in-the-us wine-bars karaoke-bars","Social venues sell the experience even as drinking itself declines."),
   ("play-and-compete","Play & compete","bowling-centers-in-the-us go-kart-racing-tracks paintball-fields pool-and-billiard-halls","Competitive-socializing venues turn an afternoon into a paid experience."),
  ],
  "B · Days out & escapes":[
   ("theme-and-parks","Theme parks & thrills","amusement-parks-in-the-us water-parks ice-rinks","Big-ticket days out keep pricing power as families trade goods for memories."),
   ("culture-and-nature","Culture & nature","museums-in-the-us zoos-and-aquariums historic-sites-in-the-us","Cultural and nature attractions ride the shift to meaningful outings."),
  ],
  "C · The premium night":[
   ("stay-and-celebrate","Staying & celebrating","boutique-hotels casino-hotels-in-the-us wedding-services-in-the-us","Boutique stays, casinos, and weddings sell the premium, once-in-a-while experience."),
   ("the-big-screen","The big screen fights back","movie-theaters-in-the-us concert-and-event-promotion-in-the-us","Theaters and live events survive by being an experience streaming can't copy."),
  ],
  "E · The big picture":[
   ("the-experience-economy","The experience economy","amusement-parks-in-the-us bars-and-nightclubs-in-the-us boutique-hotels movie-theaters-in-the-us","Capstone: spending shifts from stuff to experiences; venues and events win, commodity goods lose."),
  ]}},

{"slug":"the-immigration-squeeze","acc":"orange","lens":"Societal","title":"The Immigration Squeeze",
 "signature":"Whole industries quietly run on immigrant labor — so immigration policy and border enforcement, not wages alone, now decide who can staff the work at all.",
 "groups":{
  "A · Who grows and processes the food":[
   ("the-fields","The fields","agriculture-forestry-fishing-and-hunting-in-the-us fruit-and-nut-farming-in-the-us vegetable-farming-in-the-us","Farm work depends on immigrant labor; enforcement is an existential input risk."),
   ("the-plants","The processing plants","chicken-and-turkey-meat-production-in-the-us meat-beef-and-poultry-processing-in-the-us dairy-product-production-in-the-us","Meat and dairy plants run on the same labor pool — a hidden supply-chain fragility."),
  ],
  "B · Who builds and cleans":[
   ("the-trades","The building trades","masonry-in-the-us roofing-contractors-in-the-us drywall-and-insulation-installers-in-the-us","Construction trades are heavily immigrant-staffed; policy tightens an already-short labor market."),
   ("the-service-labor","The service labor","janitorial-services-in-the-us landscaping-services-in-the-us maids-nannies-and-gardeners-in-the-us","Cleaning, landscaping, and domestic work face the same sourcing squeeze."),
  ],
  "C · Who cares and who's detained":[
   ("care-labor","The care labor","home-care-providers-in-the-us nursing-care-facilities-in-the-us","Elder and health care lean on immigrant workers just as demand surges."),
   ("the-enforcement-complex","The enforcement complex","correctional-facilities-in-the-us background-check-services","Detention and vetting are the other, growing side of immigration policy."),
  ],
  "E · The big picture":[
   ("the-immigration-squeeze","The immigration squeeze","agriculture-forestry-fishing-and-hunting-in-the-us meat-beef-and-poultry-processing-in-the-us masonry-in-the-us home-care-providers-in-the-us","Capstone: labor availability is set by policy, not just pay; automated or higher-wage operators cope, labor-dependent ones don't."),
  ]}},

{"slug":"commodity-whiplash","acc":"gold","lens":"Economic","title":"Commodity Whiplash",
 "signature":"Mining, drilling, and growing move on violent price cycles set by geopolitics and weather — the extraction economy the country forgot it still runs on.",
 "groups":{
  "A · Digging it up":[
   ("metals-mining","Mining the metals","gold-and-silver-ore-mining-in-the-us copper-nickel-lead-and-zinc-mining-in-the-us iron-ore-mining-in-the-us","Metal miners live and die by global prices and the electrification demand wave."),
   ("the-quarry","Rock, sand & the quarry","stone-mining-in-the-us sand-and-gravel-mining-in-the-us mineral-and-phosphate-mining-in-the-us","Aggregates track construction demand and energy costs."),
   ("coal-and-decline","Coal & the managed decline","coal-mining-in-the-us","Coal rides a structural decline punctuated by data-center power spikes."),
  ],
  "B · Drilling & refining":[
   ("oil-and-gas","Oil & gas extraction","oil-drilling-and-gas-extraction-in-the-us oil-and-gas-field-services-in-the-us petroleum-refining-in-the-us","Drillers and refiners swing on crude prices and policy whiplash."),
   ("the-fuels","Fuels & petrochemicals","ethanol-fuel-production-in-the-us petrochemical-manufacturing-in-the-us gasoline-and-petroleum-wholesaling-in-the-us","Fuel and petrochemical makers pass through — or eat — volatile input costs."),
  ],
  "C · Growing it":[
   ("the-farm-cycle","The farm price cycle","agribusiness-in-the-us wheat-barley-and-sorghum-farming-in-the-us soybean-processing","Farmers and processors are whipsawed by commodity prices, tariffs, and weather."),
   ("fertilizer-and-inputs","Fertilizer & the inputs","fertilizer-manufacturing-in-the-us corn-wheat-and-soybean-wholesaling-in-the-us","Fertilizer and grain trading concentrate the commodity risk of the whole food chain."),
  ],
  "E · The big picture":[
   ("commodity-whiplash","Commodity whiplash","gold-and-silver-ore-mining-in-the-us oil-drilling-and-gas-extraction-in-the-us agribusiness-in-the-us fertilizer-manufacturing-in-the-us","Capstone: the extraction economy runs on violent price cycles; hedgers and consolidators survive, small single-commodity players don't."),
  ]}},
]
