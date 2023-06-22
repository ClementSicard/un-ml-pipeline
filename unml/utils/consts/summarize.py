class SummarizationConsts:
    """
    Summarization constants
    """

    MODELS = {"DistillBART-xsum", "DistillBART-cnn"}
    SUMMARY_MIN_LENGTH = 30
    SUMMARY_MAX_TOKEN_LENGTH = 180
    DEFAULT_SUMMARIZATION_MODEL = "DistillBART-xsum"
