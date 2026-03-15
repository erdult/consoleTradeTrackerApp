-

# FX CLI Project: Mission Brief

## 🎯 Goal

Build a functional Linux console application (Python-based) that tracks a user-specified FX pair, fetches real-time prices, monitors related news, and displays an economic calendar.

## 🛠 Tech Stack & APIs

* **Language:** Python 3.10+
* **Price Data:** [ExchangeRate-API](https://www.exchangerate-api.com/) (Free Tier)
* **News:** [NewsData.io](https://newsdata.io/) (Free Tier)
* **Calendar:** [Finnhub.io](https://finnhub.io/) or [Tradermade](https://tradermade.com/) (Economic Calendar endpoints)
* **UI:** `rich` or `blessed` (for a clean terminal dashboard)

## 🏗 Requirements & MVP Scope

1. **Input:** Accept a currency pair via command line argument or initial prompt (e.g., `USD/JPY`).
2. **Rate Tracker:** Fetch current mid-market rate and display it with a "Last Updated" timestamp.
3. **News Feed:** Fetch the last 5 headlines related to the base or quote currency's countries.
4. **Economic Calendar:** List "High Impact" events (Interest rate decisions, CPI, NFP) for the next 7 days for the relevant currencies.
5. **Auto-Refresh:** Implement a basic loop or a "Press R to Refresh" mechanic.

## 🤖 Autonomy Rules

* **Permissions:** You have full permission to use `bash`, `pip install`, and `git commit`.
* **Workflow:** 
1. Use myenv virtual environment, if you need additional packages you can install them but keep track of packages you have added
2. Create the file structure (`main.py`, `api_client.py`, `utils.py`).
3. Implement modules one by one.
4. **Commit and push to GitHub independently** after each functional component is verified.
* **Completion:** Do not stop for confirmation until the app successfully displays all three data points (Price, News, Calendar) for a given pair.

## 🔑 Environment Variables

Assume the following will be in a `.env.keys` file 
* `EXCHANGE_RATE_API_KEY`
* `NEWSDATA_API_KEY`
* `FINNHUB_API_KEY`


## Git Workflow
- **Branching:** Work directly on `main` for the MVP.
- **Commits:** Use conventional commit messages (e.g., `feat: add price fetching logic`).
- **Syncing:** Pull before starting a task and push immediately after a successful test run.
- **Attribution:** [Optional] Set `"gitAttribution": true` in settings if you want to track which lines Claude wrote.



---

