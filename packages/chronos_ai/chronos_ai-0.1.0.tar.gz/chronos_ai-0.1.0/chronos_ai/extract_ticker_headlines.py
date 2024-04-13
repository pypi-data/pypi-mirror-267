from typing import Any


def extract_ticker_headlines(ticker_news: list[Any]) -> list[str]:
    return [item["title"] for item in ticker_news]
