"""
Shared helpers for the Assignment 3 system tests.

Website under test: LambdaTest E-commerce Playground (OpenCart + Poco theme)
https://ecommerce-playground.lambdatest.io/

Every test file imports from here so that locators, waits and screenshots are
written once and behave the same for every team member.

[VERIFY] Locators were written from the standard OpenCart / Poco markup. Before
your first run, open each page in Chrome DevTools (F12 -> Elements, Ctrl+F) and
confirm the selector in the LOCATORS section still matches. If one does not,
change it HERE only; every test picks up the fix.
"""

import os
import re
import time
import uuid
from decimal import Decimal
from urllib.parse import urlencode

from selenium.common.exceptions import (
    ElementClickInterceptedException,
    ElementNotInteractableException,
    TimeoutException,
)
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# --------------------------------------------------------------------------
# Configuration
# --------------------------------------------------------------------------
BASE = "https://ecommerce-playground.lambdatest.io/index.php"
DEFAULT_PASSWORD = "Test@1234"   # valid password used for every new account
TIMEOUT = 15                     # seconds for explicit waits (live site can be slow)

# Screenshots are written to <project>/evidence/<name>.png
EVIDENCE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "evidence")

# --------------------------------------------------------------------------
# LOCATORS  [VERIFY each in DevTools before the first run]
# --------------------------------------------------------------------------
# Login page (route=account/login)
LOGIN_EMAIL = (By.ID, "input-email")
LOGIN_PASSWORD = (By.ID, "input-password")
LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")

# Register page (route=account/register)
REG_FIRSTNAME = (By.ID, "input-firstname")
REG_LASTNAME = (By.ID, "input-lastname")
REG_EMAIL = (By.ID, "input-email")
REG_TELEPHONE = (By.ID, "input-telephone")
REG_PASSWORD = (By.ID, "input-password")
REG_CONFIRM = (By.ID, "input-confirm")
REG_AGREE_LABEL = (By.CSS_SELECTOR, "label[for='input-agree']")  # custom checkbox: click its label
REG_AGREE_INPUT = (By.ID, "input-agree")
REG_CONTINUE = (By.CSS_SELECTOR, "input[value='Continue']")

# Header search (the theme renders desktop + mobile copies; we use the visible one)
SEARCH_INPUT = (By.CSS_SELECTOR, "input[name='search']")
RESULT_NAMES = (By.CSS_SELECTOR, ".product-thumb h4 a, .product-layout h4 a")

# Product page (route=product/product&product_id=...)
QUANTITY_INPUT = (By.CSS_SELECTOR, "input[name='quantity']")
ADD_TO_CART_BUTTON = (By.XPATH, "//button[contains(@class,'button-cart') or @id='button-cart']")
COMPARE_BUTTON = (
    By.XPATH,
    "//button[contains(@title,'Compare this Product') or normalize-space(.)='Compare this Product']",
)
REVIEW_TAB = (By.XPATH, "//a[contains(@href,'#tab-review') or contains(normalize-space(.),'Write a review')]")
REVIEW_NAME = (By.ID, "input-name")
REVIEW_TEXT = (By.ID, "input-review")
REVIEW_SUBMIT = (By.ID, "button-review")

# Comparison page (route=product/compare): one "Remove" link per product column
COMPARE_REMOVE_LINKS = (By.XPATH, "//a[contains(@href,'product/compare') and contains(@href,'remove=')]")

# Cart page (route=checkout/cart)
CART_ROWS = (By.XPATH, "//div[@id='content']//form//table/tbody/tr[.//input[starts-with(@name,'quantity')]]")

# --------------------------------------------------------------------------
# Messages the site normally shows  [VERIFY wording on the live site]
# --------------------------------------------------------------------------
MSG_LOGIN_NO_MATCH = "No match for E-Mail Address and/or Password"
MSG_ALREADY_REGISTERED = "E-Mail Address is already registered"
MSG_PRIVACY = "You must agree to the Privacy Policy"
MSG_CONFIRM_MISMATCH = "Password confirmation does not match password"
MSG_FIRSTNAME_LENGTH = "First Name must be between 1 and 32 characters"
MSG_PASSWORD_LENGTH = "Password must be between 4 and 20 characters"
MSG_ACCOUNT_CREATED = "Your Account Has Been Created"
MSG_COMPARE_ADDED = "to your product comparison"
MSG_COMPARE_MODIFIED = "You have modified your product comparison"
MSG_COMPARE_EMPTY = "You have not chosen any products to compare"
MSG_CART_ADDED = "to your shopping cart"
MSG_CART_EMPTY = "Your shopping cart is empty"
MSG_CART_STOCK = "not available in the desired quantity or not in stock"
MSG_REVIEW_THANKS = "Thank you for your review"
MSG_REVIEW_RATING = "Please select a review rating"
MSG_REVIEW_NAME_LENGTH = "Review Name must be between 3 and 25 characters"
MSG_REVIEW_TEXT_LENGTH = "Review Text must be between 25 and 1000 characters"
MSG_REVIEW_LOGIN = "Please login or register to review"
MSG_SEARCH_NO_MATCH = "There is no product that matches the search criteria"


# --------------------------------------------------------------------------
# Generic helpers
# --------------------------------------------------------------------------
def url(route, **params):
    """Build a full site URL, e.g. url('account/login')."""
    query = {"route": route, **params}
    return f"{BASE}?{urlencode(query)}"


def unique_email():
    """A fresh e-mail for every registration, so parallel testers never collide."""
    return f"a3tester.{int(time.time() * 1000)}{uuid.uuid4().hex[:4]}@example.com"


def shot(driver, name):
    """Save evidence/<name>.png and return its path (used in the Test Results tables)."""
    os.makedirs(EVIDENCE_DIR, exist_ok=True)
    path = os.path.join(EVIDENCE_DIR, f"{name}.png")
    driver.save_screenshot(path)
    return path


def visible(driver, locator, timeout=TIMEOUT):
    """Wait until at least one element matching the locator is displayed; return the first such element."""
    def first_displayed(drv):
        for element in drv.find_elements(*locator):
            if element.is_displayed():
                return element
        return False
    return WebDriverWait(driver, timeout).until(first_displayed)


def click(driver, element):
    """Click like a user; if a sticky header or overlay covers the element, fall back to a JavaScript click."""
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
    try:
        element.click()
    except (ElementClickInterceptedException, ElementNotInteractableException):
        driver.execute_script("arguments[0].click();", element)


def type_into(element, text):
    """Clear a field and type the given text into it."""
    element.clear()
    element.send_keys(text)


def body_text(driver):
    """All visible text on the page (used to look for alerts and messages)."""
    return driver.find_element(By.TAG_NAME, "body").text


def wait_for_text(driver, text, timeout=TIMEOUT):
    """Wait until the given text is visible anywhere on the page; return True, or False on timeout."""
    try:
        WebDriverWait(driver, timeout).until(lambda d: text in body_text(d))
        return True
    except TimeoutException:
        return False


def wait_for_any_text(driver, texts, timeout=5):
    """Wait for whichever of several messages appears first; return it, or None if none appears."""
    try:
        return WebDriverWait(driver, timeout).until(
            lambda d: next((t for t in texts if t in body_text(d)), False)
        )
    except TimeoutException:
        return None


def money(text):
    """Turn '$1,194.00' into Decimal('1194.00') so totals are compared exactly, not as floats."""
    match = re.search(r"[\d,]+\.\d{2}", text)
    assert match, f"No price found in {text!r}"
    return Decimal(match.group(0).replace(",", ""))


def make_text(length):
    """Realistic review/enquiry text of an exact length (used for boundary values)."""
    phrase = "Good sound and solid build quality. "
    text = (phrase * (length // len(phrase) + 1))[:length]
    if text.endswith(" "):          # never end on a space, in case the site trims input
        text = text[:-1] + "."
    assert len(text) == length
    return text


# --------------------------------------------------------------------------
# Function-level actions (one per function under test)
# --------------------------------------------------------------------------
def register(driver, email, password=DEFAULT_PASSWORD, confirm=None, firstname="Nam",
             lastname="Tester", telephone="0412345678", agree=True):
    """F2: fill and submit the registration form. Does not assert; tests decide what to expect."""
    driver.get(url("account/register"))
    type_into(visible(driver, REG_FIRSTNAME), firstname)
    type_into(visible(driver, REG_LASTNAME), lastname)
    type_into(visible(driver, REG_EMAIL), email)
    type_into(visible(driver, REG_TELEPHONE), telephone)
    type_into(visible(driver, REG_PASSWORD), password)
    type_into(visible(driver, REG_CONFIRM), password if confirm is None else confirm)
    if agree:
        click(driver, visible(driver, REG_AGREE_LABEL))
        checkbox = driver.find_element(*REG_AGREE_INPUT)
        if not checkbox.is_selected():           # the label click did not tick it: tick the input itself
            driver.execute_script("arguments[0].click();", checkbox)
    click(driver, visible(driver, REG_CONTINUE))


def login(driver, email, password):
    """F1: fill and submit the login form."""
    driver.get(url("account/login"))
    type_into(visible(driver, LOGIN_EMAIL), email)
    type_into(visible(driver, LOGIN_PASSWORD), password)
    click(driver, visible(driver, LOGIN_BUTTON))


def logout(driver):
    """End the session so the next step starts logged out."""
    driver.get(url("account/logout"))


def search(driver, keyword):
    """F6: type a keyword into the visible header search box and press Enter."""
    driver.get(url("common/home"))
    box = visible(driver, SEARCH_INPUT)
    click(driver, box)
    type_into(box, keyword)
    box.send_keys(Keys.ENTER)
    WebDriverWait(driver, TIMEOUT).until(EC.url_contains("route=product/search"))


def result_names(driver):
    """Names of the products listed on the current search results page."""
    return [e.text.strip() for e in driver.find_elements(*RESULT_NAMES) if e.text.strip()]


def open_product(driver, product_id):
    """Open a product page directly by its ID."""
    driver.get(url("product/product", product_id=product_id))
    WebDriverWait(driver, TIMEOUT).until(EC.presence_of_element_located((By.TAG_NAME, "h1")))


def open_from_results(driver, product_id):
    """From a results page, click the link to the given product (falls back to the direct URL)."""
    links = [a for a in driver.find_elements(By.CSS_SELECTOR, f"a[href*='product_id={product_id}']")
             if a.is_displayed()]
    if links:
        click(driver, links[0])
        WebDriverWait(driver, TIMEOUT).until(EC.url_contains(f"product_id={product_id}"))
    else:
        open_product(driver, product_id)


def add_to_compare(driver, product_id):
    """F3: open a product page and click 'Compare this Product'; return True if the success alert appeared."""
    open_product(driver, product_id)
    click(driver, visible(driver, COMPARE_BUTTON))
    return wait_for_text(driver, MSG_COMPARE_ADDED)


def compare_removes(driver):
    """Remove links on the comparison page, one per product column."""
    return driver.find_elements(*COMPARE_REMOVE_LINKS)


def add_to_cart(driver, quantity):
    """F4: on an open product page, set the quantity and click Add to Cart."""
    type_into(visible(driver, QUANTITY_INPUT), str(quantity))
    click(driver, visible(driver, ADD_TO_CART_BUTTON))


def cart_lines(driver):
    """Open the cart page; return one dict per line: name, quantity, unit price and line total."""
    driver.get(url("checkout/cart"))
    wait_for_any_text(driver, ["Shopping Cart", MSG_CART_EMPTY], timeout=TIMEOUT)
    lines = []
    for row in driver.find_elements(*CART_ROWS):
        cells = row.find_elements(By.TAG_NAME, "td")
        qty = row.find_element(By.XPATH, ".//input[starts-with(@name,'quantity')]").get_attribute("value")
        lines.append({
            "name": cells[1].text.strip(),
            "quantity": int(qty),
            "unit": money(cells[-2].text),     # second-last column = unit price
            "total": money(cells[-1].text),    # last column = line total
        })
    return lines
