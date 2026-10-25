from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# SCENARIO 1: Submiting a valid review

driver = webdriver.Edge()

# Go to a product page
driver.get("https://opencart.abstracta.us/index.php?route=product/product&product_id=43")

# Open review form
review_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#tab-review')]"))
)
review_tab.click()

# Selecting a rating (5/5 in this case)
rating_label = driver.find_element(By.XPATH, "//input[@name='rating' and @value='5']")
rating_label.click()

# Typing in a name
name_textbox = driver.find_element(By.ID, "input-name")
name_textbox.send_keys("Nathan")

# Typing a review that has appropriate length
review_textbox = driver.find_element(By.ID, "input-review")
review_textbox.send_keys("I can tell you're acting your heart out")

# Click the submit review button
submit_button = driver.find_element(By.ID, "button-review")
submit_button.click()

success_alert = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'alert-success')]"))
)
assert "Thank you for your review" in success_alert.text, "Test Failed: Success message not found."

print("Test Passed: Valid review submitted.")

time.sleep(5)
driver.quit()

