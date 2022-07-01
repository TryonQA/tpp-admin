import tpp_test_scripts as t
import time
import sys

args = sys.argv
url = t.qa_url
if len(args) > 1:
    if args[1] == "uat":
        url =t.uat_url
    if args[1] == "dev":
        url = t.dev_url

driver = t.init_driver()

t.login_tpp(driver,url)
time.sleep(2)
t.create_drivers(driver,100)

#DRIVER CLICK
t.go_to_drivers(driver)
time.sleep(3)

#DRIVER TESTS
t.view_driver_tests(driver)
t.edit_driver_tests(driver)
t.edit_driver_tests_invalid(driver)

t.ctt_test(driver,t.DRIVER_KEY,False)

t.go_to_drivers(driver)
time.sleep(3)
t.test_delete_driver(driver)
t.go_to_drivers(driver)

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
