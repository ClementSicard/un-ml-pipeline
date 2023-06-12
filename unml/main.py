from loguru import logger

from unml.utils.args import parse_args
from unml.utils.text import getDocumentText

if __name__ == "__main__":
    args = parse_args()
    logger.debug(f"Arguments: {args}")

    text = getDocumentText(url=args["url"])
    logger.debug(f"Text: {text}")
