from os import path as _path
import typing as _typing
import pymongo.database as _db
from .database import database_connect
from .general import create_directory
from .constants import DATABASE_NAME, MONGODB_URI, TO_PARSE_DIRECTORY, DEFAULT_STARTING_LINK
from .models import queue as _queue


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

    queue = _queue.Queue(db)
    queue.add(DEFAULT_STARTING_LINK)

    return db
