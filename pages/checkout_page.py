from dataclasses import dataclass
from playwright.sync_api import Page
from pages.base_page import BasePage
from api.account_api import UserData


@dataclass
class ParsedAddress:
    full_name: str
    address_lines: list[str]
    raw_text: str


class CheckoutPage(BasePage):
    DELIVERY_ADDRESS_BLOCK = "#address_delivery"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def get_delivery_address(self) -> ParsedAddress:
        block = self.page.locator(self.DELIVERY_ADDRESS_BLOCK)
        raw_text = block.inner_text()

        lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

        return ParsedAddress(
            full_name=lines[0] if lines else "",
            address_lines=lines[1:],
            raw_text=raw_text,
        )

    def assert_address_matches_registration(self, user: UserData) -> None:
        parsed = self.get_delivery_address()
        full_text_normalized = parsed.raw_text.lower()

        fields_to_check = {
            "firstname": user.firstname,
            "lastname": user.lastname,
            "address1": user.address1,
            "city": user.city,
            "zipcode": user.zipcode,
            "state": user.state,
        }

        missing_fields = []
        for field_name, expected_value in fields_to_check.items():
            if expected_value.lower() not in full_text_normalized:
                missing_fields.append((field_name, expected_value))

        assert not missing_fields, (
            "Address save failed.\n"
            f"Fields not found: {missing_fields}\n"
            f"Page error text: {parsed.raw_text!r}"
        )
