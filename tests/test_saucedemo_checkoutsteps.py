import pytest
from pytest_bdd import scenarios, when, then      # ✅ removed: given (duplicate import too)
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

pytestmark = pytest.mark.regression

scenarios("../features/saucedemocheckout.feature")

# @given("user is logged into saucedemo") is inherited from common_steps.py


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


@then("order should be successfully placed")
def verify_order(page):
    assert CheckoutPage(page).is_order_successful()
    