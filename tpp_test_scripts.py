from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
## ADJUST ABOVE BASED ON LOCAL INSTALL

FILTER_TAGS = ["Clear to transport","Not clear to transport",">=1000000","<1000000",\
    "Wheelchair v. available","Has drug testing","Has supplier diversity"]
COVERAGE_SEARCH_KEY = "coverage_tp"
NAME_SEARCH_KEY = "name_tp"

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

def get_company_data(driver):
    co_entries_orig = get_company_entries(driver)
    num_entries = len(co_entries_orig)
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
            legal_data = driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2"]/div/div/div/div')
            l_data_text = []
            #test = 0
            for ld_pt in legal_data:
                #print(str(test)+" - "+ld_pt.text)
                l_data_text.append(ld_pt.text)
                #test+=1
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
            #this_co_data = [data_text[5],[ins_data_text[6],ins_data_text[7],ins_data_text[8]],data_text[4],data_text[6],data_text[7],this_co_name]
            this_co_data = {
                "clear":data_text[5],
                "ins_list":[ins_data_text[6],ins_data_text[7],ins_data_text[8]],
                "wheelchair":data_text[4],
                "drug":data_text[6],
                "diversity":data_text[7],
                "name":this_co_name,
                "owner_first":l_data_text[47],
                "owner_last":l_data_text[49],
                "coverage_area":l_data_text[93]
            }

            co_data.append(this_co_data)
            i+=1
            buttons2 = driver.find_elements_by_xpath('//a')
            for b in buttons2:
                if b.text == "Back to Transportation Providers":
                    b.click()
                    break
            time.sleep(1)
    return co_data

def filter_checks(driver,filter_buttons_list):
    #collect on screen elements
    readout = "Testing "
    if len(filter_buttons_list)>1:
        readout += "COMBO "
    for nums in filter_buttons_list:
        readout += FILTER_TAGS[nums]
        readout += ' / '
    print(readout)
    score = 0
    time.sleep(2)
    co_data = get_company_data(driver)
    
    #check co data
    for d_list in co_data:
        this_pass = True
        if 0 in filter_buttons_list:
            if d_list["clear"] != 'Yes':
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[0])
        if 1 in filter_buttons_list:
            if d_list["clear"] != 'No':
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[1])
        if 2 in filter_buttons_list:
            all_under = True
            for i_data in d_list["ins_list"]:
                if len(i_data) >= 13:
                    all_under = False
            if all_under:
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[2])
        if 3 in filter_buttons_list:
            all_over = True
            for i_data in d_list["ins_list"]:
                if len(i_data) < 13:
                    all_over = False
            if all_over:
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[3])
        if 4 in filter_buttons_list:
            if d_list["wheelchair"] != 'Yes':
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[4])
        if 5 in filter_buttons_list:
            if d_list["drug"] != 'Yes':
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[5])
        if 6 in filter_buttons_list:
            if d_list["diversity"] != 'Yes':
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[6])
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

def run_clear_filter_test(driver):
    print('TESTING - Filter pop-up - CLEAR FILTER Button:')
    test_clicks = [0,2,4,6]

    filter_clicker(driver,test_clicks,False)

    #check clicks match ordered clicks
    checkboxes = driver.find_elements_by_xpath('//span[@class="MuiIconButton-label"]/input')

    check_i = 0
    all_checked = True
    for c in checkboxes:
        checked_atr = c.get_attribute('checked')
        if check_i in test_clicks:
            if checked_atr != 'true':
                all_checked = False
        #print(checked_atr)
        check_i += 1
    #print(all_checked)

    filter_reset(driver,False,False)

    checkboxes_after = driver.find_elements_by_xpath('//span[@class="MuiIconButton-label"]/input')
    check_i = 0
    none_checked = True
    for c in checkboxes_after:
        checked_atr = c.get_attribute('checked')
        if checked_atr != None:
            none_checked = False
        #print(checked_atr)
        check_i += 1
    #print(none_checked)

    if all_checked and none_checked:
        print('Passed')
    else:
        print('FAILED')


def search_element_by_key(driver,element_key):
    if element_key == NAME_SEARCH_KEY:
        element = driver.find_element_by_xpath('//input[@placeholder="Search by name"]')
    if element_key == COVERAGE_SEARCH_KEY:
        element = driver.find_element_by_xpath('//input[@placeholder="Search by coverage area"]')
    return element

def clear_element_by_key(driver,element_key):
    if element_key == NAME_SEARCH_KEY:
        clear_element = driver.find_element_by_xpath('//input[@placeholder="Search by name"]//ancestor::div[1]/div/button')
    if element_key == COVERAGE_SEARCH_KEY:
        clear_element = driver.find_element_by_xpath('//input[@placeholder="Search by coverage area"]//ancestor::div[1]/div/button')
    return clear_element

def text_to_search(driver,search_text,element_key):
    search_field = search_element_by_key(driver,element_key)
    search_field.send_keys(search_text)
    time.sleep(2)

def search_test(driver,search_list,test_field_key,expected_results=None):
    possibles = len(search_list)
    for to_search in search_list:
        readout = "Searching and testing '" + to_search + "'"
        if expected_results == 1:
            readout += " for EXACT match"
        if expected_results == 0:
            readout += " for NO RESULT"
        print(readout)
        text_to_search(driver,to_search,test_field_key)
        to_search_to_check = to_search.lower()
        results = get_company_data(driver)
        num_results = len(get_company_entries(driver))
        passing_results = 0
        for co in results:
            name = co["name"]
            print(name)
            if expected_results != 0:
                if test_field_key == NAME_SEARCH_KEY:
                    if to_search_to_check in name.lower() or to_search_to_check in co["owner_first"].lower() or to_search_to_check in co["owner_last"].lower():
                        if to_search_to_check in name.lower():
                            print("PASS - Company name")
                        else:
                            print("PASS - Owner name")
                        passing_results += 1
                    else:
                        print("FAIL")
                elif test_field_key == COVERAGE_SEARCH_KEY:
                    if to_search_to_check in co["coverage_area"].lower():
                        print("PASS")
                        passing_results += 1
                    else:
                        print("FAIL")
            else:
                print("Above errant result detected")
                passing_results-=1
        if num_results > 0:
            if expected_results != 0:
                score = (passing_results/num_results)*100.0
                print(str(num_results) + " returned results tested.")
                print(str(score)+ '%' + " contained '"+ to_search + "'")
                if expected_results == 1:
                    if passing_results > 1:
                        print("None exact match - " + str(passing_results) + " results - FAIL")
                    else:
                        print("Exact match single result PASS")
            else:
                print("FAIL - " + str(abs(passing_results)) + " errant results found.")
        else:
            if expected_results != 0:
                print("No results to test.")
            else:
                print("PASS -No search results confirmed.")
        driver.refresh()

def test_clear_search(driver,test_field_key):
    text_to_search(driver,"Test Clear Button",test_field_key)
    search_element = search_element_by_key(driver,test_field_key)
    pre_value = search_element.get_attribute('value')
    #print(pre_value)
    clear_button = clear_element_by_key(driver,test_field_key)
    clear_button.click()
    search_element = search_element_by_key(driver,test_field_key)
    value = search_element.get_attribute('value')
    #print(value)
    if len(pre_value) > 0 and value == "":
        print('Clear Text Button - '+ test_field_key +' - PASSED')


login_tpp(driver)
time.sleep(2)

should_partial = ['bobby','end','rob','be','transp']
#search_test(driver,should_partial,NAME_SEARCH_KEY)
should_full = ['Character Test Incorporated','Endwerpower Inc','Zeepickamazz Direct Corp.']
#search_test(driver,should_full,NAME_SEARCH_KEY,1)
shouldnt = ["zzzz","qqqq","pppp"]
#search_test(driver,shouldnt,NAME_SEARCH_KEY,0)
# TODO add accumulator in test function to measure total passes v fails
should_coverage = ["333","bos"]
#search_test(driver,should_coverage,COVERAGE_SEARCH_KEY)

test_clear_search(driver,COVERAGE_SEARCH_KEY)
test_clear_search(driver,NAME_SEARCH_KEY)

#UNCOMMENT to run individual tests
#run_clear_filter_test(driver)
#run_all_filter_tests(driver)  
# Need to create entries for [1,2,5] / [1,2,6] for testing  
#run_single_filter_test(driver,[1,2,5])
#run_single_filter_test(driver,[3,4])


time.sleep(3)

#driver.close()
driver.quit()