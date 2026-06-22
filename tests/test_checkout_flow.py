import allure
import pytest
from playwright.sync_api import Page
from api.account_api import UserData
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from tests.conftest import BASE_URL


@allure.feature("Checkout flow")
@allure.story("Full scenario: API setup + UI checkout + API teardown")
@pytest.mark.smoke
def test_full_checkout_flow(browser_page: Page, registered_user: UserData):

    login_page = LoginPage(browser_page, BASE_URL)
    products_page = ProductsPage(browser_page, BASE_URL)
    cart_page = CartPage(browser_page, BASE_URL)
    checkout_page = CheckoutPage(browser_page, BASE_URL)

    with allure.step("1. Open login page"):
        login_page.open_login_page()

    with allure.step("2. Login as API created user"):
        login_page.login(registered_user.email, registered_user.password)
        login_page.assert_logged_in()

    with allure.step("3. Add two products into the cart"):
        products_page.open_products_page()
        added_products = products_page.add_random_products_to_cart(count=2)
        added_names = [p.name for p in added_products]
        allure.attach(
            "\n".join(added_names),
            name="Products added",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("4. Open carts and check items"):
        cart_page.open_cart_page()
        cart_page.assert_items_present(added_names)
        cart_page.proceed_to_checkout()

    with allure.step("5. Checkout data check"):
        checkout_page.assert_address_matches_registration(registered_user)
