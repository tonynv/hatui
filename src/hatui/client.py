"""Home Assistant API client."""

import asyncio
from typing import Any
from dataclasses import dataclass
import httpx


@dataclass
class Entity:
    """Represents a Home Assistant entity."""
    entity_id: str
    state: str
    friendly_name: str
    domain: str
    attributes: dict[str, Any]
    last_changed: str

    @classmethod
    def from_api(cls, data: dict[str, Any]) -> "Entity":
        """Create Entity from API response."""
        entity_id = data.get("entity_id", "")
        return cls(
            entity_id=entity_id,
            state=data.get("state", "unknown"),
            friendly_name=data.get("attributes", {}).get("friendly_name", entity_id),
            domain=entity_id.split(".")[0] if "." in entity_id else "",
            attributes=data.get("attributes", {}),
            last_changed=data.get("last_changed", ""),
        )


class HomeAssistantClient:
    """Async client for Home Assistant REST API."""

    def __init__(self, server: str, token: str):
        """Initialize the client.

        Args:
            server: Home Assistant server URL (e.g., http://localhost:8123)
            token: Long-lived access token
        """
        self.server = server.rstrip("/")
        self.token = token
        self._client: httpx.AsyncClient | None = None

    async def __aenter__(self):
        """Async context manager entry."""
        self._client = httpx.AsyncClient(
            base_url=self.server,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            timeout=10.0,
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self._client:
            await self._client.aclose()

    @property
    def client(self) -> httpx.AsyncClient:
        """Get the HTTP client."""
        if self._client is None:
            raise RuntimeError("Client not initialized. Use async context manager.")
        return self._client

    async def get_states(self) -> list[Entity]:
        """Get all entity states."""
        response = await self.client.get("/api/states")
        response.raise_for_status()
        return [Entity.from_api(item) for item in response.json()]

    async def get_state(self, entity_id: str) -> Entity:
        """Get state of a specific entity."""
        response = await self.client.get(f"/api/states/{entity_id}")
        response.raise_for_status()
        return Entity.from_api(response.json())

    async def call_service(
        self, domain: str, service: str, entity_id: str | None = None, **kwargs
    ) -> dict[str, Any]:
        """Call a Home Assistant service."""
        data = kwargs
        if entity_id:
            data["entity_id"] = entity_id

        response = await self.client.post(
            f"/api/services/{domain}/{service}",
            json=data,
        )
        response.raise_for_status()
        return response.json()

    async def turn_on(self, entity_id: str, **kwargs) -> dict[str, Any]:
        """Turn on an entity."""
        domain = entity_id.split(".")[0]
        return await self.call_service(domain, "turn_on", entity_id, **kwargs)

    async def turn_off(self, entity_id: str) -> dict[str, Any]:
        """Turn off an entity."""
        domain = entity_id.split(".")[0]
        return await self.call_service(domain, "turn_off", entity_id)

    async def toggle(self, entity_id: str) -> dict[str, Any]:
        """Toggle an entity."""
        domain = entity_id.split(".")[0]
        return await self.call_service(domain, "toggle", entity_id)

    async def get_config(self) -> dict[str, Any]:
        """Get Home Assistant configuration."""
        response = await self.client.get("/api/config")
        response.raise_for_status()
        return response.json()

    async def check_connection(self) -> bool:
        """Check if connection to Home Assistant is working."""
        try:
            response = await self.client.get("/api/")
            return response.status_code == 200
        except Exception:
            return False
