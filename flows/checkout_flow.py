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
        """
        Complete end-to-end checkout flow.
        If data is not provided, it will be fetched from data_factory.
        """

        # Load data (default or passed)
        if data is None:
            data = get_checkout_data()

        # Flow steps
        self.inventory.add_item_to_cart()
        self.inventory.go_to_cart()
        self.cart.click_checkout()

        self.checkout.enter_details(
            data["first_name"],
            data["last_name"],
            data["postal_code"]
        )

        self.checkout.finish_checkout()
        
