from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
def create_driver():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Specify the path to the chromedriver binary
    chromedriver_path = "/app/chromedriver/chromedriver"

    service = ChromeService("/app/chromedriver/chromedriver")
    return webdriver.Chrome(service = service, options=options)

# Example usage:
driver = create_driver()
# Now you can use the driver object for web automation tasks
