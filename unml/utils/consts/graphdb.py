class GraphDBConsts:
    """
    GraphDBConsts is a class that contains constants for the GraphDB handler.
    """

    # GraphDB URI, from Docker compose environment
    URI = "bolt://neo4j:7687"
    USER = None
    PASSWORD = None
    AUTH = (USER, PASSWORD)
