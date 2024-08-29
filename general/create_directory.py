from os import makedirs as _makedirs


# !Create a directory
def create_directory(directory_name: str) -> None:
    """Creates directory"""
    _makedirs(directory_name)
