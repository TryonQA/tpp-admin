from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
## ADJUST ABOVE BASED ON LOCAL INSTALL

FILTER_TAGS = ["Clear to transport","Not clear to transport",">=1000000","<1000000",\
    "Wheelchair v. available","Has drug testing","Has supplier diversity"]

creds = open('creds.txt')
creds_data = creds.readline()
comma = creds_data.find(",")
user = creds_data[:comma]
password = creds_data[comma+1:]
creds.close()

driver = webdriver.Chrome(PATH)
driver.implicitly_wait(4)

def login_tpp(driver):
    driver.get('https://tpp-qa.americanlogistics.com/providers')
    #time.sleep(2)
    button = driver.find_element_by_class_name('MuiButton-containedPrimary')
    button.click()
    #time.sleep(3)
    uname = driver.find_element_by_id('i0116')
    uname.send_keys(user)

    u_button = driver.find_element_by_id('idSIButton9')
    u_button.click()
    time.sleep(2)

    pwd = driver.find_element_by_id('i0118')
    pwd.send_keys(password)

    p_button = driver.find_element_by_id('idSIButton9')
    p_button.click()
    time.sleep(2)

    c_button = driver.find_element_by_id('idSIButton9')
    c_button.click()

def open_filters_menu(driver):
    driver.refresh()
    time.sleep(1)
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    f_knob = driver.find_element_by_xpath('//div[@aria-haspopup="listbox"]')
    #driver.execute_script("return arguments[0].scrollIntoView(true);", f_knob)
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(f_knob, f_knob.size['width']-25, 0)
    action.click()
    action.perform()
    #f_knob.click()

def close_filters_menu(driver):
    f_knob = driver.find_element_by_class_name('MuiSelect-selectMenu')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(f_knob, -10, 0)
    action.click()
    action.perform()

def get_company_entries(driver):
    companies = driver.find_elements_by_xpath('//a[@class="MuiTypography-root MuiLink-root MuiLink-underlineHover MuiTypography-colorTextPrimary"]')
    return companies

def filter_clicker(driver,filter_buttons_list,close=True):
    #filter buttons indexed 0-6
    open_filters_menu(driver)
    filters = driver.find_elements_by_xpath('//span[@class="MuiTypography-root MuiListItemText-primary MuiTypography-body1 MuiTypography-displayBlock"]')
    for index in filter_buttons_list:
        filters[index].click()
    if close:
        close_filters_menu(driver)

def filter_reset(driver,open=True,close=True):
    if open:
        open_filters_menu(driver)
    clear_button = driver.find_element_by_xpath('//button[@class="MuiButtonBase-root MuiButton-root MuiButton-text MuiButton-fullWidth"]')
    clear_button.click()
    if close:
        close_filters_menu(driver)


def filter_checks(driver,filter_buttons_list):
    #collect on screen elements
    readout = "Testing "
    if len(filter_buttons_list)>1:
        readout += "COMBO "
    for nums in filter_buttons_list:
        readout += FILTER_TAGS[nums]
        readout += ' / '
    print(readout)
    time.sleep(2)
    co_entries_orig = get_company_entries(driver)
    num_entries = len(co_entries_orig)
    score = 0
    co_data = []
    i = 0
    # get co data
    while i < num_entries:
        co_entries = get_company_entries(driver)
        num_entries = len(co_entries)
        if i < len(co_entries):
            company = co_entries[i] 
            company.click()
            time.sleep(2)
            title_element = driver.find_element_by_xpath('//span[@class="MuiTypography-root MuiCardHeader-title MuiTypography-h5 MuiTypography-displayBlock"]/div/div')
            this_co_name = title_element.text
            data = driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-sm-12 MuiGrid-grid-md-6 MuiGrid-grid-lg-3"]/div/div/div[2]')
            data_text = []
            for d_pt in data:
                #print(d_pt.text)
                data_text.append(d_pt.text)
            buttons = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiTab-root MuiTab-textColorPrimary MuiTab-fullWidth"]')
            ins_button = buttons[1]
            ins_button.click()
            ins_data = driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-sm-12 MuiGrid-grid-md-6 MuiGrid-grid-lg-3"]/div/div/div[2]')
            ins_data_text = []
            for i_pt in ins_data:
                ins_data_text.append(i_pt.text)
            this_co_data = [data_text[5],[ins_data_text[6],ins_data_text[7],ins_data_text[8]],data_text[4],data_text[6],data_text[7],this_co_name]

            co_data.append(this_co_data)
            i+=1
            buttons2 = driver.find_elements_by_xpath('//a')
            for b in buttons2:
                if b.text == "Back to Transportation Providers":
                    b.click()
                    break
            time.sleep(1)
    
    #check co data
    for d_list in co_data:
        this_pass = True
        if 0 in filter_buttons_list:
            if d_list[0] != 'Yes':
                this_pass = False
                print(d_list[5] + " FAILED " + FILTER_TAGS[0])
        if 1 in filter_buttons_list:
            if d_list[0] != 'No':
                this_pass = False
                print(d_list[5] + " FAILED " + FILTER_TAGS[1])
        if 2 in filter_buttons_list:
            all_under = True
            for i_data in d_list[1]:
                if len(i_data) >= 13:
                    all_under = False
            if all_under:
                this_pass = False
                print(d_list[5] + " FAILED " + FILTER_TAGS[2])
        if 3 in filter_buttons_list:
            all_over = True
            for i_data in d_list[1]:
                if len(i_data) < 13:
                    all_over = False
            if all_over:
                this_pass = False
                print(d_list[5] + " FAILED " + FILTER_TAGS[3])
        if 4 in filter_buttons_list:
            if d_list[2] != 'Yes':
                this_pass = False
                print(d_list[5] + " FAILED " + FILTER_TAGS[4])
        if 5 in filter_buttons_list:
            if d_list[3] != 'Yes':
                this_pass = False
                print(d_list[5] + " FAILED " + FILTER_TAGS[5])
        if 6 in filter_buttons_list:
            if d_list[4] != 'Yes':
                this_pass = False
                print(d_list[5] + " FAILED " + FILTER_TAGS[6])
        if this_pass:
            score+=1

    if num_entries > 0:
        test_score = (score/num_entries)*100.0
        print(str(test_score)+"%")
    else:
        print("Filter yields no results")

def print_element_info(e):
    location = e.location
    size = e.size
    w, h = size['width'], size['height']

    print(location)
    print(size)
    print(w, h)

def run_single_filter_test(driver,click_list):
    filter_clicks = click_list
    filter_clicker(driver,filter_clicks)
    time.sleep(2)
    filter_checks(driver,filter_clicks)
    filter_reset(driver)

def run_all_filter_tests(driver):
    click_list = [0,1,2,3,4,5,6]
    while len(click_list)>0:
        print(click_list)
        if len(click_list) > 0:
            run_single_filter_test(driver,click_list)
        ascending = True
        for i in range(0, len(click_list), 1):
            if i == 0:
                pass
            else:
                if click_list[i] != click_list[i-1]+1:
                    ascending = False
        if ascending:
            if click_list[-1] == 6 and click_list:
                click_list.pop(-1)
                if len(click_list) > 0:
                    if click_list[0] != 0:
                        print('reach')
                        reduction = click_list[0]
                        for i in range(0, len(click_list), 1):
                            click_list[i] = click_list[i] - reduction
            else:
                click_list[-1]+=1
        else:
            if click_list[-1] != 6:
                click_list[-1] += 1
            else:
                for i in range(len(click_list)-1, -1, -1):
                    if click_list[i] > click_list[i-1]+1:
                        click_list[i-1]+=1
                        if click_list[i] > click_list[i-1]+1:
                            for i2 in range(i,len(click_list),1):
                                click_list[i2] = click_list[i2-1]+1
                        break
    """         
    click_list = [6]
    while click_list[0]>=0:
        print(click_list)
        
        if click_list[-1] == 6 and len(click_list) > 6 - click_list[0]:
            click_list = [(click_list[0]-1)]
        else:
            if len(click_list)>1 and click_list[-1] > click_list[-2]+1:
                click_list[-1] -= 1
            else:
                click_list.append(6)
    """ 

login_tpp(driver)
time.sleep(2)

filter_clicker(driver,[0,1,2,3,4,5,6],False)
filter_reset(driver,False,False)
# need filter test

#loop this for all combos
run_all_filter_tests(driver)    

"""
#FILTER CHECK DEMO
filter_clicks = [0,2,5]
filter_clicker(driver,filter_clicks)
time.sleep(2)
filter_checks(driver,filter_clicks)
filter_reset(driver)
"""






#close_filters_menu(driver)
time.sleep(3)
#test_1(driver)
#driver.close()
driver.quit()