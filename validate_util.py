import time
import tpp_test_scripts as t


def is_expired(date_string,today_string):
    expired = False
    date_year = int(date_string[-4:])
    d_f_s = date_string.find("/")
    date_month = int(date_string[:d_f_s])
    d_s_s = date_string.find("/",d_f_s+1)
    date_date = int(date_string[d_f_s+1:d_s_s])


    today_year = int(today_string[-4:])
    t_f_s = today_string.find("/")
    today_month = int(today_string[:t_f_s])
    t_s_s = today_string.find("/",t_f_s+1)
    today_date = int(today_string[t_f_s+1:t_s_s])

    if date_year < today_year:
        expired = True
    else:
        if date_year == today_year:
            if date_month < today_month:
                expired = True
            else:
                if date_month == today_month:
                    if date_date <= today_date:
                        expired = True
    return expired

def reformat_date(raw_date):
    date = ""
    m=raw_date[5:7]
    y= raw_date[:4]
    d= raw_date[-2:]
    if d[0]=="0":
        d=d[-1]
    if m[0]=="0":
        m=m[-1]
    date = m+"/"+d+"/"+y
    return date

def add_space(provider):
    return provider.replace(" ","  ")


""

today = "10/25/2021"

driver = t.init_driver()
t.login_tpp(driver,t.qa_url)
time.sleep(5)

email_text = open('email_text.txt')

provider = " start!!test"
this_fail = True
not_in_db = False
for line in email_text:
    if "Missing" not in line and "Expired" not in line and "expires" not in line:
        
        if this_fail == False:
            print("**" + provider + " passed**")
        else:
            print("!!! " + provider + " FAILED !!!")
        driver.refresh()
        provider = line[:-1]
        print("")
        print(provider)
        print("   validating:")
        t.text_to_search(driver,provider,t.NAME_SEARCH_KEY)
        search_not_done = True
        tries = 3
        while search_not_done and tries > 0:
            time.sleep(2)
            entries = t.get_company_entries(driver)
            if len(entries)>0:
                if entries[0].text[:4] == provider[:4]:
                    search_not_done = False
                else:
                    driver.refresh()
                    t.text_to_search(driver,provider,t.NAME_SEARCH_KEY)
            tries -= 1
        if len(t.get_company_entries(driver)) == 0:
            provider = add_space(provider)
            driver.refresh()
            time.sleep(1)
            t.text_to_search(driver,provider,t.NAME_SEARCH_KEY)
            time.sleep(4)

        if len(t.get_company_entries(driver)) > 0:
            t.click_entry(driver,0)
            time.sleep(3)
            this_fail = False
            ctt = t.get_ctt(driver)
            active = t.get_active(driver)
            #print(ctt)
            #print(active)
            not_in_db = False
            t.click_documents(driver)
            time.sleep(4)
            doc_states = []
            doc_states = t.get_document_upload_states(driver)
            #print(doc_states)
            doc_exp = []
            aute_exp = t.get_comm_auto_exp(driver)
            #print(aute_exp)
            if active != "Active":
                print("FAIL!! - " + provider + " not ACTIVE")
                this_fail = True
            if ctt != "No":
                print("FAIL!! - " + provider + " already CTT")
                this_fail = True
        else:
            this_fail = True
            print(provider + " NOT IN DB!!")
            not_in_db = True
    else:
        if not not_in_db:
            if "Commercial Auto Insurance" in line:
                if "expires" in line:
                    first_edit = line[:-1]
                    raw_date=first_edit[-10:]
                    exp = reformat_date(raw_date)
                    if exp != aute_exp:
                        print("FAIL!! - " + aute_exp + " auto ins exp. doesn't match ("+exp+")")
                        this_fail = True        
                    
                else:
                    expired = is_expired(aute_exp,today)
                    if expired:
                        print("    Commercial Auto Insurance confirmed Expired")
                    else:
                        print("FAIL! - Commercial Auto Insurance has current exp date of "+aute_exp)
                        this_fail = True
            else:
                if "expires" in line:
                    first_edit = line[:-1]
                    raw_date=first_edit[-10:]
                    exp = reformat_date(raw_date)

                    doc_i = line.find(' expires')
                    doc_type = line[:doc_i]
                    t.click_documents(driver)
                    row = t.get_doc_row(driver,doc_type)
                    #check expired
                    effectiveEnd = driver.find_element_by_xpath('//div[@data-field="EffectiveEndDate" and @data-rowindex="'+str(row)+'"]').text

                    if exp != effectiveEnd:
                        print("FAIL!! - " + effectiveEnd + " "+ doc_type +" exp. doesn't match ("+exp+")")
                        this_fail = True
                else:    
                    if " Missing" in line:   
                        doc_type = line[:-1].removesuffix(" Missing")             
                        if doc_type in doc_states:
                            print("    "+doc_type + " confirmed Missing")
                        else:
                            print("FAIL! - "+doc_type+" reported missing UPLOADED")
                            this_fail = True
                    else:
                        doc_type = line[:-1].removesuffix(" Expired")
                        t.click_documents(driver)
                        row = t.get_doc_row(driver,doc_type)
                        #check expired
                        effectiveEnd = driver.find_element_by_xpath('//div[@data-field="EffectiveEndDate" and @data-rowindex="'+str(row)+'"]').text
                        #print(effectiveEnd)
                        expired = is_expired(effectiveEnd,today)
                        if expired:
                            print("    "+doc_type + " confirmed Expired")
                        else:
                            print("FAIL! - "+doc_type+" has current exp date of "+effectiveEnd)
                            this_fail = True

""



driver.close()

driver.quit()





email_text.close()