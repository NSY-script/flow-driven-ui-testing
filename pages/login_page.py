"""
Login Page Object Model

Contains locators and atomic UI actions for the login form.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from base.base_page import BasePage


class LoginPage(BasePage):
    """Page Object for user login."""

    def __init__(self, driver: WebDriver):
        """Initialize LoginPage with WebDriver instance."""
        super().__init__(driver)

    # Locators
    LOGIN_REGISTER_LINK = (By.LINK_TEXT, "Login or register")
    LOGIN_NAME_INPUT = (By.ID, "loginFrm_loginname")
    PASSWORD_INPUT = (By.ID, "loginFrm_password")
    LOGIN_BUTTON = (By.XPATH, "//button[@title='Login']")
    ERROR_MESSAGE_CONTAINER = (By.XPATH, "//*[contains(@class, 'error') or contains(text(), 'Incorrect')]")
    MY_ACCOUNT_INDICATOR = (By.XPATH, "//a[contains(text(), 'My Account')]")
    LOGOUT_LINK = (By.LINK_TEXT, "Logout")

    def click_login_register_link(self) -> None:
        """Click the Login/Register link."""
        self.element_utils.click(self.LOGIN_REGISTER_LINK)

    def enter_login_name(self, login_name: str) -> None:
        """Enter login name/email."""
        self.element_utils.type_text(self.LOGIN_NAME_INPUT, login_name)

    def enter_password(self, password: str) -> None:
        """Enter password."""
        self.element_utils.type_text(self.PASSWORD_INPUT, password)

    def click_login_button(self) -> None:
        """Click the Login button."""
        # Wait for button to be clickable before clicking
        self.wait_utils.wait_for_clickable(self.LOGIN_BUTTON, timeout=10)
        self.element_utils.click(self.LOGIN_BUTTON)

    def get_error_message(self) -> str:
        """Get the error message text."""
        element = self.element_utils.find_element(self.ERROR_MESSAGE_CONTAINER)
        return element.text if element else ""

    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.element_utils.is_displayed(self.ERROR_MESSAGE_CONTAINER)

    def is_my_account_displayed(self) -> bool:
        """Check if My Account indicator is displayed (confirms successful login)."""
        # Use wait utility to ensure page has loaded after login
        element = self.wait_utils.wait_for_visibility(self.MY_ACCOUNT_INDICATOR, timeout=10)
        return element is not None

    def get_my_account_text(self) -> str:
        """Get the My Account link text."""
        element = self.element_utils.find_element(self.MY_ACCOUNT_INDICATOR)
        return element.text if element else ""

    def click_logout_link(self) -> None:
        """Click the Logout link."""
        self.element_utils.click(self.LOGOUT_LINK)

    def is_logout_link_displayed(self) -> bool:
        """Check if Logout link is displayed."""
        return self.element_utils.is_displayed(self.LOGOUT_LINK)
