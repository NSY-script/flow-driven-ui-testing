"""
Screenshot Utilities

Provides screenshot capture functionality for reporting and debugging.
"""

import os
from datetime import datetime
from selenium.webdriver.remote.webdriver import WebDriver
from typing import Optional


class ScreenshotUtils:
    """Utility class for capturing screenshots."""

    def __init__(self, driver: WebDriver, folder: str = "screenshots"):
        """
        Initialize ScreenshotUtils with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
            folder: Folder path to save screenshots (default: "screenshots")
        """
        self.driver = driver
        self.folder = folder
        self._ensure_folder_exists()

    def _ensure_folder_exists(self) -> None:
        """Create screenshot folder if it doesn't exist."""
        try:
            if not os.path.exists(self.folder):
                os.makedirs(self.folder, exist_ok=True)
        except Exception:
            pass

    def capture(self, name: str, folder: Optional[str] = None) -> Optional[str]:
        """
        Capture a screenshot and save it to disk.

        Args:
            name: Screenshot file name (without extension)
            folder: Override default folder path (optional)

        Returns:
            Full file path if successful, None otherwise
        """
        try:
            target_folder = folder if folder else self.folder
            self._ensure_folder_exists() if not folder else os.makedirs(
                target_folder, exist_ok=True
            )

            # Generate unique filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(target_folder, filename)

            # Capture screenshot
            self.driver.save_screenshot(filepath)
            return filepath
        except Exception:
            return None

    def capture_with_timestamp(self, name: str) -> Optional[str]:
        """
        Capture screenshot with automatic timestamp in filename.

        Args:
            name: Base name for the screenshot

        Returns:
            Full file path if successful, None otherwise
        """
        return self.capture(name)

    def capture_full_page(self, name: str) -> Optional[str]:
        """
        Capture full page screenshot (standard screenshot).

        Args:
            name: Screenshot file name (without extension)

        Returns:
            Full file path if successful, None otherwise
        """
        return self.capture(name)

    def capture_element(
        self, element, name: str, folder: Optional[str] = None
    ) -> Optional[str]:
        """
        Capture screenshot of a specific element.

        Args:
            element: WebElement to capture
            name: Screenshot file name (without extension)
            folder: Override default folder path (optional)

        Returns:
            Full file path if successful, None otherwise
        """
        try:
            if not element:
                return None

            target_folder = folder if folder else self.folder
            os.makedirs(target_folder, exist_ok=True)

            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{name}_{timestamp}.png"
            filepath = os.path.join(target_folder, filename)

            element.screenshot(filepath)
            return filepath
        except Exception:
            return None

    @staticmethod
    def create_folder_if_not_exists(folder: str) -> bool:
        """
        Create a folder if it doesn't exist.

        Args:
            folder: Folder path to create

        Returns:
            True if folder created or already exists, False otherwise
        """
        try:
            os.makedirs(folder, exist_ok=True)
            return True
        except Exception:
            return False
