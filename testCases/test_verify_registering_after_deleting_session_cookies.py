"""
Test: Verify Registration After Deleting Session Cookies

Validates that users can successfully register even after session cookies
are cleared from the browser. This ensures the application maintains
state properly and doesn't depend on persistent session cookies.

Test Scenario:
    1. Delete all browser session cookies
    2. Navigate to registration page
    3. Fill all mandatory registration fields
    4. Submit registration form
    5. Verify success page is displayed

Expected Result:
    - Registration succeeds despite cookie deletion
    - Success confirmation page is displayed
    - Timestamp-based unique email prevents duplicates
"""

import json
import pytest
from datetime import datetime

from config.settings import USERS_DATA_FILE
from pages.register_page import RegisterPage
from flows.register_flow import RegisterFlow


@pytest.mark.ui
@pytest.mark.regression
@pytest.mark.flaky(reruns=2, reruns_delay=2)
def test_verify_registering_after_deleting_session_cookies(browser_driver):
    """
    Test: Registration After Deleting Session Cookies
    
    Verifies that user registration succeeds even after all session cookies
    are cleared from the browser. Tests the application's ability to maintain
    proper state and handle registration without relying on persistent cookies.
    
    Test Flow:
        1. Clear all browser session cookies
        2. Navigate to registration page
        3. Fill mandatory fields (firstname, lastname, email, address, etc.)
        4. Accept terms and conditions
        5. Submit registration
        6. Verify registration success
    
    Assertions:
        - Registration method returns True (success)
        - Success page is displayed
        - No cookie-related errors occur
    
    Markers:
        - @pytest.mark.ui: UI interaction test
        - @pytest.mark.regression: Core functionality test
        - @pytest.mark.flaky: May need retries due to timing
    """
    # ========== Setup ==========
    # Load test data from configuration
    with open(USERS_DATA_FILE, 'r') as file:
        users_data = json.load(file)
    
    user_data = users_data.get('valid_user')
    assert user_data is not None, "Test data 'valid_user' not found in users.json"
    
    # Initialize Page Object and Flow
    register_page = RegisterPage(browser_driver)
    register_flow = RegisterFlow(register_page)
    
    # Generate unique email and login for each test run to avoid "already registered" error
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
    unique_email = f"cookie_deletion_{timestamp}@example.com"
    unique_loginname = f"cookieuser_{timestamp}"
    
    # Extract test data from configuration
    firstname = user_data.get('firstname')
    lastname = user_data.get('lastname')
    email = unique_email
    address = user_data.get('address')
    city = user_data.get('city')
    zone_id = user_data.get('zone_id')
    postcode = user_data.get('postcode')
    country_id = user_data.get('country_id')
    loginname = unique_loginname
    telephone = user_data.get('telephone')
    password = user_data.get('password')
    
    # ========== Test Execution ==========
    # Call the Flow method to perform registration after deleting session cookies
    registration_successful = register_flow.verify_registering_after_deleting_session_cookies(
        firstname=firstname,
        lastname=lastname,
        email=email,
        address=address,
        city=city,
        zone_id=zone_id,
        postcode=postcode,
        country_id=country_id,
        loginname=loginname,
        telephone=telephone,
        password=password,
    )
    
    # ========== Test Assertions ==========
    print(f"\nRegistration Result: {registration_successful}")
    
    # Assert registration was successful
    assert registration_successful is True, (
        "Registration after deleting session cookies should succeed. "
        "Application should handle cookie deletion gracefully."
    )
    
    # Verify success page message (additional validation)
    success_message = register_page.get_success_message()
    print(f"Success Message: {success_message}")
    assert success_message, (
        "Success message should be displayed after registration"
    )
    
    print("\n✓ Test Passed: Registration successful after deleting session cookies")
    print(f"✓ User '{loginname}' registered successfully with email: {email}")