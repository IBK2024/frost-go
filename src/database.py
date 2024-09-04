import typing as _typing
import pymongo.database as _db
import pymongo.mongo_client as _dbClient
import pymongo.server_api as _dbServer


# !Connect to database
def database_connect(mongodb_uri: str, database_name: str) -> _db.Database[_typing.Dict[str, _typing.Any]]:
    """
    Connect to database.
    Also send a ping to confirm successful connection.
    """

    # !Create a new client and connect to the server
    client: _dbClient.MongoClient[_typing.Dict[str, _typing.Any]] = _dbClient.MongoClient(
        mongodb_uri, server_api=_dbServer.ServerApi("1")
    )

    # !Send a ping to confirm a successful connection to database
    client.admin.command("ping")
    print("Successfully connected to MongoDB!")

    # !Return client
    return client[database_name]
