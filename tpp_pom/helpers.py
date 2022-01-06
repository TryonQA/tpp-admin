import time
from selenium import webdriver
from selenium.webdriver.chrome import options
from selenium.webdriver.common.keys import Keys
import random
import datetime
import requests

def parse_yes_no(text_y_n):
    if text_y_n == "No" or text_y_n == "Inactive":
        return False
    elif text_y_n == "Yes" or text_y_n == "Active":
        return True
    else:
        return None

def strip_non_numeric(string_to_format):
    finished = ""
    for char in string_to_format:
        if char.isnumeric():
            finished+=char
    return finished

def scroll_top(driver:webdriver.Chrome):
    driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)

def check_for_warnings(driver:webdriver.Chrome):
    optional_return = False
    warnings = driver.find_elements_by_xpath('//div[@class="MuiAlert-message css-1w0ym84"]')
    if len(warnings)>0:
        optional_return = True
    return optional_return

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

DIGITS = '123456789'
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

def get_qa_tag():
    return str(datetime.datetime.now()) + " tryon-qa-gb"

STATES = [
 "Alaska",
 "Alabama",
 "Arkansas",
 "Arizona",
 "California",
 "Colorado",
 "Connecticut",
 "Delaware",
 "Florida",
 "Georgia",
 "Hawaii",
 "Iowa",
 "Idaho",
 "Illinois",
 "Indiana",
 "Kansas",
 "Kentucky",
 "Louisiana",
 "Massachusetts",
 "Maryland",
 "Maine",
 "Michigan",
 "Minnesota",
 "Missouri",
 "Mississippi",
 "Montana",
 "North Carolina",
 "North Dakota",
 "Nebraska",
 "New Hampshire",
 "New Jersey",
 "New Mexico",
 "Nevada",
 "New York",
 "Ohio",
 "Oklahoma",
 "Oregon",
 "Pennsylvania",
 "Rhode Island",
 "South Carolina",
 "South Dakota",
 #"Tennessee",
 "Texas",
 "Utah",
 "Virginia",
 "Vermont",
 "Washington",
 "Wisconsin",
 "West Virginia",
 "Wyoming"]

def compare_provider_data(orig_tp,to_compare_tp):
    differences = []
    for key in orig_tp:
        if orig_tp[key] != to_compare_tp[key]:
            differences.append(key+" - "+str(orig_tp[key]) + " / " + str(to_compare_tp[key]))
    return differences

def get_new_provider_data():

    company_name = get_random_name() + " transportation co."
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
    m_phone = str(area_code+get_random_number(7))
    d_phone = str(area_code+get_random_number(7))
    c_first = get_random_name()
    c_last = get_random_name()
    acct = get_random_number(8)+get_random_char(4)
    b_phone = str(area_code+get_random_number(7))
    o_first = get_qa_tag()
    o_last = get_random_name()
    o_phone = str(area_code+get_random_number(7))
    ein = str(get_random_number(9))
    npi = str(get_random_number(6))
    ins_co = get_random_name()+'-'+get_random_name()+' insurance'
    policy = get_random_char(3) + get_random_number(6)
    ins_co2 = get_random_name()+'-'+get_random_name()+' insurance'
    policy2 = get_random_char(3) + get_random_number(6)
    comm_agg=str(random.randint(1,1000)*10000)
    bi_pp=str(random.randint(1,1000)*10000)
    bi_pa=str(random.randint(1,1000)*10000)
    pd_pa=str(random.randint(1,1000)*10000)
    bank = get_random_char(1)+". "+get_random_char(1)+". "+get_random_name()+get_random_name()+" bank"
    b_acct = get_random_number(12)
    b_route = get_random_number(9)

    provider_data = {
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
        "AccountNumber":acct,
        "BillingPhone":b_phone,
        "MessagingMethod":"SMS",
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
        
        "State": STATES[state_i],
        "BillingState": STATES[state_i],
        "LegalEntityStateCode": STATES[state_i],
        "PhysicalState": STATES[state_i],
        "LegalEntityTypeID": "LLC",
        "LegalEntityStatusID": "Good Standing",
        "TransportationProviderTypeID": "Out-of-network",
        "TransportationProviderTierID": "Silver",
        "CommercialInsuranceStrengthID": "A+",
        "AutoInsuranceStrengthID": "A+",

        "BankName": bank,
        "BankAccountNumber": "xxxxxxxx"+b_acct[-4:],
        "BankRoutingNumber": "xxxxx"+b_route[-4:],

        #checkboxes
        "HasReceivedProviderManual": False,
        "HasWheelchairVehiclesAvailable": False,
        "HasReceivedNEMTProviderManual": False,
        "HasSupplierDiversity": False,
        "HasRegulatedDrugTesting": False,
        "IsClearToTransport": False,
        "IsActive": True,
        "IsCompliant": False,
        "HasWorkersComp": False
    }
    
    return provider_data

def get_driver_data(active=True):
    name = get_random_name()
    driver_data = {
        "FirstName": get_qa_tag(),
        "LastName": name,
        "Email": name + get_random_number(2) + "@fake.com",
        "DriverPhone": get_random_number(10,phone=True),
        "DriversLicenseNumber": get_random_number(8),
        "EmergencyContactFirstName": get_random_name(),
        "EmergencyContactLastName": name,
        "EmergencyContactPhone": get_random_number(10,phone=True),
        "DriverLicenseIssuedInStateCode": STATES[random.randint(0,49)],
        "Active":active
    }
    return driver_data

def get_random_vin():
    res = requests.get("https://randomvin.com/getvin.php?type=fake")
    vin = res.text
    return vin

REAL_VEHICLES = [("Ford","Transit 350"),("Dodge","Grand Caravan"),("Honda","Accord"),\
    ("Ford","F-150"),("GMC","Yukon"),("Toyota","Yaris")]

def get_vehicle_data(active=True):
    vin = get_random_vin()
    v_index = random.randint(0,len(REAL_VEHICLES)-1)
    makeModel = REAL_VEHICLES[v_index]
    make = makeModel[0]
    model = makeModel[1]
    v_data = {
        "LicensePlate":'tryon-qa-gb',
        "VehicleVIN":vin,
        "VehicleMake":make,
        "VehicleModel":model,
        "VehicleYear":str(2000+random.randint(0,22)),
        "LicenseStateCode":STATES[random.randint(0,49)],
        "Active":active
    }
    return v_data

def refresh_site(driver:webdriver.Chrome):
    driver.refresh()

class Dropdown:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.options = self.driver.find_elements_by_xpath('//li[@role="option"]')

    def refresh(self):
        self.options = self.driver.find_elements_by_xpath('//li[@role="option"]')

    def click_by_index(self,index):
        if index < len(self.options):
            self.options[index].click()
            time.sleep(2)
    
    def click_by_key(self,key):
        self.refresh()
        for o in self.options:
            if key == o.text:  
                o.click()
                break
        time.sleep(1)

class DocPopUp:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.uploadable_file_path = "C:\\Users\\drgre\\Tryon\\tpp-admin\\test.pdf"
        self.refresh()

    def refresh(self):
        self.doc_type_button = self.driver.find_element_by_xpath('//label[contains(text(),"Document type")]//ancestor::div[1]')
        self.file_input = self.driver.find_element_by_xpath('//input[@id="fileUploadButton"]')
        self.save_button = self.driver.find_element_by_xpath('//button[contains(text(),"Save")]')
        self.date_inputs = self.driver.find_elements_by_xpath('//input[@placeholder="mm/dd/yyyy"]')

    def select_doc_type(self,key):
        self.doc_type_button.click()
        time.sleep(0.5)
        doc_type_dropdown = Dropdown(self.driver)
        doc_type_dropdown.click_by_key(key)
        self.refresh()

    def add_valid_dates(self):
        year_now = int(datetime.date.today().year)
        past_year = year_now - 1
        next_year = year_now + 1
        self.date_inputs[0].send_keys("0105"+str(past_year))
        self.date_inputs[1].send_keys("0105"+str(past_year))
        self.date_inputs[2].send_keys("0105"+str(next_year))
        self.refresh()

    def edit_dates(self):
        year_now = int(datetime.date.today().year)
        early_year = year_now - 2
        past_year = year_now - 1
        next_year = year_now + 1
        self.date_inputs[0].send_keys(Keys.CONTROL + "a")
        self.date_inputs[0].send_keys(Keys.DELETE)
        self.date_inputs[0].send_keys("0"+str(get_random_number(1))+"1"+str(get_random_number(1))+str(early_year))
        self.date_inputs[1].send_keys(Keys.CONTROL + "a")
        self.date_inputs[1].send_keys(Keys.DELETE)
        self.date_inputs[1].send_keys("0"+str(get_random_number(1))+"1"+str(get_random_number(1))+str(past_year))
        self.date_inputs[2].send_keys(Keys.CONTROL + "a")
        self.date_inputs[2].send_keys(Keys.DELETE)
        self.date_inputs[2].send_keys("0"+str(get_random_number(1))+"1"+str(get_random_number(1))+str(next_year))
        self.refresh()

    def set_file(self):
        self.file_input.send_keys(self.uploadable_file_path)
        self.refresh()

    def click_save(self):
        self.save_button.click()
        time.sleep(2)

