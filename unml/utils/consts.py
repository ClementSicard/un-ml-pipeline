from pathlib import Path


class IOConsts:
    """
    IO constants
    """

    DOWNLOADS_FOLDER = Path.home() / ".unml" / "downloads"


class LoggerConsts:
    """
    Logger constants
    """

    LOGGER_LEVELS = {"debug", "info", "success", "warning", "error", "critical"}
    DEFAULT_LOGGER_LEVEL = "debug"


class ModelConsts:
    """
    Models constants
    """

    ML_TASKS = {"summarization", "automatic-speech-recognition", "ner", "translation"}


class SummarizationConsts:
    """
    Summarization constants
    """

    MODELS = {"DistillBART"}
    SUMMARY_MIN_LENGTH = 30
    SUMMARY_MAX_LENGTH = 180
    DEFAULT_SUMMARIZATION_MODEL = "DistillBART"


class NERConsts:
    """
    Named Entity Recognition constants
    """

    DEFAULT_NER_MODEL = "RoBERTa"
