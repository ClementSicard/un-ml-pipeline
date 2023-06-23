class SummarizationConsts:
    """
    Summarization constants
    """

    MODELS = {"DistilBART-xsum", "DistilBART-cnn"}
    SUMMARY_MIN_LENGTH = 30
    SUMMARY_MAX_TOKEN_LENGTH = 180
    DEFAULT_SUMMARIZATION_MODEL = "DistilBART-xsum"
