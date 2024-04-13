import yfinance as yf
from tenacity import retry, wait_exponential


@retry(wait=wait_exponential(multiplier=2, min=4, max=10))
def get_yf_ticker_news(ticker: str):
    return yf.Ticker(ticker).news
