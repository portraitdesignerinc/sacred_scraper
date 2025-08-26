import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

CHROME_DRIVER = r"C:\selenium\139.0.7258.2\chromedriver-win64\chromedriver.exe"
CHROME_BINARY = r"C:\selenium\139.0.7258.2\chrome-win64\chrome_proxy.exe"
HYMNS_URL = "https://www.churchofjesuschrist.org/media/music/collections/hymns?lang=eng"

# Rotating user agents and proxy configurations
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.1 Safari/605.1.15"
]

PROXY_LIST = [
    "144.126.254.255:80",
    "103.156.17.41:8080", 
    "95.217.62.36:3128",
    "138.197.102.119:80",
    "165.232.129.150:80"
]

def random_wait():
    return random.randint(7, 15)

def human_wait():
    return random.uniform(8, 18)

def micro_pause():
    time.sleep(random.uniform(0.3, 0.8))



def create_browser():
    # Rotate user agent and proxy for each session
    user_agent = random.choice(USER_AGENTS)
    proxy = random.choice(PROXY_LIST)
    
    options = Options()
    options.binary_location = CHROME_BINARY
    options.add_argument("--remote-debugging-port=9222")
    
    # Anti-detection arguments
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument(f"--proxy-server=http://{proxy}")
    options.add_argument("--disable-web-security")
    options.add_argument("--allow-running-insecure-content")
    
    driver = webdriver.Chrome(service=Service(CHROME_DRIVER), options=options)
    
    # Remove webdriver property
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    print(f"Using User Agent: {user_agent[:50]}...")
    print(f"Using Proxy: {proxy}")
    
    return driver

def test_single_href_selection(target_href):
    driver = create_browser()
    
    driver.get(HYMNS_URL)
    time.sleep(random_wait())
    
    element = driver.find_element(By.XPATH, f"//a[@href='{target_href}']")
    element.click()
    time.sleep(random_wait())
    
    print(f"Navigated to: {driver.current_url}")
    print(f"Title: {driver.title}")
    
    # Pure Selenium scrolling - find body element and send Page Down key
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.PAGE_DOWN)
    time.sleep(random_wait())
    
    # Download functionality
    try:
        # 1. Click the Download button
        download_button = driver.find_element(By.XPATH, "//button[normalize-space()='Download']")
        download_button.click()
        micro_pause()
        
        # 2. Wait for the dropdown dialog to appear
        dialog = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "dialog.DownloadButton__StyledCallout-sc-1jax8yp-0"))
        )
        time.sleep(human_wait())
        
        # 3. Get the PDF link inside the dropdown
        pdf_link = driver.find_element(By.XPATH, "//a[contains(@href, '.pdf')]")
        pdf_url = pdf_link.get_attribute("href")
        print(f"PDF Download Link: {pdf_url}")
        
    except Exception as e:
        print(f"Download process failed: {e}")
    
    driver.quit()

# MAIN EXECUTION
target_href = "/media/music/songs/the-morning-breaks?crumbs=hymns&lang=eng"
test_single_href_selection(target_href)
print("Complete!")