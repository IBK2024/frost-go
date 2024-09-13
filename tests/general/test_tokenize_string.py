from pytest import fixture

from src.general import tokenize_string


class TestTokenizeString:
    """Test tokenize string function"""

    @staticmethod
    @fixture
    def mock_string():
        """Mock string"""
        yield "This is a fake string. And this is another fake string"

    @staticmethod
    @fixture
    def expected_output():
        """Expected output"""
        yield {"This": 1, "fake": 2, "string": 2, "And": 1, "another": 1}

    @staticmethod
    def test_mock_url1(mock_string, expected_output):
        """Test tokenize string function"""
        assert len(tokenize_string(mock_string)) == 5
        for word in tokenize_string(mock_string):
            assert tokenize_string(mock_string)[word] == expected_output[word]
