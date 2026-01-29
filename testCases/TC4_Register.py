
import json
import pytest
from datetime import datetime

from config.settings import USERS_DATA_FILE
from pages.register_page import RegisterPage
from flows.register_flow import RegisterFlow


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.register
def test_verify_registering_with_newsletter_subscription(driver):
    # Arrange: Load valid test user data from configuration
    with open(USERS_DATA_FILE, 'r') as file:
        users_data = json.load(file)
    
    user_data = users_data.get('valid_user')
    assert user_data is not None, "Test data 'valid_user' not found in users.json"

    # Generate unique email for each test run to avoid "already registered" error
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    unique_email = f"newsletter_user_{timestamp}@example.com"
    unique_loginname = f"newsletter_user_{timestamp}"
    
    # Act: Execute the registration flow with newsletter subscription enabled
    register_page = RegisterPage(driver)
    register_flow = RegisterFlow(register_page)
    
    result = register_flow.verify_registering_with_newsletter_subscription(
        firstname=user_data.get('firstname'),
        lastname=user_data.get('lastname'),
        email=unique_email,
        telephone=user_data.get('telephone'),
        password=user_data.get('password'),
        address=user_data.get('address'),
        city=user_data.get('city'),
        zone_id=user_data.get('zone_id'),
        postcode=user_data.get('postcode'),
        country_id=user_data.get('country_id'),
        loginname=unique_loginname
    )
    
    # Assert: Verify successful registration with newsletter subscription
    assert result is True, "Registration with newsletter subscription should succeed"
