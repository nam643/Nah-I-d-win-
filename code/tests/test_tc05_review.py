"""
TC05 - F5 Submitting a Product Review
Tester: [FILL]
Product: iPod Touch (product_id=32). Review text limits 25-1000 characters, name 3-25 [VERIFY].
If the site asks guests to log in before reviewing, the test logs in with the shared account (F1).
Evidence: evidence/TC05_*.png
"""

import pytest

import helpers

IPOD_TOUCH = 32
VALID_TEXT = "Great sound quality and the battery easily lasts a full day of use."


def open_review_form(driver, request, via_search=False):
    """Open the product page and the review form; log in first if guests may not review."""
    if via_search:
        helpers.search(driver, "iPod Touch")                        # F6 test-flow dependency
        helpers.open_from_results(driver, IPOD_TOUCH)
    else:
        helpers.open_product(driver, IPOD_TOUCH)
    if helpers.MSG_REVIEW_LOGIN in helpers.body_text(driver):        # F1 dependency, only if required
        account = request.getfixturevalue("account")
        helpers.login(driver, account.email, account.password)
        helpers.open_product(driver, IPOD_TOUCH)
    tabs = [t for t in driver.find_elements(*helpers.REVIEW_TAB) if t.is_displayed()]
    if tabs:                                                         # some layouts hide the form in a tab
        helpers.click(driver, tabs[0])


def submit_review(driver, name, text, rating):
    """Fill the review form; rating=None leaves the stars unselected."""
    helpers.type_into(helpers.visible(driver, helpers.REVIEW_NAME), name)
    helpers.type_into(helpers.visible(driver, helpers.REVIEW_TEXT), text)
    if rating is not None:
        star = driver.find_element("css selector", f"input[name='rating'][value='{rating}']")
        driver.execute_script("arguments[0].click();", star)        # stars are styled radios
    helpers.click(driver, helpers.visible(driver, helpers.REVIEW_SUBMIT))


def test_tc05_s1_valid_review(driver, request):
    """S1 (success): valid name, 67-character text, 4 stars -> submitted for approval."""
    open_review_form(driver, request, via_search=True)
    submit_review(driver, "Nam T", VALID_TEXT, 4)
    shown = helpers.wait_for_text(driver, helpers.MSG_REVIEW_THANKS)
    helpers.shot(driver, "TC05_S1")
    assert shown


# S2 (validation): one invalid field per input set, each with its own warning.
@pytest.mark.parametrize(
    "case, name, text, rating, expected",
    [
        ("a", "Nam T", VALID_TEXT, None, helpers.MSG_REVIEW_RATING),      # no rating
        ("b", "Na", VALID_TEXT, 4, helpers.MSG_REVIEW_NAME_LENGTH),        # name 2 chars (< 3)
        ("c", "Nam T", "Too short.", 4, helpers.MSG_REVIEW_TEXT_LENGTH),   # text 10 chars (< 25)
    ],
    ids=["S2a-no-rating", "S2b-name-2-chars", "S2c-text-10-chars"],
)
def test_tc05_s2_invalid_fields(driver, request, case, name, text, rating, expected):
    open_review_form(driver, request)
    submit_review(driver, name, text, rating)
    shown = helpers.wait_for_text(driver, expected)
    helpers.shot(driver, f"TC05_S2{case}")
    assert shown, f"Expected message: {expected}"
    assert helpers.MSG_REVIEW_THANKS not in helpers.body_text(driver)


# S3 (edge): review-text length just outside and exactly on each limit.
@pytest.mark.parametrize(
    "case, length, accepted",
    [("a", 24, False), ("b", 25, True), ("c", 1000, True), ("d", 1001, False)],
)
def test_tc05_s3_text_length_boundaries(driver, request, case, length, accepted):
    open_review_form(driver, request)
    submit_review(driver, "Nam T", helpers.make_text(length), 5)
    expected = helpers.MSG_REVIEW_THANKS if accepted else helpers.MSG_REVIEW_TEXT_LENGTH
    shown = helpers.wait_for_text(driver, expected)
    helpers.shot(driver, f"TC05_S3{case}")
    assert shown, f"{length} characters: expected message {expected!r}"
