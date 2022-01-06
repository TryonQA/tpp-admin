from selenium import webdriver
import time
import vehicles_form
import helpers as h
from providers_detail import DocumentsSub

class VehicleDetail:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.refresh_buttons()

    def refresh_buttons(self):
        self.info_button = self.driver.find_element_by_xpath('//button[contains(text(),"Vehicle info")]')
        self.documents_button = self.driver.find_element_by_xpath('//button[contains(text(),"Documents")]')

        self.edit_button = self.driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
        self.back_button = self.driver.find_element_by_xpath('//a[contains(text(), "Back")]')

    def get_documents_subpage(self) -> DocumentsSub:
        self.documents_button.click()
        self.refresh_buttons()
        time.sleep(1)
        return DocumentsSub(self.driver)

    def click_back(self):
        self.back_button.click()

    def open_edit_form(self) -> vehicles_form.VehicleForm:
        self.refresh_buttons()
        self.edit_button.click()
        time.sleep(1)
        edit_form = vehicles_form.VehicleForm(self.driver)
        return edit_form