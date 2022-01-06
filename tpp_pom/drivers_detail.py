from selenium import webdriver
import time
import drivers_form
import helpers as h
from providers_detail import DocumentsSub

class DriverDetail:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.refresh_buttons()

    def refresh_buttons(self):
        self.info_button = self.driver.find_element_by_xpath('//button[contains(text(),"Driver Info")]')
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

    def open_edit_form(self) -> drivers_form.DriverForm:
        self.refresh_buttons()
        self.edit_button.click()
        time.sleep(1)
        edit_form = drivers_form.DriverForm(self.driver)
        return edit_form