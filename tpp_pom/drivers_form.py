from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from helpers import Dropdown

class DriverForm:
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

    def change_field(self,new_text,key):
        field = self.driver.find_element_by_xpath('//input[@name="'+key+'"]')
        field.send_keys(Keys.CONTROL + "a")
        field.send_keys(Keys.DELETE)
        field.send_keys(new_text)

    def complete_form(self,driver_data_dictionary):
        d = driver_data_dictionary
        self.driver.find_element_by_xpath('//input[@name="FirstName"]').send_keys(d["FirstName"])
        self.driver.find_element_by_xpath('//input[@name="LastName"]').send_keys(d["LastName"])
        self.driver.find_element_by_xpath('//input[@name="Email"]').send_keys(d["Email"])
        self.driver.find_element_by_xpath('//input[@name="DriverPhone"]').send_keys(d["DriverPhone"])
        self.driver.find_element_by_xpath('//input[@name="DriversLicenseNumber"]').send_keys(d["DriversLicenseNumber"])
        self.driver.find_element_by_xpath('//input[@name="EmergencyContactFirstName"]').send_keys(d["EmergencyContactFirstName"])
        self.driver.find_element_by_xpath('//input[@name="EmergencyContactLastName"]').send_keys(d["EmergencyContactLastName"])
        self.driver.find_element_by_xpath('//input[@name="EmergencyContactPhone"]').send_keys(d["EmergencyContactPhone"])

        messaging_method_dropdown = self.open_dropdown("mui-component-select-MessagingMethod")
        messaging_method_dropdown.click_by_index(1)

        state_dropdown = self.open_dropdown("mui-component-select-DriverLicenseIssuedInStateCode")
        state_dropdown.click_by_key(driver_data_dictionary["DriverLicenseIssuedInStateCode"])

        if driver_data_dictionary["Active"]:
            self.driver.find_element_by_xpath('//span[contains(text(), "Active")]//ancestor::label[1]/span/input').click()