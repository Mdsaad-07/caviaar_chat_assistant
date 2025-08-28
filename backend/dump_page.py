from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import time

# Your paths (update if needed)
chromedriver_path = r'C:\chromedriver-win64\chromedriver.exe'
brave_path = r'C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe'

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.binary_location = brave_path

service = Service(executable_path=chromedriver_path)

driver = webdriver.Chrome(service=service, options=options)
driver.get('https://caviaarmode.com/collections/all')
time.sleep(5)  # Wait for load

# Save page source
data = driver.page_source

with open('page_dump.html', 'w', encoding='utf-8') as f:
    f.write(data)

driver.quit()

print("Saved page source to page_dump.html. Open it in a browser and inspect products.")
