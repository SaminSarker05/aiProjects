```
## Project Descriptions

### 2048_agent/
AI agent for the 2048 game using expectiminimax algorithm with alpha-beta pruning.

Tech: Python
Features: 3-level search depth, adversarial modeling, multiple weighted heuristics
Heuristics: Open cells, max tile value, monotonicity, smoothness, edge tiles, snake pattern
Performance: Consistently achieves 1024 and 2048 tiles

### monkey_agent/
Multi-agent coding assistant using LangChain/LangGraph and OpenAI GPT-4 for automated code generation.

Tech: Python, LangChain, LangGraph, OpenAI GPT-4
Features: Three-agent system (Planner, Architect, Coder), file system tools, state graph orchestration
Agents: Plan generation → Task breakdown → Code implementation
Example Output: Generated todo app in monkey-generated-code/


### rss-mcp_server/
MCP server for searching and fetching RSS feed entries from Google Blog and YouTube.

Tech: Python, FastMCP, feedparser
Features: RSS feed search, query matching, remote deployment ready
Feeds: Google Blog Search, Google Cloud YouTube channel
Deployment: FastMCP Cloud Platform (needs fix)


### stock_mcp_server/
MCP server integrated with Alpaca Trading API and yfinance for automated paper trading.

Tech: Python, FastMCP, Alpaca API, yfinance
Features: Position tracking, market orders (buy/sell), stock prices, account balance, order history
Trading: Paper trading account only
Resources: Stock price lookup with stock://{symbol} URI


Example queries:
- "what are all my positions and order history?"
- "buy 2 AAPL at market price"
- "get current price of TSLA"

### sudoku/
Sudoku solver modeled as a constraint satisfaction problem with backtracking.

Tech: Python
Algorithm: Backtracking with Minimum Remaining Values (MRV) heuristic and forward checking
Features: Efficient pruning, early failure detection, constraint propagation
Approach: CSP with domain reduction for unassigned variables

## Note

Each project is self-contained.
```
