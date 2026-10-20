from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# SCENARIO 3: Submiting a review but the review content is not of appropriate length

driver = webdriver.Edge()

# Go to a product page
driver.get("https://ecommerce-playground.lambdatest.io/index.php?route=product/product&path=20&product_id=28")

# Choosing rating 
star_xpath = "//input[@name='rating' and @value='5']/following-sibling::label[1]"
five_star_label = WebDriverWait(driver, 10).until(
    EC.element_to_be_clickable((By.XPATH, star_xpath))
)
five_star_label.click()

# Inputing a name
name_textbox = driver.find_element(By.ID, "input-name")
name_textbox.send_keys("Ethan")

# Inputing a review that has an unappropriate length (under 25 characters in this case)
review_textbox = driver.find_element(By.ID, "input-review")
review_textbox.send_keys("Under 25 chars")

# Click submit review button
submit_button = driver.find_element(By.ID, "button-review")
submit_button.click()

time.sleep(5)
driver.quit()
