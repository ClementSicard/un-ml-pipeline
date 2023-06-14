import os

DOWNLOADS_FOLDER = os.path.join(os.path.dirname(os.path.dirname(__file__)), "downloads")


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
