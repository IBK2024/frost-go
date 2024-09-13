import math

import uvicorn
from fastapi import FastAPI

from .constants import MAX_NUMBER_OF_THREADS, TO_PARSE_DIRECTORY
from .crawler import Crawler as _Crawler
from .parser import Parser as _Parser
from .setup import setup


# !Main code
async def main() -> None:
    """
    Main Code does the following:
        - Starts the uvicorn server
        - Runs background tasks
    """
    background_task()
    config = uvicorn.Config(app, port=5000, log_level="info", reload=True)
    server = uvicorn.Server(config)
    await server.serve()


# !Background tasks to run while runing the API
def background_task() -> None:
    """Background tasks to run while runing the API"""
    db = setup()
    _Crawler(math.ceil(MAX_NUMBER_OF_THREADS / 2), TO_PARSE_DIRECTORY, db)
    _Parser(math.ceil(MAX_NUMBER_OF_THREADS / 2), TO_PARSE_DIRECTORY, db)


app = FastAPI()
