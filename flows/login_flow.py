from pages.login_page import LoginPage

class LoginFlow:
    def __init__(self, driver):
        self.login_page = LoginPage(driver)

    def login_as_standard_user(self):
        self.login_page.login("standard_user", "secret_sauce")
        