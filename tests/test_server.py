from mcp.client import Client

from mcp_youtube_search import youtube
from mcp_youtube_search.server import create_server
from tests.test_youtube import SAMPLE


async def test_tool_is_listed_with_schemas():
    async with Client(create_server()) as client:
        tools = {tool.name: tool for tool in (await client.list_tools()).tools}
    assert set(tools) == {"search_youtube"}
    assert tools["search_youtube"].input_schema["required"] == ["query"]
    assert tools["search_youtube"].annotations.read_only_hint is True


async def test_search_returns_structured_videos(monkeypatch):
    monkeypatch.setenv("SERP_API_KEY", "k")
    monkeypatch.setattr(youtube, "_search", lambda params, key: SAMPLE)
    async with Client(create_server()) as client:
        result = await client.call_tool("search_youtube", {"query": "mcp", "max_results": 1})
    assert not result.is_error and len(result.structured_content["result"]) == 1


async def test_missing_key_is_a_tool_error(monkeypatch):
    monkeypatch.delenv("SERP_API_KEY", raising=False)
    async with Client(create_server()) as client:
        result = await client.call_tool("search_youtube", {"query": "mcp"})
    assert result.is_error and "SERP_API_KEY" in result.content[0].text
