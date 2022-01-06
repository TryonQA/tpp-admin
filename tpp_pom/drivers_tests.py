from selenium import webdriver
import providers_home
import time
import helpers as h

def create_driver_test(driver:webdriver.Chrome):
    test_tag = "Create New Driver"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        detail_page = providers_page.open_provder_detail()
        drivers_list = detail_page.get_drivers_subpage()
        initial_num_drivers = drivers_list.driver_count
        new_driver_data = h.get_driver_data()
        drivers_list.add_driver(new_driver_data)
        drivers_list.refresh()
        end_num_drivers = drivers_list.driver_count
        if end_num_drivers == initial_num_drivers +1:
            result = "PASS"
        else:
            result = "FAIL"
            detail += "No new driver created"
        detail_page.refresh_buttons()
        detail_page.click_back()

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def driver_navigation_test(driver:webdriver.Chrome):
    test_tag = "Driver Navigation"
    result = "PASS"
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        drivers_page = providers_page.open_drivers_home()
        driver_detail = drivers_page.open_driver_detail()
        driver_edit = driver_detail.open_edit_form()
        driver_edit.close()
        driver_detail.refresh_buttons()
        driver_detail.click_back()
        drivers_page.refresh()
        drivers_page.providers_button.click()
        # Lack of errors reflects proper navigation

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)


def template_test(driver:webdriver.Chrome):
    test_tag = ""
    result = ""
    detail = ""

    try:
        pass

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

"""

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

"""