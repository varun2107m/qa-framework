from pytest_bdd import when, then
from pages.cart_page import CartPage


@when("user proceeds to checkout")
def proceed_to_checkout(page):
    CartPage(page).proceed_to_checkout()


@then("cart should contain items")
def cart_has_items(page):
    assert CartPage(page).is_item_present(), "Expected items in cart but cart was empty"
    
    
