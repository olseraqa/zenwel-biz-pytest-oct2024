import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

import logging
import time

# Add paths to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from pages.customer.customer_page import CustomerPage
from pages.customer.customer_edit_page import CustomerEditPage
from pages.login.login_page import LoginPage
from pages.login.location_page import LocationPage
from tests.credential.test_credential import LoginData, ENVIRONMENT, CUSTOMER_EDIT_DATA
from tests.branch_setting import get_url_based_on_environment

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

def login_and_select_location(driver, url):
    login_page = LoginPage(driver, url)
    location_page = LocationPage(driver)

    login_page.open_login_page()
    login_page.enter_email(LoginData[ENVIRONMENT][0][0])
    login_page.enter_password(LoginData[ENVIRONMENT][0][1])
    login_page.click_login()
    assert login_page.verify_login_success(), "Login failed!"

    assert location_page.select_location(LoginData[ENVIRONMENT][0][2]), f"Failed to select location: {LoginData[ENVIRONMENT][0][2]}"
    assert location_page.verify_dashboard_loaded(), "Failed to load dashboard!"

def edit_customer(edit_page, old_name, new_name, new_email, new_phone, new_gender):
    edit_page.open_edit_page(old_name)
    logger.info(f"Opened edit page for customer: {old_name}")

    edit_page.switch_to_details_tab()
    logger.info("Switched to details tab")

    edit_page.fill_customer_details(
        name=new_name,
        email=new_email,
        phone=new_phone,
        gender=new_gender
    )

    edit_page.save_customer(new_name)

def test_customer_edit(driver):
    url = get_url_based_on_environment(ENVIRONMENT)
    login_and_select_location(driver, url)

    customer_page = CustomerPage(driver)
    edit_page = CustomerEditPage(driver)

    customer_page.open_customer_page()
    logger.info("Opened customer page")

    edit_customer(edit_page,
                  CUSTOMER_EDIT_DATA['old_name'],
                  CUSTOMER_EDIT_DATA['new_name'],
                  CUSTOMER_EDIT_DATA['new_email'],
                  CUSTOMER_EDIT_DATA['new_phone'],
                  CUSTOMER_EDIT_DATA['new_gender'])

    # Add a small delay to allow the page to refresh
    time.sleep(2)

    assert customer_page.verify_customer_details(CUSTOMER_EDIT_DATA['new_name']), \
        f"Customer name {CUSTOMER_EDIT_DATA['new_name']} not found in the customer list"

    logger.info(f"Customer {CUSTOMER_EDIT_DATA['new_name']} successfully edited and verified")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
