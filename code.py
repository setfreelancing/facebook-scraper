from concurrent.futures import process
import datetime
from logging import exception
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pa
import random
import time
import os
datarow = []
colomns = []
with open('./Input/settings.txt', 'r') as f:
    try:
        mainUrl = f.readline()
        chromedriverpath = f.readline()
    except Exception as e :
        print('Please provide a valid url or chrome driver path'+e.args[0])

    
    
#Just an rng factor for the delay between requests to make the bot more human
def random_float(low, high):
    return random.random()*(high-low) + low
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chromedriverpath,chrome_options=chrome_options)
try:
    driver.get("https://www.facebook.com")
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
    time.sleep(random_float(1,3))
    username.clear()
    username.send_keys("majholmeme@gmail.com")
    time.sleep(random_float(1,3))
    password.clear()
    password.send_keys("mhmdashek445")
    time.sleep(random_float(1,3))
    button = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(random_float(1,3))
    driver.get(mainUrl)
    divexist = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='ihqw7lf3']")))
    try:
        reviews_and_rating = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".lr9zc1uh.a5q79mjw.g1cxx5fr.b1v8xokw"))).text.split('\n')[2]
        rating = reviews_and_rating.split('(')[0][0:-1]
        reviews = reviews_and_rating.split('(')[1][0:-1]
    except Exception as e:
        reviews_and_rating = None
    try:  
        reviews_and_rating = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".lr9zc1uh.a5q79mjw.g1cxx5fr.b1v8xokw"))).text.split('\n')[2]
        rating = reviews_and_rating.split('(')[0][0:-1]
        reviews = reviews_and_rating.split('(')[1][0:-1]
    except Exception as e:
        reviews_and_rating = None
    #driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        video_text = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR,".lrazzd5p.oo9gr5id.hzawbc8m"))).text
    except Exception as e:
        video_text = None
    try:
        views_vid= WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh e9vueds3 j5wam9gi b1v8xokw m9osqain']"))).text
    except Exception as e:
        views_vid = None
    title = driver.find_element(By.CLASS_NAME, "embtmqzv").text
    time.sleep(random_float(1,3))
    elements = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='s9t1a10h']")))
    elements =  driver.find_element(By.XPATH, "//div[@class='s9t1a10h']//span[@dir='auto']")
    print("created_at")
    print("===>",elements.get_attribute('innerHTML'))
    driver.get(mainUrl+'/about/?ref=page_internal')
    elements = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[class='je60u5p8']")))
    alldivs = driver.find_elements(By.CLASS_NAME, 'je60u5p8')
    for i in alldivs:
        isfirst = True
        firstdiv =""
        space = ""
        titledivs = i.find_elements(By.XPATH, ".//span[@dir='auto']")
        for v in titledivs:
            print(space,v.text)
            if (isfirst):
                isfirst = False
                space = "===>"
                firstdiv = v.text
            else:
                if(v.text != "Send message"):
                    datarow.append([v.text,firstdiv])
    if reviews_and_rating != None :
        datarow.append([rating,'Rating'])
        datarow.append([reviews, 'Reviews'])
    if video_text != None :
        datarow.append([video_text,'Video Text'])
    if views_vid != None : 
        datarow.append([views_vid,'views'])
    datarow.append([title,'Page Name'])
except Exception as e:
    print('error: ',e)
driver.close()
driver.quit()
dt_f = pa.DataFrame(data=datarow,columns=['Text','Parent'])
desktop = os.path.join(os.path.join(os.environ['USERPROFILE']), 'OneDrive') + '\Desktop'
isExist = os.path.exists(desktop)
csvpath = os.path.join(desktop,str(int(round(datetime.datetime.timestamp(datetime.datetime.now())))))+'.csv'
dt_f.to_csv(csvpath,index=False)