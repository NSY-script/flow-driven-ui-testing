"""
Session Utilities

Provides session-level utilities for cookie management and page navigation.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from typing import List, Dict, Optional


class SessionUtils:
    """Utility class for session and cookie management."""

    def __init__(self, driver: WebDriver):
        """
        Initialize SessionUtils with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
        """
        self.driver = driver

    def get_all_cookies(self) -> List[Dict]:
        """
        Get all cookies from the current session.

        Args:
            None

        Returns:
            List of cookie dictionaries, empty list if error
        """
        try:
            return self.driver.get_cookies()
        except Exception:
            return []

    def get_cookie(self, name: str) -> Optional[Dict]:
        """
        Get a specific cookie by name.

        Args:
            name: Cookie name

        Returns:
            Cookie dictionary if found, None otherwise
        """
        try:
            return self.driver.get_cookie(name)
        except Exception:
            return None

    def delete_all_cookies(self) -> bool:
        """
        Delete all cookies from the current session.

        Args:
            None

        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.delete_all_cookies()
            return True
        except Exception:
            return False

    def delete_cookie(self, name: str) -> bool:
        """
        Delete a specific cookie by name.

        Args:
            name: Cookie name

        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.delete_cookie(name)
            return True
        except Exception:
            return False

    def refresh_page(self) -> bool:
        """
        Refresh the current page (F5).

        Args:
            None

        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.refresh()
            return True
        except Exception:
            return False

    def navigate_back(self) -> bool:
        """
        Navigate back to the previous page.

        Args:
            None

        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.back()
            return True
        except Exception:
            return False

    def navigate_forward(self) -> bool:
        """
        Navigate forward to the next page.

        Args:
            None

        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.forward()
            return True
        except Exception:
            return False

    def get_current_url(self) -> str:
        """
        Get the current page URL.

        Args:
            None

        Returns:
            Current URL, or empty string if error
        """
        try:
            return self.driver.current_url
        except Exception:
            return ""

    def get_page_title(self) -> str:
        """
        Get the current page title.

        Args:
            None

        Returns:
            Page title, or empty string if error
        """
        try:
            return self.driver.title
        except Exception:
            return ""

    def get_page_source(self) -> str:
        """
        Get the HTML source of the current page.

        Args:
            None

        Returns:
            Page source HTML, or empty string if error
        """
        try:
            return self.driver.page_source
        except Exception:
            return ""

    def maximize_window(self) -> bool:
        """
        Maximize the browser window.

        Args:
            None

        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.maximize_window()
            return True
        except Exception:
            return False

    def minimize_window(self) -> bool:
        """
        Minimize the browser window.

        Args:
            None

        Returns:
            True if successful, False otherwise
        """
        try:
            self.driver.minimize_window()
            return True
        except Exception:
            return False
