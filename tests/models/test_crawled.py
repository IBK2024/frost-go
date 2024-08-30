import datetime as _datetime
from typing import Any as _any, Generator as _generator, Literal as _literal
import pytest as _pytest
import mongomock as _mongomock
import models.crawled as _crawled
from general.constants import CRAWLED_COLLECTION_NAME


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
        yield _crawled.CrawledModel(id=_datetime.datetime.today().timestamp(), url="https://google.com")

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
        crawled.add(mock_crawled_item.url)
        assert len(list(mock_db[CRAWLED_COLLECTION_NAME].find())) == 1
        assert list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["url"] == mock_crawled_item.url

        # !Test adding if url already exists
        item_id = list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["id"]
        crawled.add(mock_crawled_item.url)
        assert len(list(mock_db[CRAWLED_COLLECTION_NAME].find())) == 1
        assert list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["url"] == mock_crawled_item.url
        assert list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]["id"] == item_id

    @staticmethod
    def test_get_one(mock_crawled_item, mock_db) -> None:
        """Test get one model function"""
        crawled = _crawled.Crawled(mock_db)

        crawled.add(mock_crawled_item.url)

        # !Test function
        item = list(mock_db[CRAWLED_COLLECTION_NAME].find())[0]
        print(item)
        assert crawled.get_one({"url": item["url"]})
        assert crawled.get_one({"id": item["id"]})

    @staticmethod
    def test_get(mock_crawled_item, mock_db) -> None:
        """Test get model function"""
        crawled = _crawled.Crawled(mock_db)

        crawled.add(mock_crawled_item.url)

        # !Test function
        assert len(crawled.get()) == 1

        item = crawled.get_one({"url": mock_crawled_item.url})
        assert crawled.get()[0]["url"] == item["url"]
        assert crawled.get()[0]["id"] == item["id"]
