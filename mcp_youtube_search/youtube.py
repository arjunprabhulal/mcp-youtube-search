"""YouTube search through the SerpApi YouTube engine."""

from __future__ import annotations

import asyncio
import logging
import os
from typing import Any

import serpapi
from mcp.server.mcpserver.exceptions import ToolError
from pydantic import BaseModel, Field

logger = logging.getLogger("mcp_youtube_search")

API_KEY_ENV = "SERP_API_KEY"


class Video(BaseModel):
    """One video from YouTube's search results."""

    title: str
    link: str
    channel: str
    views: str = Field(description="View count as YouTube shows it, or Unknown")
    published_date: str = Field(description="Relative date as YouTube shows it, such as '2 weeks ago'")
    duration: str = Field(description="Length, such as '12:34'")
    thumbnail: str | None = None
    description: str | None = None


class YouTubeSearchError(ToolError):
    """The search couldn't run or SerpApi refused it: reported to the model as a tool error with this message."""


def api_key() -> str:
    key = os.environ.get(API_KEY_ENV, "").strip()
    if not key:
        raise YouTubeSearchError(f"Set {API_KEY_ENV} to your SerpApi key (serpapi.com) to search YouTube.")
    return key


def search_params(query: str, language: str = "en", country: str = "us") -> dict[str, Any]:
    return {"engine": "youtube", "search_query": query.strip(), "hl": language, "gl": country}


def format_videos(results: dict[str, Any], max_results: int = 10) -> list[Video]:
    videos = []
    for item in (results.get("video_results") or [])[:max_results]:
        channel = item.get("channel") or {}
        thumbnail = item.get("thumbnail") or {}
        videos.append(
            Video(
                title=item.get("title", "Unknown"),
                link=item.get("link", ""),
                channel=channel.get("name", "Unknown channel") if isinstance(channel, dict) else str(channel),
                views=str(item.get("views", "Unknown")),
                published_date=item.get("published_date", "Unknown"),
                duration=item.get("length", "Unknown"),
                thumbnail=(thumbnail.get("static") if isinstance(thumbnail, dict) else thumbnail) or None,
                description=item.get("description") or None,
            )
        )
    return videos


def _search(params: dict[str, Any], key: str) -> dict[str, Any]:
    try:
        return dict(serpapi.Client(api_key=key).search(params))
    except serpapi.SerpApiError as error:
        raise YouTubeSearchError(f"SerpApi: {error}") from error


async def search_youtube(query: str, max_results: int = 10, language: str = "en", country: str = "us") -> list[Video]:
    """Search YouTube. The API key is never logged."""
    if not query.strip():
        raise YouTubeSearchError("Give a search query.")
    key = api_key()
    logger.info("Searching YouTube for %r", query)
    results = await asyncio.to_thread(_search, search_params(query, language, country), key)
    if results.get("error"):
        raise YouTubeSearchError(f"SerpApi: {results['error']}")
    return format_videos(results, max_results)
