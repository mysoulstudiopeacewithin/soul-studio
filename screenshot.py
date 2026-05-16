import sys
import os
from playwright.sync_api import sync_playwright

PORT = 8080
URL = f"http://localhost:{PORT}/"
OUT = os.path.join(os.path.dirname(__file__), "screenshot.png")

def take_screenshot():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 390, "height": 844})
        try:
            page.goto(URL, timeout=5000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            page.screenshot(path=OUT, full_page=False)
            print(f"Screenshot saved: {OUT}")
        except Exception as e:
            print(f"Screenshot failed: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    take_screenshot()
