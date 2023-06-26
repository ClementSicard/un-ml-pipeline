from typing import Any, Dict, List

import spacy

from unml.models.model import Model


class spaCyNER(Model):
    """
    Class for `spaCy` NER model
    """

    MODEL_NAME = "en_core_web_trf"

    def __init__(self, modelName: str = MODEL_NAME) -> None:
        self.model = spacy.load(modelName)

    def recognize(self, text: str) -> List[Dict[str, Any]]:
        """
        See doc for `NamedEntityRecognizer` class
        """
        entities = []
        doc = self.model(text)

        for entity in doc.ents:
            entities.append(
                {
                    "entity_group": entity.label_,
                    "score": None,  # spaCy does not provide a score
                    "word": entity.text,
                    "start": entity.start_char,
                    "end": entity.end_char,
                }
            )

        return entities
