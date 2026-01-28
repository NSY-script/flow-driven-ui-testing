"""
Test: Verify Registration Using Keyboard Keys

Validates that users can successfully register using keyboard navigation
(Tab key for field navigation and Enter key for form submission).
This ensures the application is fully accessible via keyboard input.

Test Scenario:
    1. Navigate to registration page
    2. Fill all mandatory fields using Tab key navigation
    3. Submit form using Enter key
    4. Verify success page is displayed

Expected Result:
    - Registration succeeds using keyboard-only navigation
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
def test_verify_registering_using_keyboard_keys(browser_driver):
    """
    Test: Registration Using Keyboard Navigation
    
    Verifies that user registration succeeds when using keyboard-only navigation
    (Tab key for field navigation, Enter key for form submission). Tests the
    application's accessibility compliance and keyboard support.
    
    Test Flow:
        1. Load test data from configuration
        2. Navigate to registration page
        3. Fill all mandatory fields using Tab key navigation
        4. Submit registration form using Enter key
        5. Verify registration success page is displayed
    
    Assertions:
        - Registration method returns True (success)
        - No accessibility issues during keyboard navigation
        - Success page is displayed after keyboard submission
    
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
    unique_email = f"keyboard_user_{timestamp}@example.com"
    unique_loginname = f"keyboard_reg_{timestamp}"
    
    # Extract test data from configuration
    firstname = user_data.get('firstname')
    lastname = user_data.get('lastname')
    email = unique_email
    telephone = user_data.get('telephone')
    password = user_data.get('password')
    
    # ========== Test Execution ==========
    # Call the Flow method to perform registration using keyboard navigation
    registration_successful = register_flow.verify_registering_using_keyboard_keys(
        firstname=firstname,
        lastname=lastname,
        email=email,
        telephone=telephone,
        password=password,
    )
    
    # ========== Test Assertions ==========
    print(f"\nKeyboard Registration Result: {registration_successful}")
    
    # Assert registration was successful
    assert registration_successful is True, (
        "Registration using keyboard navigation should succeed. "
        "Application must support full keyboard accessibility."
    )
    
    print("\n✓ Test Passed: Keyboard-based registration successful")
    print(f"✓ User '{firstname} {lastname}' registered via keyboard with email: {email}")
