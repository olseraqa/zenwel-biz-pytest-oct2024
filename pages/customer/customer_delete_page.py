from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from pages.customer.locators_customer import CustomerLocators
import logging
import time

class CustomerDeletePage(BasePage):
    # Locators
    CUSTOMER_ROW = "//td[contains(@class, 'el-table__cell')]//div[contains(@class, 'font-14') and contains(text(), '{}')]"
    RINCIAN_TAB = "//div[@id='tab-details' and contains(@class, 'el-tabs__item') and text()='Rincian']"
    DELETE_BUTTON = "//button[contains(@class, 'el-button--danger') and .//span[contains(text(), 'Hapus Customer')]]"
    CONFIRM_DELETE_BUTTON = "//button[contains(@class, 'el-button--text') and .//span[contains(text(), 'Konfirmasi')]]"
    CUSTOMER_DETAILS = "//div[@data-v-0684b27b='' and contains(., '{}')]"

    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def open_customer_details(self, customer_name):
        self.logger.info(f"Opening details page for customer: {customer_name}")
        self.click_element(CustomerLocators.CUSTOMER_ROW(customer_name))
        self.wait_for_page_load()

    def switch_to_details_tab(self, customer_name):
        self.logger.info(f"Switching to 'Rincian' tab for customer: {customer_name}")
        
        customer_details_locator = CustomerLocators.CUSTOMER_PROFILE(customer_name)
        self.wait_for_element_visible(customer_details_locator)
        self.click_element(CustomerLocators.RINCIAN_TAB)
        self.wait_for_page_load()
        time.sleep(3)  # Add a 3-second delay as requested earlier
        
        self.logger.info(f"Successfully switched to 'Rincian' tab for customer: {customer_name}")

    def click_delete_button(self):
        self.logger.info("Clicking delete button")
        self.click_element(CustomerLocators.DELETE_BUTTON)

    def confirm_delete(self):
        self.logger.info("Confirming delete action")
        self.click_element(CustomerLocators.CONFIRM_DELETE_BUTTON)

    def delete_customer(self, customer_name):
        self.open_customer_details(customer_name)
        self.switch_to_details_tab(customer_name)
        self.click_delete_button()
        self.confirm_delete()
        self.logger.info(f"Customer {customer_name} deleted successfully")

    def is_customer_deleted(self, customer_name):
        return not self.is_element_present(CustomerLocators.CUSTOMER_ROW(customer_name))

    def wait_for_element_visible(self, locator, timeout=10):
        self.logger.info(f"Waiting for element to be visible: {locator}")
        element = WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )
        self.logger.info(f"Element is now visible: {locator}")
        return element
