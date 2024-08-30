from fastapi import FastAPI
from setup import setup
from crawler import Crawler as _Crawler
from general.constants import TO_PARSE_DIRECTORY, MAX_NUMBER_OF_THREADS


# !Background tasks to run while runing the API
def background_task() -> None:
    """Background tasks to run while runing the API"""
    db = setup()
    _Crawler(MAX_NUMBER_OF_THREADS, TO_PARSE_DIRECTORY, db)


app = FastAPI()
