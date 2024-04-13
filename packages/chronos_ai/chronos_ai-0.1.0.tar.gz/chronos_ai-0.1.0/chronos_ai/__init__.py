import argparse
from speech_user_interface import (
    speech_user_interface,
    speak_text,
    compare_strings,
)

from .analyze_stock_headlines import analyze_stock_headlines
from .create_ticker_list import create_ticker_list
from .CONSTANTS import FOREX_TICKERS

__name__ == "__main__"
__all__ = ["train", "forecast", "saturn_utils", "saturn_forecaster"]


def analyze_parse_args():
    parser = argparse.ArgumentParser(
        description="The analyze method of Chronos."
    )
    parser.add_argument(
        "--ticker",
        type=str,
        help="Call with --ticker to pass the desired ticker to analyze",
        required=True,
        default=False,
        const=True,
        nargs="?",
        dest="ticker",
    )
    return parser.parse_args()


def function_to_run(input_text: str):
    if compare_strings(input_text, "scan"):
        scan()


def main():
    # build()
    speech_user_interface()
    analyze()


def analyze():
    print("Analyzing...")

    args = analyze_parse_args()

    return analyze_stock_headlines(args.ticker)


def scan(forex: bool = True):
    print("Scanning for forex currency pairs to buy/short...")
    speak_text("Scanning for forex currency pairs to buy/short...")

    largest_sentiment = 0.0
    lowest_sentiment = 10000.0
    if not forex:
        tickers = create_ticker_list()
    else:
        tickers = FOREX_TICKERS
    best_ticker: str = tickers[0]
    worst_ticker: str = tickers[0]
    i: int = 0
    for ticker in tickers:
        sentiment = analyze_stock_headlines(ticker)

        if sentiment > largest_sentiment:
            best_ticker = ticker
            largest_sentiment = sentiment
        if sentiment < lowest_sentiment:
            worst_ticker = ticker
            lowest_sentiment = sentiment

        if i % 10 == 0:
            print(
                "(best_ticker, largest_sentiment), (worst_ticker, lowest_sentiment):",
                (best_ticker, largest_sentiment),
                (worst_ticker, lowest_sentiment),
            )
            speak_text(
                "(best_ticker, largest_sentiment), (worst_ticker, lowest_sentiment):"
                + f"{(best_ticker, largest_sentiment)}"
                + f"{(worst_ticker, lowest_sentiment)}"
            )

        i += 1

    print(
        "(best_ticker, largest_sentiment), (worst_ticker, lowest_sentiment):",
        (best_ticker, largest_sentiment),
        (worst_ticker, lowest_sentiment),
    )
    speak_text(
        "(best_ticker, largest_sentiment), (worst_ticker, lowest_sentiment):"
        + f"{(best_ticker, largest_sentiment)}"
        + f"{(worst_ticker, lowest_sentiment)}"
    )
    return (best_ticker, largest_sentiment), (worst_ticker, lowest_sentiment)
