import random
from dataclasses import dataclass
from playwright.sync_api import Page
from pages.base_page import BasePage


@dataclass
class AddedProduct:
    name: str
    index: int


class ProductsPage(BasePage):
    PRODUCT_CARDS = ".features_items .product-image-wrapper"
    PRODUCT_NAME_IN_CARD = ".productinfo p"
    ADD_TO_CART_BUTTON_IN_CARD = ".productinfo .add-to-cart"
    CONTINUE_SHOPPING_BUTTON = ".modal-content button:has-text('Continue Shopping')"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open_products_page(self) -> None:
        self.open(f"{self.base_url}/products")

    def add_random_products_to_cart(self, count: int = 2) -> list[AddedProduct]:
        cards = self.page.locator(self.PRODUCT_CARDS)
        total_count = cards.count()
        assert total_count >= count, (
            f"Product count: ({total_count}), is less than needed: ({count})"
        )

        chosen_indexes = random.sample(range(total_count), count)
        added: list[AddedProduct] = []

        for idx in chosen_indexes:
            card = cards.nth(idx)
            name = card.locator(self.PRODUCT_NAME_IN_CARD).inner_text().strip()

            card.hover()
            card.locator(self.ADD_TO_CART_BUTTON_IN_CARD).click()

            self.page.click(self.CONTINUE_SHOPPING_BUTTON)
            added.append(AddedProduct(name=name, index=idx))

        return added
