class CartPage:
    def __init__(self, page):
        self.page = page

    def is_item_present(self):
        return self.page.locator(".cart_item").count() > 0

    def proceed_to_checkout(self):
        self.page.click("#checkout")