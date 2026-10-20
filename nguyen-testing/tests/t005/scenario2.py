from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# SCENARIO 2: Submitting an empty review (None of the fields are filled)

driver = webdriver.Edge()

# Go to a product page
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=product/product&path=20&product_id=28")

# Click submit review button without inputing anything in the fields
submit_button = driver.find_element(By.ID, "button-review")
submit_button.click()

time.sleep(5)
driver.quit()
