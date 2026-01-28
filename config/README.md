# Configuration & Test Data Guide

## Overview

This directory contains all project-level configuration, settings, and test data for the Selenium POM automation framework.

## Files & Directories

### `pytest.ini`
Pytest configuration file for test discovery, markers, and reporting.

**Key Features:**
- **Test Discovery:** Configures test path (`tests/`), file patterns, and function naming
- **Markers:** Organizes tests by feature (register, login, search, cart, checkout, orders, account, downloads, wishlist)
- **Reporting:** Enables HTML, JUnit XML, and Allure reporting
- **Logging:** Configures console and file logging
- **Warnings:** Filters deprecation warnings

**Usage:**
```bash
# Run all tests
pytest

# Run tests with specific marker
pytest -m register

# Run tests with HTML report
pytest --html=reports/html/report.html

# Run tests with Allure reporting
pytest --alluredir=reports/allure-results
```

### `settings.py`
Centralized project configuration and constants.

**Key Sections:**

1. **Project Structure**
   - Paths to all project directories (data, pages, flows, utilities, reports)
   - Automatically configures based on project root

2. **Environment Configuration**
   - Support for `dev`, `staging`, and `prod` environments
   - Set via `ENVIRONMENT` environment variable
   - Default: `dev`

3. **Application URLs**
   - Base URL for target application
   - Page-specific URLs (login, register, search, etc.)

4. **Wait & Timeout Configuration**
   - `DEFAULT_TIMEOUT`: 10 seconds
   - `IMPLICIT_WAIT`: 5 seconds
   - `PAGE_LOAD_TIMEOUT`: 15 seconds
   - Configurable via environment variables

5. **Browser Configuration**
   - Browser selection (chrome, firefox, edge)
   - Headless mode support
   - Window size settings
   - Browser-specific options

6. **Reporting**
   - Allure report support
   - HTML report generation
   - JUnit XML for CI/CD

7. **Feature Flags**
   - Enable/disable features dynamically
   - Useful for testing different configurations

**Usage in Tests:**
```python
from config.settings import BASE_URL, DEFAULT_TIMEOUT, BROWSER

# Use in your test code
driver.get(BASE_URL)
WebDriverWait(driver, DEFAULT_TIMEOUT).until(EC.presence_of_element_located(locator))
```

**Environment Variables:**
```bash
# Set environment
export ENVIRONMENT=staging
export BROWSER=firefox
export HEADLESS=true
export DEFAULT_TIMEOUT=15
export HEADLESS=true

# Run tests with custom configuration
ENVIRONMENT=prod BROWSER=chrome pytest
```

### `data/` Directory

Contains all test data in JSON format for different features.

#### `users.json`
User credentials and account data for login/registration tests.

**Scenarios Covered:**
- Valid user with correct credentials
- Invalid credentials (wrong password)
- Non-existent user
- Invalid email formats
- Empty fields
- Special characters in email

**Usage:**
```python
import json
from config.settings import USERS_DATA_FILE

with open(USERS_DATA_FILE) as f:
    users_data = json.load(f)
    valid_user = users_data['valid_user']
    email = valid_user['email']
    password = valid_user['password']
```

#### `products.json`
Product information for search, cart, and checkout tests.

**Data Includes:**
- Product name, category, price, quantity
- SKU (Stock Keeping Unit)
- Special test cases (out of stock, discontinued, high/low prices)

**Scenarios Covered:**
- Valid products (single and multiple)
- High quantity items
- Out of stock products
- Discontinued items
- Products with special characters in names

#### `search.json`
Search keywords and filters for product search tests.

**Scenarios Covered:**
- Single result searches
- Multiple result searches
- No results searches
- Empty search
- Special characters
- Case sensitivity
- Price range filters

#### `cart.json`
Shopping cart scenarios and states.

**Scenarios Covered:**
- Single item cart
- Multiple items cart
- High quantity items
- Empty cart
- Quantity updates
- Item removal

#### `checkout.json`
Checkout and payment information.

**Scenarios Covered:**
- Valid checkout with billing and shipping
- Same address for billing/shipping
- Missing address fields
- Invalid email formats
- Invalid phone numbers
- Invalid postal codes
- Invalid credit card numbers
- Expired credit cards

#### `wishlist.json`
Wishlist operations and states.

**Scenarios Covered:**
- Add single product
- Add multiple products
- Remove products
- Duplicate products
- Empty wishlist
- Move to cart
- Share wishlist

#### `account.json`
Account information updates and password changes.

**Scenarios Covered:**
- Update first name, last name, email, phone
- Update all fields
- Invalid email format
- Change password (valid scenario)
- Change password with incorrect current password
- Password mismatch
- Same as current password

#### `orders.json`
Order history and order details.

**Scenarios Covered:**
- Single item order
- Multiple item orders
- High quantity orders
- Different order statuses (completed, shipped, pending, delivered, cancelled)
- Order calculations (subtotal, shipping, tax, total)

## Directory Structure

```
config/
├── __init__.py
├── pytest.ini
├── settings.py
└── README.md (this file)

data/
├── users.json
├── products.json
├── search.json
├── cart.json
├── checkout.json
├── wishlist.json
├── account.json
└── orders.json
```

## Environment-Specific Configuration

### Development (Default)
```bash
ENVIRONMENT=dev
BASE_URL=https://automationteststore.com
BROWSER=chrome
HEADLESS=false
LOG_LEVEL=DEBUG
```

### Staging
```bash
ENVIRONMENT=staging
BASE_URL=https://staging.automationteststore.com
BROWSER=chrome
HEADLESS=true
LOG_LEVEL=INFO
```

### Production
```bash
ENVIRONMENT=prod
BASE_URL=https://automationteststore.com
BROWSER=chrome
HEADLESS=true
LOG_LEVEL=INFO
```

## CI/CD Integration

### GitHub Actions
The framework automatically detects CI/CD environments (GitHub Actions, Jenkins, GitLab CI, Travis, CircleCI) and adjusts configuration accordingly:
- Enables headless mode
- Sets log level to INFO
- Enables HTML and JUnit XML reporting
- Disables interactive features

### Environment Variables
Set in your CI/CD pipeline:
```yaml
env:
  ENVIRONMENT: prod
  BROWSER: chrome
  HEADLESS: true
  GITHUB_ACTIONS: true
```

## Best Practices

### 1. Test Data Management
- **Don't hardcode credentials** in tests - use `users.json`
- **Keep test data realistic** - use valid formats for emails, phone numbers, etc.
- **Separate positive and negative scenarios** - organize in same file with clear names
- **Update data periodically** - sync with actual application requirements

### 2. Configuration Management
- **Use environment variables** for CI/CD
- **Never commit sensitive data** (actual passwords, API keys)
- **Use configuration classes** instead of magic numbers
- **Document all settings** in comments

### 3. Path Handling
- **Use `settings.py` paths** - automatically handles platform differences (Windows/Linux/macOS)
- **Never use hardcoded paths** - use `DATA_DIR`, `REPORTS_DIR`, etc.
- **Create directories** if needed - framework creates them automatically

### 4. Timeout Configuration
- **Adjust based on network** - increase for slow connections
- **Use explicit waits** - don't rely on implicit waits alone
- **Set reasonable timeouts** - typically 10-15 seconds for element operations

## Adding New Test Data

When adding new features:

1. **Identify data requirements**
   - What user roles/types are needed?
   - What product scenarios exist?
   - What error cases should be tested?

2. **Create data file** (if new feature)
   - Follow existing JSON structure
   - Use descriptive scenario names
   - Include descriptions for clarity

3. **Update `settings.py`**
   - Add path to new data file
   - Add any new URLs or timeouts
   - Add feature flag if needed

4. **Example: Adding new feature data**
   ```json
   {
     "scenario_name": {
       "field1": "value1",
       "field2": "value2",
       "description": "What this scenario tests"
     }
   }
   ```

## Loading Test Data in Tests

### Basic Loading
```python
import json
from config.settings import USERS_DATA_FILE

with open(USERS_DATA_FILE) as f:
    users = json.load(f)
```

### With Error Handling
```python
import json
from config.settings import PRODUCTS_DATA_FILE

try:
    with open(PRODUCTS_DATA_FILE) as f:
        products = json.load(f)
except FileNotFoundError:
    raise Exception(f"Test data file not found: {PRODUCTS_DATA_FILE}")
except json.JSONDecodeError:
    raise Exception(f"Invalid JSON in: {PRODUCTS_DATA_FILE}")
```

### Using Fixtures (Pytest)
```python
import json
import pytest
from config.settings import USERS_DATA_FILE

@pytest.fixture(scope="session")
def user_data():
    with open(USERS_DATA_FILE) as f:
        return json.load(f)

def test_login(user_data):
    valid_user = user_data['valid_user']
    # Use valid_user in test
```

## Troubleshooting

### Issue: Configuration not loading
**Solution:** Ensure `config/__init__.py` exists and is empty (package marker)

### Issue: Test data file not found
**Solution:** Check file exists in `data/` folder, verify filename in `settings.py`

### Issue: Wrong environment being used
**Solution:** 
```bash
# Check current environment
echo $ENVIRONMENT
# Set environment
export ENVIRONMENT=staging
```

### Issue: Timeout errors
**Solution:** Increase `DEFAULT_TIMEOUT` in `settings.py` or via environment variable
```bash
export DEFAULT_TIMEOUT=20
```

## References

- [pytest.ini Documentation](https://docs.pytest.org/en/stable/ini.html)
- [Selenium WebDriver Waits](https://selenium.dev/documentation/webdriver/waits/)
- [Test Data Management Best Practices](https://www.saucelabs.com/blog/test-data-management)
- [CI/CD Best Practices](https://docs.github.com/en/actions/automating-builds-and-testing)
