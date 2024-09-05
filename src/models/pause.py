import datetime as _dt
import typing as _typing
import pydantic as _pydantic
import pymongo.collection as _collection
import pymongo.database as _db
from .constants import PAUSE_COLLECTION_NAME


# !Pause model
class PauseModel(_pydantic.BaseModel):
    """Model for the items in pause collection in the database"""

    id: float
    url: str
    exp_date: float


# !Pause database collection
class Pause:
    """Pause database collection"""

    collection: _collection.Collection[_typing.Dict[str, _typing.Any]]

    def __init__(self, db: _db.Database[_typing.Dict[str, _typing.Any]]) -> None:
        self.db = db
        self.collection = db[PAUSE_COLLECTION_NAME]

    def is_exist(self, field: _typing.Dict[str, _typing.Any]) -> bool:
        """
        Checks if the particular link exists in database
        """
        is_exist: _typing.Dict[str, _typing.Any] | None = self.get_one(field)

        if is_exist:
            return True

        return False

    def add(self, url: str) -> _typing.Dict[str, _typing.Any]:
        """
        Creates a new item in the pause collection in the database
        """

        # !Verifies url using pydantic
        link = PauseModel(
            id=_dt.datetime.today().timestamp(),
            url=url,
            exp_date=(_dt.datetime.now() + _dt.timedelta(days=30)).timestamp(),
        )

        # !Check if link already in database if it is returns it
        if self.is_exist({"url": link.url}):
            item_in_db = self.get_one({"url": link.url})

            if item_in_db:
                return PauseModel(**item_in_db).model_dump()

        # !If not in database creates a new instance.
        self.collection.insert_one(link.model_dump())

        # !Returns the inserted item
        return link.model_dump()

    def get_one(self, filter_keys: _typing.Dict[str, _typing.Any] | None) -> _typing.Dict[str, _typing.Any] | None:
        """Gets one item from the database using the given filter"""

        item_in_db = self.collection.find_one(filter_keys)
        if item_in_db is None:
            return None

        return PauseModel(**item_in_db).model_dump()

    def get(self) -> _typing.List[_typing.Dict[str, str | float]]:
        """Gets all the items in the collection"""
        return [PauseModel(**item).model_dump() for item in self.collection.find()]

    def remove(self, filter_keys: _typing.Dict[str, _typing.Any]) -> None:
        """Removes item from database"""
        self.collection.delete_many(filter_keys)
