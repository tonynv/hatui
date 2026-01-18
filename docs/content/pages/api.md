---
title: API Reference
description: HATUI Python API documentation
order: 3
---

## HomeAssistantClient

The `HomeAssistantClient` class provides an async interface to the Home Assistant REST API.

### Basic Usage

```python
from hatui.client import HomeAssistantClient

async with HomeAssistantClient(
    server="http://localhost:8123",
    token="your-token"
) as client:
    # Get all entity states
    entities = await client.get_states()

    # Toggle a light
    await client.toggle("light.living_room")
```

### Methods

#### get_states()

Returns a list of all entity states.

```python
entities = await client.get_states()
for entity in entities:
    print(f"{entity.entity_id}: {entity.state}")
```

#### get_state(entity_id)

Returns the state of a specific entity.

```python
entity = await client.get_state("light.living_room")
print(f"State: {entity.state}")
print(f"Brightness: {entity.attributes.get('brightness')}")
```

#### call_service(domain, service, entity_id, **kwargs)

Calls a Home Assistant service.

```python
await client.call_service(
    "light", "turn_on",
    entity_id="light.living_room",
    brightness=255
)
```

#### turn_on(entity_id, **kwargs)

Turns on an entity.

```python
await client.turn_on("light.kitchen", brightness=128)
```

#### turn_off(entity_id)

Turns off an entity.

```python
await client.turn_off("light.kitchen")
```

#### toggle(entity_id)

Toggles an entity's state.

```python
await client.toggle("switch.fan")
```

#### get_config()

Returns the Home Assistant configuration.

```python
config = await client.get_config()
print(f"Version: {config['version']}")
print(f"Location: {config['location_name']}")
```

## Entity Class

The `Entity` dataclass represents a Home Assistant entity.

### Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `entity_id` | str | The entity ID (e.g., "light.living_room") |
| `state` | str | Current state (e.g., "on", "off", "72") |
| `friendly_name` | str | Human-readable name |
| `domain` | str | Entity domain (e.g., "light", "sensor") |
| `attributes` | dict | Additional entity attributes |
| `last_changed` | str | ISO timestamp of last state change |

### Example

```python
entity = await client.get_state("light.living_room")

print(entity.entity_id)      # "light.living_room"
print(entity.state)          # "on"
print(entity.friendly_name)  # "Living Room Light"
print(entity.domain)         # "light"
print(entity.attributes)     # {"brightness": 255, "color_mode": "brightness"}
```
