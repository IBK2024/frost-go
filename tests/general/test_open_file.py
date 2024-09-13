import pytest

from src.general import open_file


@pytest.fixture
def create_test_file(tmp_path):
    def _create_test_file(file_name, file_content, encoding=None):
        file_path = tmp_path / file_name
        file_path.write_text(file_content, encoding=encoding)
        return file_path.parent, file_path.name

    return _create_test_file


@pytest.mark.parametrize(
    "file_name, file_content, encoding, expected_content",
    [
        ("test_file_utf8.txt", "Hello, World!", "utf-8", "Hello, World!"),
        ("test_file_ascii.txt", "ASCII content", "ascii", "ASCII content"),
        ("test_file_no_encoding.txt", "No encoding specified", None, "No encoding specified"),
    ],
    ids=["utf-8 encoding", "ascii encoding", "no encoding"],
)
def test_open_file_happy_path(create_test_file, file_name, file_content, encoding, expected_content):
    # Arrange
    file_location, file_name = create_test_file(file_name, file_content, encoding)

    # Act
    result = open_file(file_name, str(file_location), encoding)

    # Assert
    assert result == expected_content


@pytest.mark.parametrize(
    "file_name, file_content, encoding, expected_content",
    [
        ("empty_file.txt", "", "utf-8", ""),
        ("large_file.txt", "A" * 10**6, "utf-8", "A" * 10**6),
    ],
    ids=["empty file", "large file"],
)
def test_open_file_edge_cases(create_test_file, file_name, file_content, encoding, expected_content):
    # Arrange
    file_location, file_name = create_test_file(file_name, file_content, encoding)

    # Act
    result = open_file(file_name, str(file_location), encoding)

    # Assert
    assert result == expected_content
