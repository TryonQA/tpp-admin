from selenium import webdriver
import time

PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"

dev_url = 'https://tpp-dev.americanlogistics.com/providers'
qa_url = 'https://tpp-qa.americanlogistics.com/providers'
uat_url = 'https://tpp-uat.americanlogistics.com/providers'
## ADJUST ABOVE BASED ON LOCAL INSTALL

def parse_url(args):
    url = qa_url
    if len(args) > 1:
        if args[1] == "uat":
            url =uat_url
        if args[1] == "dev":
            url = dev_url
    return url

def init_driver(url) -> webdriver.Chrome:
    driver = webdriver.Chrome(PATH)
    driver.implicitly_wait(5)
    driver.get(url)
    time.sleep(2)

    return driver

def get_username_and_password(role = "admin"):
    creds = open('creds.txt')

    creds_data = creds.readline()
    comma = creds_data.find(",")
    user = creds_data[:comma]
    password = creds_data[comma+1:]
    ""
    creds_data_2 = creds.readline()
    comma2 = creds_data_2.find(",")
    acc_user = creds_data_2[:comma2]
    acc_password = creds_data_2[comma2+1:]

    creds_data_3 = creds.readline()
    comma3 = creds_data_3.find(",")
    ro_user = creds_data_3[:comma3]
    ro_password = creds_data_3[comma3+1:]

    #print(ro_user,ro_password)
    ""
    creds.close()

    if role == "admin":
        return user, password
    elif role == "billing":
        return acc_user, acc_password
    elif role == "read-only":
        return ro_user, ro_password

def end_session(driver:webdriver.Chrome):
    driver.close()
    driver.quit()

class ResultHandler:
    def __init__(self):
        self.results = []

    def handle_results(self,result_tup):
        print(result_tup)
        self.results.append(result_tup)