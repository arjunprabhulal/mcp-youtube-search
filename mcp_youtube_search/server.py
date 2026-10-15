"""MCP server and command line for YouTube search."""

from __future__ import annotations

import argparse
import asyncio
import logging
import os
import sys
from typing import Annotated

from dotenv import load_dotenv
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations
from pydantic import Field

from mcp_youtube_search import __version__
from mcp_youtube_search.youtube import Video, YouTubeSearchError, search_youtube


def create_server() -> MCPServer:
    server = MCPServer(
        "mcp-youtube-search",
        title="YouTube Search",
        description="Search YouTube videos through SerpApi.",
        version=__version__,
        instructions="Use search_youtube to find videos. Needs SERP_API_KEY.",
    )

    @server.tool(
        name="search_youtube", title="Search YouTube", annotations=ToolAnnotations(read_only_hint=True, open_world_hint=True)
    )
    async def search_youtube_tool(
        query: Annotated[str, Field(min_length=1, description="What to search for")],
        max_results: Annotated[int, Field(ge=1, le=50, description="How many videos to return (1-50)")] = 10,
        language: Annotated[str, Field(description="Interface language code, such as en")] = "en",
        country: Annotated[str, Field(description="Country code, such as us")] = "us",
    ) -> list[Video]:
        """Search YouTube for videos: title, link, channel, views, publish date, duration and description."""
        return await search_youtube(query, max_results, language, country)

    return server


def main() -> None:
    load_dotenv()
    parser = argparse.ArgumentParser(prog="mcp-youtube-search", description="YouTube search MCP server (SerpApi)")
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command")
    serve = sub.add_parser("server", help="Run the MCP server (the default)")
    serve.add_argument("--connection_type", choices=["stdio", "http"], default="stdio")
    serve.add_argument("--host", default="127.0.0.1")
    serve.add_argument("--port", type=int, default=3002)
    search = sub.add_parser("search", help="Search from the command line")
    search.add_argument("query")
    search.add_argument("--max-results", type=int, default=10)
    search.add_argument("--language", default="en")
    search.add_argument("--country", default="us")
    args = parser.parse_args()
    # Logs go to stderr: in stdio mode stdout carries the MCP messages.
    level = os.environ.get("LOG_LEVEL", "INFO").upper()
    logging.basicConfig(stream=sys.stderr, level=level, format="%(levelname)s %(name)s: %(message)s")

    if args.command == "search":
        try:
            videos = asyncio.run(search_youtube(args.query, args.max_results, args.language, args.country))
        except YouTubeSearchError as error:
            sys.exit(str(error))
        for number, video in enumerate(videos, 1):
            print(f"{number}. {video.title}")
            print(f"   {video.channel} | {video.duration} | {video.views} | {video.published_date}\n   {video.link}")
        return

    server = create_server()
    if getattr(args, "connection_type", "stdio") == "http":
        server.run("streamable-http", host=args.host, port=args.port)
    else:
        server.run("stdio")


if __name__ == "__main__":
    main()
