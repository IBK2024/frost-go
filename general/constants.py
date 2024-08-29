from config.env import ENV

DATABASE_NAME = "search_engine"
MONGODB_URI = ENV["MONGODB_URI"]
TO_PARSE_DIRECTORY = "./assets/toParse"
QUEUE_COLLECTION_NAME = "queue"
