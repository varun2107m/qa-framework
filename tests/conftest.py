import pytest
import os
from dotenv import load_dotenv
from utils.config_reader import get_base_url

import tests.steps.common_steps
import tests.steps.cart_steps

from utils.driver_factory import get_browser, teardown_browser
from utils.config_reader import get_base_url



load_dotenv()


@pytest.fixture(scope="function")
def page():
    playwright, browser, context, page = get_browser()
    yield page
    teardown_browser(playwright, browser, context)


@pytest.fixture
def driver(page):
    page.goto(get_base_url())
    return page


