from pytest import fixture

from src.general import get_scheme


class TestGetScheme:
    """Test get scheme function"""

    @staticmethod
    @fixture
    def mock_url1():
        """Mock url"""
        yield "https://google.com"

    @staticmethod
    @fixture
    def mock_url2():
        """Mock url"""
        yield "http://google.com"

    @staticmethod
    def test_mock_url1(mock_url1):
        """Test function using mock url 1"""
        assert get_scheme(mock_url1) == "https"

    @staticmethod
    def test_mock_url2(mock_url2):
        """Test function using mock url 2"""
        assert get_scheme(mock_url2) == "http"
