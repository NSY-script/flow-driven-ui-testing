"""
Test file for verifying user registration with mandatory fields.

This test file validates the business workflow of registering a new user
using ONLY the RegisterFlow class and its verify_registering_with_mandatory_fields method.

Architecture:
- Tests are isolated to the FLOW layer
- Browser setup handled by pytest fixtures
- Test data injected via fixtures
- No direct Page object or Selenium API usage in tests
"""

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
    """
    Test successful registration with valid mandatory fields.

    This test validates the RegisterFlow.verify_registering_with_mandatory_fields
    method by executing the complete registration workflow with only mandatory
    fields (email and password) and verifying successful account creation.

    Args:
        driver: WebDriver fixture for browser automation

    Expected Outcome:
        - Registration flow completes successfully
        - User account is created with valid email and password
        - Success status is returned by the flow method
    """
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

