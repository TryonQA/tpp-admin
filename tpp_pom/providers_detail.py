from selenium import webdriver
import time
import providers_form
import drivers_form
import vehicles_form
import helpers as h

class InsuranceSub:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.insurance_data_raw = self.driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-item MuiGrid-grid-sm-12 MuiGrid-grid-md-6 MuiGrid-grid-lg-3 css-1mrm2vh"]/div/div/div[2]')

class DriversSub:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.refresh()

    def refresh(self):
        self.add_button = self.driver.find_element_by_xpath('//button[contains(text(),"Add Driver")]')
        self.driver_count = len(self.driver.find_element_by_xpath('//div[@class="MuiDataGrid-virtualScrollerRenderZone css-12efcmn"]').find_elements_by_xpath('.//div[@role="row"]'))

    def add_driver(self,new_driver_dictionary):
        self.add_button.click()
        time.sleep(0.5)
        form = drivers_form.DriverForm(self.driver)
        form.complete_form(new_driver_dictionary)
        form.save_form()
        if form.check_form_alive():
            form.close()
        else:
            time.sleep(1)
            back_button = self.driver.find_element_by_xpath('//a[contains(text(), "Back")]')
            back_button.click()
            time.sleep(2)


class VehiclesSub:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.refresh()
    
    def refresh(self):
        self.add_button = self.driver.find_element_by_xpath('//button[contains(text(),"Add Vehicle")]')
        self.vehicle_count = len(self.driver.find_element_by_xpath('//div[@class="MuiDataGrid-virtualScrollerRenderZone css-12efcmn"]').find_elements_by_xpath('.//div[@role="row"]'))

    def add_vehicle(self,new_vehicle_dictionary):
        self.add_button.click()
        time.sleep(0.5)
        form = vehicles_form.VehicleForm(self.driver)
        form.complete_form(new_vehicle_dictionary)
        form.save_form()
        if form.check_form_alive():
            form.close()
        else:
            time.sleep(1)
            back_button = self.driver.find_element_by_xpath('//a[contains(text(), "Back")]')
            back_button.click()
            time.sleep(2)

class DocumentsSub:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.doc_entry_xpath = '//div[@data-field="DocumentTypeName"]'
        self.refresh()

    def refresh(self):
        self.document_states = self.get_document_upload_states() #TODO
        self.edit_buttons = self.driver.find_elements_by_xpath('//button[@aria-label="edit" and not(@disabled)]')  
        self.delete_buttons = self.driver.find_elements_by_xpath('//button[@aria-label="delete" and not(@disabled)]')
        self.add_document_button = self.driver.find_element_by_xpath('//button[contains(text(),"Add Document")]')

    def upload_top_open_document(self):
        doc_index = 0
        if len(self.document_states) > 0:
            for state in self.document_states:
                if state != None:
                    break
                doc_index += 1
            self.document_upload(self.document_states[doc_index])
            time.sleep(1)
        else:
            self.document_upload(None)

    def open_upload(self) -> h.DocPopUp:
        self.add_document_button.click()
        time.sleep(1)
        return h.DocPopUp(self.driver)

    def get_parent_row(self,edit_button_index=0):
        parents = self.driver.find_elements_by_xpath('//button[@aria-label="edit" and not(@disabled)]//ancestor::div[2]')
        return parents[edit_button_index].get_attribute("data-rowindex")


    def get_top_document_detail(self):
        row = self.get_parent_row()
        signedOn = self.driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div[3]').text
        effectiveStart = self.driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div[4]').text
        effectiveEnd = self.driver.find_element_by_xpath('//div[@data-rowindex="'+str(row)+'"]/div[5]').text
        return (signedOn,effectiveStart,effectiveEnd)

    def edit_document(self,doc_index=0):
        self.edit_buttons[doc_index].click()
        time.sleep(1)
        doc_popup = h.DocPopUp(self.driver)
        doc_popup.edit_dates()
        time.sleep(1)
        doc_popup.click_save()
        time.sleep(1)
        self.refresh()

    def delete_document(self,doc_index=0):
        self.delete_buttons[doc_index].click()
        time.sleep(1)
        yes_button = self.driver.find_element_by_xpath('//button[contains(text(),"Yes")]')
        yes_button.click()
        time.sleep(1)

    def document_upload(self,doc_label):
        upload_popup = self.open_upload()
        if doc_label != None:
            upload_popup.select_doc_type(doc_label)
        upload_popup.add_valid_dates()
        upload_popup.set_file()
        upload_popup.click_save()
        time.sleep(3)

    def get_document_upload_states(self):
        self.driver.implicitly_wait(0.5)
        states = []
        doc_entries = self.driver.find_elements_by_xpath(self.doc_entry_xpath)
        doc_entries = doc_entries[1:]
        for d in doc_entries:
            if len(d.find_elements_by_xpath('.//a[@target="_blank"]')) > 0:
                states.append(None)
            else:
                states.append(d.find_element_by_xpath('.//div').text)
            doc_entries = self.driver.find_elements_by_xpath(self.doc_entry_xpath)
            doc_entries = doc_entries[1:]
        self.driver.implicitly_wait(5)
        return states

class ProviderDetail:
    def __init__(self,driver:webdriver.Chrome):
        self.driver = driver
        self.refresh_buttons()

    def refresh_buttons(self):
        self.info_button = self.driver.find_element_by_xpath('//button[contains(text(),"Transportation info")]')
        self.documents_button = self.driver.find_element_by_xpath('//button[contains(text(),"Documents")]')
        self.insurance_button = self.driver.find_element_by_xpath('//button[contains(text(),"Insurance")]')

        self.drivers_button = self.driver.find_element_by_xpath('//button[contains(text(),"Drivers")]')
        self.vehicles_button = self.driver.find_element_by_xpath('//button[contains(text(),"Vehicles")]')
        self.notes_button = self.driver.find_element_by_xpath('//button[contains(text(),"Notes")]')

        self.edit_button = self.driver.find_element_by_xpath('//button[contains(text(),"Edit")]')
        self.back_button = self.driver.find_element_by_xpath('//a[contains(text(), "Back")]')

    def get_insurance_subpage(self) -> InsuranceSub:
        self.insurance_button.click()
        self.refresh_buttons()
        time.sleep(1)
        return InsuranceSub(self.driver)

    def get_documents_subpage(self) -> DocumentsSub:
        self.documents_button.click()
        self.refresh_buttons()
        time.sleep(1)
        return DocumentsSub(self.driver)

    def get_drivers_subpage(self) -> DriversSub:
        self.drivers_button.click()
        self.refresh_buttons()
        time.sleep(1)
        return DriversSub(self.driver)

    def get_vehicles_subpage(self) -> VehiclesSub:
        self.vehicles_button.click()
        self.refresh_buttons()
        time.sleep(1)
        return VehiclesSub(self.driver)

    def click_back(self):
        self.back_button.click()

    def open_edit_form(self) -> providers_form.ProviderForm:
        self.refresh_buttons()
        self.edit_button.click()
        time.sleep(1)
        edit_form = providers_form.ProviderForm(self.driver)
        return edit_form

    def get_data(self):
        data = self.driver.find_elements_by_xpath('//div[@class="MuiGrid-root MuiGrid-container MuiGrid-spacing-xs-2 css-isbt42"]/div/div/div/div')
        l_data_text = []
        test = 0
        for ld_pt in data:
            #print(str(test)+" - "+ld_pt.text)
            l_data_text.append(ld_pt.text)
            test+=1

        #buttons = driver.find_elements_by_xpath('//button[@class="MuiButtonBase-root MuiTab-root MuiTab-textColorPrimary MuiTab-fullWidth"]')
        insurance_sub = self.get_insurance_subpage()
        ins_data = insurance_sub.insurance_data_raw
        ins_data_text = []
        i_test = 0
        for i_pt in ins_data:
            #print("ins-"+str(i_test)+" - "+i_pt.text)
            ins_data_text.append(i_pt.text)
            i_test += 1
        #this_co_data = [data_text[5],[ins_data_text[6],ins_data_text[7],ins_data_text[8]],data_text[4],data_text[6],data_text[7],this_co_name]

        this_co_data = {
            "TransportationProviderName":l_data_text[1],
            "EmailAddress":l_data_text[3],
            "MainContactFirstName":l_data_text[5],
            "MainContactLastName":l_data_text[7],
            "AddressLine1":l_data_text[9],
            "City":l_data_text[13],
            "ZipCode":l_data_text[17],
            "County":l_data_text[19],
            "MainPhone":h.strip_non_numeric(l_data_text[21])[1:],
            "DispatchPhone":h.strip_non_numeric(l_data_text[23])[1:],
            "MessagingMethod":l_data_text[25],
            "BillingContactFirstName":l_data_text[27],
            "BillingContactLastName":l_data_text[29],
            "BillingEmailAddress":l_data_text[41],
            "BillingAddressLine1":l_data_text[31],
            "BillingCity":l_data_text[35],
            "BillingZipCode":l_data_text[39],
            "AccountNumber":l_data_text[43],
            "BillingPhone":h.strip_non_numeric(l_data_text[45])[1:],
            "OwnerFirstName":l_data_text[57],
            "OwnerLastName":l_data_text[59],
            "OwnerEmailAddress":l_data_text[61],
            "OwnerPhone":h.strip_non_numeric(l_data_text[63])[1:],
            "EmployerIdentificationNumber":l_data_text[53],
            "LegalEntityBusinessName":l_data_text[55],
            "PhysicalAddressLine1":l_data_text[73],
            "PhysicalCity":l_data_text[77],
            "PhysicalZipCode":l_data_text[81],
            "NPINumber":l_data_text[105],
            "CommercialInsuranceCompanyName":ins_data_text[0],
            "CommercialInsurancePolicyNumber":ins_data_text[1],
            "CommercialAggregateAmount":h.strip_non_numeric(ins_data_text[4])[:-2],
            "AutoInsuranceCompanyName":ins_data_text[5],
            "AutoInsurancePolicyNumber":ins_data_text[6],
            "AutoBodilyInjuryPerson":h.strip_non_numeric(ins_data_text[9])[:-2],
            "AutoBodilyInjuryAccident":h.strip_non_numeric(ins_data_text[10])[:-2],
            "AutoPropertyDamage":h.strip_non_numeric(ins_data_text[11])[:-2],
            "AutoCombinedLimit":h.strip_non_numeric(ins_data_text[12])[:-2],
            "CoverageAreas":l_data_text[109],
            
            #dropdowns
            "State": l_data_text[15],
            "BillingState": l_data_text[37],
            "LegalEntityStateCode": l_data_text[67],
            "PhysicalState": l_data_text[79],
            "LegalEntityTypeID": l_data_text[69],
            "LegalEntityStatusID": l_data_text[71],
            "TransportationProviderTypeID": l_data_text[83],
            "TransportationProviderTierID": l_data_text[85],
            "CommercialInsuranceStrengthID": ins_data_text[3],
            "AutoInsuranceStrengthID": ins_data_text[8],
            
            #ADD BANK
            "BankName": l_data_text[47],
            "BankAccountNumber": l_data_text[51],
            "BankRoutingNumber": l_data_text[49],

            #checkboxes
            "HasReceivedProviderManual": h.parse_yes_no(l_data_text[87]),
            "HasWheelchairVehiclesAvailable": h.parse_yes_no(l_data_text[91]),
            "HasReceivedNEMTProviderManual": h.parse_yes_no(l_data_text[101]),
            "HasSupplierDiversity": h.parse_yes_no(l_data_text[97]),
            "HasRegulatedDrugTesting": h.parse_yes_no(l_data_text[95]),
            "IsClearToTransport": h.parse_yes_no(l_data_text[93]),
            "IsActive": h.parse_yes_no(l_data_text[99]),
            "IsCompliant": h.parse_yes_no(l_data_text[103]),
            "HasWorkersComp": h.parse_yes_no(ins_data_text[13])
        }

        return this_co_data


