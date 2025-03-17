from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

def get_all_links(url):
    # Setup Chrome options (Visible browser)
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Commented to keep browser visible

    # Initialize WebDriver
    service = Service()  # Ensure ChromeDriver is set up correctly
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(url)  # Open the URL
        driver.implicitly_wait(10)  # Wait for elements to load

        # Extract all anchor (<a>) tags
        links = driver.find_elements(By.TAG_NAME, "a")

        # Get the href attribute of each link (only valid links)
        urls = [link.get_attribute("href") for link in links if link.get_attribute("href")]

        return urls
    finally:
        input("Press Enter to close the browser...")  # Keep browser open
        driver.quit()  # Close the browser session

# Example usage
url = "https://support.thetrainline.com/en/support/solutions/folders/78000000023"  # Replace with your target URL
all_links = get_all_links(url)

# Print the extracted URLs
print("\nExtracted Links:")
for link in all_links:
    print(link)
