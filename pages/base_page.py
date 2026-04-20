from playwright.sync_api import Page
import time

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click(self, locator, retries=3):
        for attempt in range(retries):
            try:
                self.page.locator(locator).click(timeout=5000)
                return
            except Exception:
                if attempt == retries - 1:
                    raise
                time.sleep(1)

    def fill(self, locator, value):
        self.page.locator(locator).fill(value)

    def wait_for_element(self, locator):
        self.page.locator(locator).wait_for(state="visible", timeout=5000)
        