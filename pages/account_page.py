"""
Account Page

Page object for account management functionality.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from base.base_page import BasePage


class AccountPage(BasePage):
    """Page object for account management functionality."""

    def __init__(self, driver: WebDriver):
        """Initialize AccountPage with WebDriver instance."""
        super().__init__(driver)
        self.wait = WebDriverWait(driver, 10)

    # ==================== Locators ====================

    ACCOUNT_DASHBOARD_LINK = (By.XPATH, "//a[contains(text(), 'Account Dashboard')]")
    ACCOUNT_INFORMATION_LINK = (By.XPATH, "//a[contains(text(), 'Account Information')]")
    EDIT_ACCOUNT_BUTTON = (By.ID, "edit-account-button")
    EDIT_ACCOUNT_LINK = (By.XPATH, "//a[contains(text(), 'Edit Account')]")

    # Account Information Fields
    ACCOUNT_FIRST_NAME = (By.ID, "account_firstname")
    ACCOUNT_LAST_NAME = (By.ID, "account_lastname")
    ACCOUNT_EMAIL = (By.ID, "account_email")
    ACCOUNT_TELEPHONE = (By.ID, "account_telephone")
    ACCOUNT_COMPANY = (By.ID, "account_company")

    # Account Details
    ACCOUNT_ADDRESS_BOOK = (By.XPATH, "//a[contains(text(), 'Address Book')]")
    CHANGE_PASSWORD_LINK = (By.XPATH, "//a[contains(text(), 'Change Password')]")
    CHANGE_PASSWORD_BUTTON = (By.ID, "change-password-button")

    # Password Fields
    CURRENT_PASSWORD = (By.ID, "current_password")
    NEW_PASSWORD = (By.ID, "new_password")
    CONFIRM_PASSWORD = (By.ID, "confirm_password")

    # Account Dashboard Elements
    ACCOUNT_DASHBOARD_HEADER = (By.CLASS_NAME, "account-dashboard-header")
    ACCOUNT_INFORMATION_SECTION = (By.CLASS_NAME, "account-information-section")
    ORDERS_HISTORY_LINK = (By.XPATH, "//a[contains(text(), 'Order History')]")
    WISHLIST_LINK = (By.XPATH, "//a[contains(text(), 'Wishlist')]")
    DOWNLOADS_LINK = (By.XPATH, "//a[contains(text(), 'Downloads')]")
    LOGOUT_LINK = (By.XPATH, "//a[contains(text(), 'Logout')]")

    # Save and Cancel Buttons
    SAVE_CHANGES_BUTTON = (By.ID, "save-account-changes")
    SAVE_BUTTON = (By.XPATH, "//button[contains(text(), 'Save')]")
    CANCEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Cancel')]")

    # Messages and Indicators
    SUCCESS_MESSAGE_CONTAINER = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE_CONTAINER = (By.CLASS_NAME, "error-message")
    NOTIFICATION_CONTAINER = (By.CLASS_NAME, "notification")

    # ==================== Atomic Actions ====================

    def click_account_dashboard_link(self) -> None:
        """Click account dashboard link."""
        self.wait.until(EC.element_to_be_clickable(self.ACCOUNT_DASHBOARD_LINK)).click()

    def click_account_information_link(self) -> None:
        """Click account information link."""
        self.wait.until(EC.element_to_be_clickable(self.ACCOUNT_INFORMATION_LINK)).click()

    def click_edit_account_button(self) -> None:
        """Click edit account button."""
        self.wait.until(EC.element_to_be_clickable(self.EDIT_ACCOUNT_BUTTON)).click()

    def click_edit_account_link(self) -> None:
        """Click edit account link."""
        self.wait.until(EC.element_to_be_clickable(self.EDIT_ACCOUNT_LINK)).click()

    def enter_account_first_name(self, first_name: str) -> None:
        """Enter account first name."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_FIRST_NAME))
        element.clear()
        element.send_keys(first_name)

    def enter_account_last_name(self, last_name: str) -> None:
        """Enter account last name."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_LAST_NAME))
        element.clear()
        element.send_keys(last_name)

    def enter_account_email(self, email: str) -> None:
        """Enter account email."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_EMAIL))
        element.clear()
        element.send_keys(email)

    def enter_account_telephone(self, telephone: str) -> None:
        """Enter account telephone."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_TELEPHONE))
        element.clear()
        element.send_keys(telephone)

    def enter_account_company(self, company: str) -> None:
        """Enter account company."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_COMPANY))
        element.clear()
        element.send_keys(company)

    def get_account_first_name(self) -> str:
        """Get account first name value."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_FIRST_NAME))
        return element.get_attribute("value")

    def get_account_last_name(self) -> str:
        """Get account last name value."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_LAST_NAME))
        return element.get_attribute("value")

    def get_account_email(self) -> str:
        """Get account email value."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_EMAIL))
        return element.get_attribute("value")

    def get_account_telephone(self) -> str:
        """Get account telephone value."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_TELEPHONE))
        return element.get_attribute("value")

    def get_account_company(self) -> str:
        """Get account company value."""
        element = self.wait.until(EC.presence_of_element_located(self.ACCOUNT_COMPANY))
        return element.get_attribute("value")

    def click_change_password_link(self) -> None:
        """Click change password link."""
        self.wait.until(EC.element_to_be_clickable(self.CHANGE_PASSWORD_LINK)).click()

    def click_change_password_button(self) -> None:
        """Click change password button."""
        self.wait.until(EC.element_to_be_clickable(self.CHANGE_PASSWORD_BUTTON)).click()

    def enter_current_password(self, password: str) -> None:
        """Enter current password."""
        element = self.wait.until(EC.presence_of_element_located(self.CURRENT_PASSWORD))
        element.clear()
        element.send_keys(password)

    def enter_new_password(self, password: str) -> None:
        """Enter new password."""
        element = self.wait.until(EC.presence_of_element_located(self.NEW_PASSWORD))
        element.clear()
        element.send_keys(password)

    def enter_confirm_password(self, password: str) -> None:
        """Enter confirm password."""
        element = self.wait.until(EC.presence_of_element_located(self.CONFIRM_PASSWORD))
        element.clear()
        element.send_keys(password)

    def click_save_changes_button(self) -> None:
        """Click save changes button."""
        self.wait.until(EC.element_to_be_clickable(self.SAVE_CHANGES_BUTTON)).click()

    def click_save_button(self) -> None:
        """Click save button."""
        self.wait.until(EC.element_to_be_clickable(self.SAVE_BUTTON)).click()

    def click_cancel_button(self) -> None:
        """Click cancel button."""
        self.wait.until(EC.element_to_be_clickable(self.CANCEL_BUTTON)).click()

    def click_orders_history_link(self) -> None:
        """Click orders history link."""
        self.wait.until(EC.element_to_be_clickable(self.ORDERS_HISTORY_LINK)).click()

    def click_wishlist_link(self) -> None:
        """Click wishlist link."""
        self.wait.until(EC.element_to_be_clickable(self.WISHLIST_LINK)).click()

    def click_downloads_link(self) -> None:
        """Click downloads link."""
        self.wait.until(EC.element_to_be_clickable(self.DOWNLOADS_LINK)).click()

    def click_logout_link(self) -> None:
        """Click logout link."""
        self.wait.until(EC.element_to_be_clickable(self.LOGOUT_LINK)).click()

    def get_success_message(self) -> str:
        """Get success message."""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.SUCCESS_MESSAGE_CONTAINER))
            return element.text
        except Exception:
            return ""

    def get_error_message(self) -> str:
        """Get error message."""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.ERROR_MESSAGE_CONTAINER))
            return element.text
        except Exception:
            return ""

    def get_notification_message(self) -> str:
        """Get notification message."""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.NOTIFICATION_CONTAINER))
            return element.text
        except Exception:
            return ""

    def is_account_dashboard_displayed(self) -> bool:
        """Check if account dashboard is displayed."""
        try:
            self.wait.until(EC.presence_of_element_located(self.ACCOUNT_DASHBOARD_HEADER))
            return True
        except Exception:
            return False

    def is_account_information_section_displayed(self) -> bool:
        """Check if account information section is displayed."""
        try:
            self.wait.until(EC.presence_of_element_located(self.ACCOUNT_INFORMATION_SECTION))
            return True
        except Exception:
            return False

    def is_account_information_form_displayed(self) -> bool:
        """Check if account information form (editable fields) is displayed."""
        try:
            self.wait.until(EC.presence_of_element_located(self.ACCOUNT_FIRST_NAME))
            return True
        except Exception:
            return False

    def is_save_changes_button_displayed(self) -> bool:
        """Check if save changes button is displayed."""
        try:
            self.wait.until(EC.presence_of_element_located(self.SAVE_CHANGES_BUTTON))
            return True
        except Exception:
            return False

    def is_save_changes_button_enabled(self) -> bool:
        """Check if save changes button is enabled."""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.SAVE_CHANGES_BUTTON))
            return element.is_enabled()
        except Exception:
            return False

    def is_edit_account_button_displayed(self) -> bool:
        """Check if edit account button is displayed."""
        try:
            self.wait.until(EC.presence_of_element_located(self.EDIT_ACCOUNT_BUTTON))
            return True
        except Exception:
            return False

    def is_logout_link_displayed(self) -> bool:
        """Check if logout link is displayed."""
        try:
            self.wait.until(EC.presence_of_element_located(self.LOGOUT_LINK))
            return True
        except Exception:
            return False
