import pytest
from dotenv import load_dotenv
from utils.config_reader import get_base_url

load_dotenv()


@pytest.fixture
def driver(page):
    page.goto(get_base_url())
    return page



