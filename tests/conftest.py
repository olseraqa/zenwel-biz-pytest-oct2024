import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from pages.login.login_page import LoginPage
from pages.login.location_page import LocationPage
from tests.credential.test_credential import LoginData, ENVIRONMENT
from tests.branch_setting import get_url_based_on_environment

@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def logged_in_driver(driver):
    url = get_url_based_on_environment(ENVIRONMENT)
    login_page = LoginPage(driver, url)
    location_page = LocationPage(driver)

    login_page.open_login_page()
    login_page.enter_email(LoginData[ENVIRONMENT][0][0])
    login_page.enter_password(LoginData[ENVIRONMENT][0][1])
    login_page.click_login()
    assert login_page.verify_login_success(), "Login gagal!"

    assert location_page.select_location(LoginData[ENVIRONMENT][0][2]), f"Gagal memilih lokasi: {LoginData[ENVIRONMENT][0][2]}"
    assert location_page.verify_dashboard_loaded(), "Gagal memuat dashboard!"

    return driver
