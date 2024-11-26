from selenium.webdriver.common.by import By

class LoginLocators:
    EMAIL_INPUT = (By.CSS_SELECTOR, "input[type='email']")
    PASSWORD_INPUT = (By.CSS_SELECTOR, "input[type='password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button.btn-block")
    SUCCESS_MESSAGE = (
        By.XPATH, 
        "//p[contains(text(), 'Pilih lokasi transaksi') or contains(text(), 'Select transaction location')]"
    )
