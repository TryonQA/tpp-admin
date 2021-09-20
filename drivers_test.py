import tpp_test_scripts as t
import time

PATH = "C:\Program Files (x86)\ChromeDriver\chromedriver.exe"
## ADJUST ABOVE BASED ON LOCAL INSTALL

creds = open('creds.txt')
creds_data = creds.readline()
comma = creds_data.find(",")
user = creds_data[:comma]
password = creds_data[comma+1:]
creds.close()

dev_url = 'https://tpp-dev.americanlogistics.com/providers'
qa_url = 'https://tpp-qa.americanlogistics.com/providers'

active_url = dev_url

driver = t.init_driver()

t.login_tpp(driver)

#DRIVER CLICK
t.go_to_drivers(driver)
time.sleep(3)

#DRIVER TESTS
t.view_driver_tests(driver)
t.edit_driver_tests(driver)
t.edit_driver_tests_invalid(driver)
t.test_delete_driver(driver)

#DRIVER SEARCHES
t.test_clear_search(driver,t.DRIVER_SEARCH_KEY)

driver_should = ['greg','bell','john','k r']
t.search_test(driver,driver_should,t.DRIVER_SEARCH_KEY)
driver_should_full = ['mohny jind','amber potts','chris sheppard']
t.search_test(driver,driver_should_full,t.DRIVER_SEARCH_KEY,1)
shouldnt = ["zzzz","qqqq","pppp"]
t.search_test(driver,shouldnt,t.DRIVER_SEARCH_KEY,0)

#NAV TESTS
t.run_all_sort_tests(driver)
t.page_entries_test(driver)
t.page_change_test(driver,3)

driver.close()

driver.quit()
