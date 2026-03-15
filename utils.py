"""
Utility functions for the FX CLI application.
"""

import re
from typing import Optional, Tuple
from datetime import datetime


def parse_currency_pair(pair_str: str) -> Optional[Tuple[str, str]]:
    """
    Parse a currency pair string like 'USD/JPY' or 'EURUSD'.

    Args:
        pair_str: Currency pair string

    Returns:
        Tuple of (base_currency, target_currency) or None if invalid
    """
    if not pair_str or not isinstance(pair_str, str):
        return None

    pair_str = pair_str.strip().upper()

    # Try format like USD/JPY or EUR-USD
    if '/' in pair_str:
        parts = pair_str.split('/')
    elif '-' in pair_str:
        parts = pair_str.split('-')
    else:
        # Assume 6 characters like EURUSD
        if len(pair_str) == 6:
            parts = [pair_str[:3], pair_str[3:]]
        else:
            return None

    if len(parts) != 2:
        return None

    base_currency, target_currency = parts[0], parts[1]

    # Validate currency codes (3 letters)
    if not (len(base_currency) == 3 and base_currency.isalpha()):
        return None
    if not (len(target_currency) == 3 and target_currency.isalpha()):
        return None

    return base_currency, target_currency


def format_timestamp(timestamp_str: str) -> str:
    """
    Format an ISO timestamp string to a readable format.

    Args:
        timestamp_str: ISO format timestamp string

    Returns:
        Formatted timestamp string
    """
    try:
        dt = datetime.fromisoformat(timestamp_str.replace('Z', '+00:00'))
        return dt.strftime('%Y-%m-%d %H:%M:%S')
    except (ValueError, AttributeError):
        return timestamp_str


def format_rate(rate: float, base_currency: str, target_currency: str) -> str:
    """
    Format an exchange rate for display.

    Args:
        rate: Exchange rate
        base_currency: Base currency code
        target_currency: Target currency code

    Returns:
        Formatted rate string
    """
    if rate is None:
        return "N/A"

    # Format with appropriate decimal places
    if rate >= 100:
        formatted_rate = f"{rate:,.2f}"
    elif rate >= 10:
        formatted_rate = f"{rate:,.3f}"
    elif rate >= 1:
        formatted_rate = f"{rate:,.4f}"
    else:
        formatted_rate = f"{rate:,.6f}"

    return f"{base_currency}/{target_currency}: {formatted_rate}"


def truncate_text(text: str, max_length: int = 80) -> str:
    """
    Truncate text to specified length and add ellipsis if needed.

    Args:
        text: Text to truncate
        max_length: Maximum length

    Returns:
        Truncated text
    """
    if not text:
        return ""
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + "..."


def get_country_from_currency(currency_code: str) -> str:
    """
    Get country name from currency code.

    Args:
        currency_code: Currency code (e.g., 'USD', 'JPY')

    Returns:
        Country name
    """
    currency_to_country = {
        'USD': 'United States',
        'EUR': 'European Union',
        'JPY': 'Japan',
        'GBP': 'United Kingdom',
        'AUD': 'Australia',
        'CAD': 'Canada',
        'CHF': 'Switzerland',
        'CNY': 'China',
        'NZD': 'New Zealand',
        'SEK': 'Sweden',
        'NOK': 'Norway',
        'MXN': 'Mexico',
        'SGD': 'Singapore',
        'HKD': 'Hong Kong',
        'INR': 'India',
        'BRL': 'Brazil',
        'ZAR': 'South Africa',
        'RUB': 'Russia',
        'KRW': 'South Korea',
        'TRY': 'Turkey',
    }

    return currency_to_country.get(currency_code.upper(), currency_code.upper())


def validate_currency_code(currency_code: str) -> bool:
    """
    Validate a currency code.

    Args:
        currency_code: Currency code to validate

    Returns:
        True if valid, False otherwise
    """
    if not currency_code or not isinstance(currency_code, str):
        return False

    currency_code = currency_code.strip().upper()
    if len(currency_code) != 3:
        return False

    return currency_code.isalpha()