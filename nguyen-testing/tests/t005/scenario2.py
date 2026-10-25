from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# SCENARIO 2: Submitting an empty review (None of the fields are filled)

driver = webdriver.Edge()

# Go to a product page
driver.get("https://opencart.abstracta.us/index.php?route=product/product&product_id=43")

# Open review form
review_tab = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//a[contains(@href, '#tab-review')]"))
)
review_tab.click()

# Click submit review button without inputing anything in the fields
submit_button = driver.find_element(By.ID, "button-review")
submit_button.click()

warning_alert = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger')]"))
)
assert "Warning: Please select a review rating!" in warning_alert.text, "Test Failed: Warning message not displayed for empty form."

print("Test Passed: Empty review error displayed.")

time.sleep(5)
driver.quit()
