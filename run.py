from fastapi import FastAPI
from general.constants import DATABASE_NAME, MONGODB_URI
from config.database import database_connect


# !Background tasks to run while runing the API
def background_task() -> None:
    """Background tasks to run while runing the API"""
    db = database_connect(MONGODB_URI, DATABASE_NAME)


app = FastAPI()
