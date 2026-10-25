from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# SCENARIO 3: Submitting a review with an invalid email (email not registered yet)

driver = webdriver.Edge()

# Go to login page
driver.get("https://opencart.abstracta.us/index.php?route=account/login")

# Type in an email that has not been registered
email_input = driver.find_element(By.ID, "input-email")
email_input.send_keys("notavalidemail@gmail.com")

# Type in wrong password (not that it matters)
password_input = driver.find_element(By.ID, "input-password")
password_input.send_keys("incorrectpassword")

# Click the login button
login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
login_button.click()

warning_alert = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'alert-danger')]"))
)

expected_error = "Warning: No match for E-Mail Address and/or Password."
assert expected_error in warning_alert.text, f"Test Failed: Expected '{expected_error}', got '{warning_alert.text}'"

print("Test Passed: System handled empty login form correctly.")
time.sleep(5)
driver.quit()
