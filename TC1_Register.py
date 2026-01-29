
import json
import pytest
import time
import random
import string

from config.settings import USERS_DATA_FILE
from pages.register_page import RegisterPage
from flows.register_flow import RegisterFlow


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.register
def test_verify_registering_with_mandatory_fields(driver):
  
    # Arrange: Load valid test user data from configuration
    import time
    with open(USERS_DATA_FILE, 'r') as file:
        users_data = json.load(file)
    
    user_data = users_data.get('valid_user').copy()
    assert user_data is not None, "Test data 'valid_user' not found in users.json"
    
    # Generate truly unique data for each test run
    timestamp = int(time.time() * 1000)  # Milliseconds for better uniqueness
    random_suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    unique_id = f"{timestamp}_{random_suffix}"
    
    user_data['email'] = f"validuser_{unique_id}@example.com"
    user_data['loginname'] = f"johndoe_{unique_id}"

    # Act: Execute the registration flow with ALL mandatory fields
    register_page = RegisterPage(driver)
    register_flow = RegisterFlow(register_page)
    result = register_flow.verify_registering_with_mandatory_fields(
        firstname=user_data.get('firstname'),
        lastname=user_data.get('lastname'),
        email=user_data.get('email'),
        address=user_data.get('address'),
        city=user_data.get('city'),
        zone_id=user_data.get('zone_id'),
        postcode=user_data.get('postcode'),
        country_id=user_data.get('country_id'),
        loginname=user_data.get('loginname'),
        password=user_data.get('password'),
        telephone=user_data.get('telephone')
    )

    # Assert: Verify successful registration
    assert result is True, "Registration with valid mandatory fields should succeed"

