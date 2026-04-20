from pytest_bdd import given
from utils.config_reader import load_config
from pages.login_page import LoginPage


@given("user is logged into saucedemo")
def user_logged_in(page):
    config = load_config()
    page.goto(config["environments"]["qa"]["base_url"])
    LoginPage(page).login("standard_user", "secret_sauce")
    
    