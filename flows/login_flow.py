from pages.login_page import LoginPage
from test_data.users import get_user
import os


class LoginFlow:
    def __init__(self, driver):
        self.login_page = LoginPage(driver)

    def login(self, username, password):
        self.login_page.login(username, password)

    def login_as_user(self, user_type="standard"):
        user = get_user(user_type)

        # Env override (kept for CI/CD, non-breaking)
        username = os.getenv(f"{user_type.upper()}_USERNAME", user["username"])
        password = os.getenv(f"{user_type.upper()}_PASSWORD", user["password"])

        self.login(username, password)

    # backward compatibility
    def login_as_standard_user(self):
        self.login_as_user("standard")
        
        
        