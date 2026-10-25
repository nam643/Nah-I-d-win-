from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# SCENARIO 2: Invalid/No matches found for search

driver = webdriver.Edge()

# Go to main page (search bar is on top)
driver.get("https://opencart.abstracta.us/index.php?route=common/home")

# Type in the search bar random keys and pressing search
search_bar = driver.find_element(By.NAME, "search")
search_bar.send_keys("soidjfosnvlkhvilafiadnhimladmlinhvciahmcfiosnyfiushefishdfv,kfhdfkvnmskiu" + Keys.ENTER)

products = driver.find_elements(By.CSS_SELECTOR, ".product-layout")
assert len(products) == 0, f"Test Failed: Expected 0 products, but found {len(products)}."

print("Test Passed: Invalid search correctly returned zero products.")
time.sleep(5)
driver.quit()
