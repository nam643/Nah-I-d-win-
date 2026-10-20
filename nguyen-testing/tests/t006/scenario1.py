from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# SCENARIO 1: Searching for a product

driver = webdriver.Edge()

# Go to main page (search bar is on top)
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")

# Typing in the name of a product and search for it
search_bar = driver.find_element(By.NAME, "search")
search_bar.send_keys("imac" + Keys.ENTER)

time.sleep(5)
driver.quit()
