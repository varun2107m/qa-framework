import os
import pytest
from pytest_bdd import scenarios, when, then, parsers
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

pytestmark = pytest.mark.smoke

BASE_DIR = os.path.dirname(__file__)
scenarios(os.path.join(BASE_DIR, "features", "saucedemo.feature"))


@when(parsers.parse('user logs in with "{username}" and "{password}"'))
def login(page, username, password):
    LoginPage(page).login(username, password)


@when("user adds item to cart")
def add_item_to_cart(page):
    InventoryPage(page).add_first_item_to_cart()


@then("inventory page should be displayed")
def verify_inventory(page):
    assert InventoryPage(page).is_inventory_visible()


@then("item should be visible in cart")
def verify_item_in_cart(page):
    assert InventoryPage(page).is_item_in_cart()
    



    
