#!/usr/bin/python3

"""
Extract data from cloud and store it locally
"""

import json
import logging
import os
from pathlib import Path

import pendulum

from utils import download_file

# NOTE: file that contains data sources
DATA_SOURCES_FILE = Path(os.path.join("src", "elt_practice_2024", "data_sources.json"))

# NOTE: create log file naming convention
LOG_NOW_TIMESTAMP = pendulum.now().to_iso8601_string()
LOG_FILENAME = os.path.join(
    "src", "elt_practice_2024", "logs", f"{LOG_NOW_TIMESTAMP}_data_extraction.log"
)
Path(os.path.dirname(LOG_FILENAME)).mkdir(parents=True, exist_ok=True)
LOG_ENCODING = "utf-8"
LOG_FILE_MODE = "w"
LOG_FORMATTER = "%(asctime)s %(name)12s %(levelname)8s %(message)s"

# NOTE: setup logging
logging.basicConfig(
    filename=LOG_FILENAME,
    filemode=LOG_FILE_MODE,
    encoding=LOG_ENCODING,
    level=logging.DEBUG,
    format=LOG_FORMATTER,
)

# NOTE: define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(logging.Formatter(LOG_FORMATTER))

# NOTE: add the handler to the root logger
logging.getLogger("").addHandler(console)
logging.info("beginning data extraction")

logging.info("import data sources config")
with open(DATA_SOURCES_FILE, mode="r", encoding="utf-8") as f:
    data_sources = json.load(f)

logging.info("for each client, download the excel files from the cloud")
excel_filenames = []
for client in data_sources.keys():
    for file_type in data_sources[client].keys():
        for file in data_sources[client][file_type]:
            excel_filename_path = Path(
                os.path.join("src", "elt_practice_2024", file["excel_filename"])
            )
            excel_filenames.append(excel_filename_path)
            logging.info(
                f"for client {client} and for file type {file_type}, "
                "downloading url {file['url']} locally to {excel_filename_path}"
            )
            download_file(
                url=file["url"], filename=excel_filename_path, overwrite=False
            )
