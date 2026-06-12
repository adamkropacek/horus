#!/usr/bin/env python3
"""Embed the stage-6 history cache (demo-data/history/*.json) into demo.html.

Replaces the block between ==HISTORY-CACHE-START== / ==HISTORY-CACHE-END== markers.
Repeatable: run again after a monthly touch of the cache files.
ensure_ascii=True keeps the embedded blob free of raw unicode dashes by construction.
"""
import glob
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
HIST_DIR = REPO / "clients/scaleyourinfo/strategy/_research/truthseeker/demo-data/history"
DEMO = HERE / "demo.html"

DASH_RE = re.compile("[‒–—―−]")

data = {}
for p in sorted(HIST_DIR.glob("*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    data[d["id"]] = d

if not data:
    sys.exit("no history files found in " + str(HIST_DIR))

blob = json.dumps(data, ensure_ascii=True, separators=(",", ":")).replace("</", "<\\/")
if DASH_RE.search(blob):
    sys.exit("ABORT: raw unicode dash in embedded blob")

html = DEMO.read_text(encoding="utf-8")
start_marker = "/* ==HISTORY-CACHE-START=="
end_marker = "/* ==HISTORY-CACHE-END== */"
i = html.index(start_marker)
j = html.index(end_marker) + len(end_marker)
head_end = html.index("*/", i) + 2  # keep the explanatory comment block intact

new_block = (html[i:head_end] + "\nconst HISTORY = " + blob + ";\n" + end_marker)
DEMO.write_text(html[:i] + new_block + html[j:], encoding="utf-8")
print(f"embedded {len(data)} situations, {len(blob)//1024} KB: {', '.join(sorted(data))}")
