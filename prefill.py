
import tpp_test_scripts as t
import time

driver = t.init_driver()
t.login_tpp(driver)
time.sleep(5)

t.click_entry(driver,0)
t.prefill_providers(driver)