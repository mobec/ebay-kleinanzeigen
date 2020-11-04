from kleinanzeigen.article import Article

from typing import List
import requests

from dateutil import parser as dparser
import datetime

import re

from bs4 import BeautifulSoup

def scrape_articles_list(html: str) -> List[Article]:
    soup = BeautifulSoup(html, 'html.parser')

    articles = soup.find_all("article", attrs={"class":"aditem"})

    scraped_articles = []
    for article in articles:
        # parse article ID
        ebay_kleinanzeigen_id = int(article.get('data-adid'))
        
        # name
        article_ellipsis = article.find("a", attrs={"class": "ellipsis"})
        name = article_ellipsis.string.strip()
        
        # url
        relative_url = article_ellipsis.get("href")

        # price
        article_details_price = article.find(attrs={"class": "aditem-details"}).find("strong")
        if not article_details_price or not article_details_price.string:
            # this is an ad tarned as article
            continue
        price_line = article_details_price.string.strip()
        price = price_line

        # time
        article_addon = article.find(attrs={"class": "aditem-addon"})
        if not article_addon or not article_addon.string:
            # this is an ad tarned as article
            continue
        article_date = article_addon.string.strip()
        time = dparser.parse(article_date, fuzzy=True, dayfirst=True)
        if "Gestern" in article_date:
            time = datetime.datetime.combine(datetime.date.today() - datetime.timedelta(days=1), time.time())
        if "Heute" in article_date:
            time = datetime.datetime.combine(datetime.date.today(), time.time())

        scraped_articles.append(Article(ebay_kleinanzeigen_id, name, price, relative_url, time))

    return scraped_articles

def scrape_url(url: str) -> List[Article]:
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    qq = requests.get(url, headers={'User-Agent': user_agent})
    text = qq.text

    return scrape_articles_list(text)
