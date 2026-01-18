# HATUI - Home Assistant Terminal User Interface

A terminal-based dashboard for Home Assistant built with [Textual](https://textual.textualize.io/).

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Features

- View all Home Assistant entities in a terminal UI
- Toggle lights, switches, fans, and covers
- Tabbed interface for different entity types (Lights, Switches, Sensors, Climate)
- Auto-refresh every 30 seconds
- Keyboard-driven navigation

## Installation

### From PyPI (coming soon)

```bash
pip install hatui
```

### From Source

```bash
git clone https://github.com/tonynv/hatui.git
cd hatui
pip install -e .
```

### Using pipx

```bash
pipx install hatui
```

## Configuration

Set the following environment variables:

```bash
export HASS_SERVER="http://your-homeassistant:8123"
export HASS_TOKEN="your-long-lived-access-token"
```

### Getting a Long-Lived Access Token

1. Go to your Home Assistant web UI
2. Click your profile (bottom left)
3. Scroll down to "Long-Lived Access Tokens"
4. Click "Create Token"
5. Copy the token and set it as `HASS_TOKEN`

## Usage

```bash
hatui
```

Or run as a module:

```bash
python -m hatui
```

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit |
| `r` | Refresh entities |
| `t` or `Enter` | Toggle selected entity |
| `1` | Lights tab |
| `2` | Switches tab |
| `3` | Sensors tab |
| `4` | Climate tab |
| `5` | All entities tab |
| `↑/↓` | Navigate entities |
| `Tab` | Switch tabs |

## Screenshots

```
┌─────────────────────────────────────────────────────────────────┐
│ HATUI - Home Assistant TUI                                      │
├─────────────────────────────────────────────────────────────────┤
│ Lights │ Switches │ Sensors │ Climate │ All                     │
├─────────────────────────────────────────────────────────────────┤
│ Entity              │ Name           │ State │ Last Changed     │
│ light.living_room   │ Living Room    │ ON    │ 2026-01-17 15:30 │
│ light.bedroom       │ Bedroom        │ OFF   │ 2026-01-17 14:22 │
│ light.kitchen       │ Kitchen        │ ON    │ 2026-01-17 15:45 │
├─────────────────────────────────────────────────────────────────┤
│ Home | http://10.0.0.28:8123 | HA 2026.1.1                      │
└─────────────────────────────────────────────────────────────────┘
```

## Development

```bash
# Clone the repo
git clone https://github.com/tonynv/hatui.git
cd hatui

# Install dev dependencies
pip install -e ".[dev]"

# Run linting
ruff check src/

# Run type checking
mypy src/

# Run tests
pytest
```

## Requirements

- Python 3.10+
- Home Assistant instance with API access
- Long-lived access token

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## Related Projects

- [hass-cli](https://github.com/home-assistant-ecosystem/home-assistant-cli) - Official Home Assistant CLI
- [Textual](https://github.com/Textualize/textual) - TUI framework for Python
