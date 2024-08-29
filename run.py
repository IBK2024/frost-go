from fastapi import FastAPI
from setup import setup


# !Background tasks to run while runing the API
def background_task() -> None:
    """Background tasks to run while runing the API"""
    setup()


app = FastAPI()
