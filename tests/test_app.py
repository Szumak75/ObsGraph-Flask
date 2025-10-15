"""
Author:  Jacek Kotlarski <jacek.kotlarski@bioseco.com>
Created: 2025-10-15

Purpose: Tests for the main Flask application.
"""

from datetime import datetime
from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient

from obsgraph_flask.app import app


@pytest.fixture
def client() -> FlaskClient:
    """Create test client for Flask app.

    ### Returns:
    FlaskClient - Test client for making requests to the app.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        return client


class TestIndexRoute:
    """Tests for the main index route."""

    def test_index_get_returns_200(self, client: FlaskClient) -> None:
        """Test that GET request to index returns 200 status code.

        ### Arguments:
        * client: FlaskClient - The test client fixture.
        """
        response: Any = client.get("/")
        assert response.status_code == 200

    def test_index_returns_html(self, client: FlaskClient) -> None:
        """Test that index returns HTML content.

        ### Arguments:
        * client: FlaskClient - The test client fixture.
        """
        response: Any = client.get("/")
        assert b"text/html" in response.content_type.encode()

    def test_index_contains_current_year(self, client: FlaskClient) -> None:
        """Test that index page contains current year.

        ### Arguments:
        * client: FlaskClient - The test client fixture.
        """
        response: Any = client.get("/")
        current_year: int = datetime.now().year
        assert str(current_year).encode() in response.data

    def test_index_post_returns_200(self, client: FlaskClient) -> None:
        """Test that POST request to index returns 200 status code.

        ### Arguments:
        * client: FlaskClient - The test client fixture.
        """
        response: Any = client.post("/", data={"year": "2025", "month": "10"})
        assert response.status_code == 200

    def test_index_post_with_year_month(self, client: FlaskClient) -> None:
        """Test that POST with year and month returns correct formatted date.

        ### Arguments:
        * client: FlaskClient - The test client fixture.
        """
        response: Any = client.post("/", data={"year": "2025", "month": "10"})
        assert b"2025-10" in response.data

    def test_index_post_with_single_digit_month(
        self,
        client: FlaskClient,
    ) -> None:
        """Test that single digit month is zero-padded.

        ### Arguments:
        * client: FlaskClient - The test client fixture.
        """
        response: Any = client.post("/", data={"year": "2025", "month": "5"})
        assert b"2025-05" in response.data

    def test_index_default_values(self, client: FlaskClient) -> None:
        """Test that index uses current date as defaults.

        ### Arguments:
        * client: FlaskClient - The test client fixture.
        """
        response: Any = client.get("/")
        current_year: int = datetime.now().year
        current_month: int = datetime.now().month
        expected_date: str = f"{current_year:04d}-{current_month:02d}"
        assert expected_date.encode() in response.data


class TestAppConfiguration:
    """Tests for Flask app configuration."""

    def test_app_exists(self) -> None:
        """Test that Flask app instance exists."""
        assert app is not None
        assert isinstance(app, Flask)

    def test_app_name(self) -> None:
        """Test that Flask app has correct name."""
        assert app.name == "obsgraph_flask.app"
