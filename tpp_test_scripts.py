from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, random

PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
## ADJUST ABOVE BASED ON LOCAL INSTALL

FILTER_TAGS = ["Clear to transport","Not clear to transport",\
    "Wheelchair v. available","Has drug testing","Has supplier diversity"]
COVERAGE_SEARCH_KEY = "coverage_tp"
NAME_SEARCH_KEY = "name_tp"

creds = open('creds.txt')
creds_data = creds.readline()
comma = creds_data.find(",")
user = creds_data[:comma]
password = creds_data[comma+1:]
creds.close()

dev_url = 'https://tpp-dev.americanlogistics.com/providers'
qa_url = 'https://tpp-qa.americanlogistics.com/providers'

driver = webdriver.Chrome(PATH)
driver.implicitly_wait(4)

def login_tpp(driver):
    driver.get(dev_url)
    #time.sleep(2)
    button = driver.find_element_by_class_name('MuiButton-containedPrimary')
    button.click()
    time.sleep(3)
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

def scroll_top(driver):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

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

def get_current_company_data(driver):
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
        "ins_list":[ins_data_text[3],ins_data_text[3],ins_data_text[5]],
        "wheelchair":data_text[4],
        "drug":data_text[6],
        "diversity":data_text[7],
        "name":this_co_name,
        "owner_first":l_data_text[47],
        "owner_last":l_data_text[49],
        "coverage_area":l_data_text[97]
    }
    return this_co_data


def get_all_company_data(driver):
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
            """
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
                "ins_list":[ins_data_text[3],ins_data_text[3],ins_data_text[5]],
                "wheelchair":data_text[4],
                "drug":data_text[6],
                "diversity":data_text[7],
                "name":this_co_name,
                "owner_first":l_data_text[47],
                "owner_last":l_data_text[49],
                "coverage_area":l_data_text[93]
            }
            """
            this_co_data = get_current_company_data(driver)
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
    co_data = get_all_company_data(driver)
    num_entries = len(co_data)
    
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
            if d_list["wheelchair"] != 'Yes':
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[2])
        if 3 in filter_buttons_list:
            if d_list["drug"] != 'Yes':
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[3])
        if 4 in filter_buttons_list:
            if d_list["diversity"] != 'Yes':
                this_pass = False
                print(d_list["name"] + " FAILED " + FILTER_TAGS[4])
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
    click_list = [0,1,2,3,4]
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
            if click_list[-1] == 4 and click_list:
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
            if click_list[-1] != 4:
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
    test_clicks = [0,2,4]

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
        results = get_all_company_data(driver)
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
                    print(co["coverage_area"].lower())
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
                print("PASS - No search results confirmed.")
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

def click_entry(driver,index):
    co_entries = get_company_entries(driver)
    company = co_entries[index] 
    company.click()

def test_back_button(driver):
    #this can be made more general
    start_url = driver.current_url
    #print(start_url)
    #Replace with nav to?
    click_entry(driver,0)
    #Replace with nav out?
    buttons2 = driver.find_elements_by_xpath('//a')
    for b in buttons2:
        if b.text == "Back to Transportation Providers":
            b.click()
            break
    end_url = driver.current_url
    #print(end_url)
    if start_url == end_url:
        print('Back to TP button - PASS')
    else:
        print('Back to TP button - FAIL')

def row_counter(driver,render_field_index = 0):
    render_fields = driver.find_elements_by_xpath('//div[@class="MuiDataGrid-renderingZone"]')
    doc_list = render_fields[render_field_index]
    docs = doc_list.find_elements_by_xpath('.//div[@role="row"]')
    return len(docs)

def click_all_date_buttons(driver):
    date_buttons = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root"]')
    for db in date_buttons:
        driver.execute_script("arguments[0].scrollIntoView();", db)
        time.sleep(0.5)
        db.click()
        time.sleep(1)
        dates = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root MuiPickersDay-day"]')
        dates[random.randint(0,len(dates)-1)].click()
        time.sleep(0.5)

def dropdown_handler(driver,id,click_index):
    scroll_top(driver)
    st_dropdown = driver.find_element_by_xpath('//div[@id="'+id+'"]')
    driver.execute_script("arguments[0].scrollIntoView();", st_dropdown)
    st_dropdown.click()
    time.sleep(1)
    st_options = driver.find_elements_by_xpath('//li[@role="option"]')
    st_options[click_index].click()

V_NAME = "aeiou"
C_NAME = ["b","br","cr","ch","g","gr","m","n","l","cl","d","fr","r","s","st","j","p","c"]
E_NAME = ['d','b','bb','ck','rl','g','ll','nd','n','te','hn','tt','se','l']
def get_random_name():
    name = ""
    if random.randint(0,3) == 0:
        name+= V_NAME[random.randint(0,len(V_NAME)-1)]
    name += C_NAME[random.randint(0,len(C_NAME)-1)]
    name += V_NAME[random.randint(0,len(V_NAME)-1)]
    if random.randint(0,6) == 0:
        name += V_NAME[random.randint(0,len(V_NAME)-1)]
    name += E_NAME[random.randint(0,len(E_NAME)-1)]
    if random.randint(0,6) == 0:
        name += V_NAME[random.randint(0,len(V_NAME)-1)]
    if random.randint(0,4) == 0:
        name += 'y'
    return name

DIGITS = '0123456789'
def get_random_number(digits,phone = False):
    number = ''
    if phone:
        number += DIGITS[random.randint(2,len(DIGITS)-1)]
        for i in range(digits-1):
            number+= DIGITS[random.randint(0,len(DIGITS)-1)]
    else:    
        for i in range(digits):
            number+= DIGITS[random.randint(0,len(DIGITS)-1)]
    return number

CHARS = 'abcdefghijklmnopqrstuvwxyz'
def get_random_char(digits):
    chars=""
    for i in range(digits):
        chars += CHARS[random.randint(0,len(DIGITS)-1)]
    return chars

def complete_doc_upload(driver,doc_label):
    doc_type_button = driver.find_element_by_xpath('//label[contains(text(),"Document type")]//ancestor::div[1]')
    doc_type_button.click()
    type_button = driver.find_element_by_xpath('//li[contains(text(),"'+doc_label+'")]')
    # list contains 15 types
    type_button.click()
    date_buttons = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root"]')
    for db in date_buttons:
        db.click()
        dates = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root MuiPickersDay-day"]')
        dates[14].click()
    file_input = driver.find_element_by_xpath('//input[@id="fileUploadButton"]')
    file_input.send_keys("C:\\Users\\drgre\\Tryon\\tpp-admin\\test.pdf")
    save_button = driver.find_element_by_xpath('//span[contains(text(),"Save")]')
    save_button.click()
    time.sleep(3)

def print_inputs(driver):
    inputs = driver.find_elements_by_xpath('//input')
    for i in inputs:
        print(i.get_attribute('name'))

def complete_driver_form(driver):
    click_all_date_buttons(driver)
    first = get_random_name()
    phone = get_random_number(10,True)
    last = get_random_name()
    
    driver.find_element_by_xpath('//input[@name="FirstName"]').send_keys(first)
    driver.find_element_by_xpath('//input[@name="LastName"]').send_keys(last)
    driver.find_element_by_xpath('//input[@name="Email"]').send_keys(first[0]+'_'+last+'@int.com')
    driver.find_element_by_xpath('//input[@name="DriverPhone"]').send_keys(phone)
    driver.find_element_by_xpath('//input[@name="DriversLicenseNumber"]').send_keys(get_random_number(8))
    driver.find_element_by_xpath('//input[@name="EmergencyContactFirstName"]').send_keys(get_random_name())
    driver.find_element_by_xpath('//input[@name="EmergencyContactLastName"]').send_keys(last)
    driver.find_element_by_xpath('//input[@name="EmergencyContactPhone"]').send_keys(phone[0:3]+get_random_number(7))

    dropdown_handler(driver,"mui-component-select-MessagingMethod",2)
    dropdown_handler(driver,"mui-component-select-DriverLicenseIssuedInStateCode",random.randint(0,49))

    save_driver_button = driver.find_element_by_xpath('//span[contains(text(), "Save")]')
    save_driver_button.click()

    time.sleep(1)

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back to Drivers")]')
    back_button.click()

    time.sleep(2)

def complete_vehicle_form(driver):
    click_all_date_buttons(driver)
    driver.find_element_by_xpath('//input[@name="LicensePlate"]').send_keys(get_random_char(3)+get_random_number(3))
    driver.find_element_by_xpath('//input[@name="VehicleVIN"]').send_keys(get_random_char(2)+get_random_number(1)+\
        get_random_char(2)+get_random_number(2)+get_random_char(1)+get_random_number(1)+get_random_char(2)+get_random_number(6))
    driver.find_element_by_xpath('//input[@name="VehicleMake"]').send_keys('Ford')
    driver.find_element_by_xpath('//input[@name="VehicleModel"]').send_keys('Transit 350')
    driver.find_element_by_xpath('//input[@name="VehicleYear"]').send_keys(str(2000+random.randint(0,22)))

    dropdown_handler(driver,"mui-component-select-LicenseStateCode",random.randint(0,49))
    # TODO Waiting on fix -> VehicleTypeID
    dropdown_handler(driver,"mui-component-select-VehicleTypeID",random.randint(0,15))
    dropdown_handler(driver,"mui-component-select-VehicleColorID",random.randint(0,16))

    save_v_button = driver.find_element_by_xpath('//span[contains(text(), "Save")]')
    save_v_button.click()

    time.sleep(1)

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back to Vehicles")]')
    back_button.click()

    time.sleep(2)

def get_document_upload_states(driver):
    states = []
    doc_entries = driver.find_elements_by_xpath('//div[@data-field="DocumentTypeName"]')
    doc_entries = doc_entries[1:]
    print("Checking " + str(len(doc_entries)) + " documents for upload status", end='', flush=True)
    for d in doc_entries:
        print('.', end='', flush=True)
        if len(d.find_elements_by_xpath('.//a[@target="_blank"]')) > 0:
            states.append(None)
        else:
            states.append(d.find_element_by_xpath('.//div').text)
    print('.')
    return states

def view_provider_tests(driver):
    test_back_button(driver)

    #TODO ideally create NEW TP to test
    click_entry(driver,0)

    buttons = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiTab-root MuiTab-textColorPrimary MuiTab-fullWidth"]')
    doc_button = buttons[0]
    doc_button.click()
    time.sleep(2)

    #evaluate doc states
    initial_docs = get_document_upload_states(driver)
    #determine doc to add
    check_index = 0
    for state in initial_docs:
        if state != None:
            break
        check_index += 1

    #add doc
    add_doc_button = driver.find_element_by_xpath('//span[contains(text(), "Add Document")]')
    add_doc_button.click()
    complete_doc_upload(driver,initial_docs[check_index])

    #evaluate do state
    final_docs = get_document_upload_states(driver)
    """
    #Get initial state
    initial_rows = row_counter(driver)
    print(initial_rows)

    #Add doc
    add_doc_button = driver.find_element_by_xpath('//span[contains(text(), "Add Document")]')
    add_doc_button.click()
    complete_doc_upload(driver)

    #get final state
    final_rows = row_counter(driver)
    print(final_rows)
    """
    if final_docs[check_index] == None:
        print("PASS - document successfully added")
    else:
        print("FAIL - document not added")


    ## same for DRIVER ##
    d_initial_rows = row_counter(driver,1)
    print(d_initial_rows)
    add_driver_button = driver.find_element_by_xpath('//span[contains(text(), "Add Driver")]')
    add_driver_button.click()
    #inputs = driver.find_elements_by_xpath('//input')

    complete_driver_form(driver)

    d_final_rows = row_counter(driver,1)
    print(d_final_rows)
    if d_final_rows == d_initial_rows + 1:
        print("PASS - driver successfully added")
    else:
        print("FAIL - driver not added")

    time.sleep(1)

    ## for vehicles ##

    vehicles_button = driver.find_element_by_xpath('//span[contains(text(), "Vehicles")]')
    vehicles_button.click()
    time.sleep(1)

    v_initial_rows = row_counter(driver,1)
    print(v_initial_rows)

    add_vehicles_button = driver.find_element_by_xpath('//span[contains(text(), "Add Vehicle")]')
    add_vehicles_button.click()
    complete_vehicle_form(driver)

    # TODO might require back button click

    time.sleep(1)

    v_final_rows = row_counter(driver,1)
    print(v_final_rows)
    if v_final_rows == v_initial_rows + 1:
        print("PASS - vehicle successfully added")
    else:
        print("FAIL - vehicle not added")

    driver.refresh()

def sort_test(driver,sort_button_path,results_path,sort_forward,text_test=True,attribute=None):
    passed = True
    sort_button = driver.find_element_by_xpath(sort_button_path)
    sort_button.click()
    time.sleep(3)
    results = driver.find_elements_by_xpath(results_path)
    prev = None
    for r in results:
        """
        atts = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', r)
        print(atts)
        """
        if text_test:
            data = r.text.lower()
        else:
            data = r.get_attribute(attribute)
        print(data)
        if prev != None:
            # watch tests for un tested non text attributes
            if sort_forward:
                if data < prev:
                    passed = False
            else:
                if data > prev:
                    passed = False
        prev = data

    if passed:
        print('PASS - sort success')
    else:
        print('FAIL - sorting problem')

def run_all_sort_tests(driver):
    #by co name
    sort_button_path = '//div[contains(text(),"Company name")]'
    results_path = '//div[@data-field="TransportationProviderName"]/a'
    sort_test(driver,sort_button_path,results_path,True)
    sort_test(driver,sort_button_path,results_path,False)

    """
    #email sorting disabled 9/14
    email_sort_path = '//div[contains(text(),"Dispatch email")]'
    email_results_path = '//div[@data-field="EmailAddress"]'

    sort_test(driver,email_sort_path,email_results_path,True)
    sort_test(driver,email_sort_path,email_results_path,False)
    """

    #clear sort
    clear_sort_path = '//div[contains(text(),"Clear to transport")]'
    clear_results_path = '//div[@data-field="IsClearToTransport"]'
    clear_attribute = 'data-value'
    sort_test(driver,clear_sort_path,clear_results_path,True,False,clear_attribute)
    sort_test(driver,clear_sort_path,clear_results_path,False,False,clear_attribute)

    #active sort
    active_sort_path = '//div[contains(text(),"Active")]'
    active_results_path = '//div[@data-field="IsActive"]'
    active_attribute = 'data-value'
    sort_test(driver,active_sort_path,active_results_path,True,False,active_attribute)
    sort_test(driver,active_sort_path,active_results_path,False,False,active_attribute)

def get_target_num_entries(driver):
    dropdown = driver.find_element_by_xpath('//div[@class="MuiSelect-root MuiSelect-select MuiTablePagination-select MuiSelect-selectMenu MuiInputBase-input"]')
    return int(dropdown.text)

def get_reported_start(driver):
    page_readout = driver.find_element_by_xpath('//div[@class="MuiToolbar-root MuiToolbar-regular MuiTablePagination-toolbar MuiToolbar-gutters"]/p[2]').text
    dash_i = page_readout.find('-')
    return int(page_readout[0:dash_i])

def get_reported_end(driver):
    page_readout = driver.find_element_by_xpath('//div[@class="MuiToolbar-root MuiToolbar-regular MuiTablePagination-toolbar MuiToolbar-gutters"]/p[2]').text
    dash_i = page_readout.find('-')
    space_i = page_readout.find(" ")
    return int(page_readout[dash_i+1:space_i])

def evaluate_entries_per_page(driver):
    target_num_entries = get_target_num_entries(driver)
    reported_end = get_reported_end(driver)
    reported_start = get_reported_start(driver)
    reported_num_entries = reported_end-reported_start+1
    actual_num_entries = row_counter(driver)
    if target_num_entries == actual_num_entries:
        print('PASS - requested entries matches actual entries - '+str(actual_num_entries))
    else:
        print('FAIL - requested entries '+str(target_num_entries)+' - actual '+str(actual_num_entries))
    if reported_num_entries == target_num_entries:
        print('PASS - readout shows correct number of rows - '+str(reported_num_entries))
    else:
        print('FAIL - requested entries '+str(target_num_entries)+' - readout shows '+str(reported_num_entries))

def page_entries_test(driver):
    dropdown_guide = [1,2,3,4,5,0]
    for i in dropdown_guide:
        dropdown = driver.find_element_by_xpath('//div[@class="MuiSelect-root MuiSelect-select MuiTablePagination-select MuiSelect-selectMenu MuiInputBase-input"]')
        num_entries_dropdown_id = dropdown.get_attribute('id')
        print(num_entries_dropdown_id)
        #watch this, getting some odd behavior from big entry list loading
        dropdown_handler(driver,num_entries_dropdown_id,i)
        time.sleep(10)
        evaluate_entries_per_page(driver)

def page_change_test(driver,pages_to_test):
    pages = pages_to_test
    page = 0
    while page < pages:
        target_end = get_reported_end(driver) + get_target_num_entries(driver)
        first_entry = driver.find_elements_by_xpath('//div[@data-field="TransportationProviderName"]/a')[0].text

        #get initial stat
        next_button = driver.find_element_by_xpath('//button[@title="Next page"]')
        next_button.click()
        time.sleep(1.5)
        #click
        #check reaout as +rows per page
        new_end = get_reported_end(driver)
        new_first_entry = driver.find_elements_by_xpath('//div[@data-field="TransportationProviderName"]/a')[0].text
        if (new_end == target_end) and (first_entry != new_first_entry):
            print('PASS - goes to next page')
        else:
            print('FAIL - page nav error')
        #then do backwards
        page += 1
    while page > 0:
        target_end = get_reported_end(driver) - get_target_num_entries(driver)
        first_entry = driver.find_elements_by_xpath('//div[@data-field="TransportationProviderName"]/a')[0].text

        #get initial stat
        next_button = driver.find_element_by_xpath('//button[@title="Previous page"]')
        next_button.click()
        time.sleep(4)
        #click
        #check reaout as +rows per page
        new_end = get_reported_end(driver)
        new_first_entry = driver.find_elements_by_xpath('//div[@data-field="TransportationProviderName"]/a')[0].text
        if (new_end == target_end) and (first_entry != new_first_entry):
            print('PASS - goes to previous page')
        else:
            print('FAIL - page nav error')
        #then do backwards
        page -= 1

def complete_create_tp_form(driver,company_name,save = True):
    click_all_date_buttons(driver)
    scroll_top(driver)
    
    first = get_random_name()
    last = get_random_name()
    email_end = '@'+company_name[0]+'tc.com'
    email = last+email_end
    address = str(random.randint(1,12000))+" "+get_random_name()+" st."
    city_seed = get_random_name() + get_random_name()
    city = city_seed + " city"
    state_i = random.randint(0,49)
    zipcode = get_random_number(5)
    county = city_seed
    area_code = get_random_number(3,True)
    driver.find_element_by_xpath('//input[@name="TransportationProviderName"]').send_keys(company_name)
    driver.find_element_by_xpath('//input[@name="EmailAddress"]').send_keys(email)
    driver.find_element_by_xpath('//input[@name="MainContactFirstName"]').send_keys(first)
    driver.find_element_by_xpath('//input[@name="MainContactLastName"]').send_keys(last)
    driver.find_element_by_xpath('//input[@name="AddressLine1"]').send_keys(address)
    #AddressLine2
    driver.find_element_by_xpath('//input[@name="City"]').send_keys(city)
    #State
    dropdown_handler(driver,"mui-component-select-State",state_i)
    driver.find_element_by_xpath('//input[@name="ZipCode"]').send_keys(zipcode)
    driver.find_element_by_xpath('//input[@name="County"]').send_keys(county)
    driver.find_element_by_xpath('//input[@name="MainPhone"]').send_keys(area_code+get_random_number(7))
    #MainPhoneCountryCode
    #MainPhoneExtension
    driver.find_element_by_xpath('//input[@name="DispatchPhone"]').send_keys(area_code+get_random_number(7))
    #DispatchPhoneCountryCode
    #DispatchPhoneExtension
    c_first = get_random_name()
    c_last = get_random_name()
    driver.find_element_by_xpath('//input[@name="BillingContactFirstName"]').send_keys(c_first)
    driver.find_element_by_xpath('//input[@name="BillingContactLastName"]').send_keys(c_last)
    driver.find_element_by_xpath('//input[@name="BillingEmailAddress"]').send_keys(c_last+email_end)
    driver.find_element_by_xpath('//input[@name="BillingAddressLine1"]').send_keys(address)
    #BillingAddressLine2
    driver.find_element_by_xpath('//input[@name="BillingCity"]').send_keys(city)
    #BillingState
    dropdown_handler(driver,"mui-component-select-BillingState",state_i)
    driver.find_element_by_xpath('//input[@name="BillingZipCode"]').send_keys(zipcode)
    driver.find_element_by_xpath('//input[@name="AccountNumber"]').send_keys(get_random_number(8))
    driver.find_element_by_xpath('//input[@name="BillingPhone"]').send_keys(area_code+get_random_number(7))
    #BillingPhoneCountryCode
    #BillingPhoneExtension
    o_first = get_random_name()
    o_last = get_random_name()
    driver.find_element_by_xpath('//input[@name="OwnerFirstName"]').send_keys(o_first)
    driver.find_element_by_xpath('//input[@name="OwnerLastName"]').send_keys(o_last)
    driver.find_element_by_xpath('//input[@name="OwnerEmailAddress"]').send_keys(o_last+email_end)
    driver.find_element_by_xpath('//input[@name="OwnerPhone"]').send_keys(area_code+get_random_number(7))
    #OwnerPhoneCountryCode
    #OwnerPhoneExtension
    driver.find_element_by_xpath('//input[@name="EmployerIdentificationNumber"]').send_keys(get_random_number(9))
    driver.find_element_by_xpath('//input[@name="LegalEntityBusinessName"]').send_keys(email_end[1:4]+" inc.")
    #LegalEntityStateCode
    dropdown_handler(driver,"mui-component-select-LegalEntityStateCode",random.randint(0,49))
    driver.find_element_by_xpath('//input[@name="PhysicalAddressLine1"]').send_keys(address)
    #PhysicalAddressLine2
    driver.find_element_by_xpath('//input[@name="PhysicalCity"]').send_keys(city)
    #PhysicalState
    dropdown_handler(driver,"mui-component-select-PhysicalState",state_i)
    driver.find_element_by_xpath('//input[@name="PhysicalZipCode"]').send_keys(zipcode)


    #LegalEntityTypeID
    dropdown_handler(driver,"mui-component-select-LegalEntityTypeID",random.randint(0,7))
    #LegalEntityStatusID
    dropdown_handler(driver,"mui-component-select-LegalEntityStatusID",1)

    #TransportationProviderTypeID
    dropdown_handler(driver,"mui-component-select-TransportationProviderTypeID",1)
    #TransportationProviderTierID
    dropdown_handler(driver,"mui-component-select-TransportationProviderTierID",1)


    driver.find_element_by_xpath('//input[@name="NPINumber"]').send_keys(get_random_number(6))


    driver.find_element_by_xpath('//input[@name="InsuranceCompanyName"]').send_keys(get_random_name()+'-'+get_random_name()+' insurance')
    driver.find_element_by_xpath('//input[@name="InsurancePolicyNumber"]').send_keys(get_random_char(3) + get_random_number(6))

    #InsuranceStrengthID
    dropdown_handler(driver,"mui-component-select-InsuranceStrengthID",1)

    driver.find_element_by_xpath('//input[@name="InsurancePerPerson"]').send_keys(str(random.randint(1,1000)*10000))
    driver.find_element_by_xpath('//input[@name="InsurancePerAccident"]').send_keys(str(random.randint(1,1000)*10000))
    driver.find_element_by_xpath('//input[@name="InsurancePerProperty"]').send_keys(str(random.randint(1,1000)*10000))

    driver.find_element_by_xpath('//textarea[@rows="10"]').send_keys(city)

    if save:
        save_button = driver.find_element_by_xpath('//span[contains(text(),"Save")]')
        save_button.click()

def test_create_tp(driver):
    add_tp_button = driver.find_element_by_xpath('//span[contains(text(),"Add Provider")]')
    add_tp_button.click()
    co_name = get_random_name() + " transportation co."
    complete_create_tp_form(driver,co_name)
    time.sleep(2)
    still_create = driver.find_elements_by_xpath('//h6')
    if len(still_create) > 0:
        print('FAIL - TP creation errors')
        close_create(driver)
    else:
        back_button = driver.find_element_by_xpath('//a[contains(text(), "Back to Transportation Providers")]')
        back_button.click()

        time.sleep(3)
        results = driver.find_elements_by_xpath('//div[@data-field="TransportationProviderName"]/a')
        if results[0].text == co_name:
            print('PASS - Created new TP - '+results[0].text)
        else:
            print('FAIL - TP not created')

def confirm_errors_message(driver,text_msg = ""):
    time.sleep(0.5)
    optional_return = False
    warnings = driver.find_elements_by_xpath('//div[@class="MuiAlert-message"]')
    if len(warnings)>0 and "There are errors" in warnings[0].text:
        print('PASS - Warning displayed '+text_msg)
        optional_return = True
    else:
        print('FAIL - No warning displayed '+text_msg)
    return optional_return

def test_create_tp_no_data(driver):
    add_tp_button = driver.find_element_by_xpath('//span[contains(text(),"Add Provider")]')
    add_tp_button.click()
    save_button = driver.find_element_by_xpath('//span[contains(text(),"Save")]')
    save_button.click()
    confirm_errors_message(driver)
    close_create(driver)

def test_create_tp_invalid_field(driver):
    add_tp_button = driver.find_element_by_xpath('//span[contains(text(),"Add Provider")]')
    add_tp_button.click()
    co_name = get_random_name() + " transportation co."
    complete_create_tp_form(driver,co_name,False)
    email_field = driver.find_element_by_xpath('//input[@name="EmailAddress"]')
    email_field.send_keys(Keys.CONTROL + "a")
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys(get_random_char(5))
    save_button = driver.find_element_by_xpath('//span[contains(text(),"Save")]')
    save_button.click()
    confirm_errors_message(driver)
    close_create(driver)

def close_create(driver):
    close_button = driver.find_element_by_xpath('//button[@data-testid="close"]')
    close_button.click()
    to_close = driver.find_elements_by_xpath('//p[contains(text(),"close without saving")]')
    if len(to_close) > 0:
        confirm_button = driver.find_element_by_xpath('//span[contains(text(),"Yes")]')
        confirm_button.click()

def test_open_close_create_tp(driver):
    add_tp_button = driver.find_element_by_xpath('//span[contains(text(),"Add Provider")]')
    add_tp_button.click()
    time.sleep(0.5)
    add_page_proof = driver.find_elements_by_xpath('//h6')
    if len(add_page_proof) > 0:
        print('PASS - Add provider page opened')
    else:
        print('FAIL - Add provider not opened')

    close_create(driver)
    add_page_proof = driver.find_elements_by_xpath('//h6')
    if len(add_page_proof) < 1:
        print('PASS - Add provider page closed')
    else:
        print('FAIL - Add provider not closed')


def test_delete_tp(driver):
    #check initial state
    co_to_kill = driver.find_elements_by_xpath('//div[@data-field="TransportationProviderName"]/a')[0].text

    delete_buttons = driver.find_elements_by_xpath('//button[@data-testid="delete"]')
    delete_buttons[0].click()

    no_button = driver.find_element_by_xpath('//span[contains(text(),"No")]')
    no_button.click()

    delete_buttons = driver.find_elements_by_xpath('//button[@data-testid="delete"]')
    delete_buttons[0].click()

    yes_button = driver.find_element_by_xpath('//span[contains(text(),"Yes")]')
    yes_button.click()

    time.sleep(1)
    top_result = driver.find_elements_by_xpath('//div[@data-field="TransportationProviderName"]/a')[0].text
    if top_result != co_to_kill:
        print('PASS - '+co_to_kill+' deleted')
    else:
        print('FAIL - '+ co_to_kill+ ' not deleted')

def open_tp_edit(driver,index):
    click_entry(driver,index)
    time.sleep(2)
    edit_button = driver.find_element_by_xpath('//span[contains(text(),"Edit")]')
    edit_button.click()
    time.sleep(0.5)

def test_edit_tp_open_close(driver):
    open_tp_edit(driver,0)
    add_page_proof = driver.find_elements_by_xpath('//h6')
    if len(add_page_proof) > 0:
        print('PASS - Edit provider page opened')
    else:
        print('FAIL - Edit provider not opened')
    close_create(driver)
    add_page_proof = driver.find_elements_by_xpath('//h6')
    if len(add_page_proof) < 1:
        print('PASS - Edit provider page closed')
    else:
        print('FAIL - Edit provider not closed')
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back to Transportation Providers")]')
    back_button.click()

def test_edit_tp_invalid_field(driver):
    open_tp_edit(driver,0)
    email_field = driver.find_element_by_xpath('//input[@name="EmailAddress"]')
    email_field.send_keys(Keys.CONTROL + "a")
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys(get_random_char(5))
    save_button = driver.find_element_by_xpath('//span[contains(text(),"Save")]')
    save_button.click()
    confirm_errors_message(driver)
    close_create(driver)
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back to Transportation Providers")]')
    back_button.click()

def test_edit_tp(driver):
    open_tp_edit(driver,0)
    new_name = get_random_name()
    field = driver.find_element_by_xpath('//input[@name="OwnerFirstName"]')
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys(get_random_char(5))
    save_button = driver.find_element_by_xpath('//span[contains(text(),"Save")]')
    save_button.click()
    time.sleep(2)
    still_create = driver.find_elements_by_xpath('//h6')
    if len(still_create) > 0:
        print('FAIL - TP edit save errors')
        close_create(driver)
    else:
        co_data = get_current_company_data(driver)
        #test codata v new_name
        if co_data['owner_first'] == new_name:
            print('PASS - Successful TP edit')
        else:
            print('FAIL - TP not edited')

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back to Transportation Providers")]')
    back_button.click()

login_tpp(driver)
time.sleep(5)

#TP EDIT TESTS
test_edit_tp_open_close(driver)
test_edit_tp_invalid_field(driver)
test_edit_tp(driver)

#TP CREATION TESTS
test_create_tp_invalid_field(driver)
test_open_close_create_tp(driver)
test_create_tp_no_data(driver)
test_create_tp(driver)
test_delete_tp(driver)


#UNCOMMENT to run individual tests
#FILTERS
run_clear_filter_test(driver)
#running all filter tests is time consuming
#run_all_filter_tests(driver)  
run_single_filter_test(driver,[1,2,5])
run_single_filter_test(driver,[3,4])

#SEARCHES
should_partial = ['bobby','end','rob','be','transp']
search_test(driver,should_partial,NAME_SEARCH_KEY)
should_full = ['cag transportation co.','ubrol transportation co.','achihn transportation co.']
search_test(driver,should_full,NAME_SEARCH_KEY,1)
shouldnt = ["zzzz","qqqq","pppp"]
search_test(driver,shouldnt,NAME_SEARCH_KEY,0)
# TODO add accumulator in test function to measure total passes v fails
should_coverage = ["city","all of"]
search_test(driver,should_coverage,COVERAGE_SEARCH_KEY)
should_full_coverage = ["ifrisenibb city","All of Orgeon State"]
search_test(driver,should_full_coverage,COVERAGE_SEARCH_KEY)
shouldnt_coverage = ["zzzz","qqqq","pppp"]
search_test(driver,shouldnt_coverage,COVERAGE_SEARCH_KEY,0)

#SEARCH CLEAR
test_clear_search(driver,COVERAGE_SEARCH_KEY)
test_clear_search(driver,NAME_SEARCH_KEY)

#TODO create new TP first, test that tp, delete that tp
view_provider_tests(driver)

run_all_sort_tests(driver)

page_entries_test(driver)
page_change_test(driver,3)

time.sleep(3)

driver.close()


driver.quit()