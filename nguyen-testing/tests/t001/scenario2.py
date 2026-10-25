from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# SCENARIO 2: Logging in without putting in credentials

driver = webdriver.Edge()

# Go to login page
driver.get("https://opencart.abstracta.us/index.php?route=account/login")

# Click login button without typing anything in the email and password input
login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
login_button.click()

warning_alert = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger')]"))
)

expected_error = "Warning: No match for E-Mail Address and/or Password."
assert expected_error in warning_alert.text, f"Test Failed: Expected '{expected_error}', got '{warning_alert.text}'"

print("Test Passed: System correctly rejected invalid credentials.")
time.sleep(5)
driver.quit()
