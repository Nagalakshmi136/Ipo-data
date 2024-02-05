from selenium import webdriver
# from config import CHROME_PROFILE_PATH
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# from constants import GMP_TODAY_URl
import pandas as pd

def get_gmp_today(driver,url,today_date):
    driver.get(url)
    wait = WebDriverWait(driver,500)
    title_paths = '//*[@id="openIPO"]/div/div[1]/div/table/thead/tr/th'
    title_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH,title_paths)))
    titles = []
    for cell in title_elements:
        titles.append(cell.text.replace(" ","_"))
    ipos_data = []
    rows_path = '//*[@id="openIPO"]/div/div[1]/div/table/tbody/tr'
    rows = len(wait.until(EC.presence_of_all_elements_located((By.XPATH,rows_path))))
    for row in range(1,rows+1):
        cells = wait.until(EC.presence_of_all_elements_located((By.XPATH,f'//*[@id="openIPO"]/div/div[1]/div/table/tbody/tr[{row}]/td')))
        ipo_data = {}
        for i in range(len(cells)-1):
            ipo_data[titles[i]] = cells[i].text
        ipos_data.append(ipo_data)
    df = pd.DataFrame(ipos_data)
    df[titles[5]] = pd.to_datetime(df[titles[5]])
    df[titles[6]] = pd.to_datetime(df[titles[6]])
    filtered_df = df[(df[titles[5]]<=today_date) & (df[titles[6]]>=today_date)]
    ipos_data = filtered_df.to_dict(orient='index')
    # driver.quit()
    return str(ipos_data)

            
