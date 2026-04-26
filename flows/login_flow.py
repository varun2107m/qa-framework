import os
from pages.login_page import LoginPage


class LoginFlow:
    def __init__(self, driver):
        self.login_page = LoginPage(driver)

    def login_as_standard_user(self):
        username = os.getenv("APP_USERNAME", "standard_user")
        password = os.getenv("APP_PASSWORD", "secret_sauce")
        self.login_page.login(username, password)

    def login(self, username, password):
        self.login_page.login(username, password)
        
        