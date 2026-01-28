# 🎯 Automation Test Store - Selenium Framework

A flow-driven, boundary-enforced UI automation framework built with Selenium and Pytest, designed for scalable end-to-end testing in cloud-native CI/CD environments.

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [What This Does](#-what-this-does)
- [Project Structure](#-project-structure)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Running Tests](#-running-tests)
- [Test Organization](#-test-organization)
- [Page Object Model](#-page-object-model)
- [Test Data Management](#-test-data-management)
- [CI/CD Pipeline](#-cicd-pipeline)
- [Docker Support](#-docker-support)
- [Reporting](#-reporting)

---

## ⚡ Quick Start

Get up and running in 3 minutes:

```bash
# 1. Clone and navigate to project
cd /Users/najib/Desktop/automationteststore

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run smoke tests
pytest -m smoke -v

# 4. View the HTML report
open reports/html/report.html
```

---

## 🎪 What This Does

This framework automates end-to-end testing for an e-commerce store:

✅ **User Management** - Registration, login, account updates, password changes
✅ **Shopping Features** - Product search, cart operations, wishlist management
✅ **Checkout & Orders** - Multi-step checkout, payment validation, order history
✅ **Advanced Features** - Keyboard navigation, performance testing, downloads, security

---

## 📁 Project Structure

```
automationteststore/
├── config/           # Settings & configuration (settings.py, pytest.ini)
├── base/             # BasePage with 40+ reusable methods
├── pages/            # 11 Page Objects (LoginPage, CartPage, etc.)
├── flows/            # 11 Business workflows (RegisterFlow, CheckoutFlow, etc.)
├── utilities/        # Logger, screenshot handler, wait handler
├── testCases/        # 80+ test cases organized by feature
├── data/             # JSON test data (users, products, orders, etc.)
├── reports/          # HTML, Allure, JUnit reports & screenshots
├── docker/           # Dockerfile & docker-compose.yml
├── .github/workflows/# GitHub Actions CI/CD (ui-tests.yml)
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

---

## 🛠 Tech Stack

| Component | Tool | Version |
|-----------|------|---------|
| **Language** | Python | 3.11+ |
| **Test Framework** | Pytest | 7.4.3 |
| **Browser Automation** | Selenium WebDriver | 4.15.2 |
| **Reporting** | Allure + pytest-html | 2.13.2 / 4.1.1 |
| **CI/CD** | GitHub Actions | Latest |
| **Containerization** | Docker | Latest |

---

## 📦 Installation

### Prerequisites
- Python 3.11+, pip, Git
- Chrome/Firefox for local testing

### Setup

```bash
# 1. Clone the repository
git clone <repository-url> && cd automationteststore

# 2. Create virtual environment
python -m venv venv && source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Verify
pytest --version && python -c "import selenium; print(selenium.__version__)"
```

---

## 🧪 Running Tests

### Basic Execution

```bash
pytest                                          # All tests
pytest -v                                       # Verbose
pytest -s                                       # Show prints
pytest testCases/test_login.py                 # Specific file
pytest testCases/test_login.py::test_name      # Specific test
```

### By Category (Markers)

```bash
pytest -m smoke                                 # Quick checks
pytest -m sanity                                # Basic functionality
pytest -m regression                            # Full suite
pytest -m critical                              # Business critical
pytest -m login -m cart                         # Multiple markers
```

### With Filters

```bash
pytest -k "login" -v                           # Keyword matching
pytest -k "not slow"                           # Exclude keyword
pytest --co -q                                 # Count tests
```

### Generate Reports

```bash
# HTML Report
pytest --html=reports/html/report.html --self-contained-html && open reports/html/report.html

# JUnit XML (for CI/CD)
pytest --junitxml=reports/junit/junit.xml

# Allure Report
pytest --alluredir=reports/allure-results && allure serve reports/allure-results

# All combined
pytest -v --html=reports/html/report.html --self-contained-html \
  --junitxml=reports/junit/junit.xml --alluredir=reports/allure-results
```

### Advanced Options

```bash
HEADLESS=true pytest                           # Headless mode
ENVIRONMENT=prod pytest                        # Production env
pytest -n auto                                 # Parallel (install: pytest-xdist)
pytest -v -x                                   # Stop on first failure
pytest --durations=10                          # Show slowest tests
```

---

## 📊 Test Organization

### Test Markers

| Marker | Purpose | Command |
|--------|---------|---------|
| `smoke` | Quick sanity | `pytest -m smoke` |
| `sanity` | Basic functionality | `pytest -m sanity` |
| `regression` | Full suite | `pytest -m regression` |
| `critical` | Business critical | `pytest -m critical` |
| `login` / `cart` / `checkout` | Feature-specific | `pytest -m login` |
| `slow` | Long-running | `pytest -m "not slow"` |

### Test Coverage (80+ tests)

- **Authentication**: 8 tests (register, login, validation)
- **Shopping Cart**: 12 tests (add, remove, update, calculations)
- **Checkout**: 8 tests (payment, shipping, orders)
- **Order History**: 6 tests (viewing, pagination, security)
- **Wishlist**: 4 tests (add, remove, updates)
- **Search**: 12 tests (keywords, filters, categories)
- **Account**: 8 tests (profile, password changes)
- **Downloads**: 9 tests (access, permissions)
- **Advanced**: 15 tests (keyboard nav, performance, edge cases)

---

## 🏗 Page Object Model

All pages inherit from `BasePage` which provides 40+ helper methods:

```python
# Element Interaction
click(locator) | type_text(locator, text) | clear_field(locator)
double_click() | right_click() | hover()

# Waits & Visibility
wait_for_element() | wait_for_visibility() | is_element_present()

# Data Retrieval
get_text(locator) | get_attribute() | get_value()

# Assertions
assert_text_present() | assert_element_present() | assert_title_contains()

# Navigation
get_current_url() | get_page_title() | navigate_back() | refresh_page()
```

### Creating a Page Object

```python
from base.base_page import BasePage
from selenium.webdriver.common.by import By

class NewPage(BasePage):
    HEADER = (By.CLASS_NAME, "page-header")
    SUBMIT_BTN = (By.ID, "submit-button")
    
    def fill_form(self, data):
        self.type_text((By.ID, "field1"), data['field1'])
        self.click(self.SUBMIT_BTN)
```

---

## 📋 Test Data

Test data in JSON files under `data/` directory:

```json
{
  "valid_user": {
    "firstName": "John",
    "lastName": "Doe",
    "email": "john@example.com",
    "password": "SecurePass123!"
  }
}
```

Using in tests:
```python
import json

with open('data/users.json', 'r') as f:
    data = json.load(f)
user = data['valid_user']
```

**Available files**: users.json, products.json, search_data.json, cart.json, checkout.json, orders.json, wishlist.json, account.json

---

## 🚀 CI/CD Pipeline

### GitHub Actions

Tests run automatically on:
- ✅ Push to main/develop
- ✅ Pull requests
- ✅ Daily at 2 AM UTC
- ✅ Manual trigger

### Workflow Matrix

```
Jobs:
- Smoke tests (fast feedback)
- Sanity tests (basic functionality)
- Regression tests (comprehensive)

Each job runs independently with:
- Parallel execution
- HTML, JUnit, Allure reports
- Screenshots on failure
- 30-minute timeout
```

**View Results**: GitHub Actions tab → Artifacts → Download reports

---

## 🐳 Docker Support

```bash
# Build image
docker build -f docker/Dockerfile -t automation-tests .

# Run tests
docker run --rm automation-tests pytest -m smoke

# With Docker Compose
docker-compose -f docker/docker-compose.yml up
```

Benefits: ✅ Consistent environment | ✅ No local setup | ✅ Easy CI/CD | ✅ Isolated execution

---

## 📊 Reporting

### Report Types

1. **HTML Report** - Comprehensive results, timings, screenshots
2. **JUnit XML** - CI/CD integration (GitHub, Jenkins)
3. **Allure Report** - Interactive, history tracking, trend analysis

```bash
open reports/html/report.html                  # HTML
allure serve reports/allure-results            # Allure (interactive)
tail -f reports/logs/test_execution.log        # Logs
open reports/screenshots/                      # Failure evidence
```

---

## 🎓 Best Practices

### ✅ Do's
- Single responsibility per test
- Descriptive test names
- Use pytest fixtures
- Keep locators in page objects
- Use explicit waits

### ❌ Don'ts
- Vague test names (test_1)
- Multiple assertions per test
- Hardcoded sleep() calls
- Locators in test code
- Implicit waits for everything

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| Tests timeout | Increase `IMPLICIT_WAIT` in settings.py |
| Element not found | Verify selector, add explicit waits |
| Flaky tests | Use waits, avoid sleep() |
| Report not generated | Check `reports/` directory exists |
| Docker fails | Rebuild: `docker build --no-cache` |

---

## 📞 Support

- 📖 [FRAMEWORK_GUIDE.md](FRAMEWORK_GUIDE.md) - Detailed documentation
- 🚀 [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Quick commands
- ⚙️ [config/README.md](config/README.md) - Configuration
- 📧 Contact: najibsunusi19@gmail.com

---

## 📄 License

MIT License - See LICENSE file

---

**Last Updated**: January 28, 2026 | **Version**: 1.0.0 | **Status**: Production Ready ✅

