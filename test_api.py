#!/usr/bin/env python3
"""
Test script to verify API clients work.
"""

import sys
from api_client import APIClient

def test_api_client():
    """Test the API client functionality."""
    print("Testing API Client...")

    try:
        client = APIClient()
        print("✓ API client initialized successfully")
    except Exception as e:
        print(f"✗ Failed to initialize API client: {e}")
        return False

    # Test exchange rate API
    print("\nTesting Exchange Rate API (USD/JPY)...")
    rate_data = client.get_exchange_rate('USD', 'JPY')
    if rate_data:
        print(f"✓ Exchange rate: {rate_data['rate']} {rate_data['base']}/{rate_data['target']}")
    else:
        print("✗ Failed to fetch exchange rate")
        return False

    # Test news API
    print("\nTesting News API (USD)...")
    news_data = client.get_news('USD', limit=2)
    if news_data:
        print(f"✓ Found {len(news_data)} news articles")
        for i, article in enumerate(news_data[:2], 1):
            print(f"  {i}. {article['title'][:50]}...")
    else:
        print("✗ Failed to fetch news (might be API limit or no articles)")
        # Don't fail the test for news - API might have rate limits

    # Test economic calendar API
    print("\nTesting Economic Calendar API (US)...")
    calendar_data = client.get_economic_calendar('US', days=3)
    if calendar_data:
        print(f"✓ Found {len(calendar_data)} economic events")
        for i, event in enumerate(calendar_data[:3], 1):
            print(f"  {i}. {event['event'][:40]}...")
    else:
        print("✗ Failed to fetch economic calendar (might be API limit or no events)")
        # Don't fail the test for calendar - API might have rate limits

    print("\n✅ All API tests completed!")
    return True

if __name__ == "__main__":
    success = test_api_client()
    sys.exit(0 if success else 1)