import sys
import os
import pytest
import logging

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..','..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from pages.customer.customer_page import CustomerPage
from tests.credential.test_credential import CUSTOMER_TYPE, NEW_CUSTOMER_DATA

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TestCustomer:
    @staticmethod
    def add_customer(customer_page: CustomerPage) -> str:
        customer_page.click_add_customer()
        customer_data = NEW_CUSTOMER_DATA()

        customer_page.fill_customer_details(
            name=customer_data['name'],
            email=customer_data['email'],
            phone=customer_data['phone'],
            gender=customer_data['gender']
        )

        if CUSTOMER_TYPE == 'satusehat':
            TestCustomer._fill_satusehat_details(customer_page, customer_data)

        customer_page.save_customer(customer_data['name'])
        return customer_data['name']

    @staticmethod
    def _fill_satusehat_details(customer_page: CustomerPage, customer_data: dict) -> None:
        customer_page.fill_additional_details(
            birthplace=customer_data['birthplace'],
            birthdate=customer_data['birthdate'],
            nationality=customer_data['nationality'],
            marital_status=customer_data['marital_status']
        )
        customer_page.fill_identity_details(
            id_type=customer_data['id_type'],
            id_number=customer_data['id_number']
        )
        customer_page.fill_address(
            address_type=customer_data['address_type'],
            address=customer_data['address'],
            country=customer_data['country'],
            province=customer_data['province'],
            city=customer_data['city']
        )
        customer_page.fill_additional_address_details(
            district=customer_data['district'],
            village=customer_data['village'],
            rt=customer_data['rt'],
            rw=customer_data['rw'],
            postal_code=customer_data['postal_code']
        )
        customer_page.select_communication_language(customer_data['communication_language'])

    def test_add_customer(self, logged_in_driver):
        customer_page = CustomerPage(logged_in_driver)
        customer_page.open_customer_page()
        customer_name = self.add_customer(customer_page)

        assert customer_page.verify_customer_added(customer_name), "Failed to add customer!"
        assert customer_page.verify_customer_details(name=customer_name), "Customer details do not match!"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
