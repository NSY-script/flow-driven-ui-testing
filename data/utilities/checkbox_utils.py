"""
Checkbox Utilities

Provides safe checkbox and radio button state management.
"""

from selenium.webdriver.remote.webelement import WebElement


class CheckboxUtils:
    """Utility class for checkbox and radio button interactions."""

    @staticmethod
    def is_checked(element: WebElement) -> bool:
        """
        Check if checkbox or radio button is currently selected.

        Args:
            element: Checkbox or radio button WebElement

        Returns:
            True if checked, False if unchecked or error
        """
        try:
            if not element:
                return False
            return element.is_selected()
        except Exception:
            return False

    @staticmethod
    def check(element: WebElement) -> bool:
        """
        Check the checkbox or radio button (click only if unchecked).

        Args:
            element: Checkbox or radio button WebElement

        Returns:
            True if action successful, False otherwise
        """
        try:
            if not element:
                return False

            # Only click if not already checked
            if not element.is_selected():
                element.click()

            return element.is_selected()
        except Exception:
            return False

    @staticmethod
    def uncheck(element: WebElement) -> bool:
        """
        Uncheck the checkbox (click only if checked).

        Args:
            element: Checkbox or radio button WebElement

        Returns:
            True if action successful, False otherwise
        """
        try:
            if not element:
                return False

            # Only click if already checked
            if element.is_selected():
                element.click()

            return not element.is_selected()
        except Exception:
            return False

    @staticmethod
    def toggle(element: WebElement) -> bool:
        """
        Toggle checkbox state (check if unchecked, uncheck if checked).

        Args:
            element: Checkbox or radio button WebElement

        Returns:
            True if action successful, False otherwise
        """
        try:
            if not element:
                return False

            element.click()
            return True
        except Exception:
            return False

    @staticmethod
    def set_state(element: WebElement, checked: bool) -> bool:
        """
        Set checkbox to specific state.

        Args:
            element: Checkbox or radio button WebElement
            checked: Desired state (True = checked, False = unchecked)

        Returns:
            True if action successful and state matches desired state, False otherwise
        """
        try:
            if not element:
                return False

            is_currently_checked = element.is_selected()

            if checked and not is_currently_checked:
                element.click()
            elif not checked and is_currently_checked:
                element.click()

            return element.is_selected() == checked
        except Exception:
            return False
