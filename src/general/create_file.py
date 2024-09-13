def create_file(file_name: str, file_destination: str, file_content: str) -> None:
    """Creates a file with the specified name and writes content to it.

    Args:
        file_name(str): The name of the file to be created.
        file_destination(str): The directory where the file will be stored.
        file_content(str): The content to be written to the file.

    Returns:
        None
    """
    with open(f"{file_destination}/{file_name}", "w", encoding="utf8") as file:
        file.write(file_content)
