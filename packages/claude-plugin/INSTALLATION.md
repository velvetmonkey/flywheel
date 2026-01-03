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

## Step 1: Clone or Download the Plugin

```bash
# Clone the repository
git clone https://github.com/bencassie/flywheel.git

# Or download and extract the ZIP from GitHub
```

Note your plugin path:
- **WSL**: `/mnt/c/Users/YOUR_USER/src/flywheel/packages/claude-plugin`
- **Windows**: `C:/Users/YOUR_USER/src/flywheel/packages/claude-plugin`
- **macOS/Linux**: `~/src/flywheel/packages/claude-plugin`

---

## Step 2: Configure Claude Code Settings

Add the plugin to your Claude Code settings file.

### WSL Configuration

Edit `~/.claude.json` or your project's `.claude/settings.local.json`:

```json
{
  "extraKnownMarketplaces": {
    "flywheel": {
      "source": {
        "source": "directory",
        "path": "/mnt/c/Users/YOUR_USER/src/flywheel/plugins/flywheel"
      }
    }
  },
  "enabledPlugins": {
    "flywheel@flywheel": true
  }
}
```

### Windows Configuration

Edit `C:\Users\YOUR_USER\.claude.json` or your project's `.claude\settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "flywheel": {
      "source": {
        "source": "directory",
        "path": "C:/Users/YOUR_USER/src/flywheel/plugins/flywheel"
      }
    }
  },
  "enabledPlugins": {
    "flywheel@flywheel": true
  }
}
```

### macOS/Linux Configuration

Edit `~/.claude.json` or your project's `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "flywheel": {
      "source": {
        "source": "directory",
        "path": "/Users/YOUR_USER/src/flywheel/plugins/flywheel"
      }
    }
  },
  "enabledPlugins": {
    "flywheel@flywheel": true
  }
}
```

---

## Step 3: Create Vault Configuration

Create `.flywheel.json` in your Obsidian vault root:

```json
{
  "$schema": "./plugins/flywheel/config/config-schema.json",
  "vault_name": "My Vault",
  "paths": {
    "daily_notes": "daily-notes",
    "weekly_notes": "weekly-notes",
    "monthly_notes": "monthly-notes",
    "quarterly_notes": "quarterly-notes",
    "yearly_notes": "yearly-notes",
    "templates": "templates",
    "achievements": "personal/goals/Achievements.md"
  },
  "sections": {
    "log": "## Log",
    "food": "# Food",
    "habits": "# Habits"
  }
}
```

Adjust paths to match your vault structure.

---

## Step 4: Install Rules

Claude Code plugins cannot bundle rules - they must be copied to your vault's `.claude/rules/` directory.

```bash
# Create rules directory
mkdir -p /path/to/vault/.claude/rules

# Copy rule documentation (see rules.md for full content)
```

**Required rules** (see [rules.md](rules.md) for complete files):

| Rule | Purpose |
|------|---------|
| `obsidian-syntax.md` | Prevents angle brackets, wrapped wikilinks |
| `daily-notes.md` | Enforces daily note structure |
| `folder-organization.md` | Protects folder hierarchy |
| `platform-requirements.md` | WSL/Windows setup docs |

---

## Step 5: Restart Claude Code

Close and reopen Claude Code (or start a new session) to load the plugin.

**Verify plugin loaded:**
- On session start, you should see the Flywheel briefing
- Skills like `food`, `rebuild-wikilink-cache` should be available

Continue to Step 6 to install the required smoking-mirror MCP server.

---

## Step 6: Install Flywheel MCP (Required)

The Flywheel MCP server is **required** for vault intelligence, wikilink cache, and entity detection.

### WSL Configuration

Add to `.mcp.json` in your vault:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "/mnt/c/Users/YOUR_USER/obsidian/YOUR_VAULT"
      }
    }
  }
}
```

### Windows Configuration

Add to `.mcp.json` in your vault (note the `cmd /c` wrapper):

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "cmd",
      "args": ["/c", "npx", "-y", "@bencassie/flywheel-mcp"],
      "env": {
        "PROJECT_PATH": "C:/Users/YOUR_USER/obsidian/YOUR_VAULT"
      }
    }
  }
}
```

---

## Dual WSL/Windows Setup

The correct multi-platform architecture:

| File | Purpose | Path Format | Committed? |
|------|---------|-------------|------------|
| `.claude/settings.json` | Universal baseline | WSL (`/mnt/c/...`) | Yes (git) |
| `~/.claude.json` projects override | Windows-specific | Windows (`C:\...`) | No (local) |

### How It Works

**On WSL:**
- Uses `.claude/settings.json` directly with `/mnt/c/...` paths
- WSL natively resolves these paths
- No user-level override needed

**On Windows:**
- Loads `.claude/settings.json` (WSL paths don't work on Windows)
- User-level `~/.claude.json` provides Windows path override via `projects` section
- Override takes precedence, allowing plugins to load

### Configuration Examples

**`.claude/settings.json` (committed to git):**
```json
{
  "extraKnownMarketplaces": {
    "flywheel": {
      "source": {
        "source": "directory",
        "path": "/mnt/c/Users/YOUR_USER/src/flywheel"
      }
    }
  },
  "enabledPlugins": {
    "flywheel@flywheel": true
  }
}
```

**`C:\Users\YOUR_USER\.claude.json` (Windows user config - NOT committed):**
```json
{
  "mcpServers": { /* user-level servers */ },
  "projects": {
    "C:\Users\YOUR_USER\obsidian\YOUR_VAULT": {
      "extraKnownMarketplaces": {
        "flywheel": {
          "source": {
            "source": "directory",
            "path": "C:/Users/YOUR_USER/src/flywheel/plugins/flywheel/plugins/flywheel"
          }
        }
      },
      "mcpServers": {
        "smoking-mirror": {
          "command": "cmd",
          "args": ["/c", "npx", "-y", "smoking-mirror@latest"],
          "env": { "OBSIDIAN_VAULT_PATH": "C:/Users/YOUR_USER/obsidian/YOUR_VAULT" }
        }
      }
    }
  }
}
```

**IMPORTANT:** Project keys in Windows user config must use **backslashes** (`C:\Users\...`) for proper matching.

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

1. **Check `enabledPlugins`**: Must include `"flywheel@flywheel": true`
2. **Check plugin structure**: `skills/` directory must exist with skill folders

### Flywheel MCP not connecting

1. **Check PROJECT_PATH**: Must point to your vault root
2. **Windows users**: Use `cmd /c npx` wrapper, not direct `npx`
3. **Run `claude mcp list`**: Verify server shows as connected

---

## Uninstallation

1. Remove `extraKnownMarketplaces` and `enabledPlugins` entries from settings
2. Delete `.flywheel.json` from vault (optional - keeps your config)
3. Delete the plugin directory (optional)
4. Restart Claude Code
