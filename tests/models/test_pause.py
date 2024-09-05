import datetime as _datetime
from typing import Any as _any, Generator as _generator, Literal as _literal
import pytest as _pytest
import mongomock as _mongomock
import src.models.pause as _pause
from src.models.constants import PAUSE_COLLECTION_NAME


class TestPause:
    """Tests the pause model"""

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
    def mock_pause_item():
        """Fake pause model item"""
        yield _pause.PauseModel(
            id=_datetime.datetime.today().timestamp(),
            url="https://google.com",
            exp_date=(_datetime.datetime.now() + _datetime.timedelta(days=30)).timestamp(),
        )

    @staticmethod
    def test_is_exist(mock_pause_item, mock_db) -> None:
        """Test is exist model function"""
        pause = _pause.Pause(mock_db)

        # !Test if the link doesn't exist
        assert not pause.is_exist({"id": mock_pause_item.id})
        assert not pause.is_exist({"url": mock_pause_item.url})

        # !Test if the link exists
        mock_db[PAUSE_COLLECTION_NAME].insert_one(mock_pause_item.model_dump())

        assert pause.is_exist({"url": mock_pause_item.url})
        assert pause.is_exist({"id": mock_pause_item.id})

    @staticmethod
    def test_add(mock_pause_item, mock_db) -> None:
        """Test add model function"""
        pause = _pause.Pause(mock_db)

        # !Test add
        pause.add(mock_pause_item.url)
        assert len(list(mock_db[PAUSE_COLLECTION_NAME].find())) == 1
        assert list(mock_db[PAUSE_COLLECTION_NAME].find())[0]["url"] == mock_pause_item.url

        # !Test adding if url already exists
        item_id = list(mock_db[PAUSE_COLLECTION_NAME].find())[0]["id"]
        pause.add(mock_pause_item.url)
        assert len(list(mock_db[PAUSE_COLLECTION_NAME].find())) == 1
        assert list(mock_db[PAUSE_COLLECTION_NAME].find())[0]["url"] == mock_pause_item.url
        assert list(mock_db[PAUSE_COLLECTION_NAME].find())[0]["id"] == item_id

    @staticmethod
    def test_get_one(mock_pause_item, mock_db) -> None:
        """Test get one model function"""
        pause = _pause.Pause(mock_db)

        pause.add(mock_pause_item.url)

        # !Test function
        item = list(mock_db[PAUSE_COLLECTION_NAME].find())[0]
        print(item)
        assert pause.get_one({"url": item["url"]})
        assert pause.get_one({"id": item["id"]})

    @staticmethod
    def test_get(mock_pause_item, mock_db) -> None:
        """Test get model function"""
        pause = _pause.Pause(mock_db)

        pause.add(mock_pause_item.url)

        # !Test function
        assert len(pause.get()) == 1

        item = pause.get_one({"url": mock_pause_item.url})
        assert pause.get()[0]["url"] == item["url"]
        assert pause.get()[0]["id"] == item["id"]

    @staticmethod
    def test_remove(mock_pause_item, mock_db) -> None:
        """Test the remove model function"""
        pause = _pause.Pause(mock_db)

        pause.add(mock_pause_item.url)
        pause.remove({"url": mock_pause_item.url})

        # !Test function
        assert len(pause.get()) == 0
        assert pause.get_one({"url": mock_pause_item.url}) is None
