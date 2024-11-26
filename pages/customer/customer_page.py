import os
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
import logging
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from tests.credential.test_credential import CUSTOMER_TYPE
from pages.customer.locators_customer import CustomerLocators


class CustomerPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logger = logging.getLogger(__name__)

    def open_customer_page(self):
        self.logger.info("Opening customer page")
        customer_menu = self.find_element(*CustomerLocators.CUSTOMER_MENU)
        customer_menu.click()
        time.sleep(5)

    def click_add_customer(self):
        self.logger.info("Clicking add customer button")
        add_button = self.find_element(*CustomerLocators.ADD_CUSTOMER_BUTTON)
        add_button.click()

    def fill_customer_details(self, name, email, phone, gender="disable"):
        self.logger.info(f"Filling customer details for {name}")
        self.enter_text(name, *CustomerLocators.NAME_INPUT)
        self.enter_text(email, *CustomerLocators.EMAIL_INPUT)
        self.enter_text(phone, *CustomerLocators.PHONE_INPUT)
        
        gender_map = {
            "disable": "Non-Aktifkan",
            "M": "Pria",
            "F": "Wanita",
            "Male": "Pria",
            "Female": "Wanita"
        }
        
        gender_value = gender_map.get(gender, "Non-Aktifkan")
        self.click_element(CustomerLocators.GENDER_RADIO(gender_value))

    def select_communication_language(self, language):
        self.logger.info(f"Selecting communication language: {language}")  # Add this line
        self.select_dropdown_option("Bahasa Komunikasi", language)

    def fill_address(self, address_type, address, country, province, city):
        self.logger.info("Filling address details")
        self.select_dropdown_option("Tipe Alamat", address_type)
        self.enter_text(address, *CustomerLocators.ADDRESS_INPUT)
        
        self.logger.info("Waiting for 5 seconds after selecting country")
        time.sleep(2)

        self.select_dropdown_option("Negara", country)        
        self.select_dropdown_option("Provinsi", province, wait_time=10)  # Increased wait time for province
        self.select_dropdown_option("Kota", city)

    def select_dropdown_option(self, label, option, max_attempts=3, wait_time=10):
        self.logger.info(f"Selecting {option} for {label}")
        dropdown_xpath = f"//label[text()='{label}']/following-sibling::div//input[@readonly]"
        option_xpath = f"//span[normalize-space(text())='{option}']"

        for attempt in range(max_attempts):
            try:
                # Wait for the dropdown to be clickable
                dropdown = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, dropdown_xpath))
                )

                # Scroll the dropdown into view
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", dropdown)
                time.sleep(0.5)  # Short pause after scrolling

                # Try to click using different methods
                try:
                    dropdown.click()
                except ElementClickInterceptedException:
                    self.logger.warning(f"Direct click failed for {label} dropdown, attempting JavaScript click")
                    self.driver.execute_script("arguments[0].click();", dropdown)

                # Wait for the option to be clickable
                option_element = WebDriverWait(self.driver, wait_time).until(
                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                )
                option_element.click()

                # Verify selection
                selected_value = dropdown.get_attribute("value")
                if selected_value == option:
                    self.logger.info(f"Successfully selected {option} for {label}")
                    return True
                else:
                    self.logger.warning(f"Selection verification failed. Expected {option}, but got {selected_value}")
            except (ElementClickInterceptedException, TimeoutException) as e:
                self.logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_attempts - 1:
                    self.logger.error(f"Failed to select {option} for {label} after {max_attempts} attempts")
                    self.take_screenshot(f"select_dropdown_failure_{label}")
                    raise
                time.sleep(1)  # Wait before retrying

        return False

    def save_customer(self, customer_name):
        self.logger.info("Saving customer")
        self.click_element(CustomerLocators.SAVE_BUTTON)

        # Check if CUSTOMER_TYPE is 'satusehat'
        if CUSTOMER_TYPE == 'satusehat':
            # Wait for the dialog to appear and click the "Simpan & Sinkron" button
            sync_button_locator = CustomerLocators.SYNC_BUTTON
            self.click_element(sync_button_locator)

        # Verify that the customer was added successfully
        if self.verify_customer_added(customer_name):
            self.logger.info(f"Customer '{customer_name}' added successfully")
        else:
            self.logger.error(f"Failed to add customer '{customer_name}'")
            raise Exception(f"Customer '{customer_name}' was not added successfully")

        # Verify that the customer was added successfully
        if self.verify_customer_added(customer_name):
            self.logger.info(f"Customer '{customer_name}' added successfully")
        else:
            self.logger.error(f"Failed to add customer '{customer_name}'")
            raise Exception(f"Customer '{customer_name}' was not added successfully")

    def click_element(self, locator, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable(locator)
            )
            self.logger.info(f"Found clickable element: {locator}")
            
            # Scroll the element into view
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            time.sleep(0.5)  # Short pause after scrolling

            # Try to click the element
            try:
                element.click()
                self.logger.info(f"Clicked element: {locator}")
            except ElementClickInterceptedException:
                self.logger.warning(f"Direct click failed for {locator}, attempting JavaScript click")
                self.driver.execute_script("arguments[0].click();", element)
                self.logger.info(f"Performed JavaScript click on element: {locator}")
        except TimeoutException:
            self.logger.error(f"Failed to find clickable element: {locator}")
            raise Exception(f"Element not found or not clickable: {locator}")

    def verify_customer_added(self, customer_name, timeout=10):
        self.logger.info(f"Verifying if customer '{customer_name}' was added")
        customer_locator = CustomerLocators.CUSTOMER_DETAILS(customer_name)
        
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(customer_locator)
            )
            self.logger.info(f"Customer '{customer_name}' found in the table")
            return True
        except TimeoutException:
            self.logger.warning(f"Customer '{customer_name}' not found in the table within {timeout} seconds")
            return False
    
    def verify_customer_details(self, name):
        self.logger.info(f"Verifying customer details for {name}")
        try:
            customer_name_xpath = CustomerLocators.CUSTOMER_DETAILS(name)
            
            # Wait for the element to be present
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, customer_name_xpath))
            )

            # Verify name
            if self.is_element_present((By.XPATH, customer_name_xpath)):
                self.logger.info(f"Customer details for {name} verified successfully")
                return True
            else:
                self.logger.error(f"Customer name {name} not found")
                return False
        except Exception as e:
            self.logger.error(f"Customer details verification failed: {str(e)}")
            return False

    def close_overlay(self):
        try:
            close_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable(CustomerLocators.CLOSE_BUTTON)
            )
            close_button.click()
            time.sleep(0.1)  # Wait for the overlay to close
        except TimeoutException:
            self.logger.warning("No overlay close button found. Proceeding.")

    def fill_additional_details(self, birthplace, birthdate, nationality, marital_status):
        self.enter_text(birthplace, *CustomerLocators.BIRTHPLACE_INPUT)
        
        # Handle date of birth
        year, month, day = birthdate.split('-')
        
        # Select year
        year_dropdown = self.find_element(*CustomerLocators.BIRTHDATE_YEAR)
        year_dropdown.click()
        year_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(@class, 'el-select-dropdown__item') and normalize-space(text())='{year}']"))
        )
        year_option.click()

        # Select month
        month_dropdown = self.find_element(*CustomerLocators.BIRTHDATE_MONTH)
        month_dropdown.click()
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 'Jul', 'Agt', 'Sep', 'Okt', 'Nov', 'Des']
        month_name = month_names[int(month) - 1]
        month_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(@class, 'el-select-dropdown__item')]/span[text()='{month_name}']"))
        )
        month_option.click()

        # Select day
        day_dropdown = self.find_element(*CustomerLocators.BIRTHDATE_DAY)
        day_dropdown.click()
        day_option = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//li[contains(@class, 'el-select-dropdown__item')]/span[text()='{int(day):02d}']"))
        )
        day_option.click()

        self.select_dropdown_option("Kewarganegaraan", nationality)
        
        # Select marital status
        marital_status_dropdown = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[text()='Status Pernikahan']/following-sibling::div//input[@readonly]"))
        )

        # Scroll the element into view
        self.driver.execute_script("arguments[0].scrollIntoView(true);", marital_status_dropdown)
        time.sleep(1)  # Short pause after scrolling

        # Try to click and select the marital status
        max_attempts = 3
        for attempt in range(max_attempts):
            try:
                # Click to open dropdown
                self.driver.execute_script("arguments[0].click();", marital_status_dropdown)
                time.sleep(1)  # Wait for dropdown to open

                # Try to find and click the option
                option_xpath = f"//li[contains(@class, 'el-select-dropdown__item')]//span[contains(text(), '{marital_status}')]"
                option = WebDriverWait(self.driver, 5).until(
                    EC.element_to_be_clickable((By.XPATH, option_xpath))
                )
                option.click()
                break  # If successful, break the loop
            except (TimeoutException, ElementClickInterceptedException, NoSuchElementException) as e:
                if attempt == max_attempts - 1:  # If it's the last attempt
                    self.logger.error(f"Failed to select marital status after {max_attempts} attempts. Error: {str(e)}")
                    raise
                else:
                    self.logger.warning(f"Attempt {attempt + 1} failed. Retrying...")
                    time.sleep(1)  # Wait before retrying

        # Verify selection
        selected_value = marital_status_dropdown.get_attribute("value")
        assert selected_value == marital_status, f"Expected marital status '{marital_status}', but got '{selected_value}'"

    def fill_identity_details(self, id_type, id_number=None):
        self.logger.info(f"Filling identity details: {id_type}")
        
        # Map the id_type to the corresponding value
        id_type_map = {
            "ID Sendiri": "1",
            "Tanpa ID": "3"
        }
        
        # Select the appropriate radio button
        radio_xpath = f"//label[contains(@class, 'el-radio-button')]//input[@value='{id_type_map.get(id_type, '1')}']"
        radio_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, radio_xpath))
        )
        self.driver.execute_script("arguments[0].click();", radio_button)

        # If "ID Sendiri" is selected and id_number is provided, enter the ID number
        if id_type == "ID Sendiri" and id_number:
            self.enter_text(id_number, By.XPATH, "//label[text()='Nomor Kartu Identitas']/following-sibling::div//input")

    def fill_additional_address_details(self, district, village, rt, rw, postal_code):
        self.select_dropdown_option("Kecamatan", district)
        self.select_dropdown_option("Kelurahan", village)
        self.enter_text(rt, *CustomerLocators.RT_INPUT)
        self.enter_text(rw, *CustomerLocators.RW_INPUT)
        self.enter_text(postal_code, *CustomerLocators.POSTAL_CODE_INPUT)

    def verify_customer_details(self, name):
        self.logger.info(f"Verifying customer details for {name}")
        try:
            customer_name_xpath = f"//div[contains(@class, 'font-14') and contains(@class, 'color-1') and contains(@class, 'font-bold')][normalize-space()='{name}']"
            
            # Wait for the element to be present
            WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_element_located((By.XPATH, customer_name_xpath))
            )

            # Verify name
            if self.is_element_present((By.XPATH, customer_name_xpath)):
                self.logger.info(f"Customer details for {name} verified successfully")
                return True
            else:
                self.logger.error(f"Customer name {name} not found")
                return False
        except Exception as e:
            self.logger.error(f"Customer details verification failed: {str(e)}")
            return False



