import time
import tpp_test_scripts as t
import sys

read_only = False

args = sys.argv
url = t.qa_url
if len(args) > 1:
    if args[1] == "uat":
        url =t.uat_url
    if args[1] == "dev":
        url = t.dev_url
""
#t.test_accounting(url)
""
driver = t.init_driver()

t.login_tpp(driver,url)
time.sleep(5)
""

#TP EDIT TESTS
t.test_edit_tp_open_close(driver)
t.test_edit_tp_invalid_field(driver)
t.test_edit_tp(driver)

#TP CREATION TESTS
t.test_create_tp_invalid_field(driver)
t.test_open_close_create_tp(driver)
t.test_create_tp_no_data(driver)
""
t.test_create_tp(driver)



""
#FILTERS
t.run_clear_filter_test(driver)
#running all filter tests is time consuming
#t.run_all_filter_tests(driver)  
t.run_single_filter_test(driver,[1,2,4])
t.run_single_filter_test(driver,[3,4])


#SEARCHES
""
#FULL
""
should_partial = ['bobby','end','rob','be']
t.search_test(driver,should_partial,t.NAME_SEARCH_KEY)
should_full = ["Winmunax Direct Group",'Melissa Medical Transport','Needed For Testing Inc.']
t.search_test(driver,should_full,t.NAME_SEARCH_KEY,1)
shouldnt = ["zzzz"]
t.search_test(driver,shouldnt,t.NAME_SEARCH_KEY,0)
# TODO add accumulator in test function to measure total passes v fails
should_coverage = ["n f","bos","97"]
t.search_test(driver,should_coverage,t.COVERAGE_SEARCH_KEY)
should_full_coverage = ["97239","San Francisco, Los Angeles, San Diego"]
t.search_test(driver,should_full_coverage,t.COVERAGE_SEARCH_KEY)
shouldnt_coverage = ["zzzz"]
t.search_test(driver,shouldnt_coverage,t.COVERAGE_SEARCH_KEY,0)
""

#SEARCH CLEAR
t.test_clear_search(driver,t.COVERAGE_SEARCH_KEY)
t.test_clear_search(driver,t.NAME_SEARCH_KEY)
""
#PROVIDER TESTS
t.view_provider_tests(driver)
""
t.ctt_test(driver,t.TP_KEY)

#DELETE TEST
t.test_delete_tp(driver)
""
#NAV TESTS
t.run_all_sort_tests(driver)

t.page_entries_test(driver)
t.page_change_test(driver,3)

time.sleep(3)

driver.close()


driver.quit()