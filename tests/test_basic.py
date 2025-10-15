"""
Author:  Jacek Kotlarski <jacek.kotlarski@bioseco.com>
Created: 2025-10-15

Purpose: Basic test to verify pytest installation and configuration.
"""


def test_basic():
    """Basic test to verify pytest is working correctly."""
    assert True


def test_addition():
    """Test basic arithmetic operation."""
    assert 1 + 1 == 2


def test_string_operations():
    """Test string operations."""
    test_string = "ObsGraph-Flask"
    assert "Flask" in test_string
    assert test_string.startswith("ObsGraph")
