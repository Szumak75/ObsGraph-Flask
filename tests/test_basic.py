"""
Author:  Jacek Kotlarski <jacek.kotlarski@bioseco.com>
Created: 2025-10-15

Purpose: Basic test to verify pytest installation and configuration.
"""


def test_basic() -> None:
    """Basic test to verify pytest is working correctly."""
    assert True


def test_addition() -> None:
    """Test basic arithmetic operation."""
    result: int = 1 + 1
    assert result == 2


def test_string_operations() -> None:
    """Test string operations."""
    test_string: str = "ObsGraph-Flask"
    assert "Flask" in test_string
    assert test_string.startswith("ObsGraph")
