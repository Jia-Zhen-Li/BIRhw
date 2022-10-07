# -*- coding: UTF-8 -*-
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time,json,os
from django.conf import settings

str_test="32265180,33975005,33572857,33236131,33305456,32853038,35105985,33307513,32868092,34241776,33244462,32679589,33024307,32971147,33666147,33053381,33435929,32889088,33868239,33246480,33811458,34333882,32703064,33442016,33288230,33807592,32889701,33506952,33010669,33206207,32921216,34815503,34866128,33664170,34941414,32582617,35029046,33132005,33428706,34181630,33633106,35163638,33003103,32378801,33278517,33210477,33193418,33193377,34258904,33617700,33303302,33136431,34324964,34918317,34024060,34949249,33829393,33287245,34162043,33543668,34563684,33877122,33989898,34207756,34696528,33788668,33561753,33464917,32358960,34410360,34059436,33187528,33948037,33903964,33682604,33852809,34056843,33851612,34855502,33531805,34156698,34812049,34490732,35945375,33843611,33795584,34288409,33193427,34213514,33160064,33293238,33833211,34659259,33775065,32944809,33989051,33185582,34535791,34864875,33689569"

from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
print(BASE_DIR)


term = input('term')
size = int(input('size'))
text_list=[]
url='https://twitter.com/search?q='+term
options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
driverPath=os.path.join('chromedrive','chromedriver.exe')
#driverPath='chromedriver'
chrome = webdriver.Chrome(executable_path=driverPath,chrome_options=options) 
chrome.get(url)
time.sleep(1)

while(size>len(text_list)):
    html_source = chrome.page_source
    tweet={'user':'','id':'','text':'','time':''}
    #print(html_source)

    soup = BeautifulSoup(html_source,'lxml')
    tweetText = soup.find_all('div',{'data-testid':'tweetText'})
    tweetUser = soup.find_all('span',{'class':'css-901oao css-16my406 css-1hf3ou5 r-poiln3 r-bcqeeo r-qvutc0'})
    tweetID = soup.find_all('div',{'class':'css-901oao css-1hf3ou5 r-14j79pv r-18u37iz r-37j5jr r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0'})
    tweetTime = soup.find_all('time')
    for i in range(len(tweetText)):
        tweet['user']=tweetUser[i].text
        print(tweetID[i].text)
        tweet['id']=tweetID[i].text
        tweet['text']=tweetText[i].text
        print(tweetTime[i])
        tweet['time']=tweetTime[i]['datetime']

        text_list.append(tweet)
        print(tweet)
    #scroll down until size == len(text_list)
    last_height = chrome.execute_script("return document.body.scrollHeight")
    chrome.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(1)

    # Calculate new scroll height and compare with last scroll height
    new_height = chrome.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    if size<=len(text_list):
        break
    last_height = new_height

print(len(text_list))
    