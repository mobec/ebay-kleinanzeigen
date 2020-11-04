#!/usr/bin/env python3

# small debug application to debug the crawer

import argparse

from kleinanzeigen import scraper
import database
from search_task import SearchTask, SearchTaskState, run_search_task

parser = argparse.ArgumentParser()
parser.add_argument("urls", metavar='url', type=str, nargs='+', help="one or more urls containing ebay-kleinanzeigen.de searches.")
args = parser.parse_args()

if not isinstance(args.urls, list):
    args.urls = [args.urls]

for url in list(args.urls):
    database.tasks.append(SearchTask(url))

while True:
    for task in database.tasks:
        state = database.task_states.get(task, SearchTaskState())
        articles, state = run_search_task(task, state)
        database.task_states[task] = state
        if articles:
            print(articles)