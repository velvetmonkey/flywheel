# Installation Guide

Platform-specific installation instructions for Flywheel Plugin.

## Prerequisites

### All Platforms

1. **Python 3.8+** installed and available as `python3` in PATH
2. **Claude Code** installed with plugin support

### Windows

Ensure Python is installed and added to PATH during installation.

**Verify installation:**
```powershell
python3 --version
# Should show: Python 3.x.x
```

### macOS

Python 3 should be available. If not:

```bash
brew install python
```

---

## Quick Install (Recommended)

### Step 1: Configure Flywheel MCP Server

Add to `.mcp.json` in your vault (or `~/.claude.json` for user-level):

**macOS/Linux/WSL:**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/path/to/your/vault"
      }
    }
  }
}
```

**Windows (requires `cmd /c` wrapper):**
```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "C:/path/to/your/vault"
      }
    }
  }
}
```

### Step 2: Install the Plugin

In Claude Code, run these commands:

```
/plugin marketplace add bencassie/flywheel
/plugin install flywheel@bencassie-flywheel
```

### Step 3: Create Vault Configuration (Optional)

Create `.flywheel.json` in your vault root for customization:

```json
{
  "vault_name": "My Vault",
  "paths": {
    "daily_notes": "daily-notes",
    "weekly_notes": "weekly-notes",
    "templates": "templates"
  },
  "sections": {
    "log": "## Log",
    "food": "# Food"
  }
}
```

### Step 4: Restart Claude Code

Close and reopen Claude Code to load the plugin.

**Verify plugin loaded:**
- On session start, you should see the Flywheel briefing
- Skills like `/vault-health`, `/auto-log` should be available

---

## Developer Setup (From Source)

For contributors or users who want to run from a local clone.

### Step 1: Clone the Repository

```bash
git clone https://github.com/bencassie/flywheel.git
```

Note your plugin path:
- **WSL**: `/mnt/c/Users/YOUR_USER/src/flywheel/packages/claude-plugin`
- **Windows**: `C:/Users/YOUR_USER/src/flywheel/packages/claude-plugin`
- **macOS/Linux**: `~/src/flywheel/packages/claude-plugin`

### Step 2: Configure Claude Code Settings

Add the plugin to your Claude Code settings file.

**WSL** - Edit `~/.claude.json`:
```json
{
  "extraKnownMarketplaces": {
    "flywheel": {
      "source": {
        "source": "directory",
        "path": "/mnt/c/Users/YOUR_USER/src/flywheel/packages/claude-plugin"
      }
    }
  },
  "enabledPlugins": {
    "flywheel@bencassie-flywheel": true
  }
}
```

**Windows** - Edit `C:\Users\YOUR_USER\.claude.json`:
```json
{
  "extraKnownMarketplaces": {
    "flywheel": {
      "source": {
        "source": "directory",
        "path": "C:/Users/YOUR_USER/src/flywheel/packages/claude-plugin"
      }
    }
  },
  "enabledPlugins": {
    "flywheel@bencassie-flywheel": true
  }
}
```

**macOS/Linux** - Edit `~/.claude.json`:
```json
{
  "extraKnownMarketplaces": {
    "flywheel": {
      "source": {
        "source": "directory",
        "path": "/Users/YOUR_USER/src/flywheel/packages/claude-plugin"
      }
    }
  },
  "enabledPlugins": {
    "flywheel@bencassie-flywheel": true
  }
}
```

### Step 3: Configure MCP Server

Follow the MCP configuration in Quick Install Step 1 above.

### Step 4: Restart Claude Code

---

## Dual WSL/Windows Setup

For developers working on both WSL and Windows:

| File | Purpose | Path Format | Committed? |
|------|---------|-------------|------------|
| `.claude/settings.json` | Universal baseline | WSL (`/mnt/c/...`) | Yes (git) |
| `~/.claude.json` projects override | Windows-specific | Windows (`C:\...`) | No (local) |

### How It Works

**On WSL:**
- Uses `.claude/settings.json` directly with `/mnt/c/...` paths
- WSL natively resolves these paths

**On Windows:**
- Loads `.claude/settings.json` (WSL paths don't work)
- User-level `~/.claude.json` provides Windows path override via `projects` section

### Configuration Example

**`C:\Users\YOUR_USER\.claude.json` (Windows user config):**
```json
{
  "projects": {
    "C:\\Users\\YOUR_USER\\obsidian\\YOUR_VAULT": {
      "extraKnownMarketplaces": {
        "flywheel": {
          "source": {
            "source": "directory",
            "path": "C:/Users/YOUR_USER/src/flywheel/packages/claude-plugin"
          }
        }
      },
      "mcpServers": {
        "flywheel": {
          "command": "cmd",
          "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
          "env": { "PROJECT_PATH": "C:/Users/YOUR_USER/obsidian/YOUR_VAULT" }
        }
      }
    }
  }
}
```

**IMPORTANT:** Project keys must use **backslashes** (`C:\Users\...`) for matching.

---

## Installing Rules (Optional)

Claude Code plugins cannot bundle rules - copy to your vault's `.claude/rules/` directory.

See [rules.md](rules.md) for available rules:

| Rule | Purpose |
|------|---------|
| `obsidian-syntax.md` | Prevents angle brackets, wrapped wikilinks |
| `daily-notes.md` | Enforces daily note structure |
| `folder-organization.md` | Protects folder hierarchy |

---

## Troubleshooting

### Hooks not running

1. **Check Python**: Run `python3 --version` - should show Python 3.x
2. **Check paths**: Verify plugin path exists and is accessible

### Plugin not loading

1. **Check settings file**: Ensure JSON is valid (no trailing commas)
2. **Check path format**: Use forward slashes even on Windows (`C:/Users/...`)
3. **Restart Claude Code**: Plugins load on startup

### Skills not available

1. **Check marketplace**: Run `/plugin` to verify flywheel is installed
2. **Check `enabledPlugins`**: Must include `"flywheel@bencassie-flywheel": true`

### Flywheel MCP not connecting

1. **Check PROJECT_PATH**: Must point to your vault root
2. **Windows users**: Use `cmd /c npx` wrapper, not direct `npx`
3. **Run `claude mcp list`**: Verify server shows as connected

---

## Uninstallation

**Marketplace install:**
```
/plugin uninstall flywheel@bencassie-flywheel
/plugin marketplace remove flywheel
```

**Directory install:**
1. Remove `extraKnownMarketplaces` and `enabledPlugins` entries from settings
2. Delete `.flywheel.json` from vault (optional)
3. Restart Claude Code
