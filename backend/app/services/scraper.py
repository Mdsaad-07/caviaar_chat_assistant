import json
from typing import List, Dict
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_products(url: str = "https://caviaarmode.com/collections/all") -> List[Dict]:
    """Scrape product data using Selenium for dynamic content"""
    options = Options()
    # options.add_argument('--headless')  # Commented out for debugging, shows browser window
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36')
    
    # Your paths
    options.binary_location = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'
    chromedriver_path = r'C:\chromedriver-win64\chromedriver.exe'
    
    service = Service(executable_path=chromedriver_path)
    
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    
    # Wait for page body to load
    try:
        WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
        print("Page loaded successfully.")
        time.sleep(5)  # Wait additional time for JS
    except:
        print("Timeout: Page not loaded.")
        driver.quit()
        return []
    
    # Scroll to load lazy content
    for _ in range(3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
    
    products = []
    
    # Note: Update selector after inspection
    items = driver.find_elements(By.CSS_SELECTOR, 'li.grid__item')
    
    print(f"Found {len(items)} product containers")
    
    for item in items:
        try:
            name = item.find_element(By.CSS_SELECTOR, '.card__heading').text.strip()
            price = item.find_element(By.CSS_SELECTOR, '.price__regular .price-item').text.strip()
            description = item.find_element(By.CSS_SELECTOR, '.card__information p').text.strip() if item.find_elements(By.CSS_SELECTOR, '.card__information p') else ""
            image_url = item.find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
            product_url = "https://caviaarmode.com" + item.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
            category = item.find_element(By.CSS_SELECTOR, '.motion-reduce').text.strip() if item.find_elements(By.CSS_SELECTOR, '.motion-reduce') else "Unknown"
            
            products.append({
                "name": name,
                "price": price,
                "description": description,
                "image_url": image_url,
                "url": product_url,
                "category": category
            })
        except:
            print("Skipped an item due to missing elements.")
            continue
        time.sleep(0.5)
    
    driver.quit()
    
    # Save to JSON
    with open('app/products.json', 'w') as f:
        json.dump(products, f)
    
    return products

if __name__ == "__main__":
    products = scrape_products()
    print(f"Scraped {len(products)} products:")
    for p in products[:5]:
        print(p)
    print("Data saved to app/products.json")
