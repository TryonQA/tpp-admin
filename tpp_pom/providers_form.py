from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from helpers import Dropdown

class ProviderForm:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.refresh()
        self.header_text = self.driver.find_element_by_xpath('//h6').text 
        self.confirm_popup_xpath = '//p[contains(text(),"close without saving")]'
        self.confirm_yes_xpath = '//button[contains(text(),"Yes")]'   

    def refresh(self):  
        self.close_button = self.driver.find_element_by_xpath('//button[@data-testid="close"]')
        self.save_button = self.driver.find_element_by_xpath('//button[contains(text(),"Save")]')

    def close(self):
        self.close_button.click()
        time.sleep(2)
        #TODO check for confirm close pop up
        to_close = self.driver.find_elements_by_xpath(self.confirm_popup_xpath)
        if len(to_close) > 0:
            confirm_button = self.driver.find_element_by_xpath(self.confirm_yes_xpath)
            confirm_button.click()

    def open_dropdown(self,id) -> Dropdown:
        dropdown = self.driver.find_element_by_xpath('//div[@id="'+id+'"]')
        self.driver.execute_script("arguments[0].scrollIntoView();", dropdown)
        dropdown.click()
        return Dropdown(self.driver)

    def save_form(self):
        self.save_button.click()
        time.sleep(2)

    def check_form_alive(self):
        alive = False
        if len(self.driver.find_elements_by_xpath('//h6')) > 0:
            alive = True
        return alive

    def invalidate_email(self):
        email_field = self.driver.find_element_by_xpath('//input[@name="EmailAddress"]')
        email_field.send_keys(Keys.CONTROL + "a")
        email_field.send_keys(Keys.DELETE)
        email_field.send_keys("notanemail")

    def change_field(self,new_text,key):
        field = self.driver.find_element_by_xpath('//input[@name="'+key+'"]')
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(new_text)

    def complete_form(self,provider_data_dictionary):
        d = provider_data_dictionary
        self.driver.find_element_by_xpath('//input[@name="TransportationProviderName"]').send_keys(d["TransportationProviderName"])
        self.driver.find_element_by_xpath('//input[@name="EmailAddress"]').send_keys(d["EmailAddress"])
        self.driver.find_element_by_xpath('//input[@name="MainContactFirstName"]').send_keys(d["MainContactFirstName"])
        self.driver.find_element_by_xpath('//input[@name="MainContactLastName"]').send_keys(d["MainContactLastName"])
        self.driver.find_element_by_xpath('//input[@name="AddressLine1"]').send_keys(d["AddressLine1"])
        self.driver.find_element_by_xpath('//input[@name="City"]').send_keys(d["City"])
        self.driver.find_element_by_xpath('//input[@name="ZipCode"]').send_keys(d["ZipCode"])
        self.driver.find_element_by_xpath('//input[@name="County"]').send_keys(d["County"])
        self.driver.find_element_by_xpath('//input[@name="MainPhone"]').send_keys(d["MainPhone"])
        self.driver.find_element_by_xpath('//input[@name="DispatchPhone"]').send_keys(d["DispatchPhone"])
        self.driver.find_element_by_xpath('//input[@name="BillingContactFirstName"]').send_keys(d["BillingContactFirstName"])
        self.driver.find_element_by_xpath('//input[@name="BillingContactLastName"]').send_keys(d["BillingContactLastName"])
        self.driver.find_element_by_xpath('//input[@name="BillingEmailAddress"]').send_keys(d["BillingEmailAddress"])
        self.driver.find_element_by_xpath('//input[@name="BillingAddressLine1"]').send_keys(d["BillingAddressLine1"])
        self.driver.find_element_by_xpath('//input[@name="BillingCity"]').send_keys(d["BillingCity"])
        self.driver.find_element_by_xpath('//input[@name="BillingZipCode"]').send_keys(d["BillingZipCode"])
        self.driver.find_element_by_xpath('//input[@name="AccountNumber"]').send_keys(d["AccountNumber"])
        self.driver.find_element_by_xpath('//input[@name="BillingPhone"]').send_keys(d["BillingPhone"])
        self.driver.find_element_by_xpath('//input[@name="OwnerFirstName"]').send_keys(d["OwnerFirstName"])
        self.driver.find_element_by_xpath('//input[@name="OwnerLastName"]').send_keys(d["OwnerLastName"])
        self.driver.find_element_by_xpath('//input[@name="OwnerEmailAddress"]').send_keys(d["OwnerEmailAddress"])
        self.driver.find_element_by_xpath('//input[@name="OwnerPhone"]').send_keys(d["OwnerPhone"])
        self.driver.find_element_by_xpath('//input[@name="EmployerIdentificationNumber"]').send_keys(d["EmployerIdentificationNumber"])
        self.driver.find_element_by_xpath('//input[@name="LegalEntityBusinessName"]').send_keys(d["LegalEntityBusinessName"])
        self.driver.find_element_by_xpath('//input[@name="PhysicalAddressLine1"]').send_keys(d["PhysicalAddressLine1"])
        self.driver.find_element_by_xpath('//input[@name="PhysicalCity"]').send_keys(d["PhysicalCity"])
        self.driver.find_element_by_xpath('//input[@name="PhysicalZipCode"]').send_keys(d["PhysicalZipCode"])
        self.driver.find_element_by_xpath('//input[@name="NPINumber"]').send_keys(d["NPINumber"])
        self.driver.find_element_by_xpath('//input[@name="CommercialInsuranceCompanyName"]').send_keys(d["CommercialInsuranceCompanyName"])
        self.driver.find_element_by_xpath('//input[@name="CommercialInsurancePolicyNumber"]').send_keys(d["CommercialInsurancePolicyNumber"])
        self.driver.find_element_by_xpath('//input[@name="AutoInsuranceCompanyName"]').send_keys(d["AutoInsuranceCompanyName"])
        self.driver.find_element_by_xpath('//input[@name="AutoInsurancePolicyNumber"]').send_keys(d["AutoInsurancePolicyNumber"])
        self.driver.find_element_by_xpath('//input[@name="CommercialAggregateAmount"]').send_keys(d["CommercialAggregateAmount"])
        self.driver.find_element_by_xpath('//input[@name="AutoBodilyInjuryPerson"]').send_keys(d["AutoBodilyInjuryPerson"])
        self.driver.find_element_by_xpath('//input[@name="AutoBodilyInjuryAccident"]').send_keys(d["AutoBodilyInjuryAccident"])
        self.driver.find_element_by_xpath('//input[@name="AutoPropertyDamage"]').send_keys(d["AutoPropertyDamage"])
        self.driver.find_element_by_xpath('//input[@name="BankName"]').send_keys(d["BankName"])
        self.driver.find_element_by_xpath('//input[@name="BankAccountNumber"]').send_keys(d["BankAccountNumber"])
        self.driver.find_element_by_xpath('//input[@name="BankRoutingNumber"]').send_keys(d["BankRoutingNumber"])
        self.driver.find_element_by_xpath('//textarea[@rows="10"]').send_keys(d["CoverageAreas"])
        self.driver.find_element_by_xpath('//span[contains(text(), "Active")]//ancestor::label[1]/span/input').click()
        state_dropdown = self.open_dropdown("mui-component-select-State")
        state_dropdown.click_by_key(d["State"])
        messaging_dropdown = self.open_dropdown("mui-component-select-DefaultDriverMessagingMethodID")
        messaging_dropdown.click_by_key(d["MessagingMethod"])
        b_state_dropdown = self.open_dropdown("mui-component-select-BillingState")
        b_state_dropdown.click_by_key(d["BillingState"])
        l_state_dropdown = self.open_dropdown("mui-component-select-LegalEntityStateCode")
        l_state_dropdown.click_by_key(d["LegalEntityStateCode"])
        p_state_dropdown = self.open_dropdown("mui-component-select-PhysicalState")
        p_state_dropdown.click_by_key(d["PhysicalState"])
        le_type_dropdown = self.open_dropdown("mui-component-select-LegalEntityTypeID")
        le_type_dropdown.click_by_key(d["LegalEntityTypeID"])
        le_status_dropdown = self.open_dropdown("mui-component-select-LegalEntityStatusID")
        le_status_dropdown.click_by_key(d["LegalEntityStatusID"])
        p_type_dropdown = self.open_dropdown("mui-component-select-TransportationProviderTypeID")
        p_type_dropdown.click_by_key(d["TransportationProviderTypeID"])
        p_tier_dropdown = self.open_dropdown("mui-component-select-TransportationProviderTierID")
        p_tier_dropdown.click_by_key(d["TransportationProviderTierID"])
        c_strength_dropdown = self.open_dropdown("mui-component-select-CommercialInsuranceStrengthID")
        c_strength_dropdown.click_by_key(d["CommercialInsuranceStrengthID"])
        a_strength_dropdown = self.open_dropdown("mui-component-select-AutoInsuranceStrengthID")
        a_strength_dropdown.click_by_key(d["AutoInsuranceStrengthID"])
        #TODO handle dates
        date_inputs = self.driver.find_elements_by_xpath('//input[@placeholder="mm/dd/yyyy"]')
        for di in date_inputs:
            di.send_keys("01052022")

