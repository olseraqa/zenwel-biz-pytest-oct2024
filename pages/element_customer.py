from selenium.webdriver.common.by import By

class CustomerElement:
    CUSTOMER_ROW = (By.XPATH, "//td[contains(@class, 'el-table__cell')]//div[contains(@class, 'font-14') and contains(text(), '{}')]")
    RINCIAN_TAB = (By.XPATH, "//div[@id='tab-details' and contains(@class, 'el-tabs__item') and text()='Rincian']")
    OVERLAY = (By.XPATH, "//div[contains(@class, 'el-message') or contains(@class, 'el-loading-mask')]")
    NAME_INPUT = (By.XPATH, "//label[text()='Nama']/following-sibling::div//input")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::div//input")
    PHONE_INPUT = (By.XPATH, "//label[text()='No. Telpon']/following-sibling::div//input")
    GENDER_RADIO = (By.XPATH, "//label[text()='Jenis Kelamin']/following-sibling::div//span[contains(text(),'{}')]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(., 'Simpan')]")