import os
import pytest
import allure
from playwright.sync_api import sync_playwright, Page
from api.client import ApiClient
from api.account_api import AccountApiClient, UserData
from utils.data_factory import generate_unique_user

BASE_URL = "https://automationexercise.com"
API_BASE_URL = "https://automationexercise.com"


@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="session")
def browser(playwright_instance):
    headless = os.getenv("HEADLESS", "true").lower() != "false"
    browser_instance = playwright_instance.chromium.launch(headless=headless)
    yield browser_instance
    browser_instance.close()


@pytest.fixture
def browser_page(browser) -> Page:
    context = browser.new_context()
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="session")
def account_api() -> AccountApiClient:
    client = ApiClient(base_url=API_BASE_URL)
    return AccountApiClient(client)


@pytest.fixture
def registered_user(account_api: AccountApiClient):
    user: UserData = generate_unique_user()

    with allure.step(f"Creating user {user.email}"):
        account_api.create(user)

    yield user

    with allure.step(f"Deleting user {user.email}"):
        account_api.delete(user.email, user.password)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call" or not report.failed:
        return

    page: Page | None = item.funcargs.get("browser_page")
    if page is None:
        return

    try:
        screenshot_bytes = page.screenshot(full_page=True)
        allure.attach(
            screenshot_bytes,
            name="screenshot_on_failure",
            attachment_type=allure.attachment_type.PNG,
        )

        html_content = page.content()
        allure.attach(
            html_content,
            name="page_source_on_failure",
            attachment_type=allure.attachment_type.HTML,
        )
    except Exception as artifact_error:
        allure.attach(
            f"Artifact save failed: {artifact_error}",
            name="artifact_capture_error",
            attachment_type=allure.attachment_type.TEXT,
        )
