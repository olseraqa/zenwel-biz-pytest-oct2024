from selenium.webdriver.common.by import By

class LocationLocators:
    # Locator untuk memilih lokasi
    @staticmethod
    def LOCATION_BUTTON(location_name):
        return (By.XPATH, f"//div[contains(@class,'block-link flex-block-link pointer ml-auto mr-auto') and .//div[contains(text(),'{location_name}')]]")

    # Locator untuk memverifikasi bahwa dashboard telah dimuat
    DASHBOARD_ELEMENT = (By.XPATH, "//li[@id='menu-wrapper--home' and @class='el-menu-item is-active submenu-title-noDropdown']")
