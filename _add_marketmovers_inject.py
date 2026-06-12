#!/usr/bin/env python3
"""Add 3 non-conflict world-mover situations (central banks, AI chips, oil/OPEC) to the demo SEED,
in full HORUS structure, from live headlines pulled 2026-06-10. Widens scope past conflict per Adam.
No verdict, descriptive claims, real carriers, steelmanned opposition. ASCII-hyphen guard. Idempotent."""
import re, json, html, sys
from pathlib import Path

F = Path(__file__).with_name("demo.html")
MARKER = "MARKETMOVERS-2026-06-10"
DASHES = {"‐":"-","‑":"-","‒":"-","–":"-","—":"-","―":"-","−":"-"}

def C(s):
    s = html.unescape(str(s))
    for k,v in DASHES.items(): s = s.replace(k,v)
    return s.strip()

def clean_obj(o):
    if isinstance(o,dict): return {k:clean_obj(v) for k,v in o.items()}
    if isinstance(o,list): return [clean_obj(x) for x in o]
    if isinstance(o,str): return C(o)
    return o

def carrier(source, kind, named, primacy, provenance, motive):
    return {"source":source,"kind":kind,"named":named,"primacy":primacy,"provenance":provenance,"motive":motive}

EVENTS = [
  {
    "id":"central-banks-rates-2026-06",
    "title":"Central Banks Diverge: A New Fed Chair Holds as the ECB Moves to Hike",
    "scope":"markets","status":"developing","watchers":9200000,
    "geo":{"lat":38.9,"lng":-77.04,"place":"Washington DC / Frankfurt"},
    "neutralLine":"Monetary policy has split across the Atlantic. With a leadership change at the US Federal Reserve and inflation reaccelerating, markets are repricing the path of rates, while the ECB heads into a June 11 decision widely expected to hike. Whether tightening tames inflation or tips weak economies into recession is genuinely contested.",
    "claims":[
      {"statement":"Inflation is reaccelerating, so central banks must stay tight (or hike) now to stop it becoming entrenched.",
       "carriers":[
         carrier("Reuters: 'Warsh takes the Fed's helm as inflation climbs'","wire service",True,"primary","original","Newswire reporting the policy backdrop"),
         carrier("The Corner.eu: 'ECB set to raise rates amid resurgent inflation risks'","journalist",True,"secondary","original","European financial press, hawkish read"),
         carrier("Reuters: 'Time to nip inflation in the bud: five questions for the ECB'","wire service",True,"secondary","original","Frames the hawkish case ahead of the decision")],
       "strongest":"Headline inflation has turned back up in both the US and euro area, and central banks with a price-stability mandate treat re-acceleration as the dominant risk; the ECB is widely reported set to act on June 11, and a US dollar bid on inflation prints signals markets pricing a higher-for-longer stance.",
       "opposition":{
         "statement":"Several economists call further hikes a mistake: growth and consumer sentiment are weakening, much of the inflation is energy-driven (a supply shock monetary policy cannot fix), and tightening into a slowdown risks forcing a recession rather than a soft landing.",
         "carriers":[
           carrier("CNBC: 'Energy prices take center stage as the ECB prepares to decide'","journalist",True,"primary","original","Notes the inflation is partly an energy/supply story"),
           carrier("Anadolu Ajansi: 'ECB may hike amid inflation-recession dilemma'","wire service",True,"secondary","original","Frames the recession trade-off"),
           carrier("Axios: 'December rate cut now looks questionable'","journalist",True,"secondary","echo","Tracks how cut expectations have unwound")],
         "why":"A rate path is a bet on which risk dominates - sticky inflation or a stalling economy. If the inflation is supply-driven (energy, shipping), hiking raises the cost of a recession without addressing the cause. The dispute is empirical and not settled until the data lands."}}
    ],
    "timeline":[
      {"date":"2026-05-16","event":"Kevin Warsh comes into the Fed facing a big 'family fight' over cutting interest rates","shift":"Live feed item // CNBC // pulled 2026-06-10"},
      {"date":"2026-05-22","event":"Warsh takes the Fed's helm as inflation climbs, consumer sentiment dives","shift":"Live feed item // Reuters // pulled 2026-06-10"},
      {"date":"2026-06-08","event":"With Fed set to meet next week, December's rate cut now looks questionable","shift":"Live feed item // Axios // pulled 2026-06-10"},
      {"date":"2026-06-09","event":"Fed rate decision 2026: Powell is out, Warsh is in, and markets are repricing everything","shift":"Live feed item // Mitrade // pulled 2026-06-10"},
      {"date":"2026-06-10","event":"Energy prices take center stage as the ECB prepares to decide on rates","shift":"Live feed item // CNBC // pulled 2026-06-10"},
      {"date":"2026-06-10","event":"US inflation print could lift the US dollar today","shift":"Live feed item // TorFX // pulled 2026-06-10"}
    ],
    "manufacturedConsensus":"Watch for 'the Fed has pivoted' framing on a single data point or speech. One print or one new chair's tone does not equal a confirmed policy turn; the timeline shows expectations swinging both ways within weeks.",
    "scenarios":[
      {"statement":"ECB hikes June 11 and the Fed holds, widening EUR-USD policy divergence and moving the currency pair.",
       "restsOn":["ECB June 11 decision (scheduled)","reported US dollar strength on inflation prints","economists split on US December cut"],
       "note":"Theory, not a prediction. Rests on a scheduled meeting and reported positioning; the actual decision and guidance can break either way."},
      {"statement":"If inflation proves energy-driven and growth rolls over, a 2026 hike is reversed within months, repeating prior stop-go cycles.",
       "restsOn":["CNBC framing of energy as the inflation driver","weak consumer sentiment reports","historical central-bank reversals after supply shocks"],
       "note":"Theory. Falsifiable: if core inflation stays high while growth holds, the supply-shock reading weakens."}
    ]
  },
  {
    "id":"ai-chip-export-controls-2026-06",
    "title":"AI Chip Export Controls: Taiwan and Washington Tighten, Beijing Redesigns",
    "scope":"tech","status":"developing","watchers":6400000,
    "geo":{"lat":24.81,"lng":120.97,"place":"Hsinchu / Taipei"},
    "neutralLine":"The US, and now reportedly Taiwan, are tightening controls on advanced AI chip exports to China, framed as containing a strategic rival. China argues the curbs are accelerating its own indigenous chip industry. Whether export controls slow or speed China's AI capability is the core dispute.",
    "claims":[
      {"statement":"Export controls are necessary and effective at slowing China's access to the compute behind frontier AI and advanced weapons.",
       "carriers":[
         carrier("Bloomberg: 'Taiwan mulls curbs on AI chip exports to China to align with US'","wire service",True,"primary","original","Reports the alignment move"),
         carrier("DigiTimes: 'Taiwan weighs tougher AI chip export curbs as US lawmakers push'","journalist",True,"secondary","original","Industry trade press, supply-chain detail"),
         carrier("Al Jazeera: 'US says ban on AI chip shipments applies to Chinese firms outside China'","wire service",True,"secondary","original","Reports the extraterritorial reach of the rules")],
       "strongest":"The most advanced AI accelerators are made by a handful of firms dependent on a narrow Taiwan/US/Netherlands toolchain; restricting that chokepoint demonstrably forces Chinese firms onto older or scarcer hardware in the near term, and allied alignment (US plus Taiwan) closes obvious workarounds.",
       "opposition":{
         "statement":"The same controls are reported to be forcing China to redesign and fund a domestic chip industry, potentially producing a more self-sufficient long-run competitor; a containment tool can accelerate the very capability it aims to deny.",
         "carriers":[
           carrier("South China Morning Post: 'How US export curbs are forcing China to redesign its AI chip industry'","journalist",True,"primary","original","Hong Kong outlet; argues the acceleration effect"),
           carrier("South China Morning Post: 'What Washington's latest AI chip guidance means for Chinese tech firms'","journalist",True,"secondary","original","Tracks Chinese-industry response"),
           carrier("The Economic Times: 'Taiwan weighs stricter export controls on AI chip sales to China'","wire service",True,"secondary","echo","Indian financial press; regional framing")],
         "why":"Containment and acceleration can both be true on different time horizons: a near-term slowdown plus a long-term push toward self-sufficiency. The dispute turns on how fast China can substitute, which is unknown and partly hidden."}}
    ],
    "timeline":[
      {"date":"2026-06-01","event":"US says ban on AI chip shipments applies to Chinese firms outside China","shift":"Live feed item // Al Jazeera // pulled 2026-06-10"},
      {"date":"2026-06-01","event":"How US export curbs are forcing China to redesign its AI chip industry","shift":"Live feed item // South China Morning Post // pulled 2026-06-10"},
      {"date":"2026-06-06","event":"What does Washington's latest AI chip guidance mean for Chinese tech firms?","shift":"Live feed item // South China Morning Post // pulled 2026-06-10"},
      {"date":"2026-06-09","event":"Taiwan weighs stricter export controls on AI chip sales to China","shift":"Live feed item // The Economic Times // pulled 2026-06-10"},
      {"date":"2026-06-10","event":"Taiwan mulls curbs on AI chip exports to China to align with US","shift":"Live feed item // Bloomberg // pulled 2026-06-10"}
    ],
    "manufacturedConsensus":"Both 'controls are working' and 'controls are backfiring' are pushed hard by sources with stakes (policymakers vs Chinese-industry press). Watch which time horizon each one quietly assumes.",
    "scenarios":[
      {"statement":"Taiwan formalises curbs aligning with the US, tightening the allied chokehold on advanced nodes.",
       "restsOn":["Bloomberg and DigiTimes reports that Taiwan is weighing curbs","US lawmaker pressure for tighter controls"],
       "note":"Theory. Rests on reporting that a decision is being weighed, not yet made."},
      {"statement":"Controls accelerate a Chinese domestic toolchain that narrows the gap on a multi-year horizon.",
       "restsOn":["SCMP reporting on forced redesign","historical precedent of sanctions spurring import substitution"],
       "note":"Theory. Falsifiable: if Chinese frontier-model compute stalls for years, the acceleration thesis weakens."}
    ]
  },
  {
    "id":"oil-opec-grip-2026-06",
    "title":"Oil's Swing Vote: OPEC's Grip Loosens as Geopolitics Sets the Price",
    "scope":"markets","status":"developing","watchers":5100000,
    "geo":{"lat":26.57,"lng":56.25,"place":"Strait of Hormuz"},
    "neutralLine":"Crude prices are being pulled between OPEC output signals, a reported UAE exit from the bloc, and geopolitical chokepoints (Strait of Hormuz, Red Sea). Whether OPEC still sets the oil price, or whether geopolitics and non-OPEC supply now dominate, is openly disputed.",
    "claims":[
      {"statement":"OPEC still steers the oil price through coordinated output decisions.",
       "carriers":[
         carrier("Bloomberg: 'OPEC signals higher output; geopolitical risks weigh on markets'","wire service",True,"primary","original","Newswire on OPEC output signalling"),
         carrier("OPEC output communiques","official record",True,"primary","original","The cartel's own production guidance")],
       "strongest":"OPEC and its allies still control a large share of spare production capacity, and output announcements continue to move futures within the trading session, which is the textbook definition of price-setting power.",
       "opposition":{
         "statement":"Multiple outlets argue OPEC's influence is fading: a reported UAE exit, a chokepoint (Hormuz) and Red Sea disruption setting prices regardless of quotas, and non-OPEC plus Chinese demand dynamics cushioning the market beyond the cartel's reach.",
         "carriers":[
           carrier("Yahoo Finance: 'Oil market fate isn't in OPEC's hands anymore'","journalist",True,"primary","original","Argues the loss-of-control thesis"),
           carrier("hkcna.hk: 'Hormuz Strait choke-hold lets OPEC lose influence'","journalist",True,"secondary","original","Hong Kong outlet; chokepoint framing"),
           carrier("negocios.com: report that the UAE has left OPEC","journalist",True,"secondary","echo","Spanish-language business press; unconfirmed elsewhere")],
         "why":"If a single shipping chokepoint or a member exit moves prices more than a quota decision, pricing power has shifted from the cartel to geopolitics and logistics. The UAE-exit claim is single-sourced here and is exactly the kind of item that needs corroboration."}}
    ],
    "timeline":[
      {"date":"2026-06-09","event":"Lower crude oil prices bring gas prices down","shift":"Live feed item // iHeart // pulled 2026-06-10"},
      {"date":"2026-06-10","event":"OPEC signals higher output; geopolitical risks weigh on markets","shift":"Live feed item // Bloomberg // pulled 2026-06-10"},
      {"date":"2026-06-10","event":"Oil market fate isn't in OPEC's hands anymore","shift":"Live feed item // Yahoo Finance // pulled 2026-06-10"},
      {"date":"2026-06-10","event":"Hormuz Strait choke-hold lets OPEC lose influence in energy market","shift":"Live feed item // hkcna.hk // pulled 2026-06-10"},
      {"date":"2026-06-10","event":"Report: the UAE has left OPEC (single-sourced, uncorroborated)","shift":"Live feed item // negocios.com // pulled 2026-06-10 // flagged as needing corroboration"}
    ],
    "manufacturedConsensus":"The 'UAE has left OPEC' item appears single-sourced here. A market-moving claim carried by one outlet without corroboration is exactly where attention can outrun verification - shown, not judged.",
    "scenarios":[
      {"statement":"Hormuz / Red Sea disruption keeps a geopolitical premium in crude regardless of OPEC quota decisions.",
       "restsOn":["Red Sea Houthi shipping situation (linked)","Bloomberg note on geopolitical risk","Hormuz chokepoint reporting"],
       "note":"Theory. Connects to the Red Sea situation via the same chokepoints and Iran-linked actors."}
    ]
  }
]

def find_matching_bracket(text, open_idx):
    depth=0
    for i in range(open_idx,len(text)):
        if text[i]=='[': depth+=1
        elif text[i]==']':
            depth-=1
            if depth==0: return i
    raise ValueError("no matching ]")

def main():
    t=F.read_text(encoding="utf-8")
    if MARKER in t:
        print("already added; aborting"); return 1
    m=re.search(r'"events"\s*:\s*\[',t)
    if not m: print("ERR: events array not found"); return 2
    ob=t.index('[',m.start())
    cb=find_matching_bracket(t,ob)
    blocks=[]
    for ev in EVENTS:
        js=json.dumps(clean_obj(ev),ensure_ascii=False,indent=2)
        js="\n".join("      "+ln for ln in js.split("\n"))  # indent to 6 spaces
        blocks.append(js)
    before=t[:cb].rstrip()
    sep="" if before.endswith("[") else ","
    inject=sep+"\n"+",\n".join(blocks)+"\n    "
    t=before+inject+t[cb:]
    t=t.replace("/* SEED-END */","/* SEED-END */ /* "+MARKER+" */",1)
    F.write_text(t,encoding="utf-8")
    bad=sum(t.count(d) for d in DASHES)
    print(f"added {len(EVENTS)} situations. unicode-dash count: {bad}")
    return 0

if __name__=="__main__":
    sys.exit(main())
