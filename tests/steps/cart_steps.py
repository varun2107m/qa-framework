from pytest_bdd import when
from pages.inventory_page import InventoryPage


@when("user adds item to cart")
def add_item(page):
    InventoryPage(page).add_first_item_to_cart()
    InventoryPage(page).go_to_cart()
    
