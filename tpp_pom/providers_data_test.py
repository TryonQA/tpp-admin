from selenium import webdriver
import providers_home
import providers_detail
import time
import helpers as h

def create_provider_no_data_test(driver:webdriver.Chrome):
    test_tag = "Create Provider - No Data"
    result = ""
    detail = ""

    try:
        providers_home_page = providers_home.ProvidersHome(driver)
        create_form = providers_home_page.open_add_provider_form()
        create_form.save_form()
        time.sleep(2)
        create_form.refresh()
        if h.check_for_warnings(driver):
            result = "PASS"
            detail += "Warning displayed"

        else:
            result = "FAIL"
            detail += "No warning displayed"
        create_form.close()
    
    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def create_provider_invalid_data_test(driver:webdriver.Chrome):
    test_tag = "Create Provider - Invalid Data"
    result = ""
    detail = ""

    try:
        providers_home_page = providers_home.ProvidersHome(driver)
        create_form = providers_home_page.open_add_provider_form()
        provider_data = h.get_new_provider_data()
        create_form.complete_form(provider_data)

        create_form.invalidate_email()

        create_form.save_form()
        time.sleep(2)
        create_form.refresh()
        if h.check_for_warnings(driver):
            result = "PASS"
            detail += "Warning displayed"
            create_form.close()
            time.sleep(1)

        else:
            result = "FAIL"
            detail += "No warning displayed"
        
        if create_form.check_form_alive():
            create_form.close()
    
    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def create_provider_test(driver:webdriver.Chrome):
    test_tag = "Create Provider"
    result = ""
    detail = ""

    try:
        providers_home_page = providers_home.ProvidersHome(driver)
        create_form = providers_home_page.open_add_provider_form()
        provider_data = h.get_new_provider_data()
        create_form.complete_form(provider_data)

        create_form.save_form()
        time.sleep(2)
        
        if create_form.check_form_alive():
            result = "FAIL"
            detail += "Form remains open"
            create_form.close()

        else:
            new_provider_page = providers_detail.ProviderDetail(driver)
            finished_provider_data = new_provider_page.get_data()
            new_provider_page.click_back()
            #differences = h.compare_provider_data(provider_data,finished_provider_data)
            if finished_provider_data["TransportationProviderName"] == provider_data["TransportationProviderName"]\
                and finished_provider_data["AccountNumber"] == provider_data["AccountNumber"]\
                    and finished_provider_data["IsActive"] == provider_data["IsActive"]:
                result = 'PASS'
                detail += finished_provider_data["TransportationProviderName"] + " created successfully"
            else:
                result = "FAIL"
                detail += "Problem with Provider creation "+str(finished_provider_data)
    
    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def edit_provider_invalid_test(driver:webdriver.Chrome):
    test_tag = "Edit Provider - Invalid Data"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        detail_page = providers_page.open_provder_detail()
        edit_form = detail_page.open_edit_form()
        edit_form.invalidate_email()

        edit_form.save_form()
        time.sleep(2)
        edit_form.refresh()
        if h.check_for_warnings(driver):
            result = "PASS"
            detail += "Warning displayed"
            edit_form.close()
            time.sleep(1)

        else:
            result = "FAIL"
            detail += "No warning displayed"
        
        if edit_form.check_form_alive():
            edit_form.close()

        detail_page.refresh_buttons()
        detail_page.click_back()

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def edit_provider_test(driver:webdriver.Chrome):
    test_tag = "Edit Provider"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        detail_page = providers_page.open_provder_detail()
        edit_form = detail_page.open_edit_form()
        
        new_name = h.get_random_name() + "-" +h.get_random_name()
        key_for_test = "MainContactLastName"

        edit_form.change_field(new_name,key_for_test)

        edit_form.save_form()
        time.sleep(2)
        if edit_form.check_form_alive():
            edit_form.close()
            result = "FAIL"
            detail += "Save failed. "

        detail_page.refresh_buttons()
        final_data = detail_page.get_data()
        detail_page.click_back()

        if final_data[key_for_test] == new_name:
            result = "PASS"
        else:
            result = "FAIL"
            detail += "Data unchanged."

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def provider_document_upload_test(driver:webdriver.Chrome):
    test_tag = "Document Upload - Provider"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        detail_page = providers_page.open_provder_detail()
        documents = detail_page.get_documents_subpage()
        initial_state = documents.document_states
        documents.upload_top_open_document()
        documents.refresh()
        final_state = documents.document_states
        index_to_check = 0
        for s in initial_state:
            if s != None:
                break
            index_to_check+=1
        if final_state[index_to_check] == None:
            result = "PASS"
        else:
            result = "FAIL"
            detail += "Trouble uploading document - "+initial_state[index_to_check] 
        detail_page.refresh_buttons()
        detail_page.click_back()

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def provider_document_edit_test(driver:webdriver.Chrome):
    test_tag = "Document Edit - Provider"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        detail_page = providers_page.open_provder_detail()
        documents = detail_page.get_documents_subpage()
        if len(documents.edit_buttons) > 0:
            start_detail = documents.get_top_document_detail()
            documents.edit_document()
            end_detail = documents.get_top_document_detail()
            if start_detail != end_detail:
                result = "PASS"
            else:
                result = "FAIL"
                detail += "Edits failed"
        else:
            result = "FAIL"
            detail += "No documents uploaded to edit"
        
        detail_page.refresh_buttons()
        detail_page.click_back()

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def provider_document_delete_test(driver:webdriver.Chrome):
    test_tag = "Document Delete - Provider"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        detail_page = providers_page.open_provder_detail()
        documents = detail_page.get_documents_subpage()
        initial_state = documents.document_states
        documents.delete_document()
        documents.refresh()
        final_state = documents.document_states
        index_to_check = 0
        for s in initial_state:
            if s == None:
                break
            index_to_check+=1
        if final_state[index_to_check] != None:
            result = "PASS"
        else:
            result = "FAIL"
            detail += "Trouble deleting document"
        detail_page.refresh_buttons()
        detail_page.click_back()

    except Exception as e:
        result = "FAIL"
        detail = e
        h.refresh_site(driver)

    return (result,test_tag,detail)

def delete_provider_test(driver:webdriver.Chrome):
    test_tag = "Delete Provider"
    result = ""
    detail = ""

    try:
        providers_page = providers_home.ProvidersHome(driver)
        target_data = providers_page.get_top_provider_data()
        providers_page.delete_provider()
        time.sleep(1)
        providers_page.refresh()
        after_data = providers_page.get_top_provider_data()
        if target_data["TransportationProviderName"] != after_data["TransportationProviderName"]:
            result = "PASS"
        else:
            result = "FAIL"
            detail += target_data["TransportationProviderName"] + "not deleted."
        
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

#PROVIDER TESTS

    #ADD DRIVER

    #ADD VEHICLE

t.ctt_test(driver,t.TP_KEY)

#DELETE TEST
t.test_delete_tp(driver)
"""