import pytest
from pytest_bdd import scenarios, given, when, then, parsers
from utils.config_reader import load_config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.smoke

scenarios("../features/saucedemo.feature")


# ----------------------------
# GIVEN
# ----------------------------
@given("user opens saucedemo login page")
def open_login(page):
    config = load_config()
    page.goto(config["environments"]["qa"]["base_url"])


@given("user is logged into saucedemo")
def user_logged_into_saucedemo(page):
    config = load_config()
    page.goto(config["environments"]["qa"]["base_url"])
    LoginPage(page).login("standard_user", "secret_sauce")
    assert "inventory" in page.url


# ----------------------------
# WHEN
# ----------------------------
@when(parsers.parse('user logs in with "{username}" and "{password}"'))
def login(page, username, password):
    LoginPage(page).login(username, password)


@when("user adds item to cart")
def add_item_to_cart(page):
    InventoryPage(page).add_first_item_to_cart()


# ----------------------------
# THEN
# ----------------------------
@then("inventory page should be displayed")
def verify_inventory(page):
    assert InventoryPage(page).is_inventory_visible()


@then("item should be visible in cart")
def verify_item_in_cart(page):
    assert InventoryPage(page).is_item_in_cart()

    
