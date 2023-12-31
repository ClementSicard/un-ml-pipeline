from typing import Any, Dict, List, Tuple

from unml.models.ner.FLERT import FLERT
from unml.models.ner.RoBERTa import RoBERTa
from unml.models.ner.spaCy import spaCyNER
from unml.utils.consts.ner import NERConsts
from unml.utils.misc import log
from unml.utils.text import TextUtils


class NamedEntityRecognizer:
    """
    This class represents a general object to recognize named entities in text.
    """

    nerExtractor: RoBERTa | FLERT | spaCyNER

    def __init__(
        self,
        model: str = NERConsts.DEFAULT_NER_MODEL,
    ) -> None:
        parsedModel = NERConsts.ARGS_MAP[model]
        match parsedModel:
            case "RoBERTa":
                self.nerExtractor = RoBERTa()
            case "FLERT":
                self.nerExtractor = FLERT()
            case "spaCyNER":
                self.nerExtractor = spaCyNER()
            case _:
                self.nerExtractor = FLERT()

        log(
            f"NamedEntityRecognizer {parsedModel} instantiated with model {self.nerExtractor.MODEL_NAME}!",
            verbose=True,
            level="success",
        )

    def recognize(
        self,
        text: str,
        verbose: bool = False,
    ) -> Tuple[Dict[str, int], List[str], List[str], List[Dict[str, Any]]]:
        """
        Recognize named entities in a text, using chunks of tokens fed
        sequentially to the model.

        Parameters
        ----------
        `text` : `str`
            The text from which we need to extract named entities
        `verbose` : `bool`, optional
            Controls the verbose of the output, by default False

        Returns
        -------
        `Tuple[Dict[str, int], List[str], List[str], List[Dict[str, Any]]]`
            The cleaned list of named entities in the text as dictionnary with
            the entity and its frequency, the extracted countries, the extracted
            UN bodies and the detailed entities output
        """
        results = self.nerExtractor.recognize(text=text)

        cleanedEntities = self.cleanDetailedEntities(
            detailedEntities=results,
            verbose=verbose,
        )

        countries = TextUtils.extractCountries(text=text)
        bodies = TextUtils.extractUNBodies(text=text)

        log(
            f"Named entities by chunking found: {len(cleanedEntities)}:,",
            verbose=verbose,
            level="success",
        )

        # Top 10 entities
        log(
            f"Top {min(10, len(cleanedEntities)):,} entities: {list(cleanedEntities.items())[:10]}",
            verbose=verbose,
            level="info",
        )
        return cleanedEntities, countries, bodies, results

    def cleanDetailedEntities(
        self,
        detailedEntities: List[Dict[str, Any]],
        verbose: bool = False,
    ) -> Dict[str, int]:
        """
        Clean the detailed entities output from the model.

        Parameters
        ----------
        `detailedEntities` : `List[Dict[str, Any]]`
            The detailed entities output from the model
        `verbose` : `bool`, optional
            Controls the verbose of the output, by default False

        Returns
        -------
        `Dict[str, int]`
            The cleaned detailed entities output from the model,
            with the entity name and its frequency
        """
        entities: Dict[str, int] = {}
        for entity in detailedEntities:
            if entity["word"] in entities:
                entities[entity["word"]] += 1
            else:
                if TextUtils.isInvalidEntity(entity=entity["word"]):
                    continue

                elif self.initialsAreAlreadyInEntities(
                    entity=entity["word"],
                    entities=entities,
                    verbose=verbose,
                ):
                    initials = TextUtils.getInitials(entity["word"])
                    entities[initials] += 1
                else:
                    entities[entity["word"]] = 1

        # Sort the entities by their frequency
        sortedEntites = {
            k: v
            for k, v in sorted(entities.items(), key=lambda item: item[1], reverse=True)
        }

        return sortedEntites

    def initialsAreAlreadyInEntities(
        self,
        entity: str,
        entities: Dict[str, int],
        verbose: bool = False,
    ) -> bool:
        """
        Check if the initials of an entity are already in the entities dictionary.

        Parameters
        ----------
        `entity` : `str`
            The full text entity
        `entities` : `Dict[str, int]`
            The dictionnary of already-seen entities
        `verbose` : `bool`, optional
            Controls the verbose of the output, by default False

        Returns
        -------
        `bool`
            Whether or not the initials of the entity are already in the
            entities dictionary
        """
        result = False

        if len(entity.split()) > 1:
            # Get the iitials
            initials = TextUtils.getInitials(entity)
            if initials and initials in entities:
                log(
                    f"Initials {initials} already exist. Adding {entity} as {initials}",
                    level="info",
                    verbose=verbose,
                )
                result = True

        return result
