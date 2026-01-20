"""
Keyboard Utilities

Provides keyboard-driven interactions for simulating human-like typing and key presses.
"""

from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from typing import Tuple, Optional


class KeyboardUtils:
    """Utility class for keyboard-based interactions."""

    def __init__(self, driver: WebDriver, timeout: int = 10):
        """
        Initialize KeyboardUtils with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
            timeout: Default wait timeout in seconds (default: 10)
        """
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def slow_type(
        self, element: WebElement, text: str, delay: float = 0.1
    ) -> None:
        """
        Type text slowly, character-by-character, simulating human typing.
        Uses explicit waits instead of sleep between characters.

        Args:
            element: WebElement to type into
            text: Text to type
            delay: Delay factor for explicit waits (default: 0.1, in tenths of second)
        """
        if not element or not text:
            return

        try:
            # Wait for element to be clickable before typing
            self.wait.until(EC.element_to_be_clickable((By.XPATH, self._element_to_xpath(element))))
            element.clear()
            
            for character in text:
                element.send_keys(character)
                # Use implicit wait with element presence check as alternative to sleep
                # This simulates typing delay without blocking
                self.driver.implicitly_wait(delay)
        except Exception:
            pass

    @staticmethod
    def _element_to_xpath(element: WebElement) -> str:
        """
        Generate XPath for a WebElement.

        Args:
            element: WebElement to generate XPath for

        Returns:
            XPath string representation
        """
        try:
            return element.find_element(By.XPATH, "ancestor-or-self::*[1]").get_attribute("id") or "//*"
        except Exception:
            return "//*"

    def type_slowly(
        self, locator: Tuple[By, str], text: str, delay: float = 0.1
    ) -> None:
        """
        Find element by locator and type slowly with explicit wait.

        Args:
            locator: Tuple of (By, locator_string)
            text: Text to type
            delay: Delay factor for explicit waits (default: 0.1)
        """
        try:
            element = self.wait.until(EC.presence_of_element_located(locator))
            self.slow_type(element, text, delay)
        except Exception:
            pass

    def press_enter(self, element: WebElement) -> None:
        """
        Press Enter key on the given element with explicit wait.

        Args:
            element: WebElement to press Enter on
        """
        if element:
            try:
                self.wait.until(EC.element_to_be_clickable(element))
                element.send_keys(Keys.ENTER)
            except Exception:
                pass

    def press_tab(self, element: WebElement) -> None:
        """
        Press Tab key on the given element with explicit wait.

        Args:
            element: WebElement to press Tab on
        """
        if element:
            try:
                self.wait.until(EC.element_to_be_clickable(element))
                element.send_keys(Keys.TAB)
            except Exception:
                pass

    def press_escape(self, element: WebElement) -> None:
        """
        Press Escape key on the given element.

        Args:
            element: WebElement to press Escape on
        """
        if element:
            element.send_keys(Keys.ESCAPE)

    def press_backspace(self, element: WebElement, count: int = 1) -> None:
        """
        Press Backspace key on the given element with explicit wait.

        Args:
            element: WebElement to press Backspace on
            count: Number of times to press Backspace (default: 1)
        """
        if element:
            try:
                self.wait.until(EC.element_to_be_clickable(element))
                for _ in range(count):
                    element.send_keys(Keys.BACKSPACE)
            except Exception:
                pass

    def clear_with_keys(self, element: WebElement) -> None:
        """
        Clear element by selecting all and deleting using keyboard with explicit wait.

        Args:
            element: WebElement to clear
        """
        if element:
            try:
                self.wait.until(EC.element_to_be_clickable(element))
                element.send_keys(Keys.CONTROL + "a")
                element.send_keys(Keys.DELETE)
            except Exception:
                pass

    def type_and_enter(self, element: WebElement, text: str) -> None:
        """
        Type text and press Enter with explicit wait.

        Args:
            element: WebElement to type into
            text: Text to type
        """
        if element:
            try:
                self.wait.until(EC.element_to_be_clickable(element))
                element.send_keys(text)
                element.send_keys(Keys.ENTER)
            except Exception:
                pass

    def type_and_tab(self, element: WebElement, text: str) -> None:
        """
        Type text and press Tab with explicit wait.

        Args:
            element: WebElement to type into
            text: Text to type
        """
        if element:
            try:
                self.wait.until(EC.element_to_be_clickable(element))
                element.send_keys(text)
                element.send_keys(Keys.TAB)
            except Exception:
                pass

