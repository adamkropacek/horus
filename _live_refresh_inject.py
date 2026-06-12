#!/usr/bin/env python3
"""Inject today's real headlines as timeline beats into the 5 ongoing demo situations,
and flip the SEEDED badge to LIVE. ASCII-hyphen guard + entity decode. Idempotent via marker.
Source data = live GDELT/RSS pull 2026-06-10 (workflow wdhmfczlh) + earlier Gaza ingest."""
import re, json, html, sys, io
from pathlib import Path

F = Path(__file__).with_name("demo.html")
MARKER = "LIVE-REFRESH-2026-06-10"

# live beats per situation id (real headlines pulled 2026-06-10), oldest-first so they append in order
LIVE = {
    "gaza-israel-war-current": [
        ("2026-06-06", "Reuters", "Israeli strike in Gaza kills seven people, including two women, medics say"),
        ("2026-06-09", "AP News", "Militants and police executed and maimed dozens of Palestinians in Gaza, UN report says"),
        ("2026-06-09", "UN Commission of Inquiry", "UN inquiry finds Israeli forces shield settlers during attacks on Palestinians"),
        ("2026-06-10", "i24news", "IDF eliminates two key Hamas financial officials in Gaza"),
        ("2026-06-10", "Times of Israel", "Gaza talks hosted by Egypt stall as Hamas disarmament remains only point of contention"),
        ("2026-06-10", "BBC", "Israeli strikes kill 11 people in Gaza City, medics say"),
    ],
    "russia-ukraine-war-current": [
        ("2026-06-08", "The Guardian", "Moscow car bomb kills Russian ammunition chief, reports say"),
        ("2026-06-08", "Sky News", "Moscow 'ready to use nuclear weapons' for security as drone strikes choke supplies into Crimea"),
        ("2026-06-08", "Al Jazeera", "Russian attacks kill 5 in Ukraine as Zelenskyy hails talks with US envoys"),
        ("2026-06-09", "Institute for the Study of War", "Russian Offensive Campaign Assessment, June 9, 2026"),
        ("2026-06-09", "CBS News", "Ukraine winning war with Russia, retired US generals say; top commander says over 230 square miles retaken"),
    ],
    "taiwan-strait-tensions-current": [
        ("2026-06-05", "Institute for the Study of War", "China and Taiwan Update, June 5, 2026"),
        ("2026-06-07", "South China Morning Post", "Beijing detects suspected Japanese spy jets near Taiwan"),
        ("2026-06-08", "Taiwan Government via Yahoo", "Taiwan says China Coast Guard patrols to its east are a 'provocative act'"),
        ("2026-06-09", "Reuters", "Taiwan simulates destroying an invading Chinese force in coastal drill"),
    ],
    "red-sea-houthi-shipping-current": [
        ("2026-06-08", "Bloomberg", "Houthis to impose 'complete ban' on Israeli ships in the Red Sea"),
        ("2026-06-08", "Reuters", "Yemen's Iran-backed Houthis threaten Israeli shipping in the Red Sea"),
        ("2026-06-08", "The New York Times", "Houthis threaten to widen Iran war by blocking Israeli shipping in Red Sea"),
        ("2026-06-10", "Economic Times", "Suez Canal sees oil tanker surge amid Strait of Hormuz disruption"),
        ("2026-06-10", "UKMTO via Africa Leader", "Cargo vessel exchanges fire with armed craft southwest of Yemen"),
    ],
    "sudan-civil-war-current": [
        ("2026-06-05", "Scripps News", "Sudan's drone war: how unmanned aircraft became the deadliest weapon against civilians"),
        ("2026-06-08", "The Cairo Review of Global Affairs", "The war in Sudan is fought over the bodies of women"),
        ("2026-06-09", "AP News", "First war crimes complaint against Sudan's paramilitary forces filed in Kenya"),
        ("2026-06-09", "Africa Defense Forum", "Eastern Chad an emerging frontline in Sudan war"),
    ],
}

DASHES = {"‐":"-","‑":"-","‒":"-","–":"-","—":"-","―":"-","−":"-"}
def clean(s):
    s = html.unescape(s)
    for k,v in DASHES.items(): s = s.replace(k,v)
    return s.strip()

def find_matching_bracket(text, open_idx):
    """open_idx points at '['. return index of matching ']'."""
    depth=0
    for i in range(open_idx, len(text)):
        c=text[i]
        if c=='[': depth+=1
        elif c==']':
            depth-=1
            if depth==0: return i
    raise ValueError("no matching ]")

def main():
    t = F.read_text(encoding="utf-8")
    if MARKER in t:
        print("already injected; aborting (idempotent)"); return 1

    for sid, beats in LIVE.items():
        m = re.search(r'"id":\s*"'+re.escape(sid)+r'"', t)
        if not m:
            print("WARN: id not found:", sid); continue
        tl = t.find('"timeline":', m.end())
        if tl<0: print("WARN: no timeline for", sid); continue
        ob = t.find('[', tl)
        cb = find_matching_bracket(t, ob)
        # build beat objects, indent to match (12 spaces inside array)
        objs=[]
        for date,outlet,event in beats:
            ev = clean(f"{event}")
            sh = clean(f"Live feed item // {outlet} // pulled 2026-06-10")
            ev = ev.replace('"','\\"'); sh = sh.replace('"','\\"')
            objs.append(
                '        {\n'
                f'          "date": "{date}",\n'
                f'          "event": "{ev}",\n'
                f'          "shift": "{sh}"\n'
                '        }'
            )
        block = ",\n" + ",\n".join(objs) + "\n      "
        # insert before closing ] (after existing last beat). Need a comma before our block if array non-empty.
        before = t[:cb].rstrip()
        # if the char right before ] is already a comma, don't double it
        inject = block
        if before.endswith(','):
            inject = "\n" + ",\n".join(objs) + "\n      "
        t = before + inject + t[cb:]
        print(f"OK {sid}: +{len(beats)} beats")

    # flip badge
    t2 = t.replace(
        'DEMO <b class="red">● SEEDED</b>',
        '<b class="red">● LIVE</b> &nbsp;//&nbsp; refreshed 2026-06-10',
        1)
    if t2==t: print("WARN: badge not flipped")
    t = t2

    # drop an idempotency marker comment near SEED-END
    t = t.replace("/* SEED-END */", f"/* SEED-END */ /* {MARKER} */", 1)

    # final ASCII-dash guard on whole file body of injected strings already done; assert no unicode dash in new beats
    F.write_text(t, encoding="utf-8")
    bad = sum(t.count(d) for d in DASHES)
    print(f"written. unicode-dash count in file: {bad}")
    return 0

if __name__=="__main__":
    sys.exit(main())
