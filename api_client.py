"""
API client for fetching FX data, news, and economic calendar.
"""

import os
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import time
from dotenv import load_dotenv

load_dotenv('.env.keys')


class APIClient:
    """Main API client for all data sources."""

    def __init__(self):
        self.exchange_rate_api_key = os.getenv('EXCHANGE_RATE_API_KEY')
        self.newsdata_api_key = os.getenv('NEWSDATA_API_KEY')
        self.finnhub_api_key = os.getenv('FINNHUB_API_KEY')

        if not self.exchange_rate_api_key:
            raise ValueError("EXCHANGE_RATE_API_KEY not found in environment variables")
        if not self.newsdata_api_key:
            raise ValueError("NEWSDATA_API_KEY not found in environment variables")
        if not self.finnhub_api_key:
            raise ValueError("FINNHUB_API_KEY not found in environment variables")

    def get_exchange_rate(self, base_currency: str, target_currency: str) -> Optional[Dict]:
        """
        Get current exchange rate from ExchangeRate-API.

        Args:
            base_currency: Base currency code (e.g., 'USD')
            target_currency: Target currency code (e.g., 'JPY')

        Returns:
            Dictionary with rate data or None if error
        """
        try:
            url = f"https://v6.exchangerate-api.com/v6/{self.exchange_rate_api_key}/pair/{base_currency}/{target_currency}"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('result') == 'success':
                return {
                    'rate': data.get('conversion_rate'),
                    'base': base_currency,
                    'target': target_currency,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                print(f"API Error: {data.get('error-type', 'Unknown error')}")
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request error fetching exchange rate: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error fetching exchange rate: {e}")
            return None

    def get_news(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Get news articles from NewsData.io.

        Args:
            query: Search query (e.g., 'USD' or 'Japan economy')
            limit: Maximum number of articles to return

        Returns:
            List of news article dictionaries
        """
        try:
            url = "https://newsdata.io/api/1/news"
            params = {
                'apikey': self.newsdata_api_key,
                'q': query,
                'language': 'en',
                'size': limit
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get('status') == 'success':
                articles = []
                for article in data.get('results', [])[:limit]:
                    articles.append({
                        'title': article.get('title', 'No title'),
                        'description': article.get('description', 'No description'),
                        'source': article.get('source_id', 'Unknown'),
                        'published': article.get('pubDate', ''),
                        'url': article.get('link', '')
                    })
                return articles
            else:
                print(f"News API Error: {data.get('message', 'Unknown error')}")
                return []

        except requests.exceptions.RequestException as e:
            print(f"Request error fetching news: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error fetching news: {e}")
            return []

    def get_economic_calendar(self, country_code: str = "US", days: int = 7) -> List[Dict]:
        """
        Get economic calendar events from Finnhub.io.

        Args:
            country_code: Country code (e.g., 'US', 'JP', 'EU')
            days: Number of days to look ahead

        Returns:
            List of economic calendar events
        """
        try:
            # Calculate date range
            from_date = datetime.now().strftime('%Y-%m-%d')
            to_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')

            url = "https://finnhub.io/api/v1/calendar/economic"
            params = {
                'token': self.finnhub_api_key,
                'from': from_date,
                'to': to_date
            }

            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            events = []
            if data and isinstance(data, dict) and 'economicCalendar' in data:
                for event in data['economicCalendar']:
                    # Filter by country if specified
                    if country_code and event.get('country') != country_code:
                        continue

                    # Only include high impact events
                    if event.get('impact') == 'high':
                        events.append({
                            'event': event.get('event', 'Unknown'),
                            'country': event.get('country', 'Unknown'),
                            'date': event.get('date', ''),
                            'time': event.get('time', ''),
                            'impact': event.get('impact', 'medium'),
                            'actual': event.get('actual'),
                            'forecast': event.get('forecast'),
                            'previous': event.get('previous')
                        })

            return events[:10]  # Limit to 10 events

        except requests.exceptions.RequestException as e:
            print(f"Request error fetching economic calendar: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error fetching economic calendar: {e}")
            return []

    def get_currency_info(self, currency_code: str) -> Dict[str, str]:
        """
        Get basic information about a currency (country names).

        Args:
            currency_code: Currency code (e.g., 'USD', 'JPY')

        Returns:
            Dictionary with currency information
        """
        # Simple mapping for common currencies
        currency_info = {
            'USD': {'country': 'United States', 'name': 'US Dollar'},
            'EUR': {'country': 'European Union', 'name': 'Euro'},
            'JPY': {'country': 'Japan', 'name': 'Japanese Yen'},
            'GBP': {'country': 'United Kingdom', 'name': 'British Pound'},
            'AUD': {'country': 'Australia', 'name': 'Australian Dollar'},
            'CAD': {'country': 'Canada', 'name': 'Canadian Dollar'},
            'CHF': {'country': 'Switzerland', 'name': 'Swiss Franc'},
            'CNY': {'country': 'China', 'name': 'Chinese Yuan'},
            'NZD': {'country': 'New Zealand', 'name': 'New Zealand Dollar'},
            'SEK': {'country': 'Sweden', 'name': 'Swedish Krona'},
            'NOK': {'country': 'Norway', 'name': 'Norwegian Krone'},
            'MXN': {'country': 'Mexico', 'name': 'Mexican Peso'},
            'SGD': {'country': 'Singapore', 'name': 'Singapore Dollar'},
            'HKD': {'country': 'Hong Kong', 'name': 'Hong Kong Dollar'},
            'INR': {'country': 'India', 'name': 'Indian Rupee'},
            'BRL': {'country': 'Brazil', 'name': 'Brazilian Real'},
            'ZAR': {'country': 'South Africa', 'name': 'South African Rand'},
            'RUB': {'country': 'Russia', 'name': 'Russian Ruble'},
            'KRW': {'country': 'South Korea', 'name': 'South Korean Won'},
            'TRY': {'country': 'Turkey', 'name': 'Turkish Lira'},
        }

        return currency_info.get(currency_code.upper(), {'country': 'Unknown', 'name': currency_code.upper()})