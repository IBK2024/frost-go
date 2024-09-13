from os import path, rmdir

import pytest

from src.general import create_directory


@pytest.mark.parametrize(
    "directory_name",
    [
        ("test_dir_1"),  # *happy path
        ("test_dir_2"),  # *happy path
        ("nested/test_dir_3"),  # *nested directory
        ("nested/dir/with/multiple/levels"),  # *deeply nested directory
    ],
    ids=[
        "happy_path_test_dir_1",
        "happy_path_test_dir_2",
        "nested_directory_test_dir_3",
        "deeply_nested_directory",
    ],
)
def test_create_directory_happy_path(directory_name):
    # !Act
    create_directory(directory_name)

    # !Assert
    assert path.exists(directory_name)
    assert path.isdir(directory_name)

    # ! Cleanup
    rmdir(directory_name)


@pytest.mark.parametrize(
    "directory_name",
    [
        ("a" * 255),  # *maximum length directory name
        ("dir_with_special_chars_!@#$%^&*()"),  # *directory with special characters
    ],
    ids=[
        "max_length_directory_name",
        "directory_with_special_characters",
    ],
)
def test_create_directory_edge_cases(directory_name):
    # !Act
    create_directory(directory_name)

    # !Assert
    assert path.exists(directory_name)
    assert path.isdir(directory_name)

    # !Cleanup
    rmdir(directory_name)


@pytest.mark.parametrize(
    "directory_name, expected_exception",
    [
        ("./src", FileExistsError),  # *directory already exists
        ("", FileNotFoundError),  # *empty directory name
    ],
    ids=[
        "directory_already_exists",
        "empty_directory_name",
    ],
)
def test_create_directory_error_cases(directory_name, expected_exception):
    # !Act and Assert
    with pytest.raises(expected_exception):
        create_directory(directory_name)
