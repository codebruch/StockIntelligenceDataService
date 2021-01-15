from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
import decimal 
import os, sys
import datetime
import time
import locale
import requests
import argparse
import socketio
import json
import pandas as pd

calledTimes = 0

#Table Structure


def dataframeFromMySQL(MysqlConn,WKN):
    return 0

def dataframeToMySQL(df,MysqlConn,WKN):
    return 0


def getTableValuesOnePage(driver,ec):
    global calledTimes
    
    df = pd.DataFrame(
    {"Date" : [],
    "Open" : [],
    "High" : [],
    "Low" : [],
    "Close" : [],
    "Volume" : []
    })


    cnt = 0

    calledTimes = calledTimes + 1
    print('calledTimes: '+str(calledTimes))
    try: 
        WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, './/*[@id="id_pricedata-layer"]/div/div[2]/div/div/div/div/div/div/div[2]/table')))
    except (TimeoutException):
        print("end of pagination")
        return liste

    table = driver.find_elements_by_xpath('.//*[@id="id_pricedata-layer"]/div/div[2]/div/div/div/div/div/div/div[2]/table')
    #table = driver.find_elements_by_class_name('table table--collapse-sm display table--mobile-table')
    WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.CLASS_NAME, 'table__column--top')))
  
    records = table[0].find_elements_by_class_name('table__column--top') 
    time.sleep(2)
    for record in records:

        print('cnt: '+str(cnt))
        #print(record)
        ccount = cnt % 6
        if ccount == 0:
            print('Date: ' + record.text)
            Date = record.text
        if ccount == 1:
            print('Open: ' + record.text)
            Open = record.text
        if ccount == 2:
            print('High: ' + record.text)
            High = record.text  
        if ccount == 3:
            print('Low: ' + record.text)
            Low = record.text  
        if ccount == 4:
            print('Close: ' + record.text)
            Close = record.text 
        if ccount == 5:
            print('Volume: ' + record.text)
            Volume = record.text
                
            dfTmp = pd.DataFrame(
            {"Date" : [Date],
            "Open" : [Open],
            "High" : [High],
            "Low" : [Low],
            "Close" : [Close],
            "Volume" : [Volume]
            })
            df.append(dfTmp)


            

        cnt = (cnt + 1)

    return  (cnt,df) 

parser = argparse.ArgumentParser()
parser.add_argument('-w', '--wkn')
args = parser.parse_args()
wkn = args.wkn

locale.setlocale(locale.LC_ALL, 'de_DE.UTF-8') # 
print(os.getcwd())



chrome_options = Options()
#chrome_options.add_argument("--disable-extensions")
#chrome_options.add_argument("--disable-gpu")
#chrome_options.add_argument("--no-sandbox") # linux only
#chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works


path = os.path.dirname(os.path.abspath(__file__))
prefs = {"download.default_directory":path}

chrome_options.add_experimental_option("prefs", prefs)


driver = webdriver.Chrome(r"C:\\Users\\d047102\\Desktop\\StockIntelligenceDataService\\chromedriver.exe",options=chrome_options) #C:\\Users\\d047102\\Desktop\\DemoDataGrabber
#//*[@id="app--idDemoSearchField-inner"]

driver.get("https://www.comdirect.de/inf/index.html")
driver.maximize_window()
#driver.implicitly_wait(2)
WebDriverWait(driver, 60).until(ec.presence_of_element_located((By.XPATH, './/*[@id="uc-btn-accept-banner"]')))
YesButton = driver.find_elements_by_xpath('.//*[@id="uc-btn-accept-banner"]')

YesButton[0].click()

searchField = driver.find_elements_by_xpath('.//*[@id="search_form"]/input')
print("Element is visible? " + str(searchField[0].is_displayed()))

searchField[0].send_keys(wkn)

searchButton = driver.find_elements_by_xpath('.//*[@id="search_form"]/a')

searchButton[0].click()




WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.LINK_TEXT, 'Chart')))




selectMarket = driver.find_elements_by_xpath('.//*[@id="marketSelect"]')
if len(selectMarket) > 0:
    selectMarket[0]
    Select(selectMarket[0]).select_by_visible_text('Xetra')


time.sleep(2)
driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.LINK_TEXT, 'Chart'))))
time.sleep(1)
ActionChains(driver).move_to_element(WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "body > div.cif-scope-content-wrapper.siteFrame.advertising-scope > div > div:nth-child(2) > div.col__content.col__content--no-padding.hidden-print.bg-color--cd-black-7 > div > div > div > div.button-group__container.hidden-sm > a:nth-child(4) > span")))).click().perform()

driver.implicitly_wait(5)


time.sleep(2)
driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.LINK_TEXT, 'Max'))))
time.sleep(1)
ActionChains(driver).move_to_element(WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#chartForm > div.button-area.outer-spacing--none > div > div > div.button-group__container.hidden-sm.hidden-md > a:nth-child(8) > span")))).click().perform()

time.sleep(2)


time.sleep(2)
driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.LINK_TEXT, 'Kursdaten'))))
time.sleep(1)
ActionChains(driver).move_to_element(WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#openQuoteListButton")))).click().perform()

#time.sleep(2)
#driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.LINK_TEXT, 'Daten für Excel (csv) exportieren'))))
#time.sleep(1)
#demos = driver.find_elements_by_class_name('coverpic-desc-icons-asset-role') 
#ActionChains(driver).move_to_element(WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.CSS_SELECTOR, "#id_pricedata-layer > div > div.layer__content.layer__content--wider-lg > div > div > div > div > div > div > div.button-area.button-area--single-right > div > a > span")))).click().perform()

#//*[@id="id_pricedata-layer"]/div/div[2]/div/div/div/div/div/div/div[3]/div[1]/div[2]

recordcount = -1
while recordcount != 0:
    (recordcount,df) = getTableValuesOnePage(driver,ec)
    print('recordcount: ' + str(recordcount))

    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.CLASS_NAME, 'icon__svg'))))
   
    ActionChains(driver).move_to_element(WebDriverWait(driver, 20).until(ec.element_to_be_clickable((By.XPATH, './/*[@id="id_pricedata-layer"]/div/div[2]/div/div/div/div/div/div/div[3]/div[1]/div[2]')))).click().perform()
    time.sleep(1)
    driver.execute_script("arguments[0].scrollIntoView();", WebDriverWait(driver, 20).until(ec.visibility_of_element_located((By.XPATH, './/*[@id="FORM_KURSDATEN"]/div[3]'))))

    


