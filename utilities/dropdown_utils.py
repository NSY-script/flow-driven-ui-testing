"""
Dropdown Utilities

Provides generic dropdown/select element handling using Selenium Select.
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select
from typing import Optional, List


class DropdownUtils:
    """Utility class for dropdown and select element interactions."""

    @staticmethod
    def select_by_visible_text(element: WebElement, text: str) -> bool:
        """
        Select option by visible text.

        Args:
            element: Select WebElement
            text: Visible text of the option to select

        Returns:
            True if selection successful, False otherwise
        """
        try:
            if not element:
                return False
            select = Select(element)
            select.select_by_visible_text(text)
            return True
        except Exception:
            return False

    @staticmethod
    def select_by_value(element: WebElement, value: str) -> bool:
        """
        Select option by value attribute.

        Args:
            element: Select WebElement
            value: Value attribute of the option to select

        Returns:
            True if selection successful, False otherwise
        """
        try:
            if not element:
                return False
            select = Select(element)
            select.select_by_value(value)
            return True
        except Exception:
            return False

    @staticmethod
    def select_by_index(element: WebElement, index: int) -> bool:
        """
        Select option by index (0-based).

        Args:
            element: Select WebElement
            index: Index of the option to select

        Returns:
            True if selection successful, False otherwise
        """
        try:
            if not element or index < 0:
                return False
            select = Select(element)
            select.select_by_index(index)
            return True
        except Exception:
            return False

    @staticmethod
    def get_selected_option_text(element: WebElement) -> Optional[str]:
        """
        Get the visible text of the currently selected option.

        Args:
            element: Select WebElement

        Returns:
            Text of selected option, or None if no selection
        """
        try:
            if not element:
                return None
            select = Select(element)
            selected_option = select.first_selected_option
            return selected_option.text if selected_option else None
        except Exception:
            return None

    @staticmethod
    def get_selected_option_value(element: WebElement) -> Optional[str]:
        """
        Get the value attribute of the currently selected option.

        Args:
            element: Select WebElement

        Returns:
            Value of selected option, or None if no selection
        """
        try:
            if not element:
                return None
            select = Select(element)
            selected_option = select.first_selected_option
            return selected_option.get_attribute("value") if selected_option else None
        except Exception:
            return None

    @staticmethod
    def get_all_options(element: WebElement) -> List[str]:
        """
        Get all available option texts in the dropdown.

        Args:
            element: Select WebElement

        Returns:
            List of option texts, empty list if none or error
        """
        try:
            if not element:
                return []
            select = Select(element)
            options = select.options
            return [option.text for option in options]
        except Exception:
            return []

    @staticmethod
    def is_multiple(element: WebElement) -> bool:
        """
        Check if dropdown supports multiple selections.

        Args:
            element: Select WebElement

        Returns:
            True if multiple selection is supported, False otherwise
        """
        try:
            if not element:
                return False
            select = Select(element)
            return select.is_multiple
        except Exception:
            return False

    @staticmethod
    def deselect_all(element: WebElement) -> bool:
        """
        Deselect all options (only works for multi-select dropdowns).

        Args:
            element: Select WebElement

        Returns:
            True if deselection successful, False otherwise
        """
        try:
            if not element:
                return False
            select = Select(element)
            select.deselect_all()
            return True
        except Exception:
            return False
