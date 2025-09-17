# server.py

import feedparser
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Demo")

# Add a latest news tool
@mcp.tool()
def latest_news() -> list:
    """Fetch the latest 5 news headlines from a public RSS feed"""
    feed_url = "https://feeds.bbci.co.uk/news/rss.xml"
    feed = feedparser.parse(feed_url)
    headlines = []
    for entry in feed.entries[:5]:
        headlines.append(entry.title)
    return headlines

# Add a weather tool for Chicago
@mcp.tool()
def chicago_weather() -> str:
    """Fetch the current weather for Chicago from a public RSS feed"""
    feed_url = "https://w1.weather.gov/xml/current_obs/KORD.rss"
    feed = feedparser.parse(feed_url)
    if feed.entries:
        entry = feed.entries[0]
        return entry.title + ": " + entry.summary
    return "Weather information not available."

# Add a weather resource for any city (using NWS station codes for US cities)
@mcp.resource("weather://{station_code}")
def get_weather(station_code: str) -> str:
    """Fetch the current weather for a given US city by NWS station code (e.g., KORD for Chicago)"""
    feed_url = f"https://w1.weather.gov/xml/current_obs/{station_code}.rss"
    feed = feedparser.parse(feed_url)
    if feed.entries:
        entry = feed.entries[0]
        return entry.title + ": " + entry.summary
    return "Weather information not available."

# Add a stock price resource (mocked, as public APIs require a key)
@mcp.resource("stock://{symbol}")
def get_stock_price(symbol: str) -> str:
    """Return a mock stock price for a given symbol (replace with real API if available)"""
    # In production, use a real API like Yahoo Finance or Alpha Vantage
    mock_prices = {"AAPL": 175.12, "GOOG": 2825.23, "MSFT": 330.45, "TSLA": 750.10}
    price = mock_prices.get(symbol.upper(), None)
    if price:
        return f"{symbol.upper()} price: ${price}"
    return f"No price data available for {symbol.upper()}"

@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized welcome message"""
    return f"Welcome, {name}!. Hope you are having a great day !!"


# Main execution block - this is required to run the server
if __name__ == "__main__":
    print("Starting MCP server...")
    mcp.run()
    print("MCP server is running on http://localhost:5000")
    print("Available tools:", mcp.list_tools())