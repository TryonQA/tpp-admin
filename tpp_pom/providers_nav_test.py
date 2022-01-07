import providers_home
from selenium import webdriver
import helpers as h
import time

def filter_clear_test(driver:webdriver.Chrome):
    test_tag = "Clear Filter Button"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        filter_popup: providers_home.Filter = providers_page.open_filter()
        original_checkbox_state = filter_popup.get_checkbox_states()
        filter_popup.click_filter_checkboxes([1,3,5])
        clicked_checkbox_state = filter_popup.get_checkbox_states()
        filter_popup.click_clear_button()
        final_checkbox_state = filter_popup.get_checkbox_states()
        filter_popup.close()
        if final_checkbox_state == original_checkbox_state and \
            final_checkbox_state != clicked_checkbox_state:
            result = "PASS"
        else:
            result = "FAIL"
    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)


def filter_test(driver:webdriver.Chrome, filter_list):
    test_tag = "Filter Results"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        filter_popup: providers_home.Filter = providers_page.open_filter()
        filter_popup.click_filter_checkboxes(filter_list)
        for t in filter_list:
            test_tag += " - " + filter_popup.tags[t]
        time.sleep(3)
        filter_popup.close()
        time.sleep(5)
        filtered_providers_page = providers_home.ProvidersHome(driver)
        provider_data = filtered_providers_page.get_all_providers_data()
        filter_popup: providers_home.Filter = filtered_providers_page.open_filter()
        filter_popup.click_clear_button()
        filter_popup.close()
        passing_providers = 0
        for d_list in provider_data:
            this_pass = True
            if 0 in filter_list:
                if d_list["IsClearToTransport"] != True:
                    this_pass = False
                    detail += d_list["TransportationProviderName"] + " not CTT "
            if 1 in filter_list:
                if d_list["IsClearToTransport"] != False:
                    this_pass = False
                    detail += d_list["TransportationProviderName"] + " CTT "
            if 2 in filter_list:
                if d_list["IsActive"] != True:
                    this_pass = False
                    detail += d_list["TransportationProviderName"] + " not Active "
            if 3 in filter_list:
                if d_list["IsActive"] != False:
                    this_pass = False
                    detail += d_list["TransportationProviderName"] + " Active "
            if 4 in filter_list:
                if d_list["HasWheelchairVehiclesAvailable"] != True:
                    this_pass = False
                    detail += d_list["TransportationProviderName"] + " not Wheelchair Avail. "
            if 5 in filter_list:
                if d_list["HasRegulatedDrugTesting"] != True:
                    this_pass = False
                    detail += d_list["TransportationProviderName"] + " not Drug Tested "
            if 6 in filter_list:
                if d_list["HasSupplierDiversity"] != True:
                    this_pass = False
                    detail += d_list["TransportationProviderName"] + " not Has Diversity "
            if this_pass:
                passing_providers+=1

        if len(provider_data) > 0:
            test_score = (passing_providers/len(provider_data))
            if test_score >= 1.0:
                result = "PASS"
            else:
                result = "FAIL"
        else:
            detail = "Filter yields no results"
            result = "PASS"

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def search_providers_test(driver:webdriver.Chrome,text_to_search,results_expected = True):
    test_tag = "Provider Search: " + text_to_search
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        providers_page.provider_search(text_to_search)

        search_results = providers_page.get_all_providers_data()
        providers_page.clear_provider_search()

        to_search_to_check = text_to_search.lower()
        passing_results = 0
        for r in search_results:
            if to_search_to_check in r["TransportationProviderName"].lower() or to_search_to_check in r["OwnerFirstName"].lower() or \
                to_search_to_check in r["OwnerLastName"].lower() or to_search_to_check in r["LegalEntityBusinessName"].lower():
                passing_results += 1
            else:
                detail += r["TransportationProviderName"] + " incorrectly returned. "
        
        if len(search_results) > 0:
            if results_expected:
                test_score = (passing_results/len(search_results))
                if test_score >= 1.0:
                    result = "PASS"
                else:
                    result = "FAIL"
            else:
                result = "FAIL"
                detail += "Unexpected results"

        else:
            detail += "Search returns no results"
            if results_expected:
                result = "FAIL"
            else:
                result = "PASS"
    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def search_coverage_area_test(driver:webdriver.Chrome,text_to_search,results_expected = True):
    test_tag = "Coverage Search: " + text_to_search
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        providers_page.coverage_search(text_to_search)

        search_results = providers_page.get_all_providers_data()
        providers_page.clear_coverage_search()

        to_search_to_check = text_to_search.lower()
        passing_results = 0
        for r in search_results:
            if to_search_to_check in r["CoverageAreas"].lower():
                passing_results += 1
            else:
                detail += r["TransportationProviderName"] + " incorrectly returned. "
        
        if len(search_results) > 0:
            if results_expected:
                test_score = (passing_results/len(search_results))
                if test_score >= 1.0:
                    result = "PASS"
                else:
                    result = "FAIL"
            else:
                result = "FAIL"
                detail += "Unexpected results"

        else:
            detail += "Search returns no results"
            if results_expected:
                result = "FAIL"
            else:
                result = "PASS"
    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def search_clear_test(driver:webdriver.Chrome):
    test_tag = "Search Clear"
    result = "PASS"
    detail = ""

    try:

        providers_page = providers_home.ProvidersHome(driver)
        providers_page.coverage_search("Testing clear button")
        providers_page.provider_search("Testing clear button")

        time.sleep(1)

        providers_page.clear_coverage_search()
        providers_page.clear_provider_search()

        p_search_text = providers_page.provider_search_field.get_attribute('value')
        c_search_text = providers_page.coverage_search_field.get_attribute('value')

        if p_search_text != "":
            result = "FAIL"
            detail += "Provider search: "+p_search_text+" "
        if c_search_text != "":
            result = "FAIL"
            detail += "Coverage search: "+c_search_text+" "
    
    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def sort_test(driver:webdriver.Chrome):
    test_tag = "Sorting - Providers"
    result = ""
    detail = ""

    #TODO

    return (result,test_tag,detail)

def rows_per_page_test(driver:webdriver.Chrome):
    test_tag = "Changing Rows Per Page"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        providers_page.rows_per_page_50()
        if providers_page.num_providers == 50:
            result = "PASS"
        else:
            result = "FAIL"
            detail += str(providers_page.num_providers) + " results returned instead of 50 "
        
        if result == "PASS":
            providers_page.rows_per_page_10()
            if providers_page.num_providers == 10:
                result = "PASS"
            else:
                result = "FAIL"
                detail += str(providers_page.num_providers) + " results returned instead of 10 "

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

    return (result,test_tag,detail)

def next_page_test(driver:webdriver.Chrome):
    test_tag = "Next Page - Providers"
    result = "PASS"
    detail = ""

    try:

        providers_page = providers_home.ProvidersHome(driver)
        start_provider_name = providers_page.get_fresh_provider_links()[0].text
        start_last_num = providers_page.get_reported_end()

        providers_page.go_to_next_page()
        time.sleep(2)

        end_provider_name = providers_page.get_fresh_provider_links()[0].text
        end_first_num = providers_page.get_reported_start()

        if end_first_num != start_last_num+1:
            result = "FAIL"
            detail += str(start_last_num) + " v. " + str(end_first_num)

        if start_provider_name == end_provider_name:
            result = "FAIL"
            detail += "Results unchanged"

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def previous_page_test(driver:webdriver.Chrome):
    test_tag = "Previous Page - Providers"
    result = "PASS"
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        start_provider_name = providers_page.get_fresh_provider_links()[0].text
        start_first_num = providers_page.get_reported_start()

        providers_page.go_to_previous_page()
        time.sleep(2)

        end_provider_name = providers_page.get_fresh_provider_links()[0].text
        end_last_num = providers_page.get_reported_end()

        if start_first_num != end_last_num+1:
            result = "FAIL"
            detail += str(start_first_num) + " v. " + str(end_last_num)

        if start_provider_name == end_provider_name:
            result = "FAIL"
            detail += "Results unchanged"
    
    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def open_close_add_provider_form_test(driver:webdriver.Chrome):
    test_tag = "Add Provider Navigation"
    result = "FAIL"
    detail = ""
    try: 
        providers_page = providers_home.ProvidersHome(driver)
        form = providers_page.open_add_provider_form()
        time.sleep(1)

        header_text = form.header_text
        if header_text == "Add Provider":
            result = "PASS"
        else:
            detail += "Form not reached. "

        form.close()
        if len(driver.find_elements_by_xpath('//h6')) != 0:
            result = "FAIL"
            detail += "Form not closed. "
    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def open_close_provider_edit(driver:webdriver.Chrome):
    test_tag = "Edit Provider Naviagation"
    result = "FAIL"
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        detail_page = providers_page.open_provder_detail()
        edit_form = detail_page.open_edit_form()
        header_text = edit_form.header_text
        if header_text == "Update Provider":
            result = "PASS"
        else:
            detail += "Form not reached. "
        edit_form.close()
        if len(driver.find_elements_by_xpath('//h6')) != 0:
            result = "FAIL"
            detail += "Form not closed. "
        detail_page.refresh_buttons()
        detail_page.click_back()

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def provider_back_button_test(driver:webdriver.Chrome):
    test_tag = "Provider Back Button"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        first_provider_name = providers_page.get_fresh_provider_links()[0].text
        detail_page = providers_page.open_provder_detail()
        if detail_page.get_data()["TransportationProviderName"] == first_provider_name:
            result = "PASS"
        else:
            result = "FAIL"
            detail += "Failed to reach provider detail "
        detail_page.click_back()
        providers_page.refresh()
        if len(providers_page.get_fresh_provider_links())==0:
            result = "FAIL"
            detail += "Back did not return home "
            h.refresh_site(driver)

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
