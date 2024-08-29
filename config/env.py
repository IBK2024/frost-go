import os as _os
import typing as _typing
import dotenv as _dotenv
from config.constants import PATH_TO_ENV

# !Load env file
_dotenv.load_dotenv(PATH_TO_ENV)

# !Env object
ENV: _typing.Dict[str, str] = {"MONGODB_URI": _os.getenv("MONGODB_URI", "mongodb://localhost:27017/")}
