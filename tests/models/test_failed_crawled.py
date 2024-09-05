import datetime as _datetime
from typing import Any as _any, Generator as _generator, Literal as _literal
import pytest as _pytest
import mongomock as _mongomock
import src.models.failed_crawled as _failed_crawled
from src.models.constants import FAILED_CRAWLED_COLLECTION_NAME


class TestFailedCrawled:
    """Tests the failed crawled model"""

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
    def mock_reason():
        """Fake failed crawled reason"""
        yield "test reson"

    @_pytest.fixture
    @staticmethod
    def mock_failed_crawled_item(mock_reason):
        """Fake failed crawled model item"""
        yield _failed_crawled.FailedCrawledModel(
            id=_datetime.datetime.today().timestamp(), url="https://google.com", reason=mock_reason
        )

    @staticmethod
    def test_is_exist(mock_failed_crawled_item, mock_db) -> None:
        """Test is exist model function"""
        failed_crawled = _failed_crawled.FailedCrawled(mock_db)

        # !Test if the link doesn't exist
        assert not failed_crawled.is_exist({"id": mock_failed_crawled_item.id})
        assert not failed_crawled.is_exist({"url": mock_failed_crawled_item.url})

        # !Test if the link exists
        mock_db[FAILED_CRAWLED_COLLECTION_NAME].insert_one(mock_failed_crawled_item.model_dump())

        assert failed_crawled.is_exist({"url": mock_failed_crawled_item.url})
        assert failed_crawled.is_exist({"id": mock_failed_crawled_item.id})

    @staticmethod
    def test_add(mock_failed_crawled_item, mock_db, mock_reason) -> None:
        """Test add model function"""
        failed_crawled = _failed_crawled.FailedCrawled(mock_db)

        # !Test add
        failed_crawled.add(mock_failed_crawled_item.url, mock_reason)
        assert len(list(mock_db[FAILED_CRAWLED_COLLECTION_NAME].find())) == 1
        assert list(mock_db[FAILED_CRAWLED_COLLECTION_NAME].find())[0]["url"] == mock_failed_crawled_item.url
        assert list(mock_db[FAILED_CRAWLED_COLLECTION_NAME].find())[0]["reason"] == mock_failed_crawled_item.reason

        # !Test adding if url already exists
        item_id = list(mock_db[FAILED_CRAWLED_COLLECTION_NAME].find())[0]["id"]
        failed_crawled.add(mock_failed_crawled_item.url, mock_reason)
        assert len(list(mock_db[FAILED_CRAWLED_COLLECTION_NAME].find())) == 1
        assert list(mock_db[FAILED_CRAWLED_COLLECTION_NAME].find())[0]["url"] == mock_failed_crawled_item.url
        assert list(mock_db[FAILED_CRAWLED_COLLECTION_NAME].find())[0]["id"] == item_id

    @staticmethod
    def test_get_one(mock_failed_crawled_item, mock_db, mock_reason) -> None:
        """Test get one model function"""
        failed_crawled = _failed_crawled.FailedCrawled(mock_db)

        failed_crawled.add(mock_failed_crawled_item.url, mock_reason)

        # !Test function
        item = list(mock_db[FAILED_CRAWLED_COLLECTION_NAME].find())[0]
        print(item)
        assert failed_crawled.get_one({"url": item["url"]})
        assert failed_crawled.get_one({"id": item["id"]})

    @staticmethod
    def test_get(mock_failed_crawled_item, mock_db, mock_reason) -> None:
        """Test get model function"""
        failed_crawled = _failed_crawled.FailedCrawled(mock_db)

        failed_crawled.add(mock_failed_crawled_item.url, mock_reason)

        # !Test function
        assert len(failed_crawled.get()) == 1

        item = failed_crawled.get_one({"url": mock_failed_crawled_item.url})
        assert failed_crawled.get()[0]["url"] == item["url"]
        assert failed_crawled.get()[0]["id"] == item["id"]

    @staticmethod
    def test_remove(mock_failed_crawled_item, mock_db, mock_reason) -> None:
        """Test the remove model function"""
        failed_crawled = _failed_crawled.FailedCrawled(mock_db)

        failed_crawled.add(mock_failed_crawled_item.url, mock_reason)
        failed_crawled.remove({"url": mock_failed_crawled_item.url})

        # !Test function
        assert len(failed_crawled.get()) == 0
        assert failed_crawled.get_one({"url": mock_failed_crawled_item.url}) is None
