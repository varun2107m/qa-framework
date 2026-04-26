import pytest
from utils.driver_factory import get_browser, teardown_browser
from utils.config_reader import get_config


@pytest.fixture
def driver():
    playwright, browser, context, page = get_browser()

    # ✅ Fetch base URL from config
    base_url = get_config("base_url")

    if not base_url:
        raise ValueError("base_url not found in config")

    page.goto(base_url)

    yield page  # Expose Playwright page as driver

    teardown_browser(playwright, browser, context)
    
