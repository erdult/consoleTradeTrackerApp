# FX CLI - Terminal-based Foreign Exchange Tracker

A console application that tracks FX pairs, fetches real-time prices, monitors related news, and displays economic calendar.

## Features

- **Real-time Exchange Rates**: Fetch current mid-market rates using ExchangeRate-API
- **Related News**: Get latest news articles for tracked currencies
- **Economic Calendar**: View high-impact economic events (requires Finnhub API key)
- **Rich Terminal UI**: Beautiful terminal interface using `rich` library
- **Auto-refresh**: Manual refresh with `R` key, auto-refresh every 30 seconds

## Quick Start

### Prerequisites

- Python 3.10+
- Conda environment `myenv` (or create new virtual environment)
- API keys for:
  - [ExchangeRate-API](https://www.exchangerate-api.com/) (Free tier)
  - [NewsData.io](https://newsdata.io/) (Free tier)
  - [Finnhub.io](https://finnhub.io/) (Free tier) - for economic calendar

### Installation

1. Clone the repository:
```bash
git clone https://github.com/erdult/consoleTradeTrackerApp.git
cd consoleTradeTrackerApp
```

2. Activate conda environment:
```bash
conda activate myenv
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Create `.env.keys` file with your API keys:
```bash
cat > .env.keys << EOF
EXCHANGE_RATE_API_KEY=your_exchange_rate_api_key
NEWSDATA_API_KEY=your_newsdata_api_key
FINNHUB_API_KEY=your_finnhub_api_key
EOF
```

### Usage

Run with a currency pair:
```bash
python main.py USD/JPY
```

Or let the application prompt you:
```bash
python main.py
```

### Controls

- **R**: Refresh data manually
- **Q**: Quit application

## Project Structure

```
.
├── main.py              # Main application with UI
├── api_client.py        # API clients for all data sources
├── utils.py             # Utility functions (parsing, formatting)
├── test_api.py          # API testing script
├── .env.keys           # API keys (not in git)
└── README.md           # This file
```

## API Notes

### ExchangeRate-API
- Free tier: 1,500 requests/month
- No authentication required for free tier (uses API key in URL)

### NewsData.io
- Free tier: 200 requests/day
- Limited to recent news only

### Finnhub.io
- Free tier: 60 requests/minute
- Economic calendar endpoint requires API key
- If you get 403 errors, your API key may need activation

## Development

### Testing APIs
```bash
python test_api.py
```

### Adding New Features
1. Follow conventional commit messages
2. Test API endpoints independently
3. Ensure graceful error handling

## Limitations

- Economic calendar may fail if Finnhub API key is not activated
- News API has daily limits
- Terminal UI requires compatible terminal emulator

## License

MIT License