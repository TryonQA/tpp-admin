
import tpp_test_scripts as t
import time
import sys

args = sys.argv
url = t.qa_url
if len(args) > 1:
    if args[1] == "uat":
        url =t.uat_url
    if args[1] == "dev":
        url = t.dev_url

driver = t.init_driver()
t.login_tpp(driver,url)
time.sleep(5)

t.click_entry(driver,0)
t.prefill_providers(driver)