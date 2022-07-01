#to run: python load_tester.py env users request_num
#what I've been running: python load_tester.py dev 1 250

#Will need to install selenium for python and download the appropriate selenium chrome driver locally
#https://selenium-python.readthedocs.io/
#https://chromedriver.chromium.org/downloads

import time
import sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
## ADJUST ABOVE BASED ON LOCAL INSTALL ##

dev_url = 'https://tpp-dev.americanlogistics.com/providers'
qa_url = 'https://tpp-qa.americanlogistics.com/providers'
uat_url = 'https://tpp-uat.americanlogistics.com/providers'

#vvv Change below to false to leave browsers open on complete"
CLEANUP = True

#vvv Tune time between requests here vvv
DELAY = 1.95
#DEFAULTS for no arg usage
users = 1
request_num = 50

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome(PATH, options=options)
    
    driver.implicitly_wait(4)
    return driver

def login_tpp(driver,url):
    if url == dev_url:
        pre = "dev"
    if url == qa_url:
        pre = "qa"
    if url == uat_url:
        pre = "uat"
    u = pre + "_admin@tryon.com"
    p = "Try.tpp.23"

    driver.get(url)
    #time.sleep(2)
    username_field = driver.find_element_by_xpath('//input[@name="username"]')
    username_field.send_keys(u)
    driver.find_element_by_xpath('//input[@id="idp-discovery-submit"]').click()
    time.sleep(3)
    
    password_field = driver.find_element_by_xpath('//input[@name="password"]')
    password_field.send_keys(p)
    driver.find_element_by_xpath('//input[@id="okta-signin-submit"]').click()
    time.sleep(5)

def text_to_search(driver,search_text):
    search_field = driver.find_element_by_xpath('//input[@placeholder="Search by name"]')
    search_field.send_keys(Keys.CONTROL + 'a')
    search_field.send_keys(search_text)


args = sys.argv
url = qa_url
if len(args) > 1:
    if args[1] == "uat":
        url =uat_url
    if args[1] == "dev":
        url = dev_url
    if len(args) > 2:
        users = int(args[2])
    if len(args) > 3:
        request_num = int(args[3])

driver_list = []

for u in range(users):
    driver = init_driver()
    driver_list.append(driver)

for driver in driver_list:
    login_tpp(driver,url)

time.sleep(5)

to_search = "transpo"
end = len(to_search)
down = True
for r in range(request_num):
    current_search = to_search[0:end]
    if down:
        if end > 1:
            end-=1
        else:
            down = False
            end+=1
    else:
        if end < len(to_search):
            end+= 1
        else:
            down = True
            end-=1
    time.sleep(DELAY)
    for driver in driver_list:
        text_to_search(driver,current_search)

if CLEANUP:
    for driver in driver_list:
        driver.close()
        driver.quit()  