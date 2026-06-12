#!/usr/bin/env python3
"""Inject workflow seed data into demo.html SEED block. Validates shape first."""
import json, sys, re, pathlib

OUT = r"C:/Users/adamk/AppData/Local/Temp/claude/c--Users-adamk-Desktop-newvs/eb85fe46-7afd-4b7f-a759-41619c7c183b/tasks/w3sysjg7a.output"
HTML = pathlib.Path(r"C:/Users/adamk/Desktop/newvs/.work/horus-site/demo.html")

env = json.load(open(OUT, encoding="utf-8"))
data = env["result"]

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
data = clean(data)

events = data["events"]
mc = data["microcopy"]

# ---- validate ----
errs = []
SCOPES = {"geopolitics", "markets", "tech", "conflict"}
STATUS = {"developing", "aged"}
KINDS = {"state media", "wire service", "journalist", "official record",
         "independent OSINT", "research paper", "market research", "public debate"}
for e in events:
    for f in ("id", "title", "scope", "neutralLine", "status", "watchers", "claims", "timeline"):
        if f not in e:
            errs.append(f"event {e.get('id','?')} missing {f}")
    if e.get("scope") not in SCOPES:
        errs.append(f"event {e.get('id')} bad scope {e.get('scope')}")
    if e.get("status") not in STATUS:
        errs.append(f"event {e.get('id')} bad status {e.get('status')}")
    e.setdefault("scenarios", [])
    e.setdefault("manufacturedConsensus", None)
    # geo-coordinates for the globe (matched by id substring)
    GEO = {
        "nord-stream": {"lat": 55.5, "lng": 15.65, "place": "Baltic Sea, off Bornholm"},
        "covid": {"lat": 30.59, "lng": 114.30, "place": "Wuhan, China"},
        "al-ahli": {"lat": 31.52, "lng": 34.45, "place": "Gaza City"},
        "svb": {"lat": 37.39, "lng": -121.96, "place": "Santa Clara, USA"},
        "prigozhin": {"lat": 55.75, "lng": 37.62, "place": "Moscow, Russia"},
        "wagner": {"lat": 55.75, "lng": 37.62, "place": "Moscow, Russia"},
    }
    for key, geo in GEO.items():
        if key in e["id"]:
            e["geo"] = geo
            break
    if "geo" not in e:
        errs.append(f"event {e.get('id')} has no geo match")
    for c in e.get("claims", []):
        for f in ("statement", "carriers", "strongest", "opposition"):
            if f not in c:
                errs.append(f"{e['id']} claim missing {f}")
        for cr in c.get("carriers", []) + c.get("opposition", {}).get("carriers", []):
            if cr.get("kind") not in KINDS:
                errs.append(f"{e['id']} carrier bad kind {cr.get('kind')}")
for f in ("tagline", "noVerdictExplainer", "kindLegend", "primacyLegend",
          "freeGate", "proGate", "methodologyNote", "emptyState"):
    if f not in mc:
        errs.append(f"microcopy missing {f}")

print(f"events={len(events)}  microcopy_keys={len(mc)}")
print("event ids:", [e["id"] for e in events])
print("scopes:", [e["scope"] for e in events])
print("claims/event:", [len(e["claims"]) for e in events])
print("scenarios/event:", [len(e["scenarios"]) for e in events])
print("mfgConsensus set:", [bool(e.get("manufacturedConsensus")) for e in events])
if errs:
    print("VALIDATION ERRORS:")
    for x in errs:
        print("  -", x)
    sys.exit(1)
print("VALIDATION OK")

# ---- inject ----
seed = {"microcopy": mc, "events": events}
block = "/* SEED-START */\nconst SEED = " + json.dumps(seed, ensure_ascii=False, indent=2) + ";\n/* SEED-END */"
html = HTML.read_text(encoding="utf-8")
new = re.sub(r"/\* SEED-START \*/.*?/\* SEED-END \*/", lambda m: block, html, count=1, flags=re.DOTALL)
if new == html:
    print("ERROR: SEED block not found / unchanged"); sys.exit(2)
HTML.write_text(new, encoding="utf-8")
print(f"INJECTED -> {HTML}  ({len(new)} bytes)")
