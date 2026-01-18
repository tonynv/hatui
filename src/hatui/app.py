"""HATUI - Home Assistant Terminal User Interface."""

import os
import asyncio
from typing import ClassVar

from textual import on, work
from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header,
    Footer,
    Static,
    DataTable,
    Button,
    Input,
    Label,
    TabbedContent,
    TabPane,
    LoadingIndicator,
)
from textual.screen import ModalScreen

from .client import HomeAssistantClient, Entity


class EntityTable(DataTable):
    """DataTable for displaying Home Assistant entities."""

    BINDINGS = [
        Binding("enter", "toggle_entity", "Toggle"),
        Binding("r", "refresh", "Refresh"),
    ]

    def __init__(self, domain_filter: str | None = None, **kwargs):
        super().__init__(**kwargs)
        self.domain_filter = domain_filter
        self.entities: dict[str, Entity] = {}

    def action_toggle_entity(self) -> None:
        """Toggle the selected entity."""
        if self.cursor_row is not None:
            row_key = self.get_row_at(self.cursor_row)
            if row_key:
                entity_id = str(row_key.value)
                self.app.toggle_entity(entity_id)

    def action_refresh(self) -> None:
        """Refresh entities."""
        self.app.refresh_entities()


class StatusBar(Static):
    """Status bar showing connection info."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.server = ""
        self.version = ""
        self.location = ""

    def update_status(self, server: str, version: str, location: str) -> None:
        """Update status bar content."""
        self.server = server
        self.version = version
        self.location = location
        self.update(f" {location} | {server} | HA {version}")


class HATUIApp(App):
    """Home Assistant Terminal User Interface."""

    TITLE = "HATUI - Home Assistant TUI"
    CSS = """
    Screen {
        background: $surface;
    }

    #main-container {
        height: 100%;
        width: 100%;
    }

    #status-bar {
        dock: bottom;
        height: 1;
        background: $primary;
        color: $text;
        padding: 0 1;
    }

    EntityTable {
        height: 100%;
    }

    DataTable > .datatable--cursor {
        background: $accent;
    }

    .entity-on {
        color: $success;
    }

    .entity-off {
        color: $error;
    }

    .tab-pane {
        padding: 1;
    }

    #loading {
        align: center middle;
        height: 100%;
    }

    .hidden {
        display: none;
    }
    """

    BINDINGS: ClassVar[list[Binding]] = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("t", "toggle", "Toggle"),
        Binding("1", "tab_lights", "Lights", show=False),
        Binding("2", "tab_switches", "Switches", show=False),
        Binding("3", "tab_sensors", "Sensors", show=False),
        Binding("4", "tab_climate", "Climate", show=False),
        Binding("5", "tab_all", "All", show=False),
    ]

    def __init__(self, server: str | None = None, token: str | None = None):
        super().__init__()
        self.ha_server = server or os.environ.get("HASS_SERVER", "")
        self.ha_token = token or os.environ.get("HASS_TOKEN", "")
        self.client: HomeAssistantClient | None = None
        self.entities: dict[str, Entity] = {}
        self._refresh_task: asyncio.Task | None = None

    def compose(self) -> ComposeResult:
        """Compose the UI."""
        yield Header()
        yield Container(
            LoadingIndicator(id="loading"),
            TabbedContent(
                TabPane("Lights", EntityTable(domain_filter="light", id="lights-table"), id="lights"),
                TabPane("Switches", EntityTable(domain_filter="switch", id="switches-table"), id="switches"),
                TabPane("Sensors", EntityTable(domain_filter="sensor", id="sensors-table"), id="sensors"),
                TabPane("Climate", EntityTable(domain_filter="climate", id="climate-table"), id="climate"),
                TabPane("All", EntityTable(id="all-table"), id="all"),
                id="tabs",
                classes="hidden",
            ),
            id="main-container",
        )
        yield StatusBar(id="status-bar")
        yield Footer()

    async def on_mount(self) -> None:
        """Handle app mount."""
        if not self.ha_server or not self.ha_token:
            self.notify(
                "Set HASS_SERVER and HASS_TOKEN environment variables",
                severity="error",
            )
            return

        self.client = HomeAssistantClient(self.ha_server, self.ha_token)
        await self.connect_and_load()
        self.start_auto_refresh()

    @work(exclusive=True)
    async def connect_and_load(self) -> None:
        """Connect to Home Assistant and load entities."""
        if not self.client:
            return

        loading = self.query_one("#loading", LoadingIndicator)
        tabs = self.query_one("#tabs", TabbedContent)

        try:
            async with self.client as client:
                # Check connection
                if not await client.check_connection():
                    self.notify("Failed to connect to Home Assistant", severity="error")
                    return

                # Get config for status bar
                config = await client.get_config()
                status_bar = self.query_one("#status-bar", StatusBar)
                status_bar.update_status(
                    self.ha_server,
                    config.get("version", "unknown"),
                    config.get("location_name", "Home"),
                )

                # Get all states
                entities = await client.get_states()
                self.entities = {e.entity_id: e for e in entities}

                # Update tables
                self.update_all_tables()

                # Show tabs, hide loading
                loading.add_class("hidden")
                tabs.remove_class("hidden")

                self.notify(f"Loaded {len(entities)} entities")

        except Exception as e:
            self.notify(f"Error: {e}", severity="error")

    def update_all_tables(self) -> None:
        """Update all entity tables."""
        tables = {
            "lights-table": "light",
            "switches-table": "switch",
            "sensors-table": "sensor",
            "climate-table": "climate",
            "all-table": None,
        }

        for table_id, domain in tables.items():
            try:
                table = self.query_one(f"#{table_id}", EntityTable)
                self.update_table(table, domain)
            except Exception:
                pass

    def update_table(self, table: EntityTable, domain: str | None) -> None:
        """Update a specific entity table."""
        table.clear(columns=True)
        table.add_columns("Entity", "Name", "State", "Last Changed")

        filtered = [
            e for e in self.entities.values()
            if domain is None or e.domain == domain
        ]

        # Sort by domain then name
        filtered.sort(key=lambda e: (e.domain, e.friendly_name))

        for entity in filtered:
            state_display = entity.state
            if entity.domain in ("light", "switch", "fan"):
                state_display = "ON" if entity.state == "on" else "OFF" if entity.state == "off" else entity.state

            # Format last changed
            last_changed = entity.last_changed[:19].replace("T", " ") if entity.last_changed else ""

            table.add_row(
                entity.entity_id,
                entity.friendly_name[:40],
                state_display,
                last_changed,
                key=entity.entity_id,
            )

    @work(exclusive=True)
    async def refresh_entities(self) -> None:
        """Refresh all entities."""
        if not self.client:
            return

        try:
            async with self.client as client:
                entities = await client.get_states()
                self.entities = {e.entity_id: e for e in entities}
                self.update_all_tables()
                self.notify("Refreshed")
        except Exception as e:
            self.notify(f"Refresh failed: {e}", severity="error")

    @work(exclusive=True)
    async def toggle_entity(self, entity_id: str) -> None:
        """Toggle an entity."""
        if not self.client:
            return

        entity = self.entities.get(entity_id)
        if not entity:
            return

        if entity.domain not in ("light", "switch", "fan", "cover", "lock"):
            self.notify(f"Cannot toggle {entity.domain}", severity="warning")
            return

        try:
            async with self.client as client:
                await client.toggle(entity_id)
                self.notify(f"Toggled {entity.friendly_name}")
                # Refresh after toggle
                await asyncio.sleep(0.5)
            await self.refresh_entities()
        except Exception as e:
            self.notify(f"Toggle failed: {e}", severity="error")

    def start_auto_refresh(self, interval: int = 30) -> None:
        """Start auto-refresh timer."""
        self.set_interval(interval, self.refresh_entities)

    def action_refresh(self) -> None:
        """Refresh action."""
        self.refresh_entities()

    def action_toggle(self) -> None:
        """Toggle current entity."""
        tabs = self.query_one("#tabs", TabbedContent)
        active_tab = tabs.active
        if active_tab:
            table_id = f"{active_tab}-table"
            try:
                table = self.query_one(f"#{table_id}", EntityTable)
                table.action_toggle_entity()
            except Exception:
                pass

    def action_tab_lights(self) -> None:
        """Switch to lights tab."""
        self.query_one("#tabs", TabbedContent).active = "lights"

    def action_tab_switches(self) -> None:
        """Switch to switches tab."""
        self.query_one("#tabs", TabbedContent).active = "switches"

    def action_tab_sensors(self) -> None:
        """Switch to sensors tab."""
        self.query_one("#tabs", TabbedContent).active = "sensors"

    def action_tab_climate(self) -> None:
        """Switch to climate tab."""
        self.query_one("#tabs", TabbedContent).active = "climate"

    def action_tab_all(self) -> None:
        """Switch to all tab."""
        self.query_one("#tabs", TabbedContent).active = "all"


def main():
    """Run the HATUI app."""
    app = HATUIApp()
    app.run()


if __name__ == "__main__":
    main()
