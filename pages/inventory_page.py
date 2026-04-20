from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def is_inventory_visible(self):
        return self.page.locator(".inventory_list").is_visible()

    def add_first_item_to_cart(self):
        self.page.wait_for_selector(".inventory_item button")
        self.page.locator("[data-test^='add-to-cart']").first.click()

    def go_to_cart(self):
        self.click(".shopping_cart_link")

    def is_item_in_cart(self):
        return self.page.locator(".shopping_cart_badge").is_visible()
    
