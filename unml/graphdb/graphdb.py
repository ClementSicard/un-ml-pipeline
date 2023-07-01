from typing import Any, Dict, List, Optional

from neo4j import EagerResult, GraphDatabase
from neo4j._data import Record

from unml.utils.consts.graphdb import GraphDBConsts
from unml.utils.misc import log
from unml.utils.types.document import Document


class GraphDB:
    """
    GraphDB class is a class that handles the connection to a `neo4j` GraphDB.
    """

    _instance: Optional["GraphDB"] = None

    def __new__(cls) -> "GraphDB":
        """
        GraphDB constructor to ensure singleton pattern.

        Returns
        -------
        `GraphDB`
            The GraphDB instance
        """
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls)
            log("Created a new GraphDB instance", level="info", verbose=True)

        return cls._instance

    def __init__(self) -> None:
        """
        GraphDB constructor
        """
        self.URI = GraphDBConsts.URI
        self.AUTH = GraphDBConsts.AUTH
        self.driver = GraphDatabase.driver(self.URI, auth=self.AUTH)

    def __del__(self) -> None:
        """
        GraphDB destructor: when object gets destroyed, close the driver
        """
        self.driver.close()

    def query(
        self,
        query: str,
        params: Optional[Dict[str, Any]] = None,
        returnSummary: bool = False,
        verbose: bool = False,
    ) -> List[Record] | EagerResult:
        """
        Execute a query on the GraphDB.

        Parameters
        ----------
        `query` : `str`
            Query to execute
        `params` : `Optional[Dict[str, Any]]`, optional
            Parameters of the query to be replaced, by default `None`
        `returnSummary` : `bool`, optional
            Return the summary or not. If `True`, returns the summary,
            otherwise returns the records, by default `False`
        `verbose` : `bool`, optional
            Controls the verbose of the output, by default `False`

        Returns
        -------
        `List[Record] | EagerResult`
            List of records returned by the query
        """
        querySummary = self.driver.execute_query(
            query_=query,
            parameters_=params,
        )

        records, summary, _ = querySummary

        log(
            "The query `{query}` returned {records_count} records in {time} ms.".format(
                query=summary.query,
                records_count=len(records),
                time=summary.result_available_after,
            ),
            verbose=verbose,
        )

        return summary if returnSummary else records

    def _createLinksToEntities(self, doc: Document, verbose: bool = False) -> None:
        """
        Creates links to entities in the GraphDB.

        Parameters
        ----------
        `doc` : `Document`
            Document to create links to entities for
        `verbose` : `bool`, optional
            Verbose of the output, by default `False`
        """
        log("Not implemented yet", verbose=verbose, level="error")
        pass

    def createDocument(self, doc: Document, verbose: bool = False) -> None:
        """
        Create a document in the GraphDB using `Document` class function
        `toGraphDBObject()` to convert the document to the body a Cypher query.

        Parameters
        ----------
        `doc` : `Document`
            Document to create
        `verbose` : `bool`, optional
            Controls the output verbose, by default `False`
        """
        query = f"""
        MERGE ({doc.toGraphDBObject()})
        """
        summary: EagerResult = self.query(
            query=query,
            verbose=verbose,
            returnSummary=True,
        )

        log(
            f"Created {summary.counters.nodes_created} document(s) in"
            + f" {summary.result_available_after} ms.",
            verbose=verbose,
        )

        self._createLinksToEntities(doc=doc, verbose=verbose)

    def checkConnection(self) -> None:
        """
        Check if the connection to the GraphDB is successful.

        Raises
        ------
        `ConnectionError`
            If the connection is not successful
        """
        try:
            self.driver.verify_connectivity()
        except Exception as e:
            raise ConnectionError(
                f"Could not connect to the GraphDB at {self.URI} with auth {self.AUTH}"
            ) from e
