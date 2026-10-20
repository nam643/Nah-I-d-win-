from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# SCENARIO 1: Submiting a valid review

driver = webdriver.Edge()

# Go to a product page
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=product/product&path=20&product_id=28")

# Selecting a rating (5 stars in this case)
star_xpath = "//input[@name='rating' and @value='5']/following-sibling::label[1]"
five_star_label = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, star_xpath))
)
five_star_label.click()

# Typing in a name
name_textbox = driver.find_element(By.ID, "input-name")
name_textbox.send_keys("Nathan")

# Typing a review that has appropriate length
review_textbox = driver.find_element(By.ID, "input-review")
review_textbox.send_keys("I can tell you're acting your heart out")

# Click the submit review button
submit_button = driver.find_element(By.ID, "button-review")
submit_button.click()

time.sleep(5)
driver.quit()

