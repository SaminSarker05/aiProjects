from mcp.server.fastmcp import FastMCP
import yfinance as yf

mcp = FastMCP("StockPriceServer")

@mcp.tool()
def get_stock_price(ticker: str) -> float:
    """
    Get the current price of a stock.
    args:
        ticker: str, the stock ticker symbol
    returns: float, the current price of the stock
    """
    try:
        stock_ticker = yf.Ticker(ticker)
        data = stock_ticker.history(period="1d")
        if data.empty:
            info = stock_ticker.info
            price = info.get("regularMarketPrice", None)
            if price:
                return float(price)
            else:
                return -1.0
        else:
            price = data['Close'].iloc[-1]
            return float(price)
    except Exception:
        return -1.0

@mcp.resource("stock://{symbol}")
def stock_resource(symbol: str) -> str:
    """
    Get the current price of a stock
    formatted as a string.
    """
    price = get_stock_price(symbol)
    if price < 0:
        return f"Error: Failed to get stock price for {symbol}"
    return f"The current price of {symbol} is {price}"

@mcp.tool()
def get_stock_history(symbol: str, period: str = "1mo") -> str:
    """
    Return historical stock data for give ticker symbol and period.
    Return data as a csv formated string.
    args:
        symbol: str, the stock ticker symbol
        period: str, the time period to get data for, default is 1 month
    returns: str, the historical stock data
    """
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period=period)
        if data.empty():
            return f"Error: Failed to get stock data for {symbol}"
        return data.to_csv()
    except Exception:
        return f"Error: Failed to get stock data for {symbol}"

if __name__ == "__main__":
    mcp.run()
