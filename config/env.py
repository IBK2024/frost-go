from os import getenv
from typing import Dict
from dotenv import load_dotenv
from config.constants import PATH_TO_ENV

# !Load env file
load_dotenv(PATH_TO_ENV)

# !Env object
ENV: Dict[str, str] = {
    "MONGODB_URI": getenv("MONGODB_URI", "mongodb://localhost:27017/")
}
