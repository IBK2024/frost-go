import pytest

from src.crawler.check_robots_txt import check_robots_txt


@pytest.mark.parametrize(
    "url, robot_txt, bot_name, expected",
    [
        # Happy path tests
        ("http://example.com/page", "User-agent: *\nDisallow: /private", "mybot", True),
        ("http://example.com/private", "User-agent: *\nDisallow: /private", "mybot", False),
        ("http://example.com/page", "User-agent: mybot\nDisallow: /private", "mybot", True),
        ("http://example.com/private", "User-agent: mybot\nDisallow: /private", "mybot", False),
        # Edge cases
        ("http://example.com/", "User-agent: *\nDisallow: /", "mybot", False),
        ("http://example.com/page", "User-agent: *\nDisallow: ", "mybot", True),
        ("http://example.com/page", "User-agent: *\nDisallow: /private\nAllow: /page", "mybot", True),
        ("http://example.com/private/page", "User-agent: *\nDisallow: /private\nAllow: /private/page", "mybot", True),
        # Error cases
        ("http://example.com/page", "", "mybot", True),  # Empty robots.txt
        ("http://example.com/page", "User-agent: *\nDisallow: /private", "", True),  # Empty bot name
        ("http://example.com/page", "User-agent: *\nDisallow: /private", "unknownbot", True),  # Unknown bot name
    ],
    ids=[
        "happy_path_allowed",
        "happy_path_disallowed",
        "specific_bot_allowed",
        "specific_bot_disallowed",
        "edge_case_root_disallowed",
        "edge_case_no_disallow",
        "edge_case_allow_specific",
        "edge_case_allow_specific_in_disallowed",
        "error_case_empty_robots_txt",
        "error_case_empty_bot_name",
        "error_case_unknown_bot_name",
    ],
)
def test_check_robots_txt(url, robot_txt, bot_name, expected):

    # Act
    result = check_robots_txt(url, robot_txt, bot_name)

    # Assert
    assert result == expected
