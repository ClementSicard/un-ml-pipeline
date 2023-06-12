from argparse import ArgumentParser
from typing import Any, Dict


def parse_args() -> Dict[str, Any]:
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", type=str, required=True)
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
    )
    return vars(parser.parse_args())
