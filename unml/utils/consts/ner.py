class NERConsts:
    """
    Named Entity Recognition constants
    """

    MODELS = {"RoBERTa", "FLERT", "spaCyNER"}

    DEFAULT_NER_MODEL = "spacy"

    ARGS_MAP = {
        "roberta": "RoBERTa",
        "flert": "FLERT",
        "spacy": "spaCyNER",
    }
