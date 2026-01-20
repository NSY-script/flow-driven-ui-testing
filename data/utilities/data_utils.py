"""
Data Utilities

Provides test-safe data generation helpers without external dependencies.
"""

import random
import string
from datetime import datetime
from typing import Optional


class DataUtils:
    """Utility class for generating test data."""

    @staticmethod
    def generate_random_email(prefix: str = "user") -> str:
        """
        Generate a random email address for testing.

        Args:
            prefix: Email prefix (default: "user")

        Returns:
            Random email address
        """
        try:
            random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            return f"{prefix}_{timestamp}_{random_suffix}@example.com"
        except Exception:
            return f"{prefix}@example.com"

    @staticmethod
    def generate_random_string(length: int = 8) -> str:
        """
        Generate a random alphanumeric string.

        Args:
            length: Length of the string (default: 8)

        Returns:
            Random string
        """
        try:
            if length < 1:
                length = 8
            return "".join(random.choices(string.ascii_letters + string.digits, k=length))
        except Exception:
            return "test"

    @staticmethod
    def generate_random_number(length: int = 4) -> str:
        """
        Generate a random numeric string.

        Args:
            length: Length of the number (default: 4)

        Returns:
            Random numeric string
        """
        try:
            if length < 1:
                length = 4
            return "".join(random.choices(string.digits, k=length))
        except Exception:
            return "0000"

    @staticmethod
    def generate_random_phone(format_str: str = "1234567890") -> str:
        """
        Generate a random phone number.

        Args:
            format_str: Example format (default: "1234567890")

        Returns:
            Random phone number based on format
        """
        try:
            if not format_str:
                format_str = "1234567890"
            return "".join(random.choices(string.digits, k=len(format_str)))
        except Exception:
            return "1234567890"

    @staticmethod
    def generate_random_name(length: int = 8) -> str:
        """
        Generate a random name (alphabetic characters only).

        Args:
            length: Length of the name (default: 8)

        Returns:
            Random name
        """
        try:
            if length < 1:
                length = 8
            return "".join(random.choices(string.ascii_letters, k=length))
        except Exception:
            return "testname"

    @staticmethod
    def generate_random_password(length: int = 12) -> str:
        """
        Generate a random strong password.

        Args:
            length: Length of the password (default: 12)

        Returns:
            Random password with mix of characters
        """
        try:
            if length < 8:
                length = 12
            chars = string.ascii_letters + string.digits + "!@#$%^&*()"
            password = "".join(random.choices(chars, k=length))
            return password
        except Exception:
            return "Password123!"

    @staticmethod
    def generate_timestamp() -> str:
        """
        Generate a timestamp string for unique identifiers.

        Args:
            None

        Returns:
            Timestamp in format YYYYMMDD_HHMMSS
        """
        return datetime.now().strftime("%Y%m%d_%H%M%S")

    @staticmethod
    def generate_unique_id(prefix: str = "id") -> str:
        """
        Generate a unique identifier with prefix and timestamp.

        Args:
            prefix: Prefix for the ID (default: "id")

        Returns:
            Unique identifier
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]
            random_suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=4))
            return f"{prefix}_{timestamp}_{random_suffix}"
        except Exception:
            return f"{prefix}_default"

    @staticmethod
    def generate_random_username(prefix: str = "user", length: int = 4) -> str:
        """
        Generate a random username.

        Args:
            prefix: Username prefix (default: "user")
            length: Length of random suffix (default: 4)

        Returns:
            Random username
        """
        try:
            random_suffix = "".join(random.choices(string.ascii_lowercase + string.digits, k=length))
            return f"{prefix}_{random_suffix}"
        except Exception:
            return f"{prefix}_test"

    @staticmethod
    def repeat_string(text: str, count: int) -> str:
        """
        Repeat a string multiple times.

        Args:
            text: Text to repeat
            count: Number of repetitions

        Returns:
            Repeated string
        """
        try:
            if count < 1:
                return text
            return text * count
        except Exception:
            return text
