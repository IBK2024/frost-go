import datetime as _datetime
from typing import Any as _any, Generator as _generator, Literal as _literal
import pytest as _pytest
import mongomock as _mongomock
import models.queue as _queue
from general.constants import QUEUE_COLLECTION_NAME


class TestQueue:
    """Tests the queue model"""

    @_pytest.fixture
    @staticmethod
    def mock_client():
        """Mock mongodb client"""
        yield _mongomock.MongoClient()

    @_pytest.fixture
    @staticmethod
    def mock_db(mock_client):
        """Mock database"""
        yield mock_client["db"]

    @_pytest.fixture
    @staticmethod
    def mock_queue_item():
        """Fake queue model item"""
        yield _queue.QueueModel(id=_datetime.datetime.today().timestamp(), url="https://google.com")

    @staticmethod
    def test_is_exist(mock_queue_item, mock_db) -> None:
        """Test is exist model function"""
        queue = _queue.Queue(mock_db)

        # !Test if the link doesn't exist
        assert not queue.is_exist({"id": mock_queue_item.id})
        assert not queue.is_exist({"url": mock_queue_item.url})

        # !Test if the link exists
        mock_db[QUEUE_COLLECTION_NAME].insert_one(mock_queue_item.model_dump())

        assert queue.is_exist({"url": mock_queue_item.url})
        assert queue.is_exist({"id": mock_queue_item.id})

    @staticmethod
    def test_add(mock_queue_item, mock_db) -> None:
        """Test add model function"""
        queue = _queue.Queue(mock_db)

        # !Test add
        queue.add(mock_queue_item.url)
        assert len(list(mock_db[QUEUE_COLLECTION_NAME].find())) == 1
        assert list(mock_db[QUEUE_COLLECTION_NAME].find())[0]["url"] == mock_queue_item.url

        # !Test adding if url already exists
        item_id = list(mock_db[QUEUE_COLLECTION_NAME].find())[0]["id"]
        queue.add(mock_queue_item.url)
        assert len(list(mock_db[QUEUE_COLLECTION_NAME].find())) == 1
        assert list(mock_db[QUEUE_COLLECTION_NAME].find())[0]["url"] == mock_queue_item.url
        assert list(mock_db[QUEUE_COLLECTION_NAME].find())[0]["id"] == item_id

    @staticmethod
    def test_get_one(mock_queue_item, mock_db) -> None:
        """Test get one model function"""
        queue = _queue.Queue(mock_db)

        queue.add(mock_queue_item.url)

        # !Test function
        item = list(mock_db[QUEUE_COLLECTION_NAME].find())[0]
        print(item)
        assert queue.get_one({"url": item["url"]})
        assert queue.get_one({"id": item["id"]})

    @staticmethod
    def test_get(mock_queue_item, mock_db) -> None:
        """Test get model function"""
        queue = _queue.Queue(mock_db)

        queue.add(mock_queue_item.url)

        # !Test function
        assert len(queue.get()) == 1

        item = queue.get_one({"url": mock_queue_item.url})
        assert queue.get()[0]["url"] == item["url"]
        assert queue.get()[0]["id"] == item["id"]
