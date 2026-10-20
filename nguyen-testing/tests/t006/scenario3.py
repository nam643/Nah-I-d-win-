from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# SCENARIO 3: Searching without typing anything in the search bar

driver = webdriver.Edge()

# Go to main page (search bar is on top)
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")

# Immediately search without any input in search bar
search_bar = driver.find_element(By.NAME, "search")
search_bar.send_keys(Keys.ENTER)

time.sleep(5)
driver.quit()
