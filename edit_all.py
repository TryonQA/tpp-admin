import tpp_test_scripts as t
import time

driver = t.init_driver()

t.login_tpp(driver)
time.sleep(2)

t.hundred_per_page(driver)
time.sleep(4)

t.text_to_search(driver,"tryon-qa-gb",t.NAME_SEARCH_KEY)
num_results = len(t.get_company_entries(driver))

for i in range(num_results):
    t.click_entry(driver,i)
    time.sleep(2)

    # DO WHATEVER HERE
    num_drivers = t.row_counter(driver)
    driver_names = t.get_all_driver_names(driver)
    print(driver_names)
    for di in range(num_drivers):
        if "tryon-qa-gb" not in driver_names[di]:
            t.click_driver(driver,di)
            t.blank_driver_dates(driver)
            t.edit_driver_by_field(driver,"FirstName","tryon-qa-gb")
            time.sleep(1)

    t.back_to_tp(driver)
    time.sleep(2)

