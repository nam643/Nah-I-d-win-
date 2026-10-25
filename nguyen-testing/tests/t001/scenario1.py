from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# SCENARIO 1: Logging in with a valid registered account

driver = webdriver.Edge()

# Go to login page
driver.get("https://opencart.abstracta.us/index.php?route=account/login")

# Type in a registered email
email_input = driver.find_element(By.ID, "input-email")
email_input.send_keys("validemail@gmail.com")

# Type in the correct password
password_input = driver.find_element(By.ID, "input-password")
password_input.send_keys("correctpassword")

# Click login button
login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
login_button.click()

account_header_xpath = "//h2[text()='My Account']"
account_header = WebDriverWait(driver, 5).until(
    EC.visibility_of_element_located((By.XPATH, account_header_xpath))
)

assert account_header.is_displayed(), "Test Failed: User was not redirected to the My Account dashboard."

print("Test Passed: Successfully logged in.")

time.sleep(5)
driver.quit()

