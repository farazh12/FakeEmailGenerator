import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker

# Initialize Faker
fake = Faker()

# --- CONFIGURATION: REPLACE THESE WITH YOUR WEBSITE'S ACTUAL IDs OR NAMES ---
selectors = {
    "first_name_field": "firstname",  # Change to your site's ID or Name
    "last_name_field": "lastname",    # Change to your site's ID or Name
    "email_field": "email",          # Change to your site's ID or Name
    "password_field": "password",    # Change to your site's ID or Name
    "submit_button": "//button[@type='submit']" # This is an XPath
}

def fill_form():
    url = input("Enter the website link: ")
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    wait = WebDriverWait(driver, 10) # Wait up to 10 seconds

    try:
        driver.get(url)

        # Generate data
        f_name = fake.first_name()
        l_name = fake.last_name()
        email = fake.email()
        pwd = fake.password(length=12)

        # Wait for fields to be visible, then type
        # NOTE: If your site uses IDs, change 'By.NAME' to 'By.ID'
        wait.until(EC.presence_of_element_located((By.NAME, selectors["first_name_field"]))).send_keys(f_name)
        wait.until(EC.presence_of_element_located((By.NAME, selectors["last_name_field"]))).send_keys(l_name)
        wait.until(EC.presence_of_element_located((By.NAME, selectors["email_field"]))).send_keys(email)
        wait.until(EC.presence_of_element_located((By.NAME, selectors["password_field"]))).send_keys(pwd)

        # Click the button (Using XPath for the button)
        submit = wait.until(EC.element_to_be_clickable((By.XPATH, selectors["submit_button"])))
        submit.click()

        print(f"Successfully attempted signup for: {email}")
        time.sleep(10) # Stay open to see results

    except Exception as e:
        print(f"Error: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    fill_form()
