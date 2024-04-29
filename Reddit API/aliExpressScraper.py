from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Function to scrape items from AliExpress Bestsellers page
def scrape_aliexpress_bestsellers():
    # Set up Selenium WebDriver
    service = Service('/path/to/chromedriver')  # Update with your chromedriver path
    service.start()
    driver = webdriver.Remote(service.service_url)
    driver.get("https://www.aliexpress.com/popular")
    
    # Find and print titles and prices of items
    titles = driver.find_elements(By.CSS_SELECTOR, ".list-item .item-title")
    prices = driver.find_elements(By.CSS_SELECTOR, ".list-item .value")
    for title, price in zip(titles, prices):
        print(f"Title: {title.text}")
        print(f"Price: {price.text}")
        print()

    # Quit Selenium WebDriver
    driver.quit()

# Scrape and print items from AliExpress Bestsellers page
scrape_aliexpress_bestsellers()
