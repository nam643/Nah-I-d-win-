from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# SCENARIO 3: Submitting a review with an invalid email (email not registered yet)

driver = webdriver.Edge()

# Go to login page
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")

# Type in an email that has not been registered
email_input = driver.find_element(By.ID, "input-email")
email_input.send_keys("notavalidemail@gmail.com")

# Type in wrong password (not that it matters)
password_input = driver.find_element(By.ID, "input-password")
password_input.send_keys("incorrectpassword")

# Click the login button
login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
login_button.click()

time.sleep(5)
driver.quit()
