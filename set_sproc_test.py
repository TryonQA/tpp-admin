import tpp_test_scripts as t
import time

providers = [
("ustabb transportation co.","auto",None),
("muga transportation co.","doc","Company Permit"),
("chute transportation co.","docexp","Company Permit"),
("cate transportation co.","doc","Direct Deposit"),
("chun transportation co.","doc","Disclosure of Convictions"),
("suck transportation co.","doc","Exhibit C Business Associate Agreement"),
("gab transportation co.","doc","Insurance Acord 25 (Automobile and General Liability)"),
("gitt transportation co.","docexp","Insurance Acord 25 (Automobile and General Liability)"),
("jitt transportation co.","doc","Provider Questionnaire"),
("nugget transportation co.","doc","Transportation Provider Agreement (TPA) v10.16.2019"),
("jute transportation co.","doc","Voided Check"),
("gresea transportation co.","doc","W-9"),
("imicky transportation co.","doc","Disclosure of Ownership"),
("ceg transportation co.","doc","BGC"),
("cig transportation co.","doc","Insurance Credentialing List")]

driver = t.init_driver()
t.login_tpp(driver)
time.sleep(5)


for tp in providers:
    try:
        driver.find_element_by_xpath('//button[@data-testid="clear"]').click()
    except:
        print('button disabled')
    t.text_to_search(driver,tp[0],t.NAME_SEARCH_KEY)
    time.sleep(3)
    t.click_entry(driver,0)
    time.sleep(2)

    if tp[1] == "auto":
        t.tp_future_auto_ins(driver)
    elif tp[1] == "docexp":
        t.edit_doc_by_title(driver,tp[2],False)

    t.click_documents(driver)
    t.upload_all_docs(driver)
    data = t.get_current_company_data(driver)
    ctt_status = data["IsClearToTransport"]
    if not ctt_status:
        t.toggle_ctt(driver)
        time.sleep(2.5)

    if tp[1] == "doc":
        t.delete_doc_by_title(driver,tp[2])
    elif tp[1] == "docexp":
        t.edit_doc_by_title(driver,tp[2])
    else:
        t.tp_past_auto_ins(driver)

    t.back_to_providers(driver)
    time.sleep(2)
    #print(tp)


driver.close()

driver.quit()