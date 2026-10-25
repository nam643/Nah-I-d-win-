from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# SCENARIO 1: Searching for a product

driver = webdriver.Edge()

# Go to main page (search bar is on top)
driver.get("https://opencart.abstracta.us/index.php?route=common/home")

# Typing in the name of a product and search for it
search_bar = driver.find_element(By.NAME, "search")
search_bar.send_keys("imac" + Keys.ENTER)

products = driver.find_elements(By.CSS_SELECTOR, ".product-layout")
assert len(products) > 0, "Test Failed: Expected to find at least one product for 'imac', but found none."

print("Test Passed: Valid search successfully returned product results.")
time.sleep(5)
driver.quit()
