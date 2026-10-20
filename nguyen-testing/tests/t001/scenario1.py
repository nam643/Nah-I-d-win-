from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# SCENARIO 1: Logging in with a valid registered account

driver = webdriver.Edge()

# Go to login page
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")

# Type in a registered email
email_input = driver.find_element(By.ID, "input-email")
email_input.send_keys("validemail@gmail.com")

# Type in the correct password
password_input = driver.find_element(By.ID, "input-password")
password_input.send_keys("correctpassword")

# Click login button
login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
login_button.click()

time.sleep(5)
driver.quit()

