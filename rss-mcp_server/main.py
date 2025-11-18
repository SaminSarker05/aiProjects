"""
RSS Feed Search MCP Server

The server provides tools to search and fetch entries from RSS feeds
specifically from Google Blog Search and Google Cloud YouTube channel.

Deployed on FastMCP Cloud Platform. [Need to Fix]
https://rss-crimson-condor.fastmcp.app/mcp
"""

from mcp.server.fastmcp import FastMCP  # import official python SDK
import feedparser
import logging
import sys
import ssl
import certifi
from dataclasses import dataclass

# configure SSL and logging
ssl._create_default_https_context = ssl._create_unverified_context
logging.basicConfig(level=logging.INFO, stream=sys.stderr)

@dataclass
class RSSFeedConfig:
    name: str
    url: str
    description: str

FEEDS = {
    "google_blog": RSSFeedConfig(
        name = "Google Blog Search",
        url = "https://blog.google/rss/",
        description = "RSS feed from official Google Blog Search"
    ),
    "google_cloud_youtube": RSSFeedConfig(
        name = "Google Cloud YouTube Channel",
        url = "https://www.youtube.com/feeds/videos.xml?channel_id=UCJS9pqu9BzkAMNTmzNMNhvg",
        description = "RSS feed from Google Cloud YouTube channel"
    ),
}

mcp = FastMCP("RSSFeedSearch")

def search_feed(feed_url: str, query: str, max_results: int) -> list:
    try:
        
        feed = feedparser.parse(feed_url)
        logging.info(f"Feed bozo flag: {feed.bozo}")
        
        results = []
        query_lower = query.lower()
        for entry in feed.entries:
            title = entry.get("title", "")
            description = entry.get("description", "")

            if query_lower in title.lower() or query_lower in description.lower():
                results.append({
                    "title": title,
                    "link": entry.get("link", ""),
                    "description": description
                })
            if len(results) >= max_results:
                break
        
        return results or [{"message": "no matching entries found."}]
    except Exception as e:
        logging.error(f"Error fetching or parsing feed: {e}")
        return [{"error": str(e)}]

@mcp.tool()
def list_available_feeds() -> list:
    """
    List all available RSS feeds.
    returns: list of available RSS feeds with name, url, and description
    """
    return [
        {
            "name": config.name,
            "url": config.url,
            "description": config.description
        }
        for config in FEEDS.values()
    ]

@mcp.tool()
def fetch_google_blog_feed(query: str, max_results: int=5) -> list:
    """
    Fetch RSS feed entries from Google Blog Search based on a query.
    args:
        query: str, the search query - title or description
        max_results: int, maximum number of results to return
    returns: list of blog feed entries matching query
    """
    
    return search_feed(FEEDS["google_blog"].url, query, max_results)

@mcp.tool()
def fetch_youtube_feed(query: str, max_results: int=5) -> list:
    """
    Fetch RSS feed entries from Google Cloud YouTube channel based on a query.
    args:
        query: str, the search query - title or description
        max_results: int, maximum number of results to return
    returns: list of video feed entries matching query
    """
    
    return search_feed(FEEDS["google_cloud_youtube"].url, query, max_results)
    
if __name__ == "__main__":
    mcp.run(transport="sse") # http transport for remote deployment
