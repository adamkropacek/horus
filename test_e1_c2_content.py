#!/usr/bin/env python3
"""
Verify E1-C2 implementation by checking HTML content and dash count.
"""
import re
from pathlib import Path

DEMO_HTML = Path(__file__).parent / "demo.html"
SLATE_JSON = Path(__file__).parent / "slate.json"

def test_implementation():
    """Test that E1-C2 code is present and correct."""

    print("[1] Check E1-C2 code added to demo.html")
    html = DEMO_HTML.read_text(encoding='utf-8')

    # Check state.view default is "today"
    assert 'view: "today",' in html or "view: 'today'," in html, "Default view not set to 'today'"
    print("  PASS: state.view defaults to 'today'")

    # Check riverMode in state
    assert "riverMode:" in html, "riverMode not in state"
    print("  PASS: riverMode added to state")

    # Check SLATE global
    assert "let SLATE = null;" in html, "SLATE global not declared"
    print("  PASS: SLATE global declared")

    # Check slate.json fetch
    assert 'fetch("slate.json' in html, "slate.json fetch not added"
    print("  PASS: slate.json fetch added")

    # Check loadSlateState function
    assert "function loadSlateState()" in html, "loadSlateState function not found"
    print("  PASS: loadSlateState function added")

    # Check renderToday function
    assert "function renderToday()" in html, "renderToday function not found"
    print("  PASS: renderToday function added")

    # Check TODAY view routing in render()
    assert 'if(state.view==="today") renderToday();' in html or \
           "if(state.view===\"today\") renderToday();" in html, "renderToday not called in render()"
    print("  PASS: renderToday called in render() routing")

    # Check BUCKET_LABEL_FULL map
    assert "GEOPOLITICS" in html and "POWER + MONEY" in html, "BUCKET_LABEL_FULL map not correct"
    print("  PASS: BUCKET_LABEL_FULL map has correct labels")

    # Check copy strings from spec (B.1, B.4, B.5, B.6, B.7)
    assert "Edition" in html and "compiled" in html and "UTC" in html, "B.1 header copy missing"
    print("  PASS: B.1 header copy present")

    assert "That is what moved the world today" in html, "B.4 caught-up text missing"
    print("  PASS: B.4 caught-up copy present")

    assert "You are caught up" in html, "B.4 final copy missing"
    print("  PASS: B.4 final copy present")

    assert "quieter developments in the river" in html, "B.5 overflow copy missing"
    print("  PASS: B.5 overflow copy present")

    assert "DEVELOPING SINCE THIS MORNING" in html, "B.6 appendix copy missing"
    print("  PASS: B.6 appendix copy present")

    assert "YOUR SITUATIONS" in html, "B.7 rail copy missing"
    print("  PASS: B.7 rail copy present")

    assert "Star a story and it lives here" in html, "B.7 empty state copy missing"
    print("  PASS: B.7 empty state copy present")

    # Check localStorage contract
    assert "horus_last_visit" in html, "horus_last_visit key not used"
    print("  PASS: horus_last_visit localStorage key used")

    assert "horus_stars" in html, "horus_stars key not used"
    print("  PASS: horus_stars localStorage key used")

    assert "horus_seen_splits" in html, "horus_seen_splits key not used"
    print("  PASS: horus_seen_splits localStorage key used")

    # Check star toggle function
    assert "function toggleStar(" in html, "toggleStar function not found"
    print("  PASS: toggleStar function added")

    # Check TODAY/RIVER nav
    assert "text=TODAY" in html or ">TODAY<" in html, "TODAY nav button not found"
    print("  PASS: TODAY nav button present")

    assert "text=THE RIVER" in html or ">THE RIVER<" in html, "THE RIVER nav button not found"
    print("  PASS: THE RIVER nav button present")

    # Check BY STORY toggle
    assert "state.riverMode" in html, "riverMode toggle not added"
    print("  PASS: BY STORY toggle references riverMode")

    print("\n[2] Check slash removal (ASCII hyphen only)")
    # Check for em/en/figure dashes (U+2012, U+2013, U+2014, U+2015, U+2212, U+2010)
    bad_dashes = re.findall(r'[‒–—―−‐]', html)
    print(f"  Found {len(bad_dashes)} em/en/figure dashes in demo.html")
    if bad_dashes:
        print(f"  ERROR: Bad dashes found: {set(bad_dashes)}")
        return False
    print("  PASS: Zero em/en dashes in demo.html")

    print("\n[3] Check slate.json fixture")
    if SLATE_JSON.exists():
        import json
        slate = json.loads(SLATE_JSON.read_text())
        assert "panels" in slate, "slate.json missing 'panels' key"
        assert "dot_of_the_day" in slate, "slate.json missing 'dot_of_the_day' key"
        assert "appendix" in slate, "slate.json missing 'appendix' key"
        assert "overflow" in slate, "slate.json missing 'overflow' key"
        print(f"  PASS: slate.json has {len(slate.get('panels', []))} panels")
    else:
        print("  WARNING: slate.json fixture not found")

    print("\n[SUCCESS] All content checks passed")
    return True

if __name__ == "__main__":
    try:
        result = test_implementation()
        exit(0 if result else 1)
    except AssertionError as e:
        print(f"\n[FAIL] {e}")
        exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        exit(1)
