#chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\Users\dammy.OLUWADAMILOLA\VS Developer\localhost"

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

url = "https://rowy.app/p/overlapd-13268/tables"

options = webdriver.ChromeOptions()
options.add_experimental_option("debuggerAddress","localhost:9222")
#options.add_argument("--headless")
#options.add_argument('--disable-blink-features=AutomationControlled')
#options.add_argument("--disable-extensions")
#options.add_experimental_option('useAutomationExtension', False)
#options.add_experimental_option("excludeSwitches", ["enable-automation"])
#options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3")
driver = webdriver.Chrome(options=options)

driver.get(url)

time.sleep(200)

