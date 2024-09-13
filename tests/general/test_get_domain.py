from pytest import fixture

from src.general import get_domain


class TestGetDomain:
    """Test get domain function"""

    @staticmethod
    @fixture
    def mock_url1():
        """Mock url 1"""
        yield "https://google.com"

    @staticmethod
    @fixture
    def mock_url2():
        """Mock url 2"""
        yield "http://abc.google.com"

    @staticmethod
    def test_using_mock_url1(mock_url1):
        """Test function using mock url 1"""
        assert get_domain(mock_url1) == "google.com"

    @staticmethod
    def test_using_mock_url2(mock_url2):
        """Test function using mock url 2"""
        assert get_domain(mock_url2) == "google.com"
