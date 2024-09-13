import typing as _typing
from os import path as _path

import pymongo.database as _db

from .config.database import database_connect
from .constants import (
    DATABASE_NAME,
    DEFAULT_STARTING_LINK,
    MONGODB_URI,
    TO_PARSE_DIRECTORY,
)
from .general import create_directory
from .models import Crawled, Queue


# !Setup fuction
def setup() -> _db.Database[_typing.Dict[str, _typing.Any]]:
    """
    Sets up the project.

    Does the following:
        - Connects to the database
        - Adds starting link if no other link in it.
        - Creates necessary folders.
    """

    db = database_connect(MONGODB_URI, DATABASE_NAME)

    # !Make sure toParse directory exists
    if not _path.exists(TO_PARSE_DIRECTORY):
        create_directory(TO_PARSE_DIRECTORY)

    queue = Queue(db)
    crawled = Crawled(db)

    if len(crawled.get()) == 0 and len(queue.get()) == 0:
        queue.add(DEFAULT_STARTING_LINK)

    return db
