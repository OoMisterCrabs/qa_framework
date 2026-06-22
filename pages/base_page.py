from playwright.sync_api import Page


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def open(self, url: str) -> None:
        self.page.goto(url)

    def is_visible(self, locator: str) -> bool:
        return self.page.locator(locator).is_visible()

    def text_of(self, locator: str) -> str:
        return self.page.locator(locator).inner_text().strip()
