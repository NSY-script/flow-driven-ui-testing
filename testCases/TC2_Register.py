
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
