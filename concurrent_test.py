import time
import tpp_test_scripts as tpp
import threading

def run_test(driver):
    should_full = ['bobby','end','rob','be','transp']
    tpp.hundred_per_page(driver)
    tpp.search_test(driver,should_full,tpp.NAME_SEARCH_KEY,1)
    tpp.test_edit_tp(driver)
    driver.close()
    driver.quit()



how_many = 12
drivers = []
while how_many > 0:
    driver = tpp.init_driver()
    tpp.login_tpp(driver)
    time.sleep(5)
    drivers.append(driver)
    how_many -= 1
    t = threading.Thread(target=run_test,args=(driver,))
    t.start()

"""
for d in drivers:
    t = threading.Thread(target=run_test,args=(d,))
    t.start()
"""
