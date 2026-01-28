"""
BasePage

Base class for all Page Objects in the automation framework.

This class provides:
- Safe wrappers around Selenium WebDriver calls
- Explicit wait handling via utilities
- Common page-level helper methods
- Browser-agnostic implementation
- Element interaction abstractions
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from utilities.wait_utils import WaitUtils
from utilities.element_utils import ElementUtils


class BasePage:
    """
    Base class for all Page Objects.

    Provides common functionality for element interactions, waiting,
    visibility checks, and navigation.

    Attributes:
        driver: The WebDriver instance (passed from test fixtures)
        wait_utils: WaitUtils instance for explicit waits
    """

    def __init__(self, driver: WebDriver):
        """
        Initialize BasePage with a WebDriver instance.

        Args:
            driver: An already-initialized WebDriver instance (ChromeDriver, FirefoxDriver, etc.)

        Example:
            driver = webdriver.Chrome()
            page = LoginPage(driver)
        """
        self.driver = driver
        self.wait_utils = WaitUtils(driver)
        self.element_utils = ElementUtils(driver)

    # ==================== Element Interaction Methods ====================

    def find(self, locator: tuple) -> WebElement:
        """
        Find and return a single element using explicit wait.

        Delegates waiting logic to wait_utils to ensure element is present
        before returning. Fails fast if element not found.

        Args:
            locator: Tuple of (By.*, selector) e.g., (By.ID, "element_id")

        Returns:
            WebElement: The found element

        Raises:
            TimeoutException: If element not found within wait timeout
            NoSuchElementException: If locator strategy is invalid

        Example:
            element = self.find((By.ID, "username"))
        """
        return self.wait_utils.wait_for_element_presence(locator)

    def find_all(self, locator: tuple) -> list:
        """
        Find and return multiple elements matching the locator.

        Args:
            locator: Tuple of (By.*, selector) e.g., (By.CLASS_NAME, "item")

        Returns:
            list: List of WebElement objects (empty list if no elements found)

        Example:
            items = self.find_all((By.CLASS_NAME, "product"))
        """
        try:
            self.wait_utils.wait_for_element_presence(locator)
            return self.driver.find_elements(*locator)
        except Exception:
            return []

    def click(self, locator: tuple) -> None:
        """
        Click on an element after ensuring it's visible and clickable.

        Uses explicit wait to ensure element is clickable before clicking.
        Uses ActionChains for safer clicking in edge cases.

        Args:
            locator: Tuple of (By.*, selector)

        Raises:
            TimeoutException: If element not clickable within timeout
            ElementNotInteractableException: If element cannot be clicked

        Example:
            self.click((By.ID, "submit_button"))
        """
        element = self.wait_utils.wait_for_element_clickable(locator)
        element.click()

    def double_click(self, locator: tuple) -> None:
        """
        Double-click on an element.

        Args:
            locator: Tuple of (By.*, selector)

        Example:
            self.double_click((By.ID, "element_id"))
        """
        element = self.wait_utils.wait_for_element_clickable(locator)
        ActionChains(self.driver).double_click(element).perform()

    def right_click(self, locator: tuple) -> None:
        """
        Right-click on an element.

        Args:
            locator: Tuple of (By.*, selector)

        Example:
            self.right_click((By.CLASS_NAME, "context_menu"))
        """
        element = self.wait_utils.wait_for_element_clickable(locator)
        ActionChains(self.driver).context_click(element).perform()

    def hover(self, locator: tuple) -> None:
        """
        Hover over an element.

        Useful for revealing hidden elements or tooltips.

        Args:
            locator: Tuple of (By.*, selector)

        Example:
            self.hover((By.ID, "dropdown"))
        """
        element = self.wait_utils.wait_for_element_presence(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    def type(self, locator: tuple, text: str, clear_first: bool = True) -> None:
        """
        Type text into an input field.

        Optionally clears the field before typing. Uses explicit wait to ensure
        element is present and ready for input.

        Args:
            locator: Tuple of (By.*, selector)
            text: Text to type
            clear_first: Whether to clear field before typing (default: True)

        Raises:
            TimeoutException: If element not found within timeout

        Example:
            self.type((By.ID, "username"), "john_doe")
            self.type((By.ID, "search"), "query", clear_first=False)
        """
        element = self.wait_utils.wait_for_element_presence(locator)
        if clear_first:
            element.clear()
        element.send_keys(text)

    def clear(self, locator: tuple) -> None:
        """
        Clear the value of an input field.

        Args:
            locator: Tuple of (By.*, selector)

        Example:
            self.clear((By.ID, "search_field"))
        """
        element = self.wait_utils.wait_for_element_presence(locator)
        element.clear()

    def type_slowly(self, locator: tuple, text: str, delay: float = 0.05) -> None:
        """
        Type text slowly into an input field with delay between characters.

        Useful for testing character-by-character input validation or autocomplete.

        Args:
            locator: Tuple of (By.*, selector)
            text: Text to type
            delay: Delay in seconds between each character (default: 0.05)

        Example:
            self.type_slowly((By.ID, "password"), "secretpass", delay=0.1)
        """
        element = self.wait_utils.wait_for_element_presence(locator)
        element.clear()
        for character in text:
            element.send_keys(character)
            self.driver.implicitly_wait(delay)

    def submit_form(self, locator: tuple) -> None:
        """
        Submit a form element.

        Args:
            locator: Tuple of (By.*, selector) pointing to a form element

        Example:
            self.submit_form((By.ID, "login_form"))
        """
        element = self.wait_utils.wait_for_element_presence(locator)
        element.submit()

    # ==================== State & Visibility Methods ====================

    def is_visible(self, locator: tuple, timeout: int = None) -> bool:
        """
        Check if an element is both present and visible.

        Combines presence check with visibility verification.

        Args:
            locator: Tuple of (By.*, selector)
            timeout: Optional timeout in seconds (uses default if not specified)

        Returns:
            bool: True if element is visible, False otherwise

        Example:
            if self.is_visible((By.ID, "message")):
                print(self.get_text((By.ID, "message")))
        """
        try:
            self.wait_utils.wait_for_element_visibility(locator, timeout=timeout)
            return True
        except Exception:
            return False

    def is_displayed(self, locator: tuple) -> bool:
        """
        Check if an element is displayed (CSS display property, not visibility).

        Immediately checks without waiting.

        Args:
            locator: Tuple of (By.*, selector)

        Returns:
            bool: True if element is displayed, False otherwise

        Example:
            is_modal_displayed = self.is_displayed((By.CLASS_NAME, "modal"))
        """
        try:
            element = self.driver.find_element(*locator)
            return element.is_displayed()
        except Exception:
            return False

    def is_enabled(self, locator: tuple) -> bool:
        """
        Check if an element is enabled.

        Useful for checking if buttons, inputs, or form elements are interactive.

        Args:
            locator: Tuple of (By.*, selector)

        Returns:
            bool: True if element is enabled, False otherwise

        Example:
            if self.is_enabled((By.ID, "submit_button")):
                self.click((By.ID, "submit_button"))
        """
        try:
            element = self.driver.find_element(*locator)
            return element.is_enabled()
        except Exception:
            return False

    def is_present(self, locator: tuple) -> bool:
        """
        Check if an element is present in the DOM (without visibility check).

        Args:
            locator: Tuple of (By.*, selector)

        Returns:
            bool: True if element is in DOM, False otherwise

        Example:
            if self.is_present((By.ID, "hidden_field")):
                text = self.get_text((By.ID, "hidden_field"))
        """
        try:
            self.driver.find_element(*locator)
            return True
        except Exception:
            return False

    def get_text(self, locator: tuple) -> str:
        """
        Get the visible text content of an element.

        Uses explicit wait to ensure element is present before retrieving text.

        Args:
            locator: Tuple of (By.*, selector)

        Returns:
            str: The text content (empty string if element not found)

        Example:
            error_message = self.get_text((By.CLASS_NAME, "error"))
        """
        try:
            element = self.find(locator)
            return element.text
        except Exception:
            return ""

    def get_attribute(self, locator: tuple, attribute: str) -> str:
        """
        Get an attribute value from an element.

        Args:
            locator: Tuple of (By.*, selector)
            attribute: Name of the attribute (e.g., "value", "href", "placeholder")

        Returns:
            str: The attribute value (empty string if not found)

        Example:
            href = self.get_attribute((By.ID, "link"), "href")
            value = self.get_attribute((By.ID, "input"), "value")
        """
        try:
            element = self.find(locator)
            return element.get_attribute(attribute) or ""
        except Exception:
            return ""

    def get_css_property(self, locator: tuple, css_property: str) -> str:
        """
        Get the computed CSS property value of an element.

        Args:
            locator: Tuple of (By.*, selector)
            css_property: CSS property name (e.g., "color", "background-color")

        Returns:
            str: The CSS property value

        Example:
            color = self.get_css_property((By.ID, "button"), "background-color")
        """
        try:
            element = self.find(locator)
            return element.value_of_css_property(css_property)
        except Exception:
            return ""

    def count_elements(self, locator: tuple) -> int:
        """
        Count the number of elements matching a locator.

        Args:
            locator: Tuple of (By.*, selector)

        Returns:
            int: Number of matching elements

        Example:
            product_count = self.count_elements((By.CLASS_NAME, "product"))
        """
        try:
            elements = self.driver.find_elements(*locator)
            return len(elements)
        except Exception:
            return 0

    # ==================== Navigation Methods ====================

    def get_current_url(self) -> str:
        """
        Get the current URL of the page.

        Returns:
            str: The current URL

        Example:
            current_url = self.get_current_url()
            assert "login" in current_url
        """
        return self.driver.current_url

    def refresh_page(self) -> None:
        """
        Refresh the current page.

        Useful for resetting state or testing page reload behavior.

        Example:
            self.refresh_page()
        """
        self.driver.refresh()

    def go_back(self) -> None:
        """
        Navigate back to the previous page (browser back button).

        Example:
            self.go_back()
        """
        self.driver.back()

    def go_forward(self) -> None:
        """
        Navigate forward to the next page (browser forward button).

        Example:
            self.go_forward()
        """
        self.driver.forward()

    def navigate_to(self, url: str) -> None:
        """
        Navigate to a specific URL.

        Args:
            url: The URL to navigate to

        Example:
            self.navigate_to("https://automationteststore.com")
        """
        self.driver.get(url)

    # ==================== Window & Alert Helpers ====================

    def get_page_title(self) -> str:
        """
        Get the title of the current page.

        Returns:
            str: The page title

        Example:
            title = self.get_page_title()
        """
        return self.driver.title

    def get_page_source(self) -> str:
        """
        Get the HTML source of the current page.

        Returns:
            str: The page HTML source

        Example:
            if "expected_text" in self.get_page_source():
                pass
        """
        return self.driver.page_source

    def switch_to_frame(self, locator: tuple) -> None:
        """
        Switch focus to an iframe element.

        Args:
            locator: Tuple of (By.*, selector) pointing to the iframe

        Example:
            self.switch_to_frame((By.ID, "payment_iframe"))
        """
        frame_element = self.find(locator)
        self.driver.switch_to.frame(frame_element)

    def switch_to_default_content(self) -> None:
        """
        Switch focus back to the main page content from an iframe.

        Example:
            self.switch_to_default_content()
        """
        self.driver.switch_to.default_content()

    def accept_alert(self) -> str:
        """
        Accept (click OK on) an alert dialog.

        Returns:
            str: The alert text before accepting

        Example:
            alert_text = self.accept_alert()
        """
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.accept()
        return alert_text

    def dismiss_alert(self) -> str:
        """
        Dismiss (click Cancel on) an alert dialog.

        Returns:
            str: The alert text before dismissing

        Example:
            alert_text = self.dismiss_alert()
        """
        alert = self.driver.switch_to.alert
        alert_text = alert.text
        alert.dismiss()
        return alert_text

    def type_alert(self, text: str) -> None:
        """
        Type text into a prompt alert dialog.

        Args:
            text: Text to type into the alert

        Example:
            self.type_alert("user_input")
        """
        alert = self.driver.switch_to.alert
        alert.send_keys(text)

    # ==================== Scroll Methods ====================

    def scroll_to_element(self, locator: tuple) -> None:
        """
        Scroll the page to bring an element into view.

        Useful when element is off-screen and needs to be visible for interaction.

        Args:
            locator: Tuple of (By.*, selector)

        Example:
            self.scroll_to_element((By.ID, "footer_link"))
        """
        element = self.find(locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_top(self) -> None:
        """
        Scroll the page to the top.

        Example:
            self.scroll_to_top()
        """
        self.driver.execute_script("window.scrollTo(0, 0);")

    def scroll_to_bottom(self) -> None:
        """
        Scroll the page to the bottom.

        Example:
            self.scroll_to_bottom()
        """
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_by_pixels(self, x: int, y: int) -> None:
        """
        Scroll the page by a specific number of pixels.

        Args:
            x: Pixels to scroll horizontally (positive = right)
            y: Pixels to scroll vertically (positive = down)

        Example:
            self.scroll_by_pixels(0, 500)  # Scroll down 500 pixels
        """
        self.driver.execute_script(f"window.scrollBy({x}, {y});")

    # ==================== Keyboard & Mouse Helpers ====================

    def press_key(self, locator: tuple, key: str) -> None:
        """
        Press a keyboard key on a focused element.

        Args:
            locator: Tuple of (By.*, selector)
            key: Key to press (e.g., Keys.ENTER, Keys.TAB, Keys.ESCAPE)

        Example:
            self.press_key((By.ID, "search"), Keys.ENTER)
        """
        element = self.find(locator)
        element.send_keys(key)

    def press_enter(self, locator: tuple) -> None:
        """
        Press Enter key on an element.

        Args:
            locator: Tuple of (By.*, selector)

        Example:
            self.press_enter((By.ID, "search_button"))
        """
        self.press_key(locator, Keys.ENTER)

    def press_escape(self, locator: tuple) -> None:
        """
        Press Escape key on an element.

        Args:
            locator: Tuple of (By.*, selector)

        Example:
            self.press_escape((By.ID, "modal"))
        """
        self.press_key(locator, Keys.ESCAPE)

    def press_tab(self, locator: tuple) -> None:
        """
        Press Tab key on an element.

        Args:
            locator: Tuple of (By.*, selector)

        Example:
            self.press_tab((By.ID, "field_1"))
        """
        self.press_key(locator, Keys.TAB)

    # ==================== Utility Methods ====================

    def wait_for(self, condition_callable, timeout: int = None) -> None:
        """
        Wait for a custom condition to be true.

        Delegates to wait_utils for flexible waiting with custom conditions.

        Args:
            condition_callable: A callable that returns True/False
            timeout: Optional timeout in seconds

        Example:
            self.wait_for(lambda: self.is_visible((By.ID, "modal")), timeout=5)
        """
        self.wait_utils.wait_for_condition(condition_callable, timeout=timeout)

    def execute_script(self, script: str, *args) -> any:
        """
        Execute JavaScript code in the context of the page.

        Args:
            script: JavaScript code to execute
            *args: Arguments to pass to the script (can use as arguments[0], arguments[1], etc.)

        Returns:
            The return value of the JavaScript code

        Example:
            result = self.execute_script("return document.title;")
            self.execute_script("arguments[0].style.display = 'none';", element)
        """
        return self.driver.execute_script(script, *args)

    def execute_async_script(self, script: str, *args) -> any:
        """
        Execute asynchronous JavaScript code.

        Useful for testing Ajax calls and async operations.

        Args:
            script: JavaScript code with callback at the end
            *args: Arguments to pass to the script

        Returns:
            The return value of the callback

        Example:
            self.execute_async_script("window.setTimeout(arguments[arguments.length - 1], 1000);")
        """
        return self.driver.execute_async_script(script, *args)

    def take_screenshot(self, filename: str) -> str:
        """
        Take a screenshot of the current page.

        Args:
            filename: Name of the screenshot file (with or without .png extension)

        Returns:
            str: The full path to the saved screenshot

        Example:
            screenshot_path = self.take_screenshot("login_page")
        """
        from utilities.screenshot_utils import ScreenshotUtils

        screenshot_utils = ScreenshotUtils(self.driver)
        return screenshot_utils.capture(filename)

    def get_element_size(self, locator: tuple) -> dict:
        """
        Get the size (width and height) of an element.

        Args:
            locator: Tuple of (By.*, selector)

        Returns:
            dict: Dictionary with 'width' and 'height' keys

        Example:
            size = self.get_element_size((By.ID, "button"))
            print(size['width'], size['height'])
        """
        try:
            element = self.find(locator)
            size = element.size
            return {"width": size["width"], "height": size["height"]}
        except Exception:
            return {"width": 0, "height": 0}

    def get_element_location(self, locator: tuple) -> dict:
        """
        Get the location (x, y coordinates) of an element.

        Args:
            locator: Tuple of (By.*, selector)

        Returns:
            dict: Dictionary with 'x' and 'y' keys

        Example:
            location = self.get_element_location((By.ID, "button"))
            print(location['x'], location['y'])
        """
        try:
            element = self.find(locator)
            location = element.location
            return {"x": location["x"], "y": location["y"]}
        except Exception:
            return {"x": 0, "y": 0}

    # ==================== Context Manager Support ====================

    def __enter__(self):
        """Support 'with' statement usage of BasePage."""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Cleanup when exiting 'with' block."""
        pass
