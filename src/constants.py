from .config.env import ENV

DATABASE_NAME = "search_engine"
MONGODB_URI = ENV["MONGODB_URI"]
TO_PARSE_DIRECTORY = "./assets/toParse"
MAX_NUMBER_OF_THREADS = 10
DEFAULT_STARTING_LINK = "https://www.wikipedia.org/"
