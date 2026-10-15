# Changelog

## 0.2.0

- Works with the current MCP Python SDK (2.x) and the official `serpapi` client: 0.1.x imported `GoogleSearch`, which the declared `serpapi` package doesn't have, and depended on Google ADK only to build one schema.
- One tool, `search_youtube`, with validated inputs, structured results and read-only annotations; a missing key or a SerpApi error comes back to the model as a clear tool error.
- `mcp-youtube-search server` no longer prints to stdout, which carries the stdio protocol; logs go to stderr and never include the API key. `--connection_type http` serves Streamable HTTP.
- Python 3.10 or later, `pyproject` with uv, bounded dependencies; build output and egg-info removed from the repository.
- Tests, CI on Python 3.10 to 3.14, trusted publishing to PyPI, and an MCP Registry entry.
