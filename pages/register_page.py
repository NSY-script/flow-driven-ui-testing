"""
Register Page Object Model

Contains locators and atomic UI actions for the registration form.
"""

from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from base.base_page import BasePage
from utilities.dropdown_utils import DropdownUtils


class RegisterPage(BasePage):
    """Page Object for user registration."""

    def __init__(self, driver: WebDriver):
        """Initialize RegisterPage with WebDriver instance."""
        super().__init__(driver)
        self.dropdown_utils = DropdownUtils()

    # Locators - Using stable XPath with normalize-space() for text matching
    LOGIN_REGISTER_LINK = (By.XPATH, "//a[normalize-space()='Login or register']")
    # Locators - Using stable XPath with id attributes for reliability
    LOGIN_REGISTER_LINK = (By.XPATH, "//a[normalize-space()='Login or register']")
    FIRSTNAME_INPUT = (By.XPATH, "//input[@id='AccountFrm_firstname']")
    LASTNAME_INPUT = (By.XPATH, "//input[@id='AccountFrm_lastname']")
    EMAIL_INPUT = (By.XPATH, "//input[@id='AccountFrm_email']")
    TELEPHONE_INPUT = (By.XPATH, "//input[@id='AccountFrm_telephone']")
    FAX_INPUT = (By.XPATH, "//input[@id='AccountFrm_fax']")
    COMPANY_INPUT = (By.XPATH, "//input[@id='AccountFrm_company']")
    ADDRESS_INPUT = (By.XPATH, "//input[@id='AccountFrm_address_1']")
    CITY_INPUT = (By.XPATH, "//input[@id='AccountFrm_city']")
    ZONE_DROPDOWN = (By.XPATH, "//select[@id='AccountFrm_zone_id']")
    POSTCODE_INPUT = (By.XPATH, "//input[@id='AccountFrm_postcode']")
    COUNTRY_DROPDOWN = (By.XPATH, "//select[@id='AccountFrm_country_id']")
    LOGINNAME_INPUT = (By.XPATH, "//input[@id='AccountFrm_loginname']")
    PASSWORD_INPUT = (By.XPATH, "//input[@id='AccountFrm_password']")
    CONFIRM_PASSWORD_INPUT = (By.XPATH, "//input[@id='AccountFrm_confirm']")
    NEWSLETTER_YES_RADIO = (By.XPATH, "//input[@id='AccountFrm_newsletter1']")
    NEWSLETTER_NO_RADIO = (By.XPATH, "//input[@id='AccountFrm_newsletter0']")
    TERMS_CHECKBOX = (By.XPATH, "//input[@id='AccountFrm_agree']")
    CONTINUE_BUTTON = (By.XPATH, "//button[normalize-space()='Continue']")
    # Success message locators - check multiple possible variations after registration
    SUCCESS_MESSAGE_CONTAINER = (By.XPATH, "//*[contains(text(), 'Your Account') or contains(text(), 'Thank you') or contains(text(), 'Success')]")
    ERROR_MESSAGE_CONTAINER = (By.XPATH, "//div[@class='error']")
    SUCCESS_PAGE_CONTINUE_BUTTON = (By.XPATH, "//a[normalize-space()='Continue']")

    def click_login_register_link(self) -> None:
        """Click the Login/Register entry link."""
        self.element_utils.click(self.LOGIN_REGISTER_LINK)
    
    def navigate_to_register_page(self) -> None:
        """Navigate directly to registration page via URL."""
        # Get the current base URL and navigate to register page
        base_url = self.driver.current_url.split('/index.php')[0]
        register_url = f"{base_url}/index.php?rt=account/create"
        self.driver.get(register_url)
        # Wait for the form to load
        self.wait_utils.wait_for_element(self.FIRSTNAME_INPUT, timeout=10)

    def enter_firstname(self, firstname: str) -> None:
        """Enter first name."""
        self.element_utils.type_text(self.FIRSTNAME_INPUT, firstname)

    def enter_lastname(self, lastname: str) -> None:
        """Enter last name."""
        self.element_utils.type_text(self.LASTNAME_INPUT, lastname)

    def enter_email(self, email: str) -> None:
        """Enter email address."""
        self.element_utils.type_text(self.EMAIL_INPUT, email)

    def enter_address(self, address: str) -> None:
        """Enter street address."""
        self.element_utils.type_text(self.ADDRESS_INPUT, address)

    def enter_city(self, city: str) -> None:
        """Enter city name."""
        self.element_utils.type_text(self.CITY_INPUT, city)

    def select_zone(self, zone_id: str) -> None:
        """Select state/province from dropdown using Selenium Select class."""
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        import time
        
        # Wait for dropdown to be present and clickable
        dropdown_element = self.wait_utils.wait_for_element(self.ZONE_DROPDOWN, timeout=5)
        
        # Add a small delay to ensure dropdown options are fully loaded
        time.sleep(0.3)
        
        # Wait for dropdown to be clickable with a longer timeout
        WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable(self.ZONE_DROPDOWN))
        
        # Refresh the element reference after wait
        dropdown_element = self.driver.find_element(*self.ZONE_DROPDOWN)
        
        # Create Select object and select by visible text
        select = Select(dropdown_element)
        
        # Print all available options for debugging
        all_options = select.options
        print(f"DEBUG: Found {len(all_options)} zone options")
        
        try:
            select.select_by_visible_text(zone_id)
            print(f"DEBUG: Successfully selected zone: {zone_id}")
        except Exception as e:
            print(f"DEBUG: Error selecting zone {zone_id}: {str(e)}")
            print(f"DEBUG: Attempting to find and click {zone_id} manually...")
            # Try to find and click manually
            found = False
            for option in all_options:
                if option.text.strip() == zone_id:
                    option.click()
                    found = True
                    print(f"DEBUG: Successfully clicked zone option: {zone_id}")
                    break
            if not found:
                print(f"DEBUG: Available zone options:")
                for opt in all_options:
                    print(f"  Value: '{opt.get_attribute('value')}' | Text: '{opt.text.strip()}'")
                raise Exception(f"Zone '{zone_id}' not found in dropdown")

    def enter_postcode(self, postcode: str) -> None:
        """Enter postal code."""
        self.element_utils.type_text(self.POSTCODE_INPUT, postcode)

    def select_country(self, country_id: str) -> None:
        """Select country from dropdown using Selenium Select class."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Wait for dropdown to be present and clickable
        dropdown_element = self.wait_utils.wait_for_element(self.COUNTRY_DROPDOWN)
        WebDriverWait(self.driver, 0.5).until(EC.element_to_be_clickable(self.COUNTRY_DROPDOWN))
        
        # Create Select object and select by visible text
        select = Select(dropdown_element)
        try:
            select.select_by_visible_text(country_id)
            print(f"DEBUG: Successfully selected country: {country_id}")
        except Exception as e:
            print(f"DEBUG: Error selecting country {country_id}: {str(e)}")
            raise

    def enter_loginname(self, loginname: str) -> None:
        """Enter login name/username."""
        self.element_utils.type_text(self.LOGINNAME_INPUT, loginname)

    def enter_telephone(self, telephone: str) -> None:
        """Enter telephone number."""
        self.element_utils.type_text(self.TELEPHONE_INPUT, telephone)

    def enter_fax(self, fax: str) -> None:
        """Enter fax number."""
        self.element_utils.type_text(self.FAX_INPUT, fax)

    def enter_company(self, company: str) -> None:
        """Enter company name."""
        self.element_utils.type_text(self.COMPANY_INPUT, company)

    def enter_password(self, password: str) -> None:
        """Enter password."""
        self.element_utils.type_text(self.PASSWORD_INPUT, password)

    def enter_confirm_password(self, password: str) -> None:
        """Enter password confirmation."""
        self.element_utils.type_text(self.CONFIRM_PASSWORD_INPUT, password)

    def select_newsletter_yes(self) -> None:
        """Select Yes for newsletter subscription."""
        self.element_utils.click(self.NEWSLETTER_YES_RADIO)

    def select_newsletter_no(self) -> None:
        """Select No for newsletter subscription."""
        self.element_utils.click(self.NEWSLETTER_NO_RADIO)

    def check_terms_and_conditions(self) -> None:
        """Check the Terms & Conditions checkbox."""
        self.element_utils.click(self.TERMS_CHECKBOX)

    def click_continue_button(self) -> None:
        """Click the Continue button on registration form."""
        self.element_utils.click(self.CONTINUE_BUTTON)

    def click_success_page_continue_button(self) -> None:
        """Click the Continue button on the success page."""
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        
        # Wait for success page continue button to be clickable
        WebDriverWait(self.driver, 0.5).until(EC.element_to_be_clickable(self.SUCCESS_PAGE_CONTINUE_BUTTON))
        self.element_utils.click(self.SUCCESS_PAGE_CONTINUE_BUTTON)

    def get_success_message(self) -> str:
        """
        Get the success message text with explicit waits and visibility checks.
        
        Includes debugging for CSS properties and element visibility issues.
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException, NoSuchElementException
        import time
        
        try:
            print("DEBUG: get_success_message() - Starting...")
            
            # Wait for element to be present in DOM
            print("DEBUG: Waiting for element presence in DOM (10s)...")
            wait = WebDriverWait(self.driver, 10)
            element = wait.until(
                EC.presence_of_element_located(self.SUCCESS_MESSAGE_CONTAINER)
            )
            print(f"DEBUG: Element found in DOM: {element is not None}")
            
            # Wait for element to be visible on screen
            print("DEBUG: Waiting for element visibility (10s)...")
            element = wait.until(
                EC.visibility_of_element_located(self.SUCCESS_MESSAGE_CONTAINER)
            )
            print(f"DEBUG: Element is visible: {element is not None}")
            
            # Get CSS properties to check for hidden state
            z_index = element.value_of_css_property("z-index")
            display = element.value_of_css_property("display")
            visibility = element.value_of_css_property("visibility")
            opacity = element.value_of_css_property("opacity")
            
            print(f"DEBUG: CSS Properties - z-index: {z_index}, display: {display}, visibility: {visibility}, opacity: {opacity}")
            
            # Check if element is truly clickable/visible
            is_displayed = element.is_displayed()
            print(f"DEBUG: element.is_displayed(): {is_displayed}")
            
            # Get text
            text = element.text.strip() if element else ""
            print(f"DEBUG: Success message text: '{text}'")
            
            return text
            
        except TimeoutException as e:
            print(f"DEBUG: TimeoutException - Element not found/visible: {str(e)}")
            # Try alternative methods to get the message
            try:
                elements = self.driver.find_elements(*self.SUCCESS_MESSAGE_CONTAINER)
                print(f"DEBUG: Found {len(elements)} elements matching locator")
                for idx, el in enumerate(elements):
                    print(f"  Element {idx}: displayed={el.is_displayed()}, text='{el.text}'")
                    if el.is_displayed():
                        return el.text.strip()
            except Exception as inner_e:
                print(f"DEBUG: Error finding elements: {str(inner_e)}")
            return ""
        except Exception as e:
            print(f"DEBUG: Unexpected error in get_success_message(): {str(e)}")
            import traceback
            traceback.print_exc()
            return ""

    def is_success_message_displayed(self) -> bool:
        """
        Check if registration was successful with explicit waits and comprehensive debugging.
        
        Checks multiple indicators:
        1. URL navigation to success page
        2. Presence of success message element
        3. Visibility of success message
        4. Page content for success indicators
        """
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        from selenium.common.exceptions import TimeoutException
        import time
        
        try:
            print("\n=== is_success_message_displayed() - Starting ===")
            
            # Strategy 1: Wait for URL change to success page
            print("DEBUG: Strategy 1 - Waiting for URL change to success page (15s)...")
            wait = WebDriverWait(self.driver, 15)
            
            try:
                # Wait for URL to contain 'account/success'
                wait.until(
                    lambda driver: "account/success" in driver.current_url
                )
                print(f"DEBUG: URL changed to success page: {self.driver.current_url}")
                return True
            except TimeoutException:
                print("DEBUG: URL did not change to success page within 15s")
            
            # Strategy 2: Wait for success message element to be visible
            print("DEBUG: Strategy 2 - Waiting for success message element visibility (10s)...")
            try:
                element = wait.until(
                    EC.visibility_of_element_located(self.SUCCESS_MESSAGE_CONTAINER),
                    message="Success message not visible"
                )
                print(f"DEBUG: Success message element is visible: {element.text}")
                return True
            except TimeoutException as e:
                print(f"DEBUG: Success message element not visible: {str(e)}")
            
            # Strategy 3: Check page content for success indicators
            print("DEBUG: Strategy 3 - Checking page content for success indicators...")
            current_url = self.driver.current_url
            page_source = self.driver.page_source
            page_title = self.driver.title
            
            print(f"  Current URL: {current_url}")
            print(f"  Page Title: {page_title}")
            
            success_indicators = {
                "account/success in URL": "account/success" in current_url,
                "'Your Account' in page": "Your Account" in page_source,
                "'Success' in page": "Success" in page_source,
                "'Thank you' in page": "Thank you" in page_source,
                "'congratulations' in page": "congratulations" in page_source.lower(),
            }
            
            for indicator_name, result in success_indicators.items():
                print(f"  {indicator_name}: {result}")
            
            if any(success_indicators.values()):
                print("DEBUG: SUCCESS - One or more success indicators found!")
                return True
            
            # Strategy 4: Try to find element by alternative locators
            print("DEBUG: Strategy 4 - Trying alternative locators...")
            alternative_locators = [
                (By.XPATH, "//h1[contains(text(), 'Your Account')]"),
                (By.XPATH, "//div[contains(text(), 'Thank you')]"),
                (By.XPATH, "//h1[contains(text(), 'Success')]"),
                (By.CLASS_NAME, "contentpanel"),
            ]
            
            for idx, locator in enumerate(alternative_locators):
                try:
                    elements = self.driver.find_elements(*locator)
                    if elements:
                        print(f"  Alternative locator {idx} found {len(elements)} element(s)")
                        for el in elements:
                            if el.is_displayed():
                                print(f"    - Visible element: {el.text[:50]}...")
                                return True
                except Exception as e:
                    print(f"  Alternative locator {idx} error: {type(e).__name__}")
            
            print("DEBUG: FAILED - No success indicators found")
            return False
            
        except Exception as e:
            print(f"DEBUG: EXCEPTION in is_success_message_displayed(): {str(e)}")
            import traceback
            traceback.print_exc()
            return False

    def get_error_message(self) -> str:
        """Get the error message text."""
        element = self.element_utils.find_element(self.ERROR_MESSAGE_CONTAINER)
        return element.text if element else ""

    def is_error_message_displayed(self) -> bool:
        """Check if error message is displayed."""
        return self.element_utils.is_displayed(self.ERROR_MESSAGE_CONTAINER)
