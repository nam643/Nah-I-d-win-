from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# SCENARIO 2: Logging in without putting in credentials

driver = webdriver.Edge()

# Go to login page
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=account/login")

# Click login button without typing anything in the email and password input
login_button = driver.find_element(By.XPATH, "//input[@value='Login']")
login_button.click()

time.sleep(5)
driver.quit()
