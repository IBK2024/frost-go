import typing as _typing
import pymongo.database as _db
import config.database as database
from general.constants import DATABASE_NAME, MONGODB_URI


# !Setup fuction
def setup() -> _db.Database[_typing.Dict[str, _typing.Any]]:
    """
    Sets up the project.

    Does the following:
      - Connects to the database
      - Adds starting link if no other link in it.
      - Creates necessary folders.
    """

    db = database.database_connect(MONGODB_URI, DATABASE_NAME)

    return db
