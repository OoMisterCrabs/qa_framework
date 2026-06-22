from dataclasses import dataclass
from playwright.sync_api import Page
from pages.base_page import BasePage


@dataclass
class CartItem:
    name: str
    price: str
    quantity: str
    total: str


class CartPage(BasePage):
    CART_ROWS = "#cart_info_table tbody tr"
    ITEM_NAME = ".cart_description h4 a"
    ITEM_PRICE = ".cart_price p"
    ITEM_QUANTITY = ".cart_quantity button"
    ITEM_TOTAL = ".cart_total .cart_total_price"
    PROCEED_TO_CHECKOUT_BUTTON = "a:has-text('Proceed To Checkout')"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open_cart_page(self) -> None:
        self.open(f"{self.base_url}/view_cart")

    def get_cart_items(self) -> list[CartItem]:
        rows = self.page.locator(self.CART_ROWS)
        items: list[CartItem] = []

        for i in range(rows.count()):
            row = rows.nth(i)
            items.append(
                CartItem(
                    name=row.locator(self.ITEM_NAME).inner_text().strip(),
                    price=row.locator(self.ITEM_PRICE).inner_text().strip(),
                    quantity=row.locator(self.ITEM_QUANTITY).inner_text().strip(),
                    total=row.locator(self.ITEM_TOTAL).inner_text().strip(),
                )
            )
        return items

    def assert_items_present(self, expected_names: list[str]) -> None:
        actual_names = [item.name for item in self.get_cart_items()]

        for expected_name in expected_names:
            assert expected_name in actual_names, (
                f"Product '{expected_name}' was not found in cart. "
                f"Cart contains: {actual_names}"
            )

    def proceed_to_checkout(self) -> None:
        self.page.click(self.PROCEED_TO_CHECKOUT_BUTTON)
