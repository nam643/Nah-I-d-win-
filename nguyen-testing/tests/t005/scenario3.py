from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# SCENARIO 3: Submiting a review but the review content is not of appropriate length

driver = webdriver.Edge()

# Go to a product page
driver.get("https://opencart.abstracta.us/index.php?route=product/product&product_id=43")

# Open review form
review_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#tab-review')]"))
)
review_tab.click()

# Choosing rating 
rating_label = driver.find_element(By.XPATH, "//input[@name='rating' and @value='5']")
rating_label.click()

# Inputing a name
name_textbox = driver.find_element(By.ID, "input-name")
name_textbox.send_keys("Ethan")

# Inputing a review that has an unappropriate length (under 25 characters in this case)
review_textbox = driver.find_element(By.ID, "input-review")
review_textbox.send_keys("Under 25 chars")

# Click submit review button
submit_button = driver.find_element(By.ID, "button-review")
submit_button.click()

warning_alert = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger')]"))
)
assert "Warning: Review Text must be between 25 and 1000 characters!" in warning_alert.text, "Test Failed: Warning message not displayed for empty form."

print("Test Passed: Review Text error displayed correctly.")\

time.sleep(5)
driver.quit()
