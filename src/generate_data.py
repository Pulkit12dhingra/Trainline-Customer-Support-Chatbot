import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from tqdm import tqdm  # Import tqdm for progress bar

# Setup WebDriver options
options = Options()
# Uncomment for headless mode
# options.add_argument("--headless")

# Initialize WebDriver
service = Service()
driver = webdriver.Chrome(service=service, options=options)

# File paths
input_file = "data/urls.txt"
output_file = "data/content.txt"

# Ensure data directory exists
os.makedirs("data", exist_ok=True)


# Read URLs from list.txt
try:
    with open(input_file, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"⚠️ File {input_file} not found! Please create it and add URLs.")
    driver.quit()
    exit()


# Open output file in write mode to clear previous content
with open(output_file, "w", encoding="utf-8") as file:
    file.write("Extracted Content from Trainline Support Pages\n")
    file.write("=" * 80 + "\n\n")



try:
    for url in tqdm(urls, desc="Processing URLs", unit="page"):  # Progress bar with tqdm
        # Open the webpage
        driver.get(url)

        # Allow the page to load
        time.sleep(3)

        # Step 1: Click "Accept All Cookies" before anything else
        try:
            cookie_button = driver.find_element(By.ID, "onetrust-accept-btn-handler")  # OneTrust "Accept All" button
            cookie_button.click()
            time.sleep(2)  # Wait for cookies to be accepted
        except NoSuchElementException:
            pass  # Ignore if cookie button is not found

        # Step 2: Remove any remaining cookie banners
        script_remove_cookie_banner = """
        let cookieBanner = document.getElementById("onetrust-banner-sdk");
        if (cookieBanner) {
            cookieBanner.remove();
        }
        """
        driver.execute_script(script_remove_cookie_banner)

        # Step 3: Open all dropdowns
        script_open_dropdowns = """
        document.querySelectorAll('.accound-content').forEach(el => {
            el.style.display = 'block';  // Keep open
            el.style.overflow = 'visible';
        });

        document.querySelectorAll('.account-heading').forEach(el => {
            el.setAttribute('aria-expanded', 'true');  // Mark as expanded
        });
        """
        driver.execute_script(script_open_dropdowns)

        # Wait before extracting content
        time.sleep(5)

        # Step 4: Extract text from the specific div with class="tab-content-layer current"
        try:
            content_element = driver.find_element(By.CLASS_NAME, "tab-content-layer.current")
            content_text = content_element.text
        except NoSuchElementException:
            content_text = "⚠️ No content found in 'tab-content-layer current'."

        # Step 5: Append extracted text to the file
        with open(output_file, "a", encoding="utf-8") as file:
            file.write(f"URL: {url}\n")
            file.write("Extracted Content:\n")
            file.write(content_text + "\n")
            file.write("=" * 80 + "\n\n")

        # Short wait before processing the next URL
        time.sleep(3)

finally:
    # Close the browser
    driver.quit()
