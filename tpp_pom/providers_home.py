from selenium import webdriver
import providers_detail
import providers_form
import drivers_home
import vehicles_home
import time
from helpers import Dropdown
from helpers import scroll_top

class ProvidersHome:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.provider_link_xpath = '//a[@href="#"]'
        self.num_providers = len(self.driver.find_elements_by_xpath(self.provider_link_xpath))

        self.username = self.driver.find_element_by_xpath('//header/div/div[2]').text
        self.result_numbers_xpath = '//div[@class="MuiToolbar-root MuiToolbar-gutters MuiToolbar-regular MuiTablePagination-toolbar css-1wif0xq"]/p[2]'

        self.refresh()

    def provider_search(self,search_text):
        self.provider_search_field.send_keys(search_text)
        time.sleep(3)
    
    def clear_provider_search(self):
        self.refresh()
        self.clear_providers_search_button.click()
        self.refresh()
    
    def coverage_search(self,search_text):
        self.coverage_search_field.send_keys(search_text)
        time.sleep(3)

    def clear_coverage_search(self):
        self.refresh()
        self.clear_coverage_search_button.click()
        self.refresh()

    def refresh(self):
        if len(self.driver.find_elements_by_xpath(self.provider_link_xpath)) > 0:
            self.num_providers = len(self.driver.find_elements_by_xpath(self.provider_link_xpath))
        else: 
            self.num_providers = 0
        self.filter_button = self.driver.find_element_by_xpath('//div[@aria-haspopup="listbox"]')
        self.provider_search_field = self.driver.find_element_by_xpath('//input[@placeholder="Search by name"]')
        self.coverage_search_field = self.driver.find_element_by_xpath('//input[@placeholder="Search by coverage area"]')
        self.clear_providers_search_button = self.driver.find_element_by_xpath('//input[@placeholder="Search by name"]//ancestor::div[1]/div/button')
        self.clear_coverage_search_button = self.driver.find_element_by_xpath('//input[@placeholder="Search by coverage area"]//ancestor::div[1]/div/button')
        self.rows_per_page_dropdown = self.driver.find_element_by_xpath('//div[@class="MuiTablePagination-select MuiSelect-select MuiSelect-standard MuiInputBase-input css-1cccqvr"]')
        self.next_page_button = self.driver.find_element_by_xpath('//button[@title="Go to next page"]')
        self.previous_page_button = self.driver.find_element_by_xpath('//button[@title="Go to previous page"]')
        self.sort_buttons = self.driver.find_elements_by_xpath('//div[@class="MuiDataGrid-columnHeader MuiDataGrid-columnHeader--sortable"]')
        self.add_provider_button = self.driver.find_element_by_xpath('//button[contains(text(),"Add Provider")]')
        self.delete_buttons = self.driver.find_elements_by_xpath('//button[@data-testid="delete"]')
        self.drivers_button = self.driver.find_element_by_xpath('//a[contains(text(),"Drivers")]')
        self.vehicles_button = self.driver.find_element_by_xpath('//a[contains(text(),"Vehicles")]')
    
    def open_add_provider_form(self):
        scroll_top(self.driver)
        self.add_provider_button.click()
        time.sleep(1)
        new_provider_form = providers_form.ProviderForm(self.driver)
        return new_provider_form
    
    def open_filter(self):
        self.refresh()
        self.filter_button.click()
        time.sleep(1)
        new_filter_popup = Filter(self.driver)
        return new_filter_popup

    def delete_provider(self,provider_index = 0):
        self.delete_buttons[provider_index].click()
        time.sleep(0.5)
        yes_button = self.driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
        yes_button.click()
        time.sleep(1)

    def get_fresh_provider_links(self):
        return self.driver.find_elements_by_xpath(self.provider_link_xpath)

    def get_all_providers_data(self):
        provider_data = []
        i = 0
        # get co data

        self.refresh()
        while i < self.num_providers:
            links = self.get_fresh_provider_links()
            if i < len(links):
                links[i].click()
                time.sleep(2)
                this_provider = providers_detail.ProviderDetail(self.driver)
                this_provider_data = this_provider.get_data()
                this_provider.click_back()
                provider_data.append(this_provider_data)
                time.sleep(1)
            i+=1
        return provider_data

    def get_top_provider_data(self):
        links = self.get_fresh_provider_links()
        links[0].click()
        time.sleep(1)
        this_provider = providers_detail.ProviderDetail(self.driver)
        this_provider_data = this_provider.get_data()
        this_provider.click_back()
        time.sleep(0.5)
        self.refresh()
        return this_provider_data

    def open_provder_detail(self,entry_index = 0) -> providers_detail.ProviderDetail:
        links = self.get_fresh_provider_links()
        links[entry_index].click()
        time.sleep(1)
        this_provider = providers_detail.ProviderDetail(self.driver)
        return this_provider

    def go_to_next_page(self):
        self.next_page_button.click()
        time.sleep(3)
        self.refresh()

    def go_to_previous_page(self):
        self.previous_page_button.click()
        time.sleep(3)
        self.refresh()

    def get_reported_start(self):
        page_readout = self.driver.find_element_by_xpath(self.result_numbers_xpath).text
        dash_i = page_readout.find('-')
        return int(page_readout[0:dash_i])

    def get_reported_end(self):
        page_readout = self.driver.find_element_by_xpath(self.result_numbers_xpath).text
        dash_i = page_readout.find('-')
        space_i = page_readout.find(" ")
        return int(page_readout[dash_i+1:space_i])

    def rows_per_page_10(self):
        self.rows_per_page_dropdown.click()
        rows_dropdown = Dropdown(self.driver)
        rows_dropdown.click_by_index(0)
        time.sleep(3)
        self.refresh()

    def rows_per_page_50(self):
        self.rows_per_page_dropdown.click()
        rows_dropdown = Dropdown(self.driver)
        rows_dropdown.click_by_index(4)
        time.sleep(3)
        self.refresh()

    def open_drivers_home(self):
        self.drivers_button.click()
        time.sleep(1)
        return drivers_home.DriversHome(self.driver)
    
    def open_vehicles_home(self):
        self.vehicles_button.click()
        time.sleep(1)
        return vehicles_home.VehiclesHome(self.driver)



class Filter:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.filter_checkboxes = self.driver.find_elements_by_xpath('//span[@class="MuiTypography-root MuiTypography-body1 MuiListItemText-primary css-yb0lig"]')
        self.clear_button = driver.find_element_by_xpath('//button[@class="MuiButton-root MuiButton-contained MuiButton-containedPrimary MuiButton-sizeMedium MuiButton-containedSizeMedium MuiButton-fullWidth MuiButtonBase-root css-1lzpfma"]')
        self.checkboxes_xpath = '//input[@type="checkbox"]'
        self.checkboxes = self.driver.find_elements_by_xpath(self.checkboxes_xpath)
        self.knob = driver.find_element_by_xpath('//ul[@aria-labelledby="filter-label"]')
        self.tags = ["Clear to transport","Not clear to transport","Active","Not Active",\
            "Wheelchair v. available","Has drug testing","Has supplier diversity"]

    def get_checkbox_states(self):
        checkboxes = self.driver.find_elements_by_xpath(self.checkboxes_xpath)
        states = []
        for c in checkboxes:
            states.append(c.get_attribute('checked'))
        return states

    def click_filter_checkboxes(self,click_list:list[int]):
        for i in click_list:
            self.filter_checkboxes[i].click()
        time.sleep(2)

    def click_clear_button(self):
        self.clear_button.click()

    def close(self):
        action = webdriver.common.action_chains.ActionChains(self.driver)
        action.move_to_element_with_offset(self.knob, -4, 0)
        action.click()
        action.perform()
        time.sleep(1)


