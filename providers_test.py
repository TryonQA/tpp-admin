import time
import tpp_test_scripts as t

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
time.sleep(5)

###UNCOMMENT test to run individual tests###

#TP EDIT TESTS
t.test_edit_tp_open_close(driver)
t.test_edit_tp_invalid_field(driver)
t.test_edit_tp(driver)

#TP CREATION TESTS
t.test_create_tp_invalid_field(driver)
t.test_open_close_create_tp(driver)
t.test_create_tp_no_data(driver)
t.test_create_tp(driver)
#t.test_delete_tp(driver)

#FILTERS
t.run_clear_filter_test(driver)
#running all filter tests is time consuming
#t.run_all_filter_tests(driver)  
t.run_single_filter_test(driver,[1,2,4])
t.run_single_filter_test(driver,[3,4])

#SEARCHES
should_partial = ['bobby','end','rob','be','transp']
t.search_test(driver,should_partial,t.NAME_SEARCH_KEY)
should_full = ['Varfropedor Direct','Tupglibilax WorldWide','ubrol transportation co.']
t.search_test(driver,should_full,t.NAME_SEARCH_KEY,1)
shouldnt = ["zzzz","qqqq","pppp"]
t.search_test(driver,shouldnt,t.NAME_SEARCH_KEY,0)
# TODO add accumulator in test function to measure total passes v fails
should_coverage = ["city","all of"]
t.search_test(driver,should_coverage,t.COVERAGE_SEARCH_KEY)
should_full_coverage = ["ifrisenibb city","All of Orgeon State"]
t.search_test(driver,should_full_coverage,t.COVERAGE_SEARCH_KEY)
shouldnt_coverage = ["zzzz","qqqq","pppp"]
t.search_test(driver,shouldnt_coverage,t.COVERAGE_SEARCH_KEY,0)

#SEARCH CLEAR
t.test_clear_search(driver,t.COVERAGE_SEARCH_KEY)
t.test_clear_search(driver,t.NAME_SEARCH_KEY)


#PROVIDER TESTS
t.view_provider_tests(driver)

#NAV TESTS
t.run_all_sort_tests(driver)

t.page_entries_test(driver)
t.page_change_test(driver,3)

time.sleep(3)

driver.close()


driver.quit()