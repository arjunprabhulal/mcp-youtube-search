# MCP YouTube Search

<!-- mcp-name: io.github.arjunprabhulal/mcp-youtube-search -->

An MCP server that searches YouTube through [SerpApi](https://serpapi.com/youtube-search-api), for Claude, Cursor and other MCP clients: titles, links, channels, views, publish dates, durations and descriptions.

[![CI](https://github.com/arjunprabhulal/mcp-youtube-search/actions/workflows/ci.yml/badge.svg)](https://github.com/arjunprabhulal/mcp-youtube-search/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/mcp-youtube-search)](https://pypi.org/project/mcp-youtube-search/)

## Requirements

- Python 3.10 or later (or [uv](https://docs.astral.sh/uv/))
- A SerpApi key in `SERP_API_KEY` (serpapi.com has a free tier)

## Use it from an MCP client

```json
{
  "mcpServers": {
    "youtube-search": {
      "command": "uvx",
      "args": ["mcp-youtube-search", "server"],
      "env": { "SERP_API_KEY": "your-serpapi-key" }
    }
  }
}
```

Or `pip install mcp-youtube-search` and use `"command": "mcp-youtube-search", "args": ["server"]`.

## Command line

```bash
export SERP_API_KEY="your-serpapi-key"
mcp-youtube-search search "model context protocol" --max-results 5
mcp-youtube-search server                                      # MCP over stdio
mcp-youtube-search server --connection_type http --port 3002   # Streamable HTTP at http://127.0.0.1:3002/mcp
```

`LOG_LEVEL=DEBUG` shows more detail on stderr. The API key is never logged.

## Tool

| Tool | What it does |
| --- | --- |
| `search_youtube` | Videos for a query. `query`; optional `max_results` (1-50, default 10), `language` (default `en`), `country` (default `us`). Returns structured results: title, link, channel, views, publish date, duration, thumbnail, description. |

## Development

```bash
uv sync
uv run pytest
uv run ruff check .
```

## License

MIT
