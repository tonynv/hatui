"""Tests for HATUI application."""

import pytest
from hatui.app import HATUIApp


class TestHATUIApp:
    """Tests for HATUIApp."""

    def test_app_init_with_params(self):
        """Test app initialization with parameters."""
        app = HATUIApp(
            server="http://localhost:8123",
            token="test-token",
        )

        assert app.ha_server == "http://localhost:8123"
        assert app.ha_token == "test-token"

    def test_app_init_from_env(self, monkeypatch):
        """Test app initialization from environment variables."""
        monkeypatch.setenv("HASS_SERVER", "http://envserver:8123")
        monkeypatch.setenv("HASS_TOKEN", "env-token")

        app = HATUIApp()

        assert app.ha_server == "http://envserver:8123"
        assert app.ha_token == "env-token"

    def test_app_title(self):
        """Test app has correct title."""
        assert HATUIApp.TITLE == "HATUI - Home Assistant TUI"
