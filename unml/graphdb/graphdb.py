from typing import Any, Dict, List, Optional

from neo4j import GraphDatabase, ResultSummary
from neo4j._data import Record

from unml.utils.consts.graphdb import GraphDBConsts
from unml.utils.misc import log
from unml.utils.types.document import Document
from unml.utils.types.record import Record as UNMLRecord


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
    ) -> List[Record] | ResultSummary:
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

        self._createLinksToUNBodies(doc=doc, verbose=verbose)
        self._createLinksToSubjects(doc=doc, verbose=verbose)

    def _createLinksToSubjects(self, doc: Document, verbose: bool = False) -> None:
        """
        Create links to subjects in the GraphDB.

        Parameters
        ----------
        `doc` : `Document`
            Document to create links to subjects for
        `verbose` : `bool`, optional
            Verbose, by default `False`
        """
        if doc.subjects:
            for subject in doc.subjects:
                self.createLinkToEntity(
                    doc=doc,
                    entity=subject,
                    relationshipType="IS_ABOUT",
                    verbose=verbose,
                )
        else:
            log(
                f"Document {doc.recordId} has no subjects to link to",
                level="warning",
                verbose=verbose,
            )

    def _createLinksToUNBodies(self, doc: Document, verbose: bool = False) -> None:
        """
        Create links to UN bodies in the GraphDB.

        Parameters
        ----------
        `doc` : `Document`
            Document to create links to subjects for
        `verbose` : `bool`, optional
            Verbose, by default `False`
        """
        if doc.unBodies:
            for unBody in doc.unBodies:
                self.createLinkToEntity(
                    doc=doc,
                    entity=unBody,
                    relationshipType="REFERENCES",
                    targetKey="accronym",
                    verbose=verbose,
                )
        else:
            log(
                f"Document {doc.recordId} has no UN bodies to link to",
                level="warning",
                verbose=verbose,
            )

    def createLinkToEntity(
        self,
        doc: Document,
        entity: str,
        relationshipType: str = "IS_ABOUT",
        targetKey: str = "labelEn",
        verbose: bool = False,
    ) -> None:
        """
        Create a link to an entity in the GraphDB.

        Parameters
        ----------
        `doc` : `Document`
            Document to create link to entity for
        `entity` : `str`
            Entity to create link to
        `relationshipType` : `str`, optional
            Type of the relationship, by default `IS_ABOUT`
        `targetKey` : `str`, optional
            Key of the target node, by default `labelEn`
        `verbose` : `bool`, optional
            Verbose of the output, by default `False`
        """
        query = f"""
        MATCH (doc: Document {{ id: '{doc.recordId}' }})
        MERGE (target {{ {targetKey}: '{entity}' }})
        MERGE (doc)-[r:{relationshipType}]->(target)
        RETURN doc, r, target
        """

        self.query(query=query, verbose=verbose)

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
        summary = self.query(
            query=query,
            verbose=verbose,
            returnSummary=True,
        )

        if not isinstance(summary, ResultSummary):
            return

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

    def docExists(self, record: UNMLRecord) -> bool:
        """
        Checks if a document already exists in the GraphDB.

        Parameters
        ----------
        `record` : `UNMLRecord`
            Record to check if it exists in the GraphDB

        Returns
        -------
        `bool`
            Whether the document exists or not
        """

        query = f"""
        MATCH (doc: Document {{ id: '{record.recordId}' }})
        RETURN doc
        """

        log(f"Query: {query}", verbose=True)
        records = self.query(query=query)

        assert type(records) == list, f"Records is not a list! {type(records)}"

        return len(records) > 0
