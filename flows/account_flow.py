"""
Account Flow

Contains business workflows for account management scenarios.
"""

from pages.account_page import AccountPage


class AccountFlow:
    """Flow class for account management scenarios."""

    def __init__(self, account_page: AccountPage):
        """Initialize AccountFlow with AccountPage instance."""
        self.account_page = account_page

    # ==================== Helper Methods ====================

    def _navigate_to_account_dashboard(self) -> None:
        """Navigate to account dashboard."""
        self.account_page.click_account_dashboard_link()

    def _fill_account_information(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        telephone: str = None,
        company: str = None,
    ) -> None:
        """
        Fill account information form with provided details.

        Args:
            first_name: First name (optional)
            last_name: Last name (optional)
            email: Email address (optional)
            telephone: Telephone number (optional)
            company: Company name (optional)
        """
        if first_name:
            self.account_page.enter_account_first_name(first_name)
        if last_name:
            self.account_page.enter_account_last_name(last_name)
        if email:
            self.account_page.enter_account_email(email)
        if telephone:
            self.account_page.enter_account_telephone(telephone)
        if company:
            self.account_page.enter_account_company(company)

    def _get_account_information(self) -> dict:
        """
        Get current account information.

        Returns:
            dict: Account information (first_name, last_name, email, telephone, company)
        """
        return {
            "first_name": self.account_page.get_account_first_name(),
            "last_name": self.account_page.get_account_last_name(),
            "email": self.account_page.get_account_email(),
            "telephone": self.account_page.get_account_telephone(),
            "company": self.account_page.get_account_company(),
        }

    def _change_password(
        self,
        current_password: str,
        new_password: str,
        confirm_password: str,
    ) -> None:
        """
        Change account password.

        Args:
            current_password: Current password
            new_password: New password
            confirm_password: Confirm new password
        """
        self.account_page.click_change_password_link()
        self.account_page.enter_current_password(current_password)
        self.account_page.enter_new_password(new_password)
        self.account_page.enter_confirm_password(confirm_password)
        self.account_page.click_change_password_button()

    # ==================== Public Scenario Methods ====================

    def verify_view_account_dashboard(self) -> bool:
        """
        Verify account dashboard is displayed.

        Returns:
            bool: True if account dashboard is visible, False otherwise
        """
        self._navigate_to_account_dashboard()
        return self.account_page.is_account_dashboard_displayed()

    def verify_account_dashboard_has_required_sections(self) -> dict:
        """
        Verify account dashboard displays all required sections.

        Returns:
            dict: Dashboard sections status (dashboard, info_section, edit_button, logout_link)
        """
        self._navigate_to_account_dashboard()

        return {
            "dashboard_displayed": self.account_page.is_account_dashboard_displayed(),
            "info_section_displayed": self.account_page.is_account_information_section_displayed(),
            "edit_button_displayed": self.account_page.is_edit_account_button_displayed(),
            "logout_link_displayed": self.account_page.is_logout_link_displayed(),
        }

    def verify_update_account_information(
        self,
        first_name: str,
        last_name: str,
        email: str,
        telephone: str,
    ) -> bool:
        """
        Verify updating account information.

        Returns:
            bool: True if account update was successful, False otherwise
        """
        self._navigate_to_account_dashboard()
        self.account_page.click_edit_account_button()
        self._fill_account_information(
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
        )
        self.account_page.click_save_changes_button()

        success_message = self.account_page.get_success_message()
        return bool(success_message)

    def verify_update_account_information_displays_saved_data(
        self,
        first_name: str,
        last_name: str,
        email: str,
        telephone: str,
    ) -> dict:
        """
        Verify updated account information is displayed correctly.

        Returns:
            dict: Account information after update
        """
        self._navigate_to_account_dashboard()
        self.account_page.click_edit_account_button()
        self._fill_account_information(
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
        )
        self.account_page.click_save_changes_button()

        return self._get_account_information()

    def verify_account_update_with_invalid_email(
        self,
        first_name: str,
        invalid_email: str,
    ) -> str:
        """
        Verify account update rejects invalid email format.

        Returns:
            str: Error message displayed
        """
        self._navigate_to_account_dashboard()
        self.account_page.click_edit_account_button()
        self._fill_account_information(
            first_name=first_name,
            email=invalid_email,
        )
        self.account_page.click_save_changes_button()

        return self.account_page.get_error_message()

    def verify_account_update_with_missing_required_field(
        self,
        last_name: str,
    ) -> str:
        """
        Verify account update rejects missing required field.

        Returns:
            str: Error message displayed
        """
        self._navigate_to_account_dashboard()
        self.account_page.click_edit_account_button()
        # First name is typically required - not filling it
        self._fill_account_information(
            last_name=last_name,
        )
        self.account_page.click_save_changes_button()

        return self.account_page.get_error_message()

    def verify_change_account_password(
        self,
        current_password: str,
        new_password: str,
        confirm_password: str,
    ) -> bool:
        """
        Verify changing account password.

        Returns:
            bool: True if password change was successful, False otherwise
        """
        self._navigate_to_account_dashboard()
        self._change_password(current_password, new_password, confirm_password)

        success_message = self.account_page.get_success_message()
        return bool(success_message)

    def verify_change_password_with_incorrect_current_password(
        self,
        incorrect_password: str,
        new_password: str,
        confirm_password: str,
    ) -> str:
        """
        Verify password change rejects incorrect current password.

        Returns:
            str: Error message displayed
        """
        self._navigate_to_account_dashboard()
        self._change_password(incorrect_password, new_password, confirm_password)

        return self.account_page.get_error_message()

    def verify_change_password_with_mismatched_passwords(
        self,
        current_password: str,
        new_password: str,
        mismatched_confirm_password: str,
    ) -> str:
        """
        Verify password change rejects mismatched new passwords.

        Returns:
            str: Error message displayed
        """
        self._navigate_to_account_dashboard()
        self._change_password(current_password, new_password, mismatched_confirm_password)

        return self.account_page.get_error_message()

    def verify_account_information_form_is_editable(self) -> bool:
        """
        Verify account information form is editable.

        Returns:
            bool: True if form fields are accessible, False otherwise
        """
        self._navigate_to_account_dashboard()
        self.account_page.click_edit_account_button()

        return self.account_page.is_account_information_form_displayed()

    def verify_save_button_is_enabled_with_valid_data(
        self,
        first_name: str,
        last_name: str,
    ) -> bool:
        """
        Verify save button is enabled when valid data is provided.

        Returns:
            bool: True if save button is enabled, False otherwise
        """
        self._navigate_to_account_dashboard()
        self.account_page.click_edit_account_button()
        self._fill_account_information(
            first_name=first_name,
            last_name=last_name,
        )

        return self.account_page.is_save_changes_button_enabled()

    def update_account_with_flexible_options(
        self,
        first_name: str = None,
        last_name: str = None,
        email: str = None,
        telephone: str = None,
        company: str = None,
        change_password: bool = False,
        current_password: str = None,
        new_password: str = None,
        confirm_password: str = None,
    ) -> dict:
        """
        Update account with flexible options.

        Args:
            first_name: First name (optional)
            last_name: Last name (optional)
            email: Email address (optional)
            telephone: Telephone number (optional)
            company: Company name (optional)
            change_password: Whether to change password (default: False)
            current_password: Current password (required if change_password=True)
            new_password: New password (required if change_password=True)
            confirm_password: Confirm new password (required if change_password=True)

        Returns:
            dict: Account update result (success, message, account_info)
        """
        self._navigate_to_account_dashboard()
        self.account_page.click_edit_account_button()

        # Update account information
        self._fill_account_information(
            first_name=first_name,
            last_name=last_name,
            email=email,
            telephone=telephone,
            company=company,
        )
        self.account_page.click_save_changes_button()

        # Change password if requested
        if change_password:
            if current_password and new_password and confirm_password:
                self._change_password(current_password, new_password, confirm_password)

        success_message = self.account_page.get_success_message()
        error_message = self.account_page.get_error_message()

        return {
            "success": bool(success_message and not error_message),
            "success_message": success_message,
            "error_message": error_message,
            "account_info": self._get_account_information(),
        }
    
