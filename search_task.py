# this file manages the jobs that are created by the user

from dataclasses import dataclass
from datetime import datetime

from typing import List, Tuple

from kleinanzeigen import scraper
from kleinanzeigen import article
# TODO: make this persistent
# for now the jobstore is just a dictionary. 

@dataclass(eq=True, frozen=True, repr=True)
class SearchTask:
    """The parameters of the search task (never change)"""
    url: str

@dataclass
class SearchTaskState:
    """The (mutable) state associated with the search task"""
    latest_article_date: datetime = datetime.now()

def run_search_task(task: SearchTask, state: SearchTaskState) -> Tuple[List[article.Article], SearchTaskState]:
    articles = scraper.scrape_url(task.url)
    if not articles:
        # nothing found, nothing to do
        return articles, state

    articles = filter(lambda article: article.date > state.latest_article_date, articles)
    articles = sorted(articles, key=lambda article: article.date)
    
    if articles:
        state.latest_article_date = articles[-1].date
    
    return articles, state
    