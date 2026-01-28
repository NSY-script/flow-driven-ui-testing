"""
Test cases conftest - imports fixtures from root conftest.
"""

import pytest
import sys
import os

# Add parent directory to path so we can import from root conftest
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import all fixtures from root conftest
from conftest import *  # noqa: F401, F403
