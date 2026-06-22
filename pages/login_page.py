from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    EMAIL_INPUT = "input[data-qa='login-email']"
    PASSWORD_INPUT = "input[data-qa='login-password']"
    LOGIN_BUTTON = "button[data-qa='login-button']"
    LOGGED_IN_AS_TEXT = "li:has-text('Logged in as')"
    LOGIN_ERROR_TEXT = "p:has-text('Your email or password is incorrect!')"

    def __init__(self, page: Page, base_url: str):
        super().__init__(page)
        self.base_url = base_url

    def open_login_page(self) -> None:
        self.open(f"{self.base_url}/login")

    def login(self, email: str, password: str) -> None:
        self.page.fill(self.EMAIL_INPUT, email)
        self.page.fill(self.PASSWORD_INPUT, password)
        self.page.click(self.LOGIN_BUTTON)

    def assert_logged_in(self) -> None:
        expect(self.page.locator(self.LOGGED_IN_AS_TEXT)).to_be_visible()
