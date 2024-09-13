from typing import Any, Dict

import pymongo.database as _db
import pymongo.mongo_client as _dbClient
import pymongo.server_api as _dbServer


# !Connect to database
def database_connect(mongodb_uri: str, database_name: str) -> _db.Database[Dict[str, Any]]:
    """Connects to the database and sends a ping for confirmation successful connection

    Args:
        mongodb_uri (str): Url to the mongodb database cluster
        database_name (str): Name of the database

    Returns:
        _db.Database[Dict[str, Any]]: The database class
    """
    # !Create a new client and connect to the server
    client: _dbClient.MongoClient[Dict[str, Any]] = _dbClient.MongoClient(
        mongodb_uri, server_api=_dbServer.ServerApi("1")
    )

    # !Send a ping to confirm a successful connection to database
    client.admin.command("ping")
    print("Successfully connected to MongoDB!")

    # !Return client
    return client[database_name]
