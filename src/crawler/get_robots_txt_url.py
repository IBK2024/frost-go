from ..general import get_domain, get_scheme


def get_robots_txt_url(url: str) -> str:
    """
    Constructs the URL for the robots.txt file based on the provided URL.

    Args:
        url (str): The URL from which to extract the scheme and domain.

    Returns:
        str: The constructed URL for the robots.txt file.
    """

    scheme = get_scheme(url)
    domain = get_domain(url)

    return f"{scheme}://{domain}/robots.txt"
