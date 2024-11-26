import logging
import time
import os
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementClickInterceptedException, NoSuchElementException

class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout
        self.logger = logging.getLogger(self.__class__.__name__)
        self.screenshot_dir = '/Users/mac_air/olsera/'

    def _wait_for_condition(self, condition, locator=None, timeout=None, error_message=None):
        timeout = timeout or self.timeout
        try:
            return WebDriverWait(self.driver, timeout).until(
                condition(locator) if locator else condition
            )
        except TimeoutException:
            self.logger.error(error_message or f"Timeout waiting for condition: {condition}")
            raise

    def find_element(self, by, value, timeout=None):
        return self._wait_for_condition(
            EC.presence_of_element_located,
            (by, value),
            timeout,
            f"Failed to find element: {(by, value)}"
        )

    def click(self, by, value, timeout=None):
        self.click_element((by, value), timeout)

    def enter_text(self, text, by, value, timeout=None):
        element = self.find_element(by, value, timeout)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Entered text '{text}' into element: {(by, value)}")

    def take_screenshot(self, name=None):
        os.makedirs(self.screenshot_dir, exist_ok=True)
        name = name or time.strftime("%Y%m%d-%H%M%S")
        screenshot_path = os.path.join(self.screenshot_dir, f"{name}.png")
        self.driver.save_screenshot(screenshot_path)
        self.logger.info(f"Screenshot saved at: {screenshot_path}")
        return screenshot_path

    def wait_for_page_load(self, timeout=None):
        self._wait_for_condition(
            lambda driver: driver.execute_script("return document.readyState") == "complete",
            timeout=timeout,
            error_message=f"Page load timeout after {timeout or self.timeout} seconds"
        )
        self.logger.info("Page has finished loading")

    def is_element_present(self, locator, timeout=None):
        try:
            self._wait_for_condition(
                EC.presence_of_element_located,
                locator,
                timeout,
                f"Element not present: {locator}"
            )
            return True
        except TimeoutException:
            return False

    def click_element(self, locator, timeout=None, retry_count=3):
        timeout = timeout or self.timeout
        for attempt in range(retry_count):
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
                element.click()
                self.logger.info(f"Clicked element: {locator}")
                return
            except ElementClickInterceptedException:
                if attempt < retry_count - 1:
                    self.logger.warning(f"Click intercepted, retrying... (Attempt {attempt + 1})")
                    continue
                self.logger.error(f"Failed to click element after {retry_count} attempts: {locator}")
                raise
            except TimeoutException:
                self.logger.error(f"Element not clickable within {timeout} seconds: {locator}")
                raise
