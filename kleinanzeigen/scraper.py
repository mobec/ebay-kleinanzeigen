from article import Article
from typing import List
import requests

import logging

import re

def scrape_str(text: str) -> List[Article]:
    articles = re.findall('<article(.*?)</article', text, re.S)

    items = []
    for item in articles:
        if results := re.findall('<a.*?href="(.*?)">(.*?)</a>', item, re.S):
            url, name = results[0]
        else:
            continue

        price_line = re.findall('<strong>(.*?)</strong>', item, re.S)[0]
        negotiable = 'VB' in price_line
        price = None
        if prices := re.findall(r'\d+', price_line, re.S):
            price = int(prices[0])

        date = re.findall('aditem-addon">(.*?)</', item, re.S)[0].strip()
        if '{' in date or '<' in date:
            continue

        try:
            image = re.findall('imgsrc="(.*?)"', item, re.S)[0].strip()
        except Exception as e:
            logging.error(f'No image\n\t{item}')
            continue

        items.append(Article(name, price, negotiable, url, date, image))

    return items

def scrape_url(url: str) -> List[Article]:
    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'
    qq = requests.get(url, headers={'User-Agent': user_agent})
    text = qq.text

    return scrape_str(text)
