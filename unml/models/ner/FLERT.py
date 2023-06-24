from typing import Any, Dict, List

from flair.data import Sentence
from flair.models import SequenceTagger

from unml.models.model import Model


class FLERT(Model):
    """
    Class for FLERT (Akbik et al., 2020) model
    https://arxiv.org/abs/2011.06993
    """

    MODEL_NAME_SMALL = "flair/ner-english-fast"
    MODEL_NAME_LARGE = "flair/ner-english-large"

    def __init__(self, modelName: str = MODEL_NAME_SMALL) -> None:
        self.model = SequenceTagger.load(modelName)

    def recognize(self, text: str) -> List[Dict[str, Any]]:
        """
        See doc for `NamedEntityRecognizer` class
        """
        entities = []
        sentence = Sentence(text)

        self.model.predict(sentence)

        for entity in sentence.get_spans("ner"):
            entities.append(
                {
                    "entity_group": entity.tag,
                    "score": entity.score,
                    "word": entity.text,
                    "start": entity.start_position,
                    "end": entity.end_position,
                }
            )

        return entities
