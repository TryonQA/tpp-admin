import setup as s
import sys
import login_test
import providers_nav_test
import providers_data_test
import drivers_tests
import vehicles_tests

admin_username, admin_password = s.get_username_and_password()
url = s.parse_url(sys.argv)

driver = s.init_driver(url)
r = s.ResultHandler()

# LOGIN TEST
login_result = login_test.login_test(driver,admin_username,admin_password)
r.handle_results(login_result)

#PROVIDER HOME NAVIGATION TESTS

clear_filter_result = providers_nav_test.filter_clear_test(driver)
r.handle_results(clear_filter_result)

filter_result_a = providers_nav_test.filter_test(driver,[1,2,4])
r.handle_results(filter_result_a)

filter_result_b = providers_nav_test.filter_test(driver,[3,5])
r.handle_results(filter_result_b)

clear_searches_result = providers_nav_test.search_clear_test(driver)
r.handle_results(clear_searches_result)

search_provider_result_partial = providers_nav_test.search_providers_test(driver,"end")
r.handle_results(search_provider_result_partial)

search_provider_result_exact = providers_nav_test.search_providers_test(driver,"Winmunax Direct Group")
r.handle_results(search_provider_result_exact)

search_provider_result_none = providers_nav_test.search_providers_test(driver,"zzzz",False)
r.handle_results(search_provider_result_none)

search_coverage_result_partial = providers_nav_test.search_coverage_area_test(driver,"uni")
r.handle_results(search_coverage_result_partial)

search_coverage_result_exact = providers_nav_test.search_coverage_area_test(driver,"San Francisco, Los Angeles, San Diego")
r.handle_results(search_coverage_result_exact)

search_coverage_result_none = providers_nav_test.search_coverage_area_test(driver,"xxxx",False)
r.handle_results(search_coverage_result_none)

rows_per_page_result = providers_nav_test.rows_per_page_test(driver)
r.handle_results(rows_per_page_result)

next_page_result = providers_nav_test.next_page_test(driver)
r.handle_results(next_page_result)

previous_page_result = providers_nav_test.previous_page_test(driver)
r.handle_results(previous_page_result) #Must run after next page test

open_add_provider_result = providers_nav_test.open_close_add_provider_form_test(driver)
r.handle_results(open_add_provider_result)
""
open_close_provider_edit_result = providers_nav_test.open_close_provider_edit(driver)
r.handle_results(open_close_provider_edit_result)

provider_back_button_result = providers_nav_test.provider_back_button_test(driver)
r.handle_results(provider_back_button_result)

#REVISIT sort test in providers_nav_test

#PROVIDER DATA TESTS
create_provider_no_data_result = providers_data_test.create_provider_no_data_test(driver)
r.handle_results(create_provider_no_data_result)
""
create_provider_invalid_data_result = providers_data_test.create_provider_invalid_data_test(driver)
r.handle_results(create_provider_invalid_data_result)
""
create_provider_result = providers_data_test.create_provider_test(driver)
r.handle_results(create_provider_result)
""
edit_provider_invalid_result = providers_data_test.edit_provider_invalid_test(driver)
r.handle_results(edit_provider_invalid_result)

edit_provider_result = providers_data_test.edit_provider_test(driver)
r.handle_results(edit_provider_result)

provider_document_upload_result = providers_data_test.provider_document_upload_test(driver)
r.handle_results(provider_document_upload_result)

provider_document_edit_result = providers_data_test.provider_document_edit_test(driver)
r.handle_results(provider_document_edit_result)

provider_document_delete_result = providers_data_test.provider_document_delete_test(driver)
r.handle_results(provider_document_delete_result)

#CTT TESTS - TODO - RETURN START STATE FOR SUBSEQUENT TESTS?

# DRIVER TESTS
create_driver_result = drivers_tests.create_driver_test(driver)
r.handle_results(create_driver_result)

driver_navigation_test_result = drivers_tests.driver_navigation_test(driver)
r.handle_results(driver_navigation_test_result)

# VEHICLE TESTS
create_vehicle_result = vehicles_tests.create_vehicle_test(driver)
r.handle_results(create_vehicle_result)

vehicle_navigation_test_result = vehicles_tests.vehicle_navigation_test(driver)
r.handle_results(vehicle_navigation_test_result)

# DELETE TEST
delete_provider_result = providers_data_test.delete_provider_test(driver)
r.handle_results(delete_provider_result)

s.end_session(driver)
