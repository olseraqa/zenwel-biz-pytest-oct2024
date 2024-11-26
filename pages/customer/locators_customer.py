from selenium.webdriver.common.by import By

class CustomerLocators:
    # Navigation and general buttons
    CUSTOMER_MENU = (By.XPATH, "//a[@href='/customers/index']")
    ADD_CUSTOMER_BUTTON = (By.CSS_SELECTOR, "button.el-button.el-button--primary.is-circle")
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(., 'Simpan')]")
    SYNC_BUTTON = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(., 'Simpan & Sinkron')]")

    # Basic customer information inputs
    NAME_INPUT = (By.XPATH, "//label[text()='Nama']/following-sibling::div//input")
    EMAIL_INPUT = (By.XPATH, "//label[text()='Email']/following-sibling::div//input")
    PHONE_INPUT = (By.XPATH, "//label[text()='No. Telpon']/following-sibling::div//input")

    # Additional customer details
    BIRTHPLACE_INPUT = (By.XPATH, "//label[text()='Tempat lahir']/following-sibling::div//input")
    BIRTHDATE_YEAR = (By.XPATH, "//label[text()='Tanggal Lahir']/following-sibling::div//input[@placeholder='YYYY']")
    BIRTHDATE_MONTH = (By.XPATH, "//label[text()='Tanggal Lahir']/following-sibling::div//input[@placeholder='MMM']")
    BIRTHDATE_DAY = (By.XPATH, "//label[text()='Tanggal Lahir']/following-sibling::div//input[@placeholder='DD']")
    ID_NUMBER_INPUT = (By.XPATH, "//label[text()='Nomor Kartu Identitas']/following-sibling::div//input")

    # Dropdowns
    NATIONALITY_DROPDOWN = (By.XPATH, "//label[text()='Kewarganegaraan']/following-sibling::div//input[@readonly]")
    MARITAL_STATUS_DROPDOWN = (By.XPATH, "//label[text()='Status Pernikahan']/following-sibling::div//input[@readonly]")
    ADDRESS_TYPE_DROPDOWN = (By.XPATH, "//label[text()='Tipe Alamat']/following-sibling::div//input[@readonly]")
    COUNTRY_DROPDOWN = (By.XPATH, "//label[text()='Negara']/following-sibling::div//input[@readonly]")
    PROVINCE_DROPDOWN = (By.XPATH, "//label[text()='Provinsi']/following-sibling::div//input[@readonly]")
    CITY_DROPDOWN = (By.XPATH, "//label[text()='Kota']/following-sibling::div//input[@readonly]")
    DISTRICT_DROPDOWN = (By.XPATH, "//label[text()='Kecamatan']/following-sibling::div//input[@readonly]")
    VILLAGE_DROPDOWN = (By.XPATH, "//label[text()='Kelurahan']/following-sibling::div//input[@readonly]")
    COMMUNICATION_LANGUAGE_DROPDOWN = (By.XPATH, "//label[text()='Bahasa Komunikasi']/following-sibling::div//input[@readonly]")

    # Address inputs
    ADDRESS_INPUT = (By.XPATH, "//label[text()='Alamat']/following-sibling::div//textarea")
    RT_INPUT = (By.XPATH, "//label[text()='RT']/following-sibling::div//input")
    RW_INPUT = (By.XPATH, "//label[text()='RW']/following-sibling::div//input")
    POSTAL_CODE_INPUT = (By.XPATH, "//label[text()='Kode pos']/following-sibling::div//input")

    # Dynamic locators
    @staticmethod
    def GENDER_RADIO(gender_value):
        return (By.XPATH, f"//label[text()='Jenis Kelamin']/following-sibling::div//span[contains(text(),'{gender_value}')]")

    @staticmethod
    def CUSTOMER_IN_TABLE(name):
        return (By.XPATH, f"//td[contains(@class, 'el-table__cell')]//div[contains(@class, 'font-14') and contains(text(), '{name}')]")

    @staticmethod
    def CUSTOMER_DETAILS(name):
        return (By.XPATH, f"//div[contains(@class, 'font-14') and contains(@class, 'color-1') and contains(@class, 'font-bold')][normalize-space()='{name}']")

    @staticmethod
    def CUSTOMER_PROFILE(name):
        return (By.XPATH, f"//div[@data-v-0684b27b='' and contains(., '{name}')]")
    @staticmethod
    def dropdown_option(option):
        return (By.XPATH, f"//span[normalize-space(text())='{option}']")

    @staticmethod
    def id_type_radio(id_type):
        id_type_map = {"ID Sendiri": "1", "Tanpa ID": "3"}
        return (By.XPATH, f"//label[contains(@class, 'el-radio-button')]//input[@value='{id_type_map.get(id_type, '1')}']")

    # Locators from customer_edit_page.py & customer_delete_page.py
    CUSTOMER_ROW = lambda name: (By.XPATH, f"//td[contains(@class, 'el-table__cell')]//div[contains(@class, 'font-14') and contains(text(), '{name}')]")
    RINCIAN_TAB = (By.XPATH, "//div[@id='tab-details' and contains(@class, 'el-tabs__item') and text()='Rincian']")
    OVERLAY = (By.XPATH, "//div[contains(@class, 'el-message') or contains(@class, 'el-loading-mask')]")
    GENDER_RADIO = lambda gender: (By.XPATH, f"//label[text()='Jenis Kelamin']/following-sibling::div//span[contains(text(),'{gender}')]")
    SAVE_BUTTON = (By.XPATH, "//button[contains(@class, 'el-button--primary') and contains(., 'Simpan')]")

    # Locators from customer_delete_page.py
    DELETE_BUTTON = (By.XPATH, "//button[contains(@class, 'el-button--danger') and .//span[contains(text(), 'Hapus Customer')]]")
    CONFIRM_DELETE_BUTTON = (By.XPATH, "//button[contains(@class, 'el-button--text') and .//span[contains(text(), 'Konfirmasi')]]")
