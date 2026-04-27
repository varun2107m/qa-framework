from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError
from utils.logger import get_logger

logger = get_logger("base_page")


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def click(self, locator: str, retries: int = 3, timeout: int = 5000):
        for attempt in range(1, retries + 1):
            try:
                self.page.locator(locator).click(timeout=timeout)
                return
            except PlaywrightTimeoutError:    # ✅ only catches actual timeout errors
                logger.warning(
                    f"[click] Attempt {attempt}/{retries} timed out for '{locator}'"
                )
                if attempt == retries:
                    raise
                self.page.wait_for_timeout(1000)  # ✅ Playwright-native, non-blocking

    def fill(self, locator: str, value: str, timeout: int = 5000):
        # ✅ wait for visibility before filling
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)
        self.page.locator(locator).fill(value)

    def wait_for_element(self, locator: str, timeout: int = 5000):
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)

    def get_text(self, locator: str, timeout: int = 5000) -> str:
        self.page.locator(locator).wait_for(state="visible", timeout=timeout)
        return self.page.locator(locator).inner_text()

    def is_visible(self, locator: str) -> bool:
        return self.page.locator(locator).is_visible()
    
        