"""
Explicit Wait Utilities

Provides centralized, reusable wait methods for reliable element interactions.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from typing import Tuple, Optional


class WaitUtils:
    """Utility class for explicit waits using WebDriverWait."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize WaitUtils with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default timeout in seconds (default: 10)
        """
        self.driver = driver
        self.timeout = timeout

    def wait_for_visibility(
        self, locator: Tuple[By, str], timeout: Optional[int] = None
    ) -> Optional[WebElement]:
        """
        Wait for an element to be visible on the page.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Maximum time to wait in seconds (uses default if None)

        Returns:
            WebElement if found and visible, None otherwise
        """
        try:
            timeout_val = timeout if timeout is not None else self.timeout
            element = WebDriverWait(self.driver, timeout_val).until(
                EC.visibility_of_element_located(locator)
            )
            return element
        except Exception:
            return None

    def wait_for_clickable(
        self, locator: Tuple[By, str], timeout: Optional[int] = None
    ) -> Optional[WebElement]:
        """
        Wait for an element to be visible and enabled (clickable).

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Maximum time to wait in seconds (uses default if None)

        Returns:
            WebElement if found and clickable, None otherwise
        """
        try:
            timeout_val = timeout if timeout is not None else self.timeout
            element = WebDriverWait(self.driver, timeout_val).until(
                EC.element_to_be_clickable(locator)
            )
            return element
        except Exception:
            return None

    def wait_for_presence(
        self, locator: Tuple[By, str], timeout: Optional[int] = None
    ) -> Optional[WebElement]:
        """
        Wait for an element to be present in the DOM (not necessarily visible).

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Maximum time to wait in seconds (uses default if None)

        Returns:
            WebElement if found in DOM, None otherwise
        """
        try:
            timeout_val = timeout if timeout is not None else self.timeout
            element = WebDriverWait(self.driver, timeout_val).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except Exception:
            return None

    def wait_for_invisibility(
        self, locator: Tuple[By, str], timeout: Optional[int] = None
    ) -> bool:
        """
        Wait for an element to become invisible or disappear from the DOM.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Maximum time to wait in seconds (uses default if None)

        Returns:
            True if element becomes invisible, False otherwise
        """
        try:
            timeout_val = timeout if timeout is not None else self.timeout
            WebDriverWait(self.driver, timeout_val).until(
                EC.invisibility_of_element_located(locator)
            )
            return True
        except Exception:
            return False

    def wait_for_element(
        self, locator: Tuple[By, str], timeout: Optional[int] = None
    ) -> Optional[WebElement]:
        """
        Alias for wait_for_presence - wait for element presence in DOM.

        Args:
            locator: Tuple of (By, locator_string)
            timeout: Maximum time to wait in seconds (uses default if None)

        Returns:
            WebElement if found, None otherwise
        """
        return self.wait_for_presence(locator, timeout)
