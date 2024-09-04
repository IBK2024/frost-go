import pytest
import src.crawler.check_robots_txt as _check_robots_txt


class TestCheckRobotTxt:
    """Test the queue model"""

    @pytest.fixture
    @staticmethod
    def mock_url():
        """Fake url"""
        yield "https://abc.com/a"

    @pytest.fixture
    @staticmethod
    def mock_bot_name():
        """Mock bot name"""
        yield "FrostBot"

    @pytest.fixture
    @staticmethod
    def mock_robots_txt1():
        """Mock robots.txt file that disallows crawling for all robots"""
        with open("./tests/crawler/robot_txt/disallow_all_robots.txt", "r", encoding="utf-8") as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt2():
        """Mock robots.txt file that allows crawling for all robots"""
        with open("./tests/crawler/robot_txt/allow_all_robots.txt", "r", encoding="utf-8") as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt3():
        """Mock robots.txt file that allows crawling for frost bot"""
        with open("./tests/crawler/robot_txt/allow_frost_robots.txt", "r", encoding="utf-8") as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt4():
        """Mock robots.txt file that disallows crawling for frost bot"""
        with open("./tests/crawler/robot_txt/disallow_frost_robots.txt", "r", encoding="utf-8") as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt5():
        """
        Mock robots.txt file that allows crawling for frost bot by overriding the disallow for other
        bots
        """
        with open(
            "./tests/crawler/robot_txt/override_disallow_robots.txt",
            "r",
            encoding="utf-8",
        ) as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt6():
        """
        Mock robots.txt file that disallows crawling for frost bot by overriding the
        allow for other bots
        """
        with open(
            "./tests/crawler/robot_txt/override_allow_robots.txt",
            "r",
            encoding="utf-8",
        ) as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt7():
        """
        Mock robots.txt file that allows crawling for frost bot by overriding the allow for other
        bots
        """
        with open(
            "./tests/crawler/robot_txt/override_allow_with_allow_robots.txt",
            "r",
            encoding="utf-8",
        ) as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt8():
        """
        Mock robots.txt file that disallows crawling for frost bot by overriding the
        disallow for other bots
        """
        with open(
            "./tests/crawler/robot_txt/override_disallow_with_disallow_robots.txt",
            "r",
            encoding="utf-8",
        ) as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt9():
        """Mock robots.txt file that disallows crawling for all robots"""
        with open("./tests/crawler/robot_txt/disallow_all_robots2.txt", "r", encoding="utf-8") as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt10():
        """Mock robots.txt file that allows crawling for all robots"""
        with open("./tests/crawler/robot_txt/allow_all_robots2.txt", "r", encoding="utf-8") as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt11():
        """Mock robots.txt file that allows crawling for frost bot"""
        with open("./tests/crawler/robot_txt/allow_frost_robots2.txt", "r", encoding="utf-8") as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt12():
        """Mock robots.txt file that disallows crawling for frost bot"""
        with open("./tests/crawler/robot_txt/disallow_frost_robots2.txt", "r", encoding="utf-8") as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt13():
        """
        Mock robots.txt file that allows crawling for frost bot by overriding the disallow for other
        bots
        """
        with open(
            "./tests/crawler/robot_txt/override_disallow_robots2.txt",
            "r",
            encoding="utf-8",
        ) as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt14():
        """
        Mock robots.txt file that disallows crawling for frost bot by overriding the
        allow for other bots
        """
        with open(
            "./tests/crawler/robot_txt/override_allow_robots2.txt",
            "r",
            encoding="utf-8",
        ) as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt15():
        """
        Mock robots.txt file that allows crawling for frost bot by overriding the allow for other
        bots
        """
        with open(
            "./tests/crawler/robot_txt/override_allow_with_allow_robots2.txt",
            "r",
            encoding="utf-8",
        ) as f:
            yield f.read()

    @pytest.fixture
    @staticmethod
    def mock_robots_txt16():
        """
        Mock robots.txt file that disallows crawling for frost bot by overriding the
        disallow for other bots
        """
        with open(
            "./tests/crawler/robot_txt/override_disallow_with_disallow_robots2.txt",
            "r",
            encoding="utf-8",
        ) as f:
            yield f.read()

    @staticmethod
    def test_mock_robots_txt1(mock_url, mock_robots_txt1, mock_bot_name):
        """Test mock robots.txt one"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt1, mock_bot_name)
        assert not result

    @staticmethod
    def test_mock_robots_txt2(mock_url, mock_robots_txt2, mock_bot_name):
        """Test mock robots.txt two"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt2, mock_bot_name)

        assert result

    @staticmethod
    def test_mock_robots_txt3(mock_url, mock_robots_txt3, mock_bot_name):
        """Test mock robots.txt three"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt3, mock_bot_name)

        assert result

    @staticmethod
    def test_mock_robots_txt4(mock_url, mock_robots_txt4, mock_bot_name):
        """Test mock robots.txt four"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt4, mock_bot_name)

        assert not result

    @staticmethod
    def test_mock_robots_txt5(mock_url, mock_robots_txt5, mock_bot_name):
        """Test mock robots.txt five"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt5, mock_bot_name)

        assert result

    @staticmethod
    def test_mock_robots_txt6(mock_url, mock_robots_txt6, mock_bot_name):
        """Test mock robots.txt six"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt6, mock_bot_name)

        assert not result

    @staticmethod
    def test_mock_robots_txt7(mock_url, mock_robots_txt7, mock_bot_name):
        """Test mock robots.txt seven"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt7, mock_bot_name)

        assert result

    @staticmethod
    def test_mock_robots_txt8(mock_url, mock_robots_txt8, mock_bot_name):
        """Test mock robots.txt eight"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt8, mock_bot_name)

        assert not result

    @staticmethod
    def test_mock_robots_txt9(mock_url, mock_robots_txt9, mock_bot_name):
        """Test mock robots.txt nine"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt9, mock_bot_name)
        assert not result

    @staticmethod
    def test_mock_robots_txt10(mock_url, mock_robots_txt10, mock_bot_name):
        """Test mock robots.txt ten"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt10, mock_bot_name)

        assert result

    @staticmethod
    def test_mock_robots_txt11(mock_url, mock_robots_txt11, mock_bot_name):
        """Test mock robots.txt eleven"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt11, mock_bot_name)

        assert result

    @staticmethod
    def test_mock_robots_txt12(mock_url, mock_robots_txt12, mock_bot_name):
        """Test mock robots.txt twelve"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt12, mock_bot_name)

        assert not result

    @staticmethod
    def test_mock_robots_txt13(mock_url, mock_robots_txt13, mock_bot_name):
        """Test mock robots.txt thirteen"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt13, mock_bot_name)

        assert result

    @staticmethod
    def test_mock_robots_txt14(mock_url, mock_robots_txt14, mock_bot_name):
        """Test mock robots.txt fourteen"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt14, mock_bot_name)

        assert not result

    @staticmethod
    def test_mock_robots_txt15(mock_url, mock_robots_txt15, mock_bot_name):
        """Test mock robots.txt fifteen"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt15, mock_bot_name)

        assert result

    @staticmethod
    def test_mock_robots_txt16(mock_url, mock_robots_txt16, mock_bot_name):
        """Test mock robots.txt sixteen"""
        result = _check_robots_txt.check_robots_txt(mock_url, mock_robots_txt16, mock_bot_name)

        assert not result
