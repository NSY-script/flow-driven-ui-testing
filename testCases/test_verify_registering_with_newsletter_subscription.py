"""
Test file for verifying user registration with newsletter subscription.

This test file validates the business workflow of registering a new user
with newsletter subscription enabled using ONLY the RegisterFlow class
and its verify_registering_with_newsletter_subscription method.

Architecture:
- Tests are isolated to the FLOW layer
- Browser setup handled by pytest fixtures
- Test data injected via fixtures
- No direct Page object or Selenium API usage in tests
"""

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
    """
    Test registration with newsletter subscription enabled.

    This test validates the RegisterFlow.verify_registering_with_newsletter_subscription
    method by executing the complete registration workflow with newsletter
    subscription option enabled and verifying successful account creation.

    Args:
        driver: WebDriver fixture for browser automation

    Expected Outcome:
        - Registration flow completes successfully
        - User account is created with newsletter subscription enabled
        - Success status is returned by the flow method
        - Success page displays "Your Account Has Been Created!"
    """
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
