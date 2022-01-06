from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from helpers import Dropdown

class VehicleForm:
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

    def complete_form(self,vehicle_data_dictionary):
        d = vehicle_data_dictionary

        self.driver.find_element_by_xpath('//input[@name="LicensePlate"]').send_keys(d["LicensePlate"])
        self.driver.find_element_by_xpath('//input[@name="VehicleVIN"]').send_keys(d["VehicleVIN"])
        self.driver.find_element_by_xpath('//input[@name="VehicleMake"]').send_keys(d["VehicleMake"])
        self.driver.find_element_by_xpath('//input[@name="VehicleModel"]').send_keys(d["VehicleModel"])
        self.driver.find_element_by_xpath('//input[@name="VehicleYear"]').send_keys(d["VehicleYear"])

        state_dropdown = self.open_dropdown("mui-component-select-LicenseStateCode")
        state_dropdown.click_by_key(d["LicenseStateCode"])
        v_type_dropdown = self.open_dropdown("mui-component-select-VehicleTypeID")
        v_type_dropdown.click_by_index(2)
        v_color_dropdown = self.open_dropdown("mui-component-select-VehicleColorID")
        v_color_dropdown.click_by_index(3)

        if d["Active"]:
            self.driver.find_element_by_xpath('//span[contains(text(), "Active")]//ancestor::label[1]/span/input').click()

        date_inputs = self.driver.find_elements_by_xpath('//input[@placeholder="mm/dd/yyyy"]')
        for di in date_inputs:
            di.send_keys("01052022")