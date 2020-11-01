#!/usr/bin/env python3

# small debug application to debug the crawer

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("urls", metavar='url', type=str, nargs='+', help="one or more urls containing ebay-kleinanzeigen.de searches.")
args = parser.parse_args()

import scraper

if not isinstance(args.urls, list):
    args.urls = [args.urls]

for url in list(args.urls):
    articles = scraper.scrape_url(url)
    print(articles)