from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from data.data_factory import get_checkout_data


class CheckoutFlow:
    def __init__(self, driver):
        self.inventory = InventoryPage(driver)
        self.cart = CartPage(driver)
        self.checkout = CheckoutPage(driver)

    def complete_checkout(self, data=None):
     if data is None:
        data = get_checkout_data()

        self.inventory.add_first_item_to_cart()  # ✅ matches InventoryPage
        self.inventory.go_to_cart()

        self.cart.proceed_to_checkout()          # ✅ matches CartPage

        self.checkout.enter_details(data)        # ✅ correct signature — pass the dict
        self.checkout.finish_order() 
        
