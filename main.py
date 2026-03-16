#!/usr/bin/env python3
"""
FX CLI - Terminal-based Foreign Exchange Tracker

A console application that tracks FX pairs, fetches real-time prices,
monitors related news, and displays economic calendar.
"""

import sys
import argparse
import time
from datetime import datetime
from typing import Optional

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.live import Live
from rich.text import Text
from rich import box
from rich.prompt import Prompt

from api_client import APIClient
from utils import parse_currency_pair, format_rate, truncate_text, get_country_from_currency


class FXCLI:
    """Main application class for FX CLI."""

    def __init__(self):
        self.console = Console()
        self.api_client = APIClient()
        self.base_currency = None
        self.target_currency = None
        self.last_refresh = None
        self.is_running = True

    def parse_arguments(self) -> Optional[tuple]:
        """Parse command line arguments."""
        parser = argparse.ArgumentParser(
            description='FX CLI - Terminal-based Foreign Exchange Tracker'
        )
        parser.add_argument(
            'pair',
            nargs='?',
            help='Currency pair (e.g., USD/JPY or EURUSD)'
        )
        args = parser.parse_args()

        if args.pair:
            parsed = parse_currency_pair(args.pair)
            if parsed:
                return parsed
            else:
                self.console.print(f"[red]Invalid currency pair format: {args.pair}[/red]")
                self.console.print("Valid formats: USD/JPY, EUR-USD, or EURUSD")
                return None

        # No pair provided, prompt user
        return self.prompt_for_pair()

    def prompt_for_pair(self) -> Optional[tuple]:
        """Prompt user for currency pair."""
        self.console.print("\n[bold cyan]FX CLI - Currency Pair Tracker[/bold cyan]")
        self.console.print("Enter a currency pair to track (e.g., USD/JPY, EURUSD):")

        while True:
            pair_input = Prompt.ask("[bold]Currency pair[/bold]", default="USD/JPY")
            parsed = parse_currency_pair(pair_input)

            if parsed:
                return parsed
            else:
                self.console.print(f"[red]Invalid format: {pair_input}[/red]")
                self.console.print("Valid formats: USD/JPY, EUR-USD, or EURUSD (3-letter codes)")

    def fetch_data(self):
        """Fetch all data from APIs."""
        data = {
            'rate': None,
            'news': [],
            'calendar': []
        }

        # Fetch exchange rate
        if self.base_currency and self.target_currency:
            data['rate'] = self.api_client.get_exchange_rate(
                self.base_currency, self.target_currency
            )

        # Fetch news for both currencies
        news_queries = [
            f"{self.base_currency} currency",
            f"{self.target_currency} currency",
            get_country_from_currency(self.base_currency),
            get_country_from_currency(self.target_currency)
        ]

        all_news = []
        for query in news_queries[:2]:  # Limit to currency codes to avoid too many requests
            news = self.api_client.get_news(query, limit=3)
            all_news.extend(news)

        # Remove duplicates by title
        seen_titles = set()
        for article in all_news:
            title = article.get('title', '')
            if title and title not in seen_titles:
                data['news'].append(article)
                seen_titles.add(title)
                if len(data['news']) >= 5:
                    break

        # Fetch economic calendar for both countries
        # Try to get country codes (simplified mapping)
        country_mapping = {
            'USD': 'US',
            'EUR': 'EU',
            'JPY': 'JP',
            'GBP': 'UK',
            'AUD': 'AU',
            'CAD': 'CA',
            'CHF': 'CH',
            'CNY': 'CN',
            'NZD': 'NZ',
            'SEK': 'SE',
            'NOK': 'NO',
            'MXN': 'MX',
            'SGD': 'SG',
            'HKD': 'HK',
            'INR': 'IN',
            'BRL': 'BR',
            'ZAR': 'ZA',
            'RUB': 'RU',
            'KRW': 'KR',
            'TRY': 'TR'
        }

        base_country = country_mapping.get(self.base_currency, 'US')
        target_country = country_mapping.get(self.target_currency, 'US')

        calendar_events = []
        for country in [base_country, target_country]:
            events = self.api_client.get_economic_calendar(country_code=country, days=7)
            calendar_events.extend(events)

        # Remove duplicates by event name and date
        seen_events = set()
        for event in calendar_events:
            event_key = f"{event.get('event')}-{event.get('date')}"
            if event_key not in seen_events:
                data['calendar'].append(event)
                seen_events.add(event_key)
                if len(data['calendar']) >= 10:
                    break

        self.last_refresh = datetime.now()
        return data

    def create_rate_panel(self, rate_data: dict) -> Panel:
        """Create panel for exchange rate display."""
        if not rate_data or not rate_data.get('rate'):
            return Panel(
                "[red]Unable to fetch exchange rate data[/red]",
                title="Exchange Rate",
                border_style="red"
            )

        rate = rate_data['rate']
        base = rate_data['base']
        target = rate_data['target']
        timestamp = rate_data.get('timestamp', '')

        rate_text = Text()
        rate_text.append(f"{base}/{target}\n", style="bold cyan")
        rate_text.append(f"{rate:,.4f}\n", style="bold white")
        rate_text.append(f"Last updated: {timestamp}", style="dim")

        return Panel(
            rate_text,
            title="Exchange Rate",
            border_style="cyan"
        )

    def create_news_table(self, news_articles: list) -> Table:
        """Create table for news articles."""
        table = Table(title="Latest News", box=box.SIMPLE, show_header=True)
        table.add_column("Source", style="cyan", width=15)
        table.add_column("Headline", style="white", width=60)
        table.add_column("Time", style="dim", width=20)

        if not news_articles:
            table.add_row("No data", "No news articles available", "")
            return table

        for article in news_articles[:5]:  # Limit to 5 articles
            source = article.get('source', 'Unknown')[:15]
            title = truncate_text(article.get('title', 'No title'), 55)
            published = article.get('published', '')[:19]

            table.add_row(source, title, published)

        return table

    def create_calendar_table(self, calendar_events: list) -> Table:
        """Create table for economic calendar."""
        table = Table(title="Economic Calendar (High Impact)", box=box.SIMPLE, show_header=True)
        table.add_column("Date", style="cyan", width=12)
        table.add_column("Country", style="green", width=8)
        table.add_column("Event", style="white", width=40)
        table.add_column("Actual", style="yellow", width=10)
        table.add_column("Forecast", style="blue", width=10)

        if not calendar_events:
            table.add_row("No data", "", "No economic events available", "", "")
            return table

        for event in calendar_events[:10]:  # Limit to 10 events
            date = event.get('date', '')[:10]
            country = event.get('country', '')[:8]
            event_name = truncate_text(event.get('event', 'Unknown'), 35)
            actual = str(event.get('actual', ''))[:8]
            forecast = str(event.get('forecast', ''))[:8]

            table.add_row(date, country, event_name, actual, forecast)

        return table

    def create_layout(self, data: dict) -> Layout:
        """Create the main layout."""
        layout = Layout()

        # Split into main area and status
        layout.split_column(
            Layout(name="main", ratio=4),
            Layout(name="status", ratio=1)
        )

        # Split main area into three sections
        layout["main"].split_row(
            Layout(name="rate", ratio=1),
            Layout(name="right_panel", ratio=2)
        )

        layout["right_panel"].split_column(
            Layout(name="news", ratio=1),
            Layout(name="calendar", ratio=1)
        )

        # Add content to each section
        layout["rate"].update(self.create_rate_panel(data.get('rate')))
        layout["news"].update(self.create_news_table(data.get('news', [])))
        layout["calendar"].update(self.create_calendar_table(data.get('calendar', [])))

        # Status panel
        status_text = Text()
        status_text.append("FX CLI | ", style="bold")
        status_text.append(f"Pair: {self.base_currency}/{self.target_currency} | ", style="cyan")
        status_text.append(f"Last refresh: {self.last_refresh.strftime('%H:%M:%S') if self.last_refresh else 'Never'} | ", style="dim")
        status_text.append("Press ", style="dim")
        status_text.append("R", style="bold green")
        status_text.append(" to refresh, ", style="dim")
        status_text.append("Q", style="bold red")
        status_text.append(" to quit", style="dim")

        layout["status"].update(Panel(status_text, border_style="dim"))

        return layout

    def display_data(self, data: dict):
        """Display all data in a simple format."""
        self.console.clear()

        # Display header
        self.console.print(f"\n[bold cyan]FX CLI - {self.base_currency}/{self.target_currency} Tracker[/bold cyan]")
        if self.last_refresh:
            self.console.print(f"[dim]Last updated: {self.last_refresh.strftime('%Y-%m-%d %H:%M:%S')}[/dim]")
        self.console.print()

        # Display exchange rate
        rate_data = data.get('rate')
        if rate_data and rate_data.get('rate'):
            self.console.print("[bold]Exchange Rate:[/bold]")
            rate_panel = self.create_rate_panel(rate_data)
            self.console.print(rate_panel)
        else:
            self.console.print("[red]No exchange rate data available[/red]")

        self.console.print()

        # Display news
        news_data = data.get('news', [])
        if news_data:
            self.console.print("[bold]Latest News:[/bold]")
            news_table = self.create_news_table(news_data)
            self.console.print(news_table)
        else:
            self.console.print("[yellow]No news articles available[/yellow]")

        self.console.print()

        # Display economic calendar
        calendar_data = data.get('calendar', [])
        if calendar_data:
            self.console.print("[bold]Economic Calendar (High Impact):[/bold]")
            calendar_table = self.create_calendar_table(calendar_data)
            self.console.print(calendar_table)
        else:
            self.console.print("[yellow]No economic calendar events available[/yellow]")

    def run(self):
        """Main application loop."""
        # Get currency pair
        parsed = self.parse_arguments()
        if not parsed:
            self.console.print("[red]Failed to get valid currency pair. Exiting.[/red]")
            sys.exit(1)

        self.base_currency, self.target_currency = parsed

        # Initial data fetch
        self.console.print(f"\n[green]Tracking {self.base_currency}/{self.target_currency}...[/green]")
        self.console.print("[dim]Fetching data...[/dim]")

        data = self.fetch_data()

        # Display initial data
        self.display_data(data)

        while self.is_running:
            # Simple input handling
            self.console.print("\n[dim]Press 'R' to refresh, 'Q' to quit[/dim]")
            user_input = input("> ").strip().upper()

            if user_input == 'Q':
                self.is_running = False
                break
            elif user_input == 'R' or user_input == '':
                # Refresh data (empty input also refreshes)
                self.console.print("[dim]Refreshing data...[/dim]")
                data = self.fetch_data()
                self.console.clear()
                self.display_data(data)
            else:
                self.console.print("[yellow]Unknown command. Press 'R' to refresh or 'Q' to quit[/yellow]")

        self.console.print("\n[green]FX CLI terminated. Goodbye![/green]")


def main():
    """Main entry point."""
    try:
        app = FXCLI()
        app.run()
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Exiting.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main()