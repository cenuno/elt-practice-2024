#!/usr/bin/python3

"""
Extract data from cloud and store it locally
"""

import logging
import os
import pathlib

import pendulum

# NOTE: create app name
APP_NAME = "elt-practice-2024"

# NOTE: create log file naming convention
LOG_NOW_TIMESTAMP = pendulum.now().to_iso8601_string()
LOG_FILENAME = os.path.join("logs", f"{LOG_NOW_TIMESTAMP}_data_extraction.log")
pathlib.Path(os.path.dirname(LOG_FILENAME)).mkdir(parents=True, exist_ok=True)
LOG_ENCODING = "utf-8"
LOG_FILE_MODE = "w"
LOG_FORMATTER = {
    "format": "%(asctime).%(msecs)03d %(name)12-s %(levelname)8-s %(message)s",
    "datefmt": "%Y-%m-%dT%H:%M:%S",
}

# NOTE: setup logging
logging.basicConfig(
    filename=LOG_FILENAME,
    filemode=LOG_FILE_MODE,
    encoding=LOG_ENCODING,
    level=logging.DEBUG,
    format=LOG_FORMATTER["format"],
    datefmt=LOG_FORMATTER["datefmt"],
)

# NOTE: define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# NOTE: add the handler to the root logger
logging.getLogger("").addHandler(console)
logging.info("beginning data extraction")

# NOTE: create specific loggers to help debug
ingestion_logger = logging.getLogger(f"{APP_NAME}.data_extraction")


def download_file(url: str, filename: pathlib.Path) -> None:
    """Download a file and store it locally

    Args:
        url (str): url that contains a file hosted on the cloud
        filename (pathlib.Path): name of file

    Returns:
        None
    """
    import requests

    # NOTE: make request
    content = requests.get(url).content

    # NOTE: create the file in write binary mode, because the data we get from net is in binary
    with open(filename, "wb") as file:
        file.write(content)
