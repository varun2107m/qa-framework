from pages.base_page import BasePage
from testdata.data_factory import get_checkout_data


class CheckoutPage(BasePage):
    def __init__(self, page):
        super().__init__(page)

    def enter_details(self, data=None):
        if data is None:
            data = get_checkout_data()
        self.fill("#first-name", data["first_name"])
        self.fill("#last-name", data["last_name"])
        self.fill("#postal-code", data["postal_code"])
        self.click("#continue")

    def finish_order(self):
        self.click("#finish")

    def is_order_successful(self):
        return self.page.locator(".complete-header").inner_text() == "Thank you for your order!"
    
    