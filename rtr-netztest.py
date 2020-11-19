from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import TimeoutException
import os,datetime,csv
import pickle

browser = webdriver.Edge(os.path.join(os.path.dirname(__file__),"msedgedriver.exe"))

try:
    try:
        browser.get('https://www.netztest.at/')
        cookies = pickle.load(open(os.path.join(os.path.dirname(__file__),'cookies.pkl'), "rb"))
      
        for cookie in cookies:
            if cookie['name'] == 'RMBTuuid':
                cookie['expiry'] = int((datetime.datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)-datetime.datetime(1970,1,1)).total_seconds()+1209600)
                browser.add_cookie(cookie)
                print ("added cookie ", cookie)
    except Exception:
        print ("Couldn't load cookies")
            
    browser.get('https://www.netztest.at/de/Test')

    delay = 30 # seconds
    #wait for button to allow test and click it
    try:
        button = WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.ui-dialog-buttonpane.ui-widget-content > div > button:nth-child(2)')))
        button.click()
        print ("Test started")
        delay = 350 # seconds
        try:
            WebDriverWait(browser, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#testresult-detail > tbody > tr:nth-child(1) > td:nth-child(2) > span')))
            print ("Page is ready!")
            print (browser.current_url)
            # save results as csv
            #DL-speed
            downspeed = browser.find_element_by_css_selector('#verlauf-detail > tbody > tr:nth-child(1) > td:nth-child(3)').text
            #UL speed
            upspeed = browser.find_element_by_css_selector('#verlauf-detail > tbody > tr:nth-child(2) > td:nth-child(3)').text
            #Ping
            ping = browser.find_element_by_css_selector('#verlauf-detail > tbody > tr:nth-child(3) > td:nth-child(3)').text
            #timestamp
            timestamp = browser.find_element_by_css_selector('#testresult-detail > tbody > tr:nth-child(1) > td:nth-child(2) > span').text
            print ("DL: "+downspeed+" ; UL: "+upspeed+" ; ping: "+ping)
            fields=[timestamp,downspeed,upspeed,ping,browser.current_url]
            with open(os.path.join(os.path.dirname(__file__),'results.csv'), 'a',newline="") as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            # save cookies
            pickle.dump(browser.get_cookies() , open(os.path.join(os.path.dirname(__file__),'cookies.pkl'),"wb"))
        except TimeoutException:
            print ("Loading took too much time!")
            print (browser.current_url)
    except TimeoutException:
        print ("Didn't find accept button")
        print (browser.current_url)

finally:
    browser.quit()