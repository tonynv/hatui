---
title: Usage
description: How to use HATUI
order: 2
---

## Starting HATUI

Simply run:

```bash
hatui
```

The application will connect to your Home Assistant instance and display all entities in a tabbed interface.

## Interface Overview

HATUI displays a terminal-based dashboard with:

- **Header**: Shows the application title
- **Tabs**: Organize entities by type (Lights, Switches, Sensors, Climate, All)
- **Entity Table**: Lists entities with their state and last changed time
- **Status Bar**: Shows your Home Assistant server info and version
- **Footer**: Displays available keyboard shortcuts

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `q` | Quit the application |
| `r` | Refresh all entities |
| `t` or `Enter` | Toggle the selected entity |
| `↑` / `↓` | Navigate up/down in the entity list |
| `Tab` | Switch between tabs |
| `1` | Switch to Lights tab |
| `2` | Switch to Switches tab |
| `3` | Switch to Sensors tab |
| `4` | Switch to Climate tab |
| `5` | Switch to All entities tab |

## Toggling Entities

To toggle a light, switch, fan, or cover:

1. Navigate to the entity using arrow keys
2. Press `t` or `Enter` to toggle

The entity will be toggled and the display will refresh to show the new state.

## Auto-Refresh

HATUI automatically refreshes entity states every 30 seconds. You can also manually refresh by pressing `r`.

## Running Over SSH

HATUI works great over SSH connections:

```bash
ssh user@server
hatui
```

It also works inside `tmux` and `screen` sessions, making it perfect for persistent dashboards.
