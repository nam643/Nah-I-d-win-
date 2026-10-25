from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# SCENARIO 3: Searching without typing anything in the search bar

driver = webdriver.Edge()

# Go to main page (search bar is on top)
driver.get("https://opencart.abstracta.us/index.php?route=common/home")

# Immediately search without any input in search bar
search_bar = driver.find_element(By.NAME, "search")
search_bar.send_keys(Keys.ENTER)

products = driver.find_elements(By.CSS_SELECTOR, ".product-layout")
assert len(products) == 0, f"Test Failed: Expected no products to be displayed for an empty search, but found {len(products)}."

print("Test Passed: Empty search returned nothing.")

time.sleep(5)
driver.quit()
