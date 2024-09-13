from urllib.parse import urlparse


def get_scheme(url: str) -> str:
    """Gets the domain for the given url
    Args:
        url(str): The url to get scheme of.

    Returns:
        str: The scheme of the given url
    """
    return urlparse(url).scheme
