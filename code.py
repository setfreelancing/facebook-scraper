import datetime
from logging import exception
import math
import this
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pa
import random
import time
import os
import csv
datarow = []
with open(r'C:\Users\admin\OneDrive\Documents\GitHub\facebook-scraper\input\settings.txt', 'r') as f:
        chromedriverpath = f.readline()

#Just an rng factor for the delay between requests to make the bot more human
def random_float(low, high):
    return random.random()*(high-low) + low

chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chromedriverpath,chrome_options=chrome_options)

def doscrape(url,maxdivs):
    thisrow=[]
    driver.get(url)
    try:
        reviews_and_rating = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".lr9zc1uh.a5q79mjw.g1cxx5fr.b1v8xokw"))).text.split('\n')[2]
        rating = reviews_and_rating.split('(')[0][0:-1]
        reviews = reviews_and_rating.split('(')[1][0:-1]
    except Exception as e:
        reviews_and_rating = None
    try:
        video_text = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR,".lrazzd5p.oo9gr5id.hzawbc8m"))).text
    except Exception as e:
        video_text = None
    try:
        views_vid= WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, "span[class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh e9vueds3 j5wam9gi b1v8xokw m9osqain']"))).text
    except Exception as e:
        views_vid = None
    title = driver.find_element(By.CLASS_NAME, "embtmqzv").text
    time.sleep(random_float(0.5,2))
    driver.get(url+'/about/?ref=page_internal')
    time.sleep(random_float(0.5,2))
    alldivs = driver.find_elements(By.CLASS_NAME, 'je60u5p8')
    thisrow.append(title)
    if reviews_and_rating != None :
        thisrow.append(rating)
        thisrow.append(reviews)
    else:
        thisrow.append('NA')
        thisrow.append('NA')
    if video_text != None :
        thisrow.append(video_text)
    else:
        thisrow.append('NA')
    if views_vid != None :
        thisrow.append(views_vid)
    else:
        thisrow.append('NA')
    currentdivs =0
    for i in alldivs:
        isfirst = True
        firstdiv =""
        titledivs = i.find_elements(By.XPATH, ".//span[@dir='auto']")
        currentdivs += len(titledivs)
        for v in titledivs:
            if (isfirst):
                isfirst = False
                firstdiv = v.text
            else:
                if(v.text != "Send message"):
                    thisrow.append(f'{firstdiv}: {v.text}')
    maxdivs = max(currentdivs, maxdivs)
    return thisrow,maxdivs
try:
    driver.get("https://www.facebook.com")
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))
    username.clear()
    username.send_keys("majholmeme@gmail.com")
    password.clear()
    password.send_keys("mhmdashek445")
    time.sleep(random_float(0.5,2))
    button = WebDriverWait(driver, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
    time.sleep(random_float(0.5,2))

except Exception as e:
    print('error: ',e)

with open(r'.\input\Book1.csv' ,'r') as csv_file:
    csv_reader= csv.reader(csv_file)
    maxdivs = 0
    for line in csv_reader:
        currentrow, mdivs = doscrape(line[0],maxdivs)
        datarow.append(currentrow)
        maxdivs = mdivs

driver.close()
driver.quit()
for row in datarow: 
    while (maxdivs + 1 - len(row)) > 0 :
        row.append('NA')
datacolumns = ['Page Title','Rating','Reviews','Video Text','Video Views']
while len(datacolumns) < maxdivs+1:
    datacolumns.append(f'About#{len(datacolumns)- 4}')
dt_f = pa.DataFrame(data=datarow,columns=datacolumns)
dest = '.\Output'
isExist = os.path.exists(dest)
csvpath = os.path.join(dest,str(int(round(datetime.datetime.timestamp(datetime.datetime.now())))))+'.csv'
dt_f.to_csv(csvpath,index=False)