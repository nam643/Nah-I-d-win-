from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# SCENARIO 2: Invalid/No matches found for search

driver = webdriver.Edge()

# Go to main page (search bar is on top)
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=common/home")

# Type in the search bar random keys and pressing search
search_bar = driver.find_element(By.NAME, "search")
search_bar.send_keys("soidjfosnvlkhvilafiadnhimladmlinhvciahmcfiosnyfiushefishdfv,kfhdfkvnmskiu" + Keys.ENTER)

time.sleep(5)
driver.quit()
