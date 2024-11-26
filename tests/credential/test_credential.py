# Login credentials
LoginData = {
    'staging': [
        (
            "zenweltesting@gmail.com",
            "zenwel",
            "ZenDev - SatuSehat"
        ),
    ],
    'production': [
        (
            "zenweltesting@gmail.com",
            "zenweltesting",
            "ZenDev - Accounting"
        ),
    ]
}

# Use the appropriate login data based on the environment
ENVIRONMENT = 'staging'  # staging or production
current_login_data = LoginData[ENVIRONMENT]

# Customer type
CUSTOMER_TYPE = 'satusehat'  # regular or satusehat

import itertools

def generate_customer_data(start=1):
    counter = itertools.count(start)
    
    def get_data():
        i = next(counter)
        return {
            'name': f"Jane Smith{i}",
            'email': f"janesmith{i}@example.com",
            'phone': "+62234567890",
            'gender': "Female",
            'birthplace': "Jakarta",
            'birthdate': "2010-01-01",
            'nationality': "WNI",
            'marital_status': "Married",
            'id_type': "ID Sendiri",
            'id_number': "1234567890123456",
            'address_type': "Home",
            'address': "123 Main St",
            'country': "Indonesia",
            'province': "Aceh",
            'city': "Kab. Aceh Selatan",
            'district': "Kluet Utara",
            'village': "Krueng Batee",
            'rt': "001",
            'rw': "002",
            'postal_code': "10310",
            'communication_language': "Indonesian",
            'notes': "SatuSehat customer",
            'tags': ["SatuSehat", "Priority"],
            'notification_preferences': {'email': True, 'sms': False},
            'marketing_preferences': True
        }
    
    return get_data

# You can now define the starting number here
NEW_CUSTOMER_DATA = generate_customer_data(start=99)  # Starts from Jane Smith8

# Customer data for editing
CUSTOMER_EDIT_DATA = {
    'old_name': "Adit",
    'new_name': "Adit new",
    'new_email': "janed.smith@example.com",
    'new_phone': "1234567890",
    'new_gender': "Female"
}

CUSTOMER_DELETE_DATA = {
    'name': 'Jane Smith'
}
