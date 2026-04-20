from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def is_item_present(self):
        return self.page.locator(".cart_item").count() > 0

    def proceed_to_checkout(self):
        self.click("#checkout")
        