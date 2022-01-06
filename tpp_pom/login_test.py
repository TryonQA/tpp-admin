import login
import providers_home
from selenium import webdriver

def login_test(driver: webdriver.Chrome, username, password):
    test_tag = "Login User"
    detail = "logged in user: " + username
    login.PreLogin(driver).start_login()
    login_page = login.LoginPage(driver)
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.finalize()
    providers_home_page = providers_home.ProvidersHome(driver)
    if providers_home_page.username == username:
        result = "PASS"
    else:
        result = "FAIL"
    return (result,test_tag,detail)

    