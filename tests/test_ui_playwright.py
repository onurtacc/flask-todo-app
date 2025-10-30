from playwright.sync_api import sync_playwright

def test_add_todo_and_screenshot():
    # Ensure the app is running in Terminal A at http://127.0.0.1:5000
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto("http://127.0.0.1:5000")
        # Try common selectors; adjust if the HTML uses different names/ids.
        # Use "python -m playwright codegen http://127.0.0.1:5000" to discover exact selectors.
        page.fill('input[name="title"]', "Buy milk")
        try:
            page.fill('input[name="description"]', "2L semi-skimmed")
        except Exception:
            pass
        page.click('text=Add')  # or the button text/id rendered on the page
        page.screenshot(path="artifacts/ui_after_add.png", full_page=True)
        assert "Buy milk" in page.content()
        browser.close()
