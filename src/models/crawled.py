import datetime as _dt
from typing import Any, Dict, List

import pydantic as _pydantic
import pymongo.collection as _collection
import pymongo.database as _db

from .constants import CRAWLED_COLLECTION_NAME


# !Crawled model
class CrawledModel(_pydantic.BaseModel):
    """Model for the items in crawled collection in the database"""

    id: float
    url: str
    status: str
    file_name: str
    rank: int
    title: str
    forward_links: list[str]
    tokens: dict[str, int]


# !Crawled database collection
class Crawled:
    """Crawled database collection"""

    collection: _collection.Collection[Dict[str, Any]]

    def __init__(self, db: _db.Database[Dict[str, Any]]) -> None:
        """Initializes the model class

        Args:
            db (_db.Database[Dict[str, Any]]): The database class
        """

        self.db = db
        self.collection = db[CRAWLED_COLLECTION_NAME]

    def is_exist(self, field: Dict[str, Any]) -> bool:
        """
        Checks if the particular link exists in database

        Args:
            field(Dict[str,Any]): The filter

        Return:
            bool: If the particular item exists
        """
        return bool(self.get_one(field))

    def add(
        self,
        url: str,
        status: str,
        file_name: str,
        rank: int = 1,
        title: str = "",
        forward_links: list[str] | None = None,
        tokens: dict[str, int] | None = None,
    ) -> Dict[str, Any]:
        """Creates a new item in the crawled collection in the database

        Args:
            url (str): The url to add
            status (str): The status of the url to add
            file_name (str): Name of the file where the html document of the link is stored
            rank (int, optional): The rank of the url. Defaults to 1.
            title (str, optional): Title of the page the url links to. Defaults to "".
            forward_links (list[str] | None, optional): All the links that the url's page links to. Defaults to None.
            tokens (dict[str, int] | None, optional): Token of the words on the page. Defaults to None.

        Returns:
            Dict[str, Any]: The newly added item
        """

        # !Verifies url using pydantic
        if forward_links is None:
            forward_links = []
        if tokens is None:
            tokens = {}

        link = CrawledModel(
            id=_dt.datetime.now().timestamp(),
            url=url,
            status=status,
            file_name=file_name,
            rank=rank,
            title=title,
            forward_links=forward_links,
            tokens=tokens,
        )

        # !Check if link already in database if it is returns it
        if self.is_exist({"url": link.url}):
            if item_in_db := self.get_one({"url": link.url}):
                return CrawledModel(**item_in_db).model_dump()

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

        item_in_db = self.collection.find_one(filter_keys)
        return None if item_in_db is None else CrawledModel(**item_in_db).model_dump()

    def get(self) -> List[Dict[str, str | int | float | list[str] | dict[str, int]]]:
        """Gets all the items in the collection"""
        return [CrawledModel(**item).model_dump() for item in self.collection.find()]

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
