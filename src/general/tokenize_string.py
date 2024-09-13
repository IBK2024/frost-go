import string as _str
from collections import Counter
from typing import Dict

from .constants import HTML_BLACKLIST, STOP_WORDS


def tokenize_string(string: str) -> Dict[str, int]:
    """Tokenizes the given string

    Args:
        string(str): The string to tokenize.

    Returns:
        Dict[str,int]: Dictionary of words and number of occurrences
    """
    # !Remove punctuation
    text = string.translate(str.maketrans("", "", _str.punctuation))

    # !Split the string into a list of words
    tokens = text.split()

    # !Remove blacklist tags
    tokens = [word for word in tokens if word not in HTML_BLACKLIST]

    # !Remove stop words
    tokens = [word for word in tokens if word not in STOP_WORDS]

    # !Return count of words
    return dict(Counter(tokens))
