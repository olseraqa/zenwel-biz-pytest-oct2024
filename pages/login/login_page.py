from pages.base_page import BasePage
from pages.login.locators_login import LoginLocators

class LoginPage(BasePage):
    def __init__(self, driver, url):
        super().__init__(driver)
        self.url = url

    def open_login_page(self):
        self.driver.get(self.url)
        self.wait_for_page_load()

    def enter_email(self, email):
        self.enter_text(email, *LoginLocators.EMAIL_INPUT)

    def enter_password(self, password):
        self.enter_text(password, *LoginLocators.PASSWORD_INPUT)

    def click_login(self):
        self.click_element(LoginLocators.LOGIN_BUTTON)

    def verify_login_success(self):
        return self.is_element_present(LoginLocators.SUCCESS_MESSAGE)

    def login(self, email, password):
        self.open_login_page()
        self.enter_email(email)
        self.enter_password(password)
        self.click_login()
        return self.verify_login_success()
