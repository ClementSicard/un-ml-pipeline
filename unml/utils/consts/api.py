from unml.utils.consts.ner import NERConsts
from unml.utils.consts.summarize import SummarizationConsts


class APIConsts:
    """
    Class for API consts
    """

    DEFAULT_PIPELINE_ARGS = {
        "summarize": True,
        "ner": True,
        "verbose": True,
        "summarizer": SummarizationConsts.DEFAULT_SUMMARIZATION_MODEL,
        "recognizer": NERConsts.DEFAULT_NER_MODEL,
    }
