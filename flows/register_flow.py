"""
Register Flow

Contains business workflows for user registration scenarios.
Uses control flow and helper methods for flexible scenario execution.
"""

from selenium.webdriver.common.keys import Keys
from pages.register_page import RegisterPage
from utilities.keyboard_utils import KeyboardUtils
from utilities.session_utils import SessionUtils


class RegisterFlow:
    """Flow class for user registration scenarios."""

    def __init__(self, register_page: RegisterPage):
        """Initialize RegisterFlow with RegisterPage instance."""
        self.register_page = register_page
        self.keyboard_utils = KeyboardUtils(register_page.driver)
        self.session_utils = SessionUtils(register_page.driver)

    # ========== Helper Methods (Private) ==========

    def _navigate_to_register(self) -> None:
        """Navigate to registration form."""
        self.register_page.navigate_to_register_page()

    def _fill_mandatory_fields(
        self,
        firstname: str,
        lastname: str,
        email: str,
        address: str,
        city: str,
        zone_id: str,
        postcode: str,
        country_id: str,
        loginname: str,
        password: str,
        telephone: str = "",
        fax: str = "",
        company: str = "",
        use_slow_typing: bool = False,
    ) -> None:
        """
        Fill all mandatory registration fields.

        Args:
            firstname: First name
            lastname: Last name
            email: Email address
            address: Street address
            city: City name
            zone_id: State/Province zone ID
            postcode: Postal code
            country_id: Country ID
            loginname: Login username
            password: Password
            telephone: Telephone number (optional)
            fax: Fax number (optional)
            company: Company name (optional)
            use_slow_typing: If True, use keyboard utils for slow typing
        """
        self.register_page.enter_firstname(firstname)
        self.register_page.enter_lastname(lastname)
        self.register_page.enter_email(email)
        if telephone:
            self.register_page.enter_telephone(telephone)
        if fax:
            self.register_page.enter_fax(fax)
        if company:
            self.register_page.enter_company(company)
        self.register_page.enter_address(address)
        self.register_page.enter_city(city)
        
        # IMPORTANT: Select country FIRST, then zone
        # Zone options are dynamically populated based on country selection
        self.register_page.select_country(country_id)
        
        # Add a small delay to allow zone dropdown to be repopulated
        import time
        time.sleep(0.5)
        
        self.register_page.select_zone(zone_id)
        self.register_page.enter_postcode(postcode)
        
        print(f"DEBUG: Entering login name: {loginname}")
        self.register_page.enter_loginname(loginname)
        
        print(f"DEBUG: Entering password: {password[:3]}...")
        self.register_page.enter_password(password)
        
        print(f"DEBUG: Entering confirm password: {password[:3]}...")
        self.register_page.enter_confirm_password(password)

    def _submit_registration(
        self,
        newsletter_subscription: bool = False,
        accept_terms: bool = True,
        use_keyboard: bool = False,
    ) -> None:
        """
        Submit registration form with optional settings.

        Args:
            newsletter_subscription: If True, select newsletter Yes
            accept_terms: If True, check terms and conditions checkbox
            use_keyboard: If True, use keyboard Enter key for submission
        """
        if newsletter_subscription:
            print("DEBUG: Selecting newsletter: Yes")
            self.register_page.select_newsletter_yes()
        else:
            print("DEBUG: Selecting newsletter: No")
            self.register_page.select_newsletter_no()

        if accept_terms:
            print("DEBUG: Checking terms and conditions")
            self.register_page.check_terms_and_conditions()

        print("DEBUG: Clicking Continue button")
        if use_keyboard:
            self.keyboard_utils.press_enter(
                self.register_page.driver.find_element(*self.register_page.CONTINUE_BUTTON)
            )
        else:
            self.register_page.click_continue_button()
        
        print("DEBUG: Form submitted")

    def _handle_save_address_alert(self) -> None:
        """Dismiss the 'Save address?' alert popup by clicking Save button."""
        try:
            import time
            from selenium.webdriver.common.by import By
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.common.exceptions import (
                TimeoutException,
            )
            
            print("DEBUG: _handle_save_address_alert() started", flush=True)
            
            driver = self.register_page.driver
            print(f"DEBUG: Got driver: {driver is not None}", flush=True)
            
            # Give browser time to show alert
            time.sleep(1)
            print("DEBUG: After initial sleep", flush=True)
            
            # Try to handle browser native JavaScript alert
            try:
                print("DEBUG: Attempting to get JavaScript alert...", flush=True)
                wait = WebDriverWait(driver, 2)
                alert = wait.until(EC.alert_is_present())
                print("DEBUG: JavaScript alert found, dismissing...", flush=True)
                alert.dismiss()
                print("DEBUG: JavaScript alert dismissed", flush=True)
                return
            except Exception as e:
                print(f"DEBUG: No JavaScript alert: {str(e)}", flush=True)
            
            # Look for HTML modal dialog
            print("DEBUG: Looking for modal dialog...", flush=True)
            try:
                wait = WebDriverWait(driver, 3)
                # Try a simple selector first
                modals = driver.find_elements(By.XPATH, "//div[@role='dialog']")
                print(f"DEBUG: Found {len(modals)} modal elements", flush=True)
                
                if not modals:
                    print("DEBUG: No modals found, checking for buttons anyway...", flush=True)
            except Exception as e:
                print(f"DEBUG: Error checking for modals: {str(e)}", flush=True)
            
            # Try multiple button selectors to find and click Save button
            button_selectors = [
                "//button[contains(text(), 'Save')]",
                "//div[@role='dialog']//button[contains(text(), 'Save')]",
                "//button[contains(., 'Save')]",
                "//div//button[1]",
            ]
            
            for selector in button_selectors:
                try:
                    print(f"DEBUG: Trying selector: {selector}", flush=True)
                    wait = WebDriverWait(driver, 1)
                    button = wait.until(
                        EC.element_to_be_clickable((By.XPATH, selector))
                    )
                    print(f"DEBUG: Found and clicking button with selector: {selector}", flush=True)
                    button.click()
                    print("DEBUG: Button clicked successfully", flush=True)
                    time.sleep(1)  # Give modal time to close
                    return
                except TimeoutException:
                    print(f"DEBUG: Timeout on selector: {selector}", flush=True)
                    continue
                except Exception as e:
                    print(f"DEBUG: Failed on selector {selector}: {type(e).__name__}", flush=True)
                    continue
            
            print("DEBUG: Could not find or click any Save button", flush=True)
            
        except Exception as outer_e:
            print(f"DEBUG: OUTER EXCEPTION in _handle_save_address_alert: {str(outer_e)}", flush=True)
            import traceback
            traceback.print_exc()
            raise

    # ========== Public Scenario Methods ==========

    def verify_registering_with_mandatory_fields(
        self,
        firstname: str,
        lastname: str,
        email: str,
        address: str,
        city: str,
        zone_id: str,
        postcode: str,
        country_id: str,
        loginname: str,
        password: str,
        telephone: str = "",
    ) -> bool:
        """
        Verify registration with all mandatory fields.

        Returns:
            bool: True if registration was successful, False otherwise.
        """
        self._navigate_to_register()
        self._fill_mandatory_fields(
            firstname=firstname,
            lastname=lastname,
            email=email,
            address=address,
            city=city,
            zone_id=zone_id,
            postcode=postcode,
            country_id=country_id,
            loginname=loginname,
            password=password,
            telephone=telephone,
        )
        self._submit_registration(newsletter_subscription=False, accept_terms=True)
        self._handle_save_address_alert()
        
        # Check if we reached the success page and close the browser immediately
        is_success = self.register_page.is_success_message_displayed()
        if is_success:
            print("DEBUG: Registration successful - closing browser")
            self.register_page.driver.quit()
        
        return is_success

    def verify_registering_with_newsletter_subscription(
        self,
        firstname: str,
        lastname: str,
        email: str,
        telephone: str,
        password: str,
        address: str = "123 Main Street",
        city: str = "New York",
        zone_id: str = "New York",
        postcode: str = "10001",
        country_id: str = "United States",
        loginname: str = None,
        fax: str = "",
        company: str = "",
    ) -> bool:
        """
        Verify registration with newsletter subscription enabled.

        Implements the complete registration flow with newsletter subscription:
        1. Navigate to register page
        2. Click Login or register link
        3. Click Continue button
        4. Fill in all mandatory fields (firstname, lastname, email, telephone, etc.)
        5. Enter password and confirm password
        6. Select newsletter subscription (Yes)
        7. Accept terms and conditions
        8. Click Continue button
        9. Verify success page

        Args:
            firstname: User first name
            lastname: User last name
            email: User email address
            telephone: User telephone number
            password: User password
            address: Street address (default: "123 Main Street")
            city: City name (default: "New York")
            zone_id: State/Province (default: "New York")
            postcode: Postal code (default: "10001")
            country_id: Country (default: "United States")
            loginname: Login name/username (if None, uses email)
            fax: Fax number (optional)
            company: Company name (optional)

        Returns:
            bool: True if registration was successful, False otherwise.
        """
        # Use email as login name if not provided
        if loginname is None:
            loginname = email
        
        # Step 1: Navigate to register page
        self._navigate_to_register()
        
        # Step 2-3: The navigation already handles the initial page load
        
        # Step 4-6: Fill all mandatory fields
        self._fill_mandatory_fields(
            firstname=firstname,
            lastname=lastname,
            email=email,
            address=address,
            city=city,
            zone_id=zone_id,
            postcode=postcode,
            country_id=country_id,
            loginname=loginname,
            password=password,
            telephone=telephone,
            fax=fax,
            company=company,
        )
        
        # Step 7-8: Submit registration with newsletter subscription enabled
        self._submit_registration(newsletter_subscription=True, accept_terms=True)
        
        # Step 9: Verify success
        return self.register_page.is_success_message_displayed()

    def verify_registering_with_missing_mandatory_fields(
        self, firstname: str, email: str
    ) -> str:
        """
        Verify registration with missing mandatory fields.

        Returns:
            str: Error message displayed on the form.
        """
        self._navigate_to_register()
        self.register_page.enter_firstname(firstname)
        self.register_page.enter_email(email)
        self.register_page.click_continue_button()

        return self.register_page.get_error_message()

    def verify_registering_with_invalid_email(
        self,
        firstname: str,
        lastname: str,
        email: str,
        telephone: str,
        password: str,
    ) -> str:
        """
        Verify registration with invalid email format.

        Returns:
            str: Error message displayed on the form.
        """
        self._navigate_to_register()
        self._fill_mandatory_fields(firstname, lastname, email, telephone, password)
        self._submit_registration(newsletter_subscription=False, accept_terms=True)

        return self.register_page.get_error_message()

    def verify_registering_with_slow_typing(
        self,
        firstname: str,
        lastname: str,
        email: str,
        telephone: str,
        password: str,
        address: str = "123 Main Street",
        city: str = "London",
        zone_id: str = "Surrey",
        postcode: str = "SW1A 1AA",
        country_id: str = "United Kingdom",
        loginname: str = "",
    ) -> bool:
        """
        Verify registration with slow character-by-character typing.

        Returns:
            bool: True if registration was successful, False otherwise.
        """
        self._navigate_to_register()
        self._fill_mandatory_fields(
            firstname=firstname,
            lastname=lastname,
            email=email,
            address=address,
            city=city,
            zone_id=zone_id,
            postcode=postcode,
            country_id=country_id,
            loginname=loginname,
            password=password,
            telephone=telephone,
            use_slow_typing=True
        )
        self._submit_registration(newsletter_subscription=False, accept_terms=True)

        return self.register_page.is_success_message_displayed()

    def verify_registering_after_deleting_session_cookies(
        self,
        firstname: str,
        lastname: str,
        email: str,
        address: str,
        city: str,
        zone_id: str,
        postcode: str,
        country_id: str,
        loginname: str,
        telephone: str,
        password: str,
    ) -> bool:
        """
        Verify registration after clearing all session cookies.
        
        Tests that the application is stateless/session-independent.
        Sequence:
        1. Navigate to register page (establish initial context)
        2. Delete all cookies (simulate session loss)
        3. Navigate again (establish fresh session)
        4. Fill form and submit (ensure registration works with fresh session)
        5. Handle browser "Save address?" alert
        6. Verify success page is displayed

        Returns:
            bool: True if registration was successful, False otherwise.
        """
        # Establish initial session context
        self._navigate_to_register()
        
        # Delete all cookies to simulate session loss
        self.session_utils.delete_all_cookies()
        
        # Navigate again with fresh session
        self._navigate_to_register()
        
        # Fill form and submit with clean session
        self._fill_mandatory_fields(
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
        self._submit_registration(newsletter_subscription=False, accept_terms=True)
        
        # Handle the "Save address?" alert that appears after form submission
        self._handle_save_address_alert()

        return self.register_page.is_success_message_displayed()

    def verify_registering_using_keyboard_keys(
        self,
        firstname: str,
        lastname: str,
        email: str,
        telephone: str,
        password: str,
        address: str = "123 Main Street",
        city: str = "Surrey",
        zone_id: str = "Surrey",
        postcode: str = "SW1A 1AA",
        country_id: str = "United Kingdom",
        loginname: str = "",
        fax: str = "",
        company: str = "",
    ) -> bool:
        """
        Verify registration using keyboard navigation (Tab/Enter).
        
        Supports both quick and full registration with optional address fields.

        Returns:
            bool: True if registration was successful, False otherwise.
        """
        self._navigate_to_register()
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.FIRSTNAME_INPUT),
            firstname
        )
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.LASTNAME_INPUT),
            lastname
        )
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.EMAIL_INPUT),
            email
        )
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.TELEPHONE_INPUT),
            telephone
        )
        if fax:
            self.keyboard_utils.type_and_tab(
                self.register_page.driver.find_element(*self.register_page.FAX_INPUT),
                fax
            )
        else:
            self.keyboard_utils.send_key(
                self.register_page.driver.find_element(*self.register_page.FAX_INPUT),
                "Tab"
            )
        if company:
            self.keyboard_utils.type_and_tab(
                self.register_page.driver.find_element(*self.register_page.COMPANY_INPUT),
                company
            )
        else:
            self.keyboard_utils.send_key(
                self.register_page.driver.find_element(*self.register_page.COMPANY_INPUT),
                "Tab"
            )
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.ADDRESS_INPUT),
            address
        )
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.CITY_INPUT),
            city
        )
        # Select country FIRST, then zone (zone options depend on country selection)
        self.register_page.select_country(country_id)
        
        # Add delay to allow zone dropdown to repopulate after country change
        import time
        time.sleep(0.5)
        
        self.register_page.select_zone(zone_id)
        
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.POSTCODE_INPUT),
            postcode
        )
        
        if not loginname:
            from datetime import datetime
            loginname = f"kb_user_{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.LOGINNAME_INPUT),
            loginname
        )
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.PASSWORD_INPUT),
            password
        )
        self.keyboard_utils.type_and_tab(
            self.register_page.driver.find_element(*self.register_page.CONFIRM_PASSWORD_INPUT),
            password
        )
        self._submit_registration(
            newsletter_subscription=False, accept_terms=True, use_keyboard=True
        )

        return self.register_page.is_success_message_displayed()

    def register_new_user_with_options(
        self,
        firstname: str,
        lastname: str,
        email: str,
        telephone: str,
        password: str,
        newsletter: bool = False,
        accept_terms: bool = True,
        use_slow_typing: bool = False,
        use_keyboard: bool = False,
    ) -> dict:
        """
        Register new user with flexible option combinations.

        Highly flexible scenario supporting multiple input methods and options.

        Args:
            firstname: User first name
            lastname: User last name
            email: User email
            telephone: User telephone
            password: User password
            newsletter: Subscribe to newsletter (default: False)
            accept_terms: Accept terms and conditions (default: True)
            use_slow_typing: Use slow character-by-character typing (default: False)
            use_keyboard: Use keyboard for navigation (default: False)

        Returns:
            dict: Registration result (success, message)
        """
        self._navigate_to_register()
        self._fill_mandatory_fields(
            firstname, lastname, email, telephone, password, use_slow_typing=use_slow_typing
        )
        self._submit_registration(
            newsletter_subscription=newsletter,
            accept_terms=accept_terms,
            use_keyboard=use_keyboard,
        )

        success = self.register_page.is_success_message_displayed()
        message = (
            self.register_page.get_success_message()
            if success
            else self.register_page.get_error_message()
        )

        return {"success": success, "message": message}
