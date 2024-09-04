from src.crawler.get_robots_txt_url import get_robots_txt_url


class TestGetRobotsTxtUrl:
    """Test get robots.txt"""

    @staticmethod
    def test_regular_url():
        "Test regular url"
        assert get_robots_txt_url("https://google.com") == "https://google.com/robots.txt"

    @staticmethod
    def test_url_with_multiple_sub_domains():
        "Test url with multiple sub domains"
        assert get_robots_txt_url("https://abc.abc.google.com") == "https://google.com/robots.txt"
