import pytest

from mcp_youtube_search import youtube
from mcp_youtube_search.youtube import YouTubeSearchError, format_videos, search_params

SAMPLE = {
    "video_results": [
        {
            "title": "Intro to MCP",
            "link": "https://youtube.com/watch?v=1",
            "channel": {"name": "AI Lab"},
            "views": 1200,
            "published_date": "2 weeks ago",
            "length": "12:34",
            "thumbnail": {"static": "https://i.ytimg.com/1.jpg"},
            "description": "MCP basics",
        },
        {"title": "Second", "link": "https://youtube.com/watch?v=2"},
    ]
}


def test_params_have_no_key():
    params = search_params(" mcp servers ", "en", "us")
    assert params == {"engine": "youtube", "search_query": "mcp servers", "hl": "en", "gl": "us"}


def test_format_videos():
    videos = format_videos(SAMPLE)
    assert videos[0].channel == "AI Lab" and videos[0].views == "1200" and videos[0].duration == "12:34"
    assert videos[1].channel == "Unknown channel" and videos[1].thumbnail is None
    assert len(format_videos(SAMPLE, max_results=1)) == 1 and format_videos({}) == []


async def test_missing_key(monkeypatch):
    monkeypatch.delenv("SERP_API_KEY", raising=False)
    with pytest.raises(YouTubeSearchError, match="SERP_API_KEY"):
        await youtube.search_youtube("mcp")


async def test_search_never_logs_the_key(monkeypatch, caplog):
    monkeypatch.setenv("SERP_API_KEY", "secret-key")
    monkeypatch.setattr(youtube, "_search", lambda params, key: SAMPLE)
    caplog.set_level("DEBUG")
    assert len(await youtube.search_youtube("mcp")) == 2
    assert "secret-key" not in caplog.text


async def test_serpapi_error(monkeypatch):
    monkeypatch.setenv("SERP_API_KEY", "k")
    monkeypatch.setattr(youtube, "_search", lambda params, key: {"error": "Invalid API key."})
    with pytest.raises(YouTubeSearchError, match="Invalid API key"):
        await youtube.search_youtube("mcp")
