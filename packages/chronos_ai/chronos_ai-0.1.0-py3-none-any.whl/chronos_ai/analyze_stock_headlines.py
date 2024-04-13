import yfinance as yf
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
import spacy.cli

from .CONSTANTS import ARTICLE_WEIGHT
from .extract_ticker_headlines import extract_ticker_headlines
from .get_full_article_text import get_full_article_text
from .get_yf_ticker_news import get_yf_ticker_news


def analyze_stock_headlines(ticker: str) -> float:
    r"""
    Perform sentiment analysis on the headlines of a ticker.
    """
    try:
        nlp = spacy.load("en_core_web_lg")
        nlp.add_pipe("spacytextblob")
    except:
        spacy.cli.download("en_core_web_lg")
        nlp = spacy.load("en_core_web_lg")
        nlp.add_pipe("spacytextblob")

    yf_ticker_news = get_yf_ticker_news(ticker)

    headlines = extract_ticker_headlines(yf_ticker_news)
    article_texts = [
        get_full_article_text(item["link"]) for item in yf_ticker_news
    ]
    headline_sentiment: float = 0.0
    article_sentiment: float = 0.0
    for headline in headlines:
        doc = nlp(headline)
        headline_sentiment += doc._.blob.polarity

    for text in article_texts:
        doc = nlp(text or "")
        article_sentiment += doc._.blob.polarity

    if len(headlines) > 0:
        headline_sentiment = headline_sentiment / len(headlines)

    if len(article_texts) > 0:
        article_sentiment = article_sentiment / len(article_texts)

    return (
        ARTICLE_WEIGHT * article_sentiment
        + (1 - ARTICLE_WEIGHT) * headline_sentiment
    )
