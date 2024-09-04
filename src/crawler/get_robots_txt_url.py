from urllib.parse import urlparse


def get_robots_txt_url(url: str) -> str:
    """Gets robot.txt url for the given page"""
    scheme = urlparse(url).scheme
    sub_domain = urlparse(url).netloc.split(".")
    domain = f"{sub_domain[-2]}.{sub_domain[-1]}"

    return f"{scheme}://{domain}/robots.txt"
