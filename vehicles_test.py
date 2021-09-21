import tpp_test_scripts as t
import time

driver = t.init_driver()

t.login_tpp(driver)

#VEHICLES CLICK
t.go_to_vehicles(driver)
time.sleep(3)

#VIEW TESTS
t.view_vehicle_tests(driver)


#SEARCH TESTS
t.test_clear_search(driver,t.VEHICLE_SEARCH_KEY)

partial_list = ["chev","it 35","2016","ge9","VT","EE"]
t.search_test(driver,partial_list,t.VEHICLE_SEARCH_KEY)

#NAV TESTS
t.run_all_sort_tests(driver)
t.page_entries_test(driver)
t.page_change_test(driver,3)

driver.close()

driver.quit()