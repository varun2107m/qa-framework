from pytest_bdd import given, when, then, parsers
from pages.login_page import LoginPage
from test_data.users import get_user
from utils.config_reader import get_base_url
import os


@given("user opens the application")
def open_application(page):
    page.goto(get_base_url())


# ✅ Single definition — shared across ALL feature files via load_steps.py
@given("user is logged into saucedemo")
def user_logged_in(page):
    page.goto(get_base_url())

    try:
        user = get_user("standard")
        username, password = user["username"], user["password"]
    except ValueError:
        username = os.getenv("STANDARD_USERNAME", "standard_user")
        password = os.getenv("STANDARD_PASSWORD", "secret_sauce")

    LoginPage(page).login(username, password)
    assert "inventory" in page.url, f"Login failed — current URL: {page.url}"


@given("user opens saucedemo login page")
def open_login_page(page):
    page.goto(get_base_url())


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

    
    