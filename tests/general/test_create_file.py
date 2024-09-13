import os
from pathlib import Path

import pytest

from src.general.create_file import create_file


@pytest.mark.parametrize(
    "file_name, file_destination, file_content, expected_file_content",
    [
        ("test1.txt", "/tmp", "Hello, World!", "Hello, World!"),  # happy path
        ("test2.txt", "/tmp", "", ""),  # empty content
        ("test3.txt", "/tmp", "1234567890", "1234567890"),  # numeric content
        ("test4.txt", "/tmp", "Special chars !@#$%^&*()", "Special chars !@#$%^&*()"),  # special characters
    ],
    ids=[
        "happy_path",
        "empty_content",
        "numeric_content",
        "special_characters",
    ],
)
def test_create_file_happy_path(file_name, file_destination, file_content, expected_file_content):
    # Act
    create_file(file_name, file_destination, file_content)

    # Assert
    with open(f"{file_destination}/{file_name}", "r", encoding="utf8") as file:
        assert file.read() == expected_file_content

    # Cleanup
    os.remove(f"{file_destination}/{file_name}")


@pytest.mark.parametrize(
    "file_name, file_destination, file_content, expected_file_content",
    [
        ("a" * 251 + ".txt", "/tmp", "Content", "Content"),  # max file name length
        ("test.txt", "/tmp", "a" * 10**6, "a" * 10**6),  # large file content
    ],
    ids=[
        "max_file_name_length",
        "large_file_content",
    ],
)
def test_create_file_edge_cases(file_name, file_destination, file_content, expected_file_content):
    # Act
    create_file(file_name, file_destination, file_content)

    # Assert
    with open(f"{file_destination}/{file_name}", "r", encoding="utf8") as file:
        assert file.read() == expected_file_content

    # Cleanup
    os.remove(f"{file_destination}/{file_name}")
