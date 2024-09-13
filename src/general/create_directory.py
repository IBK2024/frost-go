from os import makedirs


# !Create a directory
def create_directory(directory_name: str) -> None:
    """Creates directory
    Args:
        directory_name(str): The name of the directory to be created.

    Returns:
        None
    """
    makedirs(directory_name)
