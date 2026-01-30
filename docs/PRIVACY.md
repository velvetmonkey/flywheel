# Flywheel Privacy Guide

Understanding what data Flywheel accesses, indexes, and exposes to AI agents.

---

## Table of Contents

- [Privacy Summary](#privacy-summary)
- [What Leaves Localhost](#what-leaves-localhost)
- [What Gets Indexed](#what-gets-indexed)
- [What Stays Private](#what-stays-private)
- [Data Flow](#data-flow)
- [Exclusion Patterns](#exclusion-patterns)
- [Sensitive Data Handling](#sensitive-data-handling)
- [Network Calls Inventory](#network-calls-inventory)
- [Best Practices](#best-practices)

---

## Privacy Summary

**In plain terms:**

1. ✅ **Flywheel runs entirely on YOUR machine** - no cloud servers
2. ✅ **Your vault files stay on your disk** - never uploaded anywhere
3. ✅ **Index contains structure, not prose** - titles, links, tags (not content)
4. ⚠️ **Tool responses ARE sent to Claude's API** - via MCP protocol
5. ✅ **No telemetry or analytics** - zero phone-home

**Key insight:** Flywheel minimizes what AI agents see, but doesn't prevent data from reaching Claude. It's a filter, not a firewall.

---

## What Leaves Localhost

### Direct File Access (Without Flywheel)

When Claude reads your vault directly:

```
You: "Find all mentions of Project Alpha"

Claude: Reads 5,000 notes, one by one
→ ~5,000,000 tokens sent to Claude API
→ Full file contents of your entire vault exposed
```

---

### With Flywheel (Filtered Access)

```
You: "What links to Project Alpha?"

Claude: Calls get_backlinks("Project Alpha")
Flywheel: Returns ["meeting.md", "tasks.md", "notes.md"]
→ ~50 tokens sent to Claude API
→ Only file NAMES exposed, not content
```

**Structure queries send only metadata, not file content.**

---

### What Tool Responses Contain

| Tool | Data Returned | Privacy Impact |
|------|---------------|----------------|
| `get_backlinks` | File paths | **Low** (structure only) |
| `search_notes` | File paths + snippets | **Medium** (excerpts visible) |
| `get_section_content` | Section text | **High** (content visible) |
| `query_notes` | Frontmatter values | **Medium** (metadata visible) |
| `get_vault_stats` | Counts, no content | **Low** (statistics only) |

**Principle:** Graph queries expose less data than content queries.

---

## What Gets Indexed

### Indexed (In-Memory Structure)

Flywheel builds an index of vault structure:

| Data Type | Example | Purpose |
|-----------|---------|---------|
| **File paths** | `notes/project-alpha.md` | Navigation |
| **Titles** | "Project Alpha" | Entity matching |
| **Aliases** | `aliases: [PA, Alpha Project]` | Alternative names |
| **Wikilinks** | `[[Meeting Notes]]` | Graph queries |
| **Tags** | `#project`, `#active` | Filtering |
| **Frontmatter keys** | `status`, `priority` | Schema |
| **Frontmatter values** | `status: active` | Queries |
| **Headings** | `## Tasks`, `## Log` | Section nav |
| **Modification dates** | `2026-01-29` | Temporal queries |
| **File sizes** | 12,345 bytes | Statistics |

**Storage:** In-memory only (not persisted to disk, except entity cache).

---

### NOT Indexed (Stays on Disk)

| Data Type | Reason |
|-----------|--------|
| **File content/prose** | Privacy - only read on demand |
| **Code blocks** | Not relevant to graph |
| **Images** | Not indexed |
| **PDFs** | Not scanned |
| **Task content** | Only checkbox state indexed |
| **Inline content** | Only when explicitly requested |

**Exception:** `search_notes` with content query will read file contents on demand.

---

## What Stays Private

### Files Never Sent to AI

1. **Excluded folders** (see [Exclusion Patterns](#exclusion-patterns))
2. **Non-markdown files** (`.pdf`, `.png`, etc.)
3. **Hidden files** (`.git/`, `.obsidian/`)
4. **Files not queried** (if you don't ask about them, Claude never sees them)

---

### Content Only Sent on Demand

**Example:**
```
Query: "What are my hub notes?"
→ Flywheel returns: ["note1.md", "note2.md", "note3.md"]
→ File CONTENTS not sent to Claude

Query: "Show me the content of note1.md"
→ Flywheel returns: Full file content
→ NOW content is sent to Claude
```

**You control what Claude sees by what you query.**

---

## Data Flow

### Query Flow

```
┌──────────────┐
│ You (User)   │
└──────┬───────┘
       │
       │ "What links to [[Project Alpha]]?"
       ▼
┌──────────────┐
│ Claude Code  │
└──────┬───────┘
       │
       │ MCP: get_backlinks({target: "Project Alpha"})
       ▼
┌──────────────┐
│  Flywheel    │  ← Runs on YOUR machine
│   (Local)    │
└──────┬───────┘
       │
       │ Query in-memory index
       ▼
┌──────────────┐
│  Index       │  ← In memory (not on Claude's servers)
│ (Structure)  │
└──────┬───────┘
       │
       │ Return: ["meeting.md", "tasks.md"]
       ▼
┌──────────────┐
│ Claude Code  │
└──────┬───────┘
       │
       │ Response sent to Claude API
       ▼
┌──────────────┐
│ Claude API   │  ⚠️ Now Claude has file names
│ (Anthropic)  │
└──────────────┘
```

**Key points:**
1. Flywheel runs locally
2. Index queries don't access files
3. Only query RESULTS sent to Claude
4. Claude API receives minimal data

---

## Exclusion Patterns

### Excluding Sensitive Folders

Configure Flywheel to ignore folders:

```json
{
  "mcpServers": {
    "flywheel": {
      "command": "npx",
      "args": ["-y", "@velvetmonkey/flywheel-mcp"],
      "env": {
        "FLYWHEEL_EXCLUDE_PATTERNS": "_private/,secrets/,work-confidential/"
      }
    }
  }
}
```

**Effect:**
- Files in these folders NOT indexed
- AI agents can't query them (they don't know they exist)
- Still accessible via direct file reads (if agent knows path)

---

### Pattern Syntax

Comma-separated folder names:

```
"_private/,archive/,templates/"
```

**Matches:**
- `_private/secret-note.md` ✅ Excluded
- `notes/_private/secret.md` ✅ Excluded (any depth)
- `archive/old-notes.md` ✅ Excluded

**Doesn't match:**
- `notes/private-project.md` ❌ Not excluded (doesn't contain `_private/` as folder)

---

### Recommended Exclusions

```json
{
  "FLYWHEEL_EXCLUDE_PATTERNS": "_private/,secrets/,archive/,templates/,.trash/"
}
```

**Why:**
- `_private/`: Sensitive personal notes
- `secrets/`: Passwords, API keys (shouldn't be in vault, but just in case)
- `archive/`: Old notes not relevant to AI queries
- `templates/`: Template files (not real notes)
- `.trash/`: Deleted notes

---

## Sensitive Data Handling

### API Keys & Passwords

**❌ Don't store in vault:**
```yaml
---
api_key: <REDACTED>             ← BAD
password: hunter2             ← BAD
---
```

**Why:**
- If indexed, could be returned in frontmatter queries
- If queried, sent to Claude API
- Security risk

**✅ Use environment variables or secure credential managers instead.**

---

### Personal Information

**Examples:**
- Social Security Numbers
- Credit card numbers
- Medical records
- Legal documents

**Recommendations:**
1. **Keep outside vault** (use encrypted storage)
2. **Use `_private/` folder** (excluded from indexing)
3. **Avoid frontmatter** (easily queryable)

---

### Encrypted Vaults

**Scenario:** Vault is encrypted at rest (e.g., VeraCrypt, FileVault).

**Compatibility:**
- ✅ Flywheel works (accesses decrypted files)
- ✅ Index in memory (not persisted to disk unencrypted)
- ⚠️ Entity cache written to `.claude/wikilink-entities.json` (unencrypted)

**Entity cache privacy:**
- Contains: Note titles and aliases
- Doesn't contain: File contents or sensitive data
- Stored in vault (inherits vault encryption if encrypted)

**If paranoid:** Delete entity cache after use:
```bash
rm -rf /vault/.claude/wikilink-entities.json
```
(Will be regenerated on next server start)

---

## Network Calls Inventory

### Flywheel's Network Activity

**Outbound calls:**
- ❌ **NONE** - Flywheel makes zero network requests

**Inbound calls:**
- ✅ **MCP protocol** from Claude Code (local socket, not internet)

**npm package installation:**
- ✅ `npx @velvetmonkey/flywheel-mcp` downloads from npm registry
- ⚠️ Only during installation, not during use
- ✅ Standard npm packages (auditable)

---

### Claude Code's Network Activity

**When using Flywheel:**
- ✅ MCP requests to Flywheel (local only)
- ⚠️ Sends tool responses to Claude API (api.anthropic.com)

**What goes to Anthropic:**
- Your prompts
- Tool names and parameters
- Tool responses (Flywheel's query results)

**What doesn't go to Anthropic:**
- Your vault files (unless tool response includes content)
- Flywheel's index structure
- Your filesystem

See [Anthropic's Privacy Policy](https://www.anthropic.com/legal/privacy) for how they handle data.

---

## Best Practices

### 1. Use Graph Queries Over Content Queries

**Minimize data exposure:**

❌ **High exposure:**
```
"Search all notes for mentions of Project Alpha"
→ search_notes("Project Alpha")
→ Returns file contents with snippets
```

✅ **Low exposure:**
```
"What notes link to Project Alpha?"
→ get_backlinks("Project Alpha")
→ Returns only file names
```

---

### 2. Exclude Sensitive Folders

```json
{
  "FLYWHEEL_EXCLUDE_PATTERNS": "_private/,secrets/,work-confidential/"
}
```

**Effect:** AI can't query what it doesn't know exists.

---

### 3. Review Tool Responses

Claude Code shows tool responses in the conversation:

```
Tool: get_backlinks
Response: ["meeting.md", "tasks.md"]
```

**You can see what data was sent to Claude API.**

---

### 4. Use Section Queries, Not Full File Reads

❌ **High exposure:**
```
"Show me the content of daily-notes.md"
→ Returns entire file (~5,000 tokens)
```

✅ **Low exposure:**
```
"Show me the Log section from daily-notes.md"
→ Returns one section (~500 tokens)
```

**10x less data sent to Claude API.**

---

### 5. Don't Store Secrets in Vault

**Use secure credential managers:**
- 1Password, Bitwarden, etc.
- Environment variables
- OS keychain

**Not frontmatter in Obsidian.**

---

### 6. Audit Tool Usage

Review what tools your AI agent uses:

```
Debug logs:
flywheel:query get_backlinks("Project Alpha")
flywheel:query search_notes("confidential")  ← 🚨 Review this
```

**If agent searches for "confidential" unexpectedly, investigate why.**

---

## Privacy Comparison

### Flywheel vs. Direct File Access

| Aspect | Direct File Access | With Flywheel |
|--------|-------------------|---------------|
| **Data sent to Claude** | Full file contents | Metadata/excerpts |
| **Tokens per query** | ~5,000 | ~50 |
| **Exposure** | High | Low |
| **Control** | Low | Medium |
| **Audit** | Hard | Easy (tool responses visible) |

**Flywheel significantly reduces data exposure, but doesn't eliminate it.**

---

### Flywheel vs. Dataview (Obsidian Plugin)

| Aspect | Dataview | Flywheel |
|--------|----------|----------|
| **Runs where** | Inside Obsidian | Local (MCP) |
| **Data sent to cloud** | Never | Tool responses to Claude API |
| **Privacy** | Perfect (local only) | Good (minimal exposure) |

**Dataview is more private (never leaves machine).**

**Flywheel is AI-native (works with Claude Code).**

---

## Threat Model

### What Flywheel Protects Against

✅ **Bulk file reads:** Prevents Claude from reading entire vault
✅ **Token waste:** Reduces data sent to API (cost + privacy)
✅ **Accidental exposure:** Graph queries don't expose content

---

### What Flywheel Does NOT Protect Against

❌ **Intentional content reads:** If you ask "Show me note.md", content is sent
❌ **Claude API access:** Tool responses go to Anthropic
❌ **Malicious agents:** A rogue AI could still query sensitive data (if indexed)

**Flywheel is a filter, not a firewall.**

---

## Summary

**Privacy characteristics:**

1. **Local-first:** Runs on your machine, no cloud servers
2. **Minimal exposure:** Graph queries return metadata, not content
3. **User control:** You choose what to query
4. **Transparent:** Tool responses are visible
5. **No telemetry:** No analytics or tracking

**Honest limitations:**

1. Tool responses ARE sent to Claude API
2. Content queries expose file contents
3. Can't prevent malicious/accidental queries

**Best approach:**

- Use Flywheel for graph queries (low exposure)
- Use exclusion patterns for sensitive folders
- Review tool responses to see what Claude sees
- Don't store secrets in vault (use credential managers)

**Privacy is a spectrum.** Flywheel significantly reduces data exposure compared to direct file access, but doesn't make your vault invisible to AI agents.

---

## See Also

- [Configuration](./CONFIGURATION.md) - Exclusion patterns
- [Query Guide](./QUERY_GUIDE.md) - Choosing low-exposure queries
- [Comparison](./COMPARISON.md) - vs. Dataview, direct file access
- [Anthropic Privacy Policy](https://www.anthropic.com/legal/privacy)
