"""
TC01 - F1 User Login
Tester: [FILL]
Precondition: the `account` fixture registers a fresh account through F2 (F1 depends on F2).
Evidence: evidence/TC01_*.png
"""

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import helpers


def test_tc01_s1_valid_login(driver, account):
    """S1 (success): registered e-mail + correct password -> My Account page."""
    helpers.login(driver, account.email, account.password)
    WebDriverWait(driver, helpers.TIMEOUT).until(EC.url_contains("route=account/account"))
    helpers.shot(driver, "TC01_S1")                                   # evidence before asserting
    assert "My Account" in helpers.body_text(driver)
    # A Logout link only exists for a logged-in session
    assert driver.find_elements(By.XPATH, "//a[contains(@href,'route=account/logout')]")


# S2 (validation): three invalid credential classes, each must show the same warning.
# Only (a) counts as a failed attempt on the registered account (lockout is 5 attempts).
@pytest.mark.parametrize(
    "case, email_kind, password",
    [
        ("a", "registered", "WrongPass99!"),      # right e-mail, wrong password
        ("b", "unregistered", "Test@1234"),       # e-mail that has never been registered
        ("c", "blank", ""),                       # both fields left empty
    ],
)
def test_tc01_s2_invalid_credentials(driver, account, case, email_kind, password):
    email = {"registered": account.email, "unregistered": "nobody.a3.9z@example.com", "blank": ""}[email_kind]
    helpers.login(driver, email, password)
    shown = helpers.wait_for_text(driver, helpers.MSG_LOGIN_NO_MATCH)
    helpers.shot(driver, f"TC01_S2{case}")
    assert shown, "Expected the 'No match for E-Mail Address and/or Password' warning"
    assert "route=account/login" in driver.current_url               # still on the login page


def test_tc01_s3a_email_case_ignored(driver, account):
    """S3a (edge): e-mail typed in UPPER CASE should still log in (e-mail is case-insensitive)."""
    helpers.login(driver, account.email.upper(), account.password)
    try:
        WebDriverWait(driver, helpers.TIMEOUT).until(EC.url_contains("route=account/account"))
    finally:
        helpers.shot(driver, "TC01_S3a")
    assert "My Account" in helpers.body_text(driver)
    helpers.logout(driver)


def test_tc01_s3b_password_case_enforced(driver, account):
    """S3b (edge): password with changed letter case must be rejected (passwords are case-sensitive)."""
    helpers.login(driver, account.email, account.password.upper())   # 'Test@1234' -> 'TEST@1234'
    shown = helpers.wait_for_text(driver, helpers.MSG_LOGIN_NO_MATCH)
    helpers.shot(driver, "TC01_S3b")
    assert shown
    assert "route=account/login" in driver.current_url
