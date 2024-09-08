#!/usr/bin/python3

"""
Extract data from cloud and store it locally
"""

import csv
import json
import logging
import os
from pathlib import Path

import pendulum

from data_extraction_utils import download_file, process_csv

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
CLIENT_DATA_SOURCES_PATH = Path("client_data_sources.json")

# NOTE: store relevant client names
RELEVANT_CLIENT_NAMES = ["acme", "hooli"]

# NOTE: store relevant file types
RELEVANT_FILE_TYPES = ["membership", "claim"]

# NOTE: store relevant CSV options
CSV_SEP = "|"
CSV_QUOTING = csv.QUOTE_NONE

# NOTE: store data dir
INPUT_DIR = os.path.join("data", "input")
OUTPUT_DIR = os.path.join("data", "output")

# NOTE: store relevant clients in a list
with open(CLIENT_DATA_SOURCES_PATH, mode="r", encoding="utf-8") as f:
    client_data_sources = json.load(f)


logging.info("for each client, download the excel files from the cloud")
for relevant_client_name in RELEVANT_CLIENT_NAMES:
    for client_data in client_data_sources:
        # NOTE: store client info
        client_name = client_data["client_name"]
        client_id = client_data["client_id"]
        # NOTE: confirm this client exists and has the relevant file types
        if client_name == relevant_client_name and all(
            [
                file_type in client_data["file_types"].keys()
                for file_type in RELEVANT_FILE_TYPES
            ]
        ):
            # NOTE: for each file type
            for file_type in RELEVANT_FILE_TYPES:
                # NOTE: extract the file and metadata info
                files = client_data["file_types"][file_type]["files"]
                metadata = client_data["file_types"][file_type]["metadata"]
                # NOTE: for each file, download the excel files from the cloud
                for file in files:
                    external_filename = Path(
                        os.path.join(INPUT_DIR, file["external_filename"])
                    )
                    external_url = file["external_url"]
                    internal_filename = Path(
                        os.path.join(OUTPUT_DIR, file["internal_filename"])
                    )
                    metadata_columns = metadata["columns"]
                    schema = metadata["schema"]
                    table_name = metadata["table_name"]
                    relation = f"{schema}.{table_name}"
                    logging.info(
                        f"for client {client_name} and file type {file_type}, "
                        f"downloading url {external_url} locally to {external_filename}"
                    )
                    download_file(
                        url=external_url,
                        filename=external_filename,
                        overwrite=False,
                    )
                    logging.info("read in the external file, process it, and export it")
                    process_csv(
                        client_name=client_name,
                        client_id=client_id,
                        external_filename=external_filename,
                        internal_filename=internal_filename,
                        metadata_columns=metadata_columns,
                        sep=CSV_SEP,
                        quoting=CSV_QUOTING,
                        overwrite=False,
                    )
