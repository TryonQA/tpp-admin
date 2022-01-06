from selenium import webdriver
import time

class PreLogin:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver

        self.login_button  = self.driver.find_element_by_xpath('//button[contains(text(), "American Logistics Admin")]')

    def start_login(self):
        self.login_button.click()
        time.sleep(2)


class LoginPage:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver

        self.username_field_xpath = 'i0116'
        self.password_field_xpath = 'i0118'
        self.next_button_id = 'idSIButton9' 

    def enter_username(self,username):
        username_field = self.driver.find_element_by_id(self.username_field_xpath)
        username_field.send_keys(username)
        self.driver.find_element_by_id(self.next_button_id).click()
        time.sleep(2)

    def enter_password(self,password):
        password_field = self.driver.find_element_by_id(self.password_field_xpath)
        password_field.send_keys(password)
        self.driver.find_element_by_id(self.next_button_id).click()
        time.sleep(2)

    def finalize(self):
        if len(self.driver.find_elements_by_id(self.next_button_id)) > 0:
            self.driver.find_element_by_id(self.next_button_id).click()
            time.sleep(2)

    
