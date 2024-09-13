import datetime as _dt
from typing import Any, Dict, List

import pydantic as _pydantic
import pymongo.collection as _collection
import pymongo.database as _db

from .constants import QUEUE_COLLECTION_NAME


# !Queue model
class QueueModel(_pydantic.BaseModel):
    """Model for the items in queue collection in the database"""

    id: float
    url: str


# !Queue database collection
class Queue:
    """Queue database collection"""

    collection: _collection.Collection[Dict[str, Any]]
    db: _db.Database[Dict[str, Any]]

    def __init__(self, db: _db.Database[Dict[str, Any]]) -> None:
        """Initializes the model class

        Args:
            db (_db.Database[Dict[str, Any]]): The database class
        """
        self.db = db
        self.collection = db[QUEUE_COLLECTION_NAME]

    def is_exist(self, field: Dict[str, Any]) -> bool:
        """
        Checks if the particular link exists in database

        Args:
            field(Dict[str,Any]): The filter

        Return:
            bool: If the particular item exists
        """
        return bool(self.get_one(field))

    def add(self, url: str) -> Dict[str, Any]:
        """Creates a new item in the queue collection in the database

        Args:
            url (str): The url to add

        Returns:
            Dict[str, Any]: The newly added item
        """

        # !Verifies url using pydantic
        link = QueueModel(id=_dt.datetime.now().timestamp(), url=url)

        # !Check if link already in database if it is returns it
        if self.is_exist({"url": link.url}):
            if item_in_db := self.get_one({"url": link.url}):
                return QueueModel(**item_in_db).model_dump()

        # !If not in database creates a new instance.
        self.collection.insert_one(link.model_dump())

        # !Returns the inserted item
        return link.model_dump()

    def get_one(self, filter_keys: Dict[str, Any] | None) -> Dict[str, Any] | None:
        """Gets one item from the database using the given filter

        Args:
            filter_keys (Dict[str, Any] | None): The filter

        Returns:
            Dict[str, Any] | None: Returns the item if found and none if not found
        """

        if item_in_db := self.collection.find_one(filter_keys):
            return QueueModel(**item_in_db).model_dump()

        return item_in_db

    def get(self) -> List[Dict[str, str | float]]:
        """Gets all the items in the collection"""
        return [QueueModel(**item).model_dump() for item in self.collection.find()]

    def remove(self, filter_keys: Dict[str, Any]) -> None:
        """Removes item from database

        Args:
            filter_keys (Dict[str, Any]): The filter
        """
        self.collection.delete_many(filter_keys)

    def update(
        self,
        filter_keys: Dict[str, Any],
        keys: dict[str, str | int | float | list[str] | dict[str, int]],
    ) -> None:
        """Updates an item in the database

        Args:
            filter_keys (Dict[str, Any]): The filter to use to get the item to update
            keys (dict[str, str  |  int  |  float  |  list[str]  |  dict[str, int]]): The keys to update
        """
        self.collection.update_one(filter_keys, {"$set": keys})
