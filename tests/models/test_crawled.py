import datetime as _datetime
from typing import Any as _any
from typing import Generator as _generator
from typing import Literal as _literal

import mongomock as _mongomock
import pytest as _pytest

import src.models.crawled as _crawled
from src.models.constants import CRAWLED_COLLECTION_NAME


class TestCrawled:
    """Tests the crawled model"""

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
    def mock_crawled_item():
        """Fake crawled model item"""
        yield _crawled.CrawledModel(
            id=_datetime.datetime.today().timestamp(),
            url="https://google.com",
            status="test_status",
            file_name="test_filename",
            rank=1,
            title="",
            forward_links=[],
            tokens={},
        )

    @staticmethod
    def test_is_exist(mock_crawled_item, mock_db) -> None:
        """Test is exist model function"""
        crawled = _crawled.Crawled(mock_db)

        # !Test if the link doesn't exist
        assert not crawled.is_exist({"id": mock_crawled_item.id})
        assert not crawled.is_exist({"url": mock_crawled_item.url})

        # !Test if the link exists
        mock_db[CRAWLED_COLLECTION_NAME].insert_one(mock_crawled_item.model_dump())

        assert crawled.is_exist({"url": mock_crawled_item.url})
        assert crawled.is_exist({"id": mock_crawled_item.id})

    @staticmethod
    def test_add(mock_crawled_item, mock_db) -> None:
        """Test add model function"""
        crawled = _crawled.Crawled(mock_db)

        # !Test add
        crawled.add(mock_crawled_item.url, mock_crawled_item.status, mock_crawled_item.file_name)
        assert len(list(mock_db[CRAWLED_COLLECTION_NAME].find())) == 1
        assert list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["url"] == mock_crawled_item.url
        assert list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["status"] == mock_crawled_item.status
        assert list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["file_name"] == mock_crawled_item.file_name

        # !Test adding if url already exists
        item_id = list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["id"]
        crawled.add(mock_crawled_item.url, mock_crawled_item.status, mock_crawled_item.file_name)
        assert len(list(mock_db[CRAWLED_COLLECTION_NAME].find())) == 1
        assert list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["url"] == mock_crawled_item.url
        assert list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["id"] == item_id

    @staticmethod
    def test_get_one(mock_crawled_item, mock_db) -> None:
        """Test get one model function"""
        crawled = _crawled.Crawled(mock_db)

        crawled.add(mock_crawled_item.url, mock_crawled_item.status, mock_crawled_item.file_name)

        # !Test function
        item = list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]
        print(item)
        assert crawled.get_one({"url": item["url"]})
        assert crawled.get_one({"id": item["id"]})

    @staticmethod
    def test_get(mock_crawled_item, mock_db) -> None:
        """Test get model function"""
        crawled = _crawled.Crawled(mock_db)

        crawled.add(mock_crawled_item.url, mock_crawled_item.status, mock_crawled_item.file_name)

        # !Test function
        assert len(crawled.get()) == 1

        item = crawled.get_one({"url": mock_crawled_item.url})
        assert crawled.get()[0]["url"] == item["url"]
        assert crawled.get()[0]["id"] == item["id"]

    @staticmethod
    def test_remove(mock_crawled_item, mock_db) -> None:
        """Test the remove model function"""
        crawled = _crawled.Crawled(mock_db)

        crawled.add(mock_crawled_item.url, mock_crawled_item.status, mock_crawled_item.file_name)
        crawled.remove({"url": mock_crawled_item.url})

        # !Test function
        assert len(crawled.get()) == 0
        assert crawled.get_one({"url": mock_crawled_item.url}) is None

    @staticmethod
    def test_update(mock_crawled_item, mock_db) -> None:
        """Test the update model function"""
        crawled = _crawled.Crawled(mock_db)
        new_item = crawled.add(mock_crawled_item.url, mock_crawled_item.status, mock_crawled_item.file_name)

        assert new_item["url"] == mock_crawled_item.url

        # !Test update
        crawled.update({"id": new_item["id"]}, {"url": "abc"})
        assert crawled.get_one({"id": new_item["id"]})["url"] == "abc"
        assert not crawled.get_one({"id": new_item["id"]})["url"] == mock_crawled_item.url
