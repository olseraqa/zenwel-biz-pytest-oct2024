import sys
import os
import pytest
import logging

# Add paths to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.customer.customer_page import CustomerPage
from pages.customer.customer_delete_page import CustomerDeletePage
from tests.credential.test_credential import CUSTOMER_DELETE_DATA

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_customer_delete(logged_in_driver):
    driver = logged_in_driver
    customer_page = CustomerPage(driver)
    delete_page = CustomerDeletePage(driver)

    customer_page.open_customer_page()
    logger.info("Opened customer page")

    customer_name = CUSTOMER_DELETE_DATA['name']
    delete_page.delete_customer(customer_name)

    assert delete_page.is_customer_deleted(customer_name), \
        f"Customer {customer_name} was not deleted successfully"

    logger.info(f"Customer {customer_name} successfully deleted and verified")

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
