# /home/munikumar/miniconda3/envs/ipo_py/bin/python3
# Import the libraries
import requests 
from bs4 import BeautifulSoup
from utils import ipo_premium, gmp_today
from constants import IPO_PREMIUM_URL, GMP_TODAY_URL
from selenium import webdriver
from config import CHROME_PROFILE_PATH
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import time


# Define the URL of the IPO Watch website

def load_data(url: str) :
    response = requests.get(url) # Make a GET request to the URL and get the response
    soup = BeautifulSoup(response.content, "lxml") # Parse the response content as HTML using BeautifulSoup
    return soup
today_date = datetime.today()
soup = load_data(IPO_PREMIUM_URL) 
ipo_premium_data = ipo_premium.get_data(soup,today_date)
print("premium: \n"+ipo_premium_data)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
options.add_argument(CHROME_PROFILE_PATH)
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)

ipo_gmp_data = gmp_today.get_gmp_today(driver, GMP_TODAY_URL,today_date)
print("gmp: \n"+ipo_gmp_data)
url = "https://web.whatsapp.com/"
driver.get(url)
wait = WebDriverWait(driver,500)
search_box_path = '//*[@id="side"]/div[1]/div/div[2]/div[2]/div/div[1]/p'
search_box = wait.until(EC.presence_of_element_located((By.XPATH,search_box_path)))
search_box.send_keys("Ipo")
# target = '"Ipo"'
contact_path = '//span[@title="Ipo"]'
contact = wait.until(EC.presence_of_element_located((By.XPATH,contact_path)))
contact.click()
input_field_path = '//div[@class="to2l77zo gfz4du6o ag5g9lrv bze30y65 kao4egtt"][@contenteditable="true"][@title="Type a message"][@data-tab="10"]'
input_field = wait.until(EC.presence_of_element_located((By.XPATH,input_field_path)))
input_field.send_keys(ipo_premium_data+Keys.ENTER)
input_field.send_keys(ipo_gmp_data+Keys.ENTER)
time.sleep(5)
driver.quit()
