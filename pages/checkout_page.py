class CheckoutPage:
    def __init__(self, page):
        self.page = page

    def enter_details(self):
        self.page.fill("#first-name", "John")
        self.page.fill("#last-name", "Doe")
        self.page.fill("#postal-code", "12345")
        self.page.click("#continue")

    def finish_order(self):
        self.page.click("#finish")

    def is_order_successful(self):
        return self.page.locator(".complete-header").inner_text() == "Thank you for your order!"
    