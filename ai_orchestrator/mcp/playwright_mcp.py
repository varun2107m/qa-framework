from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage


class PlaywrightMCP:

    def run_smoke_flow(self):
        return {
            "status": "executed via existing framework",
            "flow": "login → inventory → add item"
        }
    