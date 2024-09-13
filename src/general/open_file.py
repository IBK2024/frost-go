def open_file(file_name: str, file_location: str, encoding: str | None = None) -> str:
    """Open a file and return its contents as a string.

    Args:
        file_name (str): The name of the file to be opened.
        file_location (str): The directory path where the file is located.
        encoding (str|None): The encoding to be used when reading the file.

    Returns:
        str: The contents of the file as a string.
    """
    with open(f"{file_location}/{file_name}", "r", encoding=encoding) as f:
        return f.read()
