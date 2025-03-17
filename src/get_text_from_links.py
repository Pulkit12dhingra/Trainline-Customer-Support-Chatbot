"""
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_page_text_selenium(url):
    # Setup Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode for efficiency

    # Initialize WebDriver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)  # Open the URL
        driver.implicitly_wait(10)  # Wait for elements to load

        # Extract all text content
        page_text = driver.find_element(By.TAG_NAME, "body").text

        return page_text
    finally:
        driver.quit()  # Close the browser session

# Example usage
#url = "https://support.thetrainline.com/en/support/solutions/folders/78000000023"  # Replace with your target URL
url = "https://support.thetrainline.com/en/support/solutions/articles/78000000553-refunding-a-uk-train-ticket"
text = get_page_text_selenium(url)
print(text)
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_expanded_text(url):
    # Setup Chrome options (Visible browser)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment if you want to run in headless mode

    # Initialize WebDriver
    service = Service()
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)  # Open the URL
        driver.implicitly_wait(10)  # Wait for elements to load

        # Find all expandable sections (assumed "+" buttons are clickable elements)
        expand_buttons = driver.find_elements(By.CLASS_NAME, "account-item")  # Update with actual class name

        for button in expand_buttons:
            try:
                button.click()  # Click the button to expand
                WebDriverWait(driver, 5).until(EC.staleness_of(button))  # Wait to ensure content is loaded
            except Exception as e:
                print(f"Could not click button: {e}")

        # Extract text content after expanding all sections
        page_text = driver.find_element(By.TAG_NAME, "body").text

        return page_text
    finally:
        input("Press Enter to close the browser...")  # Keep browser open for debugging
        driver.quit()  # Close the browser session

# Example usage
url = "https://support.thetrainline.com/en/support/solutions/articles/78000000553-refunding-a-uk-train-ticket"  # Replace with actual URL
text = get_expanded_text(url)
print(text)
