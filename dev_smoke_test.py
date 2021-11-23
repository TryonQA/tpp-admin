import time
import tpp_test_scripts as t

driver = t.init_driver()
t.login_tpp(driver,t.dev_url)
time.sleep(5)

""
""
""
#NAV TESTS
t.page_change_test(driver,3)
t.run_all_sort_tests(driver)
t.page_entries_test(driver)
""
driver.refresh()
time.sleep(3)


t.test_open_close_create_tp(driver)
t.test_create_tp_no_data(driver)
t.test_create_tp(driver)

driver.refresh()
time.sleep(3)
"""
t.test_edit_tp_open_close(driver)
t.test_edit_tp_invalid_field(driver)
t.test_edit_tp(driver)
""

driver.refresh()
time.sleep(3)

t.run_clear_filter_test(driver)
t.run_single_filter_test(driver,[1,2,4])

#LITE
should_partial = ['end']
t.search_test(driver,should_partial,t.NAME_SEARCH_KEY)
should_full = ['Hapjubover Direct Group']
t.search_test(driver,should_full,t.NAME_SEARCH_KEY,1)
# TODO add accumulator in test function to measure total passes v fails
should_coverage = ["bos"]
t.search_test(driver,should_coverage,t.COVERAGE_SEARCH_KEY)
shouldnt_coverage = ["pppp"]
t.search_test(driver,shouldnt_coverage,t.COVERAGE_SEARCH_KEY,0)

t.test_clear_search(driver,t.COVERAGE_SEARCH_KEY)
t.test_clear_search(driver,t.NAME_SEARCH_KEY)
""
""
#PROVIDER TESTS
t.view_provider_tests(driver)
#t.ctt_test(driver,t.TP_KEY)
"""
#DRIVER CLICK
t.go_to_drivers(driver)
time.sleep(3)

#DRIVER TESTS
t.view_driver_tests(driver)
t.edit_driver_tests(driver)
t.edit_driver_tests_invalid(driver)
t.test_delete_driver(driver)
driver.refresh()
""
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

driver.refresh()
time.sleep(3)

#DELETE TEST
t.test_delete_tp(driver)

driver.close()

driver.quit()