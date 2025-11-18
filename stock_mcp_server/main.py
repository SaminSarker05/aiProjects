"""
MCP server integrated with alpaca trading API and
yfinance for auomated trade executions on paper trade
account.

"""

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus
import yfinance as yf
import os
import requests

load_dotenv()

# define mcp server
mcp = FastMCP("StockPriceServer")

# define alpaca trading client
trading_client = TradingClient(
    api_key=os.getenv("ALPACA_API_KEY"),
    secret_key=os.getenv("ALPACA_SECRET_KEY"),
    paper=True
)

@mcp.tool()
def get_all_positions() -> str:
    """
    Get all positions in the account.
    returns: str, all positions in the account
    """
    portfolio = trading_client.get_all_positions()
    positions = "All positions:\n"
    for position in portfolio:
        positions += f"{position.symbol}: {position.qty}, {position.cost}, {position.market_value}\n"
    return positions
        
@mcp.tool()
def market_buy_order(symbol: str, quantity: int) -> str:
    """
    Place market order to buy a stock at market price
    for the specified quantity.
    
    args:
        symbol: str, the stock ticker symbol
        quantity: int, the number of shares to buy
    returns: str, a message indicating whether the buy was successful
    """
    try:
        market_order = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY # order is good until market closes 
        )
        order = trading_client.submit_order(market_order)
        return f"Successfully bought {quantity} shares of {symbol}"
    except Exception as e:
        return f"Failed to buy {quantity} shares of {symbol}: {e}"

@mcp.tool()
def market_sell_order(symbol: str, quantity: int) -> str:
    """
    Place market order to sell a stock at market price
    for the specified quantity.
    
    args:
        symbol: str, the stock ticker symbol
        quantity: int, the number of shares to sell
    returns: str, a message indicating whether the sell was successful
    """
    try:
        market_order = MarketOrderRequest(
            symbol=symbol,
            qty=quantity,
            side=OrderSide.SELL,
            time_in_force=TimeInForce.DAY
        )
        order = trading_client.submit_order(market_order)
        return f"Successfully sold {quantity} shares of {symbol}"
    except Exception as e:
        return f"Failed to sell {quantity} shares of {symbol}: {e}"

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

@mcp.tool()
def get_account_balance() -> str:
    """
    Get current account balance from paper trading account.
    returns: str, account information
    """
    try:
        account = trading_client.get_account()
        return f"""Account Balance:
        - Cash: ${float(account.cash):.2f}
        - Portfolio Value: ${float(account.portfolio_value):.2f}
        - Equity: ${float(account.equity):.2f}
        - Buying Power: ${float(account.buying_power):.2f}
        - Account Status: {account.status}
        """
    except Exception as e:
        return f"Error retrieving account balance: {str(e)}"

@mcp.tool()
def get_order_history(limit: int=10) -> str:
    """
    Get order history from paper trading account.
    args:
        limit: int, the maximum number of orders to return
    returns: str, formatted order history
    """
    try:
        filter = GetOrdersRequest(
            status=QueryOrderStatus.ALL,
            limit=limit
        )
        orders = trading_client.get_orders(filter=filter)
        if not orders:
            return "No orders were found."
        record = "orders: "
        for order in orders[:limit]:
            record += f"\n{order}"
        return record
    except Exception as e:
        return f"Error retrieving order history: {str(e)}"

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
        if data.empty:
            return f"Error: Failed to get stock data for {symbol}"
        return data.to_csv()
    except Exception:
        return f"Error: Failed to get stock data for {symbol}"

if __name__ == "__main__":
    mcp.run()
