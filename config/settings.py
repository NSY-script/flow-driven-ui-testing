"""
Project-level settings and configuration.

Centralizes all project constants, environment variables, paths, and defaults.
Supports multiple environments (dev, staging, prod) and CI/CD pipelines.
"""

import os
from pathlib import Path

# ==================== Project Structure ====================
PROJECT_ROOT = Path(__file__).parent.parent
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
TESTS_DIR = PROJECT_ROOT / "tests"
PAGES_DIR = PROJECT_ROOT / "pages"
FLOWS_DIR = PROJECT_ROOT / "flows"
UTILITIES_DIR = PROJECT_ROOT / "utilities"
REPORTS_DIR = PROJECT_ROOT / "reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"
LOGS_DIR = REPORTS_DIR / "logs"
HTML_REPORTS_DIR = REPORTS_DIR / "html"
ALLURE_RESULTS_DIR = REPORTS_DIR / "allure-results"
JUNIT_REPORTS_DIR = REPORTS_DIR / "junit"

# ==================== Environment Configuration ====================
# Get environment from environment variable or default to 'dev'
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev").lower()

# Environment-specific configurations
ENVIRONMENTS = {
    "dev": {
        "base_url": "https://automationteststore.com",
        "headless": False,
        "log_level": "DEBUG",
    },
    "staging": {
        "base_url": "https://staging.automationteststore.com",
        "headless": True,
        "log_level": "INFO",
    },
    "prod": {
        "base_url": "https://automationteststore.com",
        "headless": True,
        "log_level": "INFO",
    },
}

# Get environment config (fallback to dev if invalid environment specified)
ENV_CONFIG = ENVIRONMENTS.get(ENVIRONMENT, ENVIRONMENTS["dev"])

# ==================== Application URLs ====================
BASE_URL = ENV_CONFIG.get("base_url", "https://automationteststore.com")
LOGIN_PAGE_URL = f"{BASE_URL}/index.php?rt=account/login"
REGISTER_PAGE_URL = f"{BASE_URL}/index.php?rt=account/create"
SEARCH_PAGE_URL = f"{BASE_URL}/index.php?rt=product/search"
ACCOUNT_PAGE_URL = f"{BASE_URL}/index.php?rt=account/account"
CART_PAGE_URL = f"{BASE_URL}/index.php?rt=checkout/cart"
CHECKOUT_PAGE_URL = f"{BASE_URL}/index.php?rt=checkout/checkout"
ORDERS_PAGE_URL = f"{BASE_URL}/index.php?rt=account/order"
DOWNLOADS_PAGE_URL = f"{BASE_URL}/index.php?rt=account/download"
WISHLIST_PAGE_URL = f"{BASE_URL}/index.php?rt=account/wishlist"

# ==================== Wait and Timeout Configuration ====================
# Explicit wait times (seconds)
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 15))
IMPLICIT_WAIT = int(os.getenv("IMPLICIT_WAIT", 10))
PAGE_LOAD_TIMEOUT = int(os.getenv("PAGE_LOAD_TIMEOUT", 30))
ELEMENT_VISIBILITY_TIMEOUT = int(os.getenv("ELEMENT_VISIBILITY_TIMEOUT", 15))
ELEMENT_CLICKABLE_TIMEOUT = int(os.getenv("ELEMENT_CLICKABLE_TIMEOUT", 15))
POLLING_FREQUENCY = 0.5  # How often to check condition in WebDriverWait

# ==================== Browser Configuration ====================
BROWSER = os.getenv("BROWSER", "chrome").lower()
HEADLESS = os.getenv("HEADLESS", str(ENV_CONFIG.get("headless", False))).lower() == "true"
WINDOW_SIZE = (1920, 1080)  # Width x Height
ACCEPT_INSECURE_CERTS = True
START_MAXIMIZED = True

# Browser-specific options
BROWSER_OPTIONS = {
    "chrome": {
        "disable-blink-features": "AutomationControlled",
        "disable-extensions": None,
        "disable-plugins": None,
        "no-default-browser-check": None,
        "no-first-run": None,
        "disable-default-apps": None,
        "disable-popup-blocking": None,
    },
    "firefox": {
        "profile": None,  # Can be customized
    },
    "edge": {
        "disable-blink-features": "AutomationControlled",
    },
}

# ==================== Screenshot Configuration ====================
CAPTURE_SCREENSHOT_ON_FAILURE = True
CAPTURE_SCREENSHOT_ON_SUCCESS = False
SCREENSHOT_FORMAT = "png"  # png or jpg
SCREENSHOT_QUALITY = 95  # Only for jpg format

# ==================== Reporting Configuration ====================
ALLURE_REPORT_ENABLED = True
HTML_REPORT_ENABLED = True
JUNIT_REPORT_ENABLED = True

# Allure report settings
ALLURE_ENVIRONMENT_PROPERTIES = {
    "Environment": ENVIRONMENT,
    "Browser": BROWSER,
    "Base URL": BASE_URL,
    "Platform": os.getenv("PLATFORM", "Linux/macOS/Windows"),
}

# ==================== Logging Configuration ====================
LOG_LEVEL = os.getenv("LOG_LEVEL", ENV_CONFIG.get("log_level", "DEBUG"))
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

# ==================== Test Data Configuration ====================
# Paths to test data files
USERS_DATA_FILE = DATA_DIR / "users.json"
PRODUCTS_DATA_FILE = DATA_DIR / "products.json"
CART_DATA_FILE = DATA_DIR / "cart.json"
CHECKOUT_DATA_FILE = DATA_DIR / "checkout.json"
WISHLIST_DATA_FILE = DATA_DIR / "wishlist.json"
SEARCH_DATA_FILE = DATA_DIR / "search.json"
ACCOUNT_DATA_FILE = DATA_DIR / "account.json"
ORDERS_DATA_FILE = DATA_DIR / "orders.json"

# ==================== Retry Configuration ====================
MAX_RETRIES = int(os.getenv("MAX_RETRIES", 3))
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 1))  # seconds

# ==================== Feature Flags ====================
# Use these to enable/disable features for testing different scenarios
FEATURE_FLAGS = {
    "use_page_object_model": True,
    "capture_screenshots": CAPTURE_SCREENSHOT_ON_FAILURE,
    "enable_logging": True,
    "enable_allure_reporting": ALLURE_REPORT_ENABLED,
    "enable_html_reporting": HTML_REPORT_ENABLED,
    "run_headless": HEADLESS,
}

# ==================== Data Validation ====================
# These can be used for test data validation
VALID_EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
MIN_PASSWORD_LENGTH = 6
MAX_PASSWORD_LENGTH = 32

# ==================== CI/CD Detection ====================
# Detect if running in CI/CD environment
IS_CI_ENV = any(
    os.getenv(var)
    for var in [
        "CI",
        "CONTINUOUS_INTEGRATION",
        "GITHUB_ACTIONS",
        "GITLAB_CI",
        "JENKINS_HOME",
        "TRAVIS",
        "CIRCLECI",
    ]
)

# ==================== Helper Methods ====================


def get_data_file_path(filename: str) -> Path:
    """
    Get the full path to a data file.

    Args:
        filename: Name of the data file (e.g., 'users.json')

    Returns:
        Path: Full path to the data file
    """
    return DATA_DIR / filename


def get_report_file_path(filename: str, report_type: str = "html") -> Path:
    """
    Get the full path to a report file.

    Args:
        filename: Name of the report file
        report_type: Type of report (html, allure, junit)

    Returns:
        Path: Full path to the report file
    """
    if report_type == "html":
        return HTML_REPORTS_DIR / filename
    elif report_type == "allure":
        return ALLURE_RESULTS_DIR / filename
    elif report_type == "junit":
        return JUNIT_REPORTS_DIR / filename
    else:
        return REPORTS_DIR / filename


def get_screenshot_path(test_name: str) -> Path:
    """
    Get the screenshot path for a test.

    Args:
        test_name: Name of the test

    Returns:
        Path: Full path where screenshot should be saved
    """
    from datetime import datetime
    
    filename = f"{test_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{SCREENSHOT_FORMAT}"
    return SCREENSHOTS_DIR / filename


def is_headless_mode() -> bool:
    """Check if running in headless mode."""
    return HEADLESS or IS_CI_ENV


def is_local_environment() -> bool:
    """Check if running in local development environment."""
    return ENVIRONMENT == "dev" and not IS_CI_ENV


# ==================== Debug Configuration ====================
DEBUG_MODE = os.getenv("DEBUG_MODE", "False").lower() == "true"
VERBOSE_OUTPUT = os.getenv("VERBOSE_OUTPUT", "False").lower() == "true"

# ==================== API Configuration (if needed for future) ====================
API_BASE_URL = os.getenv("API_BASE_URL", BASE_URL + "/api")
API_TIMEOUT = int(os.getenv("API_TIMEOUT", 30))

# ==================== Summary ====================
CONFIG_SUMMARY = f"""
================== PROJECT CONFIGURATION ==================
Environment:        {ENVIRONMENT.upper()}
Base URL:           {BASE_URL}
Browser:            {BROWSER}
Headless:           {HEADLESS}
Default Timeout:    {DEFAULT_TIMEOUT}s
CI/CD:              {IS_CI_ENV}
Data Dir:           {DATA_DIR}
Reports Dir:        {REPORTS_DIR}
=========================================================
"""

# Uncomment to print config on import (useful for debugging)
# print(CONFIG_SUMMARY)
