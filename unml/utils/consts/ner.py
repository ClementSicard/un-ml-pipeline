class NERConsts:
    """
    Named Entity Recognition constants
    """

    MODELS = {"RoBERTa", "FLERT"}

    DEFAULT_NER_MODEL = "RoBERTa"

    ARGS_MAP = {
        "roberta": "RoBERTa",
        "flert": "FLERT",
    }
