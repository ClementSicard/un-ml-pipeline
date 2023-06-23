class SummarizationConsts:
    """
    Summarization constants
    """

    MODELS = {"DistilBARTXSUM", "DistilBARTCNN", "DistilPegasusCNN", "LED", "LongT5"}
    SUMMARY_MIN_LENGTH = 30
    SUMMARY_MAX_TOKEN_LENGTH = 180
    DEFAULT_SUMMARIZATION_MODEL = "LED"

    ARGS_MAP = {
        "pegasus": "DistilPegasusCNN",
        "bartcnn": "DistilBARTCNN",
        "bartxsum": "DistilBARTXSUM",
        "led": "LED",
        "longt5": "LongT5",
    }
