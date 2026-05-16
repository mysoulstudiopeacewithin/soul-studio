import sys
import os
import threading
import http.server
from playwright.sync_api import sync_playwright

PORT = 8080
DIR = os.path.dirname(__file__)

def take_screenshot(page_file, out_file):
    url = f"http://localhost:{PORT}/{page_file}"
    out = os.path.join(DIR, out_file)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page(viewport={"width": 390, "height": 844})
        try:
            page.goto(url, timeout=8000, wait_until="domcontentloaded")
            page.wait_for_timeout(2000)
            page.screenshot(path=out, full_page=False)
            print(f"Saved: {out}")
        except Exception as e:
            print(f"Failed: {e}", file=sys.stderr)
            sys.exit(1)
        finally:
            browser.close()

if __name__ == "__main__":
    handler = http.server.SimpleHTTPRequestHandler
    handler.log_message = lambda *a: None
    server = http.server.HTTPServer(("", PORT), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)

    os.chdir(DIR)
    thread.start()

    take_screenshot("index.html", "screenshot.png")
    take_screenshot("body-restoration.html", "screenshot-br.png")

    server.shutdown()
    print("Done.")
