"""
Element Utilities

Provides safe, generic element interaction methods for common UI actions.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.by import By
from typing import Tuple, Optional


class ElementUtils:
    """Utility class for safe element interactions."""

    def __init__(self, driver: WebDriver):
        """
        Initialize ElementUtils with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver

    def find_element(self, locator: Tuple[By, str]) -> Optional[WebElement]:
        """
        Find a single element by locator.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            WebElement if found, None otherwise
        """
        try:
            return self.driver.find_element(*locator)
        except Exception:
            return None

    def click(self, locator: Tuple[By, str]) -> bool:
        """
        Find element by locator and click it.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            True if click successful, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            if element:
                element.click()
                return True
            return False
        except Exception:
            return False

    def type_text(self, locator: Tuple[By, str], text: str) -> bool:
        """
        Find element by locator and type text into it.

        Args:
            locator: Tuple of (By, locator_string)
            text: Text to type

        Returns:
            True if typing successful, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            if element:
                element.clear()
                element.send_keys(text)
                return True
            return False
        except Exception:
            return False

    def get_text(self, locator: Tuple[By, str]) -> str:
        """
        Find element by locator and get its text.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            Element text, or empty string if not found
        """
        try:
            element = self.driver.find_element(*locator)
            return element.text if element else ""
        except Exception:
            return ""

    def is_displayed(self, locator: Tuple[By, str]) -> bool:
        """
        Check if element is displayed/visible.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            True if element is displayed, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed() if element else False
        except Exception:
            return False

    def is_enabled(self, locator: Tuple[By, str]) -> bool:
        """
        Check if element is enabled.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            True if element is enabled, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            return element.is_enabled() if element else False
        except Exception:
            return False

    def get_attribute(self, locator: Tuple[By, str], attribute: str) -> str:
        """
        Get attribute value of element.

        Args:
            locator: Tuple of (By, locator_string)
            attribute: Attribute name

        Returns:
            Attribute value, or empty string if not found
        """
        try:
            element = self.driver.find_element(*locator)
            return element.get_attribute(attribute) if element else ""
        except Exception:
            return ""

    def clear_field(self, locator: Tuple[By, str]) -> bool:
        """
        Clear an input field.

        Args:
            locator: Tuple of (By, locator_string)

        Returns:
            True if clear successful, False otherwise
        """
        try:
            element = self.driver.find_element(*locator)
            if element:
                element.clear()
                return True
            return False
        except Exception:
            return False
