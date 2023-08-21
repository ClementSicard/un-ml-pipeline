import os


class GraphDBConsts:
    """
    GraphDBConsts is a class that contains constants for the GraphDB handler.
    """

    # GraphDB URI, from Docker compose environment
    BASE_URI = os.getenv("GRAPHDB_URL", "neo4j.un-semun.orb.local")
    URI = f"bolt://{BASE_URI}:7687"
    USER = None
    PASSWORD = None
    AUTH = (USER, PASSWORD)
