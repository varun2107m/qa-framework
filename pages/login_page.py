from pages.base_page import BasePage
 
 
class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
 
    def login(self, username, password):
        self.fill("#user-name", username)
        self.fill("#password", password)
        self.click("#login-button")
        