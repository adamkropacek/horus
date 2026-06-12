#!/usr/bin/env python3
"""Keep only our 5 current ongoing situations, remove the globe entirely. ASCII-dash guard."""
import re, json
from pathlib import Path

P = Path(__file__).with_name("demo.html")
KEEP = {"russia-ukraine-war-current","gaza-israel-war-current","taiwan-strait-tensions-current",
        "red-sea-houthi-shipping-current","sudan-civil-war-current"}

def match_brace(s, i):
    assert s[i] == '{'
    depth = 0; instr = False; esc = False
    while i < len(s):
        c = s[i]
        if instr:
            if esc:
                esc = False
            elif c == '\\':
                esc = True
            elif c == '"':
                instr = False
        else:
            if c == '"':
                instr = True
            elif c == '{':
                depth += 1
            elif c == '}':
                depth -= 1
                if depth == 0:
                    return i
        i += 1
    raise ValueError("unbalanced")

t = P.read_text(encoding="utf-8")
orig_len = len(t)

# --- filter SEED.events ---
m = re.search(r'const SEED\s*=\s*', t)
ob = t.index('{', m.end())
cb = match_brace(t, ob)
data = json.loads(t[ob:cb+1])
before = len(data["events"])
data["events"] = [e for e in data["events"] if e.get("id") in KEEP]
after = len(data["events"])
t = t[:ob] + json.dumps(data, ensure_ascii=False, indent=2) + t[cb+1:]
print(f"SEED events {before} -> {after}: {[e['id'] for e in data['events']]}")

# --- remove globe ---
t = t.replace('<script defer src="https://unpkg.com/globe.gl"></script>\n', '', 1)

hs = t.index('<!-- ============ GLOBE HERO')
he = t.index('</section>', hs) + len('</section>')
while he < len(t) and t[he] in '\r\n':
    he += 1
t = t[:hs] + t[he:]

t = t.replace('  const gw=document.getElementById("globeWrap");\n'
              '  if(gw) gw.classList.toggle("show", state.view==="board"); // globe is the board hero only; never leaks onto event view\n',
              '', 1)

gs = t.index('/* ===================== GLOBE HERO')
ge = t.index('render();', gs)
t = t[:gs] + t[ge:]

leftover = t.count('initGlobe') + t.count('globeInstance') + t.count('GEO_MARKERS') + t.count('globe.gl')
print("globe JS refs leftover (want 0):", leftover)
print("unicode dashes:", len(re.findall(r'[‐-―−]', t)))

P.write_text(t, encoding="utf-8")
print("written; delta bytes:", len(t) - orig_len)
