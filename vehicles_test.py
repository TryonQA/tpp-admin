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
t.create_vehicles(driver,1)

#VEHICLES CLICK
t.go_to_vehicles(driver)
time.sleep(3)

#VIEW TESTS
t.view_vehicle_tests(driver)
t.edit_vehicle_tests(driver)
t.edit_vehicle_tests_invalid(driver)
t.test_delete_vehicle(driver)

t.ctt_test(driver,t.VEHICLE_KEY,False)
t.go_to_vehicles(driver)

#SEARCH TESTS
t.test_clear_search(driver,t.VEHICLE_SEARCH_KEY)

partial_list = ["EE","chev","it 35","2016","ge9","VT"]
t.search_test(driver,partial_list,t.VEHICLE_SEARCH_KEY)
exact_list = ["2C4RDGBG9FR725352","1FTYE1CMXHKB35284","75293J2","7ZPV112"]
t.search_test(driver,exact_list,t.VEHICLE_SEARCH_KEY,1)
none_list = ["zzzz","qqqq","pppp"]
t.search_test(driver,none_list,t.VEHICLE_SEARCH_KEY,0)

#NAV TESTS
t.run_all_sort_tests(driver)
t.page_entries_test(driver)
t.page_change_test(driver,3)

driver.close()

driver.quit()
