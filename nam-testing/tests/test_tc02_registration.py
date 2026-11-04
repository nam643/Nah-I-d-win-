"""
T002 - F2 User Registration
Techniques: input partitioning (S2) and boundary value analysis on First Name 1-32 and Password 4-20 (S3).
Evidence: evidence/TC02_*.png
"""

import pytest

import helpers

# S1 (Registration): all fields valid -> 'Your Account Has Been Created!'.
def test_tc02_s1_valid_registration(driver):
    helpers.register(driver, helpers.unique_email())
    try:
        helpers.wait_route(driver, "account/success")
    finally:
        helpers.shot(driver, "TC02_S1")
    assert helpers.MSG_ACCOUNT_CREATED in helpers.body_text(driver)


# S2 (validation): each invalid input set must be rejected with its own message.
@pytest.mark.parametrize(
    "case, overrides, expected",
    [
        ("a", {"duplicate": True}, helpers.MSG_ALREADY_REGISTERED),     # e-mail already registered
        ("b", {"agree": False}, helpers.MSG_PRIVACY),                   # Privacy Policy not ticked
        ("c", {"confirm": "Test@9999"}, helpers.MSG_CONFIRM_MISMATCH),  # Confirmation and password do not match
    ],
    ids=["S2a-duplicate-email", "S2b-policy-not-ticked", "S2c-confirm-mismatch"],
)
def test_tc02_s2_invalid_submissions(driver, account, case, overrides, expected):
    email = account.email if overrides.get("duplicate") else helpers.unique_email()
    helpers.register(
        driver,
        email,
        agree=overrides.get("agree", True),
        confirm=overrides.get("confirm"),
    )
    shown = helpers.wait_for_text(driver, expected)
    helpers.shot(driver, f"TC02_S2{case}")
    assert shown, f"Expected message: {expected}"
    assert not helpers.on_route(driver, "account/success")          # no account created


# S3 (edge): just outside the limits -> rejected; exactly on the limits -> accepted.
@pytest.mark.parametrize(
    "case, firstname, password, expected",
    [
        ("a", "A" * 33, "Test@1234", helpers.MSG_FIRSTNAME_LENGTH),  # 33 > 32
        ("b", "Nam", "Ab1", helpers.MSG_PASSWORD_LENGTH),            # 3 < 4
        ("c", "A" * 32, "Ab1!", None),                               # 32 and 4: valid boundaries
    ],
    ids=["S3a-firstname-33", "S3b-password-3", "S3c-firstname-32-password-4"],
)
def test_tc02_s3_length_boundaries(driver, case, firstname, password, expected):
    helpers.register(driver, helpers.unique_email(), password=password, firstname=firstname)
    if expected is None:
        try:
            helpers.wait_route(driver, "account/success")
        finally:
            helpers.shot(driver, f"TC02_S3{case}")
        assert helpers.MSG_ACCOUNT_CREATED in helpers.body_text(driver)
    else:
        shown = helpers.wait_for_text(driver, expected)
        helpers.shot(driver, f"TC02_S3{case}")
        assert shown, f"Expected message: {expected}"
        assert not helpers.on_route(driver, "account/success")
