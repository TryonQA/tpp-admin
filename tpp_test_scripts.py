from os import pipe
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time, random
import datetime
import requests

PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
## ADJUST ABOVE BASED ON LOCAL INSTALL

FILTER_TAGS = ["Clear to transport","Not clear to transport","Active","Not Active",\
    "Wheelchair v. available","Has drug testing","Has supplier diversity"]
REAL_VEHICLES = [("Ford","Transit 350"),("Dodge","Grand Caravan"),("Honda","Accord"),\
    ("Ford","F-150"),("GMC","Yukon"),("Toyota","Yaris")]
COVERAGE_SEARCH_KEY = "coverage_tp"
NAME_SEARCH_KEY = "name_tp"
DRIVER_SEARCH_KEY = "driver_tp"
VEHICLE_SEARCH_KEY = 'vehicle_tp'

TP_KEY = 'tp_key'
DRIVER_KEY = 'driver_key'
VEHICLE_KEY = 'vehicle_key'

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

dev_url = 'https://tpp-dev.americanlogistics.com/providers'
qa_url = 'https://tpp-qa.americanlogistics.com/providers'
uat_url = 'https://tpp-uat.americanlogistics.com/providers'
### ADJUST HERE to change environment being tested ###
active_url = qa_url

def get_qa_tag():
    return str(datetime.datetime.now()) + " tryon-qa-gb"

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--ignore-certificate-error")
    options.add_argument("--ignore-ssl-errors")
    driver = webdriver.Chrome(PATH, options=options)
    
    driver.implicitly_wait(4)
    return driver

def login_tpp(driver,url=active_url,login_key="admin"):
    ""
    if login_key == "admin":
        u = user
        p = password
    if login_key == "accounting":
        u = acc_user
        p = acc_password
    if login_key == "read_only":
        u = ro_user
        p = ro_password
    ""
    ""
    if url == dev_url:
        u = "dev" + u
    if url == qa_url:
        u = "qa" + u
    if url == uat_url:
        u = "uat" + u
    ""
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
    """
    uname = driver.find_element_by_id('i0116')
    uname.send_keys(u)

    u_button = driver.find_element_by_id('idSIButton9')
    u_button.click()
    time.sleep(2)

    pwd = driver.find_element_by_id('i0118')
    pwd.send_keys(p)

    p_button = driver.find_element_by_id('idSIButton9')
    p_button.click()
    time.sleep(2)

    if len(driver.find_elements_by_xpath('//div[@class="row text-title"]')) > 0:
        if driver.find_element_by_xpath('//div[@class="row text-title"]').text == "Stay signed in?":
            c_button = driver.find_element_by_id('idSIButton9')
            c_button.click()
    """


def scroll_top(driver):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    time.sleep(1)

def open_filters_menu(driver):
    #driver.refresh()
    
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
    f_knob = driver.find_element_by_xpath('//ul[@aria-labelledby="filter-label"]')
    try:
        action = webdriver.common.action_chains.ActionChains(driver)
        offset = -4
        action.move_to_element_with_offset(f_knob, 0, offset)
        action.click()
        action.perform()
    except:
        action = webdriver.common.action_chains.ActionChains(driver)
        offset = -2
        action.move_to_element_with_offset(f_knob, 0, offset)
        action.click()
        action.perform()

def close_hamburger(driver):
    f_knob = driver.find_element_by_xpath('//ul[@role="menu"]')
    try:
        action = webdriver.common.action_chains.ActionChains(driver)
        offset = -4
        action.move_to_element_with_offset(f_knob, 0, offset)
        action.click()
        action.perform()
    except:
        action = webdriver.common.action_chains.ActionChains(driver)
        offset = -2
        action.move_to_element_with_offset(f_knob, 0, offset)
        action.click()
        action.perform()

    

def get_company_entries(driver):
    companies:list = driver.find_elements_by_xpath('//a[@href="#"]')
    to_remove = None
    for c in companies:
        if c.text == "FAQ page":
            to_remove = c
    if c !=None:
        companies.remove(to_remove)
    return companies

def get_random_vin():
    res = requests.get("https://randomvin.com/getvin.php?type=fake")
    vin = res.text
    return vin

def get_random_dl(state):
    res = requests.get("https://gbtryonsoft.pythonanywhere.com/dl/?state="+state)
    dl = res.text
    return dl




def filter_clicker(driver,filter_buttons_list,close=True):
    #filter buttons indexed 0-6
    time.sleep(0.5)
    open_filters_menu(driver)
    time.sleep(0.5)
    filters = driver.find_elements_by_xpath('//span[@class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary css-yb0lig"]')
    #print(len(filters))
    for index in filter_buttons_list:
        filters[index].click()
    if close:
        close_filters_menu(driver)

def filter_reset(driver,open=True,close=True):
    if open:
        open_filters_menu(driver)
    clear_button = driver.find_element_by_xpath('//button[contains(text(),"Clear Filter")]')
    clear_button.click()
    if close:
        close_filters_menu(driver)

def get_all_vehicle_data(driver):
    time.sleep(2)
    co_entries_orig = get_company_entries(driver)
    num_entries = len(co_entries_orig)
    v_data = []
    i = 0
    # get co data
    while i < num_entries:
        co_entries = get_company_entries(driver)
        num_entries = len(co_entries)
        if i < len(co_entries):
            #print("checking vehicle: " + str(i+1) + " / " + str(num_entries))
            company = co_entries[i]
            driver.execute_script("arguments[0].scrollIntoView();", company) 
            company.click()
            time.sleep(2)
            this_v_data = get_current_vehicle_data(driver)
            v_data.append(this_v_data)
            i+=1
            back_to_vehicles(driver)
            time.sleep(1)
    return v_data

def get_current_driver_data(driver):
    datas = driver.find_elements_by_xpath('//div[@class="MuiTypography-root MuiTypography-body1 LabelValue-value css-9l3uo3"]')
    data_text = []
    test = 0
    for pt in datas:
        print(str(test)+" - "+pt.text)
        data_text.append(pt.text)
        test+=1
    this_d_data = {
        "FirstName":data_text[0],
        "LastName":data_text[2],
        "IsClearToTransport": parse_yes_no(data_text[17]),
    }
    return this_d_data

def provider_link_test(driver):
    link = driver.find_element_by_xpath('//a[@class="MuiTypography-root MuiTypography-inherit MuiLink-root MuiLink-underlineHover LabelLink-link css-1tltjjo"]')
    orig_provider = link.text
    link.click()
    time.sleep(1.5)
    data = get_current_company_data(driver)
    if data["TransportationProviderName"] == orig_provider:
        print("PASS - Active link to "+orig_provider)
    else:
        print("FAIL - " + orig_provider + " unreached.")
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()
    



def get_current_vehicle_data(driver):
    datas = driver.find_elements_by_xpath('//div[@class="MuiTypography-root MuiTypography-body1 LabelValue-value css-9l3uo3"]')
    data_text = []
    test = 0
    for pt in datas:
        #print(str(test)+" - "+pt.text)
        data_text.append(pt.text)
        test+=1
    this_v_data = {
        "make":data_text[0],
        "model":data_text[1],
        "year":data_text[2],
        "vin":data_text[7],
        "license":data_text[5],
        "state":data_text[6],
        "IsClearToTransport": parse_yes_no(data_text[-1]),
    }
    return this_v_data


def get_current_company_data(driver):
    if len(driver.find_elements_by_xpath('//button[contains(text(),"nfo")]')) > 0:
        ti_button = driver.find_element_by_xpath('//button[contains(text(),"nfo")]')
        ti_button.click()
    legal_data = driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-isbt42"]/div/div/div/div')
    l_data_text = []
    test = 0
    for ld_pt in legal_data:
        #print(str(test)+" - "+ld_pt.text)
        l_data_text.append(ld_pt.text)
        test+=1
    """
    data = driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-sm-12 MuiGrid-grid-md-6 MuiGrid-grid-lg-3"]/div/div/div[2]')
    data_text = []
    for d_pt in data:
        #print(d_pt.text)
        data_text.append(d_pt.text)
    """
    #buttons = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiTab-root MuiTab-textColorPrimary MuiTab-fullWidth"]')
    ins_button = driver.find_element_by_xpath('//button[contains(text(),"Insurance")]')
    ins_button.click()
    ins_data = driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-isbt42"]/div/div/div/div')
    ins_data_text = []
    i_test = 0
    for i_pt in ins_data:
        #print("ins-"+str(i_test)+" - "+i_pt.text)
        ins_data_text.append(i_pt.text)
        i_test += 1
    #this_co_data = [data_text[5],[ins_data_text[6],ins_data_text[7],ins_data_text[8]],data_text[4],data_text[6],data_text[7],this_co_name]
    """
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
    """

    this_co_data = {
        "TransportationProviderName":l_data_text[1],
        "EmailAddress":l_data_text[3],
        "MainContactFirstName":l_data_text[5],
        "MainContactLastName":l_data_text[7],
        "AddressLine1":l_data_text[9],
        "City":l_data_text[13],
        "ZipCode":l_data_text[17],
        "County":l_data_text[19],
        "MainPhone":strip_non_numeric(l_data_text[21])[1:],
        "DispatchPhone":strip_non_numeric(l_data_text[25])[1:],
        "MessagingMethod":l_data_text[29],
        "BillingContactFirstName":l_data_text[31],
        "BillingContactLastName":l_data_text[33],
        "BillingEmailAddress":l_data_text[45],
        "BillingAddressLine1":l_data_text[35],
        "BillingCity":l_data_text[39],
        "BillingZipCode":l_data_text[43],
        #"AccountNumber":l_data_text[87],
        "BillingPhone":strip_non_numeric(l_data_text[47])[1:],
        "OwnerFirstName":l_data_text[59],
        "OwnerLastName":l_data_text[61],
        "OwnerEmailAddress":l_data_text[63],
        "OwnerPhone":strip_non_numeric(l_data_text[65])[1:],
        "EmployerIdentificationNumber":l_data_text[55],
        "LegalEntityBusinessName":l_data_text[57],
        "PhysicalAddressLine1":l_data_text[75],
        "PhysicalCity":l_data_text[79],
        "PhysicalZipCode":l_data_text[83],
        "NPINumber":l_data_text[97],
        "CommercialInsuranceCompanyName":ins_data_text[85],
        "CommercialInsurancePolicyNumber":ins_data_text[87],
        "CommercialAggregateAmount":strip_non_numeric(ins_data_text[93])[:-2],
        "AutoInsuranceCompanyName":ins_data_text[95],
        "AutoInsurancePolicyNumber":ins_data_text[97],
        "AutoBodilyInjuryPerson":strip_non_numeric(ins_data_text[103])[:-2],
        "AutoBodilyInjuryAccident":strip_non_numeric(ins_data_text[105])[:-2],
        "AutoPropertyDamage":strip_non_numeric(ins_data_text[107])[:-2],
        "AutoCombinedLimit":strip_non_numeric(ins_data_text[109])[:-2],
        "CoverageAreas":l_data_text[101],
        
        #dropdowns
        "State": l_data_text[15],
        "BillingState": l_data_text[41],
        "LegalEntityStateCode": l_data_text[69],
        "PhysicalState": l_data_text[81],
        "LegalEntityTypeID": l_data_text[71],
        "LegalEntityStatusID": l_data_text[73],
        "TransportationProviderTypeID": l_data_text[85],
        #"TransportationProviderTierID": l_data_text[89],
        "CommercialInsuranceStrengthID": ins_data_text[91],
        "AutoInsuranceStrengthID": ins_data_text[101],
        
        #ADD BANK TODO
        "BankName": l_data_text[49],
        "BankAccountNumber": l_data_text[53],
        "BankRoutingNumber": l_data_text[51],

        #checkboxes
        #"HasReceivedProviderManual": parse_yes_no(l_data_text[91]),
        "HasWheelchairVehiclesAvailable": parse_yes_no(l_data_text[91]),
        #"HasReceivedNEMTProviderManual": parse_yes_no(l_data_text[105]),
        #"HasSupplierDiversity": parse_yes_no(l_data_text[101]),
        #"HasRegulatedDrugTesting": parse_yes_no(l_data_text[99]),
        "IsClearToTransport": parse_yes_no(l_data_text[93]),
        "IsActive": parse_yes_no(l_data_text[95]),
        #"IsCompliant": parse_yes_no(l_data_text[107]),
        "HasWorkersComp": ""
    }
    
    return this_co_data

def get_comm_auto_exp(driver):
    click_insurance(driver)
    ins_data = driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-sm-12 MuiGrid-grid-md-6 MuiGrid-grid-lg-3"]/div/div/div[2]')
    ins_data_text = []
    i_test = 0
    for i_pt in ins_data:
        #print("ins-"+str(i_test)+" - "+i_pt.text)
        ins_data_text.append(i_pt.text)
        i_test += 1
    exp_date = ins_data_text[7]
    return exp_date
    
def get_ctt(driver):
    legal_data = driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2"]/div/div/div/div')
    l_data_text = []
    test = 0
    for ld_pt in legal_data:
        #print(str(test)+" - "+ld_pt.text)
        l_data_text.append(ld_pt.text)
        test+=1
    return l_data_text[91]

def get_active(driver):
    legal_data = driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2"]/div/div/div/div')
    l_data_text = []
    test = 0
    for ld_pt in legal_data:
        #print(str(test)+" - "+ld_pt.text)
        l_data_text.append(ld_pt.text)
        test+=1
    return l_data_text[97]

def strip_non_numeric(string_to_format):
    finished = ""
    for char in string_to_format:
        if char.isnumeric():
            finished+=char
    return finished

def parse_yes_no(text_y_n):
    if text_y_n == "No" or text_y_n == "Inactive":
        return False
    elif text_y_n == "Yes" or text_y_n == "Active":
        return True
    else:
        return None

def get_all_company_data(driver):
    time.sleep(2)
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
            driver.execute_script("arguments[0].scrollIntoView();", company) 
            company.click()
            time.sleep(2)
            this_co_data = get_current_company_data(driver)
            co_data.append(this_co_data)
            i+=1
            buttons2 = driver.find_elements_by_xpath('//a')
            for b in buttons2:
                if b.text == "Back":
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
            if d_list["IsClearToTransport"] != True:
                this_pass = False
                print(d_list["TransportationProviderName"] + " FAILED " + FILTER_TAGS[0])
        if 1 in filter_buttons_list:
            if d_list["IsClearToTransport"] != False:
                this_pass = False
                print(d_list["TransportationProviderName"] + " FAILED " + FILTER_TAGS[1])
        #new activeFilter
        if 2 in filter_buttons_list:
            if d_list["IsActive"] != True:
                this_pass = False
                print(d_list["TransportationProviderName"] + " FAILED " + FILTER_TAGS[0])
        if 3 in filter_buttons_list:
            if d_list["IsActive"] != False:
                this_pass = False
                print(d_list["TransportationProviderName"] + " FAILED " + FILTER_TAGS[1])
        if 4 in filter_buttons_list:
            if d_list["HasWheelchairVehiclesAvailable"] != True:
                this_pass = False
                print(d_list["TransportationProviderName"] + " FAILED " + FILTER_TAGS[2])
        if 5 in filter_buttons_list:
            if d_list["HasRegulatedDrugTesting"] != True:
                this_pass = False
                print(d_list["TransportationProviderName"] + " FAILED " + FILTER_TAGS[3])
        if 6 in filter_buttons_list:
            if d_list["HasSupplierDiversity"] != True:
                this_pass = False
                print(d_list["TransportationProviderName"] + " FAILED " + FILTER_TAGS[4])
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
    #filter_reset(driver)
    driver.refresh()
    time.sleep(5)

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
    
    close_filters_menu(driver)


def search_element_by_key(driver,element_key):
    time.sleep(0.5)
    if element_key == NAME_SEARCH_KEY:
        element = driver.find_element_by_xpath('//input[@placeholder="Search for provider"]')
    if element_key == COVERAGE_SEARCH_KEY:
        element = driver.find_element_by_xpath('//input[@placeholder="Search for provider"]')
    if element_key == DRIVER_SEARCH_KEY:
        element = driver.find_element_by_xpath('//input[@placeholder="Search for a Driver"]')
    if element_key == VEHICLE_SEARCH_KEY:
        element = driver.find_element_by_xpath('//input[@placeholder="Search for a Vehicle"]')

    return element

def clear_element_by_key(driver,element_key):
    if element_key == NAME_SEARCH_KEY:
        clear_element = driver.find_element_by_xpath('//input[@placeholder="Search for provider"]//ancestor::div[1]/div/button')
    if element_key == COVERAGE_SEARCH_KEY:
        clear_element = driver.find_element_by_xpath('//input[@placeholder="Search for provider"]//ancestor::div[1]/div/button')
    if element_key == DRIVER_SEARCH_KEY:
        clear_element = driver.find_element_by_xpath('//input[@placeholder="Search for a Driver"]//ancestor::div[1]/div/button')
    if element_key == VEHICLE_SEARCH_KEY:
        clear_element = driver.find_element_by_xpath('//input[@placeholder="Search for a Vehicle"]//ancestor::div[1]/div/button')
    
    return clear_element

def simulate_typing_search(driver,to_search,search_key,time_per_char = 0.16):
    end = 1
    down = False
    for r in range(len(to_search)):
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
        time.sleep(time_per_char)
        text_to_search(driver,current_search,search_key,False)

def text_to_search(driver,search_text,element_key,pause = True):
    search_field = search_element_by_key(driver,element_key)
    search_field.send_keys(Keys.CONTROL + 'a')
    search_field.send_keys(search_text)
    if pause:
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
        simulate_typing_search(driver,to_search,test_field_key)
        to_search_to_check = to_search.lower()
        time.sleep(5)
        if test_field_key == NAME_SEARCH_KEY or test_field_key == COVERAGE_SEARCH_KEY:
            results = get_all_company_data(driver)
            num_results = len(get_company_entries(driver))
        elif test_field_key == DRIVER_SEARCH_KEY:
            results = get_all_driver_names(driver)
            num_results = len(results)
        elif test_field_key == VEHICLE_SEARCH_KEY:
            results = get_all_vehicle_data(driver)
            num_results = len(results)

        passing_results = 0
        for res in results:
            if test_field_key == NAME_SEARCH_KEY or test_field_key == COVERAGE_SEARCH_KEY:
                name = res["TransportationProviderName"]
                print(name)
            else:
                print(res)
            if expected_results != 0:
                if test_field_key == NAME_SEARCH_KEY or test_field_key == COVERAGE_SEARCH_KEY:
                    if to_search_to_check in name.lower() or to_search_to_check in res["OwnerFirstName"].lower() or to_search_to_check in res["CoverageAreas"].lower() or\
                        to_search_to_check in res["OwnerLastName"].lower() or to_search_to_check in res["LegalEntityBusinessName"].lower() or to_search_to_check in res["EmailAddress"].lower():
                        if to_search_to_check in name.lower():
                            print("PASS - Company name")
                        else:
                            print("PASS - Other Co. info")
                        passing_results += 1
                    else:
                        print("FAIL company search")
                elif test_field_key == DRIVER_SEARCH_KEY:
                    if to_search_to_check in res.lower():
                        print('PASS driver search')
                        passing_results += 1
                    else:
                        print('FAIL driver search')
                elif test_field_key == VEHICLE_SEARCH_KEY:
                    res_to_text = (res["make"]+res["model"]+res["year"]+res["vin"]+res["license"]+res["state"]).lower()
                    if to_search_to_check in res_to_text:
                        if to_search_to_check in res["make"].lower():
                            print('PASS vehicle search MAKE')
                        if to_search_to_check in res["model"].lower():
                            print('PASS vehicle search MODEL')
                        if to_search_to_check in res["year"].lower():
                            print('PASS vehicle search YEAR')
                        if to_search_to_check in res["vin"].lower():
                            print('PASS vehicle search VIN NUM.')
                        if to_search_to_check in res["license"].lower():
                            print('PASS vehicle search LIC. NUM.')
                        if to_search_to_check in res["state"].lower():
                            print('PASS vehicle search STATE')
                        passing_results += 1
                    else:
                        print("FAIL vehicle search")
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
        time.sleep(1)
        if test_field_key == DRIVER_SEARCH_KEY:
            go_to_drivers(driver)
            time.sleep(1)
        if test_field_key == VEHICLE_SEARCH_KEY:
            go_to_vehicles(driver)
            time.sleep(1)

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
    driver.execute_script("arguments[0].scrollIntoView();", company) 
    company.click()

def click_driver(driver,index):
    drivers = driver.find_elements_by_xpath('//div[@role="row"]/div/a')
    this_driver = drivers[index]
    this_driver.click()

def click_vehicle(driver,index):
    vehicles = driver.find_elements_by_xpath('//div[@role="row"]/div/a')
    this_v = vehicles[index]
    this_v.click()

def test_back_button(driver,page_key):
    #this can be made more general
    start_url = driver.current_url
    #print(start_url)
    #Replace with nav to?
    if page_key == TP_KEY:
        click_entry(driver,0)
        back_string = 'Transportation Providers'
    elif page_key == DRIVER_KEY:
        click_driver(driver,0)
        back_string = 'Drivers'
    elif page_key == VEHICLE_KEY:
        click_driver(driver,0)
        back_string = "Vehicles"
    time.sleep(0.5)
    mid_url = driver.current_url
    
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()
    time.sleep(0.5)
    end_url = driver.current_url
    #print(end_url)
    if start_url == end_url and mid_url != start_url:
        print('Back to '+back_string+' button - PASS')
    else:
        print('Back to '+back_string+' button - FAIL')

def get_driver_ctt_active_tuples(driver,render_field_index = 0):
    render_fields = driver.find_elements_by_xpath('//div[@class="MuiDataGrid-virtualScrollerRenderZone css-1inm7gi"]')
    doc_list = render_fields[render_field_index]
    docs = doc_list.find_elements_by_xpath('.//div[@role="row"]')

    driver_tups = []

    for d in docs:
        ctt_status = False
        active_status = False

        ctt_flag = d.find_element_by_xpath('.//div[@data-field="IsClearToTransport"]/div[1]/*[local-name() = "svg"]')
        ctt_flag_status = ctt_flag.get_attribute("class")
        if 'alert' not in ctt_flag_status:
            ctt_status = True

        active_flag = d.find_element_by_xpath('.//div[@data-field="IsActive"]/div[1]/*[local-name() = "svg"]')
        active_flag_status = active_flag.get_attribute("class")
        if 'alert' not in active_flag_status:
            active_status = True
        this_d_tup = (ctt_status,active_status)
        driver_tups.append(this_d_tup)

    return driver_tups


def row_counter(driver,render_field_index = 0):
    render_fields = driver.find_elements_by_xpath('//div[@class="MuiDataGrid-virtualScrollerRenderZone css-1inm7gi"]')
    doc_list = render_fields[render_field_index]
    docs = doc_list.find_elements_by_xpath('.//div[@role="row"]')
    return len(docs)

def blank_driver_dates(driver):
    time.sleep(1)
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()
    time.sleep(1)

    blank_dates(driver)

    time.sleep(1)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(1)    

def blank_dates(driver):
    dates = driver.find_elements_by_xpath('//input[@placeholder="mm/dd/yyyy"]')
    for field in dates:
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
    

def click_all_date_buttons(driver,nextMonth = False):
    date_buttons = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root MuiIconButton-edgeEnd MuiIconButton-sizeMedium css-slyssw"]')
    for db in date_buttons:
        driver.execute_script("arguments[0].scrollIntoView();", db)
        time.sleep(0.5)
        db.click()
        time.sleep(1)
        if nextMonth:
            next_month = driver.find_element_by_xpath('//button[@title="Next month"]')
            #print(next_month.get_attribute('disabled'))
            if next_month.get_attribute('disabled') == 'true':
                prev_month = driver.find_element_by_xpath('//button[@title="Previous month"]')
                prev_month.click()
                time.sleep(1.5)
            else:
                next_month.click()
                time.sleep(1.5)
                
        dates = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiPickersDay-root MuiPickersDay-dayWithMargin css-2rgxex"]')
        dates[random.randint(0,len(dates)-2)].click()
        time.sleep(0.5)

def dropdown_handler(driver,id,click_index,override_xpath = None):
    tries = 3
    scroll_top(driver)
    if override_xpath == None:
        xpath = '//input[@name="'+id+'"]//ancestor::div[1]/div'
    else:
        xpath = override_xpath
    st_dropdown = driver.find_element_by_xpath(xpath)
    driver.execute_script("arguments[0].scrollIntoView();", st_dropdown)
    time.sleep(1)
    st_dropdown.click()
    time.sleep(1)
    while tries > 0:
        st_options = driver.find_elements_by_xpath('//li[@role="option"]')
        if click_index < len(st_options):
            st_options[click_index].click()
            tries = -1
        else:
            time.sleep(2)
            tries -=1
            if tries == 0:
                print("Dropdown Handler failed")

def dropdown_scraper(driver,id,click_index,attribute=None):
    scroll_top(driver)
    st_dropdown = driver.find_element_by_xpath('//input[@name="'+id+'"]//ancestor::div[1]/div')
    driver.execute_script("arguments[0].scrollIntoView();", st_dropdown)
    st_dropdown.click()
    time.sleep(1)
    st_options = driver.find_elements_by_xpath('//li[@role="option"]')
    if attribute == None:
        return_v = st_options[click_index].text
    else:
        return_v = st_options[click_index].get_attribute(attribute)
    f_knob = driver.find_element_by_xpath('//ul[@role="listbox"]//ancestor::div[1]')
    action = webdriver.common.action_chains.ActionChains(driver)
    action.move_to_element_with_offset(f_knob, -5, 0)
    action.click()
    action.perform()
    return return_v

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
    if doc_label != None:
        doc_type_button = driver.find_element_by_xpath('//label[contains(text(),"Document type")]//ancestor::div[1]')
        doc_type_button.click()
        type_button = driver.find_element_by_xpath('//li[contains(text(),"'+doc_label+'")]')
        # list contains 15 types
        driver.execute_script("arguments[0].scrollIntoView();", type_button)
        time.sleep(0.5)
        type_button.click()
    else:
        add_button = driver.find_element_by_xpath('//button[contains(text(),"Add Document")]')
        add_button.click()

    date_buttons = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiIconButton-root MuiIconButton-edgeEnd MuiIconButton-sizeMedium css-slyssw"]')
    for db in date_buttons:
        db.click()
        if db == date_buttons[2]:
            time.sleep(0.5)
            next_month = driver.find_element_by_xpath('//button[@aria-label="Next month"]')
            next_month.click()
        else:
            time.sleep(0.5)
            pre_month = driver.find_element_by_xpath('//button[@aria-label="Previous month"]')
            pre_month.click()
        time.sleep(1.5)
        dates = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiPickersDay-root MuiPickersDay-dayWithMargin css-2rgxex"]')
        dates[14].click()
        time.sleep(1)
    file_input = driver.find_element_by_xpath('//input[@id="fileUploadButton"]')
    file_input.send_keys("C:\\Users\\drgre\\Tryon\\tpp-admin\\test.pdf")
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(3)

def print_inputs(driver):
    inputs = driver.find_elements_by_xpath('//input')
    for i in inputs:
        print(i.get_attribute('name'))

def complete_driver_form(driver,is_active = True):
    click_all_date_buttons(driver,True)
    first = get_qa_tag()
    phone = get_random_number(10,True)
    last = get_random_name()
    
    driver.find_element_by_xpath('//input[@name="FirstName"]').send_keys(first)
    driver.find_element_by_xpath('//input[@name="LastName"]').send_keys(last)
    driver.find_element_by_xpath('//input[@name="Email"]').send_keys(first[0]+'_'+last+'@int.com')
    driver.find_element_by_xpath('//input[@name="DriverPhone"]').send_keys(phone)
    #driver.find_element_by_xpath('//input[@name="DriversLicenseNumber"]').send_keys(get_random_number(8))
    driver.find_element_by_xpath('//input[@name="EmergencyContactFirstName"]').send_keys(get_random_name())
    driver.find_element_by_xpath('//input[@name="EmergencyContactLastName"]').send_keys(last)
    driver.find_element_by_xpath('//input[@name="EmergencyContactPhone"]').send_keys(phone[0:3]+get_random_number(7))

    dropdown_handler(driver,"MessagingMethod",2)
    state_index = random.randint(0,49)
    dropdown_handler(driver,"DriverLicenseIssuedInStateCode",state_index)
    state = dropdown_scraper(driver,"DriverLicenseIssuedInStateCode",state_index)
    #print(state)
    driver.find_element_by_xpath('//input[@name="DriversLicenseNumber"]').send_keys(get_random_dl(state))

    if is_active:
        driver.find_element_by_xpath('//span[contains(text(), "Active")]//ancestor::label[1]/span/input').click()

    save_driver_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_driver_button.click()

    time.sleep(3)

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

    time.sleep(2)

def back_to_providers(driver):
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def back_to_vehicles(driver):
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def back_to_drivers(driver):
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def complete_vehicle_form(driver):
    vin = get_random_vin()
    click_all_date_buttons(driver)
    driver.find_element_by_xpath('//input[@name="LicensePlate"]').send_keys(get_random_char(3)+get_random_number(3))
    driver.find_element_by_xpath('//input[@name="VehicleVIN"]').send_keys(vin)
    makeModel = REAL_VEHICLES[random.randint(0,len(REAL_VEHICLES)-1)]
    make = makeModel[0]
    model = 'tryon-qa-gb'
    driver.find_element_by_xpath('//input[@name="VehicleMake"]').send_keys(make)
    driver.find_element_by_xpath('//input[@name="VehicleModel"]').send_keys(model)
    driver.find_element_by_xpath('//input[@name="VehicleYear"]').send_keys(str(2000+random.randint(0,22)))

    dropdown_handler(driver,"LicenseStateCode",random.randint(0,49))
    # TODO Waiting on fix -> VehicleTypeID
    dropdown_handler(driver,"VehicleTypeID",random.randint(0,13))
    dropdown_handler(driver,"VehicleColorID",random.randint(0,15))

    driver.find_element_by_xpath('//span[contains(text(), "Active")]//ancestor::label[1]/span/input').click()

    save_v_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_v_button.click()

    time.sleep(2)

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

    time.sleep(2)

def get_document_upload_states(driver):
    driver.implicitly_wait(0.5)
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
        doc_entries = driver.find_elements_by_xpath('//div[@data-field="DocumentTypeName"]')
        doc_entries = doc_entries[1:]
    print('.')
    driver.implicitly_wait(4)
    return states

def upload_all_docs(driver):
    initial_docs = get_document_upload_states(driver)
    print(initial_docs)

    up_index = 0
    for state in initial_docs:
        if state != None:
            add_doc_button = driver.find_element_by_xpath('//button[contains(text(),"Add Document")]')
            add_doc_button.click()
            complete_doc_upload(driver,initial_docs[up_index])
        up_index +=1

def click_insurance(driver):
    if len(driver.find_elements_by_xpath('//button[contains(text(),"Insurance")]')) > 0:
        doc_button = driver.find_element_by_xpath('//button[contains(text(),"Insurance")]')
        doc_button.click()
        time.sleep(1)

def click_documents(driver):
    if len(driver.find_elements_by_xpath('//button[contains(text(),"Documents")]')) > 0:
        doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
        doc_button.click()
        time.sleep(1)

def test_doc_upload(driver):
    scroll_top(driver)
    if len(driver.find_elements_by_xpath('//button[contains(text(),"Documents")]')) > 0:
        doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
        doc_button.click()
        time.sleep(1)
    initial_docs = get_document_upload_states(driver)
    #determine doc to add
    check_index = 0
    if len(initial_docs)>0:
        for state in initial_docs:
            if state != None:
                break
            check_index += 1
        #add doc
        add_doc_button = driver.find_element_by_xpath('//button[contains(text(),"Add Document")]')
        add_doc_button.click()
        complete_doc_upload(driver,initial_docs[check_index])
        time.sleep(1)
    else:
        complete_doc_upload(driver,None)
    #evaluate doc state
    time.sleep(2)
    final_docs = get_document_upload_states(driver)

    if final_docs[check_index] == None:
        print("PASS - document successfully added")
    else:
        print("FAIL - document not added")


def view_provider_tests(driver):
    time.sleep(4)
    test_back_button(driver,TP_KEY)

    #TODO ideally create NEW TP to test
    click_entry(driver,0)
    doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
    doc_button.click()
    time.sleep(2)

    ## same for DRIVER ##
    d_initial_rows = row_counter(driver,1)
    print(d_initial_rows)
    add_driver_button = driver.find_element_by_xpath('//button[contains(text(),"Add Driver")]')
    driver.execute_script("arguments[0].scrollIntoView();", add_driver_button)
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

    vehicles_button = driver.find_element_by_xpath('//button[contains(text(), "Vehicles")]')
    driver.execute_script("arguments[0].scrollIntoView();", vehicles_button)
    driver.execute_script("window.scrollTo(0,50);")
    time.sleep(1)
    vehicles_button.click()
    time.sleep(1)

    v_initial_rows = row_counter(driver,1)
    print(v_initial_rows)

    add_vehicles_button = driver.find_element_by_xpath('//button[contains(text(),"Add Vehicle")]')
    driver.execute_script("arguments[0].scrollIntoView();", add_vehicles_button)
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


    test_doc_upload(driver)
    test_doc_edit(driver)
    test_doc_delete(driver)

    time.sleep(1)
    back_to_providers(driver)


def sort_test(driver,sort_button_path,results_path,sort_forward,text_test=True,attribute=None):
    passed = True
    sort_button = driver.find_element_by_xpath(sort_button_path)
    sort_button.click()
    time.sleep(4)
    results = driver.find_elements_by_xpath(results_path)
    results = results[1:]
    prev = None
    for r in results:
        """
        atts = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', r)
        print(atts)
        """
        if text_test:
            data = r.text.lower()
        else:
            data = r.get_attribute('class')
            #print(data)
            if 'alert' not in data:
                data = 'true'
            else:
                data = 'false'
        print(data)
        if prev != None:
            # watch tests for un tested non text attributes
            if sort_forward:
                if data < prev:
                    print(data + " < " + prev)
                    passed = False
            else:
                if data > prev:
                    print(data + " > " + prev)
                    passed = False
        prev = data

    if passed:
        print('PASS - sort success')
    else:
        print('FAIL - sorting problem')

def run_all_sort_tests(driver):
    time.sleep(2)
    need_attribute_list = ["IsClearToTransport","IsActive"]
    attribute = 'data-value'
    sort_tuple = get_sort_data(driver)
    print(sort_tuple)

    for t in sort_tuple:
        sort_button_path = '//div[contains(text(),"'+t[0]+'")]'
        results_path = '//div[@data-field="'+t[1]+'"]'
        flag_results_path = '//div[@data-field="'+t[1]+'"]/div[1]/*[local-name() = "svg"]'
        if t[1] in need_attribute_list:
            sort_test(driver,sort_button_path,flag_results_path,True,False,attribute)
            sort_test(driver,sort_button_path,flag_results_path,False,False,attribute)
        else:    
            sort_test(driver,sort_button_path,results_path,True)
            sort_test(driver,sort_button_path,results_path,False)

def get_target_num_entries(driver):
    dropdown = driver.find_element_by_xpath('//div[@class="MuiTablePagination-select MuiSelect-select MuiSelect-standard MuiInputBase-input css-1cccqvr"]')
    return int(dropdown.text)

def get_reported_start(driver):
    page_readout = driver.find_element_by_xpath('//div[@class="MuiToolbar-root MuiToolbar-gutters MuiToolbar-regular MuiTablePagination-toolbar css-8nphli"]/p[2]').text
    dash_i = page_readout.find('–')
    return int(page_readout[0:dash_i])

def get_reported_end(driver):
    page_readout = driver.find_element_by_xpath('//div[@class="MuiToolbar-root MuiToolbar-gutters MuiToolbar-regular MuiTablePagination-toolbar css-8nphli"]/p[2]').text
    dash_i = page_readout.find('–')
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
        dropdown = driver.find_element_by_xpath('//div[@class="MuiTablePagination-select MuiSelect-select MuiSelect-standard MuiInputBase-input css-1cccqvr"]')
        num_entries_dropdown_id = dropdown.get_attribute('id')
        print(num_entries_dropdown_id)
        #watch this, getting some odd behavior from big entry list loading
        dropdown_handler(driver,num_entries_dropdown_id,i,'//div[@id="'+num_entries_dropdown_id+'"]')
        time.sleep(10+i)
        evaluate_entries_per_page(driver)

def hundred_per_page(driver):
    dropdown = driver.find_element_by_xpath('//div[@class="MuiTablePagination-select MuiSelect-select MuiSelect-standard MuiInputBase-input css-1cccqvr"]')
    num_entries_dropdown_id = dropdown.get_attribute('id')
    #watch this, getting some odd behavior from big entry list loading
    dropdown_handler(driver,num_entries_dropdown_id,5)
    time.sleep(10)

def page_change_test(driver,pages_to_test):
    pages = pages_to_test
    page = 0
    headers = driver.find_elements_by_xpath('//div[@class="MuiDataGrid-cell--withRenderer MuiDataGrid-cell MuiDataGrid-cell--textLeft"]')
    data_field = headers[0].get_attribute('data-field')
    while page < pages:
        target_end = get_reported_end(driver) + get_target_num_entries(driver)
        first_entry = driver.find_elements_by_xpath('//div[@data-field="'+data_field+'"]/a')[0].text

        #get initial stat
        next_button = driver.find_element_by_xpath('//button[@title="Go to next page"]')
        next_button.click()
        time.sleep(3.5)
        #click
        #check reaout as +rows per page
        new_end = get_reported_end(driver)
        new_first_entry = driver.find_elements_by_xpath('//div[@data-field="'+data_field+'"]/a')[0].text
        if (new_end == target_end) and (first_entry != new_first_entry):
            print('PASS - goes to next page')
        else:
            print('FAIL - page nav error')
        #then do backwards
        page += 1
    while page > 0:
        target_end = get_reported_end(driver) - get_target_num_entries(driver)
        first_entry = driver.find_elements_by_xpath('//div[@data-field="'+data_field+'"]/a')[0].text

        #get initial stat
        next_button = driver.find_element_by_xpath('//button[@title="Go to previous page"]')
        next_button.click()
        time.sleep(4)
        #click
        #check reaout as +rows per page
        new_end = get_reported_end(driver)
        new_first_entry = driver.find_elements_by_xpath('//div[@data-field="'+data_field+'"]/a')[0].text
        if (new_end == target_end) and (first_entry != new_first_entry):
            print('PASS - goes to previous page')
        else:
            print('FAIL - page nav error')
        #then do backwards
        page -= 1

def complete_create_tp_form(driver,company_name,save = True):
    click_all_date_buttons(driver,True)
    scroll_top(driver)
    
    first = get_random_name()
    last = get_random_name()
    email_end = '@'+company_name[0]+'tc.com'
    email = last+email_end
    address = str(random.randint(1,12000))+" "+get_random_name()+" st."
    city_seed = get_random_name() + get_random_name()
    city = city_seed + " city"
    state_i = random.randint(0,49)
    zipcode = str(get_random_number(5))
    county = get_random_name() + get_random_name()+ get_random_name()
    area_code = get_random_number(3,True)
    driver.find_element_by_xpath('//input[@name="TransportationProviderName"]').send_keys(company_name)
    driver.find_element_by_xpath('//input[@name="EmailAddress"]').send_keys(email)
    driver.find_element_by_xpath('//input[@name="MainContactFirstName"]').send_keys(first)
    driver.find_element_by_xpath('//input[@name="MainContactLastName"]').send_keys(last)
    driver.find_element_by_xpath('//input[@name="AddressLine1"]').send_keys(address)
    #AddressLine2
    driver.find_element_by_xpath('//input[@name="City"]').send_keys(city)
    #State
    dropdown_handler(driver,"State",state_i)
    state = dropdown_scraper(driver,"State",state_i,"data-value")
    driver.find_element_by_xpath('//input[@name="ZipCode"]').send_keys(zipcode)
    driver.find_element_by_xpath('//input[@name="County"]').send_keys(county)
    m_phone = str(area_code+get_random_number(7))
    driver.find_element_by_xpath('//input[@name="MainPhone"]').send_keys(m_phone)
    #MainPhoneCountryCode
    #MainPhoneExtension
    d_phone = str(area_code+get_random_number(7))
    driver.find_element_by_xpath('//input[@name="DispatchPhone"]').send_keys(d_phone)
    #DispatchPhoneCountryCode
    #DispatchPhoneExtension
    c_first = get_random_name()
    c_last = get_random_name()
    driver.find_element_by_xpath('//input[@name="BillingContactFirstName"]').send_keys(c_first)
    driver.find_element_by_xpath('//input[@name="BillingContactLastName"]').send_keys(c_last)
    driver.find_element_by_xpath('//input[@name="BillingEmailAddress"]').send_keys(c_last+email_end)
    driver.find_element_by_xpath('//input[@name="BillingAddressLine1"]').send_keys(address)
    #MessagingMethod
    dropdown_handler(driver,"DefaultDriverMessagingMethodID",2)
    mm_type = dropdown_scraper(driver,"DefaultDriverMessagingMethodID",2)
    #BillingAddressLine2
    driver.find_element_by_xpath('//input[@name="BillingCity"]').send_keys(city)
    #BillingState
    dropdown_handler(driver,"BillingState",state_i)
    driver.find_element_by_xpath('//input[@name="BillingZipCode"]').send_keys(zipcode)
    #acct = get_random_number(8)+get_random_char(4)
    #driver.find_element_by_xpath('//input[@name="AccountNumber"]').send_keys(acct)
    b_phone = str(area_code+get_random_number(7))
    driver.find_element_by_xpath('//input[@name="BillingPhone"]').send_keys(b_phone)
    #BillingPhoneCountryCode
    #BillingPhoneExtension
    o_first = get_qa_tag()
    o_last = get_random_name()
    driver.find_element_by_xpath('//input[@name="OwnerFirstName"]').send_keys(o_first)
    driver.find_element_by_xpath('//input[@name="OwnerLastName"]').send_keys(o_last)
    driver.find_element_by_xpath('//input[@name="OwnerEmailAddress"]').send_keys(o_last+email_end)
    o_phone = str(area_code+get_random_number(7))
    driver.find_element_by_xpath('//input[@name="OwnerPhone"]').send_keys(o_phone)
    #OwnerPhoneCountryCode
    #OwnerPhoneExtension
    ein = str(get_random_number(9))
    driver.find_element_by_xpath('//input[@name="EmployerIdentificationNumber"]').send_keys(ein)
    driver.find_element_by_xpath('//input[@name="LegalEntityBusinessName"]').send_keys(email_end[1:4]+" inc.")
    #LegalEntityStateCode
    l_state_i = random.randint(0,49)
    dropdown_handler(driver,"LegalEntityStateCode",l_state_i)
    l_state = dropdown_scraper(driver,"LegalEntityStateCode",l_state_i,"data-value")
    driver.find_element_by_xpath('//input[@name="PhysicalAddressLine1"]').send_keys(address)
    #PhysicalAddressLine2
    driver.find_element_by_xpath('//input[@name="PhysicalCity"]').send_keys(city)
    #PhysicalState
    dropdown_handler(driver,"PhysicalState",state_i)
    driver.find_element_by_xpath('//input[@name="PhysicalZipCode"]').send_keys(zipcode)


    #LegalEntityTypeID
    ent_i = random.randint(0,6)
    dropdown_handler(driver,"LegalEntityTypeID",ent_i)
    entity = dropdown_scraper(driver,"LegalEntityTypeID",ent_i)
    #LegalEntityStatusID
    dropdown_handler(driver,"LegalEntityStatusID",1)
    status = dropdown_scraper(driver,"LegalEntityStatusID",1)

    #TransportationProviderTypeID
    dropdown_handler(driver,"TransportationProviderTypeID",1)
    p_type = dropdown_scraper(driver,"TransportationProviderTypeID",1)
    #TransportationProviderTierID
    #dropdown_handler(driver,"TransportationProviderTierID",1)
    #p_tier = dropdown_scraper(driver,"TransportationProviderTierID",1)

    npi = str(get_random_number(6))
    driver.find_element_by_xpath('//input[@name="NPINumber"]').send_keys(npi)

    ins_co = get_random_name()+'-'+get_random_name()+' insurance'
    policy = get_random_char(3) + get_random_number(6)
    driver.find_element_by_xpath('//input[@name="CommercialInsuranceCompanyName"]').send_keys(ins_co)
    driver.find_element_by_xpath('//input[@name="CommercialInsurancePolicyNumber"]').send_keys(policy)

    ins_co2 = get_random_name()+'-'+get_random_name()+' insurance'
    policy2 = get_random_char(3) + get_random_number(6)
    if len(driver.find_elements_by_xpath('//input[@name="AutoInsuranceCompanyName"]')) > 0:
        driver.find_element_by_xpath('//input[@name="AutoInsuranceCompanyName"]').send_keys(ins_co2)
        driver.find_element_by_xpath('//input[@name="AutoInsurancePolicyNumber"]').send_keys(policy2)

    #InsuranceStrengthID
    dropdown_handler(driver,"CommercialInsuranceStrengthID",1)
    com_strength = dropdown_scraper(driver,"CommercialInsuranceStrengthID",1)
    dropdown_handler(driver,"AutoInsuranceStrengthID",1)
    ai_strength = dropdown_scraper(driver,"AutoInsuranceStrengthID",1)
    comm_agg=str(random.randint(1,1000)*10000)
    bi_pp=str(random.randint(1,1000)*10000)
    bi_pa=str(random.randint(1,1000)*10000)
    pd_pa=str(random.randint(1,1000)*10000)
    combined=str(random.randint(1,1000)*10000)
    driver.find_element_by_xpath('//input[@name="CommercialAggregateAmount"]').send_keys(comm_agg)
    
    driver.find_element_by_xpath('//input[@name="AutoBodilyInjuryPerson"]').send_keys(bi_pp)
    driver.find_element_by_xpath('//input[@name="AutoBodilyInjuryAccident"]').send_keys(bi_pa)
    driver.find_element_by_xpath('//input[@name="AutoPropertyDamage"]').send_keys(pd_pa)
    #driver.find_element_by_xpath('//input[@name="AutoCombinedLimit"]').send_keys(combined)

    bank = get_random_char(1)+". "+get_random_char(1)+". "+get_random_name()+get_random_name()+" bank"
    b_acct = "" #get_random_number(12)
    b_route = "" #get_random_number(9)
    driver.find_element_by_xpath('//input[@name="BankName"]').send_keys(bank)
    #driver.find_element_by_xpath('//input[@name="BankAccountNumber"]').send_keys(b_acct)
    #driver.find_element_by_xpath('//input[@name="BankRoutingNumber"]').send_keys(b_route)


    driver.find_element_by_xpath('//textarea[@rows="10"]').send_keys(city)

    driver.find_element_by_xpath('//span[contains(text(), "Active")]//ancestor::label[1]/span/input').click()

    should = {
        "TransportationProviderName":company_name,
        "EmailAddress":email,
        "MainContactFirstName":first,
        "MainContactLastName":last,
        "AddressLine1":address,
        "City":city,
        "ZipCode":zipcode,
        "County":county,
        "MainPhone":m_phone,
        "DispatchPhone":d_phone,
        "BillingContactFirstName":c_first,
        "BillingContactLastName":c_last,
        "BillingEmailAddress":c_last+email_end,
        "BillingAddressLine1":address,
        "BillingCity":city,
        "BillingZipCode":zipcode,
        #"AccountNumber":acct,
        "BillingPhone":b_phone,
        "MessagingMethod":mm_type,
        "OwnerFirstName":o_first,
        "OwnerLastName":o_last,
        "OwnerEmailAddress":o_last+email_end,
        "OwnerPhone":o_phone,
        "EmployerIdentificationNumber":ein,
        "LegalEntityBusinessName":email_end[1:4]+" inc.",
        "PhysicalAddressLine1":address,
        "PhysicalCity":city,
        "PhysicalZipCode":zipcode,
        "NPINumber":npi,
        "CommercialInsuranceCompanyName":ins_co,
        "CommercialInsurancePolicyNumber":policy,
        "CommercialAggregateAmount":comm_agg,
        "AutoInsuranceCompanyName":ins_co2,
        "AutoInsurancePolicyNumber":policy2,
        "AutoBodilyInjuryPerson":bi_pp,
        "AutoBodilyInjuryAccident":bi_pa,
        "AutoPropertyDamage":pd_pa,
        "AutoCombinedLimit":"",
        "CoverageAreas":city,
        #dropdowns
        
        "State": state,
        "BillingState": state,
        "LegalEntityStateCode": l_state,
        "PhysicalState": state,
        "LegalEntityTypeID": entity,
        "LegalEntityStatusID": status,
        "TransportationProviderTypeID": p_type,
        #"TransportationProviderTierID": p_tier,
        "CommercialInsuranceStrengthID": com_strength,
        "AutoInsuranceStrengthID": ai_strength,

        "BankName": bank,
        "BankAccountNumber": "xxxxxxxx"+b_acct[-4:] if len(b_acct)>0 else "",
        "BankRoutingNumber": "xxxxx"+b_route[-4:] if len(b_route)>0 else "",

        #checkboxes
        #"HasReceivedProviderManual": False,
        "HasWheelchairVehiclesAvailable": False,
        #"HasReceivedNEMTProviderManual": False,
        #"HasSupplierDiversity": False,
        #"HasRegulatedDrugTesting": False,
        "IsClearToTransport": False,
        "IsActive": True,
        #"IsCompliant": False,
        "HasWorkersComp": ""

    }

    if save:
        save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
        save_button.click()
    
    return should

def back_to_tp(driver):
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def test_create_tp(driver):
    scroll_top(driver)
    add_tp_button = driver.find_element_by_xpath('//button[contains(text(),"Add Provider")]')
    add_tp_button.click()
    co_name = get_random_name() + " transportation co."
    to_check = complete_create_tp_form(driver,co_name)
    time.sleep(3)
    still_create = driver.find_elements_by_xpath('//h6[contains(text(), "Update Provider")]')
    if len(still_create) > 0:
        print('FAIL - TP creation errors')
        close_create(driver)
    else:
        strong_validate_new_tp(driver,to_check)
        back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
        back_button.click()

        time.sleep(5)
        results = driver.find_elements_by_xpath('//div[@data-field="TransportationProviderName"]/a')
        if results[0].text == co_name:
            print('PASS - Created new TP - '+results[0].text)
        else:
            print('FAIL - TP not created')

def confirm_errors_message(driver,text_msg = ""):
    time.sleep(0.5)
    optional_return = False
    warnings = driver.find_elements_by_xpath('//div[@class="MuiAlert-message css-1xsto0d"]')
    if len(warnings)>0 and "There are errors" in warnings[0].text:
        print('PASS - Warning displayed '+text_msg)
        optional_return = True
    else:
        print('FAIL - No warning displayed '+text_msg)
    return optional_return

def test_create_tp_no_data(driver):
    scroll_top(driver)
    add_tp_button = driver.find_element_by_xpath('//button[contains(text(),"Add Provider")]')
    add_tp_button.click()
    scroll_top(driver)
    time.sleep(1)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    confirm_errors_message(driver)
    close_create(driver)

def test_create_tp_invalid_field(driver):
    scroll_top(driver)
    add_tp_button = driver.find_element_by_xpath('//button[contains(text(),"Add Provider")]')
    add_tp_button.click()
    co_name = get_random_name() + " transportation co."
    complete_create_tp_form(driver,co_name,False)
    email_field = driver.find_element_by_xpath('//input[@name="EmailAddress"]')
    email_field.send_keys(Keys.CONTROL + "a")
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys(get_random_char(5))
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    confirm_errors_message(driver)
    close_create(driver)

def close_create(driver):
    close_button = driver.find_element_by_xpath('//button[@data-testid="close"]')
    close_button.click()
    to_close = driver.find_elements_by_xpath('//p[contains(text(),"close without saving")]')
    if len(to_close) > 0:
        confirm_button = driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
        confirm_button.click()

def test_open_close_create_tp(driver):
    scroll_top(driver)
    add_tp_button = driver.find_element_by_xpath('//button[contains(text(),"Add Provider")]')
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
    time.sleep(5)
    co_to_kill = driver.find_elements_by_xpath('//div[@data-field="TransportationProviderName"]/a')[0].text

    delete_buttons = driver.find_elements_by_xpath('//button[@data-testid="delete"]')
    delete_buttons[0].click()

    no_button = driver.find_element_by_xpath('//button[contains(text(),"No")]')
    no_button.click()

    delete_buttons = driver.find_elements_by_xpath('//button[@data-testid="delete"]')
    delete_buttons[0].click()

    yes_button = driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
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
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
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
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def test_edit_tp_invalid_field(driver):
    open_tp_edit(driver,0)
    email_field = driver.find_element_by_xpath('//input[@name="EmailAddress"]')
    email_field.send_keys(Keys.CONTROL + "a")
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys(get_random_char(5))
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    confirm_errors_message(driver)
    close_create(driver)
    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def test_edit_tp(driver):
    time.sleep(1.5)
    open_tp_edit(driver,0)
    time.sleep(1.5)
    new_name = get_random_name()
    field = driver.find_element_by_xpath('//input[@name="OwnerFirstName"]')
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys(new_name)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(4)
    still_create = driver.find_elements_by_xpath('//h6')
    if len(still_create) > 0:
        print('FAIL - TP edit save errors')
        close_create(driver)
    else:
        co_data = get_current_company_data(driver)
        #test codata v new_name
        if co_data['OwnerFirstName'] == new_name:
            print('PASS - Successful TP edit')
        else:
            print('FAIL - TP not edited')

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def tp_future_auto_ins(driver):
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()
    time.sleep(0.5)
    future = "12252024"
    fields = driver.find_elements_by_xpath('//label[contains(text(),"Expiration date")]//ancestor::div/div/input')
    field = fields[1]
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys(future)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(2)

def tp_past_auto_ins(driver):
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()
    time.sleep(0.5)
    past = "12252020"
    fields = driver.find_elements_by_xpath('//label[contains(text(),"Expiration date")]//ancestor::div/div/input')
    field = fields[1]
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys(past)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(2)

def get_all_driver_names(driver):
    time.sleep(1)
    all_rows = driver.find_elements_by_xpath('//div[@role="row"]')
    all_rows = all_rows[1:]
    #print(len(all_rows))
    results = []
    for r in all_rows:
        last = r.find_element_by_xpath('.//a')
        first = r.find_element_by_xpath('.//div[@data-field="DriverFirstName"]')
        full = first.text + " " + last.text
        #print(full)
        results.append(full)
    return results

def go_to_drivers(driver):
    driver_button = driver.find_element_by_xpath('//a[contains(text(),"Drivers")]')
    driver_button.click()

def go_to_vehicles(driver):
    v_button = driver.find_element_by_xpath('//a[contains(text(),"Vehicles")]')
    v_button.click()

def go_to_users(driver):
    users_button = driver.find_element_by_xpath('//button[contains(text(),"Users")]')
    driver.execute_script("arguments[0].scrollIntoView();", users_button)
    driver.execute_script("window.scrollTo(0,100);")
    time.sleep(1.5)
    users_button.click()

def complete_user_form(driver,valid=True):
    first_name = get_random_name()
    last_name = get_random_name() + get_random_name()
    if valid:
        email = first_name + "." + last_name + "@tryon.com"
    else:
        email = "blah"
    driver.find_element_by_xpath('//input[@name="FirstName"]').send_keys(first_name)
    driver.find_element_by_xpath('//input[@name="LastName"]').send_keys(last_name)
    driver.find_element_by_xpath('//input[@name="Email"]').send_keys(email)
    time.sleep(1)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()


    user_data = {
        "first": first_name,
        "last": last_name,
        "email": email,
        "admin": False,
        "accounting": False
    }
    return user_data

def click_add_user(driver):
    add_button = driver.find_element_by_xpath('//button[contains(text(),"Add User")]')
    add_button.click()

def create_new_user_valid(driver):
    click_add_user(driver)
    u_data = complete_user_form(driver)
    return u_data

def create_new_user_invalid(driver):
    click_add_user(driver)
    complete_user_form(driver,False)
    if confirm_errors_message(driver):
        print("PASS - User form warns invalid data")
        close_create(driver)
    else:
        print("FAIL - now warning displayed")
    
def edit_user(driver):
    changed_string = "changed"
    time.sleep(1)
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()
    time.sleep(1)
    field = driver.find_element_by_xpath('//input[@name="LastName"]')
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys(changed_string)
    time.sleep(1)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(2.5)
    back_to_tp(driver)
    time.sleep(1)
    last_name_elements = driver.find_elements_by_xpath('//div[@data-field="UserLastName"]')
    change_present = False
    for e in last_name_elements:
        if e.text == changed_string:
            change_present = True
    if change_present:
        print("PASS - User edited")
    else:
        print("FAIL! - User edit failed!")
        close_create(driver)

def users_tests(driver):
    click_entry(driver,0)
    time.sleep(2)
    go_to_users(driver)
    create_new_user_invalid(driver)

    time.sleep(1)
    initial_rows = row_counter(driver,0)
    print(initial_rows)
    u_data = create_new_user_valid(driver)
    time.sleep(2)
    final_rows = row_counter(driver,0)
    print(final_rows)

    if final_rows == initial_rows + 1:
        print("PASS - user successfully added")
    else:
        print("FAIL - user not added")

    last_user = driver.find_element_by_xpath('//a[contains(text(),"'+u_data["first"]+'")]')
    last_user.click()
    edit_user(driver)

    time.sleep(1)

    scroll_top(driver)
    back_to_tp(driver)

    time.sleep(2)

def notes_tests(driver):
    click_entry(driver,0)
    time.sleep(2)
    go_to_notes(driver)
    time.sleep(1)
    test_open_close_note(driver)
    time.sleep(1)
    test_note_validation(driver)
    time.sleep(1)
    test_note_create(driver)
    time.sleep(1)
    test_note_edit(driver)
    time.sleep(1)
    test_comment_open_close(driver)
    time.sleep(1)
    test_comment_validation(driver)
    time.sleep(1)
    test_comment_create(driver)
    time.sleep(1)
    test_comment_edit(driver)
    time.sleep(1)
    test_comment_delete(driver)
    time.sleep(1)
    test_note_delete(driver)
    time.sleep(1)

    scroll_top(driver)
    back_to_tp(driver)

    time.sleep(2)

def go_to_notes(driver):
    notes_button = driver.find_element_by_xpath('//button[contains(text(),"Notes")]')
    driver.execute_script("arguments[0].scrollIntoView();", notes_button)
    driver.execute_script("window.scrollTo(0,100);")
    time.sleep(1.5)
    notes_button.click()

def click_add_note(driver):
    notes_button = driver.find_element_by_xpath('//button[contains(text(),"Add Note")]')
    notes_button.click()

def test_open_close_note(driver):
    click_add_note(driver)
    time.sleep(1)
    cancel_button = driver.find_element_by_xpath('//button[contains(text(),"Cancel")]')
    cancel_button.click()
    time.sleep(1.5)
    add_note_headline_list = driver.find_elements_by_xpath('//h2[contains(text(),"Add Note")]')
    if len(add_note_headline_list) == 0:
        print("PASS - Add Note dialog opened and closed")
    else:
        print("FAIL - Open/Close Add Note dialog")

def test_note_validation(driver):
    click_add_note(driver)
    time.sleep(1)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(1.5)
    validation_alert_list = driver.find_elements_by_xpath('//p[contains(text(),"Required field")]')
    if len(validation_alert_list) > 0:
        print("PASS - Alert shown for empty Note field")
        cancel_button = driver.find_element_by_xpath('//button[contains(text(),"Cancel")]')
        cancel_button.click()
    else:
        print("FAIL - No Note Validation Alert")

def test_note_create(driver):
    test_text = "Test note " + get_qa_tag()
    click_add_note(driver)
    time.sleep(1)
    field = driver.find_element_by_xpath('//input[@name="Note"]')
    field.send_keys(test_text)

    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(1.5)
    #TODO pass/fail assertion (find text)
    matches_list = driver.find_elements_by_xpath('//td[contains(text(),"'+test_text+'")]')
    if len(matches_list) > 0:
        print("PASS - '"+test_text+"' note created")
    else:
        print("FAIL - No note detected")

def test_note_edit(driver):
    edit_text = " - note edited"
    edit_button = driver.find_element_by_xpath('//td[contains(text(),"tryon-qa")]//ancestor::tr/td[6]/button')
    edit_button.click()
    time.sleep(1)
    field = driver.find_element_by_xpath('//input[@name="Note"]')
    field.send_keys(edit_text)

    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(1.5)
    #TODO pass/fail assertion (find text)
    matches_list = driver.find_elements_by_xpath('//td[contains(text(),"'+edit_text+'")]')
    if len(matches_list) > 0:
        print("PASS - Note edited")
    else:
        print("FAIL - No edit detected")

def test_comment_open_close(driver):
    comment_button = driver.find_element_by_xpath('//td[contains(text(),"tryon-qa")]//ancestor::tr/td[6]/button[2]')
    comment_button.click()
    time.sleep(1)
    cancel_button = driver.find_element_by_xpath('//button[contains(text(),"Cancel")]')
    cancel_button.click()
    time.sleep(1.5)
    add_note_headline_list = driver.find_elements_by_xpath('//h2[contains(text(),"Add Comment")]')
    if len(add_note_headline_list) == 0:
        print("PASS - Add Comment dialog opened and closed")
    else:
        print("FAIL - Open/Close Add Comment dialog")

def test_comment_validation(driver):
    comment_button = driver.find_element_by_xpath('//td[contains(text(),"tryon-qa")]//ancestor::tr/td[6]/button[2]')
    comment_button.click()
    time.sleep(1)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(1.5)
    validation_alert_list = driver.find_elements_by_xpath('//p[contains(text(),"Required field")]')
    if len(validation_alert_list) > 0:
        print("PASS - Alert shown for empty Comment field")
        cancel_button = driver.find_element_by_xpath('//button[contains(text(),"Cancel")]')
        cancel_button.click()
    else:
        print("FAIL - No Comment Validation Alert")

def test_comment_create(driver):
    test_text = "Test comment " + get_qa_tag()
    comment_button = driver.find_element_by_xpath('//td[contains(text(),"tryon-qa")]//ancestor::tr/td[6]/button[2]')
    comment_button.click()
    time.sleep(1)
    field = driver.find_element_by_xpath('//input[@name="Note"]')
    field.send_keys(test_text)

    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(1.5)
    show_comment_button = driver.find_element_by_xpath('//td[contains(text(),"tryon-qa")]//ancestor::tr/td[1]/button')
    show_comment_button.click()
    matches_list = driver.find_elements_by_xpath('//td[contains(text(),"'+test_text+'")]')
    if len(matches_list) > 0:
        print("PASS - '"+test_text+"' comment created")
    else:
        print("FAIL - No comment detected")

def test_comment_edit(driver):
    edit_text = " - note edited"
    comment_edit_button = driver.find_element_by_xpath('//td[contains(text(),"Test comment")]//ancestor::tr/td[6]/button')
    comment_edit_button.click()
    time.sleep(1)
    field = driver.find_element_by_xpath('//input[@name="Note"]')
    field.send_keys(edit_text)

    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(1.5)
    matches_list = driver.find_elements_by_xpath('//td[contains(text(),"'+edit_text+'")]')
    if len(matches_list) > 0:
        print("PASS - Comment edited")
    else:
        print("FAIL - No comment edit")

def test_comment_delete(driver):
    full_text = driver.find_element_by_xpath('//td[contains(text(),"Test comment")]').text
    comment_delete_button = driver.find_element_by_xpath('//td[contains(text(),"Test comment")]//ancestor::tr/td[6]/button[2]')
    comment_delete_button.click()
    time.sleep(1)
    yes_button = driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
    yes_button.click()
    time.sleep(1.5)
    matching_text = driver.find_elements_by_xpath('//td[contains(text(),"'+full_text+'")]')
    if len(matching_text) == 0:
        print("PASS - Comment deleted")
    else:
        print("FAIL - Comment delete failed")

def test_note_delete(driver):
    full_text = driver.find_element_by_xpath('//td[contains(text(),"Test note")]').text
    note_delete_button = driver.find_element_by_xpath('//td[contains(text(),"Test note")]//ancestor::tr/td[6]/button[3]')
    note_delete_button.click()
    time.sleep(1)
    yes_button = driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
    yes_button.click()
    time.sleep(1.5)
    matching_text = driver.find_elements_by_xpath('//td[contains(text(),"'+full_text+'")]')
    if len(matching_text) == 0:
        print("PASS - Note deleted")
    else:
        print("FAIL - Note delete failed")

def onboarding_tests(driver):
    verify_onboarding(driver)
    test_onboarding_validation(driver)
    time.sleep(1)
    

    driver.refresh()

def verify_onboarding(driver):
    click_hamburger(driver)
    time.sleep(0.5)
    onboard_button = driver.find_elements_by_xpath('//li[contains(text(),"Onboard User")]')
    if len(onboard_button) > 0:
        print("PASS - Onboarding feature available")
    else:
        print("FAIL - Onboarding not available")
    close_hamburger(driver)
    
def test_onboarding_validation(driver):
    open_onboarding_form(driver)
    time.sleep(1)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Submit")]')
    save_button.click()
    time.sleep(1)
    validation_alert_list = driver.find_elements_by_xpath('//p[contains(text(),"Required field")]')
    if len(validation_alert_list) > 3:
        print("PASS - Alerts shown for empty fields")
    else:
        print("FAIL - No Validation Alert")

def open_onboarding_form(driver):
    click_hamburger(driver)
    time.sleep(0.5)
    onboard_button = driver.find_element_by_xpath('//li[contains(text(),"Onboard User")]')
    onboard_button.click()

def click_hamburger(driver):
    hamburger = driver.find_element_by_xpath('//button')
    hamburger.click()

def view_driver_tests(driver):
    test_back_button(driver,DRIVER_KEY)

    click_driver(driver,0)
    time.sleep(1)

    provider_link_test(driver)

    doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
    doc_button.click()
    time.sleep(2)

    test_doc_upload(driver)
    test_doc_edit(driver)
    test_doc_delete(driver)

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def view_vehicle_tests(driver):
    test_back_button(driver,VEHICLE_KEY)
    click_vehicle(driver,0)

    time.sleep(1)
    provider_link_test(driver)

    doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
    doc_button.click()
    time.sleep(2)

    test_doc_upload(driver)
    test_doc_edit(driver)
    test_doc_delete(driver)

    back_to_vehicles(driver)

def edit_driver_by_field(driver,data_tag,new_data):
    time.sleep(1)
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()
    time.sleep(1)

    field = driver.find_element_by_xpath('//input[@name="'+data_tag+'"]')
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys(new_data)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(3)

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def edit_driver_tests(driver):
    click_driver(driver,0)
    time.sleep(1)
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()

    new_name = get_random_name()
    field = driver.find_element_by_xpath('//input[@name="LastName"]')
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys(new_name)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(3)
    still_create = driver.find_elements_by_xpath('//h6')
    if len(still_create) > 0:
        print('FAIL - Driver edit save errors')
        close_create(driver)
    else:
        final_name = driver.find_element_by_xpath('//div[contains(text(), "Last name")]//ancestor::div[1]/div[2]').text
        #print(final_name)
        if final_name == new_name:
            print('PASS - Successful Driver edit')
        else:
            print('FAIL - Driver not edited')

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def edit_vehicle_tests(driver):
    click_vehicle(driver,0)
    time.sleep(1)
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()

    new_plate = get_random_char(3)+get_random_number(3)
    field = driver.find_element_by_xpath('//input[@name="LicensePlate"]')
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys(new_plate)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    time.sleep(3)
    still_create = driver.find_elements_by_xpath('//h6')
    if len(still_create) > 0:
        print('FAIL - Driver edit save errors')
        close_create(driver)
    else:
        final_name = driver.find_element_by_xpath('//div[contains(text(), "License plate")]//ancestor::div[1]/div[2]').text
        #print(final_name)
        if final_name == new_plate:
            print('PASS - Successful Driver edit')
        else:
            print('FAIL - Driver not edited')

    back_to_vehicles(driver)


def edit_driver_tests_invalid(driver):
    click_driver(driver,0)
    time.sleep(1)
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()

    email_field = driver.find_element_by_xpath('//input[@name="Email"]')
    email_field.send_keys(Keys.CONTROL + "a")
    email_field.send_keys(Keys.DELETE)
    email_field.send_keys(get_random_char(5))
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    confirm_errors_message(driver)
    close_create(driver)

    back_button = driver.find_element_by_xpath('//a[contains(text(), "Back")]')
    back_button.click()

def edit_vehicle_tests_invalid(driver):
    click_vehicle(driver,0)
    time.sleep(1)
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()

    field = driver.find_element_by_xpath('//input[@name="LicensePlate"]')
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    confirm_errors_message(driver)
    close_create(driver)

    time.sleep(1)
    print("Testing VIN validation")
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()

    field = driver.find_element_by_xpath('//input[@name="VehicleVIN"]')
    field.send_keys(Keys.CONTROL + "a")
    field.send_keys(Keys.DELETE)
    field.send_keys("1234")
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()
    confirm_errors_message(driver)
    close_create(driver)

    back_to_vehicles(driver)


def test_delete_driver(driver):
    to_kill = driver.find_elements_by_xpath('//div[@data-field="DriverLastName"]/a')[0].text

    delete_buttons = driver.find_elements_by_xpath('//button[@data-testid="delete"]')
    delete_buttons[0].click()

    no_button = driver.find_element_by_xpath('//button[contains(text(),"No")]')
    no_button.click()

    delete_buttons = driver.find_elements_by_xpath('//button[@data-testid="delete"]')
    delete_buttons[0].click()

    yes_button = driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
    yes_button.click()

    time.sleep(1)
    top_result = driver.find_elements_by_xpath('//div[@data-field="DriverLastName"]/a')[0].text
    if top_result != to_kill:
        print('PASS - '+to_kill+' deleted')
    else:
        print('FAIL - '+ to_kill+ ' not deleted')

def test_delete_vehicle(driver):
    
    make = driver.find_elements_by_xpath('//div[@data-field="VehicleMake"]/a')[0].text
    model = driver.find_elements_by_xpath('//div[@data-field="VehicleModel"]')[0+1].text
    year = driver.find_elements_by_xpath('//div[@data-field="VehicleYear"]')[0+1].text
    to_kill = make+model+year


    delete_buttons = driver.find_elements_by_xpath('//button[@data-testid="delete"]')
    delete_buttons[0].click()

    no_button = driver.find_element_by_xpath('//button[contains(text(),"No")]')
    no_button.click()

    delete_buttons = driver.find_elements_by_xpath('//button[@data-testid="delete"]')
    delete_buttons[0].click()

    yes_button = driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
    yes_button.click()

    time.sleep(1)
    make2 = driver.find_elements_by_xpath('//div[@data-field="VehicleMake"]/a')[0].text
    model2 = driver.find_elements_by_xpath('//div[@data-field="VehicleModel"]')[0+1].text
    year2 = driver.find_elements_by_xpath('//div[@data-field="VehicleYear"]')[0+1].text
    top_result = make2+model2+year2
    if top_result != to_kill:
        print('PASS - '+to_kill+' deleted')
    else:
        print('FAIL - '+ to_kill+ ' not deleted')
    
def get_sort_data(driver):
    tags = []
    headers = driver.find_elements_by_xpath('//div[@class="MuiDataGrid-columnHeader MuiDataGrid-columnHeader--sortable"]')
    for h in headers:
        tag = h.text
        data_field = h.get_attribute('data-field')
        tup = (tag,data_field)
        if tag != '':
            tags.append(tup)
    return tags

def find_not_ctt_tp(driver,section_key):
    
    time.sleep(5)
    entries = int(get_reported_end(driver))
    print(entries)
    to_do = []
    i = 0
    while i < entries:
        to_do.append(i)
        i+=1

    result_ent = None
    for ent_i in to_do:
        print(ent_i)
        click_entry(driver,ent_i)
        time.sleep(2)
        doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
        doc_button.click()
        time.sleep(2)
        doc_states = get_document_upload_states(driver)
        can_be_used = False
        for state in doc_states:
            if state != None:
                can_be_used = True
                result_ent = ent_i
                break
        if can_be_used:
            break
        else:
            print("all docs present at i="+str(ent_i))
            if section_key == VEHICLE_KEY:
                back_to_vehicles(driver)
            elif section_key == TP_KEY:
                back_to_tp(driver)
            elif section_key == DRIVER_KEY:
                back_to_drivers(driver)
    return ent_i
    

def check_ctt_status(driver):
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()
    time.sleep(1)
    ctt_highlight = driver.find_element_by_xpath('//span[contains(text(),"Clear to transport")]//ancestor::label[1]/span/input')
    disabled = ctt_highlight.get_attribute("disabled")
    #print(disabled)
    ctt = True
    if disabled == "true":
        ctt = False
        print("Clear to Transport box blocked")
    else:
        print("Clear to Transport box ACTIVE")
    close_create(driver)
    return ctt

def toggle_ctt(driver):
    edit_button = driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
    edit_button.click()
    time.sleep(0.5)
    driver.find_element_by_xpath('//textarea[@rows="10"]').send_keys("")

    ctt_box = driver.find_element_by_xpath('//span[contains(text(),"Clear to transport")]//ancestor::label[1]/span/input')
    ctt_box.click()
    save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
    save_button.click()

def compare_tp_objects(orig_tp,to_compare_tp):
    for key in orig_tp:
        if orig_tp[key] != to_compare_tp[key]:
            print("Difference found: "+key)
            print(str(orig_tp[key]) + " / " + str(to_compare_tp[key]))

def strong_validate_new_tp(driver,comp_object = None):
    if comp_object == None:
        scroll_top(driver)
        add_tp_button = driver.find_element_by_xpath('//button[contains(text(),"Add Provider")]')
        add_tp_button.click()
        #print_inputs(driver)
        co_name = get_random_name() + " transportation co."
        create_obj = complete_create_tp_form(driver,co_name)
        time.sleep(2)
    else:
        create_obj = comp_object
    
    result_obj = get_current_company_data(driver)

    compare_tp_objects(create_obj,result_obj)

def prefill_providers(driver):
    #driver.refresh()
    scroll_top(driver)
    add_tp_button = driver.find_element_by_xpath('//button[contains(text(),"Add Provider")]')
    add_tp_button.click()
    co_name = get_random_name() + " transportation co."
    complete_create_tp_form(driver,co_name,False)

def create_providers(driver,amount):
    while amount > 0:
        test_create_tp(driver)
        amount -= 1
    driver.refresh()

def create_vehicles(driver,amount):
    click_entry(driver,0)
    vehicles_button = driver.find_element_by_xpath('//button[contains(text(), "Vehicles")]')
    vehicles_button.click()
    time.sleep(1)
    while amount > 0:
        add_vehicles_button = driver.find_element_by_xpath('//button[contains(text(),"Add Vehicle")]')
        driver.execute_script("arguments[0].scrollIntoView();", add_vehicles_button)
        add_vehicles_button.click()
        complete_vehicle_form(driver)
        amount -= 1
    driver.refresh()

def create_drivers(driver,amount,ctt_test=False):
    if len(driver.find_elements_by_xpath('//button[contains(text(),"Add Driver")]')) == 0:
        click_entry(driver,0)
    time.sleep(1)
    active = True
    if ctt_test:
        active =False
    while amount > 0:
        add_driver_button = driver.find_element_by_xpath('//button[contains(text(),"Add Driver")]')
        driver.execute_script("arguments[0].scrollIntoView();", add_driver_button)
        driver.execute_script("window.scrollTo(0,100);")
        time.sleep(0.5)
        add_driver_button.click()
        complete_driver_form(driver,active)
        amount -= 1
        if active == False:
            active = True
    if not ctt_test:
        driver.refresh()


def ctt_test(driver,key,docs_needed = True):
    if key == VEHICLE_KEY:
        go_to_vehicles(driver)
    if key == DRIVER_KEY:
        go_to_drivers(driver)

    #FIND 
    if docs_needed:
        to_check_i = find_not_ctt_tp(driver,key)
    else:
        to_check_i = 0
        click_entry(driver,to_check_i)

    check_ctt_status(driver)

    time.sleep(3)
    if docs_needed:
        upload_all_docs(driver)
        time.sleep(2)
        ti_button = driver.find_element_by_xpath('//button[contains(text(),"nfo")]')
        ti_button.click()

    if key == TP_KEY:
        create_drivers(driver,2,True)
        pre_driver_tups = get_driver_ctt_active_tuples(driver)
        #print(pre_driver_tups)

    ctt_status = check_ctt_status(driver)
    if ctt_status:
        toggle_ctt(driver)
        time.sleep(2.5)
        if key == VEHICLE_KEY:
            check_obj = get_current_vehicle_data(driver)
        elif key == DRIVER_KEY:
            check_obj = get_current_driver_data(driver)
        elif key == TP_KEY:
            post_driver_tups = get_driver_ctt_active_tuples(driver)
            #print(post_driver_tups)
            check_obj = get_current_company_data(driver)
            check_driver_toggles(pre_driver_tups,post_driver_tups)
        #print(check_obj)
        if check_obj["IsClearToTransport"]:
            print("PASS - CTT successfully saved")
        else:
            print("FAIL - CTT unable to save")
    else:
        print("FAIL - CTT checkbox not cleared")
    
    if key == VEHICLE_KEY:
        back_to_vehicles(driver)
    elif key == DRIVER_KEY:
        back_to_drivers(driver)
    elif key == TP_KEY:
        back_to_tp(driver)


    time.sleep(3.5)
    ctt_flags = driver.find_elements_by_xpath('//div[@data-field="IsClearToTransport"]/div[1]/*[local-name() = "svg"]')
    #ctt_flags = ctt_flags[1:]

    flag_status = ctt_flags[to_check_i].get_attribute("class")
    if 'alert' not in flag_status:
        print("PASS - CTT flag changed")
    else:
        print("FAIL - CTT flag not updated")

    driver.refresh()

def check_driver_toggles(pre_tups,post_tups):
    passed = True
    i = 0
    for t in pre_tups:
        if t[1] == True: #active case
            if not post_tups[i][0]:
                print("Driver to CTTtoggle - FAIL!")
                passed = False
        else: #not active cas
            if t[0] != post_tups[i][0]:
                print("Erroneous driver toggle - FAIL!")
                passed = False

        i+=1
    if passed:
        print("PASS - drivers correctly toggle to CTT")
    else:
        print("FAIL - problem with driver CTT toggle")

def get_doc_row(driver,doc_type):
    title_text = driver.find_element_by_xpath('//a[contains(text(),"'+ doc_type+'")]//ancestor::div[1]')
    row = title_text.get_attribute('data-rowindex')
    return row



def test_doc_edit(driver):
    if len(driver.find_elements_by_xpath('//button[contains(text(),"Documents")]')) > 0:
        doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
        doc_button.click()

    if len(driver.find_elements_by_xpath('//button[@aria-label="edit" and not(@disabled)]')) > 0:
        edit_buttons = driver.find_elements_by_xpath('//button[@aria-label="edit" and not(@disabled)]')
        parents = driver.find_elements_by_xpath('//button[@aria-label="edit" and not(@disabled)]//ancestor::div[2]')
        row = parents[0].get_attribute("data-rowindex")
        signedOn = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div[3]').text
        effectiveStart = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div[4]').text
        effectiveEnd = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div[5]').text
        #print(signedOn + " " + effectiveStart + " " + effectiveEnd)
        edit_buttons[0].click()
        click_all_date_buttons(driver,True)
        save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
        save_button.click()
        time.sleep(1)
        signedOn2 = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div[3]').text
        effectiveStart2 = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div[4]').text
        effectiveEnd2 = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div[5]').text
        #print(signedOn2 + " " + effectiveStart2 + " " + effectiveEnd2)
        if signedOn != signedOn2:
            print("PASSED - Doc Edit - Signed On changed from "+signedOn+" to "+signedOn2)
        else:
            print("FAIL - Doc Edit - Signed On not changed")
        if effectiveStart != effectiveStart2:
            print("PASSED - Doc Edit - Effective Start changed from "+effectiveStart+" to "+effectiveStart2)
        else:
            print("FAIL - Doc Edit - Effective Start not changed")
        if effectiveEnd != effectiveEnd2:
            print("PASSED - Doc Edit - Effective End changed from "+effectiveEnd+" to "+effectiveEnd2)
        else:
            print("FAIL - Doc Edit - Effective End not changed")
    else:
        print("No documents to edit detected")

def test_doc_delete(driver):
    if len(driver.find_elements_by_xpath('//button[contains(text(),"Documents")]')) > 0:
        scroll_top(driver)
        time.sleep(1)
        doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
        doc_button.click()
        time.sleep(1)
    if len(driver.find_elements_by_xpath('//button[@aria-label="delete" and not(@disabled)]')) > 0:
        row = driver.find_element_by_xpath('//button[@aria-label="delete" and not(@disabled)]//ancestor::div[2]').get_attribute("data-rowindex")
        title = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div/a').text

        delete_button = driver.find_element_by_xpath('//button[@aria-label="delete" and not(@disabled)]')
        delete_button.click()
        
        yes_button = driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
        yes_button.click()
        time.sleep(1)
        if len(driver.find_elements_by_xpath('//div[contains(text(),"No rows")]')) > 0:
            disabled_delete = "true"
        else:
            disabled_delete = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]//button[3]').get_attribute("disabled")
        if disabled_delete == "true":
            print("PASSED - Document "+title+" deleted")
        else:
            print('FAIL - Document '+title+' not deleted')

def delete_doc_by_title(driver,title):
    if len(driver.find_elements_by_xpath('//button[contains(text(),"Documents")]')) > 0:
        scroll_top(driver)
        time.sleep(1)
        doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
        doc_button.click()
        time.sleep(1)
    if len(driver.find_elements_by_xpath('//button[@aria-label="delete" and not(@disabled)]')) > 0:
        possible_rows = driver.find_elements_by_xpath('//button[@aria-label="delete" and not(@disabled)]//ancestor::div[2]')
        for p in possible_rows:
            row = p.get_attribute("data-rowindex")
            title_to_check = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div/a').text
            if title_to_check == title:
                delete_button = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div/button[3]')
                delete_button.click()
        
                yes_button = driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
                yes_button.click()
                time.sleep(1)
    else:
        print("No docs to delete")

def edit_doc_by_title(driver,title,past = True):
    if len(driver.find_elements_by_xpath('//button[contains(text(),"Documents")]')) > 0:
        scroll_top(driver)
        time.sleep(1)
        doc_button = driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
        doc_button.click()
        time.sleep(1)
    if len(driver.find_elements_by_xpath('//button[@aria-label="delete" and not(@disabled)]')) > 0:
        possible_rows = driver.find_elements_by_xpath('//button[@aria-label="delete" and not(@disabled)]//ancestor::div[2]')
        for p in possible_rows:
            row = p.get_attribute("data-rowindex")
            title_to_check = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div/a').text
            if title_to_check == title:
                edit_button = driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div/button[2]')
                edit_button.click()
                date_fields = driver.find_elements_by_xpath('//input[@placeholder="mm/dd/yyyy"]')
                field1 = date_fields[1]
                field2 = date_fields[2]
                if past:
                    date1 = '12252020'
                    date2 = '12302020'
                else:
                    date1 = '12252020'
                    date2 = '12302022'
                field1.send_keys(Keys.CONTROL + "a")
                field1.send_keys(Keys.DELETE)
                field1.send_keys(date1)
                field2.send_keys(Keys.CONTROL + "a")
                field2.send_keys(Keys.DELETE)
                field2.send_keys(date2)
                save_button = driver.find_element_by_xpath('//button[contains(text(),"Save")]')
                save_button.click()
                time.sleep(1)

def test_accounting(url):
    driver = init_driver()
    login_tpp(driver,url,"accounting")
    time.sleep(2)

    print("TESTING ACCOUNTING PERMISSION")
    click_entry(driver,0)
    c_data = get_current_company_data(driver)

    if c_data["BankAccountNumber"].startswith("xxx"):
        print("FAIL - Bank account obscured - " + c_data["BankAccountNumber"])
    else:
        print("PASS - Bank account visible - " + c_data["BankAccountNumber"])


    if c_data["BankRoutingNumber"].startswith("xxx"):
        print("FAIL - Bank routing obscured - " + c_data["BankRoutingNumber"])
    else:
        print("PASS - Bank routing visible - " + c_data["BankRoutingNumber"])
    driver.close() 
    driver.quit()

    time.sleep(2) 





""

"""
driver = init_driver()
login_tpp(driver,dev_url)
time.sleep(2)

click_entry(driver,0)
data = get_current_company_data(driver)
print(data)
#prefill_providers(driver)
""

#create_providers(driver,1)
#create_vehicles(driver,5)
#create_drivers(driver,2)
#ctt_test(driver,TP_KEY)

#test_create_tp(driver)

#close_create(driver)
""
#driver.close()

#driver.quit()
"""