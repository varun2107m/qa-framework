from pytest_bdd import given, when, then, parsers
from utils.config_reader import load_config
from pages.login_page import LoginPage


@given("user opens the application")
def open_application(page):
    config = load_config()
    env = config.get("env", "qa")
    base_url = config["environments"][env]["base_url"]
    page.goto(base_url)


@given(parsers.parse('user logs in with "{username}" and "{password}"'))
@when(parsers.parse('user logs in with "{username}" and "{password}"'))
def login_with_credentials(page, username, password):
    LoginPage(page).login(username, password)


@then(parsers.parse('the URL should contain "{path}"'))
def url_should_contain(page, path):
    assert path in page.url, f"Expected '{path}' in URL, got: {page.url}"


@then("no error message should be displayed")
def no_error_message(page):
    assert not page.locator("[data-test='error']").is_visible()
    
    