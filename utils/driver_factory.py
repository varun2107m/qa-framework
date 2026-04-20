import os
from playwright.sync_api import sync_playwright


def get_browser():
    browser_name = os.getenv("BROWSER", "chromium")
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    slow_mo = int(os.getenv("SLOW_MO", "0"))

    supported_browsers = ["chromium", "firefox", "webkit"]
    if browser_name not in supported_browsers:
        raise ValueError(f"Unsupported browser '{browser_name}'. Choose from: {supported_browsers}")

    playwright = sync_playwright().start()

    browser = getattr(playwright, browser_name).launch(
        headless=headless,
        slow_mo=slow_mo
    )

    context = browser.new_context(
        viewport={"width": 1280, "height": 720}
    )

    page = context.new_page()
    page.set_default_timeout(60000)
    page.set_default_navigation_timeout(60000)

    return playwright, browser, context, page


def teardown_browser(playwright, browser, context):
    context.close()
    browser.close()
    playwright.stop()
    
