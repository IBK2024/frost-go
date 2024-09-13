from urllib.parse import urlparse


def get_domain(url: str) -> str:
    """Gets the domain for the given url
    Args:
        url(str): The url to get domain of.

    Returns:
        str: The domain of the given url
    """
    sub_domain = urlparse(url).netloc.split(".")
    return f"{sub_domain[-2]}.{sub_domain[-1]}"
