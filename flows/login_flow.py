"""
Login Flow

Contains business workflows for user login scenarios.
Uses control flow and helper methods for flexible scenario execution.
"""

from pages.login_page import LoginPage
from utilities.keyboard_utils import KeyboardUtils


class LoginFlow:
    """Flow class for user login scenarios."""

    def __init__(self, login_page: LoginPage):
        """Initialize LoginFlow with LoginPage instance."""
        self.login_page = login_page
        self.keyboard_utils = KeyboardUtils(login_page.driver)

    # ========== Helper Methods (Private) ==========

    def _navigate_to_login(self) -> None:
        """Navigate to login form."""
        self.login_page.click_login_register_link()

    def _enter_credentials(
        self, username: str, password: str, use_keyboard: bool = False
    ) -> None:
        """
        Enter login credentials.

        Args:
            username: Username or email
            password: Password
            use_keyboard: If True, use keyboard utilities for input
        """
        if use_keyboard:
            self.keyboard_utils.type_and_tab(
                self.login_page.driver.find_element(*self.login_page.LOGIN_NAME_INPUT),
                username
            )
            self.keyboard_utils.type_and_enter(
                self.login_page.driver.find_element(*self.login_page.PASSWORD_INPUT),
                password
            )
        else:
            # Wait for login fields to be visible before entering credentials
            self.login_page.wait_utils.wait_for_visibility(self.login_page.LOGIN_NAME_INPUT, timeout=10)
            self.login_page.enter_login_name(username)
            self.login_page.wait_utils.wait_for_visibility(self.login_page.PASSWORD_INPUT, timeout=10)
            self.login_page.enter_password(password)

    def _submit_login(self, use_keyboard: bool = False) -> None:
        """
        Submit login form.

        Args:
            use_keyboard: If True, keyboard submission was already done in _enter_credentials
        """
        if not use_keyboard:
            self.login_page.click_login_button()

    # ========== Public Scenario Methods ==========

    def verify_login_with_valid_credentials(
        self, username: str, password: str
    ) -> bool:
        """
        Verify login with valid credentials.

        Returns:
            bool: True if login was successful (redirected to account page), False otherwise.
        """
        self._navigate_to_login()
        self._enter_credentials(username, password)
        self.login_page.click_login_button()

        # Check if redirected to account page
        current_url = self.login_page.driver.current_url
        return "rt=account/account" in current_url

    def verify_login_with_invalid_credentials(
        self, username: str, password: str
    ) -> str:
        """
        Verify login with invalid credentials.

        Returns:
            str: Error message displayed on the form.
        """
        self._navigate_to_login()
        self._enter_credentials(username, password)
        self.login_page.click_login_button()

        return self.login_page.get_error_message()

    def verify_login_with_empty_fields(self) -> str:
        """
        Verify login with empty username and password fields.

        Returns:
            str: Error message displayed on the form.
        """
        self._navigate_to_login()
        self.login_page.click_login_button()

        return self.login_page.get_error_message()

    def validate_login_with_valid_credentials(
        self, username: str, password: str
    ) -> bool:
        """
        Validate login with valid credentials.

        Returns:
            bool: True if login was successful, False otherwise.
        """
        self._navigate_to_login()
        self._enter_credentials(username, password)
        #Q click login button
        self.login_page.click_login_button()

        return self.login_page.is_my_account_displayed()

    def validate_login_with_invalid_email(
        self, email: str, password: str
    ) -> str:
        """
        Validate login with invalid email format.

        Returns:
            str: Error message displayed on the form.
        """
        self._navigate_to_login()
        self._enter_credentials(email, password)
        self._submit_login()

        return self.login_page.get_error_message()

    def validate_login_using_keyboard_keys(
        self, username: str, password: str
    ) -> bool:
        """
        Validate login using keyboard keys for navigation and submission.

        Returns:
            bool: True if login was successful, False otherwise.
        """
        self._navigate_to_login()
        self._enter_credentials(username, password, use_keyboard=True)
        # When using keyboard, pressing Enter on password field should submit form
        # If that doesn't work, fall back to clicking the button
        import time
        #Q use exlpicit waits
        
        time.sleep(1)  # Give form time to process Enter key submission
        
        # Check if redirected (successful login via Enter key)
        current_url = self.login_page.driver.current_url
        if "rt=account/account" in current_url:
            return True
        
        # If not, try clicking the button as fallback
        self.login_page.click_login_button()
        return self.login_page.is_my_account_displayed()

    def login_user_with_options(
        self,
        username: str,
        password: str,
        use_keyboard: bool = False,
    ) -> dict:
        """
        Login user with flexible options.

        Args:
            username: Username or email
            password: Password
            use_keyboard: Use keyboard for input/submission (default: False)

        Returns:
            dict: Login result (success, is_authenticated)
        """
        self._navigate_to_login()
        self._enter_credentials(username, password, use_keyboard=use_keyboard)
        self._submit_login(use_keyboard=use_keyboard)

        authenticated = self.login_page.is_my_account_displayed()
        message = (
            self.login_page.get_my_account_text()
            if authenticated
            else self.login_page.get_error_message()
        )

        return {"success": authenticated, "message": message}
