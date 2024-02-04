
from selenium import webdriver
from config import CHROME_PROFILE_PATH
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from constants import GMP_TODAY_URL

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument(CHROME_PROFILE_PATH)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
url = "https://web.whatsapp.com/"
driver.get(url)
driver.quit()
driver.get(GMP_TODAY_URL)