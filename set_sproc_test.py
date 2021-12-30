import tpp_test_scripts as t
import time

providers = [
("acloihn transportation co.","auto",None),
("sil transportation co.","doc","Company Permit"),
("abase transportation co.","docexp","Company Permit"),
("eruhny transportation co.","doc","Direct Deposit"),
("cressey° transportation co.","doc","Disclosure of Convictions"),
("b^ra_or-l r+d=j transportation co.","doc","Exhibit C Business Associate Agreement"),
("#stid transportation co.","doc","Insurance Acord 25 (Automobile and General Liability)"),
("b*rl transportation co.","docexp","Insurance Acord 25 (Automobile and General Liability)"),
("m.use transportation co.","doc","Provider Questionnaire"),
("{b|k} transportation co.","doc","Transportation Provider Agreement (TPA) v10.16.2019"),
("uston transportation co.","doc","Voided Check"),
("(cr"+'%'+"d) tran$portation co.","doc","W-9"),
("juck transportation co.","doc","Disclosure of Ownership"),
("ecluck transportation co.","doc","BGC"),
("chebbu transportation co.","doc","Insurance Credentialing List")]

driver = t.init_driver()
t.login_tpp(driver)
time.sleep(5)


for tp in providers:
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

    driver.refresh()
    #print(tp)


driver.close()

driver.quit()