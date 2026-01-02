# Contributing to smoking-mirror

Thanks for your interest in contributing! Here's how to help.

## Development Setup

```bash
# Clone the repo
git clone https://github.com/bencassie/smoking-mirror.git
cd smoking-mirror

# Install dependencies
bun install

# Run in development mode (requires a vault)
OBSIDIAN_VAULT_PATH=/path/to/your/vault bun run dev

# Run tests
bun test

# Type check
npx tsc --noEmit

# Build for distribution
bun run build
```

## Testing with MCP Inspector

```bash
npx @modelcontextprotocol/inspector npx tsx src/index.ts
```

This opens an interactive UI to test tools against your vault.

## Pull Request Guidelines

1. **Run tests** before submitting: `bun test`
2. **Type check**: `npx tsc --noEmit`
3. **Add tests** for new tools
4. **Update README** tool tables if adding new tools
5. **Keep PRs focused** - one feature or fix per PR

## Adding New Tools

1. Create or update the appropriate file in `src/tools/`
2. Register the tool in `src/index.ts`
3. Add an entry to the README tool table
4. Write tests in `test/`

## Code Style

- TypeScript with strict mode
- Use Zod for input validation
- Return structured data, not content (privacy by design)
- Descriptive tool names with `get_`, `find_`, `search_` prefixes

## Ideas Welcome

- Open an issue to discuss before starting large PRs
- Feature requests: tag with `enhancement`
- Bug reports: include vault size and reproduction steps

## Questions?

Open an issue or reach out via GitHub discussions.
