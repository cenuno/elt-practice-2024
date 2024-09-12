#!/usr/bin/python3

"""
Extract data from cloud and store it locally using ClientDataManager
"""

import csv
import logging
import os
from pathlib import Path

import pendulum

from data_extraction_utils import download_file, process_csv
from client_data_manager import ClientDataManager

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

# NOTE: store data source path
CLIENT_DATA_SOURCES_PATH = Path("client_data_sources.json")

logging.info("for each client, download the excel files from the cloud")

# Iterate over each relevant client
for client_name in RELEVANT_CLIENT_NAMES:
    try:
        # Initialize ClientDataManager with the client name and path to JSON data
        client_manager = ClientDataManager(
            client_name=client_name, data_path=CLIENT_DATA_SOURCES_PATH
        )

        # Check and iterate over the relevant file types for the client
        for file_type in RELEVANT_FILE_TYPES:
            if file_type in client_manager.get_file_types():
                # Retrieve files and metadata by file type
                files = client_manager.get_files_by_type(file_type)
                metadata = client_manager.get_metadata_by_file_type(file_type)

                # Extract metadata details
                metadata_columns = metadata["columns"]

                # Iterate over each file for processing
                for file in files:
                    external_filename = Path(
                        os.path.join(INPUT_DIR, file["external_filename"])
                    )
                    external_url = file["external_url"]
                    internal_filename = Path(
                        os.path.join(OUTPUT_DIR, file["internal_filename"])
                    )

                    logging.info(
                        f"inpecting if it is necessary for client {client_name} and file type {file_type}, "
                        f"downloading url {external_url} locally to {external_filename}"
                    )

                    # Download the file
                    download_file(
                        url=external_url,
                        filename=external_filename,
                        overwrite=False,
                    )

                    logging.info("inspect if we need to process the external file")

                    # Process the downloaded file
                    process_csv(
                        client_name=client_name,
                        client_id=client_manager.client_data["client_id"],
                        external_filename=external_filename,
                        internal_filename=internal_filename,
                        metadata_columns=metadata_columns,
                        sep=CSV_SEP,
                        quoting=CSV_QUOTING,
                        overwrite=False,
                    )

    except ValueError as e:
        logging.warning(f"Skipping {client_name}: {e}")

logging.info("data extraction completed")
