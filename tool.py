import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from faker import Faker

# Initialize Faker to generate random data
fake = Faker()

def fill_registration_form():
    # 1. Ask for the link
    url = input("Please enter the website link: ")

    # Setup the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Open the website
        driver.get(url)
        
        # Wait for the page to load (you might need a more robust wait strategy)
        time.sleep(3)

        # 2. Generate random data
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        password = fake.password(length=12)

        print(f"Filling form with: {first_name}, {last_name}, {email}")

        # Locate form fields (Note: IDs/Names will vary by website)
        # These are common placeholder selectors; you must inspect the 
        # specific website to find the correct IDs, Names, or XPaths.
        driver.find_element(By.NAME, "firstname").send_keys(first_name)
        driver.find_element(By.NAME, "lastname").send_keys(last_name)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)

        # 3. Press the "Create Account" button
        # Again, the selector depends on the website's HTML structure.
        submit_button = driver.find_element(By.XPATH, "//button[contains(text(), 'Create Account')]")
        submit_button.click()

        print("Form submitted successfully.")
        
        # Keep the browser open for a few seconds to see the result
        time.sleep(5)

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    fill_registration_form()
