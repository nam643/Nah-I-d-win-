"""
pytest fixtures shared by every test file.

- driver:  a fresh Chrome window per test (so cookies, cart and comparison list start empty)
- account: one account registered through F2 at the start of the run, reused by F1 (and F5 if
           the review form requires login). This is how the F1 -> F2 dependency is honoured.
- On any failure, a screenshot evidence/FAILED_<test name>.png is saved automatically.
"""

import os
import re
import sys
from types import SimpleNamespace

import pytest
from selenium import webdriver

import helpers

# Keep the browser inside the virtual environment: when no Chrome is installed on the system,
# Selenium Manager downloads "Chrome for Testing" and a matching ChromeDriver into
# .venv/selenium-cache/ (outside a venv: ./selenium-cache/). Deleting .venv removes both.
_IN_VENV = sys.prefix != sys.base_prefix
os.environ.setdefault(
    "SE_CACHE_PATH",
    os.path.join(sys.prefix if _IN_VENV else os.path.dirname(os.path.abspath(__file__)), "selenium-cache"),
)


def make_driver():
    """Start Chrome (the copy kept in .venv/selenium-cache, downloaded on first use).
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
    """Register one account via F2 (used by T002 Scenario 2a, the duplicate-email input)."""
    drv = make_driver()
    try:
        email = helpers.unique_email()
        helpers.register(drv, email)
        helpers.wait_route(drv, "account/success")
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
