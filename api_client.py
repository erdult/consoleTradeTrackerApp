"""
API client for fetching FX data, news, and economic calendar.
"""

import os
import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import time, random
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

    def _generate_mock_calendar_events(self, country_code: str = "US", days: int = 7) -> List[Dict]:
        """
        Generate mock economic calendar events for testing.

        Args:
            country_code: Country code to filter events
            days: Number of days to generate events for

        Returns:
            List of mock economic calendar events
        """
        events = []

        # Common high-impact economic events by country
        country_events = {
            'US': [
                'Federal Funds Rate Decision',
                'Non-Farm Payrolls',
                'CPI Inflation Rate',
                'GDP Growth Rate',
                'Retail Sales',
                'Initial Jobless Claims',
                'ISM Manufacturing PMI',
                'Consumer Confidence'
            ],
            'JP': [
                'Bank of Japan Interest Rate Decision',
                'CPI Inflation Rate',
                'Unemployment Rate',
                'Industrial Production',
                'Retail Sales',
                'Trade Balance'
            ],
            'EU': [
                'ECB Interest Rate Decision',
                'CPI Inflation Rate',
                'Unemployment Rate',
                'GDP Growth Rate',
                'Manufacturing PMI',
                'Consumer Confidence'
            ],
            'UK': [
                'Bank of England Interest Rate Decision',
                'CPI Inflation Rate',
                'Unemployment Rate',
                'GDP Growth Rate',
                'Retail Sales',
                'Manufacturing PMI'
            ],
            'CA': [
                'Bank of Canada Interest Rate Decision',
                'CPI Inflation Rate',
                'Unemployment Rate',
                'GDP Growth Rate',
                'Retail Sales'
            ],
            'AU': [
                'RBA Interest Rate Decision',
                'CPI Inflation Rate',
                'Unemployment Rate',
                'GDP Growth Rate',
                'Retail Sales'
            ],
            'CH': [
                'SNB Interest Rate Decision',
                'CPI Inflation Rate',
                'Unemployment Rate',
                'GDP Growth Rate'
            ]
        }

        # Get events for the specified country or use US as default
        event_list = country_events.get(country_code, country_events['US'])

        # Generate events for the next 'days' days
        today = datetime.now()
        for day_offset in range(days):
            event_date = today + timedelta(days=day_offset)

            # Generate 1-3 events per day
            num_events = random.randint(1, 3)
            for i in range(num_events):
                event_name = random.choice(event_list)

                # Generate realistic values
                if 'Rate Decision' in event_name:
                    actual = f"{random.uniform(0.5, 5.0):.2f}%"
                    forecast = f"{random.uniform(0.5, 5.0):.2f}%"
                    previous = f"{random.uniform(0.5, 5.0):.2f}%"
                elif 'CPI' in event_name or 'Inflation' in event_name:
                    actual = f"{random.uniform(1.0, 8.0):.1f}%"
                    forecast = f"{random.uniform(1.0, 8.0):.1f}%"
                    previous = f"{random.uniform(1.0, 8.0):.1f}%"
                elif 'Unemployment' in event_name:
                    actual = f"{random.uniform(2.0, 10.0):.1f}%"
                    forecast = f"{random.uniform(2.0, 10.0):.1f}%"
                    previous = f"{random.uniform(2.0, 10.0):.1f}%"
                elif 'GDP' in event_name:
                    actual = f"{random.uniform(-2.0, 8.0):.1f}%"
                    forecast = f"{random.uniform(-2.0, 8.0):.1f}%"
                    previous = f"{random.uniform(-2.0, 8.0):.1f}%"
                else:
                    actual = f"{random.uniform(-5.0, 10.0):.1f}"
                    forecast = f"{random.uniform(-5.0, 10.0):.1f}"
                    previous = f"{random.uniform(-5.0, 10.0):.1f}"

                # Random time
                hour = random.randint(8, 16)
                minute = random.choice([0, 15, 30, 45])
                event_time = f"{hour:02d}:{minute:02d}"

                events.append({
                    'event': event_name,
                    'country': country_code,
                    'date': event_date.strftime('%Y-%m-%d'),
                    'time': event_time,
                    'impact': 'high',
                    'actual': actual,
                    'forecast': forecast,
                    'previous': previous
                })

                # Limit total events
                if len(events) >= 10:
                    break
            if len(events) >= 10:
                break

        return events

    def get_economic_calendar(self, country_code: str = "US", days: int = 7) -> List[Dict]:
        """
        Get economic calendar events from Finnhub.io.

        TEMPORARY: Using mock data while API is being fixed.

        Args:
            country_code: Country code (e.g., 'US', 'JP', 'EU')
            days: Number of days to look ahead

        Returns:
            List of economic calendar events
        """
        # TODO: Restore Finnhub API when API key is fixed
        # try:
        #     # Calculate date range
        #     from_date = datetime.now().strftime('%Y-%m-%d')
        #     to_date = (datetime.now() + timedelta(days=days)).strftime('%Y-%m-%d')
        #
        #     url = "https://finnhub.io/api/v1/calendar/economic"
        #     params = {
        #         'token': self.finnhub_api_key,
        #         'from': from_date,
        #         'to': to_date
        #     }
        #
        #     response = requests.get(url, params=params, timeout=10)
        #     response.raise_for_status()
        #     data = response.json()
        #
        #     events = []
        #     if data and isinstance(data, dict) and 'economicCalendar' in data:
        #         for event in data['economicCalendar']:
        #             # Filter by country if specified
        #             if country_code and event.get('country') != country_code:
        #                 continue
        #
        #             # Only include high impact events
        #             if event.get('impact') == 'high':
        #                 events.append({
        #                     'event': event.get('event', 'Unknown'),
        #                     'country': event.get('country', 'Unknown'),
        #                     'date': event.get('date', ''),
        #                     'time': event.get('time', ''),
        #                     'impact': event.get('impact', 'medium'),
        #                     'actual': event.get('actual'),
        #                     'forecast': event.get('forecast'),
        #                     'previous': event.get('previous')
        #                 })
        #
        #     return events[:10]  # Limit to 10 events
        #
        # except requests.exceptions.RequestException as e:
        #     print(f"Request error fetching economic calendar: {e}")
        #     return []
        # except Exception as e:
        #     print(f"Unexpected error fetching economic calendar: {e}")
        #     return []

        # TEMPORARY: Return mock data
        print(f"[INFO] Using mock economic calendar data for {country_code}")
        return self._generate_mock_calendar_events(country_code, days)[:10]

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