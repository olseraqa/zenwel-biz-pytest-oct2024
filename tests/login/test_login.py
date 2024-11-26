import sys
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from typing import Generator

# Add 'pages' path to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.login.login_page import LoginPage
from pages.login.location_page import LocationPage
from tests.credential.test_credential import LoginData, ENVIRONMENT
from tests.branch_setting import get_url_based_on_environment

@pytest.fixture(scope="function")
def driver() -> Generator[webdriver.Chrome, None, None]:
    """Set up and tear down WebDriver for each test."""
    options = webdriver.ChromeOptions()
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture(scope="function")
def login_page(driver: webdriver.Chrome) -> LoginPage:
    """Create and return a LoginPage instance."""
    url = get_url_based_on_environment(ENVIRONMENT)
    return LoginPage(driver, url)

@pytest.fixture(scope="function")
def location_page(driver: webdriver.Chrome) -> LocationPage:
    """Create and return a LocationPage instance."""
    return LocationPage(driver)

@pytest.mark.parametrize("email,password,location_name", LoginData[ENVIRONMENT])
def test_login_and_select_location(
    login_page: LoginPage,
    location_page: LocationPage,
    email: str,
    password: str,
    location_name: str
) -> None:
    """
    Test login functionality and location selection.

    Args:
        login_page: LoginPage instance
        location_page: LocationPage instance
        email: User's email
        password: User's password
        location_name: Name of the location to select
    """
    # Test login
    assert login_page.login(email, password), "Login failed!"

    # Test location selection
    assert location_page.select_location(location_name), f"Failed to select location: {location_name}"
    assert location_page.verify_dashboard_loaded(), "Failed to load dashboard!"

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--capture=no"])
