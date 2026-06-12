#!/usr/bin/env python3
"""Full-bleed HTML -> PDF (margin 0, CSS @page A4) for the HORUS system map deck."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

h = Path(sys.argv[1]).resolve()
p = Path(sys.argv[2]).resolve()
p.parent.mkdir(parents=True, exist_ok=True)
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page()
    pg.goto(f"file://{h.as_posix()}", wait_until="load", timeout=60000)
    try:
        pg.wait_for_load_state("networkidle", timeout=4000)
    except Exception:
        pass
    try:
        pg.evaluate("async () => { if (document.fonts && document.fonts.ready) { await document.fonts.ready; } }")
    except Exception:
        pass
    pg.wait_for_timeout(700)
    pg.emulate_media(media="print")
    pg.pdf(
        path=str(p),
        prefer_css_page_size=True,
        print_background=True,
        margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
    )
    b.close()
print("OK", p)
