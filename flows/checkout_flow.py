from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage

class CheckoutFlow:
    def __init__(self, driver):
        self.inventory = InventoryPage(driver)
        self.cart = CartPage(driver)
        self.checkout = CheckoutPage(driver)

    def complete_checkout(self):
        self.inventory.add_item_to_cart()
        self.inventory.go_to_cart()
        self.cart.click_checkout()
        self.checkout.enter_details("John", "Doe", "12345")
        self.checkout.finish_checkout()
        