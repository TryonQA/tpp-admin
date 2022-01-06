from selenium import webdriver
import providers_home
import time
import helpers as h

def create_vehicle_test(driver:webdriver.Chrome):
    test_tag = "Create New Vehicle"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        detail_page = providers_page.open_provder_detail()
        vehicles_list = detail_page.get_vehicles_subpage()
        initial_num_vehicles = vehicles_list.vehicle_count
        new_vehicle_data = h.get_vehicle_data()
        vehicles_list.add_vehicle(new_vehicle_data)
        vehicles_list.refresh()
        end_num_vehicles = vehicles_list.vehicle_count
        if end_num_vehicles == initial_num_vehicles +1:
            result = "PASS"
        else:
            result = "FAIL"
            detail += "No new vehicle created"
        detail_page.refresh_buttons()
        detail_page.click_back()

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def vehicle_navigation_test(driver:webdriver.Chrome):
    test_tag = "Vehicle Navigation"
    result = "PASS"
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        vehicles_page = providers_page.open_vehicles_home()
        vehicle_detail = vehicles_page.open_vehicle_detail()
        #vehicle_edit = vehicle_detail.open_edit_form()
        #vehicle_edit.close()
        time.sleep(1)
        vehicle_detail.refresh_buttons()
        vehicle_detail.click_back()
        vehicles_page.refresh()
        vehicles_page.providers_button.click()
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