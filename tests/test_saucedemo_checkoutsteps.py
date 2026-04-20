import pytest
from pytest_bdd import scenarios, given, when, then
from pytest_bdd import scenarios
from utils.config_reader import load_config
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

# ✅ REGRESSION GROUP
pytestmark = pytest.mark.regression

# Load feature file
scenarios("../features/saucedemocheckout.feature")


# ----------------------------
# GIVEN
# ----------------------------
@given("user is logged into saucedemo")
def login_precondition(page):
    config = load_config()
    page.goto(config["environments"]["qa"]["base_url"])
    LoginPage(page).login("standard_user", "secret_sauce")


# ----------------------------
# WHEN
# ----------------------------
@when("user adds item to cart")
def add_to_cart(page):
    InventoryPage(page).add_first_item_to_cart()
    InventoryPage(page).go_to_cart()


@when("user proceeds to checkout")
def proceed_checkout(page):
    CartPage(page).proceed_to_checkout()


@when("user enters checkout details")
def enter_details(page):
    CheckoutPage(page).enter_details()
    CheckoutPage(page).finish_order()


# ----------------------------
# THEN
# ----------------------------
@then("order should be successfully placed")
def verify_order(page):
    assert CheckoutPage(page).is_order_successful()