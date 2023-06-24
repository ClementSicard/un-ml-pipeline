from typing import Any, Dict, List

from tqdm import tqdm

from unml.models.model import Model
from unml.utils.text import TextUtils


class RoBERTa(Model):
    """
    Class for RoBERTa (Liu et al., 2019) model
    https://arxiv.org/abs/1907.11692
    """

    MODEL_NAME = "Jean-Baptiste/roberta-large-ner-english"

    def __init__(self, modelName: str = MODEL_NAME) -> None:
        super().__init__(modelName=modelName, task="ner", aggregation_strategy="simple")

    def recognize(self, text: str) -> List[Dict[str, Any]]:
        """
        See doc for `NamedEntityRecognizer` class
        """
        return self.recognizeFromChunked(text=text)

    def recognizeFromChunked(self, text: str) -> List[Dict[str, Any]]:
        """
        Recognize named entities from text, chunking the text into smaller
        pieces to avoid hitting the max sequence length limit.

        Parameters
        ----------
        `text` : `str`
            Text to recognize named entities from.

        Returns
        -------
        `List[Dict[str, Any]]`
            List of named entities recognized from the text.
        """
        tokenizer = self.model.tokenizer

        tokens = tokenizer.tokenize(text)

        chunkedTokens = TextUtils.chunkTokens(
            tokens=tokens,
            tokenizer=tokenizer,
        )

        results = []
        for chunk in tqdm(chunkedTokens):
            chunkResults = self.model(chunk)
            results.extend(chunkResults)

        # Type casting for JSON serialization and cleaning
        for result in results:
            result["score"] = float(f'{result["score"]:.3f}')
            result["word"] = result["word"].strip()

        return results
