#!/usr/bin/env python3
"""Append real, currently-ongoing situations to demo.html SEED (war-watch inspo).

Discipline (HORUS backbone): no verdict, all sides, real outlets, real opposition,
real timeline anchors. Content grounded to ~early 2026 knowledge; the truly-live
version is the GDELT/RSS/Groq feed phase, not this seed.

Reads the SEED block already in demo.html, appends NEW_EVENTS (dedupe by id),
sanitizes to ASCII hyphens, validates shape, rewrites the block in place.
"""
import json, re, sys, pathlib

HTML = pathlib.Path(r"C:/Users/adamk/Desktop/newvs/.work/horus-site/demo.html")

# ---- sanitize: ASCII hyphen only (Adam hard rule), straight quotes, ascii ellipsis ----
DASHES = {"—": "-", "–": "-", "‒": "-", "―": "-", "−": "-", "‐": "-", "‑": "-"}
DQUOTE = {"“": '"', "”": '"', "„": '"', "‟": '"'}
SQUOTE = {"‘": "'", "’": "'", "‚": "'", "‛": "'"}
ELLIP = {"…": "..."}
TABLE = {**DASHES, **DQUOTE, **SQUOTE, **ELLIP}
def clean(x):
    if isinstance(x, str):
        for k, v in TABLE.items():
            x = x.replace(k, v)
        return x
    if isinstance(x, list):
        return [clean(i) for i in x]
    if isinstance(x, dict):
        return {k: clean(v) for k, v in x.items()}
    return x

def C(src, kind, named, primacy, provenance, motive):
    return {"source": src, "kind": kind, "named": named, "primacy": primacy,
            "provenance": provenance, "motive": motive}

NEW_EVENTS = [
  {
    "id": "russia-ukraine-war-current",
    "title": "Russia-Ukraine War: Entrenched Front and the Negotiation Question",
    "scope": "conflict",
    "status": "developing",
    "watchers": 12000000,
    "geo": {"lat": 48.0, "lng": 37.8, "place": "Donbas front, eastern Ukraine"},
    "neutralLine": "Russia's full-scale invasion of Ukraine began on 24 February 2022. As of early 2026 fighting continues along an entrenched front in the east and south, with no negotiated settlement and active dispute over territorial control, casualty counts, and the effect of Western military support.",
    "claims": [
      {
        "statement": "Russia holds the battlefield initiative and the attritional advantage; without a major change in Western support, Ukraine cannot reverse Russian gains and a settlement on terms favourable to Moscow is the realistic trajectory.",
        "carriers": [
          C("Russian Ministry of Defence briefings", "state media", True, "secondary", "original", "Belligerent; incentive to project momentum and inevitability"),
          C("Realist Western analysts (e.g. John Mearsheimer)", "public debate", True, "secondary", "original", "Structural-realist framing; long-standing argument that Ukraine cannot win and the West provoked the war"),
          C("TASS / RT coverage", "state media", True, "secondary", "echo", "Amplify the Russian official line to domestic and foreign audiences"),
        ],
        "strongest": "Russia captured Avdiivka (Feb 2024) and made slow, costly gains across 2024-2025 while Ukraine faced manpower and ammunition shortfalls; the $61bn US aid package passed only after roughly six months of congressional delay (April 2024), showing the political fragility of Ukraine's supply.",
        "opposition": {
          "statement": "Russia's gains are measured in kilometres for enormous casualties and equipment loss; Ukraine retook about half the territory seized in 2022 (Kharkiv, Kherson), degraded the Black Sea Fleet, struck refineries deep in Russia, and held a foothold in Russia's Kursk region in 2024 - none of which fits a narrative of inevitable Russian victory.",
          "carriers": [
            C("Institute for the Study of War (ISW) daily assessments", "research paper", True, "secondary", "original", "Analytic institution; tracks tactical control with sourced maps"),
            C("Ukrainian General Staff", "official record", True, "primary", "original", "Belligerent; incentive to project resilience"),
            C("Reuters / AP frontline reporting", "wire service", True, "secondary", "original", "Agency reporting; standard war coverage"),
          ],
          "why": "An 'inevitable Russian victory' has been forecast since 2022 and repeatedly failed (Kyiv in 72 hours, the 2023 winter, a 2024 collapse). Attrition cuts both ways; Russian advances have not produced operational breakthrough or political capitulation, so the trajectory remains contested, not settled."
        }
      },
      {
        "statement": "The war has become a strategic stalemate that will end in a negotiated freeze along the current line of contact, similar to a Korea-style armistice.",
        "carriers": [
          C("US and European officials (anonymous briefings)", "official record", False, "secondary", "echo", "Manage expectations; prepare publics for a settlement"),
          C("Reuters / Financial Times analysis", "journalist", True, "secondary", "original", "Synthesis reporting on diplomatic prospects"),
          C("US administration statements pressing rapid ceasefire talks (2025)", "official record", True, "secondary", "original", "Stated priority to end the war quickly and reduce US expenditure"),
        ],
        "strongest": "Neither side achieved a decisive 2023-2024 breakthrough; front lines moved only marginally relative to the scale of forces committed, and the US administration that took office in January 2025 made ending the war a stated priority and pressed both sides toward talks.",
        "opposition": {
          "statement": "A freeze rewards the aggressor by legitimising occupation and gives Russia time to rearm; Ukraine and several European states argue an unenforced ceasefire is a pause before a larger war, not peace. Calling it a stalemate is itself a contested political act that pre-loads the outcome.",
          "carriers": [
            C("Ukrainian government statements", "official record", True, "primary", "original", "Rejects ceding sovereign territory; existential stake"),
            C("Baltic and Polish officials", "official record", True, "secondary", "original", "Front-line NATO states; view a frozen conflict as a direct security threat"),
            C("ISW analysis on Russian force reconstitution", "research paper", True, "secondary", "original", "Documents Russian rearmament and regeneration"),
          ],
          "why": "Stalemate is a snapshot, not a law. Frozen conflicts (Georgia 2008, Donbas 2015-2022) preceded renewed Russian escalation rather than ending it, so the premise that a freeze equals resolution is exactly what is in dispute."
        }
      }
    ],
    "timeline": [
      {"date": "2022-02-24", "event": "Russia launches a full-scale invasion; the assault on Kyiv fails within weeks.", "shift": "The war becomes a prolonged conventional conflict, not a quick coup."},
      {"date": "2022-09-11", "event": "Ukraine's Kharkiv counteroffensive recaptures roughly 12,000 sq km.", "shift": "Shatters the assumption of static Russian control; Western confidence rises."},
      {"date": "2022-11-11", "event": "Russia withdraws from Kherson city.", "shift": "Second major Ukrainian success; high-water mark of Ukrainian momentum."},
      {"date": "2023-06-08", "event": "Ukraine's southern counteroffensive begins; gains fall far short of expectations.", "shift": "Optimism deflates; attritional reality sets in."},
      {"date": "2024-02-17", "event": "Russia captures Avdiivka after months of assault.", "shift": "Initiative shifts to Russia amid a Ukrainian ammunition shortage."},
      {"date": "2024-04-24", "event": "US Congress passes a $61bn aid package after roughly six months of delay.", "shift": "Exposes the political fragility of the Western supply line."},
      {"date": "2024-08-06", "event": "Ukraine launches a cross-border incursion into Russia's Kursk region.", "shift": "Ukraine demonstrates offensive capability inside Russia, complicating the 'inevitable defeat' narrative."},
      {"date": "2025-01-20", "event": "A new US administration takes office prioritising rapid ceasefire diplomacy.", "shift": "Pressure for negotiations rises; the terms and the outcome remain contested."}
    ],
    "scenarios": [
      {
        "statement": "THEORY: A negotiated freeze in 2025-2026 along approximately the current lines, with Ukraine's NATO question deferred and sanctions partially traded.",
        "restsOn": ["The US administration's stated drive to end the war", "Battlefield stalemate with no breakthrough", "War fatigue in Western publics", "A Russian economy strained but not collapsing"],
        "note": "Marked theory, not a prediction. Falsified by a battlefield breakthrough or by either side refusing the line. A freeze is not a settlement and says nothing about durability."
      },
      {
        "statement": "THEORY: Protracted attrition continues into 2026 and beyond with no settlement, as neither side accepts the other's terms.",
        "restsOn": ["Maximalist war aims on both sides", "Russia's tolerance for casualties", "Continued if uneven Western supply"],
        "note": "Theory; the default path if diplomacy fails."
      }
    ],
    "manufacturedConsensus": "Both 'inevitable Russian victory' and 'Ukraine is winning' narratives have been pushed in waves by interested carriers - Russian state media for the former, some Western governments and fundraising appeals for the latter - often outrunning the sourced battlefield picture from trackers like ISW. Watch for momentum claims from belligerents that echo across aligned media faster than independent verification can confirm them."
  },

  {
    "id": "gaza-israel-war-current",
    "title": "Israel-Gaza War: Casualties, Law, and the Ceasefire Question",
    "scope": "conflict",
    "status": "developing",
    "watchers": 15000000,
    "geo": {"lat": 31.5, "lng": 34.47, "place": "Gaza Strip"},
    "neutralLine": "After the Hamas-led attack on southern Israel on 7 October 2023, Israel launched a large-scale military campaign in the Gaza Strip. The war has produced mass Palestinian casualties and displacement, a humanitarian crisis, contested ceasefire and hostage negotiations, and international legal proceedings, with sharply divergent accounts on nearly every element.",
    "claims": [
      {
        "statement": "Israel's campaign is a lawful act of self-defence against Hamas after 7 October, with civilian harm the result of Hamas embedding military assets among civilians.",
        "carriers": [
          C("Israel Defense Forces (IDF) statements", "official record", True, "primary", "original", "Belligerent; legal and reputational defence of operations"),
          C("Israeli Government Press Office", "state media", True, "secondary", "original", "National narrative and alliance management"),
          C("US State Department backing Israel's right to self-defence", "official record", True, "secondary", "original", "Ally; bounded by domestic political constraints"),
        ],
        "strongest": "The 7 October attack killed roughly 1,200 people in Israel and took about 250 hostages (Israeli and corroborated international figures); Hamas is designated a terrorist organisation by the US and EU and has used tunnel networks beneath civilian infrastructure, documented by multiple journalists.",
        "opposition": {
          "statement": "The scale and conduct of the response - tens of thousands of reported Palestinian deaths, most of Gaza displaced, restrictions on food, medicine and aid, and destruction of hospitals and housing - is argued by UN bodies, rights groups, and South Africa's ICJ case to constitute disproportionate harm and plausible breaches of the Genocide Convention, regardless of the legality of the initial casus belli.",
          "carriers": [
            C("South Africa's case at the International Court of Justice", "official record", True, "primary", "original", "State litigant invoking Genocide Convention obligations"),
            C("UN agencies (OCHA, UN human rights office)", "official record", True, "secondary", "original", "Humanitarian mandate; documents casualties and aid access"),
            C("Human Rights Watch / Amnesty International", "research paper", True, "secondary", "original", "Advocacy NGOs; rights-violation framing"),
            C("Al Jazeera on-the-ground reporting", "journalist", True, "primary", "original", "Qatari-funded; sustained Gaza coverage; seen by critics as sympathetic to the Palestinian narrative"),
          ],
          "why": "Self-defence under international law is bounded by proportionality and distinction. The dispute is not whether 7 October happened but whether the response stayed within those bounds - a question the ICJ allowed to proceed and that turns on contested, partly inaccessible facts (casualty composition, aid denial, targeting decisions)."
        }
      },
      {
        "statement": "The Gaza Health Ministry casualty figures are inflated or unreliable because the ministry operates under Hamas.",
        "carriers": [
          C("Israeli government spokespeople", "state media", True, "secondary", "original", "Belligerent; incentive to discredit adverse figures"),
          C("Some US officials questioning the numbers", "official record", True, "secondary", "echo", "Ally; manage political pressure over the toll"),
        ],
        "strongest": "The ministry operates under the Hamas-run authority, and in active war exact attribution and combatant-civilian breakdowns are genuinely hard to verify in real time.",
        "opposition": {
          "statement": "Independent reviews - including past UN and academic analyses and the figures' broad consistency with later tallies - have generally found the ministry's aggregate counts credible if imperfect; epidemiologists writing in The Lancet have argued the true toll may be undercounted, not inflated. Dismissing the numbers wholesale removes the main quantitative record.",
          "carriers": [
            C("UN OCHA (which cites and contextualises the figures)", "official record", True, "secondary", "original", "Humanitarian record-keeping"),
            C("The Lancet correspondence on excess mortality", "research paper", True, "primary", "original", "Epidemiological estimate arguing undercount"),
            C("Comparisons of ministry figures with UN tallies in prior conflicts", "research paper", True, "secondary", "original", "Historical validation of the data source"),
          ],
          "why": "The 'Hamas-run, therefore false' claim is an attribution argument, not a measurement. Reliability is an empirical question that prior conflicts and demographers have addressed, and the leading expert critique is undercounting - the opposite of the inflation claim."
        }
      }
    ],
    "timeline": [
      {"date": "2023-10-07", "event": "Hamas-led attack on southern Israel kills roughly 1,200 and takes about 250 hostages.", "shift": "Triggers the war; Israel declares war on Hamas."},
      {"date": "2023-10-27", "event": "Israel launches a major ground operation into Gaza.", "shift": "Campaign shifts from air to combined arms; casualties and displacement climb."},
      {"date": "2023-11-24", "event": "First negotiated truce and hostage-prisoner exchange, lasting about a week.", "shift": "Proves deals are possible, then collapses back into fighting."},
      {"date": "2023-12-29", "event": "South Africa files a genocide case against Israel at the ICJ.", "shift": "The war enters the international legal arena."},
      {"date": "2024-01-26", "event": "ICJ orders Israel to prevent genocidal acts and enable aid (provisional measures) without ruling on the core charge.", "shift": "Legal pressure formalised; both sides claim vindication."},
      {"date": "2024-05-06", "event": "IDF operation in Rafah amid warnings over sheltering civilians; famine warnings intensify.", "shift": "The humanitarian crisis and the aid-access dispute peak."},
      {"date": "2025-01-19", "event": "A phased ceasefire and hostage-release framework takes effect.", "shift": "Partial de-escalation; full implementation and durability remain contested."}
    ],
    "scenarios": [
      {
        "statement": "THEORY: The phased ceasefire holds partially but breaks down over the 'day after' governance question (who runs Gaza), returning to lower-intensity conflict.",
        "restsOn": ["Unresolved post-war governance", "Mutual distrust between the parties", "Disputes over hostage and prisoner sequencing"],
        "note": "Theory; falsified by a durable governance agreement or by a full collapse back to high-intensity war."
      },
      {
        "statement": "THEORY: International legal and diplomatic pressure (ICJ, ICC, allied governments) increasingly constrains operations and shapes reconstruction terms.",
        "restsOn": ["ICJ provisional measures", "Allied domestic politics", "Reconstruction funding as leverage"],
        "note": "Theory; depends on enforcement, which international courts historically lack."
      }
    ],
    "manufacturedConsensus": "Every quantitative and legal element here - casualty totals, famine classification, intent - is contested by carriers with direct stakes, and figures are amplified or dismissed along alignment lines faster than they can be independently verified. Watch for the same number cited as established fact by one camp and as fabrication by another, with neither showing its verification chain."
  },

  {
    "id": "taiwan-strait-tensions-current",
    "title": "Taiwan Strait: China's Pressure and the Chip Stakes",
    "scope": "geopolitics",
    "status": "developing",
    "watchers": 6000000,
    "geo": {"lat": 24.4, "lng": 119.5, "place": "Taiwan Strait"},
    "neutralLine": "China claims Taiwan as its territory and has stepped up military, economic and political pressure on the island, including large-scale air and naval activity around it. Taiwan, governed separately since 1949, rejects Beijing's sovereignty claim. Analysts dispute the likelihood and timing of conflict and the global economic stakes centred on Taiwan's semiconductor industry.",
    "claims": [
      {
        "statement": "China is building the capability to take Taiwan by force this decade and is using grey-zone pressure to wear the island down ahead of a possible action around 2027.",
        "carriers": [
          C("US Indo-Pacific Command / Pentagon assessments (the '2027' capability reference)", "official record", True, "secondary", "original", "Deterrence framing; budget and alliance justification"),
          C("CSIS and other think-tank wargames", "research paper", True, "secondary", "original", "Scenario analysis with influence on policy"),
          C("Taiwan Ministry of National Defence incursion logs", "official record", True, "primary", "original", "Documents PLA activity; incentive to highlight the threat for support"),
        ],
        "strongest": "The PLA has run record numbers of aircraft and vessel operations around Taiwan and large encirclement drills (notably after high-profile visits and the 2024 inauguration), and Xi Jinping has publicly tied 'reunification' to national rejuvenation and reportedly set capability milestones.",
        "opposition": {
          "statement": "Capability is not intent. An amphibious assault across the strait would be among the hardest operations in modern warfare, with severe self-harm to China (its own chip dependence, sanctions exposure, a blockade of its own trade). Many analysts argue Beijing prefers coercion and political absorption to invasion, and that '2027' is a capability marker, not a decision or a deadline.",
          "carriers": [
            C("Skeptical China analysts (academic commentary)", "public debate", True, "secondary", "original", "Caution against threat inflation"),
            C("Economic analyses of blockade and invasion costs", "market research", True, "secondary", "original", "Model the financial self-harm to China"),
            C("Reuters / FT reporting on cross-strait trade interdependence", "wire service", True, "secondary", "original", "Agency reporting on economic ties"),
          ],
          "why": "The '2027' date is widely reported as a deadline but originates as a capability-readiness reference, not an order to attack. China's dependence on imported advanced chips and seaborne trade makes a kinetic Taiwan war extraordinarily costly to Beijing, so inferring imminent invasion from drills conflates posture with decision."
        }
      },
      {
        "statement": "A conflict over Taiwan would be a global economic catastrophe because Taiwan (TSMC) makes most of the world's most advanced semiconductors.",
        "carriers": [
          C("Semiconductor industry analyses", "market research", True, "secondary", "original", "Model supply-chain concentration risk"),
          C("US and allied officials justifying de-risking and onshoring (CHIPS Act)", "official record", True, "secondary", "original", "Policy justification for industrial subsidies"),
        ],
        "strongest": "TSMC manufactures the large majority of the most advanced logic chips; a strait conflict or blockade would disrupt supply to nearly every electronics and defence chain, with estimates of multi-trillion-dollar global output loss.",
        "opposition": {
          "statement": "The 'silicon shield' cuts both ways and may be eroding: onshoring (US, Japan, Germany fabs) is deliberately reducing single-point dependence, and some argue the shield could invite rather than deter action (an incentive to seize fabs intact or to move before diversification completes). The catastrophe is real but its deterrent value is contested.",
          "carriers": [
            C("Analysts questioning the silicon-shield thesis", "research paper", True, "secondary", "original", "Challenge the deterrence assumption"),
            C("Reporting on TSMC overseas fab build-out", "wire service", True, "secondary", "original", "Documents diversification away from the island"),
          ],
          "why": "Whether chip concentration deters or invites conflict is genuinely undecided. Diversification weakens the shield over time, and an aggressor's calculus around the fabs (seize, destroy, or be deterred) is exactly the contested variable, so the 'catastrophe therefore deterrence' chain does not close."
        }
      }
    ],
    "timeline": [
      {"date": "2022-08-02", "event": "US House Speaker Pelosi visits Taiwan; China responds with unprecedented live-fire drills encircling the island.", "shift": "Establishes large encirclement drills as a coercion tool."},
      {"date": "2024-01-13", "event": "Lai Ching-te (DPP) wins Taiwan's presidential election.", "shift": "Beijing views the result as separatist; tensions rise."},
      {"date": "2024-05-23", "event": "China launches 'Joint Sword-2024A' drills after Lai's inauguration.", "shift": "Drills become a routine response to political milestones."},
      {"date": "2024-10-14", "event": "China stages further large-scale 'Joint Sword' drills around Taiwan.", "shift": "Normalises a high tempo of military pressure."},
      {"date": "2025-01-01", "event": "Record grey-zone activity and cross-strait friction continue into 2025.", "shift": "Pressure sustained; the invasion debate remains unresolved."}
    ],
    "scenarios": [
      {
        "statement": "THEORY: China continues indefinite grey-zone coercion (drills, economic pressure, disinformation) short of invasion, aiming for political absorption over years.",
        "restsOn": ["The high cost of an amphibious invasion", "The effectiveness of sustained coercion", "China's internal economic priorities"],
        "note": "Theory; the modal expert expectation, not a certainty."
      },
      {
        "statement": "THEORY: A blockade or quarantine, not a full invasion, becomes Beijing's coercive tool of choice, testing the US and allied response below the threshold of open war.",
        "restsOn": ["Lower military risk than an amphibious assault", "Ambiguity that complicates the allied response", "PLA naval growth"],
        "note": "Theory; falsified if Beijing judges a blockade to be as escalatory as an invasion."
      }
    ],
    "manufacturedConsensus": "The '2027 invasion' shorthand has hardened into received wisdom through repetition across officials, think-tanks and media, often detached from its origin as a capability-readiness reference. Watch how a hedged intelligence assessment becomes a flat prediction once it echoes across aligned outlets and budget debates."
  },

  {
    "id": "red-sea-houthi-shipping-current",
    "title": "Red Sea Shipping: Houthi Attacks and the Supply-Chain Shock",
    "scope": "markets",
    "status": "developing",
    "watchers": 3000000,
    "geo": {"lat": 12.6, "lng": 43.4, "place": "Bab-el-Mandeb, southern Red Sea"},
    "neutralLine": "Since late 2023, Yemen's Houthi movement has attacked commercial and naval vessels in the Red Sea and Gulf of Aden, saying it targets ships linked to Israel in response to the Gaza war. A US-led coalition has struck Houthi targets in Yemen. The attacks rerouted much global shipping around Africa, raising costs and delivery times, with disputes over the cause, the effectiveness of the response, and Iran's role.",
    "claims": [
      {
        "statement": "The Houthi campaign is an Iran-directed proxy operation, and US and UK strikes are a necessary and largely effective response to restore freedom of navigation.",
        "carriers": [
          C("US CENTCOM operational statements", "official record", True, "primary", "original", "Belligerent; justify and report strikes"),
          C("US and UK government statements on Iranian support", "official record", True, "secondary", "original", "Attribute responsibility upstream to Iran"),
        ],
        "strongest": "The Houthis receive weapons and intelligence support from Iran (documented in UN Panel of Experts reporting and interdictions of Iranian arms shipments), and CENTCOM has reported destroying launchers and intercepting missiles and drones.",
        "opposition": {
          "statement": "The Houthis act with significant autonomy rather than as simple Iranian puppets; the strikes did not stop the attacks, which continued and adapted; and over-attribution to Iran risks miscalculation. Critics argue the campaign treats a symptom while the stated driver, the Gaza war, goes unaddressed, so 'effective' is contested.",
          "carriers": [
            C("Yemen specialists on Houthi autonomy", "research paper", True, "secondary", "original", "Scholarship cautioning against the puppet framing"),
            C("Houthi spokesman statements tying attacks to Gaza", "state media", True, "primary", "original", "Belligerent; frames attacks as solidarity, not Iranian order"),
            C("Maritime security firms reporting continued attacks despite strikes", "market research", True, "secondary", "original", "Commercial risk assessment for shippers"),
          ],
          "why": "Months of strikes did not end the attacks, which undercuts 'largely effective.' The Iran-puppet model is disputed by area specialists who note Houthi independent decision-making, and the attacks rose and fell with the Gaza war rather than only with Iranian direction - so both the cause and the cure are in dispute."
        }
      },
      {
        "statement": "The disruption is a major, durable shock to global supply chains and inflation.",
        "carriers": [
          C("Shipping and insurance analyses (Lloyd's List, freight indices)", "market research", True, "secondary", "original", "Model freight-rate and insurance impact"),
          C("Reuters / Bloomberg reporting on the collapse in Suez traffic", "wire service", True, "secondary", "original", "Agency economic reporting"),
        ],
        "strongest": "A large share of container traffic that normally transits Suez rerouted around the Cape of Good Hope, adding roughly 10 to 14 days and sharply raising spot freight rates and insurance premiums, with specific sectors (European autos, retail) reporting delays.",
        "opposition": {
          "statement": "The macro impact has been real but more contained and transitory than the worst forecasts: global goods inflation kept easing through the period, spare shipping capacity absorbed much of the shock, and rates partly normalised. The 'durable catastrophe' framing oversells a costly but managed rerouting.",
          "carriers": [
            C("Central bank and IMF assessments downplaying systemic inflation impact", "research paper", True, "secondary", "original", "Macro-stability framing"),
            C("Freight-rate data showing partial normalisation", "market research", True, "secondary", "original", "Empirical rate tracking"),
          ],
          "why": "Headline freight-rate spikes are dramatic but not the same as durable consumer inflation; capacity slack and softer demand offset much of the cost. Whether the shock is 'major and durable' or 'costly but absorbed' depends on which metric you privilege - spot rates or realised CPI."
        }
      }
    ],
    "timeline": [
      {"date": "2023-11-19", "event": "Houthis seize the car carrier Galaxy Leader in the Red Sea.", "shift": "Signals a sustained campaign against shipping."},
      {"date": "2023-12-15", "event": "Major shipping lines suspend Red Sea transit and reroute around Africa.", "shift": "Trade disruption becomes global and material."},
      {"date": "2024-01-12", "event": "The US and UK begin air and missile strikes on Houthi targets in Yemen.", "shift": "The conflict widens into a coalition-versus-Houthi exchange."},
      {"date": "2024-03-02", "event": "The bulk carrier Rubymar sinks after an attack; crew casualties occur on other vessels.", "shift": "Escalation to lethal and environmentally damaging attacks."},
      {"date": "2024-07-01", "event": "Attacks persist and adapt despite ongoing coalition strikes.", "shift": "Raises questions about the effectiveness of the military response."},
      {"date": "2025-01-19", "event": "Attack tempo tracks the Gaza ceasefire and the state of the wider conflict.", "shift": "Links the maritime crisis to the regional war rather than to strikes alone."}
    ],
    "scenarios": [
      {
        "statement": "THEORY: A durable Gaza ceasefire substantially reduces Houthi attacks, since the stated trigger eases - reconnecting maritime risk to the regional conflict rather than to the strikes.",
        "restsOn": ["The Houthi framing of attacks as Gaza solidarity", "The observed correlation with the Gaza war", "The limited effect of strikes alone"],
        "note": "Theory; falsified if attacks persist after a ceasefire, which would suggest other drivers."
      },
      {
        "statement": "THEORY: The Houthis institutionalise Red Sea interdiction as permanent leverage regardless of Gaza, normalising elevated shipping risk and insurance costs.",
        "restsOn": ["Enhanced Houthi capability and prestige", "Continued Iranian supply", "Weak deterrence from strikes"],
        "note": "Theory; the pessimistic case for shippers."
      }
    ],
    "manufacturedConsensus": "Two clean stories compete - 'Iran-directed terror, defeated by strikes' and 'grassroots Gaza solidarity, unstoppable' - each pushed by carriers with a stake (coalition governments versus Houthi media). The autonomous-but-Iran-supplied reality and the strikes' limited results fit neither clean story, which is why both keep getting repeated."
  },

  {
    "id": "sudan-civil-war-current",
    "title": "Sudan Civil War: Atrocities, Backers, and a Neglected Catastrophe",
    "scope": "conflict",
    "status": "developing",
    "watchers": 1500000,
    "geo": {"lat": 15.5, "lng": 32.55, "place": "Khartoum, Sudan"},
    "neutralLine": "In April 2023 war broke out between Sudan's army (SAF) and the paramilitary Rapid Support Forces (RSF), creating one of the world's largest displacement and hunger crises. The two sides, their foreign backers, and rights monitors dispute responsibility for atrocities - especially in Darfur - and the role of external arms supplies.",
    "claims": [
      {
        "statement": "The RSF is committing ethnic-targeted atrocities amounting to genocide in Darfur, enabled by foreign arms, with the United Arab Emirates widely accused of supplying it.",
        "carriers": [
          C("UN Panel of Experts on Sudan reporting", "official record", True, "primary", "original", "Mandated monitoring; documents arms flows and abuses"),
          C("US determination of atrocities and genocide", "official record", True, "secondary", "original", "Policy and accountability framing"),
          C("Human Rights Watch and investigative journalists on UAE-RSF links", "research paper", True, "secondary", "original", "Rights documentation; sourcing arms routes"),
        ],
        "strongest": "Multiple independent investigations and a UN Panel of Experts found credible evidence of RSF ethnic massacres in Darfur (echoing the 2000s genocide) and credible indications of external resupply via routes implicating the UAE; the US has formally characterised RSF actions as genocide.",
        "opposition": {
          "statement": "The UAE categorically denies arming the RSF and calls the claims unproven; the SAF also stands accused of atrocities (indiscriminate air strikes, siege starvation), so a single-villain framing is contested. Proving specific arms shipments to a legal standard is genuinely hard, and both belligerents have incentives to shape the narrative.",
          "carriers": [
            C("UAE government denials", "official record", True, "primary", "original", "Accused party; reputational and legal stake"),
            C("Reporting on SAF air strikes and aid obstruction", "wire service", True, "secondary", "original", "Documents abuses by the other side"),
            C("Analysts cautioning against single-actor blame", "public debate", True, "secondary", "original", "Complexity framing; both sides culpable"),
          ],
          "why": "Genocide and arms-supply claims carry legal weight and require sourced proof; the UAE's denial and the SAF's own documented abuses mean the 'RSF plus UAE villain' frame, while heavily supported, is not uncontested. The dispute is over evidentiary standard and symmetry of blame, not whether atrocities occurred."
        }
      },
      {
        "statement": "Sudan's war is a neglected crisis ignored by global media and donors relative to Ukraine and Gaza, despite larger displacement and hunger numbers.",
        "carriers": [
          C("UN OCHA and WFP appeals citing record displacement and famine", "official record", True, "primary", "original", "Humanitarian mandate and fundraising"),
          C("Humanitarian commentators on the 'attention gap'", "public debate", True, "secondary", "original", "Advocacy to raise the crisis's profile"),
        ],
        "strongest": "By UN figures Sudan became the world's largest displacement crisis, with famine confirmed in parts of Darfur, yet media coverage and funding lagged far behind other conflicts - a gap documented by coverage analyses and chronically underfunded UN appeals.",
        "opposition": {
          "statement": "The 'ignored' framing is partly a rhetorical device used to mobilise attention; major outlets and the UN have covered Sudan extensively, and comparative neglect reflects access constraints (both sides restrict journalists and aid) more than indifference. 'Ignored' can obscure why coverage is hard rather than simply absent.",
          "carriers": [
            C("Editors and press-freedom monitors on access restrictions", "journalist", True, "secondary", "original", "Explain the limits on coverage"),
            C("Aid agencies on access denial by both belligerents", "official record", True, "secondary", "original", "Document operational obstruction"),
          ],
          "why": "Underfunding is measurable, but 'ignored' is partly strategic language. Access denial, not just editorial choice, drives thin coverage, so the cause of the attention gap is contested even where the gap itself is real."
        }
      }
    ],
    "timeline": [
      {"date": "2023-04-15", "event": "Fighting erupts between the SAF and the RSF in Khartoum.", "shift": "A planned political transition collapses into open war."},
      {"date": "2023-06-15", "event": "The RSF overruns much of Khartoum and West Darfur; reports of ethnic killings in El Geneina emerge.", "shift": "The war takes on an ethnic-cleansing dimension in Darfur."},
      {"date": "2023-12-01", "event": "The UN warns of the world's largest displacement crisis.", "shift": "The humanitarian catastrophe is recognised globally."},
      {"date": "2024-08-01", "event": "Famine is confirmed in the Zamzam camp in North Darfur.", "shift": "The crisis crosses into formal famine classification."},
      {"date": "2025-01-07", "event": "The US formally determines the RSF committed genocide; the UAE denies arming the RSF.", "shift": "Legal and diplomatic stakes formalised; the backer dispute sharpens."}
    ],
    "scenarios": [
      {
        "statement": "THEORY: A de facto partition hardens - the SAF holding the north, east and centre, the RSF holding much of Darfur and the west - into a prolonged split state.",
        "restsOn": ["A territorial stalemate", "Foreign backing of both sides", "The collapse of unified national institutions"],
        "note": "Theory; falsified by a decisive military outcome or a negotiated reunification."
      },
      {
        "statement": "THEORY: External pressure on the backers (on the UAE and on the SAF's suppliers) becomes the main lever shaping any ceasefire.",
        "restsOn": ["The dependence of both forces on outside resupply", "The diplomatic leverage of Gulf and Western states"],
        "note": "Theory; depends on whether backers face real costs, which historically they often do not."
      }
    ],
    "manufacturedConsensus": "Coverage splits into a clean 'RSF and UAE villain versus SAF victim' story and a 'both sides, no good guys' story, each amplified by aligned governments and diasporas. The sourced reality - severe RSF atrocities and serious SAF abuses, with hard-to-prove external supply - fits neither, so both simplifications keep circulating where verification is hardest."
  },
]

# ---------------- load existing SEED from html ----------------
html = HTML.read_text(encoding="utf-8")
m = re.search(r"/\* SEED-START \*/\s*const SEED = (?P<json>\{.*?\});\s*/\* SEED-END \*/", html, flags=re.DOTALL)
if not m:
    print("ERROR: SEED block not found"); sys.exit(2)
seed = json.loads(m.group("json"))
events = seed["events"]
existing_ids = {e["id"] for e in events}

# ---------------- sanitize + validate new events ----------------
SCOPES = {"geopolitics", "markets", "tech", "conflict"}
STATUS = {"developing", "aged"}
KINDS = {"state media", "wire service", "journalist", "official record",
         "independent OSINT", "research paper", "market research", "public debate"}
PRIMACY = {"primary", "secondary", "downstream"}
PROV = {"original", "echo"}
errs = []
added = []
for e in NEW_EVENTS:
    e = clean(e)
    if e["id"] in existing_ids:
        print(f"skip (already present): {e['id']}"); continue
    for f in ("id", "title", "scope", "neutralLine", "status", "watchers", "claims", "timeline", "geo"):
        if f not in e:
            errs.append(f"{e.get('id','?')} missing {f}")
    if e.get("scope") not in SCOPES: errs.append(f"{e['id']} bad scope {e.get('scope')}")
    if e.get("status") not in STATUS: errs.append(f"{e['id']} bad status {e.get('status')}")
    g = e.get("geo", {})
    if not all(k in g for k in ("lat", "lng", "place")): errs.append(f"{e['id']} bad geo {g}")
    e.setdefault("scenarios", [])
    e.setdefault("manufacturedConsensus", None)
    for c in e.get("claims", []):
        for f in ("statement", "carriers", "strongest", "opposition"):
            if f not in c: errs.append(f"{e['id']} claim missing {f}")
        for cr in c.get("carriers", []) + c.get("opposition", {}).get("carriers", []):
            if cr.get("kind") not in KINDS: errs.append(f"{e['id']} carrier bad kind {cr.get('kind')}")
            if cr.get("primacy") not in PRIMACY: errs.append(f"{e['id']} carrier bad primacy {cr.get('primacy')}")
            if cr.get("provenance") not in PROV: errs.append(f"{e['id']} carrier bad provenance {cr.get('provenance')}")
    added.append(e)

if errs:
    print("VALIDATION ERRORS:")
    for x in errs: print("  -", x)
    sys.exit(1)

events.extend(added)
print(f"added {len(added)} events:", [e['id'] for e in added])
print("total events now:", len(events), "->", [e['id'] for e in events])
print("scopes:", [e['scope'] for e in events])
print("claims/event:", [len(e['claims']) for e in events])
print("with geo:", all('geo' in e for e in events))

# ---------------- inject ----------------
seed["events"] = events
block = "/* SEED-START */\nconst SEED = " + json.dumps(seed, ensure_ascii=False, indent=2) + ";\n/* SEED-END */"
new = re.sub(r"/\* SEED-START \*/.*?/\* SEED-END \*/", lambda _m: block, html, count=1, flags=re.DOTALL)
if new == html:
    print("ERROR: SEED block unchanged"); sys.exit(2)

# final ASCII-hyphen guard across the whole file
bad_dash = [c for c in ("—","–","‒","―","−","‐","‑") if c in new]
if bad_dash:
    print("ERROR: non-ASCII dash present after build:", [hex(ord(c)) for c in bad_dash]); sys.exit(3)

HTML.write_text(new, encoding="utf-8")
print(f"INJECTED -> {HTML} ({len(new.encode('utf-8'))} bytes)")
