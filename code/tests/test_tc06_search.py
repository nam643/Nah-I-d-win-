"""
TC06 - F6 Searching for a Product
Tester: [FILL]
Counts are taken from the first results page (enough for 'iPod', which fits on one page) [VERIFY].
Evidence: evidence/TC06_*.png
"""

import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import helpers


def test_tc06_s1_matching_keyword(driver):
    """S1 (success): 'iPod' -> results page listing only iPod products."""
    helpers.search(driver, "iPod")
    names = helpers.result_names(driver)
    helpers.shot(driver, "TC06_S1")
    assert "search=iPod" in driver.current_url
    assert "Search - iPod" in helpers.body_text(driver)
    assert names, "Expected at least one result"
    assert all("ipod" in n.lower() for n in names), f"Unrelated results: {names}"


# S2 (validation): non-matching, blank and script-like input.
@pytest.mark.parametrize(
    "case, keyword",
    [("a", "xyzqwe123"), ("b", ""), ("c", "<script>alert(1)</script>")],
)
def test_tc06_s2_unmatched_blank_and_script(driver, case, keyword):
    helpers.search(driver, keyword)
    # (c) A script must never run: no JavaScript alert may appear
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        alert_opened = True
        driver.switch_to.alert.dismiss()
    except TimeoutException:
        alert_opened = False
    names = helpers.result_names(driver)
    helpers.shot(driver, f"TC06_S2{case}")
    assert not alert_opened, "Search input was executed as script (XSS)"
    assert names == [], f"Expected no products, got {names}"
    if keyword:   # (a) and (c) show the no-match message; (b) blank only needs no error and no products
        assert helpers.MSG_SEARCH_NO_MATCH in helpers.body_text(driver)


# S3 (edge): case, partial word and surrounding spaces should give the same results as 'iPod'.
@pytest.mark.parametrize("case, keyword", [("a", "IPOD"), ("b", "ipo"), ("c", "   iPod   ")])
def test_tc06_s3_case_partial_and_spaces(driver, case, keyword):
    helpers.search(driver, "iPod")
    baseline = len(helpers.result_names(driver))                    # N from the S1 keyword

    helpers.search(driver, keyword)
    names = helpers.result_names(driver)
    helpers.shot(driver, f"TC06_S3{case}")
    assert len(names) == baseline, f"{keyword!r}: {len(names)} results, expected {baseline}"
    assert all("ipod" in n.lower() for n in names)
