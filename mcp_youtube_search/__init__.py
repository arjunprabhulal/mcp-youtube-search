"""MCP server that searches YouTube through SerpApi."""

from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version("mcp-youtube-search")
except PackageNotFoundError:  # running from a source checkout
    __version__ = "0.0.0"
