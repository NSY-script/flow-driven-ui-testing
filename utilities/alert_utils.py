"""
Alert Utilities

Provides browser alert and confirmation dialog handling.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    NoAlertPresentException,
    TimeoutException,
)
from typing import Optional


class AlertUtils:
    """Utility class for handling browser alerts and dialogs."""

    def __init__(self, driver: WebDriver, timeout: int = 5):
        """
        Initialize AlertUtils with WebDriver instance.

        Args:
            driver: Selenium WebDriver instance
            timeout: Timeout for alert wait in seconds (default: 5)
        """
        self.driver = driver
        self.timeout = timeout

    def wait_for_alert(self, timeout: Optional[int] = None) -> bool:
        """
        Wait for an alert to appear.

        Args:
            timeout: Maximum time to wait in seconds (uses default if None)

        Returns:
            True if alert appears, False otherwise
        """
        try:
            timeout_val = timeout if timeout is not None else self.timeout
            WebDriverWait(self.driver, timeout_val).until(EC.alert_is_present())
            return True
        except TimeoutException:
            return False
        except Exception:
            return False

    def get_alert_text(self) -> str:
        """
        Get the text content of the current alert.

        Args:
            None

        Returns:
            Alert text, or empty string if no alert present
        """
        try:
            alert = self.driver.switch_to.alert
            return alert.text if alert else ""
        except NoAlertPresentException:
            return ""
        except Exception:
            return ""

    def accept_alert(self) -> bool:
        """
        Accept (click OK) the current alert.

        Args:
            None

        Returns:
            True if alert accepted, False otherwise
        """
        try:
            alert = self.driver.switch_to.alert
            alert.accept()
            return True
        except NoAlertPresentException:
            return False
        except Exception:
            return False

    def dismiss_alert(self) -> bool:
        """
        Dismiss (click Cancel) the current alert.

        Args:
            None

        Returns:
            True if alert dismissed, False otherwise
        """
        try:
            alert = self.driver.switch_to.alert
            alert.dismiss()
            return True
        except NoAlertPresentException:
            return False
        except Exception:
            return False

    def type_in_alert(self, text: str) -> bool:
        """
        Type text in a prompt alert.

        Args:
            text: Text to type in the alert input

        Returns:
            True if text typed successfully, False otherwise
        """
        try:
            alert = self.driver.switch_to.alert
            alert.send_keys(text)
            return True
        except NoAlertPresentException:
            return False
        except Exception:
            return False

    def accept_alert_with_text(self, text: str) -> bool:
        """
        Type text in a prompt alert and accept it.

        Args:
            text: Text to type in the alert input

        Returns:
            True if action successful, False otherwise
        """
        try:
            alert = self.driver.switch_to.alert
            alert.send_keys(text)
            alert.accept()
            return True
        except NoAlertPresentException:
            return False
        except Exception:
            return False

    def is_alert_present(self) -> bool:
        """
        Check if an alert is currently present.

        Args:
            None

        Returns:
            True if alert is present, False otherwise
        """
        try:
            self.driver.switch_to.alert
            return True
        except NoAlertPresentException:
            return False
        except Exception:
            return False
