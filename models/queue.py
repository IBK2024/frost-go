import datetime as _dt
import typing as _typing
import pydantic as _pydantic
import pymongo.collection as _collection


# !Queue model
class QueueModel(_pydantic.BaseModel):
    """Model for the items in queue collection in the database"""

    id: float
    url: str


# !Queue database collection
class Queue:
    """Queue database collection"""

    collection: _collection.Collection[_typing.Dict[str, _typing.Any]]

    def __init__(self, collection: _collection.Collection[_typing.Dict[str, _typing.Any]]) -> None:
        self.collection = collection

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
        Creates a new item in the queue collection in the database
        """

        # !Verifies url using pydantic
        link = QueueModel(id=_dt.datetime.today().timestamp(), url=url)

        # !Check if link already in database if it is returns it
        if self.is_exist({"url": link.url}):
            item_in_db = self.get_one({"url": link.url})

            if item_in_db:
                return QueueModel(**item_in_db).model_dump()

        # !If not in database creates a new instance.
        self.collection.insert_one(link.model_dump())

        # !Returns the inserted item
        return link.model_dump()

    def get_one(self, filter_keys: _typing.Dict[str, _typing.Any] | None) -> _typing.Dict[str, _typing.Any] | None:
        """Gets one item from the database using the given filter"""

        item_in_db = self.collection.find_one(filter_keys)
        if item_in_db is None:
            return None

        return QueueModel(**item_in_db).model_dump()
