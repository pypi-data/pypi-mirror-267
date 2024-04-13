from bs4 import BeautifulSoup
import requests

headers = {
    "accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53",
    "Accept-Language": "en-US,en;q=0.9,it;q=0.8,es;q=0.7",
    "referer": "https://www.google.com/",
    "cookie": "DSID=AAO-7r4OSkS76zbHUkiOpnI0kk-X19BLDFF53G8gbnd21VZV2iehu-w_2v14cxvRvrkd_NjIdBWX7wUiQ66f-D8kOkTKD1BhLVlqrFAaqDP3LodRK2I0NfrObmhV9HsedGE7-mQeJpwJifSxdchqf524IMh9piBflGqP0Lg0_xjGmLKEQ0F4Na6THgC06VhtUG5infEdqMQ9otlJENe3PmOQTC_UeTH5DnENYwWC8KXs-M4fWmDADmG414V0_X0TfjrYu01nDH2Dcf3TIOFbRDb993g8nOCswLMi92LwjoqhYnFdf1jzgK0",
}


def get_full_article_text(yfinance_article_url: str):
    try:
        return get_body_text(yfinance_article_url)
    except:
        return get_readmore_link(yfinance_article_url)


def get_body_text(yfinance_article_url: str):
    html_response = requests.get(yfinance_article_url, headers=headers)
    soup = BeautifulSoup(html_response.text, features="lxml")
    full_article_text = soup.select("div.caas-body")[0].text

    return full_article_text


def get_readmore_link(yfinance_article_url: str):
    print("yfinance_article_url:", yfinance_article_url)
    html_response = requests.get(yfinance_article_url, headers=headers)
    if html_response.status_code == 404:
        return ""

    print("html_response:", html_response)
    soup = BeautifulSoup(html_response.text, features="lxml")
    print("soup:", soup)
    full_article_link = soup.find("Continue Reading")
    print("full_article_link:", full_article_link)

    print("full_article_link:", full_article_link)

    full_article_text = requests.get(full_article_link, headers=headers).text
    print("full_article_text:", full_article_text)

    exit()

    return full_article_text
