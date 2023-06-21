from pathlib import Path

DOWNLOADS_FOLDER = Path.home() / ".unml" / "downloads"


"""
Logger
"""
LOGGER_LEVELS = {"debug", "info", "success", "warning", "error", "critical"}
DEFAULT_LOGGER_LEVEL = "debug"


"""
Models
"""
ML_TASKS = {"summarization", "automatic-speech-recognition", "ner", "translation"}

"""
Summarization
"""
SUMMARY_MIN_LENGTH = 30
SUMMARY_MAX_LENGTH = 180
DEFAULT_SUMMARIZATION_MODEL = "distillbart"
