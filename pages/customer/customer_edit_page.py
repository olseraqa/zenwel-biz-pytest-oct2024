import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage
from pages.element_customer import CustomerElement
import logging
import time  # Add this import at the top of your file if it's not already there

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.credential.test_credential import CUSTOMER_TYPE, CUSTOMER_EDIT_DATA
from pages.customer.locators_customer import CustomerLocators

class CustomerEditPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def open_edit_page(self, customer_name):
        self.logger.info(f"Opening edit page for customer: {customer_name}")
        self.click_element(CustomerLocators.CUSTOMER_ROW(customer_name))
        self.wait_for_page_load()
        time.sleep(3)  # Add a 3-second delay

    def switch_to_details_tab(self):
        self.logger.info("Switching to 'Rincian' tab")
        self.click_element(CustomerLocators.RINCIAN_TAB)
        self.wait_for_page_load()
        self.logger.info("Successfully switched to 'Rincian' tab")

    def wait_for_overlay_to_disappear(self, timeout=10):
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located(CustomerLocators.OVERLAY)
            )
        except TimeoutException:
            self.logger.warning("Overlay did not disappear, proceeding anyway")

    def fill_customer_details(self, name, email, phone, gender=None):
        self.logger.info(f"Filling customer details: {name}, {email}, {phone}, {gender}")
        self.input_text(CustomerLocators.NAME_INPUT, name)
        self.input_text(CustomerLocators.EMAIL_INPUT, email)
        self.input_text(CustomerLocators.PHONE_INPUT, phone)
        self._select_gender(gender or CUSTOMER_EDIT_DATA.get('new_gender', 'disable'))

    def _select_gender(self, gender):
        gender_map = {
            "disable": "Non-Aktifkan",
            "M": "Pria",
            "F": "Wanita",
            "Male": "Pria",
            "Female": "Wanita"
        }
        # Use the gender from CUSTOMER_EDIT_DATA if available, otherwise use the provided gender
        gender_to_use = CUSTOMER_EDIT_DATA.get('new_gender', gender)
        gender_value = gender_map.get(gender_to_use, "Non-Aktifkan")
        self.click_element(CustomerLocators.GENDER_RADIO(gender_value))

    def save_customer(self, customer_name):
        self.logger.info("Saving customer")
        
        # Locator for the initial save button
        save_button_locator = (By.CSS_SELECTOR, "button.el-button.el-button--primary.font-14.font-bold.color-2.h-56.box-shadow-2")

        # Click the initial save button
        self.click_element(save_button_locator)

       # Check if CUSTOMER_TYPE is 'satusehat'
        if CUSTOMER_TYPE == 'satusehat':
            # Wait for the dialog to appear and click the "Simpan & Sinkron" button
            sync_button_locator = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(., 'Simpan & Sinkron')]")
            self.click_element(sync_button_locator)

    def input_text(self, locator, text):
        element = self.wait_for_element(locator)
        element.clear()
        element.send_keys(text)

    def select_dropdown(self, locator, option):
        select = Select(self.wait_for_element(locator))
        select.select_by_visible_text(option)

    def wait_for_element(self, locator, timeout=10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    def click_element(self, locator, timeout=10):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )
        element.click()

    def wait_for_page_load(self, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            lambda d: d.execute_script('return document.readyState') == 'complete'
        )

    def is_element_present(self, locator):
        try:
            self.driver.find_element(*locator)
            return True
        except:
            return False

    # Additional methods (fill_address, fill_additional_details, etc.) can be implemented similarly
