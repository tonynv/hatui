---
title: Installation
description: How to install and configure HATUI
order: 1
---

## Requirements

- Python 3.10 or higher
- Home Assistant instance with API access
- Long-lived access token

## Install with pipx (Recommended)

```bash
pipx install hatui
```

## Install with pip

```bash
pip install hatui
```

## Install from Source

```bash
git clone https://github.com/tonynv/hatui.git
cd hatui
pip install -e .
```

## Configuration

HATUI requires two environment variables to connect to your Home Assistant instance:

```bash
export HASS_SERVER="http://your-homeassistant:8123"
export HASS_TOKEN="your-long-lived-access-token"
```

### Getting a Long-Lived Access Token

1. Open your Home Assistant web UI
2. Click your profile icon (bottom left)
3. Scroll down to **Long-Lived Access Tokens**
4. Click **Create Token**
5. Give it a name (e.g., "HATUI")
6. Copy the token immediately (you won't see it again)

### Persistent Configuration

Add the environment variables to your shell configuration file:

**For Bash (~/.bashrc):**
```bash
echo 'export HASS_SERVER="http://your-homeassistant:8123"' >> ~/.bashrc
echo 'export HASS_TOKEN="your-token-here"' >> ~/.bashrc
```

**For Zsh (~/.zshrc):**
```bash
echo 'export HASS_SERVER="http://your-homeassistant:8123"' >> ~/.zshrc
echo 'export HASS_TOKEN="your-token-here"' >> ~/.zshrc
```

## Verify Installation

```bash
hatui --version
```

Then run:

```bash
hatui
```

You should see the HATUI terminal interface with your Home Assistant entities.
