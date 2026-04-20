class InventoryPage:
    def __init__(self, page):
        self.page = page

    def is_inventory_visible(self):
        return self.page.locator(".inventory_list").is_visible()

    def add_first_item_to_cart(self):
        self.page.locator(".inventory_item button").first.click()

    def go_to_cart(self):
        self.page.click(".shopping_cart_link")

    def is_item_in_cart(self):
        return self.page.locator(".shopping_cart_badge").is_visible()
    
