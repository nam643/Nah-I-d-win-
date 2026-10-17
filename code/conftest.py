"""
pytest fixtures shared by every test file.

- driver:  a fresh Chrome window per test (so cookies, cart and comparison list start empty)
- account: one account registered through F2 at the start of the run, reused by F1 (and F5 if
           the review form requires login). This is how the F1 -> F2 dependency is honoured.
- On any failure, a screenshot evidence/FAILED_<test name>.png is saved automatically.
"""

import os
import re
from types import SimpleNamespace

import pytest
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import helpers


def make_driver():
    """Start Chrome. Selenium Manager downloads a matching ChromeDriver automatically.
    Set HEADLESS=1 to run without a visible window (screenshots still work)."""
    options = webdriver.ChromeOptions()
    options.add_argument("--window-size=1366,900")      # desktop layout, so desktop locators are visible
    if os.getenv("HEADLESS") == "1":
        options.add_argument("--headless=new")
    return webdriver.Chrome(options=options)


@pytest.fixture
def driver():
    drv = make_driver()
    yield drv              # the test runs here
    drv.quit()             # teardown: always close the browser


@pytest.fixture(scope="session")
def account():
    """Register one account via F2 (precondition for TC01, optionally TC05)."""
    drv = make_driver()
    try:
        email = helpers.unique_email()
        helpers.register(drv, email)
        WebDriverWait(drv, helpers.TIMEOUT).until(EC.url_contains("route=account/success"))
    finally:
        drv.quit()
    return SimpleNamespace(email=email, password=helpers.DEFAULT_PASSWORD)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """After each test step: if the test body failed, screenshot the browser for the defect log."""
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", item.name)
            helpers.shot(drv, f"FAILED_{safe}")
