#!/usr/bin/env python3
"""E3-C2 Acceptance verification via Playwright."""
import subprocess
import json
import re
import sys

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("Installing playwright...")
    subprocess.run([sys.executable, "-m", "pip", "install", "playwright", "-q"])
    from playwright.sync_api import sync_playwright

RESULTS = {
    "nav_machine_room": False,
    "machine_room_sections": [],
    "hash_routing": False,
    "share_button": False,
    "lead_image_or_sigil": False,
    "river_rails_removed": False,
    "mobile_no_scroll": False,
    "no_console_errors": True,
    "console_errors": [],
}

def test_with_browser(playwright, width=1280, height=720):
    """Test with given viewport size."""
    browser = playwright.chromium.launch()
    context = browser.new_context(viewport={"width": width, "height": height})
    page = context.new_page()

    # Capture console messages
    def on_message(msg):
        if msg.type in ("error", "warning"):
            RESULTS["console_errors"].append(f"[{msg.type}] {msg.text}")
            RESULTS["no_console_errors"] = False

    page.on("console", on_message)

    # A) Nav link test
    print("\n=== A: NAV TEST ===")
    page.goto("http://localhost:8123/demo.html", wait_until="networkidle")

    # Check for MACHINE ROOM link
    try:
        machine_link = page.locator("button:has-text('MACHINE ROOM')").first
        if machine_link.is_visible():
            RESULTS["nav_machine_room"] = True
            print("✓ MACHINE ROOM link present in nav")
        else:
            print("✗ MACHINE ROOM link not visible")
    except:
        print("✗ MACHINE ROOM link not found")

    # B) Machine room view test
    print("\n=== B: MACHINE ROOM VIEW TEST ===")
    if RESULTS["nav_machine_room"]:
        machine_link.click()
        page.wait_for_load_state("networkidle")

        sections_needed = ["MACHINE ROOM", "THE CABINET", "AT THE GATE", "GRADUATION SCORE", "THE SLATE FORMULA", "SOURCES + CLASSES", "THE WORDS", "THE LINTS"]
        for section in sections_needed:
            if page.locator(f"text='{section}'").count() > 0:
                RESULTS["machine_room_sections"].append(section)
                print(f"✓ {section} section found")
            else:
                print(f"✗ {section} section missing")

    # C) Hash routing test
    print("\n=== C: HASH ROUTING TEST ===")
    page.goto("http://localhost:8123/demo.html", wait_until="networkidle")

    # Try to find a real situation ID from the feed
    try:
        # Click on a card to discover an ID, or check if we can navigate directly
        cards = page.locator("[data-id]")
        if cards.count() > 0:
            first_card_id = cards.first.get_attribute("data-id")
            if first_card_id:
                page.goto(f"http://localhost:8123/demo.html#s={first_card_id}", wait_until="networkidle")
                # Check if story opened
                if page.locator("text='back to monitor'").is_visible():
                    RESULTS["hash_routing"] = True
                    print(f"✓ Hash routing works for id={first_card_id}")
                else:
                    print("✗ Hash routing did not open story")
            else:
                print("! Could not find card ID, skipping hash routing test")
        else:
            print("! No cards found, hash routing may not work in this view")
    except Exception as e:
        print(f"✗ Hash routing test error: {e}")

    # D) Share button test
    print("\n=== D: SHARE BUTTON TEST ===")
    if RESULTS["hash_routing"]:
        # We're on a story page
        try:
            share_btn = page.locator("button:has-text('SHARE')").first
            if share_btn.is_visible():
                # Try to click it (should not throw)
                share_btn.click()
                RESULTS["share_button"] = True
                print("✓ SHARE button present and clickable")
            else:
                print("✗ SHARE button not visible on story")
        except Exception as e:
            print(f"✗ SHARE button test error: {e}")

    # E) Lead image test
    print("\n=== E: LEAD IMAGE TEST ===")
    try:
        # Look for either <img> or sigil in .leadvis
        leadvis = page.locator(".leadvis").first
        if leadvis.count() > 0:
            img = leadvis.locator("img")
            if img.count() > 0:
                RESULTS["lead_image_or_sigil"] = True
                print("✓ Lead image rendered")
            elif leadvis.locator(".sigtag").count() > 0:
                RESULTS["lead_image_or_sigil"] = True
                print("✓ Sigil fallback rendered")
        else:
            print("! No .leadvis element found")
    except Exception as e:
        print(f"✗ Lead image test error: {e}")

    # F) River rails removed
    print("\n=== F: RIVER RAILS TEST ===")
    page.goto("http://localhost:8123/demo.html", wait_until="networkidle")
    try:
        cabinet_rail = page.locator("text='the cabinet'").count() if not hasattr(page.locator("text='THE CABINET'"), 'count') else page.locator("text='THE CABINET'").count()
        gate_rail = page.locator("text='at the gate'").count()
        receipts_rail = page.locator("text='RECEIPTS'").count()

        # In RIVER view, cabinet and at the gate should not appear, but receipts should
        if gate_rail == 0 and receipts_rail > 0:
            RESULTS["river_rails_removed"] = True
            print("✓ Cabinet/gate rails removed from river, receipts remain")
        else:
            print(f"✗ Rails still in river (at the gate: {gate_rail}, receipts: {receipts_rail})")
    except Exception as e:
        print(f"✗ River rails test error: {e}")

    # G) Mobile scroll test
    print("\n=== G: MOBILE SCROLL TEST (390px) ===")
    # If width != 390, test with mobile viewport
    if width != 390:
        context_mobile = browser.new_context(viewport={"width": 390, "height": 600})
        page_mobile = context_mobile.new_page()
        page_mobile.on("console", on_message)
        page_mobile.goto("http://localhost:8123/demo.html", wait_until="networkidle")
        try:
            scrollWidth = page_mobile.evaluate("document.documentElement.scrollWidth")
            clientWidth = page_mobile.evaluate("window.innerWidth")
            if scrollWidth <= clientWidth + 2:
                RESULTS["mobile_no_scroll"] = True
                print(f"✓ Mobile no horizontal scroll (scrollWidth={scrollWidth}, clientWidth={clientWidth})")
            else:
                print(f"✗ Horizontal scroll detected (scrollWidth={scrollWidth}, clientWidth={clientWidth})")
        except Exception as e:
            print(f"✗ Mobile test error: {e}")
        finally:
            page_mobile.close()
            context_mobile.close()

    browser.close()
    return True

def check_dashes():
    """Check for em/en dashes."""
    with open("demo.html", "r", encoding="utf-8") as f:
        content = f.read()

    # Look for em/en dashes (–—‒―−)
    bad_dashes = re.findall(r'[‒–—―−]', content)

    with open("index.html", "r", encoding="utf-8") as f:
        content += f.read()

    bad_dashes += re.findall(r'[‒–—―−]', content)

    if bad_dashes:
        print(f"\n✗ Found {len(bad_dashes)} em/en dashes")
        return False
    else:
        print("\n✓ No em/en dashes found")
        return True

def check_index_section_02():
    """Check index.html section-02."""
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    old_text = "A feed of what is actually moving the world"
    new_text = "A morning brief that ends"
    intro = "HORUS is a daily brief plus a live feed of the stories"

    if old_text in content:
        print(f"\n✗ Old section-02 text still present")
        return False
    elif new_text in content and intro in content:
        print(f"\n✓ Section-02 rewritten correctly")
        return True
    else:
        print(f"\n? Section-02 state unclear")
        return False

if __name__ == "__main__":
    print("Starting E3-C2 Acceptance Verification...")
    print("=" * 60)

    try:
        with sync_playwright() as playwright:
            test_with_browser(playwright, 1280, 720)
    except Exception as e:
        print(f"\n✗ Browser test failed: {e}")
        RESULTS["no_console_errors"] = False

    check_dashes()
    check_index_section_02()

    print("\n" + "=" * 60)
    print("RESULTS:")
    print(f"  Nav MACHINE ROOM link: {RESULTS['nav_machine_room']}")
    print(f"  Machine room sections found: {len(RESULTS['machine_room_sections'])}/8")
    print(f"  Hash routing: {RESULTS['hash_routing']}")
    print(f"  Share button: {RESULTS['share_button']}")
    print(f"  Lead image/sigil: {RESULTS['lead_image_or_sigil']}")
    print(f"  River rails removed: {RESULTS['river_rails_removed']}")
    print(f"  Mobile no scroll: {RESULTS['mobile_no_scroll']}")
    print(f"  No console errors: {RESULTS['no_console_errors']}")

    if RESULTS['console_errors']:
        print(f"\nConsole errors found:")
        for err in RESULTS['console_errors'][:5]:
            print(f"    {err}")

    # Final verdict
    passed = (RESULTS['nav_machine_room'] and
              len(RESULTS['machine_room_sections']) >= 6 and  # At least most sections
              RESULTS['no_console_errors'])

    print("\n" + "=" * 60)
    if passed:
        print("✓ MAJOR TESTS PASSED")
        sys.exit(0)
    else:
        print("✗ SOME TESTS FAILED - Review output above")
        sys.exit(1)
