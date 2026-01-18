"""Tests for Home Assistant client."""

import pytest
from hatui.client import Entity, HomeAssistantClient


class TestEntity:
    """Tests for Entity class."""

    def test_from_api_basic(self):
        """Test creating entity from API response."""
        data = {
            "entity_id": "light.living_room",
            "state": "on",
            "attributes": {
                "friendly_name": "Living Room Light",
                "brightness": 255,
            },
            "last_changed": "2026-01-17T12:00:00+00:00",
        }

        entity = Entity.from_api(data)

        assert entity.entity_id == "light.living_room"
        assert entity.state == "on"
        assert entity.friendly_name == "Living Room Light"
        assert entity.domain == "light"
        assert entity.attributes["brightness"] == 255
        assert entity.last_changed == "2026-01-17T12:00:00+00:00"

    def test_from_api_missing_friendly_name(self):
        """Test entity uses entity_id when friendly_name is missing."""
        data = {
            "entity_id": "sensor.temperature",
            "state": "72",
            "attributes": {},
        }

        entity = Entity.from_api(data)

        assert entity.friendly_name == "sensor.temperature"

    def test_from_api_empty_data(self):
        """Test entity handles empty data."""
        data = {}

        entity = Entity.from_api(data)

        assert entity.entity_id == ""
        assert entity.state == "unknown"
        assert entity.domain == ""


class TestHomeAssistantClient:
    """Tests for HomeAssistantClient."""

    def test_init(self):
        """Test client initialization."""
        client = HomeAssistantClient(
            server="http://localhost:8123",
            token="test-token",
        )

        assert client.server == "http://localhost:8123"
        assert client.token == "test-token"

    def test_init_strips_trailing_slash(self):
        """Test client strips trailing slash from server URL."""
        client = HomeAssistantClient(
            server="http://localhost:8123/",
            token="test-token",
        )

        assert client.server == "http://localhost:8123"

    def test_client_not_initialized_error(self):
        """Test accessing client without context manager raises error."""
        client = HomeAssistantClient(
            server="http://localhost:8123",
            token="test-token",
        )

        with pytest.raises(RuntimeError, match="Client not initialized"):
            _ = client.client
