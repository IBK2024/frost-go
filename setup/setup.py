from os import path as _path
import typing as _typing
import pymongo.database as _db
import config.database as _database
from general.constants import (
    DATABASE_NAME,
    MONGODB_URI,
    TO_PARSE_DIRECTORY,
    QUEUE_COLLECTION_NAME,
)
from general.create_directory import create_directory
from setup.constants import DEFAULT_STARTING_LINK
import models.queue as _queue


# !Setup fuction
def setup() -> _db.Database[_typing.Dict[str, _typing.Any]]:
    """
    Sets up the project.

    Does the following:
        - Connects to the database
        - Adds starting link if no other link in it.
        - Creates necessary folders.
    """

    db = _database.database_connect(MONGODB_URI, DATABASE_NAME)

    # !Make sure toParse directory exists
    if not _path.exists(TO_PARSE_DIRECTORY):
        create_directory(TO_PARSE_DIRECTORY)

    queue = _queue.Queue(db[QUEUE_COLLECTION_NAME])
    queue.add(DEFAULT_STARTING_LINK)

    return db
