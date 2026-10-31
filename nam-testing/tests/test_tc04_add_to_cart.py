"""
T004 - F4 Adding a Product to Shopping Cart
Tester: Nam
Product: iPod Touch (product_id=32), $122.00 incl. tax, 999 in stock in the demo catalogue.
Each test gets a new browser, so the cart starts empty.
Totals are compared with Decimal (exact), never floats.
Evidence: evidence/TC04_*.png
"""

import pytest
from selenium.webdriver.support.ui import WebDriverWait

import helpers

IPOD_TOUCH = 32


def test_tc04_s1_add_valid_quantities(driver):
    """S1 (success): add 1, then 2 more -> one cart line, quantity 3, line total = 3 x unit price."""
    helpers.search(driver, "iPod Touch")                            # F6 test-flow dependency
    helpers.open_from_results(driver, IPOD_TOUCH)

    helpers.add_to_cart(driver, 1)
    shown = helpers.wait_for_text(driver, helpers.MSG_CART_ADDED)
    helpers.shot(driver, "TC04_S1a")
    assert shown, "No 'added to your shopping cart' alert"

    helpers.add_to_cart(driver, 2)
    assert helpers.wait_for_text(driver, helpers.MSG_CART_ADDED)

    lines = helpers.cart_lines(driver)
    helpers.shot(driver, "TC04_S1b")
    assert len(lines) == 1, f"Expected one cart line, got {lines}"
    line = lines[0]
    assert "iPod Touch" in line["name"]
    assert line["quantity"] == 3
    assert line["total"] == 3 * line["unit"]                        # e.g. 3 x $122.00 = $366.00


# S2 (validation): quantities outside the valid class (>= 1) must not reach the cart.
@pytest.mark.parametrize("case, quantity", [("a", "0"), ("b", "-1"), ("c", "abc")])
def test_tc04_s2_invalid_quantities(driver, case, quantity):
    helpers.open_product(driver, IPOD_TOUCH)
    helpers.add_to_cart(driver, quantity)
    message = helpers.wait_for_any_text(driver, ["Minimum", "Warning", helpers.MSG_CART_ADDED])
    helpers.shot(driver, f"TC04_S2{case}")                          # records whatever the site said
    lines = helpers.cart_lines(driver)
    assert lines == [], f"Cart should be empty after quantity {quantity!r}, got {lines}"
    # The invalid quantity must be refused, not confirmed with the normal success alert
    assert message != helpers.MSG_CART_ADDED, (
        f"Quantity {quantity!r}: the site showed the 'added to your shopping cart' success alert, "
        "although nothing was added (cart is empty)")


def test_tc04_s3_quantity_above_stock(driver):
    """S3 (edge): quantity 9999 -> cart flags the line (***) and checkout does not proceed."""
    helpers.open_product(driver, IPOD_TOUCH)
    helpers.add_to_cart(driver, 9999)
    helpers.wait_for_any_text(driver, ["Minimum", "Warning", helpers.MSG_CART_ADDED])

    helpers.cart_lines(driver)                                      # opens the cart page
    stock_warning = helpers.wait_for_text(driver, helpers.MSG_CART_STOCK, timeout=5)
    helpers.shot(driver, "TC04_S3a")
    assert stock_warning, "Expected the out-of-stock warning in the cart"

    driver.get(helpers.url("checkout/checkout"))                    # try to check out
    WebDriverWait(driver, helpers.TIMEOUT).until(lambda d: helpers.on_route(d, "checkout/"))
    helpers.shot(driver, "TC04_S3b")
    assert helpers.on_route(driver, "checkout/cart"), "Checkout should send the user back to the cart"
