"""
T003 - F3 Comparing Products
Tester: Nam
Products (product_id): iPod Touch 32, iPod Nano 36, iPod Shuffle 34, iPod Classic 48, iPhone 40.
Each test gets a new browser, so the comparison list starts empty.
Evidence: evidence/TC03_*.png
"""

from selenium.webdriver.common.by import By

import helpers

IPOD_TOUCH, IPOD_NANO, IPOD_SHUFFLE, IPOD_CLASSIC, IPHONE = 32, 36, 34, 48, 40


def removes_for(driver, product_id):
    """Remove links that belong to one product column."""
    return [a for a in helpers.compare_removes(driver) if f"remove={product_id}" in a.get_attribute("href")]


def test_tc03_s1_compare_two_products(driver):
    """S1 (success): add two products (reached through search, F6) -> two columns side by side."""
    helpers.search(driver, "iPod")                                  # F6 test-flow dependency
    helpers.open_from_results(driver, IPOD_TOUCH)
    helpers.click(driver, helpers.visible(driver, helpers.compare_button(IPOD_TOUCH)))
    assert helpers.wait_for_text(driver, helpers.MSG_COMPARE_ADDED), "No 'added to comparison' alert"

    helpers.search(driver, "iPod")
    helpers.open_from_results(driver, IPOD_NANO)
    helpers.click(driver, helpers.visible(driver, helpers.compare_button(IPOD_NANO)))
    assert helpers.wait_for_text(driver, helpers.MSG_COMPARE_ADDED)

    driver.get(helpers.url("product/compare"))
    helpers.shot(driver, "TC03_S1")   # check name, price, model, availability against each product page
    text = helpers.body_text(driver)
    assert "iPod Touch" in text and "iPod Nano" in text
    assert len(helpers.compare_removes(driver)) == 2                # exactly two product columns


def test_tc03_s2_remove_until_empty(driver):
    """S2 (validation): remove one product, then the last, then reopen the empty list in a fresh session."""
    assert helpers.add_to_compare(driver, IPOD_TOUCH)
    assert helpers.add_to_compare(driver, IPOD_NANO)
    driver.get(helpers.url("product/compare"))

    helpers.click(driver, removes_for(driver, IPOD_TOUCH)[0])       # (a) remove 1 of 2
    shown = helpers.wait_for_text(driver, helpers.MSG_COMPARE_MODIFIED)
    helpers.shot(driver, "TC03_S2a")
    assert shown
    assert len(helpers.compare_removes(driver)) == 1
    assert not removes_for(driver, IPOD_TOUCH)                      # the removed one is gone

    helpers.click(driver, removes_for(driver, IPOD_NANO)[0])        # (b) remove the last product
    empty_b = helpers.wait_for_text(driver, helpers.MSG_COMPARE_EMPTY, timeout=5)
    page_b = driver.find_element(By.ID, "content").text
    helpers.shot(driver, "TC03_S2b")
    assert not helpers.compare_removes(driver), "No product column should remain"

    driver.delete_all_cookies()                                     # (c) fresh session, open URL directly
    driver.get(helpers.url("product/compare"))
    empty_c = helpers.wait_for_text(driver, helpers.MSG_COMPARE_EMPTY, timeout=5)
    page_c = driver.find_element(By.ID, "content").text
    helpers.shot(driver, "TC03_S2c")
    assert not helpers.compare_removes(driver), "A new session should have an empty list"

    # Both screenshots are saved first, so a wrong message is reported without hiding S2c.
    assert empty_b, f"S2b: empty list should say '{helpers.MSG_COMPARE_EMPTY}', page shows: {page_b!r}"
    assert empty_c, f"S2c: empty list should say '{helpers.MSG_COMPARE_EMPTY}', page shows: {page_c!r}"


def test_tc03_s3_four_product_limit_and_duplicates(driver):
    """S3 (edge): 4 products fit; a 5th pushes out the oldest; adding the same product twice lists it once."""
    for pid in (IPOD_TOUCH, IPOD_NANO, IPOD_SHUFFLE, IPOD_CLASSIC):
        assert helpers.add_to_compare(driver, pid)
    driver.get(helpers.url("product/compare"))
    helpers.shot(driver, "TC03_S3a")
    assert len(helpers.compare_removes(driver)) == 4                # (a) four columns

    assert helpers.add_to_compare(driver, IPHONE)                   # (b) a fifth product
    driver.get(helpers.url("product/compare"))
    helpers.shot(driver, "TC03_S3b")
    assert len(helpers.compare_removes(driver)) == 4, "List should stay at four products"
    assert removes_for(driver, IPHONE), "Newest product should be in the list"
    assert not removes_for(driver, IPOD_TOUCH), "Oldest product should have been dropped"

    assert helpers.add_to_compare(driver, IPHONE)                   # (c) the same product again
    driver.get(helpers.url("product/compare"))
    helpers.shot(driver, "TC03_S3c")
    assert len(removes_for(driver, IPHONE)) == 1, "Duplicate product should appear once"
    assert len(driver.find_elements(By.XPATH, "//h1")) >= 1         # page rendered, no error
