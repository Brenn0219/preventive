from playwright.sync_api import sync_playwright

def start_browser(headless=False):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()

    return p, browser, page