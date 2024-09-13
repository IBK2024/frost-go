from os import getenv
from typing import Dict

from dotenv import load_dotenv

# !Load env file
PATH_TO_ENV: str = "./env/.env"
load_dotenv(PATH_TO_ENV)

# !Env object
ENV: Dict[str, str] = {"MONGODB_URI": getenv("MONGODB_URI", "mongodb://localhost:27017/")}
