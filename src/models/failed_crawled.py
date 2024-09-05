import datetime as _dt
import typing as _typing
import pydantic as _pydantic
import pymongo.collection as _collection
import pymongo.database as _db
from .constants import FAILED_CRAWLED_COLLECTION_NAME


# !Failed crawled model
class FailedCrawledModel(_pydantic.BaseModel):
    """Model for the items in failed crawled collection in the database"""

    id: float
    url: str
    reason: str


# !Failed crawled database collection
class FailedCrawled:
    """Failed crawled database collection"""

    collection: _collection.Collection[_typing.Dict[str, _typing.Any]]

    def __init__(self, db: _db.Database[_typing.Dict[str, _typing.Any]]) -> None:
        self.db = db
        self.collection = db[FAILED_CRAWLED_COLLECTION_NAME]

    def is_exist(self, filter_keys: _typing.Dict[str, _typing.Any]) -> bool:
        """
        Checks if the particular link exists in database
        """
        is_exist: _typing.Dict[str, _typing.Any] | None = self.get_one(filter_keys)

        if is_exist:
            return True

        return False

    def add(self, url: str, reason: str) -> _typing.Dict[str, _typing.Any]:
        """
        Creates a new item in the failed crawled collection in the database
        """

        # !Verifies url using pydantic
        link = FailedCrawledModel(id=_dt.datetime.today().timestamp(), url=url, reason=reason)

        # !Check if link already in database if it is returns it
        if self.is_exist({"url": link.url}):
            item_in_db = self.get_one({"url": link.url})

            if item_in_db:
                return FailedCrawledModel(**item_in_db).model_dump()

        # !If not in database creates a new instance.
        self.collection.insert_one(link.model_dump())

        # !Returns the inserted item
        return link.model_dump()

    def get_one(self, filter_keys: _typing.Dict[str, _typing.Any] | None) -> _typing.Dict[str, _typing.Any] | None:
        """Gets one item from the database using the given filter"""

        item_in_db = self.collection.find_one(filter_keys)
        if item_in_db is None:
            return None

        return FailedCrawledModel(**item_in_db).model_dump()

    def get(self) -> _typing.List[_typing.Dict[str, str | float]]:
        """Gets all the items in the collection"""
        return [FailedCrawledModel(**item).model_dump() for item in self.collection.find()]

    def remove(self, filter_keys: _typing.Dict[str, _typing.Any]) -> None:
        """Removes item from database"""
        self.collection.delete_many(filter_keys)
