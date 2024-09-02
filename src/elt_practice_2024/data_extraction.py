#!/usr/bin/python3

"""
Extract data from cloud and store it locally
"""

import json
import logging
import os
from pathlib import Path

import pendulum

from client_data_manager import ClientDataManager
from data_extraction_utils import download_file

# NOTE: create log file naming convention
LOG_NOW_TIMESTAMP = pendulum.now().to_iso8601_string()
LOG_FILENAME = os.path.join("logs", f"{LOG_NOW_TIMESTAMP}_data_extraction.log")
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
# NOTE: store data source path
CLIENT_DATA_SOURCES_PATH = Path(
    os.path.join("src", "etl_practice_2024", "client_data_sources.json")
)

# NOTE: store relevant clients in a list
with open(CLIENT_DATA_SOURCES_PATH, mode="r", encoding="utf-8") as f:
    client_names = list(json.load(f).keys())

logging.info("for each client, download the excel files from the cloud")
for client_name in client_names:
    # NOTE: use custom class to handle metadata fetching
    cdm = ClientDataManager(client_name=client_name, data_path=CLIENT_DATA_SOURCES_PATH)
    for file_type in cdm.get_file_types():
        for file_name in cdm.get_file_names(file_type=file_type):
            file_data = cdm.get_file_data(file_type=file_type, file_name=file_name)
            logging.info(
                f"for client {file_data.get('client_name')}, file type {file_type}, and file name {file_name}"
                f"downloading url {file_data.get('url')} locally to {file_data.get('excel_filename')}"
            )
            download_file(
                url=file_data.get("url"),
                filename=file_data.get("excel_filename"),
                overwrite=False,
            )
