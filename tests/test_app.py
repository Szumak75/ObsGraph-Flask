"""
Author:  Jacek Kotlarski --<jacek.kotlarski@bioseco.com>
Created: 2025-10-15

Purpose: Unit tests for the main Flask application routes and functionality.

This module contains pytest-based tests for the Flask application's HTTP routes,
response validation, and configuration. Tests use Flask's test client to simulate
HTTP requests without running a real server.
"""

from datetime import datetime
from typing import Any

import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import patch

from obsgraph_flask.app import app


@pytest.fixture
def client() -> FlaskClient:
    """Create and configure Flask test client.

    Configures the Flask application in testing mode and returns a test client
    that can be used to simulate HTTP requests to the application.

    ### Returns:
    FlaskClient - Test client for making HTTP requests to the app without running a server.
    """
    app.config["TESTING"] = True
    with app.test_client() as client:
        return client


class TestIndexRoute:
    """Test suite for the main index route (/) functionality.

    Tests cover both GET and POST request handling, default value behavior,
    date formatting, and response validation for the main application route.
    """

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

    def test_index_form_does_not_post_to_domain_root(
        self, client: FlaskClient
    ) -> None:
        """Test that form submission targets the current URL, not domain root.

        ### Arguments:
        * client: FlaskClient - The test client fixture.
        """
        response: Any = client.get("/")
        assert b'action="/"' not in response.data

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

    @patch("obsgraph_flask.app.obs_app.get_observium_charts")
    def test_index_renders_two_chart_sections_with_headers(
        self,
        mock_get_observium_charts: Any,
        client: FlaskClient,
    ) -> None:
        """Test that index renders two chart sections and their headers."""
        mock_get_observium_charts.return_value = [
            {"header": "TASK", "image": "data:image/png;base64,ZmFrZQ=="},
            {"header": "Biuro", "image": "data:image/png;base64,ZmFrZTI="},
        ]

        response: Any = client.get("/")

        assert response.status_code == 200
        assert b"TASK" in response.data
        assert b"Biuro" in response.data
        assert response.data.count(b"data:image/png;base64,") == 2


class TestAppConfiguration:
    """Test suite for Flask application configuration and initialization.

    Tests verify that the Flask application instance is properly initialized
    and has the correct configuration properties.
    """

    def test_app_exists(self) -> None:
        """Test that Flask app instance exists."""
        assert app is not None
        assert isinstance(app, Flask)

    def test_app_name(self) -> None:
        """Test that Flask app has correct name."""
        assert app.name == "obsgraph_flask.app"


class TestGraphDimensionsConfiguration:
    """Test suite for graph dimensions configuration."""

    def test_default_graph_width(self) -> None:
        """Test that default graph width is 1024."""
        from obsgraph_flask.app import obs_app

        # Should return default value of 1024 if not configured
        width: int = obs_app.conf_graph_width
        assert isinstance(width, int)
        assert width > 0

    def test_default_graph_height(self) -> None:
        """Test that default graph height is 600."""
        from obsgraph_flask.app import obs_app

        # Should return default value of 600 if not configured
        height: int = obs_app.conf_graph_height
        assert isinstance(height, int)
        assert height > 0
